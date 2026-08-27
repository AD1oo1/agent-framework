# Design Decisions

This document records the major architectural decisions made during the development of the Agent Framework.

Each decision captures the context, reasoning, alternatives considered, and consequences of the chosen approach.

---

## Decision 001 — AgentState Design

### Context

An AI agent needs a shared state that can evolve throughout its execution.

Different components such as the workflow, prompt system, LLM, parser, and tools need access to relevant information produced during previous execution steps.

Passing individual variables between components would make the system tightly coupled and difficult to maintain.

Therefore, the framework requires a dedicated `AgentState` object to act as the shared execution state.

### Problem

We need to determine:

- What information should belong to `AgentState`?
- Which fields should evolve during execution?
- Which fields should be appended versus overwritten?
- Which information should remain outside the state?

### Decision

Use a dedicated `AgentState` object as the primary source of information passed between execution steps.

The state will contain only information that is relevant to the evolving execution of an agent.

The initial state will contain:

- `goal`
- `messages`
- `tool_results`
- `current_plan`
- `final_answer`
- `retry_count`
- `errors`

The following information will not be part of `AgentState`:

- `available_tools`
- `metadata`

Static configuration and infrastructure-level information should remain outside the evolving execution state.

### State Update Strategy

Different fields require different update semantics.

| Field | Update Strategy | Reason |
|---|---|---|
| `goal` | Overwrite | The agent's goal may be refined during execution |
| `messages` | Append | Conversation history must be preserved |
| `tool_results` | Append | Previous tool outputs may be required for reasoning |
| `current_plan` | Overwrite | The active plan may change as execution progresses |
| `final_answer` | Set/Overwrite | Represents the latest final response |
| `retry_count` | Increment | Tracks the number of retry attempts |
| `errors` | Append | Error history should be preserved |

### Alternatives Considered

#### Option A — Generic Dictionary

Use a Python dictionary to store agent state.

**Rejected because:**

- Weak type safety
- Easy to introduce inconsistent keys
- Difficult to define explicit contracts
- Harder to maintain as the system grows

#### Option B — Passing Individual Variables

Pass only the required variables between components.

**Rejected because:**

- Creates tight coupling between components
- Function signatures become increasingly complex
- Difficult to evolve as new state becomes necessary

#### Option C — Dedicated AgentState Object

Use a dedicated domain object representing the complete execution state.

**Selected because:**

- Provides an explicit contract
- Improves type safety
- Makes state evolution predictable
- Simplifies component interfaces
- Makes debugging and testing easier
- Scales better as the framework grows

### Consequences

#### Positive

- Components communicate through a consistent state contract
- State evolution becomes explicit
- Easier testing and debugging
- Reduced coupling between workflow components
- New state fields can be introduced without changing every component interface

#### Trade-offs

- The state object can become large if responsibilities are not controlled
- Incorrect state design can lead to unnecessary coupling
- Update semantics must be clearly defined for each field

### Status

Accepted

---

## Decision 002 — Prompt Architecture

### Context

The agent needs to communicate with an LLM using prompts that contain multiple types of information, including system instructions, the current goal, contextual information, available tools, and the expected output format.

A prompt is not simply a string. Different parts of the prompt have different responsibilities and may originate from different sources.

Therefore, the framework needs a clear separation between prompt representation, prompt construction, and prompt rendering.

### Problem

We need to determine:

- How should a prompt be represented internally?
- Which component should construct the prompt?
- Which component should convert the prompt into an LLM-compatible format?
- Which prompt sections should depend on `AgentState`?
- How can we prevent prompt construction and provider/API-specific formatting from becoming tightly coupled?

### Decision

Use three separate responsibilities:

1. `Prompt`
2. `PromptBuilder`
3. `PromptRenderer`

The responsibilities are defined as follows:

#### Prompt

`Prompt` is a domain object that represents the structured prompt.

It contains:

- `system`
- `goal`
- `context`
- `tools`
- `output_format`

The `Prompt` object does not know how it will be rendered or which LLM provider will consume it.

#### PromptBuilder

`PromptBuilder` is responsible for constructing a `Prompt` from the current `AgentState` and static configuration.

The builder determines what information should be included in each prompt section.

The initial dependency strategy is:

| Prompt Section | Source |
|---|---|
| `system` | Static configuration |
| `goal` | `AgentState` |
| `context` | `AgentState` |
| `tools` | Static configuration |
| `output_format` | Static configuration |

The builder returns a structured `Prompt` object rather than a final string.

#### PromptRenderer

`PromptRenderer` is responsible for converting a `Prompt` object into the format required by the LLM interface.

The renderer owns formatting concerns such as:

- Section ordering
- Headers
- Whitespace
- Tool formatting
- Conversion to provider-independent rendered text

The renderer does not decide what information belongs in the prompt.

### Prompt Flow

The resulting flow is:

AgentState + Configuration
        ↓
PromptBuilder
        ↓
Prompt
        ↓
PromptRenderer
        ↓
Rendered Prompt
        ↓
LLMClient

### Alternatives Considered

#### Option A — Build the final string directly in PromptBuilder

The builder would construct the complete text prompt and return a string.

**Rejected because:**

- Prompt construction becomes coupled with formatting
- Difficult to support multiple rendering formats
- Harder to test prompt structure independently from formatting
- Provider/API-specific requirements can leak into prompt construction

#### Option B — Let PromptRenderer also build the prompt

The renderer would receive state and determine what information should be included.

**Rejected because:**

- Violates separation of responsibilities
- Renderer becomes aware of application state
- Makes prompt construction harder to test independently
- Creates unnecessary coupling between rendering and agent execution

#### Option C — Separate Prompt, PromptBuilder, and PromptRenderer

Use a structured `Prompt` object, a builder for constructing it, and a renderer for converting it into the required format.

**Selected because:**

- Clear separation of responsibilities
- Better testability
- Prompt structure remains provider-independent
- Rendering logic can evolve independently
- Supports multiple rendering strategies
- Keeps the LLMClient focused on LLM communication

### Design Principle

The framework follows the principle:

> Build the meaning first, render the representation later.

`PromptBuilder` decides **what the LLM should receive**.

`PromptRenderer` decides **how that information should be represented for the LLM interface**.

Neither component should take ownership of the other's responsibility.

### Consequences

#### Positive

- Prompt structure remains independent of provider-specific formatting
- Individual components are easier to test
- Multiple rendering strategies can be introduced later
- Agent state remains separate from presentation/formatting concerns
- LLM providers can evolve without changing prompt construction logic

#### Trade-offs

- Introduces additional abstractions compared with directly creating a string
- Requires maintaining a structured `Prompt` model
- Simple prompts may appear more verbose to construct

### Status

Accepted

---

## Decision 003 — LLM Abstraction

### Context

The framework needs to communicate with different Large Language Model providers.

Different providers expose different SDKs, APIs, request formats, response structures, error types, and configuration mechanisms.

If the rest of the framework directly depends on a specific provider SDK, adding or replacing a provider would require changes across multiple components.

The framework therefore needs a provider-independent abstraction.

### Problem

We need to determine:

- Where should provider-specific SDK logic live?
- What responsibilities should belong to `LLMClient`?
- How should different providers expose a common interface?
- How can the framework support multiple providers without tightly coupling the core architecture to any specific SDK?
- Should providers inherit from a common base class or implement a protocol?

### Decision

Introduce an `LLMClient` as the framework-level interface for interacting with language models and isolate provider-specific behavior behind an `LLMProvider` protocol.

The architecture will follow:

LLMClient
    ↓
LLMProvider Protocol
    ↓
Provider Implementation
    ↓
Provider SDK / API

The `LLMClient` will depend on the provider abstraction rather than directly depending on a specific SDK.

### LLMClient Responsibilities

`LLMClient` owns framework-level LLM communication policies.

Responsibilities include:

- Accepting a rendered prompt
- Delegating the actual model request to the provider
- Managing generic retry and backoff behavior
- Handling framework-level error handling
- Normalizing provider responses into framework-level representations
- Managing provider/model selection
- Collecting usage and execution metadata such as tokens, latency, and retry information

The `LLMClient` should not contain provider-specific SDK logic.

### LLMProvider Responsibilities

`LLMProvider` represents the contract that every LLM provider must satisfy.

The provider implementation is responsible for:

- Executing the actual SDK/API request
- Constructing provider-specific request payloads
- Handling provider-specific authentication/configuration
- Extracting information from provider-specific responses
- Isolating SDK-specific behavior and quirks

The provider should expose the raw provider interaction to the `LLMClient` without imposing provider-specific details on the rest of the framework.

### Provider Protocol

A `Protocol` will be used to define the provider contract.

Conceptually:

```text
LLMProvider
    │
    └── generate(...)