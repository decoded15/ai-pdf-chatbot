import google.generativeai as genai

from app.core.config import GOOGLE_API_KEY


genai.configure(
    api_key=GOOGLE_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_response(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    You are a helpful AI PDF assistant.

    Use ONLY the provided context
    to answer the user's question.

    Context:
    {context}

    Question:
    {query}
    """

    response = model.generate_content(prompt)

    return response.text