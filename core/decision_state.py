from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .entities import (
    Contradiction,
    Decision,
    DecisionOption,
    Evidence,
    Finding,
    Hypothesis,
    NextAction,
    NextActionType,
    Outcome,
    Recommendation,
    Risk,
    StateTransition,
    utc_now,
)


class DecisionState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    version: int = 0

    # Objective
    objective: str
    desired_outcome: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)

    # Knowledge
    known_facts: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)

    # Hypotheses
    hypotheses: List[Hypothesis] = Field(default_factory=list)

    # Analysis
    findings: List[Finding] = Field(default_factory=list)
    contradictions: List[Contradiction] = Field(default_factory=list)

    # Decision
    options: List[DecisionOption] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    recommendation: Optional[Recommendation] = None
    risks: List[Risk] = Field(default_factory=list)

    # Action
    next_action: Optional[NextAction] = None
    stopping_status: str = "CONTINUE"
    stopping_reason: Optional[str] = None

    # Outcome
    outcome: Optional[Outcome] = None

    # History
    history: List[StateTransition] = Field(default_factory=list)

    @field_validator("objective")
    @classmethod
    def validate_objective(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("objective cannot be empty")
        return value

    def touch(self) -> None:
        self.version += 1
        self.updated_at = utc_now()

    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence.append(evidence)
        self.touch()

    def add_evidence_and_update_hypotheses(self, evidence: Evidence):
        from .hypothesis_manager import update_hypotheses

        self.evidence.append(evidence)

        evaluations = update_hypotheses(
            self.hypotheses,
            self.evidence,
        )

        self.touch()

        return evaluations

    def add_evidence_and_update_reasoning_state(self, evidence: Evidence):
        from .contradiction_detector import (
            detect_contradictions,
            merge_contradictions,
        )
        from .hypothesis_manager import update_hypotheses

        self.evidence.append(evidence)

        hypothesis_evaluations = update_hypotheses(
            self.hypotheses,
            self.evidence,
        )

        detected_contradictions = detect_contradictions(
            self.hypotheses,
            self.evidence,
        )

        self.contradictions = merge_contradictions(
            self.contradictions,
            detected_contradictions,
        )

        self.touch()

        return {
            "hypothesis_evaluations": hypothesis_evaluations,
            "detected_contradictions": detected_contradictions,
        }

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        self.hypotheses.append(hypothesis)
        self.touch()

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)
        self.touch()

    def add_contradiction(self, contradiction: Contradiction) -> None:
        self.contradictions.append(contradiction)
        self.touch()

    def add_option(self, option: DecisionOption) -> None:
        self.options.append(option)
        self.touch()

    def add_decision(self, decision: Decision) -> None:
        self.decisions.append(decision)
        self.touch()

    def add_risk(self, risk: Risk) -> None:
        self.risks.append(risk)
        self.touch()

    def set_recommendation(self, recommendation: Recommendation) -> None:
        self.recommendation = recommendation
        self.touch()

    def set_next_action(self, action: NextAction) -> None:
        self.next_action = action

        if action.type == NextActionType.STOP:
            self.stopping_status = "STOP"
            self.stopping_reason = action.description
        else:
            self.stopping_status = "CONTINUE"
            self.stopping_reason = None

        self.touch()

    def stop(self, reason: str) -> None:
        from .state_transition import transition_state

        transition_state(
            self,
            trigger="REASONING_LIFECYCLE",
            action="STOP_REASONING",
            updates={
                "stopping_status": "STOP",
                "stopping_reason": reason,
            },
            reasoning=reason,
        )

    def continue_reasoning(
        self,
        reason: Optional[str] = None,
    ) -> None:
        from .state_transition import transition_state

        transition_state(
            self,
            trigger="REASONING_LIFECYCLE",
            action="CONTINUE_REASONING",
            updates={
                "stopping_status": "CONTINUE",
                "stopping_reason": reason,
            },
            reasoning=reason or "Reasoning should continue.",
        )