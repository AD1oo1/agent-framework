import pytest

from agent_framework.document import Document
from agent_framework.simple_chunker import SimpleChunker


def test_chunker_splits_document():

    document = Document(
        content="abcdefghij",
        metadata={
            "source": "test.txt",
        },
    )

    chunker = SimpleChunker(
        chunk_size=4,
        chunk_overlap=1,
    )

    chunks = chunker.chunk(document)

    assert [
        chunk.content
        for chunk in chunks
    ] == [
        "abcd",
        "defg",
        "ghij",
    ]


def test_chunker_preserves_metadata():

    document = Document(
        content="abcdefgh",
        metadata={
            "source": "report.pdf",
            "page": 5,
        },
    )

    chunker = SimpleChunker(
        chunk_size=4,
        chunk_overlap=1,
    )

    chunks = chunker.chunk(document)

    assert chunks[0].metadata == {
        "source": "report.pdf",
        "page": 5,
    }


def test_chunker_returns_empty_for_empty_document():

    document = Document(
        content="",
    )

    chunker = SimpleChunker()

    assert chunker.chunk(document) == []


def test_chunker_rejects_invalid_overlap():

    with pytest.raises(
        ValueError,
        match="chunk_overlap must be smaller",
    ):
        SimpleChunker(
            chunk_size=100,
            chunk_overlap=100,
        )
