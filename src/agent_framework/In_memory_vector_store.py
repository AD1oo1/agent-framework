import math

from agent_framework.chunk import DocumentChunk


class InMemoryVectorStore:

    def __init__(self) -> None:

        self._items: list[
            tuple[DocumentChunk, list[float]]
        ] = []

    def add(
        self,
        chunk: DocumentChunk,
        vector: list[float],
    ) -> None:

        if not vector:
            raise ValueError(
                "Vector cannot be empty."
            )

        self._items.append(
            (chunk, vector)
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        if not query_vector:
            raise ValueError(
                "Query vector cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        scored_items = [
            (
                self._cosine_similarity(
                    query_vector,
                    vector,
                ),
                chunk,
            )
            for chunk, vector in self._items
        ]

        scored_items.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            chunk
            for _, chunk in scored_items[:top_k]
        ]

    def _cosine_similarity(
        self,
        first: list[float],
        second: list[float],
    ) -> float:

        if len(first) != len(second):
            raise ValueError(
                "Vectors must have the same dimensions."
            )

        dot_product = sum(
            first_value * second_value
            for first_value, second_value
            in zip(first, second)
        )

        first_magnitude = math.sqrt(
            sum(
                value * value
                for value in first
            )
        )

        second_magnitude = math.sqrt(
            sum(
                value * value
                for value in second
            )
        )

        if (
            first_magnitude == 0
            or second_magnitude == 0
        ):
            raise ValueError(
                "Vectors must not be zero vectors."
            )

        return (
            dot_product
            / (
                first_magnitude
                * second_magnitude
            )
        )
