from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts):
    if not texts:
        return []
    embeddings = model.encode(texts).tolist()
    return embeddings