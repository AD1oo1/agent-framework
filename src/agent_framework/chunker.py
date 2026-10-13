from typing import Protocol

from agent_framework.document import Document
from agent_framework.chunk import DocumentChunk


class Chunker(Protocol):

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:
        ...
