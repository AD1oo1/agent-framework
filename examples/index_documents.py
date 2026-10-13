import os
from pathlib import Path

from elasticsearch import Elasticsearch
from google import genai

from agent_framework.elasticsearch_vector_store import (
    ElasticsearchVectorStore,
)
from agent_framework.gemini_embedding import (
    GeminiEmbeddingProvider,
)
from agent_framework.indexing_pipeline import IndexingPipeline
from agent_framework.markdown_loader import MarkdownLoader
from agent_framework.simple_chunker import SimpleChunker


INDEX_NAME = "agent_documents"


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    document_path = project_root / "data" / "annual_report.md"
    certificate_path = project_root / "http_ca.crt"

    gemini_client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    embedding_provider = GeminiEmbeddingProvider(
        client=gemini_client
    )

    elastic_client = Elasticsearch(
        "https://localhost:9200",
        ca_certs=str(certificate_path),
        basic_auth=(
            "elastic",
            os.environ["ELASTIC_PASSWORD"],
        ),
        request_timeout=60,
    )

    vector_store = ElasticsearchVectorStore(
        client=elastic_client,
        index_name=INDEX_NAME,
    )

    pipeline = IndexingPipeline(
        document_loader=MarkdownLoader(),
        chunker=SimpleChunker(
            chunk_size=500,
            chunk_overlap=50,
        ),
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    try:
        indexed_count = pipeline.index(document_path)
        print(f"Successfully indexed {indexed_count} chunks.")
    finally:
        elastic_client.close()


if __name__ == "__main__":
    main()
