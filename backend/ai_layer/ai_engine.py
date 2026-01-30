# ai_layer/ai_engine.py

from ai_layer.schemas import ResumeAnalysisInput, AIInsightOutput
from ai_layer import prompts


class AIEngine:
    """
    AI interpretation layer.
    This class NEVER modifies scores or logic.
    """

    def __init__(self, client=None):
        # client will later be OpenAI / LLM client
        self.client = client

    def generate_insights(self, data: ResumeAnalysisInput) -> AIInsightOutput:
        """
        Main entry point for AI insights.
        """

        # ---- MOCKED AI RESPONSE (for now) ----
        strengths = self._mock_strengths(data)
        weaknesses = self._mock_weaknesses(data)
        summary = self._mock_summary(data)

        return AIInsightOutput(
            strengths=strengths,
            weaknesses=weaknesses,
            profile_summary=summary
        )

    # -----------------------------
    # Mock logic (temporary)
    # -----------------------------

    def _mock_strengths(self, data: ResumeAnalysisInput):
        strengths = []

        if data.matched_skills.get("languages"):
            strengths.append(
                f"Proficient in {', '.join(data.matched_skills['languages'])} for backend development."
            )

        if data.matched_skills.get("frameworks"):
            strengths.append(
                f"Hands-on experience with frameworks like {', '.join(data.matched_skills['frameworks'])}."
            )

        if not strengths:
            strengths.append("Limited detectable technical strengths based on current resume.")

        return strengths

    def _mock_weaknesses(self, data: ResumeAnalysisInput):
        weaknesses = []

        for category, skills in data.missing_skills.items():
            if skills:
                weaknesses.append(
                    f"Lack of exposure to {', '.join(skills)} in {category.replace('_', ' ')}."
                )

        if not weaknesses:
            weaknesses.append("No major technical gaps detected.")

        return weaknesses

    def _mock_summary(self, data: ResumeAnalysisInput):
        total_score = data.scores.get("total", 0)

        if total_score >= 70:
            level = "strong junior to mid-level candidate"
        elif total_score >= 40:
            level = "entry-level candidate"
        else:
            level = "early-stage candidate"

        return (
            f"{level.capitalize()} with a backend-oriented profile. "
            f"Demonstrates practical development experience but requires improvement in foundational areas."
        )
