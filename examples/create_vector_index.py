import os
from pathlib import Path

from elasticsearch import Elasticsearch


INDEX_NAME = "agent_documents"


def main() -> None:
    password = os.environ["ELASTIC_PASSWORD"]

    client = Elasticsearch(
        "https://localhost:9200",
        ca_certs=str(Path("http_ca.crt")),
        basic_auth=("elastic", password),
        request_timeout=60,
    )

    if client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
        return

    client.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {
                "content": {
                    "type": "text",
                },
                "metadata": {
                    "type": "object",
                },
                "embedding": {
                    "type": "dense_vector",
                    "dims": 3072,
                    "similarity": "cosine",
                },
            }
        },
    )

    print(f"Created index: {INDEX_NAME}")


if __name__ == "__main__":
    main()
