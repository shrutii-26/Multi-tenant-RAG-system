from openai import OpenAI
from config import GROQ_API_KEY, MODEL_NAME

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are a research assistant.

Answer the question strictly using the provided context.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Answer using only provided context."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
