import os
import time
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def generate_answer(question, results):

    context = ""

    for result in results:
        context += (
            f"\n--- Page {result['page']} ---\n"
            f"{result['text']}\n"
        )

    prompt = f"""
You are FinSight, a financial research assistant.

Answer the user's question using ONLY the
information provided in the context below.

Do not invent facts or financial information.

If the context does not contain enough
information to answer the question, say:

"I don't have enough information in the
provided financial report."

Always mention the relevant page numbers
when making factual claims.

CONTEXT:
{context}

USER QUESTION:
{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("==================================\n")

        return (
            f"Gemini API Error: {type(e).__name__}: {str(e)}"
        )