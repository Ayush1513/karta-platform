import json

from app.services.gemini_service import model


def generate_recommendations(
    profile,
    skills,
    opportunity
):

    prompt = f"""
    Student Profile:

    Name: {profile.full_name}
    Course: {profile.course}
    Academic Year: {profile.academic_year}
    CGPA: {profile.cgpa}
    Bio: {profile.bio}

    Skills:
    {skills}

    Opportunity:

    Title: {opportunity.title}

    Description:
    {opportunity.description}

    Analyze how relevant this opportunity is for the student.

    Return ONLY JSON.

    Example:

    {{
        "score": 85,
        "reason": "Strong match because student skills align with opportunity requirements."
    }}
    """

    response = model.generate_content(
        prompt
    )

    text = response.text.strip()

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    try:
        return json.loads(text)

    except Exception:

        return {
            "score": 50,
            "reason": "Unable to parse AI response."
        }