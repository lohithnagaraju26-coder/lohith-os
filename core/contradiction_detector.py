from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .entities import Contradiction, Evidence, Hypothesis


@dataclass(frozen=True)
class ContradictionDetection:
    hypothesis_id: str
    evidence_ids: list[str]
    severity: float
    description: str


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _stable_contradiction_id(hypothesis_id: str, evidence_ids: Iterable[str]) -> str:
    ordered_ids = sorted(set(evidence_ids))
    return "contradiction:" + hypothesis_id + ":" + ":".join(ordered_ids)


def detect_contradictions(
    hypotheses: list[Hypothesis],
    evidence: list[Evidence],
) -> list[Contradiction]:
    """
    Detect explicit evidence conflicts around the same hypothesis.

    A contradiction exists when a hypothesis has at least one supporting
    evidence item and at least one contradicting evidence item.

    V1 intentionally relies only on explicit structured relationships.
    It does not infer semantic contradictions from claim text.
    """
    evidence_by_id = {item.id: item for item in evidence}
    detections: list[Contradiction] = []

    for hypothesis in hypotheses:
        supporting = [
            item
            for item in evidence
            if hypothesis.id in item.supports
        ]

        contradicting = [
            item
            for item in evidence
            if hypothesis.id in item.contradicts
        ]

        if not supporting or not contradicting:
            continue

        supporting_ids = [item.id for item in supporting]
        contradicting_ids = [item.id for item in contradicting]
        evidence_ids = sorted(set(supporting_ids + contradicting_ids))

        supporting_strength = max(
            item.strength for item in supporting
        )
        contradicting_strength = max(
            item.strength for item in contradicting
        )

        severity = _clamp(
            (supporting_strength + contradicting_strength) / 2
        )

        description = (
            f"Hypothesis '{hypothesis.id}' has conflicting evidence: "
            f"supporting evidence {supporting_ids} and contradicting "
            f"evidence {contradicting_ids}."
        )

        contradiction_id = _stable_contradiction_id(
            hypothesis.id,
            evidence_ids,
        )

        # Ensure all referenced evidence IDs actually exist.
        if not all(item_id in evidence_by_id for item_id in evidence_ids):
            continue

        detections.append(
            Contradiction(
                id=contradiction_id,
                description=description,
                evidence_ids=evidence_ids,
                hypothesis_ids=[hypothesis.id],
                severity=severity,
                resolved=False,
            )
        )

    return detections


def merge_contradictions(
    existing: list[Contradiction],
    detected: list[Contradiction],
) -> list[Contradiction]:
    """
    Merge newly detected contradictions without duplicating existing ones.

    Existing contradictions are preserved exactly, including their resolved
    state and resolution.
    """
    merged = list(existing)
    existing_ids = {item.id for item in existing}

    for contradiction in detected:
        if contradiction.id in existing_ids:
            continue

        merged.append(contradiction)
        existing_ids.add(contradiction.id)

    return merged
