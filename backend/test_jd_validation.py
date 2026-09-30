import sys
import os

# Add the backend directory to path
sys.path.append('c:/CV_Sir/backend')

from roles import JOB_ROLES

def is_jd_relevant_to_role(jd_text, target_role):
    """
    Simulating the logic added in app.py for validation.
    """
    role_info = JOB_ROLES.get(target_role, {})
    core_skills = role_info.get("core_skills", [])
    
    role_match = target_role.lower() in jd_text.lower()
    skill_overlap = sum(1 for s in core_skills if s.lower() in jd_text.lower())
    
    # Validation logic from app.py
    return role_match or skill_overlap >= 2

def test():
    test_cases = [
        # (JD Text, Target Role, Expected)
        ("Senior Python Developer with AWS and SQL experience", "Backend Developer", True), # Skill overlap (Python, REST API, SQL -> 2+)
        ("Sales Manager for real estate", "Backend Developer", False), # No role match, no skill overlap
        ("Frontend Engineer with React and Javascript", "Frontend Developer", True), # Role match
        ("Marketing expert in social media", "Data Analyst", False), # No match
        ("Junior Data Analyst using SQL and Pandas", "Data Analyst", True), # Role match
        ("Professional using statistics and data cleaning", "Data Analyst", True), # Skill overlap (Statistics, Data Cleaning)
    ]

    print(f"{'Target Role':<20} | {'Relevant?':<10} | {'Status'}")
    print("-" * 50)
    for jd, role, expected in test_cases:
        result = is_jd_relevant_to_role(jd, role)
        status = "PASS" if result == expected else "FAIL"
        print(f"{role:<20} | {str(result):<10} | {status}")

if __name__ == "__main__":
    test()
