from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ReasoningActionType(str, Enum):
    FRAMEWORK = "FRAMEWORK"
    RESEARCH = "RESEARCH"
    TOOL = "TOOL"
    SPECIALIST = "SPECIALIST"
    ASK_USER = "ASK_USER"
    STOP = "STOP"


class ReasoningAction(BaseModel):
    """
    Canonical action proposed by the reasoning engine.

    This is the boundary between:
        DecisionState
            ↓
        Reasoning Engine
            ↓
        Execution capability
    """

    model_config = ConfigDict(extra="forbid")

    type: ReasoningActionType

    description: str = Field(
        min_length=1
    )

    rationale: str = Field(
        min_length=1
    )

    unresolved_question: Optional[str] = None

    target: Optional[str] = None

    expected_output: Optional[str] = None

    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )

    priority: int = Field(
        default=1,
        ge=1,
    )

    evidence_required: List[str] = Field(
        default_factory=list
    )

    dependencies: List[str] = Field(
        default_factory=list
    )

    fallback_action: Optional[str] = None

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )
