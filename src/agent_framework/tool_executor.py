from agent_framework.tool import Tool, ToolResult


class ToolExecutor:

    def __init__(
        self,
        tools: list[Tool],
    ) -> None:

        self.tools = {
            tool.name: tool
            for tool in tools
        }

    def execute(
        self,
        tool_name: str,
        **kwargs,
    ) -> ToolResult:

        tool = self.tools.get(tool_name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )

        return tool.execute(
            **kwargs,
        )

    def available_tools(self) -> list[str]:

        return list(
            self.tools.keys()
        )
