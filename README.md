# 📄 PDF Resume Screening & Intelligence Platform

An intelligent, full-stack resume screening system powered by FastAPI and Next.js. It extracts text from PDF resumes, categorizes technical and soft skills, performs AI-driven candidate profiling, matches resumes against job roles, generates downloadable PDF reports, and provides an interactive dashboard.

---

## 🌐 Live Demos & Deployment

* **Frontend Dashboard (Vercel):** [https://pdf-screening-app.vercel.app](https://pdf-screening-app.vercel.app)
* **Backend API Service (Render):** [https://pdf-screening-backend.onrender.com](https://pdf-screening-backend.onrender.com) *(or your Render backend URL)*
* **Interactive API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Local)

---

## ✨ Key Features

* 📤 **PDF Upload & Text Extraction:** Native parsing of single and multi-page text PDFs with page-level fault tolerance using PyPDF2.
* 🧠 **AI Profiling & Scoring:** Evaluates candidate resumes against structured criteria, generating actionable profile summaries and automated quality scores.
* 🔍 **Skill Breakdown & Categorization:** Classifies identified skills into technical categories, frameworks, and domain expertise.
* 🎯 **Job Matching Engine:** Ranks candidate alignment against dynamic job descriptions and requirement sets.
* 📄 **Downloadable Analysis Reports:** Server-side PDF report generation (via ReportLab) for offline review and candidate evaluation summaries.
* 💬 **AI Assistant / Chatbot:** Interactive candidate Q&A for screening insights.
* 🎨 **Modern Next.js Dashboard:** Built with Next.js App Router, Tailwind CSS, TypeScript, and integrated `@vercel/analytics`.

---

## 🛠️ Tech Stack

* **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS, Vercel Analytics
* **Backend:** Python 3.x, FastAPI, Uvicorn, Pydantic
* **PDF & Utilities:** PyPDF2, ReportLab (PDF Generation)
* **AI & NLP:** Custom AI Engine layer for candidate intelligence & Q&A
* **Deployment:** Vercel (Frontend Hosting) & Render (Backend Service)
* **Version Control:** Git & GitHub

---

## 📁 Repository Structure

```text
PDF-Screening_App/
├── backend/
│   ├── ai_layer/          # AI engine and pydantic schema definitions
│   ├── job_matching/      # Job matching logic and dataset
│   ├── app.py             # FastAPI entrypoint, CORS & routes
│   ├── chatbot.py         # Q&A / Assistant logic
│   ├── screening.py       # Rule-based screening logic
│   ├── text_utils.py      # PDF text extraction and normalization
│   └── requirements.txt   # Python backend dependencies
└── frontend/
    ├── app/               # Next.js App Router pages and layouts
    ├── components/        # Reusable UI components
    ├── lib/               # Utility functions and API clients
    ├── package.json       # Node dependencies and scripts
    └── next.config.js     # Next.config
```

---

## 🚀 Local Development Setup

### 1. Backend Setup (FastAPI)

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app:app --reload --port 8000
```

The backend server will run at `http://127.0.0.1:8000`.

### 2. Frontend Setup (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Create environment configuration (.env.local)
# NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to test locally.

---

## ☁️ Deployment Guide

### Backend on Render
1. Create a **New Web Service** on Render and connect your GitHub repository.
2. Set Root Directory to `backend`.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Frontend on Vercel
1. Import project into Vercel and select the `frontend` folder as the Root Directory.
2. Add Environment Variable:
   `NEXT_PUBLIC_API_BASE_URL` = `<YOUR_RENDER_BACKEND_URL>`
3. Deploy!

---

## 📌 License & Author

Developed by [Manan](https://github.com/Manan-0708) focusing on robust backend practices, AI resume analysis, and clean web application design.
