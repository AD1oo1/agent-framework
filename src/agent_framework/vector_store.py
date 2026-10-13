from typing import Protocol

from agent_framework.chunk import DocumentChunk


class VectorStore(Protocol):

    def add(
        self,
        chunk: DocumentChunk,
        vector: list[float],
    ) -> None:
        ...

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        ...
