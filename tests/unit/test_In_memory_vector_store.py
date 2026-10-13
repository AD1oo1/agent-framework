import pytest

from agent_framework.chunk import DocumentChunk
from agent_framework.In_memory_vector_store import (
    InMemoryVectorStore,
)


def test_vector_store_returns_most_similar_chunks():

    store = InMemoryVectorStore()

    first_chunk = DocumentChunk(
        content="Revenue increased significantly.",
    )

    second_chunk = DocumentChunk(
        content="The company opened a new office.",
    )

    store.add(
        first_chunk,
        [1.0, 0.0, 0.0],
    )

    store.add(
        second_chunk,
        [0.0, 1.0, 0.0],
    )

    results = store.search(
        query_vector=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert len(results) == 1

    assert results[0].content == (
        "Revenue increased significantly."
    )


def test_vector_store_respects_top_k():

    store = InMemoryVectorStore()

    chunks = [
        DocumentChunk(content="Chunk 1"),
        DocumentChunk(content="Chunk 2"),
        DocumentChunk(content="Chunk 3"),
    ]

    vectors = [
        [1.0, 0.0],
        [0.9, 0.1],
        [0.0, 1.0],
    ]

    for chunk, vector in zip(
        chunks,
        vectors,
    ):
        store.add(chunk, vector)

    results = store.search(
        query_vector=[1.0, 0.0],
        top_k=2,
    )

    assert len(results) == 2

    assert results[0].content == "Chunk 1"

    assert results[1].content == "Chunk 2"


def test_vector_store_rejects_empty_vector():

    store = InMemoryVectorStore()

    with pytest.raises(
        ValueError,
        match="Vector cannot be empty",
    ):
        store.add(
            DocumentChunk(
                content="Test"
            ),
            [],
        )


def test_vector_store_rejects_invalid_top_k():

    store = InMemoryVectorStore()

    with pytest.raises(
        ValueError,
        match="top_k must be greater than 0",
    ):
        store.search(
            query_vector=[1.0],
            top_k=0,
        )


def test_vector_store_rejects_dimension_mismatch():

    store = InMemoryVectorStore()

    store.add(
        DocumentChunk(
            content="Test"
        ),
        [1.0, 0.0],
    )

    with pytest.raises(
        ValueError,
        match="same dimensions",
    ):
        store.search(
            query_vector=[1.0],
            top_k=1,
        )
