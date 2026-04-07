from rag.retriever import retrieve_context
from rag.llm_client import ask_llm


def ask_pipeline(question):

    context = retrieve_context(question)

    context_text = "\n".join(context)

    prompt = f"""
You are a DataOps AI agent responsible for monitoring ETL pipelines.

Use the pipeline logs below to answer the question.

Pipeline Logs:
{context_text}

Instructions:
- Identify pipeline failures
- Explain the root cause
- Suggest remediation if possible

User Question:
{question}

Answer clearly and concisely.
"""

    response = ask_llm(prompt)

    return response