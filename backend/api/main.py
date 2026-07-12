# FastAPI imports
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from pydantic import BaseModel
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database.db import engine, Base, get_db
from backend.services.memory_service import save_interview_session, get_interview_history

# Import save service
from backend.services.file_service import save_uploaded_file
from backend.services.resume_parser import (
    extract_text_from_pdf
)
from backend.agents.resume_agent import (
    clean_resume_text,
    extract_sections,
    create_candidate_profile
)
from backend.agents.skill_agent import (
    extract_skills
)
from backend.agents.resume_agent import (
    generate_resume_stats
)
from backend.agents.scoring_agent import (
    calculate_resume_score
)
from backend.agents.skill_gap_agent import (
    SkillGapAgent
)
from backend.agents.question_agent import (
    generate_questions
)
from backend.agents.interview_agent import (
    evaluate_interview
)
from backend.config.role_loader import (
    load_role_skills
)
from backend.agents.resume_improvement_agent import (
    generate_resume_improvements
)
from backend.agents.followup_question_agent import (
    generate_followup_question
)
from backend.workflows.interview_workflow import (
    graph
)
from backend.agents.compare_agent import (
    generate_resume_comparison
)

# Create app
app = FastAPI(
    title="PlacementGPT-AI API"
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

skill_gap_agent = SkillGapAgent()

class InterviewItem(
    BaseModel
):

    question: str

    skill: str

    answer: str
    
class InterviewRequest(
    BaseModel
):

    target_role: str

    interview: List[InterviewItem]
    
class FollowupRequest(
    BaseModel
):

    question: str

    answer: str

    skill: str

    target_role: str


@app.get("/")
def home():
    """
    Health check endpoint.
    """

    return {
        "message": "Backend Running"
    }
    
@app.post("/analyze-resume")
def analyze_resume(

    resume: UploadFile = File(...),

    target_role: str = Form(...),
    
    difficulty: str = Form(
        "Medium"
    )
):

    # Save uploaded PDF
    file_path = save_uploaded_file(
        resume
    )

    # Extract text
    raw_text = extract_text_from_pdf(
        file_path
    )

    # Clean text
    cleaned_text = clean_resume_text(
        raw_text
    )

    result = graph.invoke(

        {

            "resume_text":
                cleaned_text,

            "target_role":
                target_role,
                
            "difficulty":
                difficulty,

            "file_name":
                resume.filename
        }
    )

    return {

    "status":
        "success",

    "target_role":
        target_role,

    "sections":
        result["sections"],

    "skills":
        result["skills"],
        
    
     "stats":
        result["stats"],


    "resume_score":
        result["resume_score"],

    "ats_score":
        result["ats_score"],

    "score_breakdown":
        result["score_breakdown"],

    "ats_analysis":
        result["ats_analysis"],

    "skill_gap":
        result["skill_gap"],

    "resume_improvements":
        result[
            "resume_improvements"
        ],
    
     "profile":
        result["profile"],

    "questions":
        result["questions"],

    "resume_text":
        cleaned_text
}
    

class CompareRequest(BaseModel):
    target_role: str
    resume_a_data: dict
    resume_b_data: dict

@app.post("/compare-resumes-llm")
def compare_resumes_llm_api(request: CompareRequest):
    comparison = generate_resume_comparison(
        target_role=request.target_role,
        resume_a_data=request.resume_a_data,
        resume_b_data=request.resume_b_data
    )
    return comparison

@app.post("/evaluate-interview")
def evaluate_interview_api(
    request: InterviewRequest,
    db: Session = Depends(get_db)
):
    print("=" * 80)
    print("REQUEST RECEIVED")
    print(request)
    print("=" * 80)

    interview_data = [

        item.model_dump()

        for item in request.interview
    ]

    feedback = evaluate_interview(

        request.target_role,

        interview_data
    )

    # Save session to persistent memory
    save_interview_session(db, request.target_role, feedback)

    return feedback

@app.post(
    "/generate-followup"
)
def generate_followup_api(
    request: FollowupRequest
):

    return generate_followup_question(

        original_question=
            request.question,

        answer=
            request.answer,

        skill=
            request.skill,

        target_role=
            request.target_role
    )

@app.get("/history")
def get_history_api(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Fetch past interview sessions from the database."""
    return get_interview_history(db, limit)