from agent_framework.node import Node
from agent_framework.state import AgentState
from agent_framework.tool_call import ToolCall
from agent_framework.tool_executor import ToolExecutor


class ToolNode(Node):

    def __init__(
        self,
        executor: ToolExecutor,
        tool_call: ToolCall,
    ) -> None:

        self.executor = executor
        self.tool_call = tool_call

    def execute(
        self,
        state: AgentState,
    ) -> AgentState:

        result = self.executor.execute(
            tool_name=self.tool_call.tool_name,
            **self.tool_call.arguments,
        )

        state.add_tool_result(result)

        return state
