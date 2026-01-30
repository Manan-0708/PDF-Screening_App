from fastapi import FastAPI, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
from pydantic import BaseModel

import os
import shutil

from text_utils import clean_text
from screening import screen_resume
from keywords import SKILL_CATEGORIES
from chatbot import generate_response, answer_question

from ai_layer.ai_engine import AIEngine
from ai_layer.schemas import ResumeAnalysisInput

app = FastAPI(title="Resume Intelligence API")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def normalize_skills(skills):
    """
    Ensures skills are in Dict[str, List[str]] format.
    """
    if isinstance(skills, dict):
        return skills
    if isinstance(skills, list):
        return {"general": skills}
    return {}


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

    # 1) Check file existence
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # 2) Read PDF
    reader = PdfReader(file_path)
    extracted_text = ""
    failed_pages = 0

    # 3) Safe page-by-page extraction
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

    # 4) Clean text
    cleaned_text = clean_text(extracted_text)

    # 5) Rule-based screening
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    # 6) Deterministic chatbot feedback
    chatbot_feedback = generate_response(
        screening_result["total_score"],
        screening_result["breakdown"]
    )

    # 7) AI Interpretation Layer (DOWNSTREAM ONLY)
    ai_engine = AIEngine()

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

    # 8) Final response (non-breaking)
    return {
        "filename": filename,
        "score": screening_result["total_score"],
        "breakdown": screening_result["breakdown"],
        "chatbot_feedback": chatbot_feedback,
        "ai_insights": ai_insights.dict(),
        "failed_pages": failed_pages
    }


# ------------------------
# Interactive Chat Endpoint (Rule-Based Only)
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
