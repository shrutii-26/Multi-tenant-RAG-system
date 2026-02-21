import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from config import CHUNK_SIZE, OVERLAP

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def chunk_text(text: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


def build_index_for_upload(upload_folder: str):

    all_chunks = []
    metadata = []

    # Read all PDFs inside upload folder
    for file_name in os.listdir(upload_folder):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(upload_folder, file_name)

            text = extract_text_from_pdf(pdf_path)

            if not text:
                print(f"WARNING: No text extracted from {file_name}")
                continue

            chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)

            print(f"{file_name} -> Total chunks: {len(chunks)}")

            for chunk in chunks:
                all_chunks.append(chunk)
                metadata.append({"source": file_name, "content": chunk})

    # Safety guard
    if len(all_chunks) == 0:
        raise ValueError("No text chunks created. PDF may be image-based or empty.")

    # Generate embeddings
    embeddings = embedding_model.encode(all_chunks)
    embeddings = np.array(embeddings).astype("float32")

    # Safety guard
    if embeddings.shape[0] == 0:
        raise ValueError("No embeddings generated.")

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index
    faiss.write_index(index, os.path.join(upload_folder, "index.faiss"))

    # Save metadata
    np.save(os.path.join(upload_folder, "metadata.npy"), metadata)

    print("Index built successfully.")
