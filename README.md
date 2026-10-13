# Agent Framework

A modular AI agent framework built from first principles to explore the architecture and engineering principles behind modern agentic systems.

This project focuses on explicit state management, modular LLM integrations, tool execution, workflow orchestration, and retrieval-augmented generation (RAG)—without relying on a high-level agent orchestration framework.

It is a hands-on learning project designed to understand how these components work together and how their boundaries affect maintainability, reliability, and extensibility.

## Why This Project?

Modern agent frameworks simplify the development of AI applications, but they can hide many underlying architectural decisions.

The goal of this project is to understand those decisions by implementing the core building blocks independently.

Rather than focusing only on prompts and model calls, the project explores how state, messages, providers, tools, retrieval, and workflow execution interact to form an agent system.

## Features

- **Agent state and messaging:** Explicit state management, structured messages, tool results, errors, and final answers.
- **LLM abstraction:** Provider interfaces and a shared client for working with Gemini and OpenAI integrations.
- **Prompt engineering infrastructure:** Separate prompt construction and rendering components.
- **Tool execution:** Structured tool calls, registered tools, and tool execution.
- **Workflow orchestration:** Nodes, graph-based execution, conditional routing, execution tracking, and retry handling.
- **Document ingestion:** Text, Markdown, and PDF loaders.
- **Document chunking:** Configurable chunk sizes and overlap.
- **Embeddings:** Simple local embeddings and provider integrations for Gemini and OpenAI.
- **Vector retrieval:** In-memory vector storage, Elasticsearch-backed vector storage, and similarity-based retrieval.
- **RAG pipeline:** Document indexing, retrieval of relevant chunks, and LLM-based response generation.
- **Automated tests:** Unit tests and separately marked integration tests.

## Architecture

```text
                         User Goal
                             |
                             v
                         AgentState
                             |
                             v
                          Workflow
                             |
                    +--------+--------+
                    |                 |
                    v                 v
               Retrieval Node      Tool Node
                    |                 |
                    v                 v
              Vector Retriever   Tool Executor
                    |
                    v
             Retrieved Context
                    |
                    v
                  LLM Node
                    |
                    v
              Prompt Builder
                    |
                    v
              Prompt Renderer
                    |
                    v
                 LLMClient
                    |
             +------+------+
             |             |
             v             v
       Gemini Provider  OpenAI Provider
             |             |
             +------+------+
                    |
                    v
              LLM Response
                    |
                    v
              State Update
```

The diagram illustrates the main components and their responsibilities. Actual execution depends on the workflow graph configured by the application.

## RAG Pipeline

The project includes a retrieval-augmented generation workflow using document ingestion, embeddings, vector storage, retrieval, and LLM generation.

```text
Source Documents
       |
       v
 Document Loader
       |
       v
  Text Chunker
       |
       v
 Embedding Provider
       |
       v
 Vector Store
       |
       v
  User Question
       |
       v
 Query Embedding
       |
       v
 Relevant Chunks
       |
       v
   LLM Generation
       |
       v
    Final Answer
```

### Supported components

- Markdown and text document loading, with PDF loading support.
- Chunking with configurable chunk size and overlap.
- Gemini and OpenAI embedding integrations.
- In-memory and Elasticsearch-backed vector stores.
- Retrieval of relevant document chunks.
- Workflow-based retrieval and LLM generation.

## Project Structure

```text
agent-framework/
├── data/
│   └── annual_report.md
├── examples/
│   ├── create_vector_index.py
│   ├── index_documents.py
│   ├── run_rag_agent.py
│   ├── check_elasticsearch_connection.py
│   ├── demo_elasticsearch_vector_search.py
│   └── demo_gemini_embeddings.py
├── src/
│   └── agent_framework/
│       ├── agent_loop.py
│       ├── agent_runner.py
│       ├── state.py
│       ├── message.py
│       ├── prompt_builder.py
│       ├── prompt_renderer.py
│       ├── llm_client.py
│       ├── gemini_provider.py
│       ├── openai_provider.py
│       ├── tool_executor.py
│       ├── workflow.py
│       ├── router.py
│       ├── indexing_pipeline.py
│       ├── vector_retriever.py
│       ├── retrieval_node.py
│       └── ...
├── tests/
│   ├── integration/
│   └── unit/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or newer
- Git
- API credentials for the external provider you want to use
- Elasticsearch configured locally if you want to run the Elasticsearch-backed examples

### Installation

Clone the repository and enter the project directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd agent-framework
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project and its dependencies:

```bash
python -m pip install -e .
```

Install the testing dependency if it is not included in your development environment:

```bash
python -m pip install pytest
```

> **Dependency note:** Ensure `pyproject.toml` declares the runtime dependencies required by the project before relying on `pip install -e .` in a fresh environment.

### Environment Variables

Configure only the credentials needed for the integration you intend to use.

Windows PowerShell examples:

```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key"
$env:OPENAI_API_KEY = "your-openai-api-key"
$env:ELASTIC_PASSWORD = "your-elasticsearch-password"
```

Never commit real API keys, passwords, private keys, or local certificates to version control.

## Running the Examples

### 1. Create the Elasticsearch vector index

```powershell
python .\examples\create_vector_index.py
```

### 2. Index the sample document

```powershell
python .\examples\index_documents.py
```

### 3. Run the RAG workflow

```powershell
python .\examples\run_rag_agent.py
```

The Elasticsearch examples expect a locally accessible Elasticsearch instance configured for HTTPS, its CA certificate, and the appropriate credentials. The Gemini examples require valid Gemini API credentials.

Run each example independently and ensure its required services are available first.

## Testing

Run the default test suite:

```powershell
pytest
```

Integration tests are excluded from the default run to avoid requiring external services or API credentials for every test execution.

Discover integration tests:

```powershell
pytest --collect-only -q -m integration -o addopts=""
```

Run integration tests:

```powershell
pytest -m integration -o addopts=""
```

Integration tests may incur API costs and require valid credentials, network access, and any necessary services.

## Design Principles

- **Explicit boundaries:** Separate state management, prompt construction, provider integration, tool execution, and workflow orchestration.
- **Small components:** Give each component a focused responsibility.
- **Provider abstraction:** Avoid coupling the core framework to a single LLM provider.
- **Testability:** Use unit tests to validate behavior without requiring external services wherever possible.
- **Incremental engineering:** Build and verify the underlying mechanisms before introducing higher-level abstractions.

## Current Status

The project has implemented core agent execution, workflow orchestration, LLM integrations, tool execution, document indexing, vector retrieval, and a basic RAG workflow.

Planning, persistent memory, and more advanced multi-agent orchestration remain areas for future exploration unless explicitly implemented in a later version.

## Learning Objective

The primary objective is to develop a practical understanding of how agentic systems are engineered—from individual components to a working workflow—and to build a foundation for more advanced AI systems.

