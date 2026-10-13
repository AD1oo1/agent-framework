from agent_framework.chunk import DocumentChunk
from agent_framework.retrieval_node import RetrievalNode
from agent_framework.state import AgentState


class FakeRetriever:

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        return [
            DocumentChunk(
                content="Revenue was $394 billion.",
                metadata={
                    "source": "annual_report.pdf",
                    "page": 10,
                },
            ),
            DocumentChunk(
                content="Profit was $100 billion.",
                metadata={
                    "source": "annual_report.pdf",
                    "page": 11,
                },
            ),
        ]


def test_retrieval_node_adds_chunks_to_state():

    node = RetrievalNode(
        retriever=FakeRetriever(),
        top_k=2,
    )

    state = AgentState(
        goal="What was the company's revenue?"
    )

    result = node.execute(state)

    assert len(
        result.retrieved_chunks
    ) == 2

    assert (
        result.retrieved_chunks[0].content
        == "Revenue was $394 billion."
    )

    assert (
        result.retrieved_chunks[0].metadata["page"]
        == 10
    )


import pytest

from agent_framework.retrieval_node import RetrievalNode


def test_retrieval_node_rejects_invalid_top_k():

    with pytest.raises(
        ValueError,
        match="top_k must be greater than 0",
    ):
        RetrievalNode(
            retriever=None,
            top_k=0,
        )
