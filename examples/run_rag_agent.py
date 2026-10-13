import os
from pathlib import Path

from elasticsearch import Elasticsearch
from google import genai

from agent_framework.elasticsearch_vector_store import (
    ElasticsearchVectorStore,
)
from agent_framework.gemini_embedding import (
    GeminiEmbeddingProvider,
)
from agent_framework.gemini_provider import GeminiProvider
from agent_framework.llm_client import LLMClient
from agent_framework.llm_node import LLMNode
from agent_framework.prompt_builder import PromptBuilder
from agent_framework.prompt_renderer import PromptRenderer
from agent_framework.retrieval_node import RetrievalNode
from agent_framework.state import AgentState
from agent_framework.vector_retriever import VectorRetriever
from agent_framework.workflow import Workflow


INDEX_NAME = "agent_documents"


def main() -> None:

    # ---------------------------------------------------------
    # Gemini clients
    # ---------------------------------------------------------

    gemini_client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    embedding_provider = GeminiEmbeddingProvider(
        client=gemini_client
    )

    llm_provider = GeminiProvider(
        client=gemini_client
    )

    llm_client = LLMClient(
        provider=llm_provider
    )

    # ---------------------------------------------------------
    # Elasticsearch
    # ---------------------------------------------------------

    elastic_client = Elasticsearch(
        "https://localhost:9200",
        ca_certs=str(Path("http_ca.crt")),
        basic_auth=(
            "elastic",
            os.environ["ELASTIC_PASSWORD"],
        ),
        request_timeout=60,
    )

    vector_store = ElasticsearchVectorStore(
        client=elastic_client,
        index_name=INDEX_NAME,
    )

    # ---------------------------------------------------------
    # Retriever
    # ---------------------------------------------------------

    retriever = VectorRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    # ---------------------------------------------------------
    # Nodes
    # ---------------------------------------------------------

    retrieval_node = RetrievalNode(
        retriever=retriever,
        top_k=2,
    )

    llm_node = LLMNode(
        prompt_builder=PromptBuilder(),
        prompt_renderer=PromptRenderer(),
        llm_client=llm_client,
    )

    # ---------------------------------------------------------
    # Workflow
    # ---------------------------------------------------------

    workflow = Workflow()

    workflow.add_node(
        "retrieve",
        retrieval_node,
    )

    workflow.add_node(
        "generate",
        llm_node,
    )

    workflow.add_edge(
        "retrieve",
        "generate",
    )

    workflow.set_entry_point(
        "retrieve"
    )

    # ---------------------------------------------------------
    # Run
    # ---------------------------------------------------------

    state = AgentState(
        goal="How did the company's revenue perform?"
    )

    final_state = workflow.run(state)

    print("\nRetrieved context:")

    for chunk in final_state.retrieved_chunks:
        print(
            f"- {chunk.content}"
        )

    print("\nFinal answer:")
    print(final_state.final_answer)


if __name__ == "__main__":
    main()
