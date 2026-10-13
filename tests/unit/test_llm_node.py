from agent_framework.llm_node import LLMNode
from agent_framework.llm_response import LLMResponse
from agent_framework.prompt import Prompt
from agent_framework.state import AgentState


class FakePromptBuilder:

    def __init__(self):
        self.received_state = None

    def build(self, state: AgentState) -> Prompt:
        self.received_state = state

        return Prompt(
            system="System",
            goal=state.goal,
            context="Context",
        )


class FakePromptRenderer:

    def __init__(self):
        self.received_prompt = None

    def render(self, prompt: Prompt) -> str:
        self.received_prompt = prompt
        return "Rendered prompt"


class FakeLLMClient:

    def __init__(self):
        self.received_prompt = None

    def generate(self, prompt: str) -> LLMResponse:
        self.received_prompt = prompt

        return LLMResponse(
            content="Generated financial analysis"
        )


def test_llm_node_builds_renders_and_generates():

    state = AgentState(
        goal="Analyze Apple's financial health."
    )

    prompt_builder = FakePromptBuilder()
    prompt_renderer = FakePromptRenderer()
    llm_client = FakeLLMClient()

    node = LLMNode(
        prompt_builder=prompt_builder,
        prompt_renderer=prompt_renderer,
        llm_client=llm_client,
    )

    result = node.execute(state)

    assert result is state

    assert prompt_builder.received_state is state

    assert prompt_renderer.received_prompt is not None

    assert llm_client.received_prompt == "Rendered prompt"


def test_llm_node_stores_llm_response_as_final_answer():

    state = AgentState(
        goal="Analyze Apple's financial health."
    )

    prompt_builder = FakePromptBuilder()
    prompt_renderer = FakePromptRenderer()
    llm_client = FakeLLMClient()

    node = LLMNode(
        prompt_builder=prompt_builder,
        prompt_renderer=prompt_renderer,
        llm_client=llm_client,
    )

    node.execute(state)

    assert state.final_answer == "Generated financial analysis"
