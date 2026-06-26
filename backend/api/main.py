# FastAPI imports
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from pydantic import BaseModel
from typing import List

# Import save service
from backend.services.file_service import save_uploaded_file
from backend.services.resume_parser import (
    extract_text_from_pdf
)
from backend.agents.resume_agent import (
    clean_resume_text,
)
from backend.agents.interview_agent import (
    evaluate_interview
)
from backend.agents.followup_question_agent import (
    generate_followup_question
)
from backend.workflows.interview_workflow import (
    graph
)

# Create app
app = FastAPI(
    title="PlacementGPT-AI API"
)



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
    

@app.post("/evaluate-interview")
def evaluate_interview_api(
    request: InterviewRequest
):

    interview_data = [

        item.model_dump()

        for item in request.interview
    ]

    feedback = evaluate_interview(

        request.target_role,

        interview_data
    )

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