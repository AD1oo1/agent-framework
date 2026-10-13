from collections.abc import Callable

from agent_framework.state import AgentState


class ConditionalRouter:

    def __init__(
        self,
        routes: dict[str, Callable[[AgentState], bool]],
    ) -> None:
        self.routes = routes

    def route(
        self,
        state: AgentState,
    ) -> str:

        for target, condition in self.routes.items():

            if condition(state):
                return target

        raise ValueError(
            "No conditional route matched."
        )
