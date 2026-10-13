from agent_framework.router import ConditionalRouter
from agent_framework.state import AgentState


def test_conditional_router_returns_target_node():

    router = ConditionalRouter(
        routes={
            "healthy": lambda state: True,
        },
    )

    state = AgentState(
        goal="Test routing."
    )

    target = router.route(state)

    assert target == "healthy"

def test_conditional_router_returns_first_matching_route():

    router = ConditionalRouter(
        routes={
            "healthy": lambda state: True,
            "risky": lambda state: True,
        },
    )

    state = AgentState(
        goal="Test route priority."
    )

    target = router.route(state)

    assert target == "healthy"

import pytest


def test_conditional_router_raises_when_no_route_matches():

    router = ConditionalRouter(
        routes={
            "healthy": lambda state: False,
            "risky": lambda state: False,
        },
    )

    state = AgentState(
        goal="Test unmatched routing."
    )

    with pytest.raises(
        ValueError,
        match="No conditional route matched.",
    ):
        router.route(state)
