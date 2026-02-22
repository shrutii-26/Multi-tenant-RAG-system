import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables.")

MODEL_NAME = "llama-3.1-8b-instant"

CHUNK_SIZE = 300
OVERLAP = 60
TOP_K = 4
