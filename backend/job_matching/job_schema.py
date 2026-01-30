# job_matching/job_schema.py

from typing import Dict, List
from pydantic import BaseModel


class Job(BaseModel):
    """
    Represents a single job role and its requirements.
    """

    job_id: str
    title: str
    description: str

    # Required skills grouped by category
    required_skills: Dict[str, List[str]]

    # Weight of each category for this job (must sum to 1.0)
    category_weights: Dict[str, float]
