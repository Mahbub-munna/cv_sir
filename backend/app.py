from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import re
from pymongo import MongoClient
import traceback
import sys

from resume_parser import extract_text
from skill_extractor import extract_skills
from jd_scorer import compare_resume_with_jd
from roles import JOB_ROLES
from scorer import calculate_score
from career_scorer import calculate_career_readiness, classify_job_level
from job_recommender import build_external_links
from resume_validator import is_valid_resume
from skill_encyclopedia import get_skill_info


# -----------------------------------
# FastAPI App Initialization
# -----------------------------------
app = FastAPI()

# -----------------------------------
# Environment & Database Setup
# -----------------------------------
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

if not MONGODB_URI or not JWT_SECRET:
    print("WARNING: MONGODB_URI or JWT_SECRET is missing from .env")

try:
    client = MongoClient(MONGODB_URI)
    db = client.get_database() # Uses the DB specified in the URI
    users_collection = db.users
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# -----------------------------------
# Auth Models and Utils
# -----------------------------------
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = parts[1]
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# -----------------------------------
# Auth Endpoints
# -----------------------------------
@app.post("/register")
async def register(user: UserRegister):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
        
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = hash_password(user.password)
    new_user = {
        "full_name": user.full_name,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }
    users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "email": user.email, 
        "full_name": db_user.get("full_name", "")
    }



# -----------------------------------
# CORS Configuration (FIXED)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://ridyana.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Upload Directory Setup
# -----------------------------------
UPLOAD_RESUME_DIR = "uploads/resumes"
os.makedirs(UPLOAD_RESUME_DIR, exist_ok=True)


# -----------------------------------
# File Validation
# -----------------------------------
def validate_file_type(filename: str):
    allowed_extensions = (".pdf", ".docx")
    if not filename.lower().endswith(allowed_extensions):
        raise ValueError("Only PDF and DOCX files are allowed.")


# -----------------------------------
# ANALYZE ENDPOINT
# -----------------------------------
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description_text: str | None = Form(None),
    target_role: str = Form(...),
    experience_years: float = Form(0),
    projects: int = Form(0),
    current_user: str = Depends(get_current_user)
):

    try:

        # -----------------------------------
        # Validate & Save Resume
        # -----------------------------------
        validate_file_type(resume.filename)

        file_extension = os.path.splitext(resume.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        resume_path = os.path.join(UPLOAD_RESUME_DIR, unique_filename)

        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        # -----------------------------------
        # Extract Resume Text
        # -----------------------------------
        resume_text = extract_text(resume_path)
        
        # -----------------------------------
        # RESUME VALIDATION
        # -----------------------------------
        if not is_valid_resume(resume_text):
            os.remove(resume_path)
            raise HTTPException(
                status_code=400, 
                detail="The uploaded file does not appear to be a valid resume. Please upload a CV/Resume (PDF or DOCX)."
            )

        resume_skills = list(set(extract_skills(resume_text)))

        os.remove(resume_path)

        response = {
            "target_role": target_role,
            "resume_skills": resume_skills
        }

        # -----------------------------------
        # ANALYSIS SOURCE SELECTION (JD vs. ROLE)
        # -----------------------------------
        jd_provided = bool(job_description_text and job_description_text.strip())
        role_data = JOB_ROLES.get(target_role)

        if jd_provided:
            # -----------------------------------
            # SPECIFIC MODE: CV vs. JOB DESCRIPTION
            # -----------------------------------
            role_info = role_data if role_data else {}
            core_skills_for_validation = role_info.get("core_skills", [])
            
            # 1. Validation Logic
            target_role_lower = target_role.lower()
            jd_text_lower = job_description_text.lower()
            role_phrase_match = target_role_lower in jd_text_lower
            role_keywords = [w for w in target_role_lower.split() if len(w) > 2]
            role_keyword_match = any(w in jd_text_lower for w in role_keywords) if role_keywords else False
            skill_overlap_count = sum(1 for s in core_skills_for_validation if s.lower() in jd_text_lower)
            
            if not(role_phrase_match or role_keyword_match) and skill_overlap_count < 2:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Mismatched Information",
                        "message": f"The provided Job Description does not appear to match your target role: {target_role}. Please provide a relevant JD or check your role selection."
                    }
                )

            # 2. Skill Comparison (Strictly with JD)
            jd_skills = list(set(extract_skills(job_description_text)))
            jd_score, jd_matched, jd_missing = compare_resume_with_jd(
                resume_skills,
                jd_skills
            )

            # 3. Primary Metrics from JD
            primary_match_percentage = float(jd_score)
            primary_missing_skills = jd_missing
            primary_extra_skills = [
                s for s in resume_skills if s not in jd_skills
            ]

            # 4. Career Readiness (Driving from JD score)
            specific_readiness, _ = calculate_career_readiness(
                resume_skills,
                experience_years,
                projects,
                role_data if role_data else {},
                is_target_role=True,
                provided_skill_score=float(jd_score)
            )

            response.update({
                "job_description_skills": jd_skills,
                "role_match_percentage": primary_match_percentage,
                "role_missing_skills": primary_missing_skills,
                "role_extra_skills": primary_extra_skills,
                "specific_job_readiness": float(specific_readiness),
                "specific_job_level": classify_job_level(specific_readiness, experience_years, is_target_role=True),
                "jd_match_percentage": float(jd_score), # To signal JD was used
            })

        else:
            # -----------------------------------
            # GENERAL MODE: CV vs. PREDEFINED ROLE
            # -----------------------------------
            if role_data:
                role_match_percentage = calculate_score(resume_skills, role_data)
                core_skills = role_data.get("core_skills", [])
                secondary_skills = role_data.get("secondary_skills", [])
                all_role_skills = set(core_skills + secondary_skills)

                primary_match_percentage = float(role_match_percentage)
                primary_missing_skills = [s for s in all_role_skills if s not in resume_skills]
                primary_extra_skills = [s for s in resume_skills if s not in all_role_skills]
            else:
                primary_match_percentage = 0.0
                primary_missing_skills = []
                primary_extra_skills = []

            response.update({
                "role_match_percentage": primary_match_percentage,
                "role_missing_skills": primary_missing_skills,
                "role_extra_skills": primary_extra_skills,
                "jd_match_percentage": None, # Signal NO JD
                "specific_job_readiness": None
            })

        # -----------------------------------
        # ROLE RANKING CHART (Still useful for context)
        # -----------------------------------
        role_results = {}
        for r_name, r_data in JOB_ROLES.items():
            s = calculate_score(resume_skills, r_data)
            if s > 0: role_results[r_name] = float(s)

        response["role_matches"] = dict(
            sorted(role_results.items(), key=lambda x: x[1], reverse=True)
        )

        # -----------------------------------
        # CAREER PROFILE (Keep for general context)
        # -----------------------------------
        career_profile = {}
        for r_name, r_data in JOB_ROLES.items():
            score, breakdown = calculate_career_readiness(
                resume_skills,
                experience_years,
                projects,
                r_data,
                is_target_role=(r_name == target_role)
            )

            career_profile[r_name] = {
                "score": float(score),
                "level": classify_job_level(score, experience_years, is_target_role=(r_name == target_role)),
                "breakdown": breakdown
            }

        response["career_profile"] = career_profile

        return JSONResponse(content=response)

    except ValueError as ve:

        return JSONResponse(
            status_code=400,
            content={"error": str(ve)}
        )

    except Exception as e:
        # Print the full traceback to the console for debugging
        print("CRITICAL: Internal Server Error occurred in /analyze")
        traceback.print_exc(file=sys.stdout)

        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend processing failed",
                "message": str(e),
                "type": type(e).__name__
            }
        )


# -----------------------------------
# JOB RECOMMENDATION ENDPOINT
# -----------------------------------
@app.post("/job-recommendations")
async def job_recommendations(
    role: str = Form(...), 
    level: str = Form(...),
    current_user: str = Depends(get_current_user)
):

    try:

        links_data = build_external_links(role, level)

        return JSONResponse(content={
            "job_queries": links_data["job_queries"],
            "external_links": {
                "linkedin": links_data["linkedin"],
                "indeed": links_data["indeed"]
            }
        })

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": "Job recommendation failed",
                "message": str(e)
            }
        )

# -----------------------------------
# SKILL INFO ENDPOINT
# -----------------------------------
@app.get("/skill-info/{skill_name}")
async def skill_info_endpoint(
    skill_name: str, 
    current_user: str = Depends(get_current_user)
):
    return get_skill_info(skill_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)