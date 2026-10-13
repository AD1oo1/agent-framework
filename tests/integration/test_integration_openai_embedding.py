import os

import pytest
from openai import OpenAI

from agent_framework.openai_embedding import (
    OpenAIEmbeddingProvider,
)


@pytest.mark.integration
def test_real_openai_embedding():

    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip(
            "OPENAI_API_KEY is not configured."
        )

    client = OpenAI()

    provider = OpenAIEmbeddingProvider(
        client=client,
    )

    embedding = provider.embed(
        "The company generated "
        "$394 billion in revenue."
    )

    assert isinstance(
        embedding,
        list,
    )

    assert len(embedding) > 0

    assert all(
        isinstance(value, float)
        for value in embedding
    )
