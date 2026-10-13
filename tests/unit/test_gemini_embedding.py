import pytest

from agent_framework.gemini_embedding import (
    GeminiEmbeddingProvider,
)


class FakeEmbedding:

    def __init__(
        self,
        values: list[float],
    ) -> None:
        self.values = values


class FakeEmbeddingResponse:

    def __init__(
        self,
        embeddings: list[list[float]],
    ) -> None:

        self.embeddings = [
            FakeEmbedding(values)
            for values in embeddings
        ]


class FakeModels:

    def __init__(self) -> None:
        self.last_model = None
        self.last_contents = None

    def embed_content(
        self,
        model: str,
        contents,
    ) -> FakeEmbeddingResponse:

        self.last_model = model
        self.last_contents = contents

        if isinstance(contents, str):
            embeddings = [
                [0.1, 0.2, 0.3]
            ]
        else:
            embeddings = [
                [0.1, 0.2, 0.3]
                for _ in contents
            ]

        return FakeEmbeddingResponse(
            embeddings
        )


class FakeGeminiClient:

    def __init__(self) -> None:
        self.models = FakeModels()


def test_embed_returns_embedding():

    client = FakeGeminiClient()

    provider = GeminiEmbeddingProvider(
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
        client.models.last_model
        == "gemini-embedding-001"
    )

    assert (
        client.models.last_contents
        == "What was the revenue?"
    )


def test_embed_batch_returns_embeddings():

    client = FakeGeminiClient()

    provider = GeminiEmbeddingProvider(
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
        client.models.last_contents
        == [
            "Revenue was high.",
            "Profit increased.",
        ]
    )


def test_embed_rejects_empty_text():

    client = FakeGeminiClient()

    provider = GeminiEmbeddingProvider(
        client=client,
    )

    with pytest.raises(
        ValueError,
        match="Text cannot be empty",
    ):
        provider.embed("")


def test_embed_batch_returns_empty_for_empty_list():

    client = FakeGeminiClient()

    provider = GeminiEmbeddingProvider(
        client=client,
    )

    result = provider.embed_batch([])

    assert result == []


def test_embed_batch_rejects_empty_values():

    client = FakeGeminiClient()

    provider = GeminiEmbeddingProvider(
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
