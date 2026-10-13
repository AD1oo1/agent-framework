from dataclasses import dataclass, field

from agent_framework.message import Message


@dataclass
class Prompt:
    system: str
    goal: str
    context: str
    messages: list[Message] = field(default_factory=list)
    available_tools: list[str] = field(default_factory=list)
    output_format: str = ""
