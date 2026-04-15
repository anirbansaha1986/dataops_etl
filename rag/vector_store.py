import chromadb
import os

# =========================
# FORCE ABSOLUTE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "chroma_store")

print("📁 DB PATH:", DB_PATH)

# =========================
# ✅ USE PERSISTENT CLIENT
# =========================
client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(name="fraud_data")

print("📦 COLLECTION INITIAL COUNT:", collection.count())


# =========================
# ADD DOCUMENTS
# =========================
def add_documents(texts, embeddings, ids, metadatas):

    if not texts or not embeddings:
        print("❌ No data to insert")
        return

    print(f"Adding {len(texts)} documents...")

    batch_size = 1000

    for i in range(0, len(texts), batch_size):
        collection.add(
            documents=texts[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            ids=ids[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )

    print("✅ AFTER INSERT COUNT:", collection.count())