from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import uuid

from retrieval import retrieve
from generator import generate_answer
from ingestion import build_index_for_upload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str
    kb_name: str


@app.get("/")
def root():
    return {"status": "RAG API running"}


@app.post("/query")
def query_rag(request: QueryRequest):
    context, unique_sources, diagnostics = retrieve(
        query=request.question, kb_name=request.kb_name
    )

    answer = generate_answer(context, request.question)

    return {"answer": answer, "sources": unique_sources, "diagnostics": diagnostics}


from fastapi import UploadFile, File
from typing import Annotated, List


@app.post("/upload")
async def upload_files(
    files: Annotated[List[UploadFile], File(description="Multiple files")],
):
    kb_id = str(uuid.uuid4())
    upload_folder = os.path.join("indexes", kb_id)
    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        content = await file.read()
        with open(os.path.join(upload_folder, file.filename), "wb") as f:
            f.write(content)

    build_index_for_upload(upload_folder)

    return {
        "message": "Upload successful",
        "kb_id": kb_id,
        "files_uploaded": [file.filename for file in files],
    }
