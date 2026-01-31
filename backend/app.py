from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader
from pydantic import BaseModel

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# AI engine (resume insights only)
ai_engine = AIEngine()

# ------------------------
# Helpers
# ------------------------
def normalize_skills(skills):
    if isinstance(skills, dict):
        return skills
    if isinstance(skills, list):
        return {"general": skills}
    return {}


def extract_resume_skills_from_breakdown(breakdown):
    resume_skills = {}
    for category, data in breakdown.items():
        skills = data.get("matched", []) if isinstance(data, dict) else []
        resume_skills[category] = skills
    return resume_skills


def generate_analysis_pdf(filename: str, analysis: dict) -> str:
    pdf_path = os.path.join(UPLOAD_DIR, f"{filename}_analysis.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 40

    def draw(text):
        nonlocal y
        c.drawString(40, y, text)
        y -= 16
        if y < 40:
            c.showPage()
            y = height - 40

    draw("Resume Analysis Report")
    draw("=" * 50)
    draw(f"Filename: {filename}")
    draw(f"Generated on: {datetime.now().strftime('%d %b %Y %H:%M')}")
    draw("")

    draw(f"Overall Score: {analysis['score']} / 100")
    draw("")

    draw("Screening Breakdown:")
    for category, score in analysis["screening_breakdown"].items():
        draw(f"- {category.title()}: {score}")

    draw("")
    draw("AI Profile Summary:")
    draw(analysis["ai_insights"]["profile_summary"])
    draw("")

    draw("Strengths:")
    for s in analysis["ai_insights"]["strengths"]:
        draw(f"• {s}")

    draw("")
    draw("Areas to Improve:")
    for w in analysis["ai_insights"]["weaknesses"]:
        draw(f"• {w}")

    draw("")
    draw("Chatbot Feedback:")
    draw(analysis["chatbot_feedback"])

    c.save()
    return pdf_path


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
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


# ------------------------
# Extract + Screen + AI Insights
# ------------------------
@app.get("/extract-text/{filename}")
def extract_text(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    reader = PdfReader(file_path)
    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    cleaned_text = clean_text(extracted_text)
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    chatbot_feedback = generate_response(
        screening_result["total_score"],
        screening_result["breakdown"]
    )

    ai_input = ResumeAnalysisInput(
        resume_text=cleaned_text,
        scores={"total": screening_result["total_score"]},
        matched_skills=normalize_skills(screening_result["matched_skills"]),
        missing_skills=normalize_skills(screening_result["missing_skills"]),
    )

    ai_insights = ai_engine.generate_insights(ai_input)

    return {
        "filename": filename,
        "score": screening_result["total_score"],
        "screening_breakdown": {
            k: v["score"] for k, v in screening_result["breakdown"].items()
        },
        "chatbot_feedback": chatbot_feedback,
        "ai_insights": ai_insights.dict(),
    }


# ------------------------
# Download Resume Analysis PDF
# ------------------------
@app.get("/download-analysis/{filename}")
def download_analysis(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume not found")

    reader = PdfReader(file_path)
    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    cleaned_text = clean_text(extracted_text)
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    chatbot_feedback = generate_response(
        screening_result["total_score"],
        screening_result["breakdown"]
    )

    ai_input = ResumeAnalysisInput(
        resume_text=cleaned_text,
        scores={"total": screening_result["total_score"]},
        matched_skills=normalize_skills(screening_result["matched_skills"]),
        missing_skills=normalize_skills(screening_result["missing_skills"]),
    )

    ai_insights = ai_engine.generate_insights(ai_input)

    analysis = {
        "score": screening_result["total_score"],
        "screening_breakdown": {
            k: v["score"] for k, v in screening_result["breakdown"].items()
        },
        "chatbot_feedback": chatbot_feedback,
        "ai_insights": ai_insights.dict(),
    }

    pdf_path = generate_analysis_pdf(filename, analysis)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{filename}_analysis.pdf",
    )


# ------------------------
# Job Recommendations
# ------------------------
@app.get("/recommend-jobs/{filename}")
def recommend_jobs(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    reader = PdfReader(file_path)
    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    cleaned_text = clean_text(extracted_text)
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    resume_skills = extract_resume_skills_from_breakdown(
        screening_result["breakdown"]
    )

    recommendations = []

    for job in JOB_LIST:
        match = match_resume_to_job(resume_skills, job)

        flat_matched = [s for v in match["matched_skills"].values() for s in v]
        flat_missing = [s for v in match["missing_skills"].values() for s in v]

        recommendations.append({
            "job_title": match["title"],
            "match_score": match["match_score"],
            "matched_skills": flat_matched,
            "missing_skills": flat_missing,
            "ai_job_insights": (
                f"This role matches {match['match_score']}% of your skills. "
                f"Strengths include {', '.join(flat_matched[:3]) or 'general alignment'}. "
                f"Improving {', '.join(flat_missing[:3]) or 'additional skills'} can improve fit."
            )
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)

    return {"filename": filename, "job_recommendations": recommendations}
