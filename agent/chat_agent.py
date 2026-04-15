import logging

from rag.retriever import retrieve_context
from rag.llm_client import ask_llm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("AGENT")


def ask_agent(question):

    logger.info(f"User question: {question}")

    # Step 1 — Retrieve context from vector DB
    context = retrieve_context(question)

    if not context:
        logger.warning("No relevant records found in vector DB")
        return "No relevant transaction records found."

    logger.info(f"{len(context)} relevant records retrieved")

    context_text = "\n".join(context[:5])

    # Step 2 — Only now call LLM
    logger.info("Sending context to LLM")

    prompt = f"""
You are a DataOps Fraud Monitoring AI.

Use the transaction records below to answer the question.

Transactions:
{context_text}

Question:
{question}

Give a short analytical answer.
"""

    response = ask_llm(prompt)

    return response


def run_chat():

    print("\n===== DATAOPS FRAUD AI AGENT =====\n")

    while True:

        question = input("Ask question (or type exit): ")

        if question.lower() in ["exit", "quit"]:
            print("Exiting agent...")
            break

        answer = ask_agent(question)

        print("\nAI Response:\n")
        print(answer)
        print("\n")