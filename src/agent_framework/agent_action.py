from dataclasses import dataclass
from enum import Enum

from agent_framework.tool_call import ToolCall


class ActionType(str, Enum):
    FINAL_ANSWER = "final_answer"
    TOOL_CALL = "tool_call"


@dataclass
class AgentAction:

    action_type: ActionType

    tool_call: ToolCall | None = None
