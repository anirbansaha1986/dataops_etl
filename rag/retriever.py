from rag.vector_store import collection
from rag.embedder import generate_embeddings


def retrieve_context(query):

    embedding = generate_embeddings([query])

    results = collection.query(
        query_embeddings=embedding,
        n_results=3
    )

    return results["documents"][0]