import faiss
import numpy as np
import pickle
import os


def store_embeddings(chunks, embeddings):

    os.makedirs("data/vector_store", exist_ok=True)

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    embedding_array = np.array(embeddings)

    index.add(embedding_array)

    faiss.write_index(
        index,
        "data/vector_store/faiss_index.index"
    )

    with open(
        "data/vector_store/chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(chunks, f)