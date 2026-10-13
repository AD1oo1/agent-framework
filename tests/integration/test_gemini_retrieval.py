import pytest

from agent_framework.chunk import DocumentChunk
from agent_framework.gemini_embedding import GeminiEmbeddingProvider
from agent_framework.In_memory_vector_store import InMemoryVectorStore
from agent_framework.vector_retriever import VectorRetriever

from google import genai

@pytest.mark.integration
def test_gemini_semantic_retrieval() -> None:
    client = genai.Client()
    provider = GeminiEmbeddingProvider(client=client)

    vector_store = InMemoryVectorStore()

    chunks = [
        DocumentChunk(
            content=(
                "The company reported strong quarterly revenue growth "
                "driven by increased product sales."
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

    embeddings = provider.embed_batch(
        [chunk.content for chunk in chunks]
    )

    for chunk, embedding in zip(chunks, embeddings):
        vector_store.add(chunk, embedding)

    retriever = VectorRetriever(
        embedding_provider=provider,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        query="How did the company's revenue perform?",
        top_k=1,
    )

    assert len(results) == 1
    assert "revenue" in results[0].content.lower()
