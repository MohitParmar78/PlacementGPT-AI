import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Default to local SQLite for development
# For Streamlit Cloud deployment, set DATABASE_URL to a PostgreSQL URI (e.g. Supabase) in Streamlit Secrets
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/placementgpt.db")

# Ensure the data directory exists for sqlite
if DATABASE_URL.startswith("sqlite"):
    os.makedirs("./data", exist_ok=True)

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
