# flask_app.py - Flask REST API for Resume Screening & Role Matching
from flask import Flask, request, jsonify
import os

from text_utils import clean_text
from screening import screen_resume
from keywords import SKILL_CATEGORIES
from chatbot import generate_response, answer_question
from job_matching.job_data import JOB_LIST
from job_matching.matcher import match_resume_to_job

flask_app = Flask(__name__)

def extract_resume_skills_from_breakdown(breakdown):
    resume_skills = {}
    for category, data in breakdown.items():
        skills = data.get("matched", []) if isinstance(data, dict) else []
        resume_skills[category] = skills
    return resume_skills


@flask_app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "Flask REST service running", "framework": "Flask"})


@flask_app.route("/api/screen", methods=["POST"])
def screen():
    """
    Flask REST endpoint: Keyword-driven screening pipeline
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    cleaned_text = clean_text(text)
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)
    feedback = generate_response(
        screening_result["total_score"],
        screening_result["breakdown"]
    )

    return jsonify({
        "score": screening_result["total_score"],
        "breakdown": {
            k: v["score"] for k, v in screening_result["breakdown"].items()
        },
        "matched_skills": screening_result["matched_skills"],
        "missing_skills": screening_result["missing_skills"],
        "feedback": feedback
    })


@flask_app.route("/api/match-jobs", methods=["POST"])
def match_jobs():
    """
    Flask REST endpoint: Role-based matching against curated job datasets
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No resume text provided"}), 400

    cleaned_text = clean_text(text)
    screening_result = screen_resume(cleaned_text, SKILL_CATEGORIES)
    resume_skills = extract_resume_skills_from_breakdown(screening_result["breakdown"])

    recommendations = []
    for job in JOB_LIST:
        match = match_resume_to_job(resume_skills, job)
        flat_matched = [s for v in match["matched_skills"].values() for s in v]
        flat_missing = [s for v in match["missing_skills"].values() for s in v]

        recommendations.append({
            "job_id": job.job_id,
            "job_title": match["title"],
            "match_score": match["match_score"],
            "matched_skills": flat_matched,
            "missing_skills": flat_missing,
            "explanation": match["explanation"]
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return jsonify({"recommendations": recommendations})


@flask_app.route("/api/ask", methods=["POST"])
def ask():
    """
    Flask REST endpoint: Candidate screening Q&A
    """
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")
    score = data.get("score", 0)
    breakdown = data.get("breakdown", {})

    if not question:
        return jsonify({"error": "Question is required"}), 400

    response_text = answer_question(question, score, breakdown)
    return jsonify({"question": question, "answer": response_text})


if __name__ == "__main__":
    flask_app.run(port=5000, debug=True)
