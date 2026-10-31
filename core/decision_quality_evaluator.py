"""
LOHITH OS — DECISION QUALITY EVALUATOR V1

Purpose:
    Deterministically evaluate whether a recommendation is
    sufficiently supported by the current DecisionState.

This module is:
    - read-only
    - deterministic
    - model-independent
    - independent from the reasoning router
    - independent from DecisionState mutation

Decision quality is evaluated through:
    1. Evidence support
    2. Analytical support
    3. Alternative quality
    4. Risk and uncertainty
    5. Contradiction robustness
    6. Confidence calibration

Gating rules prevent a weighted score from masking critical
decision-quality failures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set

from core.decision_state import DecisionState


@dataclass(frozen=True)
class DecisionQualityEvaluation:
    """
    Deterministic evaluation artifact.

    This object does not mutate DecisionState.
    """

    overall_score: float

    evidence_support: float
    analytical_support: float
    alternative_quality: float
    risk_uncertainty: float
    contradiction_robustness: float
    confidence_calibration: float

    strengths: List[str]
    weaknesses: List[str]
    critical_gaps: List[str]

    decision_ready: bool
    recommendation: str


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _referenced_evidence(
    state: DecisionState,
) -> tuple[Set[str], Set[str]]:
    """
    Return:
        valid recommendation evidence IDs
        all evidence IDs referenced by the recommendation
    """

    if state.recommendation is None:
        return set(), set()

    all_evidence_ids = {
        evidence.id
        for evidence in state.evidence
    }

    referenced = {
        evidence_id
        for evidence_id in state.recommendation.evidence_ids
    }

    valid = referenced & all_evidence_ids

    return valid, referenced


def _evidence_support(state: DecisionState) -> float:
    if state.recommendation is None:
        return 0.0

    valid_ids, referenced_ids = _referenced_evidence(state)

    if not referenced_ids:
        return 0.0

    if not valid_ids:
        return 0.0

    evidence_by_id = {
        evidence.id: evidence
        for evidence in state.evidence
    }

    strengths = [
        evidence_by_id[evidence_id].strength
        for evidence_id in valid_ids
    ]

    reference_validity = (
        len(valid_ids) / len(referenced_ids)
    )

    strength = sum(strengths) / len(strengths)

    return _clamp(
        reference_validity * 0.4
        + strength * 0.6
    )


def _analytical_support(state: DecisionState) -> float:
    if state.recommendation is None:
        return 0.0

    recommendation_evidence = set(
        state.recommendation.evidence_ids
    )

    if not recommendation_evidence:
        return 0.0

    analytical_links = 0

    for finding in state.findings:
        if recommendation_evidence.intersection(
            finding.evidence_ids
        ):
            analytical_links += 1

    for decision in state.decisions:
        if recommendation_evidence.intersection(
            decision.evidence_ids
        ):
            analytical_links += 1

    if not state.findings and not state.decisions:
        return 0.0

    analytical_artifacts = (
        len(state.findings) + len(state.decisions)
    )

    return _clamp(
        analytical_links / analytical_artifacts
    )


def _alternative_quality(state: DecisionState) -> float:
    if len(state.options) >= 2:
        return 1.0

    if len(state.options) == 1:
        return 0.5

    return 0.0


def _risk_uncertainty(state: DecisionState) -> float:
    risk_score = 1.0 if state.risks else 0.0

    unknown_score = (
        1.0
        if not state.unknowns
        else max(
            0.0,
            1.0 - min(len(state.unknowns) / 5.0, 1.0),
        )
    )

    return _clamp(
        risk_score * 0.5
        + unknown_score * 0.5
    )


def _contradiction_robustness(
    state: DecisionState,
) -> float:
    unresolved = [
        contradiction
        for contradiction in state.contradictions
        if not contradiction.resolved
    ]

    if not unresolved:
        return 1.0

    severity = max(
        contradiction.severity
        for contradiction in unresolved
    )

    return _clamp(1.0 - severity)


def _confidence_calibration(
    state: DecisionState,
    underlying_support: float,
) -> float:
    if state.recommendation is None:
        return 0.0

    confidence = state.recommendation.confidence

    calibration_error = abs(
        confidence - underlying_support
    )

    if confidence > underlying_support:
        overconfidence_penalty = calibration_error * 1.5
    else:
        overconfidence_penalty = calibration_error

    return _clamp(
        1.0 - overconfidence_penalty
    )


def evaluate_decision_quality(
    state: DecisionState,
) -> DecisionQualityEvaluation:
    """
    Evaluate decision quality without mutating the state.
    """

    if not isinstance(state, DecisionState):
        raise TypeError(
            "evaluate_decision_quality requires a DecisionState."
        )

    if state.recommendation is None:
        return DecisionQualityEvaluation(
            overall_score=0.0,
            evidence_support=0.0,
            analytical_support=0.0,
            alternative_quality=0.0,
            risk_uncertainty=0.0,
            contradiction_robustness=1.0,
            confidence_calibration=0.0,
            strengths=[],
            weaknesses=[],
            critical_gaps=[
                "No recommendation exists."
            ],
            decision_ready=False,
            recommendation=(
                "Needs more work: create a recommendation "
                "before evaluating decision quality."
            ),
        )

    evidence_support = _evidence_support(state)
    analytical_support = _analytical_support(state)
    alternative_quality = _alternative_quality(state)
    risk_uncertainty = _risk_uncertainty(state)
    contradiction_robustness = (
        _contradiction_robustness(state)
    )

    underlying_support = _clamp(
        evidence_support * 0.45
        + analytical_support * 0.35
        + alternative_quality * 0.20
    )

    confidence_calibration = _confidence_calibration(
        state,
        underlying_support,
    )

    overall_score = _clamp(
        evidence_support * 0.25
        + analytical_support * 0.20
        + alternative_quality * 0.15
        + risk_uncertainty * 0.15
        + contradiction_robustness * 0.15
        + confidence_calibration * 0.10
    )

    strengths: List[str] = []
    weaknesses: List[str] = []
    critical_gaps: List[str] = []

    if evidence_support >= 0.75:
        strengths.append(
            "Recommendation is well supported by referenced evidence."
        )
    elif evidence_support > 0:
        weaknesses.append(
            "Evidence support is incomplete or weak."
        )
    else:
        critical_gaps.append(
            "Recommendation lacks valid supporting evidence."
        )

    if analytical_support >= 0.75:
        strengths.append(
            "Findings or decisions provide analytical support."
        )
    elif analytical_support > 0:
        weaknesses.append(
            "Analytical support is incomplete."
        )
    else:
        weaknesses.append(
            "Recommendation lacks linked analytical support."
        )

    if alternative_quality >= 1.0:
        strengths.append(
            "Multiple decision alternatives were considered."
        )
    elif alternative_quality > 0:
        critical_gaps.append(
            "Only one decision alternative is represented."
        )
    else:
        critical_gaps.append(
            "No meaningful alternatives were considered."
        )

    if risk_uncertainty >= 0.75:
        strengths.append(
            "Risks and uncertainty are adequately represented."
        )
    else:
        weaknesses.append(
            "Important risks or uncertainties remain."
        )

    if state.unknowns:
        critical_gaps.append(
            "Material unknowns remain unresolved."
        )

    if contradiction_robustness >= 0.75:
        strengths.append(
            "Recommendation is robust against known contradictions."
        )
    else:
        critical_gaps.append(
            "Unresolved contradictory evidence materially weakens the recommendation."
        )

    if confidence_calibration >= 0.75:
        strengths.append(
            "Recommendation confidence is reasonably calibrated."
        )
    else:
        weaknesses.append(
            "Recommendation confidence is poorly calibrated to underlying support."
        )

    decision_ready = (
        not critical_gaps
        and overall_score >= 0.70
    )

    if decision_ready:
        recommendation = (
            "Decision ready: the recommendation has sufficient "
            "deterministic support and no critical quality gaps."
        )
    else:
        recommendation = (
            "Needs more work: resolve critical gaps and improve "
            "decision quality before treating the recommendation "
            "as decision-ready."
        )

    return DecisionQualityEvaluation(
        overall_score=overall_score,
        evidence_support=evidence_support,
        analytical_support=analytical_support,
        alternative_quality=alternative_quality,
        risk_uncertainty=risk_uncertainty,
        contradiction_robustness=contradiction_robustness,
        confidence_calibration=confidence_calibration,
        strengths=strengths,
        weaknesses=weaknesses,
        critical_gaps=critical_gaps,
        decision_ready=decision_ready,
        recommendation=recommendation,
    )
