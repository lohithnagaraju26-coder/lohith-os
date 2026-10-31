from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict

from .decision_state import DecisionState
from .reasoning_rule import (
    ReasoningRule,
    RuleCondition,
    RuleOperator,
)


@dataclass(frozen=True)
class ConditionResult:
    """
    Result of evaluating one rule condition.
    """

    field: str
    operator: RuleOperator
    expected: Any
    actual: Any
    matched: bool


class RuleEvaluation(BaseModel):
    """
    Complete evaluation result for one reasoning rule.
    """

    model_config = ConfigDict(extra="forbid")

    rule_id: str
    rule_name: str
    matched: bool
    priority: int
    condition_results: List[ConditionResult]
    action: Optional[Any] = None
    reason: str = ""


def _get_field_value(
    state: DecisionState,
    field: str,
) -> Any:
    """
    Safely retrieve a field from DecisionState.

    Supports simple fields and dotted paths.
    Example:
        unknowns
        recommendation.confidence

    No arbitrary code execution is permitted.
    """

    current: Any = state

    for part in field.split("."):
        part = part.strip()

        if not part:
            raise ValueError(
                f"Invalid empty field segment in '{field}'."
            )

        if isinstance(current, BaseModel):
            if part not in type(current).model_fields:
                raise ValueError(
                    f"Unknown DecisionState field: '{field}'."
                )

            current = getattr(current, part)
            continue

        if isinstance(current, dict):
            if part not in current:
                return None

            current = current[part]
            continue

        raise ValueError(
            f"Cannot traverse field '{field}' "
            f"through value of type "
            f"'{type(current).__name__}'."
        )

    return current


def _is_empty(value: Any) -> bool:
    if value is None:
        return True

    if isinstance(value, str):
        return not value.strip()

    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0

    return False


def _contains(
    actual: Any,
    expected: Any,
) -> bool:
    if isinstance(actual, str):
        return str(expected).lower() in actual.lower()

    if isinstance(actual, (list, tuple, set)):
        return expected in actual

    if isinstance(actual, dict):
        return expected in actual or expected in actual.values()

    return False


def _compare(
    actual: Any,
    operator: RuleOperator,
    expected: Any,
) -> bool:

    if operator == RuleOperator.EXISTS:
        return not _is_empty(actual)

    if operator == RuleOperator.NOT_EXISTS:
        return _is_empty(actual)

    if operator == RuleOperator.EQUALS:
        return actual == expected

    if operator == RuleOperator.NOT_EQUALS:
        return actual != expected

    if operator == RuleOperator.CONTAINS:
        return _contains(actual, expected)

    if operator == RuleOperator.NOT_CONTAINS:
        return not _contains(actual, expected)

    if operator == RuleOperator.GREATER_THAN:
        return actual > expected

    if operator == RuleOperator.GREATER_THAN_OR_EQUAL:
        return actual >= expected

    if operator == RuleOperator.LESS_THAN:
        return actual < expected

    if operator == RuleOperator.LESS_THAN_OR_EQUAL:
        return actual <= expected

    if operator == RuleOperator.IN:
        if _is_empty(expected):
            return False

        return actual in expected

    if operator == RuleOperator.NOT_IN:
        if _is_empty(expected):
            return True

        return actual not in expected

    raise ValueError(
        f"Unsupported rule operator: {operator}"
    )


def evaluate_condition(
    state: DecisionState,
    condition: RuleCondition,
) -> ConditionResult:
    """
    Evaluate one declarative condition against DecisionState.
    """

    actual = _get_field_value(
        state,
        condition.field,
    )

    matched = _compare(
        actual,
        condition.operator,
        condition.value,
    )

    return ConditionResult(
        field=condition.field,
        operator=condition.operator,
        expected=condition.value,
        actual=actual,
        matched=matched,
    )


def evaluate_rule(
    state: DecisionState,
    rule: ReasoningRule,
) -> RuleEvaluation:
    """
    Evaluate all conditions in a reasoning rule.

    Rule semantics are AND:
    every condition must match.
    """

    if not rule.enabled:
        return RuleEvaluation(
            rule_id=rule.id,
            rule_name=rule.name,
            matched=False,
            priority=rule.priority,
            condition_results=[],
            action=None,
            reason="Rule is disabled.",
        )

    results = [
        evaluate_condition(
            state,
            condition,
        )
        for condition in rule.conditions
    ]

    matched = all(
        result.matched
        for result in results
    )

    if matched:
        reason = (
            f"All {len(results)} rule conditions matched."
        )
        action = rule.action
    else:
        failed = [
            result.field
            for result in results
            if not result.matched
        ]

        reason = (
            "Rule conditions failed: "
            + ", ".join(failed)
        )
        action = None

    return RuleEvaluation(
        rule_id=rule.id,
        rule_name=rule.name,
        matched=matched,
        priority=rule.priority,
        condition_results=results,
        action=action,
        reason=reason,
    )


def evaluate_rules(
    state: DecisionState,
    rules: List[ReasoningRule],
) -> List[RuleEvaluation]:
    """
    Evaluate a collection of rules.

    Results are sorted by:
        1. matched rules first
        2. highest priority first
    """

    evaluations = [
        evaluate_rule(
            state,
            rule,
        )
        for rule in rules
    ]

    return sorted(
        evaluations,
        key=lambda result: (
            not result.matched,
            -result.priority,
        ),
    )


def select_best_rule(
    state: DecisionState,
    rules: List[ReasoningRule],
) -> Optional[RuleEvaluation]:
    """
    Return the highest-priority matching rule.

    Returns None when no rule matches.
    """

    evaluations = evaluate_rules(
        state,
        rules,
    )

    for evaluation in evaluations:
        if evaluation.matched:
            return evaluation

    return None
