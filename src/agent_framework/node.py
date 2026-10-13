from abc import ABC, abstractmethod

from agent_framework.state import AgentState


class Node(ABC):

    @abstractmethod
    def execute(self, state: AgentState) -> AgentState:
        """Execute the node against the current agent state."""
        ...
