# ==========================================
# PlacementGPT-AI
# Roadmap Agent
# ==========================================

import json

from groq import Groq

from backend.config.settings import (
    GROQ_API_KEY
)

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_learning_roadmap(
    target_role,
    weaknesses,
    missing_skills
):
    """
    Generate personalized
    30-day learning roadmap.
    """

    prompt = f"""
You are an expert AI career mentor.

Target Role:
{target_role}

Weaknesses:
{json.dumps(weaknesses, indent=2)}

Missing Skills:
{json.dumps(missing_skills, indent=2)}

Create a detailed 30-day learning roadmap.

Return ONLY valid JSON.

Format:

{{
    "week_1": [
        "...",
        "..."
    ],

    "week_2": [
        "...",
        "..."
    ],

    "week_3": [
        "...",
        "..."
    ],

    "week_4": [
        "...",
        "..."
    ],

    "recommended_projects": [
        "...",
        "..."
    ],

    "recommended_resources": [
        "...",
        "..."
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

        temperature=0.2,

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

            "week_1": [],

            "week_2": [],

            "week_3": [],

            "week_4": [],

            "recommended_projects": [],

            "recommended_resources": []
        }