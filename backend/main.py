from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import os
import uuid

from ingestion import build_index_for_upload
from retrieval import retrieve
from generator import generate_answer

BASE_DIR = os.path.dirname(__file__)
INDEX_DIR = os.path.join(BASE_DIR, "indexes")

# Ensure indexes folder exists
os.makedirs(INDEX_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "RAG API running"}


class QueryRequest(BaseModel):
    question: str
    kb_name: str


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    kb_id = str(uuid.uuid4())

    # Temporary upload folder
    upload_folder = os.path.join(INDEX_DIR, kb_id)
    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDFs allowed.")

        file_location = os.path.join(upload_folder, file.filename)

        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

    # IMPORTANT: pass both folder + kb_id
    build_index_for_upload(upload_folder, kb_id)

    return {
        "message": "Upload successful",
        "kb_id": kb_id,
    }


@app.post("/query")
def query_rag(request: QueryRequest):
    context, _, diagnostics = retrieve(
        query=request.question,
        kb_name=request.kb_name,
    )

    answer = generate_answer(context, request.question)

    return {
        "answer": answer,
        "diagnostics": diagnostics,
    }
