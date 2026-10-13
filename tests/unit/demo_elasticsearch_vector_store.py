from unittest.mock import Mock

from agent_framework.chunk import DocumentChunk
from agent_framework.elasticsearch_vector_store import (
    ElasticsearchVectorStore,
)


def test_add_indexes_chunk_with_content_metadata_and_embedding():
    client = Mock()
    store = ElasticsearchVectorStore(
        client=client,
        index_name="test_documents",
    )

    chunk = DocumentChunk(
        content="Revenue increased.",
        metadata={"source": "report.md"},
    )
    vector = [0.1, 0.2, 0.3]

    store.add(chunk, vector)

    client.index.assert_called_once_with(
        index="test_documents",
        id=store.client.index.call_args.kwargs["id"],
        document={
            "content": "Revenue increased.",
            "metadata": {"source": "report.md"},
            "embedding": [0.1, 0.2, 0.3],
        },
    )
    assert len(store.client.index.call_args.kwargs["id"]) == 64

def test_search_returns_document_chunks():
    client = Mock()
    client.search.return_value = {
        "hits": {
            "hits": [
                {
                    "_source": {
                        "content": "Revenue increased.",
                        "metadata": {"source": "report.md"},
                        "embedding": [0.1, 0.2, 0.3],
                    }
                }
            ]
        }
    }

    store = ElasticsearchVectorStore(
        client=client,
        index_name="test_documents",
    )

    results = store.search(
        query_vector=[0.1, 0.2, 0.3],
        top_k=2,
    )

    assert len(results) == 1
    assert results[0].content == "Revenue increased."
    assert results[0].metadata == {"source": "report.md"}

    client.search.assert_called_once_with(
        index="test_documents",
        knn={
            "field": "embedding",
            "query_vector": [0.1, 0.2, 0.3],
            "k": 2,
            "num_candidates": 100,
        },
    )


def test_search_rejects_non_positive_top_k():
    client = Mock()
    store = ElasticsearchVectorStore(client=client)

    try:
        store.search(query_vector=[0.1], top_k=0)
    except ValueError as exc:
        assert str(exc) == "top_k must be greater than 0."
    else:
        raise AssertionError("Expected ValueError.")

    client.search.assert_not_called()
