from openai import OpenAI
from backend.config import GROQ_API_KEY, MODEL_NAME

# Create Groq-compatible OpenAI client
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")


def generate_answer(context: str, question: str) -> str:
    """
    Generates answer using Groq LLM based strictly on retrieved context.
    """

    prompt = f"""
You are a research assistant.

Answer the question strictly using the provided context.

Rules:
- Use only the given context.
- If relevant information is partially available, summarize it clearly.
- Only say "Not mentioned in the provided documents." if nothing relevant appears.
- Be concise but precise.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You answer questions using only provided documents.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
