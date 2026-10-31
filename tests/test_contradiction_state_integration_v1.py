from core.decision_state import DecisionState
from core.entities import Evidence, EvidenceType, Hypothesis


def test_evidence_hypothesis_contradiction_integration() -> None:
    state = DecisionState(
        objective="Determine whether price is the primary cause of churn.",
        hypotheses=[
            Hypothesis(
                id="H1",
                statement="Price is the primary cause of churn.",
            )
        ],
    )

    initial_version = state.version

    state.add_evidence_and_update_reasoning_state(
        Evidence(
            id="E1",
            type=EvidenceType.DATA,
            claim="Customers cite price as a major reason for churn.",
            strength=0.9,
            supports=["H1"],
        )
    )

    assert state.version == initial_version + 1
    assert len(state.evidence) == 1
    assert state.hypotheses[0].status.value == "SUPPORTED"
    assert state.contradictions == []

    result = state.add_evidence_and_update_reasoning_state(
        Evidence(
            id="E2",
            type=EvidenceType.DATA,
            claim="Customers report that pricing is not a major reason for churn.",
            strength=0.7,
            contradicts=["H1"],
        )
    )

    assert state.version == initial_version + 2
    assert len(state.evidence) == 2
    assert len(state.contradictions) == 1

    contradiction = state.contradictions[0]

    assert contradiction.hypothesis_ids == ["H1"]
    assert contradiction.evidence_ids == ["E1", "E2"]
    assert contradiction.resolved is False
    assert contradiction.severity == 0.8

    assert len(result["hypothesis_evaluations"]) == 1
    assert len(result["detected_contradictions"]) == 1

    print("PASS — Atomic evidence/hypothesis/contradiction integration.")
    print(f"Version: {state.version}")
    print(f"Hypothesis status: {state.hypotheses[0].status.value}")
    print(f"Contradictions: {len(state.contradictions)}")
    print(f"Contradiction severity: {contradiction.severity}")


if __name__ == "__main__":
    test_evidence_hypothesis_contradiction_integration()
