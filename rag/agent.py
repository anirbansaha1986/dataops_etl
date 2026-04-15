import pandas as pd
from rag.retriever import retrieve_context
from rag.llm_client import ask_llm
from utils.logger import get_logger

logger = get_logger("AGENT")

# =========================
# LOAD DATA ONCE
# =========================
df = pd.read_csv("data/creditcard.csv")


# =========================
# ANALYTICS HANDLER
# =========================
def handle_analytics(question):

    q = question.lower()

    if "total transactions" in q or "how many transactions" in q:
        return f"Total transactions: {len(df)}"

    if "fraud" in q and "how many" in q:
        fraud_count = len(df[df["Class"] == 1])
        return f"Fraud transactions: {fraud_count}"

    if "normal" in q and "how many" in q:
        normal_count = len(df[df["Class"] == 0])
        return f"Normal transactions: {normal_count}"

    if "dataset size" in q or "size of dataset" in q:
        return f"Dataset size: {len(df)} records"

    if "percentage" in q and "fraud" in q:
        fraud = len(df[df["Class"] == 1])
        total = len(df)
        return f"Fraud percentage: {(fraud/total)*100:.4f}%"

    return None


# =========================
# MAIN AGENT FUNCTION
# =========================
def ask_agent(question):

    logger.info(f"User question: {question}")

    # -------------------------
    # 1. ANALYTICS FIRST
    # -------------------------
    analytics_answer = handle_analytics(question)

    if analytics_answer:
        logger.info("ROUTE → ANALYTICS")
        return analytics_answer

    # -------------------------
    # 2. RAG RETRIEVAL
    # -------------------------
    context = retrieve_context(question)

    if context:
        logger.info(f"ROUTE → RAG + LLM | Context size: {len(context)}")

        context_text = "\n".join(context)

        prompt = f"""
You are a fraud detection assistant.

Use ONLY the transaction data below to answer.

Transaction Data:
{context_text}

Question:
{question}

Answer clearly using the data.
"""

        return ask_llm(prompt)

    # -------------------------
    # 3. BLOCK LLM (NO CONTEXT)
    # -------------------------
    logger.warning("ROUTE → BLOCKED (NO CONTEXT)")

    return (
        "I don’t have enough data context to answer this.\n"
        "Try asking about transactions, fraud examples, or patterns."
    )