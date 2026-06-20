from backend.agents.followup_question_agent import (
    generate_followup_question
)

result = generate_followup_question(

    original_question=
    "What is CNN?",

    answer=
    """
    CNN is used for image processing.
    """,

    skill=
    "Deep Learning",

    target_role=
    "Machine Learning Engineer"
)

print(result)