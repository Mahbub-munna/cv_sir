import re

def is_valid_resume(text: str) -> bool:
    """
    Checks if the provided text looks like a CV/Resume based on:
    - Keywords (Experience, Education, Skills, etc.)
    - Contact Info patterns (Email)
    - Minimum length
    """

    if not text or len(text.strip()) < 100:
        return False

    # Common resume headers
    headers = [
        "experience", "work history", "employment", 
        "education", "qualification", "academic",
        "skills", "technical summary", "core competencies",
        "projects", "achievements", "certifications",
        "objective", "summary", "profile", "curriculum vitae"
    ]

    text_lower = text.lower()
    
    # Check for at least 3 keywords
    keyword_count = sum(1 for h in headers if h in text_lower)
    
    # Check for email pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    has_email = bool(re.search(email_pattern, text))

    # Basic resume detection logic:
    # Most resumes have an email and at least 2 distinct section headers.
    if has_email and keyword_count >= 2:
        return True
    
    # If no email, check for a higher keyword count (maybe a private CV)
    if keyword_count >= 4:
        return True

    return False
