import os
import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from config import CHUNK_SIZE, OVERLAP

model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def build_index_for_upload(folder_path):
    texts = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder_path, file_name))
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() or ""
            texts.extend(chunk_text(full_text))

    if not texts:
        raise ValueError("No valid PDF content found.")

    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, os.path.join(folder_path, "index.faiss"))

    # Save chunks
    with open(os.path.join(folder_path, "chunks.txt"), "w", encoding="utf-8") as f:
        for chunk in texts:
            f.write(chunk.replace("\n", " ") + "\n===CHUNK===\n")
