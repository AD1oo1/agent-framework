import os
from pathlib import Path

from elasticsearch import Elasticsearch

from agent_framework.chunk import DocumentChunk
from agent_framework.elasticsearch_vector_store import (
    ElasticsearchVectorStore,
)
from agent_framework.gemini_embedding import GeminiEmbeddingProvider
from google import genai


INDEX_NAME = "agent_documents"


def main() -> None:
    password = os.environ["ELASTIC_PASSWORD"]

    elastic_client = Elasticsearch(
        "https://localhost:9200",
        ca_certs=str(Path("http_ca.crt")),
        basic_auth=("elastic", password),
        request_timeout=60,
    )

    gemini_client = genai.Client()
    embedding_provider = GeminiEmbeddingProvider(
        client=gemini_client
    )

    vector_store = ElasticsearchVectorStore(
        client=elastic_client,
        index_name=INDEX_NAME,
    )

    chunks = [
        DocumentChunk(
            content=(
                "The company reported strong quarterly revenue "
                "growth driven by increased product sales."
            ),
            metadata={"source": "financial_report.txt"},
        ),
        DocumentChunk(
            content=(
                "The company expanded its manufacturing facilities "
                "to increase production capacity."
            ),
            metadata={"source": "operations_report.txt"},
        ),
        DocumentChunk(
            content=(
                "The company hired additional engineers to strengthen "
                "its research and development team."
            ),
            metadata={"source": "hr_report.txt"},
        ),
    ]

    embeddings = embedding_provider.embed_batch(
        [chunk.content for chunk in chunks]
    )

    for chunk, embedding in zip(chunks, embeddings):
        vector_store.add(chunk, embedding)

    print("Documents indexed successfully.")

    query = "How did the company's revenue perform?"

    query_vector = embedding_provider.embed(query)

    results = vector_store.search(
        query_vector=query_vector,
        top_k=2,
    )

    print("\nSearch results:")

    for result in results:
        print(f"- {result.content}")
        print(f"  Metadata: {result.metadata}")


if __name__ == "__main__":
    main()
