def generate_response(score: int, breakdown: dict):
    responses= []

    #Overall Assessment
    if score >= 70:
        responses.append("The resume is strong overall.")
    elif score >= 40:
        responses.append("The resume is average overall and has room for improvement.")
    else:
        responses.append("The resume is weak overall and needs significant improvement.")

    #Category-wise Feedback
    for category,data in breakdown.items():
        if data["matched"]:
            responses.append(
                f"Good knowledge in {category} with skills: {', '.join(data['matched'])}."
            )

        if data["missing"]:
            responses.append(
                f"Consider improving skills in {category}: {', '.join(data['missing'])}."
            )
        
    return " ".join(responses)