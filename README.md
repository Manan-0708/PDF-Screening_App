# 📄 PDF Resume Screening & Job Recommendation REST API

A high-performance, full-stack resume screening and role-matching REST API built with **Python**, **Flask**, and **FastAPI**. It extracts text from PDF resumes using **PyPDF**, evaluates candidates against a keyword-driven filtering pipeline, matches candidate skill profiles against curated job datasets, generates PDF reports, and exposes a dual-framework REST API deployed on **Vercel** and **Render**.

---

## 🌐 Live Demos & API Service

* **Frontend Dashboard (Vercel):** [https://pdf-screening-app.vercel.app](https://pdf-screening-app.vercel.app)
* **Backend REST API (Render):** [https://resume-intelligence-backend-4165.onrender.com](https://resume-intelligence-backend-4165.onrender.com)
* **Interactive OpenAPI / Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Local)

---

## ✨ Features & Architecture

* **Dual-Framework Architecture (FastAPI + Flask):**
  * **FastAPI:** Handles async file uploads, PyPDF text extraction, PDF report generation, and OpenAPI spec generation.
  * **Flask REST Subsystem:** Handles candidate skill screening (`/flask/api/screen`), role-based job matching (`/flask/api/match-jobs`), and candidate Q&A (`/flask/api/ask`). The Flask WSGI service is mounted into FastAPI via Starlette `WSGIMiddleware`.
* 📄 **PyPDF-Based Parsing:** Page-by-page text extraction with support for special technical skill syntax (`C++`, `C#`, `.NET`, `Node.js`, `Python`).
* 🎯 **Keyword-Driven Filtering Pipeline:** Categorizes candidate skills across languages, CS fundamentals, frameworks, and tools.
* 📊 **Role-Based Job Matching:** Evaluates candidate skill profiles against curated job role datasets to rank job alignment percentage and identify skill gaps.
* 📥 **PDF Analysis Report Generation:** Generates downloadable candidate evaluation reports using ReportLab canvas.
* 💬 **Candidate Q&A Endpoint:** Interactive REST API endpoint answering candidate score breakdown and strength questions.

---

## 🛠️ Technologies & Tools Used

* **Language & Core:** Python 3.x
* **Frameworks:** Flask, FastAPI, Uvicorn, Starlette
* **Parsing & PDF:** PyPDF (`pypdf` / `PyPDF2`), ReportLab
* **API Architecture:** REST APIs, CORS Middleware, WSGIMiddleware
* **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS
* **Deployment & Hosting:** Vercel (Frontend), Render (Backend Service)

---

## 📁 Repository Structure

```text
PDF-Screening_App/
├── backend/
│   ├── ai_layer/          # Candidate scoring schemas & insights
│   ├── job_matching/      # Job definitions & role matcher engine
│   ├── app.py             # FastAPI entrypoint & WSGI Flask mounting
│   ├── flask_app.py       # Flask REST API microservice
│   ├── chatbot.py         # Q&A & feedback generator
│   ├── screening.py       # Keyword-driven screening pipeline
│   ├── text_utils.py      # PyPDF text cleaning & normalization
│   └── requirements.txt   # Python dependencies (Flask, FastAPI, PyPDF)
└── frontend/
    ├── app/               # Next.js App Router pages
    ├── components/        # React UI components
    └── lib/               # API client
```

---

## 🚀 Running the Project Locally

### 1. Backend (Flask + FastAPI)

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start unified FastAPI + Flask server
python -m uvicorn app:app --reload --port 8000
```

* **FastAPI Endpoints:** `http://127.0.0.1:8000`
* **Flask REST Endpoints:** `http://127.0.0.1:8000/flask/api/...`

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
cmd /c "npm run dev"
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📌 License & Author

Developed by [Manan](https://github.com/Manan-0708) — Resume Screening & Job-Recommendation REST API built using Python, Flask, FastAPI, PyPDF, REST APIs, Vercel, and Render.
