from agent_framework.prompt import Prompt


class PromptRenderer:

    def render(self, prompt: Prompt) -> str:
        sections = [
            f"System:\n{prompt.system}",
            f"Goal:\n{prompt.goal}",
            f"Context:\n{prompt.context}",
            self._render_messages(prompt),
            self._render_tools(prompt),
            f"Output Format:\n{prompt.output_format}",
        ]

        return "\n\n".join(sections)

    def _render_messages(self, prompt: Prompt) -> str:
        if not prompt.messages:
            return "Messages:"

        messages = "\n".join(
            f"{message.role.value}: {message.content}"
            for message in prompt.messages
        )

        return f"Messages:\n{messages}"

    def _render_tools(self, prompt: Prompt) -> str:
        if not prompt.available_tools:
            return "Available Tools:"

        tools = "\n".join(
            f"- {tool}"
            for tool in prompt.available_tools
        )

        return f"Available Tools:\n{tools}"
