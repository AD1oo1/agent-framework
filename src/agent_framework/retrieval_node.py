from agent_framework.node import Node
from agent_framework.retreiver import Retriever
from agent_framework.state import AgentState


class RetrievalNode(Node):

    def __init__(
        self,
        retriever: Retriever,
        top_k: int = 5,
    ) -> None:

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        self.retriever = retriever
        self.top_k = top_k

    def execute(
        self,
        state: AgentState,
    ) -> AgentState:

        chunks = self.retriever.retrieve(
            query=state.goal,
            top_k=self.top_k,
        )

        for chunk in chunks:
            state.add_retrieved_chunk(chunk)

        return state
