# job_matching/matcher.py

from typing import Dict, List
from job_matching.job_schema import Job


def match_resume_to_job(
    resume_skills: Dict[str, List[str]],
    job: Job
) -> Dict:
    """
    Matches a resume against a single job definition.
    Returns match score, matched skills, missing skills, and explanation.
    """

    total_score = 0.0
    matched_skills = {}
    missing_skills = {}

    for category, required_skills in job.required_skills.items():
        resume_category_skills = resume_skills.get(category, [])

        matched = list(set(resume_category_skills) & set(required_skills))
        missing = list(set(required_skills) - set(resume_category_skills))

        matched_skills[category] = matched
        missing_skills[category] = missing

        if required_skills:
            match_ratio = len(matched) / len(required_skills)
        else:
            match_ratio = 1.0  # no requirement → full match

        weight = job.category_weights.get(category, 0)
        total_score += match_ratio * weight

    final_score = round(total_score * 100, 2)

    explanation = generate_explanation(job.title, final_score, missing_skills)

    return {
        "job_id": job.job_id,
        "title": job.title,
        "match_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "explanation": explanation
    }


def generate_explanation(
    job_title: str,
    match_score: float,
    missing_skills: Dict[str, List[str]]
) -> str:
    """
    Rule-based explanation of job match quality.
    """

    if match_score >= 75:
        fit = "strong match"
    elif match_score >= 50:
        fit = "moderate match"
    else:
        fit = "weak match"

    gaps = [
        skill
        for skills in missing_skills.values()
        for skill in skills
    ]

    if gaps:
        gap_text = f" Missing skills: {', '.join(gaps)}."
    else:
        gap_text = " No major skill gaps detected."

    return f"{job_title} is a {fit} for this candidate.{gap_text}"
