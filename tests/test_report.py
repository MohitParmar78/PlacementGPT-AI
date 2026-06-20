from backend.agents.report_agent import (
    generate_pdf_report
)

# =====================================
# Candidate Profile
# =====================================

profile = {

    "resume_name":
        "Mohit_Resume.pdf",

    "total_skills":
        12,

    "education_found":
        True,

    "experience_found":
        True,

    "certifications_found":
        True
}

# =====================================
# Resume Scores
# =====================================

resume_score = 85

ats_score = 82

# =====================================
# Skill Gap
# =====================================

skill_gap = {

    "required_skills": [

        "Python",

        "Machine Learning",

        "Deep Learning",

        "SQL",

        "PyTorch"
    ],

    "missing_skills": [

        "PyTorch",

        "SQL"
    ]
}

# =====================================
# ATS Analysis
# =====================================

ats_analysis = {

    "matched_skills": [

        "Python",

        "Machine Learning",

        "Deep Learning"
    ],

    "missing_skills": [

        "PyTorch",

        "SQL"
    ],

    "recommendations": [

        "Add PyTorch projects",

        "Mention SQL experience",

        "Add deployment skills"
    ]
}

# =====================================
# Resume Improvements
# =====================================

resume_improvements = {

    "summary_improvements": [

        "Add stronger professional summary",

        "Highlight achievements"
    ],

    "project_improvements": [

        "Mention model accuracy",

        "Add business impact"
    ],

    "experience_improvements": [

        "Use action verbs",

        "Quantify achievements"
    ],

    "skill_improvements": [

        "Add PyTorch",

        "Add Docker"
    ],

    "ats_recommendations": [

        "Include Deep Learning keyword",

        "Include SQL keyword"
    ]
}

# =====================================
# Interview Feedback
# =====================================

interview_feedback = {

    "overall_score":
        78,

    "technical_score":
        8,

    "communication_score":
        7,

    "question_feedback": [

        {

            "question":
                "What is Machine Learning?",

            "score":
                8,

            "feedback":
                "Good answer.",

            "correct_answer":
                "Machine Learning is a subset of AI that learns patterns from data."
        },

        {

            "question":
                "What is Deep Learning?",

            "score":
                7,

            "feedback":
                "Could explain neural networks better.",

            "correct_answer":
                "Deep Learning uses neural networks with multiple layers."
        }
    ],

    "strengths": [

        "Good ML fundamentals",

        "Strong communication"
    ],

    "weaknesses": [

        "Weak SQL knowledge",

        "Limited PyTorch experience"
    ],

    "improvement_suggestions": [

        "Practice SQL",

        "Build PyTorch projects"
    ],

    "learning_roadmap": [

        "Week 1: SQL",

        "Week 2: PyTorch",

        "Week 3: CNN",

        "Week 4: Deployment"
    ]
}

# =====================================
# Generate PDF
# =====================================

pdf_path = generate_pdf_report(

    target_role=
        "Machine Learning Engineer",

    profile=
        profile,

    resume_score=
        resume_score,

    ats_score=
        ats_score,

    skill_gap=
        skill_gap,

    ats_analysis=
        ats_analysis,

    resume_improvements=
        resume_improvements,

    interview_feedback=
        interview_feedback
)

print(
    "\nPDF Generated Successfully\n"
)

print(
    pdf_path
)