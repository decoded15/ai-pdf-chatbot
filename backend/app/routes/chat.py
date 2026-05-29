from fastapi import APIRouter

from app.services.retrieval_service import (
    retrieve_relevant_chunks
)

from app.services.rag_service import (
    generate_response
)

router = APIRouter()


@router.get("/chat")
def chat(query: str):

    retrieved_chunks = retrieve_relevant_chunks(
        query
    )

    response = generate_response(
        query,
        retrieved_chunks
    )

    return {
        "query": query,
        "response": response,
        "retrieved_chunks": retrieved_chunks
    }