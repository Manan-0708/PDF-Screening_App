from fastapi import FastAPI, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
from pydantic import BaseModel

import os
import shutil

# ------------------------
# Internal Imports
# ------------------------
from text_utils import clean_text
from screening import screen_resume
from keywords import SKILL_CATEGORIES
from chatbot import generate_response, answer_question

from ai_layer.ai_engine import AIEngine
from ai_layer.schemas import ResumeAnalysisInput

from job_matching.job_data import JOB_LIST
from job_matching.matcher import match_resume_to_job


# ------------------------
# App Setup
# ------------------------
app = FastAPI(title="Resume Intelligence API")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Instantiate AI engine once (clean lifecycle)
ai_engine = AIEngine()


# ------------------------
# Helpers
# ------------------------
def normalize_skills(skills):
    """
    Ensures skills are in Dict[str, List[str]] format.
    Used only at AI boundary.
    """
    if isinstance(skills, dict):
        return skills
    if isinstance(skills, list):
        return {"general": skills}
    return {}


def extract_resume_skills_from_breakdown(breakdown):
    """
    Converts screening breakdown into resume skill dictionary
    expected by the job matcher.
    """
    resume_skills = {}

    for category, data in breakdown.items():
        if isinstance(data, dict):
            skills = (
                data.get("matched_skills")
                or data.get("found")
                or data.get("skills")
                or []
            )
        else:
            skills = []

        resume_skills[category] = skills

    return resume_skills


# ------------------------
# Models
# ------------------------
class ChatRequest(BaseModel):
    filename: str
    question: str


# ------------------------
# Health Check
# ------------------------
@app.get("/")
def health_check():
    return {"status": "API running successfully"}


# ------------------------
# Upload PDF
# ------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully"
    }


# ------------------------
# Extract + Screen + Explain + AI Insights
# ------------------------
@app.get("/extract-text/{filename}")
def extract_text(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    reader = PdfReader(file_path)
    extracted_text = ""
    failed_pages = 0

    for page in reader.pages:
        try:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        except Exception:
            failed_pages += 1

    if not extracted_text.strip():
        return {
            "filename": filename,
            "text": "",
            "note": "No extractable text found. PDF may be scanned or complex.",
            "failed_pages": failed_pages
        }

    cleaned_text = clean_text(extracted_text)

    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    chatbot_feedback = generate_response(
        screening_result["total_score"],
        screening_result["breakdown"]
    )

    # AI Interpretation Layer (DOWNSTREAM ONLY)
    ai_input = ResumeAnalysisInput(
        resume_text=cleaned_text,
        scores={"total": screening_result["total_score"]},
        matched_skills=normalize_skills(
            screening_result.get("matched_skills")
        ),
        missing_skills=normalize_skills(
            screening_result.get("missing_skills")
        )
    )

    ai_insights = ai_engine.generate_insights(ai_input)

    return {
        "filename": filename,
        "score": screening_result["total_score"],
        "breakdown": screening_result["breakdown"],
        "chatbot_feedback": chatbot_feedback,
        "ai_insights": ai_insights.dict(),
        "failed_pages": failed_pages
    }


# ------------------------
# Interactive Chat (Rule-Based Only)
# ------------------------
@app.post("/chat")
def chat_with_resume(request: ChatRequest):
    file_path = os.path.join(UPLOAD_DIR, request.filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    reader = PdfReader(file_path)
    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    if not extracted_text.strip():
        return {"response": "No readable text found in the document."}

    cleaned_text = clean_text(extracted_text)
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    response = answer_question(
        request.question,
        screening_result["total_score"],
        screening_result["breakdown"]
    )

    return {
        "question": request.question,
        "response": response
    }


# ------------------------
# Job Recommendation Endpoint
# ------------------------
@app.get("/recommend-jobs/{filename}")
def recommend_jobs(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    reader = PdfReader(file_path)
    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    if not extracted_text.strip():
        return {
            "filename": filename,
            "job_recommendations": [],
            "note": "No readable text found in resume."
        }

    cleaned_text = clean_text(extracted_text)
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    resume_skills = extract_resume_skills_from_breakdown(
        screening_result["breakdown"]
    )

    recommendations = []

    for job in JOB_LIST:
        recommendations.append(
            match_resume_to_job(resume_skills, job)
        )

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "filename": filename,
        "job_recommendations": recommendations
    }
