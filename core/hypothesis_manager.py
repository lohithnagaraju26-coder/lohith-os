from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from core.entities import Evidence, Hypothesis, HypothesisStatus


@dataclass(frozen=True)
class HypothesisEvaluation:
    hypothesis_id: str
    previous_status: HypothesisStatus
    status: HypothesisStatus
    confidence: float
    supporting_score: float
    contradicting_score: float
    supporting_evidence: List[str]
    contradicting_evidence: List[str]


def evaluate_hypothesis(
    hypothesis: Hypothesis,
    evidence: List[Evidence],
) -> HypothesisEvaluation:
    evidence_by_id: Dict[str, Evidence] = {
        item.id: item
        for item in evidence
    }

    supporting_ids = [
        item.id
        for item in evidence
        if hypothesis.id in item.supports
    ]

    contradicting_ids = [
        item.id
        for item in evidence
        if hypothesis.id in item.contradicts
    ]

    supporting_score = min(
        1.0,
        sum(
            evidence_by_id[item_id].strength
            for item_id in supporting_ids
            if item_id in evidence_by_id
        ),
    )

    contradicting_score = min(
        1.0,
        sum(
            evidence_by_id[item_id].strength
            for item_id in contradicting_ids
            if item_id in evidence_by_id
        ),
    )

    if not supporting_ids and not contradicting_ids:
        status = HypothesisStatus.OPEN
        confidence = 0.5

    elif contradicting_score >= 0.8 and (
        contradicting_score > supporting_score
    ):
        status = HypothesisStatus.REJECTED
        confidence = 1.0 - contradicting_score

    elif contradicting_score > supporting_score:
        status = HypothesisStatus.WEAKENED
        confidence = max(
            0.0,
            0.5 + (
                supporting_score - contradicting_score
            ) / 2,
        )

    elif supporting_score >= 0.8 and (
        supporting_score > contradicting_score
    ):
        status = HypothesisStatus.SUPPORTED
        confidence = supporting_score

    else:
        status = HypothesisStatus.OPEN
        confidence = 0.5 + (
            supporting_score - contradicting_score
        ) / 2

    return HypothesisEvaluation(
        hypothesis_id=hypothesis.id,
        previous_status=hypothesis.status,
        status=status,
        confidence=max(
            0.0,
            min(1.0, confidence),
        ),
        supporting_score=supporting_score,
        contradicting_score=contradicting_score,
        supporting_evidence=supporting_ids,
        contradicting_evidence=contradicting_ids,
    )


def update_hypothesis(
    hypothesis: Hypothesis,
    evidence: List[Evidence],
) -> HypothesisEvaluation:
    evaluation = evaluate_hypothesis(
        hypothesis,
        evidence,
    )

    hypothesis.status = evaluation.status
    hypothesis.confidence = evaluation.confidence
    hypothesis.supporting_evidence = (
        evaluation.supporting_evidence
    )
    hypothesis.contradicting_evidence = (
        evaluation.contradicting_evidence
    )

    return evaluation


def evaluate_hypotheses(
    hypotheses: List[Hypothesis],
    evidence: List[Evidence],
) -> List[HypothesisEvaluation]:
    return [
        evaluate_hypothesis(
            hypothesis,
            evidence,
        )
        for hypothesis in hypotheses
    ]


def update_hypotheses(
    hypotheses: List[Hypothesis],
    evidence: List[Evidence],
) -> List[HypothesisEvaluation]:
    return [
        update_hypothesis(
            hypothesis,
            evidence,
        )
        for hypothesis in hypotheses
    ]
