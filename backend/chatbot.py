def generate_response(score: int, breakdown: dict):
    responses = []

    if score >= 70:
        responses.append("The resume is overall strong.")
    elif score >= 40:
        responses.append("The resume is average and could use some improvements.")
    else:
        responses.append("The resume needs significant improvements.")
    
    for category, data in breakdown.items():
        if data["matched"]:
            responses.append(
                f"Good knowledge in {category}: {', '.join(data['matched'])}."
            )

        if data["missing"]:
            responses.append(
                f"Missing important skills in {category}: {', '.join(data['missing'])}."
            )
            
    return " ".join(responses)
    

def answer_question(question: str, score: int, breakdown: dict):
    q = question.lower()

    if "score" in q or "low" in q:
        if score >= 70:
            return "Your score is high because you match most required skills."
        elif score >= 40:
            return "Your score is moderate. You meet core requirements but miss some important skills."
        else:
            return "Your score is low because several key skill areas are missing."

    if "strength" in q:
        strengths = []
        for category, data in breakdown.items():
            if data.get("matched"):
                strengths.append(f"{category}: {', '.join(data['matched'])}")
        return "Your strengths are: " + "; ".join(strengths) if strengths else "No strong areas detected."

    if "improve" in q or "missing" in q:
        improvements = []
        for category, data in breakdown.items():
            if data.get("missing"):
                improvements.append(f"{category}: {', '.join(data['missing'])}")
        return "You should work on: " + "; ".join(improvements) if improvements else "No major improvements needed."

    return "You can ask about your score, strengths, or improvements."