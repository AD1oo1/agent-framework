from typing import Protocol

from agent_framework.chunk import DocumentChunk


class Retriever(Protocol):

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        ...
