
from scorer import calculate_score


# -----------------------------------
# Helper: Normalize Score
# -----------------------------------
def _normalize_score(value, max_value):
    """
    Normalize value against max_value into 0–100 scale.
    Caps at 100.
    """
    if max_value <= 0:
        return 0.0
        
    percentage = (value / max_value) * 100.0
    return min(percentage, 100.0)


# -----------------------------------
# Career Readiness Calculator
# -----------------------------------
def calculate_career_readiness(
    resume_skills,
    experience_years,
    projects,
    role_data,
    is_target_role=False,
    provided_skill_score=None
):
    
    """
    Calculates career readiness score using weighted components:

    Skills        → 40%
    Experience    → 40%
    Projects      → 10%
    Education     → 5%
    ATS Quality   → 5%
    """

    # -----------------------------
    # 1. Skill Score (Weighted Core + Secondary)
    # -----------------------------
    if provided_skill_score is not None:
        skills_score = provided_skill_score
    else:
        skills_score = calculate_score(resume_skills, role_data)

    # -----------------------------
    # 2. Relevance Multiplier (Logic Fix)
    # -----------------------------
    # For any role that is NOT the user-applied target role, 
    # we scale experience/projects by the skill match %.
    # 0% skill match = 0% relevancy for experience/projects.
    relevance_multiplier = 1.0 if is_target_role else (skills_score / 100.0)

    # -----------------------------
    # 3. Experience Score
    # -----------------------------
    experience_target_years = role_data.get("experience_target_years", 5)

    experience_score = _normalize_score(
        experience_years,
        experience_target_years
    ) * relevance_multiplier

    # -----------------------------
    # 4. Projects Score
    # -----------------------------
    projects_target_count = role_data.get("projects_target_count", 4)

    projects_score = _normalize_score(
        projects,
        projects_target_count
    ) * relevance_multiplier


    # -----------------------------
    # 4. Education & ATS (Optional Role Metadata)
    # -----------------------------
    education_score = float(role_data.get("education_score", 0.0))
    ats_score = float(role_data.get("ats_score", 0.0))

    # -----------------------------
    # 5. Final Weighted Score (Context-Aware Logic)
    # -----------------------------
    if skills_score == 0:
        overall_score = 0.0
    else:
        if is_target_role:
            # TARGET ROLE MODE: Prioritize Experience over Projects
            # Skills (40%) | Experience (40%) | Projects (10%) | Education (5%) | ATS (5%)
            overall_score = round(
                (skills_score * 0.40)
                + (experience_score * 0.40)
                + (projects_score * 0.10)
                + (education_score * 0.05)
                + (ats_score * 0.05),
                2,
            )
        else:
            # NORMAL MODE (Other Roles): Pure Skill Match
            # For general recommendations, we ignore the target role's experience/projects.
            overall_score = round(skills_score, 2)

    breakdown = {
        "skills_score": round(skills_score, 2),
        "experience_score": round(experience_score, 2),
        "projects_score": round(projects_score, 2),
        "education_score": round(education_score, 2),
        "ats_score": round(ats_score, 2),
        "calculation_mode": "Target (Weighted)" if is_target_role else "Normal (Skill-Only)"
    }

    return overall_score, breakdown



# -----------------------------------
# Job Level Classification (Seniority Floor Logic)
# -----------------------------------
def classify_job_level(score, experience_years, is_target_role=False):
    """
    Classify job level based on overall career readiness score AND years of experience.
    Ensures experienced users are not suggested entry-level roles for target jobs,
    while general recommendations remain strictly skill-based.
    """

    if not is_target_role:
        # RECOMMENDATION MODE: Pure Skill Match Tiers
        # Since we don't have experience records for these "other" roles, 
        # we cap them at Junior to remain logical.
        if score >= 80:
            return "Junior"
        elif score >= 65:
            return "Entry Level"
        elif score >= 50:
            return "Internship"
        else:
            return "Not Job Ready"

    # 1. Base classification based on skills/projects score (Target Role)
    score_level = "Not Job Ready"
    if score >= 95:
        score_level = "Senior"
    elif score >= 85:
        score_level = "Strong Mid"
    elif score >= 70:
        score_level = "Mid"
    elif score >= 50:
        score_level = "Junior"
    elif score >= 30:
        score_level = "Internship"


    # 2. Seniority Floor based on years of experience
    # If you have 10 years experience, you are a Senior, even if skills match is low.
    experience_floor = "Not Job Ready"
    if experience_years >= 10:
        experience_floor = "Senior (Expert)"
    elif experience_years >= 7:
        experience_floor = "Senior"
    elif experience_years >= 5:
        experience_floor = "Mid-Senior"
    elif experience_years >= 3:
        experience_floor = "Mid-Level"
    elif experience_years >= 2:
        experience_floor = "Junior"
    elif experience_years >= 1:
        experience_floor = "Internship"


    # Define level hierarchy to pick the highest floor
    levels = ["Not Job Ready", "Internship", "Entry Level", "Junior", "Mid", "Mid-Level", "Mid-Senior", "Strong Mid", "Senior", "Senior (Expert)"]
    
    score_idx = levels.index(score_level) if score_level in levels else 0
    exp_idx = levels.index(experience_floor) if experience_floor in levels else 0

    # Pick the highest floor
    final_idx = max(score_idx, exp_idx)
    return levels[final_idx]