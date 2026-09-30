import sys
import os

# Add the backend directory to path
sys.path.append('c:/CV_Sir/backend')

from career_scorer import classify_job_level

def test():
    test_cases = [
        # (Score, Exp, IsTarget, Expected)
        (20, 10, True, "Senior (Expert)"),    # Target: Seniority Floor wins
        (20, 10, False, "Not Job Ready"),     # Non-Target: Score wins (20 < 50)
        (90, 0, True, "Strong Mid"),         # Target: High skill boosts level
        (90, 0, False, "Junior"),            # Non-Target: Capped at Junior
        (66, 0, False, "Entry Level"),       # Non-Target: 66% matches Entry Level
        (55, 0, False, "Internship"),        # Non-Target: 55% matches Internship
        (80, 8, True, "Senior"),             # Target: Senior Floor
        (80, 8, False, "Junior"),            # Non-Target: Skill match 80% is Junior
    ]

    print(f"{'Score':<6} | {'Exp':<4} | {'Target':<6} | {'Result'}")
    print("-" * 50)
    for score, exp, is_target, expected in test_cases:
        result = classify_job_level(score, exp, is_target_role=is_target)
        status = "PASS" if result == expected else f"FAIL (Expected {expected})"
        print(f"{score:<6} | {exp:<4} | {str(is_target):<6} | {result:<20} {status}")

if __name__ == "__main__":
    test()
