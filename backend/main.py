from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import uuid
import uvicorn

from retrieval import retrieve
from generator import generate_answer
from ingestion import build_index_for_upload

print("Starting full RAG application...")

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
    try:
        context, unique_sources, diagnostics = retrieve(
            query=request.question, kb_name=request.kb_name
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    answer = generate_answer(context, request.question)

    return {
        "answer": answer,
        "sources": unique_sources,
        "diagnostics": diagnostics,
    }


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):

    kb_id = str(uuid.uuid4())

    upload_folder = os.path.join("indexes", kb_id)
    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        file_location = os.path.join(upload_folder, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

    build_index_for_upload(upload_folder)

    return {"message": "Upload successful", "kb_id": kb_id}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("Launching Uvicorn on port:", port)
    uvicorn.run(app, host="0.0.0.0", port=port)
