# 📄 PDF Resume Screening & Job-Recommendation REST API

A high-performance, full-stack resume screening and role-matching REST API built with **Python**, **Flask**, and **FastAPI**. It extracts text from PDF resumes using **PyPDF**, evaluates candidates against a keyword-driven filtering pipeline, matches candidate skill profiles against curated job datasets, generates PDF analysis reports, and exposes a dual-framework REST API deployed on **Vercel** and **Render**.

---

## 🌐 Live Demos & API Service

* **Frontend Dashboard (Vercel):** [https://pdf-screening-app.vercel.app](https://pdf-screening-app.vercel.app)
* **Backend REST API (Render):** [https://resume-intelligence-backend-4165.onrender.com](https://resume-intelligence-backend-4165.onrender.com)
* **Interactive OpenAPI / Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Local)

---

## ✨ Features & Architecture

* **Dual-Framework Architecture (FastAPI + Flask):**
  * **FastAPI:** Handles async file uploads, PyPDF text extraction, PDF report downloads, and OpenAPI Swagger documentation (`/docs`).
  * **Flask REST Subsystem:** Handles candidate skill screening (`/flask/api/screen`), role-based job matching (`/flask/api/match-jobs`), and health monitoring (`/flask/api/health`). Mounted into FastAPI via Starlette `WSGIMiddleware`.
* 📄 **PyPDF-Based Parsing:** Page-by-page text extraction with support for technical skill syntax (`C++`, `C#`, `.NET`, `Node.js`, `Python`).
* 🎯 **Keyword-Driven Filtering Pipeline:** Evaluates and scores candidate skills across technical categories (languages, CS fundamentals, frameworks, tools).
* 📊 **Role-Based Job Matching:** Ranks candidate skill alignment against curated job-role datasets to compute match scores and identify skill gaps.
* 📥 **PDF Analysis Report Generation:** Generates downloadable candidate evaluation reports using ReportLab canvas.
* 🎨 **Lightweight Basic Frontend:** Single-page HTML/CSS/Vanilla JS web interface connecting to REST APIs with zero Node/npm overhead.

---

## 🛠️ Technologies & Tools Used

* **Languages & Core:** Python 3.x, HTML5, CSS3, JavaScript (Vanilla)
* **Frameworks & Libraries:** Flask, FastAPI, Uvicorn, Starlette
* **Parsing & PDF:** PyPDF (`pypdf` / `PyPDF2`), ReportLab
* **API & Middleware:** REST APIs, CORS Middleware, WSGIMiddleware
* **Deployment & Hosting:** Vercel (Frontend), Render (Backend Service)
* **Version Control:** Git & GitHub

---

## 📁 Repository Structure

```text
PDF-Screening_App/
├── backend/
│   ├── ai_layer/          # Candidate scoring schemas & insights
│   ├── job_matching/      # Job definitions & role matcher engine
│   ├── app.py             # FastAPI entrypoint, static files & Flask mounting
│   ├── flask_app.py       # Flask REST API microservice
│   ├── screening.py       # Keyword-driven screening pipeline
│   ├── text_utils.py      # PyPDF text cleaning & normalization
│   └── requirements.txt   # Python backend dependencies (Flask, FastAPI, PyPDF)
└── frontend/
    ├── index.html         # Basic single-page web dashboard
    └── vercel.json        # Static deployment configuration for Vercel
```

---

## 🚀 Running the Project Locally

### 1. Environment Setup

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
```

### 2. Start Unified Server (FastAPI + Flask + Basic Frontend)

```bash
python -m uvicorn app:app --reload --port 8000
```

* **Web Interface:** Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
* **FastAPI Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Flask REST Subsystem:** [http://127.0.0.1:8000/flask/api/health](http://127.0.0.1:8000/flask/api/health)

---

## ☁️ Deployment Guide

### Backend on Render
1. Create a **New Web Service** on Render and connect your GitHub repository.
2. Set Root Directory to `backend`.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Frontend on Vercel
1. Import project into Vercel and select the `frontend` folder as the Root Directory.
2. Framework Preset: **Other** (Static HTML).
3. Deploy!

---

## 📌 License & Author

Developed by [Manan](https://github.com/Manan-0708) — Resume Screening & Job-Recommendation REST API built using Python, Flask, FastAPI, PyPDF, REST APIs, Vercel, and Render.
