def screen_resume(cleaned_text: str, skill_categories: dict):
    total_score = 0
    breakdown = {}
    matched_skills = []
    missing_skills = []

    for category, data in skill_categories.items():
        skills = data["skills"]
        weight = data["weight"]

        matched = [s for s in skills if s in cleaned_text]
        missing = [s for s in skills if s not in cleaned_text]

        category_score = 0

        if skills:
            category_score = int((len(matched) / len(skills)) * weight)

        breakdown[category] = {
            "score": category_score,
            "matched": matched,
            "missing": missing
        }

        total_score += category_score
        matched_skills.extend(matched)
        missing_skills.extend(missing)

        return {
            "total_score": total_score,
            "breakdown": breakdown,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }
