def screen_resume(cleaned_text: str, required_skills: list):
    matched = []
    missing = []

    for skill in required_skills:
        if skill in cleaned_text:
            matched.append(skill)
        else:
            missing.append(skill)

    #simple scoreing logic 
    score = int((len(matched) / len(required_skills)) * 100)

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }