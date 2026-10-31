from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .reasoning_action import ReasoningAction


class RuleOperator(str, Enum):
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT_EXISTS"
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT_CONTAINS"
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    IN = "IN"
    NOT_IN = "NOT_IN"


class RuleCondition(BaseModel):
    """
    Declarative condition used by the reasoning rule engine.

    The condition describes WHAT should be evaluated.
    It does not contain executable Python logic.
    """

    model_config = ConfigDict(extra="forbid")

    field: str = Field(
        min_length=1
    )

    operator: RuleOperator

    value: Optional[Any] = None

    description: str = Field(
        min_length=1
    )


class ReasoningRule(BaseModel):
    """
    Declarative reasoning rule.

    A rule connects a set of state conditions to a
    proposed ReasoningAction.

    The rule itself contains no execution logic.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        min_length=1
    )

    name: str = Field(
        min_length=1
    )

    description: str = Field(
        min_length=1
    )

    conditions: List[RuleCondition] = Field(
        default_factory=list
    )

    action: ReasoningAction

    priority: int = Field(
        default=1,
        ge=1
    )

    enabled: bool = True

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )
