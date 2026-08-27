# Architecture

## Overview

This document describes the architecture, component boundaries, data flow, and execution model of the Agent Framework.

The framework is designed as a modular system where each component has a clearly defined responsibility and communicates through explicit contracts.

The architecture is intentionally designed to minimize coupling between components while allowing individual components to evolve independently.

## Core Design Principles

### 1. Separation of Responsibilities

Each component should own a clearly defined responsibility and should avoid taking ownership of concerns belonging to another layer.

### 2. Explicit Contracts

Components should communicate through well-defined interfaces and domain objects rather than relying on implicit behavior or loosely structured data.

### 3. Low Coupling

Components should depend on abstractions where appropriate rather than concrete implementations.

### 4. Provider Independence

The core framework should remain independent of any specific LLM provider or SDK.

Provider-specific behavior should be isolated behind provider abstractions.

### 5. Explicit State Management

Agent execution should operate on an explicit state object that evolves throughout the workflow.

### 6. Extensibility

The architecture should allow new providers, tools, workflows, and agent types to be introduced without requiring major changes to existing components.

### 7. Testability

Components should be designed so that they can be tested independently as well as through integration tests.

## High-Level Architecture

```text
                         User
                          │
                          ▼
                    Agent / Entry Point
                          │
                          ▼
                    Workflow Engine
                          │
                          ▼
                      AgentState
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
        Prompt System   Tools      Messages
              │
              ▼
        PromptBuilder
              │
              ▼
        PromptRenderer
              │
              ▼
          LLMClient
              │
              ▼
        LLMProvider
              │
              ▼
             LLM
              │
              ▼
        LLMResponse
              │
              ▼
            Parser
              │
              ▼
            Action
              │
              ▼
        Tool Executor
              │
              ▼
         State Update
              │
              └──────────────► Next Workflow Step



---

# 3. Component Overview

| Component | Responsibility |
|---|---|
| AgentState | Maintains the evolving state of agent execution |
| Message System | Represents user, assistant, and tool interactions |
| Prompt | Represents the structured prompt domain object |
| PromptBuilder | Builds a Prompt from application state and configuration |
| PromptRenderer | Converts a Prompt into the format required by an LLM interface |
| LLMClient | Provides provider-independent LLM interaction and communication policies |
| LLMProvider | Encapsulates provider-specific SDK/API behavior |
| LLMResponse | Represents normalized model output |
| Parser | Converts structured LLM output into framework-level objects |
| Action | Represents the next operation selected by the agent |
| Tool | Performs external operations or retrieves external information |
| Workflow Engine | Controls the execution flow and state transitions |
| Agent | Coordinates reasoning and execution within the framework |


## Execution Model

The agent operates through an iterative execution loop.

At a high level:

```text
1. Receive user request
2. Initialize AgentState
3. Build prompt from current state
4. Render prompt for the LLM interface
5. Send request through LLMClient
6. Receive normalized LLMResponse
7. Parse the response
8. Determine the required Action
9. Execute the Action or Tool
10. Update AgentState
11. Evaluate whether execution is complete
12. Continue or produce the final answer