from openai import OpenAI
import os
from config import MODEL_NAME


def generate_answer(context, question):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not set.")

    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    prompt = f"""
    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Answer using the provided context only."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
