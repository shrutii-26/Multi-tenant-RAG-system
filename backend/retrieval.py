import os
import faiss
import numpy as np
from embeddings import get_embeddings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def retrieve(query: str, kb_name: str, top_k: int = 4):

    index_path = os.path.join(BASE_DIR, "indexes", kb_name, "index.faiss")
    metadata_path = os.path.join(BASE_DIR, "indexes", kb_name, "metadata.npy")

    if not os.path.exists(index_path):
        raise ValueError(f"Knowledge base not found at {index_path}")

    # Load index and metadata
    index = faiss.read_index(index_path)
    metadata = np.load(metadata_path, allow_pickle=True)

    # Embed query using HuggingFace API
    query_embedding = get_embeddings([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search
    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = []
    unique_sources = set()
    diagnostics = []

    for rank, idx in enumerate(indices[0]):
        chunk_data = metadata[idx]
        retrieved_chunks.append(chunk_data["content"])
        unique_sources.add(chunk_data["source"])

        diagnostics.append(
            {
                "rank": rank + 1,
                "source": chunk_data["source"],
                "distance": float(distances[0][rank]),
            }
        )

    context = "\n\n".join(retrieved_chunks)

    return context, list(unique_sources), diagnostics
