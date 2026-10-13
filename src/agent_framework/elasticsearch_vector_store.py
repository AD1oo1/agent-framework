import hashlib

from elasticsearch import Elasticsearch


from agent_framework import chunk
from agent_framework.chunk import DocumentChunk


class ElasticsearchVectorStore:
    def __init__(
        self,
        client: Elasticsearch,
        index_name: str = "agent_documents",
    ) -> None:
        self.client = client
        self.index_name = index_name

    def add(
        self,
        chunk: DocumentChunk,
        vector: list[float],
    ) -> None:
        self.client.index(
            index=self.index_name,
            document={
                "content": chunk.content,
                "metadata": chunk.metadata,
                "embedding": vector,
            },
        )


    def add(self, chunk: DocumentChunk, vector: list[float]) -> None:
        source = chunk.metadata.get("source", "")
        chunk_index = chunk.metadata.get("chunk_index")

        identity = f"{source}:{chunk_index}:{chunk.content}"

        document_id =   hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()

        self.client.index(
            index=self.index_name,
            id=document_id,
            document={
                "content": chunk.content,
                "metadata": chunk.metadata,
                "embedding": vector,
            },
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        response = self.client.search(
            index=self.index_name,
            knn={
                "field": "embedding",
                "query_vector": query_vector,
                "k": top_k,
                "num_candidates": max(top_k * 10, 100),
            },
        )

        results = []

        for hit in response["hits"]["hits"]:
            source = hit["_source"]

            results.append(
                DocumentChunk(
                    content=source["content"],
                    metadata=source.get("metadata", {}),
                )
            )

        return results
