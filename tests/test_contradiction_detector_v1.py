from core.contradiction_detector import (
    detect_contradictions,
    merge_contradictions,
)
from core.entities import (
    Contradiction,
    Evidence,
    EvidenceType,
    Hypothesis,
)


def make_hypothesis(hypothesis_id: str = "H1") -> Hypothesis:
    return Hypothesis(
        id=hypothesis_id,
        statement="Price is the primary cause of churn.",
    )


def make_evidence(
    evidence_id: str,
    *,
    supports: list[str] | None = None,
    contradicts: list[str] | None = None,
    strength: float = 0.8,
) -> Evidence:
    return Evidence(
        id=evidence_id,
        type=EvidenceType.DATA,
        claim=f"Evidence {evidence_id}",
        strength=strength,
        supports=supports or [],
        contradicts=contradicts or [],
    )


def test_detects_conflict() -> None:
    hypothesis = make_hypothesis()

    evidence = [
        make_evidence("E1", supports=["H1"], strength=0.9),
        make_evidence("E2", contradicts=["H1"], strength=0.7),
    ]

    contradictions = detect_contradictions(
        [hypothesis],
        evidence,
    )

    assert len(contradictions) == 1

    contradiction = contradictions[0]

    assert contradiction.hypothesis_ids == ["H1"]
    assert contradiction.evidence_ids == ["E1", "E2"]
    assert contradiction.severity == 0.8
    assert contradiction.resolved is False


def test_does_not_flag_support_only() -> None:
    hypothesis = make_hypothesis()

    evidence = [
        make_evidence("E1", supports=["H1"], strength=0.9),
        make_evidence("E2", supports=["H1"], strength=0.8),
    ]

    contradictions = detect_contradictions(
        [hypothesis],
        evidence,
    )

    assert contradictions == []


def test_does_not_flag_contradiction_only() -> None:
    hypothesis = make_hypothesis()

    evidence = [
        make_evidence("E1", contradicts=["H1"], strength=0.9),
        make_evidence("E2", contradicts=["H1"], strength=0.8),
    ]

    contradictions = detect_contradictions(
        [hypothesis],
        evidence,
    )

    assert contradictions == []


def test_ignores_unrelated_evidence() -> None:
    hypothesis = make_hypothesis()

    evidence = [
        make_evidence("E1", supports=["H2"], strength=0.9),
        make_evidence("E2", contradicts=["H2"], strength=0.8),
    ]

    contradictions = detect_contradictions(
        [hypothesis],
        evidence,
    )

    assert contradictions == []


def test_merges_without_duplicates() -> None:
    existing = [
        Contradiction(
            id="C1",
            description="Existing contradiction.",
            severity=0.7,
            resolved=True,
            resolution="Resolved by additional research.",
        )
    ]

    detected = [
        Contradiction(
            id="C1",
            description="New version should not replace existing.",
            severity=0.9,
        ),
        Contradiction(
            id="C2",
            description="New contradiction.",
            severity=0.8,
        ),
    ]

    merged = merge_contradictions(existing, detected)

    assert len(merged) == 2
    assert merged[0].id == "C1"
    assert merged[0].resolved is True
    assert merged[0].resolution == "Resolved by additional research."
    assert merged[1].id == "C2"


def run_tests() -> None:
    tests = [
        test_detects_conflict,
        test_does_not_flag_support_only,
        test_does_not_flag_contradiction_only,
        test_ignores_unrelated_evidence,
        test_merges_without_duplicates,
    ]

    for test in tests:
        test()
        print(f"PASS — {test.__name__}")

    print("PASS — Contradiction Detection V1 unit tests.")


if __name__ == "__main__":
    run_tests()
