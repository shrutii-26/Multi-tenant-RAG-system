import os
import faiss
import numpy as np
from config import TOP_K
from embedding_model import get_model

BASE_DIR = os.path.dirname(__file__)
INDEX_DIR = os.path.join(BASE_DIR, "indexes")


def retrieve(query: str, kb_name: str):

    # Use absolute deterministic path
    folder_path = os.path.join(INDEX_DIR, kb_name)

    if not os.path.exists(folder_path):
        raise ValueError(f"Knowledge base not found at {folder_path}")

    index_path = os.path.join(folder_path, "index.faiss")
    chunks_path = os.path.join(folder_path, "chunks.txt")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise ValueError("Index files missing.")

    index = faiss.read_index(index_path)

    with open(chunks_path, "r", encoding="utf-8") as f:
        raw = f.read()
        chunks = raw.split("\n===CHUNK===\n")

    model = get_model()
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, TOP_K)

    retrieved_chunks = [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]

    context = "\n".join(retrieved_chunks)

    return context, retrieved_chunks, {"distances": distances.tolist()}
