# Load environment variables
from dotenv import load_dotenv

# Access environment variables
import os

# Read .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# ChromaDB
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")