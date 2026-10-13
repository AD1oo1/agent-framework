from collections.abc import Callable
from datetime import datetime, timezone
from uuid import uuid4

from agent_framework.node import Node
from agent_framework.node_execution import (
    NodeExecution,
    NodeExecutionStatus,
)
from agent_framework.state import AgentState


class Workflow:

    def __init__(
        self,
        max_node_retries: int = 0,
    ) -> None:

        if max_node_retries < 0:
            raise ValueError(
                "max_node_retries cannot be negative."
            )

        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, list[str]] = {}
        self.max_node_retries: int = max_node_retries

        self.conditional_edges: dict[
            str,
            Callable[[AgentState], str],
        ] = {}

        self.entry_point: str | None = None
        self._executions: list[NodeExecution] = []

    @property
    def executions(self) -> tuple[NodeExecution, ...]:
        return tuple(self._executions)

    def add_node(
        self,
        name: str,
        node: Node,
    ) -> None:

        if name in self.nodes:
            raise ValueError(
                f"Node '{name}' is already registered."
            )

        self.nodes[name] = node

    def add_edge(
        self,
        source: str,
        target: str,
    ) -> None:

        if source not in self.nodes:
            raise ValueError(
                f"Source node '{source}' is not registered."
            )

        if target not in self.nodes:
            raise ValueError(
                f"Target node '{target}' is not registered."
            )

        self.edges.setdefault(source, []).append(target)

    def add_conditional_edge(
        self,
        source: str,
        condition: Callable[[AgentState], str],
    ) -> None:

        if source not in self.nodes:
            raise ValueError(
                f"Source node '{source}' is not registered."
            )

        if source in self.edges:
            raise ValueError(
                f"Node '{source}' cannot have both "
                "static and conditional edges."
            )

        if source in self.conditional_edges:
            raise ValueError(
                f"Node '{source}' already has a conditional edge is already registered."
            )

        self.conditional_edges[source] = condition

    def set_entry_point(
        self,
        name: str,
    ) -> None:

        if name not in self.nodes:
            raise ValueError(
                f"Entry point '{name}' is not registered."
            )

        self.entry_point = name

    def run(
        self,
        state: AgentState,
    ) -> AgentState:

        if not self.nodes:
            return state

        if self.entry_point is None:
            raise ValueError(
                "Workflow entry point is not configured."
            )

        self._executions.clear()

        run_id = str(uuid4())

        # ---------------------------------------------------------
        # Step 1: Discover nodes reachable through static edges
        # ---------------------------------------------------------

        reachable_nodes: set[str] = set()
        pending_discovery = [self.entry_point]

        while pending_discovery:

            current = pending_discovery.pop(0)

            if current in reachable_nodes:
                continue

            reachable_nodes.add(current)

            for target in self.edges.get(current, []):
                pending_discovery.append(target)

        # ---------------------------------------------------------
        # Step 2: Calculate indegree for the static graph
        # ---------------------------------------------------------

        indegree: dict[str, int] = {
            node_name: 0
            for node_name in reachable_nodes
        }

        for source in reachable_nodes:

            for target in self.edges.get(source, []):

                if target in reachable_nodes:
                    indegree[target] += 1

        # ---------------------------------------------------------
        # Step 3: Entry point cannot have an incoming dependency
        # ---------------------------------------------------------

        if indegree[self.entry_point] != 0:
            raise ValueError(
                "Workflow contains a cycle."
            )

        # ---------------------------------------------------------
        # Step 4: Execute workflow
        # ---------------------------------------------------------

        pending_nodes = [self.entry_point]
        processed_nodes: set[str] = set()

        while pending_nodes:

            current = pending_nodes.pop(0)

            if current in processed_nodes:
                raise ValueError(
                    "Workflow contains a cycle."
                )

            # -----------------------------------------------------
            # Create execution telemetry
            # -----------------------------------------------------

            execution = NodeExecution(
                node_name=current,
                status=NodeExecutionStatus.RUNNING,
                run_id=run_id,
                started_at=datetime.now(timezone.utc),
            )

            self._executions.append(execution)

            node = self.nodes[current]

            # -----------------------------------------------------
            # Execute node
            # -----------------------------------------------------

            attempts = 0

            while True:

                attempts += 1
                execution.attempts = attempts

                try:

                    state = node.execute(state)

                    break

                except Exception as error:

                    if attempts > self.max_node_retries:

                        execution.status = (
                            NodeExecutionStatus.FAILED
                        )

                        execution.completed_at = (
                            datetime.now(timezone.utc)
                        )

                        execution.duration = (
                            execution.completed_at
                            -  execution.started_at
                        ).total_seconds()

                        raise error

            # -----------------------------------------------------
            # Mark execution as completed
            # -----------------------------------------------------

            execution.status = (
                NodeExecutionStatus.COMPLETED
            )

            execution.completed_at = (
                datetime.now(timezone.utc)
            )

            execution.duration = (
                execution.completed_at
                - execution.started_at
            ).total_seconds()

            processed_nodes.add(current)

            # -----------------------------------------------------
            # Conditional routing
            # -----------------------------------------------------

            conditional_edge = self.conditional_edges.get(
                current
            )

            if conditional_edge is not None:

                target = conditional_edge(state)

                if target not in self.nodes:
                    raise ValueError(
                        f"Conditional target node "
                        f"'{target}' is not registered."
                    )

                if target in processed_nodes:
                    raise ValueError(
                        "Workflow contains a cycle."
                    )

                pending_nodes.append(target)

            # -----------------------------------------------------
            # Static edges
            # -----------------------------------------------------

            for target in self.edges.get(current, []):

                indegree[target] -= 1

                if indegree[target] == 0:
                    pending_nodes.append(target)

        # ---------------------------------------------------------
        # Step 5: Validate static graph completion
        #
        # Only compare against statically reachable nodes.
        # Conditional targets are discovered dynamically.
        # ---------------------------------------------------------

        static_processed_nodes = (
            processed_nodes.intersection(reachable_nodes)
        )

        if len(static_processed_nodes) != len(reachable_nodes):
            raise ValueError(
                "Workflow contains a cycle."
            )

        return state
