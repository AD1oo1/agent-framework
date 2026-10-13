import hashlib


class SimpleEmbeddingProvider:

    def __init__(
        self,
        dimensions: int = 8,
    ) -> None:

        if dimensions <= 0:
            raise ValueError(
                "dimensions must be greater than 0."
            )

        self.dimensions = dimensions

    def embed(
        self,
        text: str,
    ) -> list[float]:

        digest = hashlib.sha256(
            text.encode("utf-8")
        ).digest()

        vector = []

        for index in range(self.dimensions):

            value = digest[index] / 255

            vector.append(value)

        return vector

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return [
            self.embed(text)
            for text in texts
        ]
