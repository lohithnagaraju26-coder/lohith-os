from core.decision_state import DecisionState
from consulting.framework_executor import (
    local_framework_executor,
    run_adaptive_framework_chain,
)


def test_adaptive_framework_chain_stops_after_sufficient_progress():
    state = DecisionState(
        objective="Determine the best strategy for improving revenue."
    )

    result = run_adaptive_framework_chain(
        state,
        local_framework_executor,
        max_steps=3,
    )

    assert result is state

    assert state.findings
    assert state.decisions
    assert state.stopping_status == "STOP"

    assert state.version > 0
    assert len(state.history) > 0

    framework_executions = [
        transition
        for transition in state.history
        if transition.action == "EXECUTE_FRAMEWORK"
    ]

    assert 1 <= len(framework_executions) <= 3

    assert all(
        transition.metadata.get("framework")
        for transition in framework_executions
    )

    assert all(
        transition.metadata.get("status") == "COMPLETE_LOCAL_PLACEHOLDER"
        for transition in framework_executions
    )


def test_adaptive_framework_chain_does_not_execute_duplicate_frameworks():
    state = DecisionState(
        objective="Determine the best strategy for improving revenue."
    )

    run_adaptive_framework_chain(
        state,
        local_framework_executor,
        max_steps=5,
    )

    executed_frameworks = [
        transition.metadata.get("framework")
        for transition in state.history
        if transition.action == "EXECUTE_FRAMEWORK"
    ]

    assert len(executed_frameworks) == len(set(executed_frameworks))


def test_adaptive_framework_chain_preserves_state_history():
    state = DecisionState(
        objective="Determine whether to build or buy a software capability."
    )

    initial_version = state.version

    run_adaptive_framework_chain(
        state,
        local_framework_executor,
        max_steps=3,
    )

    assert state.version > initial_version
    assert state.history

    versions = [
        transition.after_version
        for transition in state.history
    ]

    assert versions == sorted(versions)
    assert versions[-1] == state.version