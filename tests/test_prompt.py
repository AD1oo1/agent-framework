from agent_framework.prompt import Prompt

from agent_framework.message import UserMessage


def test_prompt_creation():
    prompt = Prompt(
        system="You are a financial analyst.",
        goal="Analyze Apple.",
        context="Revenue increased by 8%.",
        available_tools=["financial_data"],
        output_format="Return a concise analysis.",
    )

    assert prompt.system == "You are a financial analyst."
    assert prompt.goal == "Analyze Apple."
    assert prompt.context == "Revenue increased by 8%."
    assert prompt.available_tools == ["financial_data"]
    assert prompt.output_format == "Return a concise analysis."


def test_prompt_tools_are_independent():
    prompt1 = Prompt(
        system="System",
        goal="Goal 1",
        context="Context",
    )

    prompt2 = Prompt(
        system="System",
        goal="Goal 2",
        context="Context",
    )

    prompt1.available_tools.append("financial_data")

    assert prompt1.available_tools == ["financial_data"]
    assert prompt2.available_tools == []


def test_prompt_optional_fields_have_defaults():
    prompt = Prompt(
        system="System",
        goal="Goal",
        context="Context",
    )

    assert prompt.available_tools == []
    assert prompt.output_format == ""

def test_prompt_messages_are_independent():
    message = UserMessage(
        content="Analyze Apple's revenue."
    )

    prompt = Prompt(
        system="System",
        goal="Analyze Apple",
        context="Context",
        messages=[message],
    )

    assert len(prompt.messages) == 1
    assert prompt.messages[0] is message
