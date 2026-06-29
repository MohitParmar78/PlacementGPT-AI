from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime

from .db import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    target_role = Column(String, index=True)
    
    # Scores
    overall_score = Column(Float)
    technical_score = Column(Float)
    communication_score = Column(Float)
    readiness = Column(String)
    
    # Complex JSON fields stored as strings
    strengths = Column(Text) 
    weaknesses = Column(Text)
    improvement_suggestions = Column(Text)
    learning_roadmap = Column(Text)
    question_feedback = Column(Text) 
    
    created_at = Column(DateTime, default=datetime.utcnow)
