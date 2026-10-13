from google import genai


class GeminiEmbeddingProvider:

    def __init__(
        self,
        client: genai.Client,
        model: str = "gemini-embedding-001",
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

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        return response.embeddings[0].values

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

        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
        )

        return [
            embedding.values
            for embedding in response.embeddings
        ]
