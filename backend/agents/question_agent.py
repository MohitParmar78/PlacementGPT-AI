# ==========================================
# PlacementGPT-AI
# Llama Question Agent
# ==========================================

import json

from groq import Groq

from backend.config.settings import (
    GROQ_API_KEY
)

# ------------------------------------------
# Groq Client
# ------------------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_questions(
    skills,
    target_role,
    sections,
    difficulty="Medium",
    max_questions=5
):
    """
    Generate personalized interview questions
    using Llama 70B.

    Parameters
    ----------
    skills : list

    target_role : str

    sections : dict

    max_questions : int
    """

    # --------------------------------------
    # Extract Resume Sections
    # --------------------------------------

    projects = sections.get(
        "projects",
        ""
    )

    experience = sections.get(
        "experience",
        ""
    )

    education = sections.get(
        "education",
        ""
    )

    # --------------------------------------
    # Build Resume Context
    # --------------------------------------

    resume_context = f"""

Target Role:
{target_role}

Skills:
{", ".join(skills)}

Projects:
{projects}

Experience:
{experience}

Education:
{education}

Difficulty:
{difficulty}

"""
    # --------------------------------------
    # Prompt
    # --------------------------------------

    prompt = f"""
You are a senior technical interviewer.

Candidate Resume:

{resume_context}

If Difficulty Easy:
Ask beginner questions.

If Difficulty Medium:
Ask interview-level questions.

If Difficulty Hard:
Ask FAANG-level deep technical questions.

Generate {max_questions} interview questions.

Rules:

1. Questions must be personalized.
2. Use project information.
3. Use skills.
4. Use experience if available.
5. Avoid generic questions like:
   - What is Python?
   - What is NLP?
6. Ask project-based questions.
7. Ask role-specific questions.

Return ONLY valid JSON.

Format:

{{
    "questions":[
        {{
            "skill":"Python",
            "question":"Why did you choose FastAPI instead of Flask?"
        }},
        {{
            "skill":"Machine Learning",
            "question":"How would you improve your model performance?"
        }}
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
        
        max_completion_tokens=1000,

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

        data = json.loads(
            result
        )

        questions = []

        for item in data[
            "questions"
        ]:

            questions.append(

                {

                    "role":
                        target_role,

                    "skill":
                        item.get(
                            "skill",
                            "General"
                        ),

                    "question":
                        item.get(
                            "question",
                            ""
                        )
                }
            )

        return questions

    except Exception as e:

        print(
            "QUESTION AGENT ERROR:",
            e
        )

        return [
            {
                "role":
                    target_role,

                "skill":
                    "General",

                "question":
                    "Tell me about one of your projects."
            }
        ]