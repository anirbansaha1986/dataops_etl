import json
from rag.embedder import generate_embeddings
from rag.vector_store import add_documents


def ingest_logs():

    with open("etl_log.json") as f:
        data = json.load(f)

    texts = []
    ids = []

    for i, file in enumerate(data["details"]):

        status = file["status"]
        filename = file["file"]

        if file["errors"]:
            error = file["errors"][0]["message"]
        else:
            error = "No errors"

        text = f"File {filename} finished with status {status}. Error: {error}"

        texts.append(text)
        ids.append(f"log_{i}")

    embeddings = generate_embeddings(texts)

    add_documents(texts, embeddings, ids)

    print("Logs successfully ingested into ChromaDB")