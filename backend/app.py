from fastapi import FastAPI, UploadFile, File, HTTPException
from PyPDF2 import PdfReader
from text_utils import clean_text
from screening import screen_resume
from keywords import SKILL_CATEGORIES
from chatbot import generate_response
import os
import shutil

app = FastAPI(title="PDF Screening API")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "API running successfully"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.get("/extract-text/{filename}")
def extract_text(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 1) Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # 2) Read PDF
    reader = PdfReader(file_path)
    extracted_text = ""
    failed_pages = 0

    # 3) Extract text page by page safely
    for page in reader.pages:
        try:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        except Exception:
            failed_pages += 1
            continue

    if not extracted_text.strip():
        return {
            "filename": filename,
            "text": "",
            "note": "No extractable text found. PDF may be scanned or complex.",
            "failed_pages": failed_pages
        }
    
    # 4) Clean text
    cleaned_text = clean_text(extracted_text)

# 5) Screen resume
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)

    chatbot_response = generate_response(
        screening_result["total_score"], screening_result["breakdown"]
    )

    return {
        "filename": filename,
    "score": screening_result["total_score"],
    "breakdown": screening_result["breakdown"],
    "chatbot_feedback": chatbot_response,
    "failed_pages": failed_pages
    }
