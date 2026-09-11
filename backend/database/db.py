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
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    # Test each pooled connection with a lightweight ping before using it, and
    # proactively recycle connections older than 5 minutes. This prevents
    # "OperationalError: server closed the connection unexpectedly" style
    # failures that happen when a managed Postgres provider (Supabase, Neon,
    # Render, etc.) or a pgbouncer in front of it drops idle connections that
    # SQLAlchemy's pool doesn't know are dead yet.
    pool_pre_ping=True,
    pool_recycle=280,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()