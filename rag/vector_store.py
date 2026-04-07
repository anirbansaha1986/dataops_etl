import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="etl_logs"
)

def add_documents(texts, embeddings, ids):
    if not texts or not embeddings:
        print("Skipping ingestion due to empty embeddings")
        return

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )