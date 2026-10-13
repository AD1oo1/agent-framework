from agent_framework.message import UserMessage
from agent_framework.state import AgentState
from agent_framework.tool import ToolResult


def test_agent_state_has_empty_messages_by_default():
    state = AgentState(goal="Analyze Apple's financial health")

    assert state.messages == []


def test_agent_state_messages_are_independent():
    state_1 = AgentState(goal="Goal 1")
    state_2 = AgentState(goal="Goal 2")

    state_1.messages.append(
        UserMessage(content="Hello")
    )

    assert len(state_1.messages) == 1
    assert len(state_2.messages) == 0


def test_agent_state_has_empty_tool_results_by_default():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    assert state.tool_results == []


def test_agent_state_tool_results_are_independent():
    state_1 = AgentState(goal="Goal 1")
    state_2 = AgentState(goal="Goal 2")

    state_1.tool_results.append(
        ToolResult(
            tool_name="stock_price",
            result={"price": 230},
        )
    )

    assert len(state_1.tool_results) == 1
    assert len(state_2.tool_results) == 0

def test_agent_state_has_empty_plan_by_default():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    assert state.current_plan == []


def test_agent_state_can_store_plan_steps():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    state.current_plan = [
        "Fetch financial statements",
        "Analyze revenue",
        "Analyze profitability",
    ]

    assert len(state.current_plan) == 3
    assert state.current_plan[0] == "Fetch financial statements"
    assert state.current_plan[2] == "Analyze profitability"

def test_agent_state_has_no_final_answer_by_default():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    assert state.final_answer is None


def test_agent_state_can_store_final_answer():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    state.final_answer = "Apple shows strong financial health."

    assert state.final_answer == "Apple shows strong financial health."

def test_agent_state_has_zero_retries_by_default():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    assert state.retry_count == 0


def test_agent_state_can_track_retries():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    state.retry_count += 1
    state.retry_count += 1

    assert state.retry_count == 2


def test_agent_state_has_empty_errors_by_default():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    assert state.errors == []


def test_agent_state_can_track_errors():
    state = AgentState(
        goal="Analyze Apple's financial health"
    )

    state.errors.append("LLM request timed out")
    state.errors.append("Tool execution failed")

    assert len(state.errors) == 2
    assert state.errors[0] == "LLM request timed out"
    assert state.errors[1] == "Tool execution failed"

def test_add_message():
    state = AgentState(goal="Analyze Apple")

    message = UserMessage(content="Analyze Apple's revenue")

    state.add_message(message)

    assert len(state.messages) == 1
    assert state.messages[0] is message


def test_add_tool_result():
    state = AgentState(goal="Analyze Apple")

    result = ToolResult(
        tool_name="financial_data",
        result={"revenue": 100},
    )

    state.add_tool_result(result)

    assert len(state.tool_results) == 1
    assert state.tool_results[0] is result


def test_add_error():
    state = AgentState(goal="Analyze Apple")

    state.add_error("Financial API failed")

    assert state.errors == ["Financial API failed"]


def test_increment_retry():
    state = AgentState(goal="Analyze Apple")

    state.increment_retry()
    state.increment_retry()

    assert state.retry_count == 2


def test_set_final_answer():
    state = AgentState(goal="Analyze Apple")

    state.set_final_answer("Apple has strong financial health.")

    assert state.final_answer == "Apple has strong financial health."
