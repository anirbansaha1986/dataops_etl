from etl.pipeline import run_pipeline
from rag.ingest_logs import ingest_logs
from rag.agent_chat import start_chat

import json

if __name__ == "__main__":

    print("\nRunning ETL Pipeline...\n")

    run_pipeline()

    print("\nIngesting logs into vector database...\n")

    ingest_logs()

    print("\nLogs ready for AI analysis.\n")

    start_chat()