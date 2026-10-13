from agent_framework.document import Document
from agent_framework.embedding import EmbeddingProvider
from agent_framework.In_memory_vector_store import InMemoryVectorStore
from agent_framework.simple_chunker import SimpleChunker
from agent_framework.simple_embedding import SimpleEmbeddingProvider
from agent_framework.vector_retriever import VectorRetriever


def test_rag_pipeline_from_document_to_retrieval():

    document = Document(
        content=(
            "The company generated revenue of "
            "$394 billion in the fiscal year. "
            "Net profit was $100 billion. "
            "The company invested $50 billion "
            "in research and development."
        ),
        metadata={
            "source": "annual_report.txt",
        },
    )

    chunker = SimpleChunker(
        chunk_size=80,
        chunk_overlap=10,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) > 1

    embedding_provider = SimpleEmbeddingProvider(
        dimensions=8,
    )

    vector_store = InMemoryVectorStore()

    for chunk in chunks:

        vector = embedding_provider.embed(
            chunk.content
        )

        vector_store.add(
            chunk=chunk,
            vector=vector,
        )

    retriever = VectorRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        query="What was the company revenue?",
        top_k=2,
    )

    assert len(results) == 2

    assert all(
        result.metadata["source"]
        == "annual_report.txt"
        for result in results
    )
