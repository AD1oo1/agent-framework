from agent_framework.chunk import DocumentChunk
from agent_framework.embedding import EmbeddingProvider
from agent_framework.vector_store import VectorStore


class VectorRetriever:

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:

        self.embedding_provider = (
            embedding_provider
        )

        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        query_vector = (
            self.embedding_provider.embed(
                query
            )
        )

        return self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )
