import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = url = (
    "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2"
)

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def get_embeddings(texts):
    response = requests.post(API_URL, headers=headers, json={"inputs": texts})

    if response.status_code != 200:
        raise Exception(f"HF API Error: {response.text}")

    return response.json()
