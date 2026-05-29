import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def retrieve_relevant_chunks(query):

    index = faiss.read_index(
        "data/vector_store/faiss_index.index"
    )

    with open(
        "data/vector_store/chunks.pkl",
        "rb"
    ) as f:

        chunks = pickle.load(f)

    query_embedding = embedding_model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding),
        k=3
    )

    retrieved_chunks = []

    for idx in indices[0]:
        retrieved_chunks.append(chunks[idx])

    return retrieved_chunks