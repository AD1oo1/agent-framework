from agent_framework import state
from agent_framework.prompt import Prompt
from agent_framework.state import AgentState


class PromptBuilder:

    def build(self, state: AgentState) -> Prompt:
        return Prompt(
            system="You are a financial analyst.",
            goal=state.goal,
            context=self._build_context(state),
            messages=state.messages,
            available_tools=self._get_available_tools(state),
            output_format="Return a concise financial analysis.",
)


    def _build_context(
        self,
        state: AgentState,
    ) -> str:

        context_parts = []

        for tool_result in state.tool_results:

            if tool_result.success:
                context_parts.append(
                    str(tool_result.result)
                )

        for chunk in state.retrieved_chunks:

            context_parts.append(
                chunk.content
            )

        return "\n".join(
            context_parts
        )



    def _get_available_tools(self, state: AgentState) -> list[str]:
        return [
            tool_result.tool_name
            for tool_result in state.tool_results
            if tool_result.success
        ]
