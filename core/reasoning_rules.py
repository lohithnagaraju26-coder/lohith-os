from typing import List

from .reasoning_action import (
    ReasoningAction,
    ReasoningActionType,
)
from .reasoning_rule import (
    ReasoningRule,
    RuleCondition,
    RuleOperator,
)


def build_reasoning_rules() -> List[ReasoningRule]:
    """
    Return the canonical V1 reasoning rule catalog.

    These rules operate on valid DecisionState objects.
    Input validation and construction of DecisionState happen
    before the reasoning engine.

    Higher priority means the rule takes precedence over
    lower-priority rules when multiple rules match.
    """

    return [
        # 100 — TERMINAL OUTCOME
        ReasoningRule(
            id="STOP-OUTCOME-COMPLETE",
            name="Outcome Already Recorded",
            description=(
                "Stop reasoning when an actual outcome "
                "has already been recorded."
            ),
            conditions=[
                RuleCondition(
                    field="outcome",
                    operator=RuleOperator.EXISTS,
                    value=True,
                    description="An outcome already exists.",
                ),
            ],
            action=ReasoningAction(
                type=ReasoningActionType.STOP,
                description=(
                    "Stop because the decision already "
                    "has an outcome."
                ),
                rationale=(
                    "Further reasoning is unnecessary once "
                    "the current decision outcome is recorded."
                ),
                expected_output="No further reasoning required.",
                confidence=0.95,
            ),
            priority=100,
        ),

        # 90 — CONTRADICTION
        ReasoningRule(
            id="RESEARCH-CONTRADICTION",
            name="Unresolved Contradiction",
            description=(
                "Investigate unresolved contradictions before "
                "advancing reasoning."
            ),
            conditions=[
                RuleCondition(
                    field="contradictions",
                    operator=RuleOperator.EXISTS,
                    value=True,
                    description="At least one contradiction exists.",
                ),
            ],
            action=ReasoningAction(
                type=ReasoningActionType.RESEARCH,
                description=(
                    "Investigate the unresolved contradiction."
                ),
                rationale=(
                    "Conflicting evidence can materially "
                    "change the decision."
                ),
                unresolved_question=(
                    "Which evidence or assumption is correct?"
                ),
                expected_output=(
                    "Evidence that resolves or narrows "
                    "the contradiction."
                ),
                confidence=0.90,
            ),
            priority=90,
        ),

        # 80 — MATERIAL UNKNOWN
        ReasoningRule(
            id="RESEARCH-UNKNOWN",
            name="Material Unknowns",
            description=(
                "Acquire evidence when important unknowns remain."
            ),
            conditions=[
                RuleCondition(
                    field="unknowns",
                    operator=RuleOperator.EXISTS,
                    value=True,
                    description="Material unknowns remain.",
                ),
            ],
            action=ReasoningAction(
                type=ReasoningActionType.RESEARCH,
                description=(
                    "Acquire evidence for the highest-value "
                    "unresolved unknown."
                ),
                rationale=(
                    "The decision cannot be reliably advanced "
                    "without resolving important unknowns."
                ),
                unresolved_question=(
                    "What information is most important "
                    "to resolve next?"
                ),
                expected_output=(
                    "New evidence addressing a material unknown."
                ),
                confidence=0.75,
            ),
            priority=80,
        ),

        # 75 — INITIAL ANALYSIS
        ReasoningRule(
            id="ANALYZE-INITIAL",
            name="Initial Structured Analysis",
            description=(
                "Begin structured analysis when a valid decision "
                "state has not yet produced findings."
            ),
            conditions=[
                RuleCondition(
                    field="outcome",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No outcome has been recorded.",
                ),
                RuleCondition(
                    field="recommendation",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No recommendation exists.",
                ),
                RuleCondition(
                    field="findings",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No findings exist yet.",
                ),
                RuleCondition(
                    field="contradictions",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No contradictions exist.",
                ),
            ],
            action=ReasoningAction(
                type=ReasoningActionType.FRAMEWORK,
                description=(
                    "Select the highest-value executable "
                    "framework for the initial analysis."
                ),
                rationale=(
                    "The decision is valid and has not yet "
                    "produced analytical findings."
                ),
                unresolved_question=(
                    "What is the highest-value question "
                    "that should be answered first?"
                ),
                expected_output=(
                    "Initial structured findings that "
                    "advance the decision."
                ),
                confidence=0.70,
            ),
            priority=75,
        ),

        # 70 — STRUCTURED ANALYSIS
        ReasoningRule(
            id="ANALYZE-WITH-FRAMEWORK",
            name="Structured Analysis Required",
            description=(
                "Use structured analysis when meaningful "
                "unresolved reasoning work remains."
            ),
            conditions=[
                RuleCondition(
                    field="findings",
                    operator=RuleOperator.EXISTS,
                    value=True,
                    description=(
                        "Existing findings can support "
                        "further structured analysis."
                    ),
                ),
            ],
            action=ReasoningAction(
                type=ReasoningActionType.FRAMEWORK,
                description=(
                    "Select the highest-value executable "
                    "framework for the current decision state."
                ),
                rationale=(
                    "Structured analysis can convert existing "
                    "findings into stronger decision insight."
                ),
                unresolved_question=(
                    "What analytical approach best advances "
                    "the decision?"
                ),
                expected_output=(
                    "Structured findings and "
                    "decision-relevant evidence."
                ),
                confidence=0.70,
            ),
            priority=70,
        ),

        # 60 — DECISION EVALUATION
        ReasoningRule(
            id="ANALYZE-DECISION-READY",
            name="Decision Evaluation Required",
            description=(
                "Evaluate available findings when material "
                "unknowns and contradictions have been resolved."
            ),
            conditions=[
                RuleCondition(
                    field="findings",
                    operator=RuleOperator.EXISTS,
                    value=True,
                    description="At least one finding exists.",
                ),
                RuleCondition(
                    field="unknowns",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No material unknowns remain.",
                ),
                RuleCondition(
                    field="contradictions",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No contradictions remain.",
                ),
            ],
            action=ReasoningAction(
                type=ReasoningActionType.FRAMEWORK,
                description=(
                    "Use a decision-oriented analytical "
                    "framework to evaluate the available findings."
                ),
                rationale=(
                    "Meaningful findings exist and material "
                    "uncertainty has been resolved."
                ),
                unresolved_question=(
                    "Which available option best satisfies "
                    "the decision objective?"
                ),
                expected_output=(
                    "A structured comparison of decision options "
                    "leading toward a recommendation."
                ),
                confidence=0.80,
            ),
            priority=60,
        ),

        # 50 — DECISION COMPLETE
        ReasoningRule(
            id="STOP-DECISION-COMPLETE",
            name="Recommendation Complete",
            description=(
                "Stop when a recommendation exists and there "
                "are no unresolved unknowns or contradictions."
            ),
            conditions=[
                RuleCondition(
                    field="recommendation",
                    operator=RuleOperator.EXISTS,
                    value=True,
                    description="A recommendation exists.",
                ),
                RuleCondition(
                    field="unknowns",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No material unknowns remain.",
                ),
                RuleCondition(
                    field="contradictions",
                    operator=RuleOperator.NOT_EXISTS,
                    value=True,
                    description="No contradictions remain.",
                ),
            ],
            action=ReasoningAction(
                type=ReasoningActionType.STOP,
                description=(
                    "Stop because the decision has a "
                    "complete recommendation."
                ),
                rationale=(
                    "A recommendation exists and no material "
                    "unknowns or contradictions remain."
                ),
                expected_output="Final decision recommendation.",
                confidence=0.95,
            ),
            priority=50,
        ),
    ]


def get_reasoning_rules() -> List[ReasoningRule]:
    """Return reasoning rules ordered by descending priority."""
    return sorted(
        build_reasoning_rules(),
        key=lambda rule: rule.priority,
        reverse=True,
    )
