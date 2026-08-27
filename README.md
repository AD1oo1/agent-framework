# Agent Framework

A modular AI agent framework built from first principles to understand and implement the core architectural patterns behind modern agentic systems.

## Why This Project?

Modern agent frameworks make it easy to build agentic workflows, but they can also hide many of the architectural decisions happening underneath.

The goal of this project is not to replace existing frameworks.

It is to understand the engineering problems they solve by designing and implementing an agent framework from scratch.

The project focuses on understanding how state, prompts, LLMs, tools, actions, and workflows interact to form a reliable and extensible agent system.

## Project Goals

- Understand agent architecture from first principles
- Design clear boundaries between framework components
- Implement explicit state management
- Build a modular prompt construction and rendering system
- Abstract LLM providers behind a common interface
- Implement structured LLM response handling
- Build tool and action execution mechanisms
- Design a workflow orchestration layer
- Support retries, error handling, and observability
- Explore planning, memory, and multi-agent orchestration
- Validate the framework using a real-world financial analysis use case

## High-Level Architecture

```text
User Query
    │
    ▼
Agent
    │
    ▼
Workflow
    │
    ▼
AgentState
    │
    ├──► PromptBuilder
    │         │
    │         ▼
    │    PromptRenderer
    │         │
    │         ▼
    │      LLMClient
    │         │
    │         ▼
    │     LLMProvider
    │
    ├──► Parser
    │
    ├──► Action
    │
    └──► Tool
              │
              ▼
        State Update
              │
              └────────► Next Step



## Case Study: Financial Analysis Agent

The framework will be validated through a multi-agent financial analysis system.

### Workflow

1. A Financial Analysis Agent analyzes financial reports and extracts relevant insights.
2. A Cash Flow Analysis Agent gathers and analyzes relevant company and web data.
3. A Synthesis Agent combines the outputs from the previous agents and produces a final analysis.


User Query
    │
    ▼
Financial Analysis Agent ──────┐
                               │
                               ▼
Cash Flow Analysis Agent ──► Synthesis Agent
                               │
                               ▼
                         Final Analysis



---

## Step 5 — Current Status

## Project Status

🚧 Work in Progress

This project is being developed incrementally, with each major architectural decision documented before implementation.

## Roadmap

- [ ] Project foundation
- [ ] AgentState
- [ ] Message system
- [ ] Prompt system
- [ ] LLM abstraction
- [ ] Structured response handling
- [ ] Parser
- [ ] Action system
- [ ] Tool system
- [ ] Workflow engine
- [ ] Agent execution loop
- [ ] Planning
- [ ] Memory
- [ ] Multi-agent orchestration
- [ ] Financial analysis case study
- [ ] Testing and observability

