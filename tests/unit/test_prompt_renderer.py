from agent_framework.message import AssistantMessage, UserMessage
from agent_framework.prompt import Prompt
from agent_framework.prompt_renderer import PromptRenderer


def test_prompt_renderer_renders_all_sections():
    prompt = Prompt(
        system="You are a financial analyst.",
        goal="Analyze Apple.",
        context="Revenue increased by 8%.",
        messages=[
            UserMessage(content="What is Apple's revenue?"),
            AssistantMessage(content="Let me analyze it."),
        ],
        available_tools=["financial_data", "stock_price"],
        output_format="Return a concise analysis.",
    )

    renderer = PromptRenderer()

    result = renderer.render(prompt)

    expected = (
        "System:\nYou are a financial analyst.\n\n"
        "Goal:\nAnalyze Apple.\n\n"
        "Context:\nRevenue increased by 8%.\n\n"
        "Messages:\n"
        "user: What is Apple's revenue?\n"
        "assistant: Let me analyze it.\n\n"
        "Available Tools:\n"
        "- financial_data\n"
        "- stock_price\n\n"
        "Output Format:\nReturn a concise analysis."
    )

    assert result == expected


def test_prompt_renderer_handles_empty_messages_and_tools():
    prompt = Prompt(
        system="System",
        goal="Goal",
        context="Context",
    )

    renderer = PromptRenderer()

    result = renderer.render(prompt)

    expected = (
        "System:\nSystem\n\n"
        "Goal:\nGoal\n\n"
        "Context:\nContext\n\n"
        "Messages:\n\n"
        "Available Tools:\n\n"
        "Output Format:\n"
    )

    assert result == expected
