from embedding_model import get_model


def get_embeddings(texts):
    model = get_model()
    embeddings = model.encode(texts)
    return embeddings.tolist()
