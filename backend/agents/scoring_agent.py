"""
PlacementGPT-AI
Advanced Resume Scoring Agent
"""

import json
from groq import Groq
from backend.config.settings import GROQ_API_KEY
from backend.models.semantic_matcher import SemanticMatcher
from backend.config.role_loader import load_role_skills

client = Groq(api_key=GROQ_API_KEY)

def _get_llm_ats_score(sections, skills, target_role, required_skills, semantic_matches, semantic_missing):
    prompt = f"""
You are an expert ATS (Applicant Tracking System) and technical recruiter.
Evaluate the candidate's resume for the role of: {target_role}.

Required Skills for the role: {json.dumps(required_skills)}
Candidate's detected skills: {json.dumps(skills)}
Candidate's experience/projects sections context: {json.dumps({k: v[:500] for k, v in sections.items() if k in ['experience', 'projects']})}

We have already performed a semantic analysis of the skills.
Semantically Matched Skills: {json.dumps(semantic_matches)}
Semantically Missing Skills: {json.dumps(semantic_missing)}

Evaluate how well the candidate matches the role based on this semantic analysis and their contextual experience.
Provide an ATS Score from 0 to 100. (Base it heavily on the semantic matches, but adjust based on experience context).
Also provide refined lists of matched skills, missing skills, and recommendations.

Return ONLY valid JSON in this exact format:
{{
    "ats_score": 85,
    "matched_skills": ["skill1", "skill2"],
    "missing_skills": ["skill3"],
    "recommendations": ["Recommendation 1", "Recommendation 2"]
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"LLM ATS Scoring failed: {e}")
        return None



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
    # ATS SCORE (Hybrid: Semantic + LLM)
    # ==================================
    
    matcher = SemanticMatcher()
    semantic_result = matcher.match_skills(skills, required_skills)
    
    matched_skills = [item["target_skill"] for item in semantic_result.get("matched", [])]
    missing_skills = [item["target_skill"] for item in semantic_result.get("missing", [])]

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

    # Use LLM for refined ATS scoring and recommendations
    llm_result = _get_llm_ats_score(sections, skills, target_role, required_skills, matched_skills, missing_skills)
    if llm_result is not None:
        ats_score = llm_result.get("ats_score", ats_score)
        matched_skills = llm_result.get("matched_skills", matched_skills)
        missing_skills = llm_result.get("missing_skills", missing_skills)
        recommendations = llm_result.get("recommendations", recommendations)
        if len(required_skills) > 0:
            keyword_match_percent = (len(matched_skills) / len(required_skills)) * 100
        else:
            keyword_match_percent = 0

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