from rag.retriever import retrieve_context
from rag.llm_client import ask_llm


def ask_agent(question):

    context = retrieve_context(question)

    context_text = "\n".join(context)

    # Simple answers without LLM
    if "fraud" in question.lower():

        fraud_count = sum(
            1 for c in context if "fraudulent" in c
        )

        return f"Detected {fraud_count} fraud transactions in retrieved records."

    # If reasoning required → call LLM

    prompt = f"""
You are a fraud detection analyst.

Historical transaction data:
{context_text}

Question:
{question}

Provide a concise answer.
"""

    return ask_llm(prompt)