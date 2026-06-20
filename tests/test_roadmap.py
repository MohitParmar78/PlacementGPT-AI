from backend.agents.roadmap_agent import (
    generate_learning_roadmap
)

result = generate_learning_roadmap(

    target_role=
    "Machine Learning Engineer",

    weaknesses=[
        "Deep Learning",
        "SQL"
    ],

    missing_skills=[
        "PyTorch",
        "CNN",
        "Window Functions"
    ]
)

print(result)