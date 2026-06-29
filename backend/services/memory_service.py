import json
from sqlalchemy.orm import Session
from backend.database.models import InterviewSession

def save_interview_session(db: Session, target_role: str, feedback: dict):
    """
    Saves an interview session and its feedback to the database.
    """
    db_session = InterviewSession(
        target_role=target_role,
        overall_score=feedback.get("overall_score", 0),
        technical_score=feedback.get("technical_score", 0),
        communication_score=feedback.get("communication_score", 0),
        readiness=feedback.get("readiness", "Unknown"),
        strengths=json.dumps(feedback.get("strengths", [])),
        weaknesses=json.dumps(feedback.get("weaknesses", [])),
        improvement_suggestions=json.dumps(feedback.get("improvement_suggestions", [])),
        learning_roadmap=json.dumps(feedback.get("learning_roadmap", [])),
        question_feedback=json.dumps(feedback.get("question_feedback", []))
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_interview_history(db: Session, limit: int = 10):
    """
    Retrieves the most recent interview sessions.
    """
    sessions = db.query(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(limit).all()
    
    history = []
    for s in sessions:
        history.append({
            "id": s.id,
            "target_role": s.target_role,
            "overall_score": s.overall_score,
            "technical_score": s.technical_score,
            "communication_score": s.communication_score,
            "readiness": s.readiness,
            "created_at": s.created_at.isoformat(),
            # Load JSON back to lists/dicts
            "strengths": json.loads(s.strengths) if s.strengths else [],
            "weaknesses": json.loads(s.weaknesses) if s.weaknesses else [],
            "improvement_suggestions": json.loads(s.improvement_suggestions) if s.improvement_suggestions else [],
            "learning_roadmap": json.loads(s.learning_roadmap) if s.learning_roadmap else [],
            "question_feedback": json.loads(s.question_feedback) if s.question_feedback else []
        })
        
    return history
