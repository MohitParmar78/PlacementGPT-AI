from backend.models.semantic_matcher import (
    SemanticMatcher
)

matcher = SemanticMatcher()

resume_skills = [

    "PyTorch",

    "TensorFlow",

    "Python",

    "Machine Learning"
]

target_skills = [

    "Deep Learning Frameworks",

    "Neural Networks",

    "SQL"
]

result = matcher.match_skills(

    resume_skills,

    target_skills
)

print(result)