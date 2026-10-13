import pytest

from agent_framework.simple_embedding import (
    SimpleEmbeddingProvider,
)


def test_embedding_returns_expected_dimensions():

    provider = SimpleEmbeddingProvider(
        dimensions=8,
    )

    vector = provider.embed(
        "Revenue increased."
    )

    assert len(vector) == 8

    assert all(
        isinstance(value, float)
        for value in vector
    )


def test_embedding_is_deterministic():

    provider = SimpleEmbeddingProvider(
        dimensions=8,
    )

    first = provider.embed(
        "Revenue increased."
    )

    second = provider.embed(
        "Revenue increased."
    )

    assert first == second


def test_different_text_produces_different_vector():

    provider = SimpleEmbeddingProvider(
        dimensions=8,
    )

    first = provider.embed(
        "Revenue increased."
    )

    second = provider.embed(
        "Revenue decreased."
    )

    assert first != second


def test_batch_embedding():

    provider = SimpleEmbeddingProvider(
        dimensions=8,
    )

    vectors = provider.embed_batch(
        [
            "Revenue increased.",
            "Profit decreased.",
        ]
    )

    assert len(vectors) == 2

    assert all(
        len(vector) == 8
        for vector in vectors
    )


def test_invalid_dimensions_are_rejected():

    with pytest.raises(
        ValueError,
        match="dimensions must be greater than 0",
    ):
        SimpleEmbeddingProvider(
            dimensions=0,
        )
