# C:\Users\Atharva P Deshpande\IT_Shaala\agent-framework\examples\test_gemini_embedding.py

from google import genai

from agent_framework.gemini_embedding import (
    GeminiEmbeddingProvider,
)


def main() -> None:

    client = genai.Client()

    provider = GeminiEmbeddingProvider(
        client=client,
    )

    embedding = provider.embed(
        "The company generated "
        "$394 billion in revenue."
    )

    print(
        f"Embedding dimensions: {len(embedding)}"
    )

    print(
        f"First 10 values: {embedding[:10]}"
    )


if __name__ == "__main__":
    main()
