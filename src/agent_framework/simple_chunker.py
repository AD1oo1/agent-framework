from agent_framework.chunk import DocumentChunk
from agent_framework.document import Document


class SimpleChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than "
                "chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        content = document.content

        if not content:
            return []

        chunks = []

        start = 0

        while start < len(content):

            end = start + self.chunk_size

            chunk_content = content[start:end]

            chunks.append(
                DocumentChunk(
                    content=chunk_content,
                    metadata=document.metadata.copy(),
                )
            )

            if end >= len(content):
                break

            start = (
                end - self.chunk_overlap
            )

        return chunks
