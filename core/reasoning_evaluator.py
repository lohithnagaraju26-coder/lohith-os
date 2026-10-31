from __future__ import annotations

from dataclasses import dataclass
from typing import List

from core.decision_state import DecisionState


@dataclass(frozen=True)
class ReasoningEvaluation:
    """
    Deterministic evaluation of progress made during one
    reasoning step.

    This is an evaluation artifact, not a mutation of DecisionState.
    """

    state_version_before: int
    state_version_after: int

    evidence_added: int
    hypotheses_added: int
    findings_added: int
    contradictions_added: int
    contradictions_resolved: int
    decisions_added: int
    risks_added: int

    unknowns_before: int
    unknowns_after: int
    unknowns_resolved: int

    recommendation_present: bool
    outcome_present: bool

    useful_progress: bool
    decision_readiness: float

    continue_reasoning: bool
    stop_reason: str
    confidence: float


def _resolved_unknowns(
    before: DecisionState,
    after: DecisionState,
) -> int:
    """
    Count unknowns that were present before but are no longer
    unresolved after the reasoning step.
    """

    before_unknowns = {
        str(item).strip()
        for item in before.unknowns
        if str(item).strip()
    }

    after_unknowns = {
        str(item).strip()
        for item in after.unknowns
        if str(item).strip()
    }

    return len(
        before_unknowns - after_unknowns
    )


def _resolved_contradictions(
    before: DecisionState,
    after: DecisionState,
) -> int:
    """
    Count contradictions that became resolved during the step.
    """

    before_by_id = {
        item.id: item
        for item in before.contradictions
    }

    resolved = 0

    for contradiction in after.contradictions:
        previous = before_by_id.get(
            contradiction.id
        )

        if (
            previous is not None
            and not previous.resolved
            and contradiction.resolved
        ):
            resolved += 1

    return resolved


def evaluate_reasoning_step(
    before: DecisionState,
    after: DecisionState,
) -> ReasoningEvaluation:
    """
    Compare two DecisionState snapshots and evaluate whether
    meaningful analytical progress occurred.

    The evaluator is intentionally deterministic and does not
    depend on an LLM.
    """

    evidence_added = max(
        0,
        len(after.evidence) - len(before.evidence),
    )

    hypotheses_added = max(
        0,
        len(after.hypotheses) - len(before.hypotheses),
    )

    findings_added = max(
        0,
        len(after.findings) - len(before.findings),
    )

    contradictions_added = max(
        0,
        len(after.contradictions)
        - len(before.contradictions),
    )

    decisions_added = max(
        0,
        len(after.decisions) - len(before.decisions),
    )

    risks_added = max(
        0,
        len(after.risks) - len(before.risks),
    )

    unknowns_before = len(before.unknowns)
    unknowns_after = len(after.unknowns)

    unknowns_resolved = _resolved_unknowns(
        before,
        after,
    )

    contradictions_resolved = (
        _resolved_contradictions(
            before,
            after,
        )
    )

    recommendation_present = (
        after.recommendation is not None
    )

    outcome_present = (
        after.outcome is not None
    )

    useful_progress = any(
        [
            evidence_added > 0,
            hypotheses_added > 0,
            findings_added > 0,
            unknowns_resolved > 0,
            contradictions_resolved > 0,
            decisions_added > 0,
            risks_added > 0,
            recommendation_present
            and before.recommendation is None,
            outcome_present
            and before.outcome is None,
        ]
    )

    readiness_components: List[float] = []

    if after.findings:
        readiness_components.append(0.25)

    if after.evidence:
        readiness_components.append(0.20)

    if after.hypotheses:
        readiness_components.append(0.15)

    if after.decisions:
        readiness_components.append(0.15)

    if after.recommendation:
        readiness_components.append(0.15)

    if not after.unknowns:
        readiness_components.append(0.10)

    decision_readiness = min(
        1.0,
        sum(readiness_components),
    )

    # A recommendation supported by analytical work, with no
    # unresolved unknowns or contradictions, is explicitly
    # decision-ready. The readiness score must reflect the
    # same stopping boundary used below.
    if (
        after.recommendation is not None
        and after.findings
        and after.evidence
        and not after.unknowns
        and not after.contradictions
    ):
        decision_readiness = max(
            decision_readiness,
            0.75,
        )

    if outcome_present:
        continue_reasoning = False
        stop_reason = (
            "An outcome has been recorded; "
            "the reasoning chain can stop."
        )

    elif (
        after.recommendation is not None
        and not after.unknowns
        and not after.contradictions
    ):
        continue_reasoning = False
        stop_reason = (
            "A recommendation exists with no "
            "unresolved unknowns or contradictions."
        )

    else:
        continue_reasoning = True
        stop_reason = (
            "Additional reasoning is still justified."
        )

    confidence = min(
        1.0,
        0.5
        + (
            0.1
            if useful_progress
            else 0.0
        )
        + (
            0.2
            if decision_readiness >= 0.75
            else 0.0
        ),
    )

    return ReasoningEvaluation(
        state_version_before=before.version,
        state_version_after=after.version,
        evidence_added=evidence_added,
        hypotheses_added=hypotheses_added,
        findings_added=findings_added,
        contradictions_added=contradictions_added,
        contradictions_resolved=contradictions_resolved,
        decisions_added=decisions_added,
        risks_added=risks_added,
        unknowns_before=unknowns_before,
        unknowns_after=unknowns_after,
        unknowns_resolved=unknowns_resolved,
        recommendation_present=recommendation_present,
        outcome_present=outcome_present,
        useful_progress=useful_progress,
        decision_readiness=decision_readiness,
        continue_reasoning=continue_reasoning,
        stop_reason=stop_reason,
        confidence=confidence,
    )
