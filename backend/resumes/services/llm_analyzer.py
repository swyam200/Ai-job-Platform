import json
from groq import Groq
from django.conf import settings


def analyze_resume(resume_text):
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    api_key = settings.GROQ_API_KEY

    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
You are a professional resume analyst.

Analyze the supplied resume and return valid JSON only.

Use exactly these keys:
- summary: concise professional summary
- strengths: list of demonstrated strengths
- weaknesses: list of areas needing improvement
- suggested_skills: list of skills recommended for future learning
- improvement_tips: list of actionable suggestions

Do not invent qualifications, skills, experience, or achievements.
Distinguish demonstrated skills from recommended skills.
"""
            },
            {
                "role": "user",
                "content": resume_text
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError(
            "The AI returned an invalid JSON response."
        ) from exc

    required_keys = {
        "summary",
        "strengths",
        "weaknesses",
        "suggested_skills",
        "improvement_tips",
    }

    if not required_keys.issubset(result.keys()):
        raise ValueError(
            "The AI response is missing required fields."
        )

    return result