# ai_layer/job_ai_engine.py

from ai_layer.job_prompts import JOB_SYSTEM_PROMPT, JOB_INSIGHT_PROMPT


class JobAIEngine:
    """
    AI layer for explaining job recommendations.
    """

    def generate_job_insights(self, job_match: dict) -> dict:
        """
        Mocked AI insights for a single job match.
        """

        matched = [
            skill
            for skills in job_match["matched_skills"].values()
            for skill in skills
        ]

        missing = [
            skill
            for skills in job_match["missing_skills"].values()
            for skill in skills
        ]

        if job_match["match_score"] >= 70:
            fit = "strong alignment"
        elif job_match["match_score"] >= 50:
            fit = "reasonable alignment"
        else:
            fit = "partial alignment"

        return {
            "fit_reason": (
                f"This role shows {fit} based on your experience with "
                f"{', '.join(matched) if matched else 'basic technical skills'}."
            ),
            "skill_gaps": missing,
            "improvement_advice": (
                "Focus on strengthening "
                f"{', '.join(missing)}." if missing
                else "Maintain and deepen your existing skill set."
            )
        }
