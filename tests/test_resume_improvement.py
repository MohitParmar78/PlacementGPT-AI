from backend.agents.resume_improvement_agent import (
    generate_resume_improvements
)

sections = {

    "projects":
    """
    Built movie recommendation system
    using Python.
    """,

    "experience":
    """
    Data Science Intern
    """,

    "education":
    """
    B.Tech Computer Science
    """
}

skills = [

    "Python",

    "Machine Learning",

    "SQL"
]

result = generate_resume_improvements(

    target_role=
    "Machine Learning Engineer",

    sections=
    sections,

    skills=
    skills
)

print(result)