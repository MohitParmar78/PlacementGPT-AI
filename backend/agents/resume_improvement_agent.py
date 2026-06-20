# ==========================================
# PlacementGPT-AI
# Resume Improvement Agent
# ==========================================

import json

from groq import Groq

from backend.config.settings import (
    GROQ_API_KEY
)

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_resume_improvements(
    target_role,
    sections,
    skills
):
    """
    Generate resume improvement suggestions.
    """

    prompt = f"""
You are a FAANG-level recruiter and resume reviewer.

Target Role:
{target_role}

Resume Sections:

{json.dumps(sections, indent=2)}

Detected Skills:

{json.dumps(skills, indent=2)}

TASK:

Review the resume and provide detailed
improvement suggestions.

Focus on:

1. Resume Summary
2. Projects
3. Experience
4. Skills
5. ATS Optimization

Return ONLY valid JSON.

Example:

{{
    "summary_improvements":[
        "Add measurable achievements."
    ],

    "project_improvements":[
        "Mention model accuracy."
    ],

    "experience_improvements":[
        "Use action verbs."
    ],

    "skill_improvements":[
        "Add PyTorch."
    ],

    "ats_recommendations":[
        "Include Deep Learning keyword."
    ]
}}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,

        response_format={
            "type": "json_object"
        }
    )

    result = (
        response
        .choices[0]
        .message
        .content
    )

    try:

        return json.loads(
            result
        )

    except Exception:

        return {

            "summary_improvements": [],

            "project_improvements": [],

            "experience_improvements": [],

            "skill_improvements": [],

            "ats_recommendations": []
        }