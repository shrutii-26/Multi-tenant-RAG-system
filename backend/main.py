from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import uuid
from fastapi import UploadFile, File
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


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        # Unique knowledge base ID
        kb_id = str(uuid.uuid4())

        upload_folder = os.path.join("indexes", kb_id)
        os.makedirs(upload_folder, exist_ok=True)

        # Save all uploaded files
        for file in files:
            if not file.filename.lower().endswith(".pdf"):
                raise ValueError("Only PDF files are supported.")

            file_location = os.path.join(upload_folder, file.filename)

            with open(file_location, "wb") as f:
                content = await file.read()
                f.write(content)

        # Build FAISS index from uploaded folder
        build_index_for_upload(upload_folder)

        return {
            "message": "Upload successful",
            "kb_id": kb_id,
            "files_uploaded": [file.filename for file in files],
        }

    except Exception as e:
        import traceback

        traceback.print_exc()
        return {"error": str(e)}


print("UPLOAD ENDPOINT LOADED")
