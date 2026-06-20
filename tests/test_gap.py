from backend.agents.skill_gap_agent import (
    SkillGapAgent
)

agent = SkillGapAgent()

resume_skills = [

    "Python",

    "TensorFlow",

    "Machine Learning"
]

target_skills = [

    "Python",

    "Deep Learning Frameworks",

    "SQL"
]

result = agent.analyze_skill_gap(

    resume_skills=
        resume_skills,

    target_skills=
        target_skills,

    target_role=
        "Machine Learning Engineer"
)

print(result)