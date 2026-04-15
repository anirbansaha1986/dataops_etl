import pandas as pd
from rag.embedder import generate_embeddings
from rag.vector_store import add_documents, collection
from rag.fraud_rules import generate_signals
from utils.logger import get_logger

logger = get_logger("INGEST")


def ingest_credit_data():

    logger.info("🚀 Starting ingestion...")

    # =========================
    # 1. LOAD DATA
    # =========================
    df = pd.read_csv("data/creditcard.csv")

    logger.info(f"Dataset loaded with {len(df)} rows")

    # =========================
    # 2. FILTER (IMPORTANT)
    # =========================
    df = df[df["Class"] == 1]   # only fraud

    logger.info(f"Fraud records: {len(df)}")

    if len(df) == 0:
        logger.error("❌ No fraud records found!")
        return

    # =========================
    # 3. BUILD DOCUMENTS
    # =========================
    texts = []
    ids = []
    metadatas = []

    for i, row in df.iterrows():

        signals = generate_signals(row)

        text = f"""
Transaction Summary:
- Amount: {row['Amount']}
- Time: {row['Time']}

Fraud Signals:
{', '.join(signals) if signals else 'No strong signals'}

Feature Snapshot:
V1={row['V1']}, V2={row['V2']}, V3={row['V3']}, V14={row['V14']}, V17={row['V17']}
"""

        texts.append(text.strip())
        ids.append(f"tx_{i}")

        metadatas.append({
            "Amount": float(row["Amount"]),
            "Class": int(row["Class"])
        })

    logger.info(f"Prepared {len(texts)} documents")

    # =========================
    # 4. EMBEDDINGS
    # =========================
    embeddings = generate_embeddings(texts)

    if not embeddings:
        logger.error("❌ Embeddings generation failed!")
        return

    logger.info(f"Generated {len(embeddings)} embeddings")

    # =========================
    # 5. STORE IN CHROMA
    # =========================
    add_documents(texts, embeddings, ids, metadatas)

    # =========================
    # 6. VERIFY STORAGE
    # =========================
    count = collection.count()

    logger.info(f"📦 Total documents in ChromaDB: {count}")

    if count == 0:
        logger.error("❌ Ingestion failed — DB is empty")
    else:
        logger.info("✅ Ingestion successful")