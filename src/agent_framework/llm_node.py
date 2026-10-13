from agent_framework.llm_client import LLMClient
from agent_framework.node import Node
from agent_framework.prompt_builder import PromptBuilder
from agent_framework.prompt_renderer import PromptRenderer
from agent_framework.state import AgentState


class LLMNode(Node):

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        prompt_renderer: PromptRenderer,
        llm_client: LLMClient,
    ) -> None:
        self.prompt_builder = prompt_builder
        self.prompt_renderer = prompt_renderer
        self.llm_client = llm_client

    def execute(self, state: AgentState) -> AgentState:
        prompt = self.prompt_builder.build(state)

        rendered_prompt = self.prompt_renderer.render(prompt)

        response = self.llm_client.generate(rendered_prompt)

        state.set_final_answer(response.content)

        return state
