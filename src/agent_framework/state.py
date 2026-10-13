from dataclasses import dataclass, field

from agent_framework.chunk import DocumentChunk
from agent_framework.message import Message
from agent_framework.tool import ToolResult


@dataclass
class AgentState:
    goal: str
    messages: list[Message] = field(
        default_factory=list
    )

    tool_results: list[ToolResult] = field(
        default_factory=list
    )

    retrieved_chunks: list[DocumentChunk] = field(
        default_factory=list
    )

    current_plan: list[str] = field(
        default_factory=list
    )

    final_answer: str | None = None

    retry_count: int = 0

    errors: list[str] = field(
        default_factory=list
    )

    def add_message(
        self,
        message: Message,
    ) -> None:
        self.messages.append(message)

    def add_tool_result(
        self,
        tool_result: ToolResult,
    ) -> None:
        self.tool_results.append(tool_result)

    def add_retrieved_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:
        self.retrieved_chunks.append(chunk)

    def add_error(
        self,
        error: str,
    ) -> None:
        self.errors.append(error)

    def increment_retry(self) -> None:
        self.retry_count += 1

    def set_final_answer(
        self,
        answer: str,
    ) -> None:
        self.final_answer = answer
