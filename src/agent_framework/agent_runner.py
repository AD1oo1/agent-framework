from agent_framework.state import AgentState
from agent_framework.workflow import Workflow


class AgentRunner:

    def __init__(
        self,
        workflow: Workflow,
    ) -> None:
        self.workflow = workflow

    def run(
        self,
        state: AgentState,
    ) -> AgentState:

        return self.workflow.run(state)
