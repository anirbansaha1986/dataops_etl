from rag.vector_store import collection
from rag.embedder import generate_embeddings
from utils.logger import get_logger

logger = get_logger("RETRIEVER")


def retrieve_context(query):

    logger.info(f"Retrieval query: {query}")

    if collection.count() == 0:
        logger.warning("ChromaDB is empty")
        return []

    embedding = generate_embeddings([query])

    results = collection.query(
        query_embeddings=embedding,
        n_results=3
    )

    docs = results.get("documents", [[]])[0]

    if not docs:
        logger.warning("No documents retrieved")
        return []

    logger.info(f"Retrieved {len(docs)} documents")

    return docs