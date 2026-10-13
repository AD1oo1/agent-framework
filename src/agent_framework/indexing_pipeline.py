
from pathlib import Path

from agent_framework.chunker import Chunker
from agent_framework.document_loader import DocumentLoader
from agent_framework.embedding import EmbeddingProvider
from agent_framework.vector_store import VectorStore


class IndexingPipeline:
    def __init__(
        self,
        document_loader: DocumentLoader,
        chunker: Chunker,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self.document_loader = document_loader
        self.chunker = chunker
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def index(self, path: str | Path) -> int:
        documents = self.document_loader.load(path)

        indexed_count = 0

        for document in documents:
            chunks = self.chunker.chunk(document)

            if not chunks:
                continue

            vectors = self.embedding_provider.embed_batch(
                [chunk.content for chunk in chunks]
            )

            if len(vectors) != len(chunks):
                raise ValueError(
                    "Embedding count must match chunk count."
                )

            for chunk_index, (chunk, vector) in enumerate(
                zip(chunks, vectors)
            ):
                indexed_chunk = type(chunk)(
                    content=chunk.content,
                    metadata={
                        **chunk.metadata,
                        "chunk_index": chunk_index,
                    },
                )

                self.vector_store.add(
                    chunk=indexed_chunk,
                    vector=vector,
                )

                indexed_count += 1

        return indexed_count
