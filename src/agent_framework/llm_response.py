from dataclasses import dataclass, field

from agent_framework.tool_call import ToolCall


@dataclass
class LLMResponse:

    content: str

    model: str | None = None

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    metadata: dict = field(
        default_factory=dict
    )

    tool_calls: list[ToolCall] = field(
        default_factory=list
    )
