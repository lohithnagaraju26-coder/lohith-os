from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EvidenceType(str, Enum):
    FACT = "FACT"
    DATA = "DATA"
    RESEARCH = "RESEARCH"
    USER_INPUT = "USER_INPUT"
    ASSUMPTION = "ASSUMPTION"
    OBSERVATION = "OBSERVATION"


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: EvidenceType
    claim: str
    source: Optional[str] = None
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
    supports: List[str] = Field(default_factory=list)
    contradicts: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class HypothesisStatus(str, Enum):
    OPEN = "OPEN"
    SUPPORTED = "SUPPORTED"
    WEAKENED = "WEAKENED"
    REJECTED = "REJECTED"


class Hypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    statement: str
    rationale: Optional[str] = None
    status: HypothesisStatus = HypothesisStatus.OPEN
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    statement: str
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    implications: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class Contradiction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    description: str
    evidence_ids: List[str] = Field(default_factory=list)
    hypothesis_ids: List[str] = Field(default_factory=list)
    severity: float = Field(default=0.5, ge=0.0, le=1.0)
    resolved: bool = False
    resolution: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)


class DecisionOption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    description: str
    benefits: List[str] = Field(default_factory=list)
    drawbacks: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    feasibility: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    expected_impact: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    statement: str
    rationale: str
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=utc_now)


class Recommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    statement: str
    rationale: str
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    tradeoffs: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class NextActionType(str, Enum):
    RESEARCH = "RESEARCH"
    ANALYZE = "ANALYZE"
    TEST = "TEST"
    DECIDE = "DECIDE"
    EXECUTE = "EXECUTE"
    REVIEW = "REVIEW"
    WAIT = "WAIT"
    STOP = "STOP"


class NextAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: NextActionType
    description: str
    rationale: str
    priority: int = Field(default=1, ge=1)
    target: Optional[str] = None
    expected_output: Optional[str] = None


class Risk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    description: str
    probability: float = Field(default=0.5, ge=0.0, le=1.0)
    impact: float = Field(default=0.5, ge=0.0, le=1.0)
    mitigation: Optional[str] = None
    evidence_ids: List[str] = Field(default_factory=list)


class Outcome(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected: Optional[str] = None
    actual: Optional[str] = None
    success: Optional[bool] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    lessons: List[str] = Field(default_factory=list)
    recorded_at: Optional[datetime] = None


class StateTransition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    timestamp: datetime = Field(default_factory=utc_now)
    trigger: str
    action: str
    before_version: int
    after_version: int
    changed_fields: List[str] = Field(default_factory=list)
    reasoning: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
