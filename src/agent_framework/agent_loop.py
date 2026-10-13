from agent_framework.llm_client import LLMClient
from agent_framework.prompt_builder import PromptBuilder
from agent_framework.prompt_renderer import PromptRenderer
from agent_framework.state import AgentState
from agent_framework.tool_executor import ToolExecutor


class AgentLoop:

    def __init__(
        self,
        llm_client: LLMClient,
        tool_executor: ToolExecutor,
        prompt_builder: PromptBuilder,
        prompt_renderer: PromptRenderer,
        max_iterations: int = 5,
    ) -> None:

        if max_iterations <= 0:
            raise ValueError(
                "max_iterations must be greater than 0."
            )

        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.prompt_builder = prompt_builder
        self.prompt_renderer = prompt_renderer
        self.max_iterations = max_iterations

    def run(
        self,
        state: AgentState,
    ) -> AgentState:

        for _ in range(self.max_iterations):

            prompt = self.prompt_builder.build(
                state
            )

            rendered_prompt = (
                self.prompt_renderer.render(
                    prompt
                )
            )

            response = self.llm_client.generate(
                rendered_prompt
            )

            if response.tool_calls:

                for tool_call in response.tool_calls:

                    result = (
                        self.tool_executor.execute(
                            tool_name=tool_call.tool_name,
                            **tool_call.arguments,
                        )
                    )

                    state.add_tool_result(
                        result
                    )

                continue

            state.set_final_answer(
                response.content
            )

            return state

        raise RuntimeError(
            "Agent loop exceeded maximum iterations."
        )
