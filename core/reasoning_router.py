from __future__ import annotations

import re
from typing import List

from consulting.framework_registry import (
    get_executable_frameworks,
    get_framework_knowledge,
)
from core.decision_state import DecisionState
from core.reasoning_action import ReasoningAction, ReasoningActionType
from core.reasoning_rule_engine import select_best_rule
from core.reasoning_rules import get_reasoning_rules


def _text(value: object) -> str:
    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(str(item) for item in value)

    if isinstance(value, dict):
        return " ".join(
            f"{key} {value}"
            for key, value in value.items()
        )

    return str(value)


def _normalize_text(value: object) -> str:
    text = _text(value).lower()
    return re.sub(r"[^a-z0-9\s]", " ", text)


def _tokens(value: object) -> set[str]:
    return {
        token
        for token in _normalize_text(value).split()
        if len(token) > 3
    }


def _state_text(state: DecisionState) -> str:
    parts = [
        state.objective,
        state.desired_outcome,
        state.context,
        state.known_facts,
        state.unknowns,
        state.assumptions,
        state.findings,
        state.contradictions,
        state.options,
        state.decisions,
        state.risks,
    ]

    if state.recommendation:
        parts.append(state.recommendation.statement)
        parts.append(state.recommendation.rationale)

    return " ".join(
        _normalize_text(part)
        for part in parts
        if part
    )


def _phrase_fit(
    state_text: str,
    phrase: str,
) -> float:
    phrase_tokens = _tokens(phrase)

    if not phrase_tokens:
        return 0.0

    state_tokens = set(state_text.split())

    overlap = len(
        phrase_tokens & state_tokens
    )

    return overlap / len(phrase_tokens)


def _list_fit(
    state_text: str,
    values: List[str],
) -> float:
    if not values:
        return 0.0

    scores = [
        _phrase_fit(state_text, value)
        for value in values
    ]

    return max(scores, default=0.0)


def _exclusion_penalty(
    state_text: str,
    exclusions: List[str],
) -> float:
    if not exclusions:
        return 0.0

    matched = sum(
        1
        for exclusion in exclusions
        if _phrase_fit(
            state_text,
            exclusion,
        ) >= 0.5
    )

    return matched * 8.0


def _relationship_fit(
    state: DecisionState,
    framework_name: str,
) -> float:
    knowledge = get_framework_knowledge(
        framework_name
    )

    if knowledge is None:
        return 0.0

    state_text = _state_text(state)

    score = 0.0

    # Selection role contributes when the role itself
    # semantically matches the current DecisionState.
    score += (
        _phrase_fit(
            state_text,
            knowledge.selection_role,
        )
        * 4.0
    )

    # Compatible frameworks provide a positive signal
    # when the current state already contains related concepts.
    score += (
        _list_fit(
            state_text,
            knowledge.compatible_frameworks,
        )
        * 2.0
    )

    # Downstream frameworks are useful when the current
    # state already contains evidence suggesting that this
    # framework is a natural continuation.
    score += (
        _list_fit(
            state_text,
            knowledge.downstream_frameworks,
        )
        * 1.5
    )

    return score


def _prerequisite_penalty(
    state: DecisionState,
    framework_name: str,
) -> float:
    knowledge = get_framework_knowledge(
        framework_name
    )

    if knowledge is None:
        return 0.0

    if not knowledge.prerequisite_frameworks:
        return 0.0

    state_text = _state_text(state)

    missing = 0

    for prerequisite in knowledge.prerequisite_frameworks:
        if _phrase_fit(
            state_text,
            prerequisite,
        ) < 0.5:
            missing += 1

    return missing * 6.0


def _score_framework(
    state: DecisionState,
    framework_name: str,
) -> float:
    knowledge = get_framework_knowledge(
        framework_name
    )

    if knowledge is None:
        return 0.0

    state_text = _state_text(state)
    score = 0.0

    # 1. Direct framework-name signal.
    if _phrase_fit(
        state_text,
        knowledge.name,
    ) >= 0.5:
        score += 10.0

    # 2. Primary-question fit.
    score += (
        _phrase_fit(
            state_text,
            knowledge.primary_question,
        )
        * 12.0
    )

    # 3. Core-question fit.
    score += (
        _phrase_fit(
            state_text,
            knowledge.core_question,
        )
        * 10.0
    )

    # 4. Trigger-condition fit.
    if knowledge.trigger_conditions:
        trigger_fit = _list_fit(
            state_text,
            knowledge.trigger_conditions,
        )

        score += trigger_fit * 10.0

    # 5. "Use when" fit.
    if knowledge.use_when:
        score += (
            _list_fit(
                state_text,
                knowledge.use_when,
            )
            * 6.0
        )

    # 6. Problem-type fit.
    score += (
        _list_fit(
            state_text,
            knowledge.problem_types,
        )
        * 4.0
    )

    # 7. Decision-type fit.
    score += (
        _list_fit(
            state_text,
            knowledge.decision_types,
        )
        * 4.0
    )

    # 8. Selection-role and relationship fit.
    score += _relationship_fit(
        state,
        framework_name,
    )

    # 9. Selection-hierarchy fit.
    score += (
        _phrase_fit(
            state_text,
            knowledge.framework_selection_hierarchy,
        )
        * 4.0
    )

    # 10. Purpose fit.
    score += (
        _phrase_fit(
            state_text,
            knowledge.purpose,
        )
        * 5.0
    )

    # 11. Evidence maturity.
    if state.known_facts:
        score += 1.0

    if state.evidence:
        score += 1.0

    if state.unknowns:
        score += 1.0

    # 12. Contradictory evidence reduces confidence
    # in ordinary framework analysis.
    if state.contradictions:
        score -= 2.0

    # 13. Exclusion conditions are strong negative signals.
    score -= _exclusion_penalty(
        state_text,
        knowledge.exclusion_conditions,
    )

    # 14. Framework prerequisites must be represented
    # before the framework becomes the preferred route.
    score -= _prerequisite_penalty(
        state,
        framework_name,
    )

    return score


def _executed_frameworks(
    state: DecisionState,
) -> set[str]:
    """
    Return the frameworks already executed for this DecisionState.

    Execution history is stored canonically in StateTransition
    metadata rather than in a separate router-maintained list.
    """

    return {
        str(
            transition.metadata.get(
                "framework",
                "",
            )
        ).strip()
        for transition in state.history
        if (
            transition.action == "EXECUTE_FRAMEWORK"
            and transition.metadata.get("framework")
        )
    }


def select_best_framework(
    state: DecisionState,
) -> str | None:
    """
    Select the strongest executable framework that has not
    already been executed for the current DecisionState.

    Framework selection remains metadata-driven and deterministic.
    """

    executed_frameworks = _executed_frameworks(
        state
    )

    candidates: List[tuple[str, float]] = []
    fallback_candidates: List[tuple[str, float]] = []

    for framework_name in get_executable_frameworks():

        # Never intentionally select a framework that has
        # already been executed in this reasoning chain.
        if framework_name in executed_frameworks:
            continue

        score = _score_framework(
            state,
            framework_name,
        )

        knowledge = get_framework_knowledge(
            framework_name
        )

        if score > 0:
            candidates.append(
                (framework_name, score)
            )

        elif (
            knowledge is not None
            and knowledge.selection_role
            == "PROBLEM_STRUCTURING"
        ):
            fallback_candidates.append(
                (framework_name, score)
            )

    if candidates:
        candidates.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return candidates[0][0]

    if fallback_candidates:
        fallback_candidates.sort(
            key=lambda item: (
                -item[1],
                item[0],
            )
        )

        return fallback_candidates[0][0]

    return None


def route_reasoning(
    state: DecisionState,
) -> ReasoningAction:
    rule_result = select_best_rule(
        state,
        get_reasoning_rules(),
    )

    if rule_result is None:
        return ReasoningAction(
            type=ReasoningActionType.STOP,
            description=(
                "No applicable reasoning rule was found."
            ),
            rationale=(
                "The reasoning rule engine could not "
                "identify a valid next step."
            ),
            confidence=0.5,
            priority=1,
        )

    action = rule_result.action

    if action is None:
        return ReasoningAction(
            type=ReasoningActionType.STOP,
            description=(
                "The matched reasoning rule produced "
                "no action."
            ),
            rationale=(
                f"Rule '{rule_result.rule_name}' matched, "
                "but no reasoning action was attached."
            ),
            confidence=0.0,
            priority=rule_result.priority,
        )

    if action.type != ReasoningActionType.FRAMEWORK:
        return action

    framework = select_best_framework(
        state
    )

    if framework is None:
        return ReasoningAction(
            type=ReasoningActionType.RESEARCH,
            description=(
                "Acquire evidence before selecting "
                "an analytical framework."
            ),
            rationale=(
                "The reasoning diagnosis calls for framework "
                "analysis, but no executable framework currently "
                "has sufficient deterministic fit."
            ),
            unresolved_question=(
                state.unknowns[0]
                if state.unknowns
                else None
            ),
            expected_output=(
                "Evidence sufficient to select "
                "the next framework."
            ),
            confidence=0.5,
            priority=rule_result.priority,
        )

    knowledge = get_framework_knowledge(
        framework
    )

    framework_score = _score_framework(
        state,
        framework,
    )

    return ReasoningAction(
        type=ReasoningActionType.FRAMEWORK,
        description=f"Run {framework}.",
        rationale=(
            f"Rule '{rule_result.rule_name}' selected "
            "framework analysis. "
            f"{framework} has the strongest deterministic "
            "fit with the current DecisionState after evaluating "
            "questions, triggers, exclusions, relationships, "
            "and prerequisites."
        ),
        unresolved_question=(
            knowledge.core_question
            if knowledge
            else None
        ),
        target=framework,
        expected_output=(
            knowledge.expected_output
            if knowledge
            else None
        ),
        confidence=0.7,
        priority=rule_result.priority,
        metadata={
            "rule_id": rule_result.rule_id,
            "framework_score": framework_score,
        },
    )