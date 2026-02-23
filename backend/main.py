from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import os
import uuid

from ingestion import build_index_for_upload
from retrieval import retrieve
from generator import generate_answer

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

    folder_path = os.path.join("indexes", kb_id)
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDFs allowed.")

        file_location = os.path.join(folder_path, file.filename)

        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

    build_index_for_upload(folder_path)

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
