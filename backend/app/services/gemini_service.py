import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )

genai.configure(
    api_key=api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def extract_skills(text: str):

    prompt = f"""
    Extract technical skills from this resume.

    Return only a Python list.

    Resume:
    {text}
    """

    response = model.generate_content(
        prompt
    )

    return response.text

def career_suggestions(profile, skills):

    prompt = f"""
    Scholar Profile:

    Name: {profile.full_name}
    Course: {profile.course}
    Academic Year: {profile.academic_year}
    CGPA: {profile.cgpa}

    Skills:
    {", ".join(skills)}

    Return ONLY valid JSON.

    {{
        "career_paths": [],
        "skills_to_learn": [],
        "courses": []
    }}
    """

    response = model.generate_content(
        prompt
    )

    result = response.text

    result = result.replace(
        "```json",
        ""
    )

    result = result.replace(
        "```",
        ""
    )

    return json.loads(result)