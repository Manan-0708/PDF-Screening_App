from typing import List, Dict, Any
from pydantic import BaseModel

class ResumeAnalysisInput(BaseModel):
    resume_text: str
    scores: Dict[str, int]
    matched_skills: Dict[str, List[str]]
    missing_skills: Dict[str, List[str]]

class AIInsightOutput(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    profile_summary: str