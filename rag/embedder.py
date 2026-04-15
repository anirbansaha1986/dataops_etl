from sentence_transformers import SentenceTransformer
from utils.logger import get_logger

logger = get_logger("EMBEDDER")

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts):
    if not texts:
        logger.warning("Empty texts for embedding")
        return []

    logger.info(f"Generating embeddings for {len(texts)} texts")
    return model.encode(texts).tolist()