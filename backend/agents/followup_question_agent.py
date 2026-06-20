import json

from groq import Groq

from backend.config.settings import (
    GROQ_API_KEY
)

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_followup_question(
    original_question,
    answer,
    skill,
    target_role
):
    """
    Generate follow-up question
    based on candidate answer.
    """

    prompt = f"""
You are a senior FAANG interviewer.

Target Role:
{target_role}

Skill:
{skill}

Original Question:
{original_question}

Candidate Answer:
{answer}

TASK:

Generate ONE deeper follow-up
question.

Rules:

- Must be related to answer.
- Must test deeper understanding.
- Must be technical.
- One question only.

Return JSON:

{{
    "followup_question":
    "..."
}}
"""

    response = client.chat.completions.create(

        model=
        "llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.4,

        response_format={
            "type":"json_object"
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

    except:

        return {

            "followup_question":
            "Could you explain that in more detail?"
        }