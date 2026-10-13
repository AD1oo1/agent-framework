import pytest

from agent_framework.chunk import DocumentChunk
from agent_framework.simple_embedding import (
    SimpleEmbeddingProvider,
)
from agent_framework.vector_retriever import (
    VectorRetriever,
)
from agent_framework.In_memory_vector_store import (
    InMemoryVectorStore,
)


def test_retriever_returns_relevant_chunks():

    embedding_provider = (
        SimpleEmbeddingProvider(
            dimensions=8,
        )
    )

    vector_store = InMemoryVectorStore()

    relevant_chunk = DocumentChunk(
        content="Apple revenue was $394 billion."
    )

    unrelated_chunk = DocumentChunk(
        content="The company opened a new office."
    )

    vector_store.add(
        relevant_chunk,
        embedding_provider.embed(
            "Apple revenue was $394 billion."
        ),
    )

    vector_store.add(
        unrelated_chunk,
        embedding_provider.embed(
            "The company opened a new office."
        ),
    )

    retriever = VectorRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        query="Apple revenue",
        top_k=1,
    )

    assert len(results) == 1


def test_retriever_rejects_empty_query():

    retriever = VectorRetriever(
        embedding_provider=(
            SimpleEmbeddingProvider()
        ),
        vector_store=(
            InMemoryVectorStore()
        ),
    )

    with pytest.raises(
        ValueError,
        match="Query cannot be empty",
    ):
        retriever.retrieve(
            query="   "
        )
