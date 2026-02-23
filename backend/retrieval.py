import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import TOP_K

from embedding_model import model


def retrieve(query: str, kb_name: str):
    folder_path = os.path.join("indexes", kb_name)

    if not os.path.exists(folder_path):
        raise ValueError("Knowledge base not found.")

    index = faiss.read_index(os.path.join(folder_path, "index.faiss"))

    with open(os.path.join(folder_path, "chunks.txt"), "r", encoding="utf-8") as f:
        raw = f.read()
        chunks = raw.split("\n===CHUNK===\n")

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, TOP_K)

    retrieved_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

    context = "\n".join(retrieved_chunks)

    return context, [], {"distances": distances.tolist()}
