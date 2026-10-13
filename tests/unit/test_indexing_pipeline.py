import pytest

from agent_framework.document import Document
from agent_framework.chunk import DocumentChunk
from agent_framework.indexing_pipeline import IndexingPipeline


class FakeDocumentLoader:
    def __init__(self, documents):
        self.documents = documents

    def load(self, path):
        return self.documents

class FakeChunker:
    def __init__(self, chunks):
        self.chunks = chunks

    def chunk(self, document):
        if isinstance(self.chunks, dict):
            return self.chunks.get(document.content, [])

        return self.chunks

class FakeEmbeddingProvider:
    def __init__(self, vectors):
        self.vectors = vectors
        self.received_texts = []
        self.call_count = 0

    def embed(self, text):
        raise NotImplementedError

    def embed_batch(self, texts):
        self.received_texts.append(texts)

        start = sum(
            len(batch)
            for batch in self.received_texts[:-1]
        )
        end = start + len(texts)

        return self.vectors[start:end]



class FakeVectorStore:
    def __init__(self):
        self.items = []

    def add(self, chunk, vector):
        self.items.append((chunk, vector))

    def search(self, query_vector, top_k=5):
        return []


def make_pipeline(documents, chunks, vectors):
    loader = FakeDocumentLoader(documents)
    chunker = FakeChunker(chunks)
    embedding_provider = FakeEmbeddingProvider(vectors)
    vector_store = FakeVectorStore()

    pipeline = IndexingPipeline(
        document_loader=loader,
        chunker=chunker,
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    return pipeline, embedding_provider, vector_store


def test_indexing_pipeline_indexes_chunks():
    document = Document(
        content="Revenue was 100 million.",
        metadata={"source": "report.txt"},
    )

    chunks = [
        DocumentChunk(
            content="Revenue was 100 million.",
            metadata={"source": "report.txt"},
        ),
        DocumentChunk(
            content="Profit was 20 million.",
            metadata={"source": "report.txt"},
        ),
    ]


def test_indexing_pipeline_indexes_chunks():
    document = Document(
        content="Revenue was 100 million.",
        metadata={"source": "report.txt"},
    )

    chunks = [
        DocumentChunk(
            content="Revenue was 100 million.",
            metadata={"source": "report.txt"},
        ),
        DocumentChunk(
            content="Profit was 20 million.",
            metadata={"source": "report.txt"},
        ),
    ]

    vectors = [
        [0.1, 0.2],
        [0.3, 0.4],
    ]

    pipeline, embedding_provider, vector_store = make_pipeline(
        documents=[document],
        chunks=chunks,
        vectors=vectors,
    )

    count = pipeline.index("report.txt")

    assert count == 2
    assert embedding_provider.received_texts == [[
        "Revenue was 100 million.",
        "Profit was 20 million.",
    ]]

    expected_chunks = [
        DocumentChunk(
            content=chunk.content,
            metadata={
                **chunk.metadata,
                "chunk_index": index,
            },
        )
        for index, chunk in enumerate(chunks)
    ]

    assert vector_store.items == list(zip(expected_chunks, vectors))



def test_indexing_pipeline_returns_zero_when_no_chunks():
    document = Document(content="", metadata={})

    pipeline, _, vector_store = make_pipeline(
        documents=[document],
        chunks=[],
        vectors=[],
    )

    count = pipeline.index("empty.txt")

    assert count == 0
    assert vector_store.items == []


def test_indexing_pipeline_raises_when_embedding_count_mismatches():
    document = Document(
        content="Some document content.",
        metadata={},
    )

    chunks = [
        DocumentChunk(content="First chunk"),
        DocumentChunk(content="Second chunk"),
    ]

    pipeline, _, vector_store = make_pipeline(
        documents=[document],
        chunks=chunks,
        vectors=[[0.1, 0.2]],
    )

    with pytest.raises(
        ValueError,
        match="Embedding count must match chunk count.",
    ):
        pipeline.index("report.txt")

    assert vector_store.items == []

def test_indexing_pipeline_indexes_multiple_documents():
    documents = [
        Document(
            content="Document one",
            metadata={"source": "one.txt"},
        ),
        Document(
            content="Document two",
            metadata={"source": "two.txt"},
        ),
    ]

    chunks_by_content = {
        "Document one": [
            DocumentChunk(
                content="Chunk one",
                metadata={"source": "one.txt"},
            ),
        ],
        "Document two": [
            DocumentChunk(
                content="Chunk two",
                metadata={"source": "two.txt"},
            ),
            DocumentChunk(
                content="Chunk three",
                metadata={"source": "two.txt"},
            ),
        ],
    }

    vectors = [
        [0.1, 0.2],
        [0.3, 0.4],
        [0.5, 0.6],
    ]

    loader = FakeDocumentLoader(documents)
    chunker = FakeChunker(chunks_by_content)
    embedding_provider = FakeEmbeddingProvider(vectors)
    vector_store = FakeVectorStore()

    pipeline = IndexingPipeline(
        document_loader=loader,
        chunker=chunker,
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    count = pipeline.index("reports/")

    assert count == 3
    assert len(vector_store.items) == 3
