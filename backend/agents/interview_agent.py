# ==========================================
# PlacementGPT-AI
# Interview Evaluation Agent
# ==========================================

import json

from groq import Groq

from backend.config.settings import (
    GROQ_API_KEY
)

client = Groq(
    api_key=GROQ_API_KEY
)


def evaluate_interview(
    target_role,
    interview_data
):
    """
    Evaluate complete interview
    using a single Llama call.
    """
    bad_answers = {

    "idk",
    "i don't know",
    "dont know",
    "no idea",
    "not sure",
    "n/a",
    "na"
}

    for item in interview_data:

        answer = (
            item.get(
                "answer",
                ""
            )
            .strip()
            .lower()
        )

        if (
            len(answer) < 5
            or
            answer in bad_answers
        ):

            item["answer"] = (
                f"{item['answer']} "
                "[VERY_POOR_ANSWER]"
            )

    interview_text = json.dumps(
        interview_data,
        indent=2
    )

    prompt = f"""
You are an expert FAANG-level technical interviewer.

Target Role:
{target_role}

Interview Responses:

{interview_text}

TASK:

Evaluate EACH interview response.

For every question provide:

1. Original question
2. Score (0-10)
3. Feedback
4. Ideal answer

Scoring Guide:

STRICT SCORING RULES:

- Empty answer = Score 0
- "I don't know" = Score 0
- "No idea" = Score 0
- Random words = Score 0
- Irrelevant answer = Score 0-2

Examples of bad answers:

"asdfgh"
"abc"
"idk"
"don't know"
"not sure"

These answers MUST receive 0.

Do NOT reward effort.

Do NOT reward attempts.

Act like a strict FAANG interviewer.

Only award scores above 5 if the answer demonstrates
real technical understanding and correctness.

0-2:
Incorrect or irrelevant answer

3-4:
Very weak understanding

5-6:
Basic understanding

7-8:
Good answer

9-10:
Excellent answer

IMPORTANT:

- Evaluate ALL questions.
- Never leave question_feedback empty.
- Always create one feedback object per question.
- Always provide at least 2 strengths.
- Always provide at least 2 weaknesses.
- Always provide at least 2 improvement suggestions.
- Generate a role-specific learning roadmap.

Return ONLY valid JSON.

Example:

{{
    "question_feedback": [
        {{
            "question": "What is Machine Learning?",

            "score": 2,

            "feedback":
            "The answer is too vague and does not explain the concept.",

            "correct_answer":
            "Machine Learning is a subset of AI that enables systems to learn patterns from data and make predictions without explicit programming."
        }}
    ],

    "technical_score": 3,

    "communication_score": 2,

    "strengths": [
        "Attempted all questions",
        "Showed willingness to answer"
    ],

    "weaknesses": [
        "Lack of technical depth",
        "Answers are too brief"
    ],

    "improvement_suggestions": [
        "Study Machine Learning fundamentals",
        "Practice explaining concepts clearly"
    ],

    "learning_roadmap": [
        "Week 1: Machine Learning Basics",
        "Week 2: Deep Learning Fundamentals",
        "Week 3: NLP and Transformers",
        "Week 4: Build a Mini Project"
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

        temperature=0.1,

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

    print("=" * 80)
    print("RAW LLAMA RESPONSE")
    print(result)
    print("=" * 80)

    try:

        result = json.loads(
            result
        )

        question_feedback = result.get(
            "question_feedback",
            []
        )

        # Calculate overall score safely

        if len(question_feedback) > 0:

            scores = [

                item.get(
                    "score",
                    0
                )

                for item in question_feedback
            ]

            average_score = (

                sum(scores)

                /

                len(scores)
            )

            if average_score < 2:

                overall_score = 10

            elif average_score < 4:

                overall_score = 30

            elif average_score < 6:

                overall_score = 50

            elif average_score < 7.5:

                overall_score = 70

            elif average_score < 9:

                overall_score = 85

            else:

                overall_score = 95

                result[
                    "overall_score"
                ] = overall_score

        else:

            result[
                "overall_score"
            ] = 0

        return result

    except Exception as e:

        print(
            "JSON ERROR:",
            e
        )

        return {

            "overall_score": 0,

            "technical_score": 0,

            "communication_score": 0,

            "question_feedback": [],

            "strengths": [],

            "weaknesses": [],

            "improvement_suggestions": [],

            "learning_roadmap": []
        }