from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from retrieval import retrieve
from generator import generate_answer
import json
from fastapi import FastAPI, UploadFile, File
from typing import List
import os
import uuid
from ingestion import build_index_for_upload
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware


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


@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        context, unique_sources, diagnostics = retrieve(
            query=request.question, kb_name=request.kb_name
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    answer = generate_answer(context, request.question)

    return {"answer": answer, "sources": unique_sources, "diagnostics": diagnostics}


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):

    kb_id = str(uuid.uuid4())

    upload_folder = os.path.join("indexes", kb_id)
    os.makedirs(upload_folder, exist_ok=True)

    file_paths = []

    for file in files:
        file_location = os.path.join(upload_folder, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        file_paths.append(file_location)

    # Build FAISS index
    build_index_for_upload(upload_folder)

    return {"message": "Upload successful", "kb_id": kb_id}
