import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"

CHUNK_SIZE = 300
OVERLAP = 60
TOP_K = 4
