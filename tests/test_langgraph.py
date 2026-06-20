from backend.workflows.interview_workflow import (
    graph
)

result = graph.invoke(

    {

        "resume_text": """

        Skills
        Python
        SQL
        Machine Learning

        Projects
        Movie Recommendation Engine

        Education
        B.Tech CSE

        """,

        "target_role":
        "Machine Learning Engineer"
    }
)

print(result)