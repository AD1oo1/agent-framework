from openai import OpenAI


class OpenAIEmbeddingProvider:

    def __init__(
        self,
        client: OpenAI,
        model: str = "text-embedding-3-small",
    ) -> None:

        self.client = client
        self.model = model

    def embed(
        self,
        text: str,
    ) -> list[float]:

        if not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        if any(
            not text.strip()
            for text in texts
        ):
            raise ValueError(
                "Texts cannot contain empty values."
            )

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [
            item.embedding
            for item in response.data
        ]
