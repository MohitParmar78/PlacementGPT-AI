from typing import TypedDict


class PlacementState(
    TypedDict,
    total=False
):

    resume_text: str
    target_role: str
    difficulty: str
    is_valid: bool
    sections: dict
    skills: list
    stats: dict
    profile: dict
    resume_score: int
    ats_score: int
    score_breakdown: dict
    ats_analysis: dict
    skill_gap: dict
    resume_improvements: dict
    questions: list

from backend.agents.resume_agent import extract_sections

def section_node(state):
    sections = extract_sections(state["resume_text"])
    return {"sections": sections}
    
from backend.agents.skill_agent import extract_skills

def skill_node(state):
    skills_section = state["sections"].get("skills", "")
    skills = extract_skills(skills_section)
    return {"skills": skills}

def verification_node(state):
    sections = state.get("sections", {})
    skills = state.get("skills", [])
    
    # Check if there is meaningful data parsed
    is_valid = True
    if not skills and not sections.get("experience", "").strip() and not sections.get("education", "").strip():
        is_valid = False
        
    return {"is_valid": is_valid}

def check_validity(state):
    if state.get("is_valid", True):
        return "valid"
    return "invalid"

def dispatch_node(state):
    # Dummy node to fan-out from
    return {}

def fallback_node(state):
    # Safe defaults if resume is unparsable
    return {
        "profile": {"total_skills": 0, "skills": []},
        "resume_score": 0,
        "ats_score": 0,
        "score_breakdown": {"skills": 0, "projects": 0, "education": 0, "experience": 0, "certifications": 0},
        "ats_analysis": {"matched_skills": [], "missing_skills": [], "recommendations": ["Upload a readable resume."]},
        "skill_gap": {"missing_skills": [], "required_skills": []},
        "resume_improvements": {},
        "questions": [],
        "stats": {"skills_count": 0, "education_found": False, "experience_found": False, "certifications_found": False}
    }

from backend.agents.resume_agent import create_candidate_profile

def profile_node(state):
    profile = create_candidate_profile(
        file_name=state.get("file_name", "Resume"),
        sections=state["sections"],
        skills=state["skills"]
    )
    return {"profile": profile}

from backend.agents.resume_agent import generate_resume_stats

def stats_node(state):
    stats = generate_resume_stats(state["sections"], state["skills"])
    return {"stats": stats}

from backend.agents.scoring_agent import calculate_resume_score

def ats_node(state):
    resume_score, ats_score, breakdown, ats_analysis = calculate_resume_score(
        state["sections"],
        state["skills"],
        state["target_role"]
    )
    return {
        "resume_score": resume_score,
        "ats_score": ats_score,
        "score_breakdown": breakdown,
        "ats_analysis": ats_analysis
    }

from backend.agents.skill_gap_agent import SkillGapAgent
from backend.config.role_loader import load_role_skills

def skill_gap_node(state):
    role_skills = load_role_skills()
    target_skills = role_skills.get(state["target_role"], [])
    agent = SkillGapAgent()
    result = agent.analyze_skill_gap(
        resume_skills=state["skills"],
        target_skills=target_skills,
        target_role=state["target_role"]
    )
    return {"skill_gap": result}

def aggregator_node(state):
    # Dummy node to fan-in to before proceeding
    return {}
    
from backend.agents.resume_improvement_agent import generate_resume_improvements

def improvement_node(state):
    improvements = generate_resume_improvements(
        target_role=state["target_role"],
        sections=state["sections"],
        skills=state["skills"]
    )
    return {"resume_improvements": improvements}

def question_node(state):
    from backend.agents.question_agent import generate_questions
    questions = generate_questions(
        skills=state["skills"],
        target_role=state["target_role"],
        sections=state.get("sections", {}),
        difficulty=state.get("difficulty", "Medium")
    )
    return {"questions": questions}

from langgraph.graph import StateGraph, END

workflow = StateGraph(PlacementState)

# Add Nodes
workflow.add_node("sections", section_node)
workflow.add_node("skills", skill_node)
workflow.add_node("verification", verification_node)
workflow.add_node("dispatch", dispatch_node)
workflow.add_node("fallback", fallback_node)

workflow.add_node("profile", profile_node)
workflow.add_node("stats", stats_node)
workflow.add_node("ats", ats_node)
workflow.add_node("skill_gap", skill_gap_node)

workflow.add_node("aggregator", aggregator_node)
workflow.add_node("improvements", improvement_node)
workflow.add_node("questions", question_node)

workflow.set_entry_point("sections")

# Routing logic
workflow.add_edge("sections", "skills")
workflow.add_edge("skills", "verification")

workflow.add_conditional_edges(
    "verification",
    check_validity,
    {
        "valid": "dispatch",
        "invalid": "fallback"
    }
)

# Fan Out (Parallel Execution)
workflow.add_edge("dispatch", "profile")
workflow.add_edge("dispatch", "stats")
workflow.add_edge("dispatch", "ats")
workflow.add_edge("dispatch", "skill_gap")

# Fan In (Aggregation)
workflow.add_edge("profile", "aggregator")
workflow.add_edge("stats", "aggregator")
workflow.add_edge("ats", "aggregator")
workflow.add_edge("skill_gap", "aggregator")

# Proceed
workflow.add_edge("aggregator", "improvements")
workflow.add_edge("improvements", "questions")

workflow.add_edge("questions", END)
workflow.add_edge("fallback", END)

graph = workflow.compile()
