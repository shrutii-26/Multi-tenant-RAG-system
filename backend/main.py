import traceback
import sys

print("=== APP STARTING ===")

try:
    from fastapi import FastAPI, UploadFile, File, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List
    import os
    import uuid
    import uvicorn

    print("Imports stage 1 OK")

    from retrieval import retrieve

    print("retrieval imported")

    from generator import generate_answer

    print("generator imported")

    from ingestion import build_index_for_upload

    print("ingestion imported")

except Exception as e:
    print("IMPORT ERROR:")
    traceback.print_exc()
    sys.exit(1)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "RAG API running"}
