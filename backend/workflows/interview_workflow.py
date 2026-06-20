from typing import TypedDict


from typing import TypedDict


class PlacementState(
    TypedDict,
    total=False
):

    resume_text: str

    target_role: str

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

from backend.agents.resume_agent import (
    extract_sections
)


def section_node(
    state
):

    sections = extract_sections(

        state["resume_text"]
    )

    return {

        "sections":
        sections
    }
    
from backend.agents.skill_agent import (
    extract_skills
)


def skill_node(
    state
):

    skills_section = (

        state["sections"]
        .get(
            "skills",
            ""
        )
    )

    skills = extract_skills(
        skills_section
    )

    return {

        "skills":
        skills
    }

from backend.agents.resume_agent import (
    create_candidate_profile
)

def profile_node(
    state
):

    profile = create_candidate_profile(

        file_name=
            state.get(
                "file_name",
                "Resume"
            ),

        sections=
            state["sections"],

        skills=
            state["skills"]
    )

    return {

        "profile":
            profile
    }

from backend.agents.resume_agent import (
    generate_resume_stats
)

def stats_node(
    state
):

    stats = generate_resume_stats(

        state["sections"],

        state["skills"]
    )

    return {

        "stats":
            stats
    }



from backend.agents.scoring_agent import (
    calculate_resume_score
)

def ats_node(
    state
):

    resume_score, ats_score, breakdown, ats_analysis = (

        calculate_resume_score(

            state["sections"],

            state["skills"],

            state["target_role"]
        )
    )

    return {

        "resume_score":
            resume_score,

        "ats_score":
            ats_score,

        "score_breakdown":
            breakdown,

        "ats_analysis":
            ats_analysis
    }

from backend.agents.skill_gap_agent import (
    SkillGapAgent
)

from backend.config.role_loader import (
    load_role_skills
)


def skill_gap_node(
    state
):

    role_skills = load_role_skills()

    target_skills = role_skills.get(

        state["target_role"],

        []
    )

    agent = SkillGapAgent()

    result = agent.analyze_skill_gap(

        resume_skills=
        state["skills"],

        target_skills=
        target_skills,

        target_role=
        state["target_role"]
    )

    return {

        "skill_gap":
        result
    }
    
from backend.agents.resume_improvement_agent import (
    generate_resume_improvements
)


def improvement_node(
    state
):

    improvements = (

        generate_resume_improvements(

            state["sections"],

            state["skills"],

            state["target_role"]
        )
    )

    return {

        "resume_improvements":
        improvements
    }

def question_node(
    state
):

    from backend.agents.question_agent import (
        generate_questions
    )

    questions = generate_questions(

        state["skills"],

        state["target_role"],

        {}
    )

    return {

        "questions":
        questions
    }

from langgraph.graph import (
    StateGraph,
    END
)

workflow = StateGraph(
    PlacementState
)

workflow.add_node(
    "sections",
    section_node
)

workflow.add_node(
    "skills",
    skill_node
)

workflow.add_node(
    "profile",
    profile_node
)

workflow.add_node(
    "stats",
    stats_node
)

workflow.add_node(
    "ats",
    ats_node
)

workflow.add_node(
    "skill_gap",
    skill_gap_node
)

workflow.add_node(
    "improvements",
    improvement_node
)

workflow.add_node(
    "questions",
    question_node
)

workflow.set_entry_point(
    "sections"
)

workflow.add_edge(
    "sections",
    "skills"
)

workflow.add_edge(
    "skills",
    "profile"
)

workflow.add_edge(
    "profile",
    "stats"
)

workflow.add_edge(
    "stats",
    "ats"
)

workflow.add_edge(
    "ats",
    "skill_gap"
)

workflow.add_edge(
    "skill_gap",
    "improvements"
)

workflow.add_edge(
    "improvements",
    "questions"
)

workflow.add_edge(
    "questions",
    END
)

graph = workflow.compile()
