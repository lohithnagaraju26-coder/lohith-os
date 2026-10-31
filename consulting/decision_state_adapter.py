from __future__ import annotations

from typing import Any, Dict

from core import (
    Decision,
    DecisionState,
    Finding,
    Risk,
    transition_state,
)


def state_to_framework_packet(
    state: DecisionState,
    framework: str = "",
) -> Dict[str, Any]:
    """
    Convert the current DecisionState into the context expected
    by the existing framework execution layer.

    DecisionState remains the source of truth.
    The returned dictionary is only an execution adapter.
    """

    evidence = {
        item.id: {
            "type": item.type.value,
            "claim": item.claim,
            "source": item.source,
            "strength": item.strength,
            "supports": list(item.supports),
            "contradicts": list(item.contradicts),
        }
        for item in state.evidence
    }

    hypotheses = [
        {
            "id": item.id,
            "statement": item.statement,
            "status": item.status.value,
            "confidence": item.confidence,
        }
        for item in state.hypotheses
    ]

    findings = [
        {
            "id": item.id,
            "statement": item.statement,
            "confidence": item.confidence,
            "evidence_ids": list(item.evidence_ids),
        }
        for item in state.findings
    ]

    contradictions = [
        {
            "id": item.id,
            "description": item.description,
            "severity": item.severity,
            "resolved": item.resolved,
            "evidence_ids": list(item.evidence_ids),
            "hypothesis_ids": list(item.hypothesis_ids),
        }
        for item in state.contradictions
    ]

    decisions = [
        {
            "id": item.id,
            "statement": item.statement,
            "rationale": item.rationale,
            "confidence": item.confidence,
            "evidence_ids": list(item.evidence_ids),
        }
        for item in state.decisions
    ]

    risks = [
        {
            "id": item.id,
            "description": item.description,
            "probability": item.probability,
            "impact": item.impact,
            "mitigation": item.mitigation,
            "evidence_ids": list(item.evidence_ids),
        }
        for item in state.risks
    ]

    return {
        "decision_state_id": state.id,
        "decision_state_version": state.version,
        "business_problem": state.objective,
        "objective": state.objective,
        "desired_outcome": state.desired_outcome,
        "context": dict(state.context),
        "known_facts": list(state.known_facts),
        "unknowns": list(state.unknowns),
        "assumptions": list(state.assumptions),
        "available_evidence": evidence,
        "hypotheses": hypotheses,
        "findings": findings,
        "contradictions": contradictions,
        "decisions": decisions,
        "risks": risks,
        "recommendation": (
            state.recommendation.model_dump()
            if state.recommendation
            else None
        ),
        "next_action": (
            state.next_action.model_dump()
            if state.next_action
            else None
        ),
        "stopping_status": state.stopping_status,
        "stopping_reason": state.stopping_reason,
        "framework": framework,
        "prior_results": [
            {
                "framework": transition.metadata.get(
                    "framework",
                    "",
                ),
                "action": transition.action,
                "reasoning": transition.reasoning,
                "after_version": transition.after_version,
            }
            for transition in state.history
            if transition.action == "EXECUTE_FRAMEWORK"
        ],
    }


def apply_framework_result_to_state(
    state: DecisionState,
    result: Dict[str, Any],
) -> DecisionState:
    """
    Apply a completed framework result to DecisionState.

    This adapter intentionally preserves the existing framework
    result format while converting its outputs into typed state.
    """

    framework = str(
        result.get("framework", "")
    ).strip()

    findings = result.get("findings", [])
    decisions = result.get("decisions", [])
    risks = result.get("risks", [])
    assumptions = result.get("assumptions", [])

    for index, finding in enumerate(findings):
        statement = str(finding).strip()

        if not statement:
            continue

        state.add_finding(
            Finding(
                id=f"{framework}-F{index + 1}",
                statement=statement,
                evidence_ids=[],
                confidence=(
                    float(result["confidence"])
                    if result.get("confidence") is not None
                    else 0.5
                ),
                implications=[],
            )
        )

    for index, decision in enumerate(decisions):
        statement = str(decision).strip()

        if not statement:
            continue

        state.add_decision(
            Decision(
                id=f"{framework}-D{index + 1}",
                statement=statement,
                rationale=f"Generated during {framework}.",
                evidence_ids=[],
                confidence=(
                    float(result["confidence"])
                    if result.get("confidence") is not None
                    else 0.5
                ),
            )
        )

    for index, risk in enumerate(risks):
        description = str(risk).strip()

        if not description:
            continue

        state.add_risk(
            Risk(
                id=f"{framework}-R{index + 1}",
                description=description,
                probability=0.5,
                impact=0.5,
                mitigation=None,
                evidence_ids=[],
            )
        )

    for assumption in assumptions:
        assumption_text = str(assumption).strip()

        if (
            assumption_text
            and assumption_text not in state.assumptions
        ):
            state.assumptions.append(
                assumption_text
            )
            state.touch()

    transition_state(
        state,
        trigger="framework_execution",
        action="EXECUTE_FRAMEWORK",
        updates={},
        reasoning=(
            f"Executed {framework} with "
            f"confidence {result.get('confidence', 0.5)}."
        ),
        metadata={
            "framework": framework,
            "status": result.get("status", ""),
            "confidence": result.get("confidence", 0.5),
        },
    )

    return state