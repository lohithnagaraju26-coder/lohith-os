from __future__ import annotations

from datetime import datetime, timezone

from core.decision_state import DecisionState
from core.entities import (
    Contradiction,
    Evidence,
    EvidenceType,
    Finding,
    Outcome,
    Recommendation,
)
from core.reasoning_action import ReasoningActionType
from core.reasoning_router import route_reasoning


def make_state(
    objective: str,
    *,
    desired_outcome: str | None = None,
    known_facts: list[str] | None = None,
    unknowns: list[str] | None = None,
    evidence: list[Evidence] | None = None,
    findings: list[Finding] | None = None,
    contradictions: list[Contradiction] | None = None,
    recommendation: Recommendation | None = None,
    outcome: Outcome | None = None,
) -> DecisionState:
    now = datetime.now(timezone.utc)

    return DecisionState(
        id="test-state",
        created_at=now,
        updated_at=now,
        objective=objective,
        desired_outcome=desired_outcome,
        known_facts=known_facts or [],
        unknowns=unknowns or [],
        evidence=evidence or [],
        findings=findings or [],
        contradictions=contradictions or [],
        recommendation=recommendation,
        outcome=outcome,
    )


def assert_framework(
    name: str,
    objective: str,
    expected_framework: str,
) -> None:
    state = make_state(objective)

    action = route_reasoning(state)

    assert action.type == ReasoningActionType.FRAMEWORK, (
        f"{name}: expected FRAMEWORK, got {action.type}"
    )

    assert action.target == expected_framework, (
        f"{name}: expected {expected_framework}, "
        f"got {action.target}"
    )


def run_tests() -> None:
    tests = []

    # 1. Revenue decline
    tests.append(
        lambda: assert_framework(
            "Revenue decline",
            "Revenue has declined significantly and management needs to identify the main drivers.",
            "Revenue Decomposition",
        )
    )

    # 2. Customer retention
    tests.append(
        lambda: assert_framework(
            "Customer retention",
            "Customer retention has deteriorated and we need to identify which customer cohorts are responsible.",
            "Cohort Analysis",
        )
    )

    # 3. Build vs Buy
    tests.append(
        lambda: assert_framework(
            "Build vs Buy",
            "We need to decide whether to build an AI capability internally, buy it from a vendor, or use a hybrid approach.",
            "Build vs Buy",
        )
    )

    # 4. AI feasibility
    tests.append(
        lambda: assert_framework(
            "AI feasibility",
            "We are considering AI automation for a repetitive business workflow and need to determine whether AI can perform the work reliably enough to create value.",
            "AI Feasibility Assessment",
        )
    )

    # 5. Competitive pressure
    tests.append(
        lambda: assert_framework(
            "Competitive pressure",
            "Competitive pressure is increasing and management needs to understand the structural attractiveness of the industry.",
            "Porter's Five Forces",
        )
    )

    # 6. Material unknown
    def test_material_unknown() -> None:
        state = make_state(
            "Determine whether we should launch the new product.",
            unknowns=[
                "We do not know the size of the addressable market."
            ],
        )

        action = route_reasoning(state)

        assert action.type == ReasoningActionType.RESEARCH
        assert action.target is None

    tests.append(test_material_unknown)

    # 7. Multiple unknowns
    def test_multiple_unknowns() -> None:
        state = make_state(
            "Evaluate whether we should enter the market.",
            unknowns=[
                "Market size is unknown.",
                "Competitor pricing is unknown.",
                "Customer willingness to pay is unknown.",
            ],
        )

        action = route_reasoning(state)

        assert action.type == ReasoningActionType.RESEARCH

    tests.append(test_multiple_unknowns)

    # 8. Contradictory evidence
    def test_contradiction() -> None:
        state = make_state(
            "Determine whether the proposed strategy is working.",
            known_facts=[
                "One dataset indicates improving performance.",
                "Another dataset indicates declining performance.",
            ],
            contradictions=[
                Contradiction(
                    id="c1",
                    description="Two reliable datasets disagree about performance.",
                    severity=0.9,
                )
            ],
        )

        action = route_reasoning(state)

        assert action.type == ReasoningActionType.RESEARCH

    tests.append(test_contradiction)

    # 9. Completed recommendation
    def test_completed_recommendation() -> None:
        state = make_state(
            "Choose the best strategic option.",
            recommendation=Recommendation(
                statement="Proceed with Option A.",
                rationale="Option A has the strongest evidence.",
                confidence=0.9,
            ),
        )

        action = route_reasoning(state)

        assert action.type == ReasoningActionType.STOP

    tests.append(test_completed_recommendation)

    # 10. Recorded outcome
    def test_recorded_outcome() -> None:
        state = make_state(
            "Execute the selected strategy.",
            outcome=Outcome(
                expected="Increase revenue.",
                actual="Revenue increased.",
                success=True,
            ),
        )

        action = route_reasoning(state)

        assert action.type == ReasoningActionType.STOP

    tests.append(test_recorded_outcome)

    # 11. Fresh strategic problem
    tests.append(
        lambda: assert_framework(
            "Fresh strategic problem",
            "Determine how the company should respond to slowing growth.",
            "Issue Tree",
        )
    )

    # 12. Broad business problem
    tests.append(
        lambda: assert_framework(
            "Broad business problem",
            "The business is underperforming and management needs to understand the major causes before deciding what to do.",
            "Issue Tree",
        )
    )

    passed = 0

    for index, test in enumerate(tests, start=1):
        try:
            test()
            print(f"PASS {index:02d}")
            passed += 1
        except AssertionError as exc:
            print(f"FAIL {index:02d}: {exc}")

    print()
    print(f"RESULT: {passed}/{len(tests)}")

    if passed != len(tests):
        raise SystemExit(1)

    print("PASS — Deterministic reasoning router V1 evaluation.")


if __name__ == "__main__":
    run_tests()