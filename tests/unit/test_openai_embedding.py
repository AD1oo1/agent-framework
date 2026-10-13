import pytest

from agent_framework.openai_embedding import (
    OpenAIEmbeddingProvider,
)


class FakeEmbeddingItem:

    def __init__(
        self,
        embedding: list[float],
    ) -> None:
        self.embedding = embedding


class FakeEmbeddingResponse:

    def __init__(
        self,
        embeddings: list[list[float]],
    ) -> None:

        self.data = [
            FakeEmbeddingItem(
                embedding
            )
            for embedding in embeddings
        ]


class FakeEmbeddings:

    def __init__(self) -> None:
        self.last_model = None
        self.last_input = None

    def create(
        self,
        model: str,
        input,
    ) -> FakeEmbeddingResponse:

        self.last_model = model
        self.last_input = input

        if isinstance(input, str):
            embeddings = [
                [0.1, 0.2, 0.3]
            ]
        else:
            embeddings = [
                [0.1, 0.2, 0.3]
                for _ in input
            ]

        return FakeEmbeddingResponse(
            embeddings
        )


class FakeOpenAIClient:

    def __init__(self) -> None:
        self.embeddings = FakeEmbeddings()


def test_embed_returns_embedding():

    client = FakeOpenAIClient()

    provider = OpenAIEmbeddingProvider(
        client=client,
    )

    result = provider.embed(
        "What was the revenue?"
    )

    assert result == [
        0.1,
        0.2,
        0.3,
    ]

    assert (
        client.embeddings.last_model
        == "text-embedding-3-small"
    )

    assert (
        client.embeddings.last_input
        == "What was the revenue?"
    )


def test_embed_batch_returns_embeddings():

    client = FakeOpenAIClient()

    provider = OpenAIEmbeddingProvider(
        client=client,
    )

    result = provider.embed_batch(
        [
            "Revenue was high.",
            "Profit increased.",
        ]
    )

    assert result == [
        [0.1, 0.2, 0.3],
        [0.1, 0.2, 0.3],
    ]

    assert (
        client.embeddings.last_input
        == [
            "Revenue was high.",
            "Profit increased.",
        ]
    )


def test_embed_rejects_empty_text():

    client = FakeOpenAIClient()

    provider = OpenAIEmbeddingProvider(
        client=client,
    )

    with pytest.raises(
        ValueError,
        match="Text cannot be empty",
    ):
        provider.embed("")


def test_embed_batch_returns_empty_for_empty_list():

    client = FakeOpenAIClient()

    provider = OpenAIEmbeddingProvider(
        client=client,
    )

    result = provider.embed_batch([])

    assert result == []


def test_embed_batch_rejects_empty_values():

    client = FakeOpenAIClient()

    provider = OpenAIEmbeddingProvider(
        client=client,
    )

    with pytest.raises(
        ValueError,
        match="Texts cannot contain empty values",
    ):
        provider.embed_batch(
            [
                "Revenue was high.",
                "",
            ]
        )
