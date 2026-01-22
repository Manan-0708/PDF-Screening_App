# 📄 PDF Screening Application

An intelligent backend system to screen PDF documents (such as resumes) by extracting text, handling different PDF types, and preparing data for rule-based and AI-driven analysis.

---

## 🚀 Project Status

**Active development**
Core backend functionality is implemented and stable.

---

## ✨ Features Implemented

* ✅ FastAPI-based backend
* ✅ PDF upload via REST API
* ✅ Server-side file storage
* ✅ Text extraction from text-based PDFs
* ✅ Graceful handling of scanned/complex PDFs
* ✅ Page-level error handling (no server crashes)
* ✅ Interactive API testing via Swagger UI

---

## 🧠 Planned Features

* 🔄 Text cleaning and normalization
* 🔍 Keyword-based resume screening
* 📊 Explainable scoring system
* 🤖 AI-assisted resume analysis
* 🎨 Frontend dashboard (React)

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **PDF Processing:** PyPDF2
* **Server:** Uvicorn
* **Version Control:** Git & GitHub

---

## ▶️ Running the Project Locally

```bash
# Clone the repository
git clone https://github.com/Manan-0708/PDF-Screening_App.git
cd PDF-Screening_App/backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --reload
```

Open in browser:

* API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 Note

This project is being developed incrementally with a focus on **real-world backend engineering practices**, robustness, and explainability.

---
