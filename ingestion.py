import os
import faiss
import numpy as np
from PyPDF2 import PdfReader
from config import CHUNK_SIZE, OVERLAP
from embedding_model import get_model

BASE_DIR = os.path.dirname(__file__)
INDEX_DIR = os.path.join(BASE_DIR, "indexes")

# Ensure indexes directory exists
os.makedirs(INDEX_DIR, exist_ok=True)


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def build_index_for_upload(upload_folder, kb_id):
    """
    upload_folder = temporary folder where PDFs are saved
    kb_id = unique knowledge base id
    """

    texts = []

    for file_name in os.listdir(upload_folder):
        if file_name.endswith(".pdf"):
            reader = PdfReader(os.path.join(upload_folder, file_name))
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() or ""
            texts.extend(chunk_text(full_text))

    if not texts:
        raise ValueError("No valid PDF content found.")

    model = get_model()
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Create permanent KB folder inside backend/indexes
    kb_path = os.path.join(INDEX_DIR, kb_id)
    os.makedirs(kb_path, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, os.path.join(kb_path, "index.faiss"))

    # Save chunks
    with open(os.path.join(kb_path, "chunks.txt"), "w", encoding="utf-8") as f:
        for chunk in texts:
            f.write(chunk.replace("\n", " ") + "\n===CHUNK===\n")
