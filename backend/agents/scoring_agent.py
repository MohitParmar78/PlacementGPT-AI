"""
PlacementGPT-AI
Advanced Resume Scoring Agent
"""

from backend.config.role_loader import (
    load_role_skills
)


def calculate_resume_score(
    sections,
    skills,
    target_role
):
    """
    Returns:

    resume_score
    ats_score
    breakdown
    ats_analysis
    """

    role_skills = load_role_skills()

    required_skills = role_skills.get(
        target_role,
        []
    )

    # ==================================
    # Resume Score
    # ==================================

    breakdown = {

        "skills": 0,

        "projects": 0,

        "education": 0,

        "experience": 0,

        "certifications": 0
    }

    # ------------------------
    # Skills
    # ------------------------

    skills_count = len(skills)

    if skills_count >= 15:

        breakdown["skills"] = 30

    elif skills_count >= 10:

        breakdown["skills"] = 25

    elif skills_count >= 5:

        breakdown["skills"] = 15

    else:

        breakdown["skills"] = 5

    # ------------------------
    # Education
    # ------------------------

    if sections.get(
        "education",
        ""
    ).strip():

        breakdown["education"] = 15

    # ------------------------
    # Experience
    # ------------------------

    if sections.get(
        "experience",
        ""
    ).strip():

        breakdown["experience"] = 20

    # ------------------------
    # Projects
    # ------------------------

    projects = sections.get(
        "projects",
        ""
    )

    if projects.strip():

        project_length = len(
            projects.split()
        )

        if project_length > 100:

            breakdown["projects"] = 25

        else:

            breakdown["projects"] = 15

    # ------------------------
    # Certifications
    # ------------------------

    if sections.get(
        "certifications",
        ""
    ).strip():

        breakdown[
            "certifications"
        ] = 10

    resume_score = sum(
        breakdown.values()
    )

    # ==================================
    # ATS SCORE
    # ==================================

    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill.lower() in [

            s.lower()

            for s in skills
        ]:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    if len(required_skills) > 0:

        keyword_match_percent = (

            len(matched_skills)

            /

            len(required_skills)

        ) * 100

    else:

        keyword_match_percent = 0

    ats_score = round(

        (keyword_match_percent * 0.6)

        +

        (resume_score * 0.4)

    )

    # ==================================
    # Recommendations
    # ==================================

    recommendations = []

    if len(
        missing_skills
    ) > 0:

        recommendations.append(

            "Add missing skills relevant to the target role."
        )

    if not sections.get(
        "projects",
        ""
    ):

        recommendations.append(

            "Add project descriptions with measurable impact."
        )

    if not sections.get(
        "experience",
        ""
    ):

        recommendations.append(

            "Add internship or practical experience."
        )

    ats_analysis = {

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "keyword_match_percent":
            round(
                keyword_match_percent,
                2
            ),

        "recommendations":
            recommendations
    }

    return (

        resume_score,

        ats_score,

        breakdown,

        ats_analysis
    )