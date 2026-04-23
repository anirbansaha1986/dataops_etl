import os
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
    df = df[df["Class"] == 1].copy()   # only fraud

    logger.info(f"Fraud records: {len(df)}")

    if len(df) == 0:
        logger.error("❌ No fraud records found!")
        return

    # =========================
    # 3. FEATURE ENGINEERING
    # =========================
    df["abs_v14"] = df["V14"].abs()
    df["abs_v17"] = df["V17"].abs()

    df["is_micro_txn"] = (df["Amount"] < 1).astype(int)
    df["is_high_amount"] = (df["Amount"] > 500).astype(int)

    df["amount_bucket"] = pd.cut(
        df["Amount"],
        bins=[-0.01, 1, 50, 500, float("inf")],
        labels=["micro", "low", "medium", "high"],
        include_lowest=True
    )

    df["signal_list"] = df.apply(generate_signals, axis=1)
    df["signal_count"] = df["signal_list"].apply(len)
    df["signal_text"] = df["signal_list"].apply(
        lambda x: ", ".join(x) if x else "No strong signals"
    )

    df["risk_score_rule_based"] = (
        df["is_micro_txn"] * 20 +
        df["is_high_amount"] * 15 +
        (df["abs_v14"] > 5).astype(int) * 30 +
        (df["abs_v17"] > 5).astype(int) * 35
    )

    logger.info("✅ Feature engineering completed")

    # =========================
    # 4. FEATURE STORE EXPORT
    # =========================
    os.makedirs("data/feature_store", exist_ok=True)

    parquet_path = "data/feature_store/transactions_features.parquet"
    csv_fallback_path = "data/feature_store/transactions_features.csv"

    try:
        df.to_parquet(parquet_path, index=False)
        logger.info(f"📦 Feature store saved to Parquet: {parquet_path}")
    except Exception as e:
        logger.warning(f"Parquet export failed ({e}). Saving CSV fallback instead.")
        df.to_csv(csv_fallback_path, index=False)
        logger.info(f"📦 Feature store saved to CSV fallback: {csv_fallback_path}")

    # =========================
    # 5. BUILD DOCUMENTS FOR RAG
    # =========================
    texts = []
    ids = []
    metadatas = []

    for i, row in df.iterrows():

        text = f"""
Transaction Summary:
- Amount: {row['Amount']}
- Time: {row['Time']}
- Amount Bucket: {row['amount_bucket']}
- Signal Count: {row['signal_count']}
- Rule Based Risk Score: {row['risk_score_rule_based']}

Fraud Signals:
{row['signal_text']}

Feature Snapshot:
V1={row['V1']}, V2={row['V2']}, V3={row['V3']}, abs_v14={row['abs_v14']}, abs_v17={row['abs_v17']}
"""

        texts.append(text.strip())
        ids.append(f"tx_{i}")

        metadatas.append({
            "Amount": float(row["Amount"]),
            "Class": int(row["Class"]),
            "amount_bucket": str(row["amount_bucket"]),
            "signal_count": int(row["signal_count"]),
            "risk_score_rule_based": int(row["risk_score_rule_based"]),
            "is_micro_txn": int(row["is_micro_txn"]),
            "is_high_amount": int(row["is_high_amount"])
        })

    logger.info(f"Prepared {len(texts)} documents")

    # =========================
    # 6. EMBEDDINGS
    # =========================
    embeddings = generate_embeddings(texts)

    if not embeddings:
        logger.error("❌ Embeddings generation failed!")
        return

    logger.info(f"Generated {len(embeddings)} embeddings")

    # =========================
    # 7. STORE IN CHROMA
    # =========================
    add_documents(texts, embeddings, ids, metadatas)

    # =========================
    # 8. VERIFY STORAGE
    # =========================
    count = collection.count()

    logger.info(f"📦 Total documents in ChromaDB: {count}")

    if count == 0:
        logger.error("❌ Ingestion failed — DB is empty")
    else:
        logger.info("✅ Ingestion successful")