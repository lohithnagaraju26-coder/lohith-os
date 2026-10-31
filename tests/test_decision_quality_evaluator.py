from core.decision_quality_evaluator import (
    evaluate_decision_quality,
)
from core.decision_state import DecisionState
from core.entities import (
    Contradiction,
    DecisionOption,
    Evidence,
    Finding,
    Recommendation,
    Risk,
)


def evidence(
    evidence_id: str,
    strength: float = 0.9,
) -> Evidence:
    return Evidence(
        id=evidence_id,
        type="DATA",
        claim=f"Evidence {evidence_id}",
        source="test",
        strength=strength,
    )


def option(option_id: str) -> DecisionOption:
    return DecisionOption(
        id=option_id,
        name=option_id,
        description=f"Option {option_id}",
    )


def recommendation(
    evidence_ids=None,
    confidence=0.8,
) -> Recommendation:
    return Recommendation(
        statement="Choose option A.",
        rationale="The evidence supports option A.",
        evidence_ids=evidence_ids or [],
        confidence=confidence,
    )


def test_no_recommendation_is_not_ready():
    state = DecisionState(
        objective="Choose the best option."
    )

    result = evaluate_decision_quality(state)

    assert not result.decision_ready
    assert result.overall_score == 0.0
    assert "No recommendation exists." in result.critical_gaps


def test_recommendation_without_evidence_is_not_ready():
    state = DecisionState(
        objective="Choose the best option.",
        recommendation=recommendation(),
    )

    result = evaluate_decision_quality(state)

    assert not result.decision_ready
    assert result.evidence_support == 0.0
    assert any(
        "supporting evidence" in gap
        for gap in result.critical_gaps
    )


def test_strong_recommendation_is_high_quality():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[
            evidence("e1", 0.9),
            evidence("e2", 0.8),
        ],
        findings=[
            Finding(
                id="f1",
                statement="Option A has the strongest economics.",
                evidence_ids=["e1", "e2"],
                confidence=0.9,
            )
        ],
        options=[
            option("a"),
            option("b"),
        ],
        risks=[
            Risk(
                id="r1",
                description="Implementation risk",
                probability=0.2,
                impact=0.4,
                mitigation="Pilot first",
                evidence_ids=["e1"],
            )
        ],
        recommendation=recommendation(
            ["e1", "e2"],
            confidence=0.85,
        ),
    )

    result = evaluate_decision_quality(state)

    assert result.decision_ready
    assert result.overall_score >= 0.70
    assert result.evidence_support >= 0.75
    assert result.alternative_quality == 1.0


def test_unresolved_contradiction_blocks_readiness():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[
            evidence("e1", 0.9),
            evidence("e2", 0.9),
        ],
        findings=[
            Finding(
                id="f1",
                statement="Option A is attractive.",
                evidence_ids=["e1"],
                confidence=0.9,
            )
        ],
        options=[
            option("a"),
            option("b"),
        ],
        risks=[
            Risk(
                id="r1",
                description="Implementation risk",
                probability=0.2,
                impact=0.4,
                mitigation="Pilot",
            )
        ],
        contradictions=[
            Contradiction(
                id="c1",
                description="Evidence conflicts.",
                evidence_ids=["e1", "e2"],
                severity=1.0,
                resolved=False,
            )
        ],
        recommendation=recommendation(
            ["e1", "e2"],
            confidence=0.9,
        ),
    )

    result = evaluate_decision_quality(state)

    assert not result.decision_ready
    assert result.contradiction_robustness == 0.0
    assert any(
        "contradictory evidence" in gap
        for gap in result.critical_gaps
    )


def test_no_alternatives_is_critical_gap():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[evidence("e1")],
        findings=[
            Finding(
                id="f1",
                statement="Option A works.",
                evidence_ids=["e1"],
                confidence=0.9,
            )
        ],
        risks=[
            Risk(
                id="r1",
                description="Execution risk",
                probability=0.2,
                impact=0.3,
                mitigation="Pilot",
            )
        ],
        recommendation=recommendation(
            ["e1"],
            confidence=0.8,
        ),
    )

    result = evaluate_decision_quality(state)

    assert not result.decision_ready
    assert result.alternative_quality == 0.0
    assert any(
        "alternatives" in gap
        for gap in result.critical_gaps
    )


def test_one_alternative_reduces_quality():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[evidence("e1")],
        findings=[
            Finding(
                id="f1",
                statement="Option A works.",
                evidence_ids=["e1"],
                confidence=0.9,
            )
        ],
        options=[option("a")],
        risks=[
            Risk(
                id="r1",
                description="Execution risk",
                probability=0.2,
                impact=0.3,
                mitigation="Pilot",
            )
        ],
        recommendation=recommendation(
            ["e1"],
            confidence=0.8,
        ),
    )

    result = evaluate_decision_quality(state)

    assert result.alternative_quality == 0.5
    assert not result.decision_ready


def test_high_confidence_with_weak_evidence_is_calibration_failure():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[evidence("e1", 0.2)],
        findings=[
            Finding(
                id="f1",
                statement="Weak evidence suggests option A.",
                evidence_ids=["e1"],
                confidence=0.3,
            )
        ],
        options=[
            option("a"),
            option("b"),
        ],
        risks=[
            Risk(
                id="r1",
                description="Execution risk",
                probability=0.2,
                impact=0.3,
                mitigation="Pilot",
            )
        ],
        recommendation=recommendation(
            ["e1"],
            confidence=0.99,
        ),
    )

    result = evaluate_decision_quality(state)

    assert result.confidence_calibration < 0.75
    assert any(
        "calibrated" in weakness
        for weakness in result.weaknesses
    )


def test_unknowns_reduce_risk_uncertainty_quality():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[evidence("e1", 0.9)],
        findings=[
            Finding(
                id="f1",
                statement="Option A is supported.",
                evidence_ids=["e1"],
                confidence=0.9,
            )
        ],
        options=[
            option("a"),
            option("b"),
        ],
        risks=[
            Risk(
                id="r1",
                description="Execution risk",
                probability=0.2,
                impact=0.3,
                mitigation="Pilot",
            )
        ],
        unknowns=[
            "Market response remains unknown.",
            "Implementation cost remains unknown.",
        ],
        recommendation=recommendation(
            ["e1"],
            confidence=0.8,
        ),
    )

    result = evaluate_decision_quality(state)

    assert result.risk_uncertainty < 1.0
    assert not result.decision_ready


def test_resolved_contradiction_does_not_block_readiness():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[
            evidence("e1", 0.9),
            evidence("e2", 0.8),
        ],
        findings=[
            Finding(
                id="f1",
                statement="Option A is supported.",
                evidence_ids=["e1", "e2"],
                confidence=0.9,
            )
        ],
        options=[
            option("a"),
            option("b"),
        ],
        risks=[
            Risk(
                id="r1",
                description="Execution risk",
                probability=0.2,
                impact=0.3,
                mitigation="Pilot",
            )
        ],
        contradictions=[
            Contradiction(
                id="c1",
                description="Previously conflicting evidence.",
                evidence_ids=["e1", "e2"],
                severity=0.9,
                resolved=True,
                resolution="Additional evidence resolved the conflict.",
            )
        ],
        recommendation=recommendation(
            ["e1", "e2"],
            confidence=0.85,
        ),
    )

    result = evaluate_decision_quality(state)

    assert result.contradiction_robustness == 1.0


def test_evaluator_does_not_mutate_state():
    state = DecisionState(
        objective="Choose the best option.",
        evidence=[evidence("e1")],
        options=[
            option("a"),
            option("b"),
        ],
        recommendation=recommendation(
            ["e1"],
            confidence=0.8,
        ),
    )

    before = state.model_dump()
    evaluate_decision_quality(state)
    after = state.model_dump()

    assert before == after


if __name__ == "__main__":
    print("PASS — Decision Quality Evaluator V1 tests loaded.")
