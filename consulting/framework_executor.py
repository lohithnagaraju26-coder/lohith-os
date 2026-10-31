"""
LOHITH OS — Framework Execution Layer V0.2

Converts framework knowledge plus business-case context into an
executable analytical packet.

This layer does NOT call an LLM yet.
It defines the contract required for real framework execution.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .framework_knowledge import get_framework, search_frameworks


@dataclass
class FrameworkExecutionResult:
    framework: str
    status: str

    # Business-case context
    business_problem: str = ""
    objective: str = ""

    # Framework instructions
    inputs: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    analysis_steps: List[str] = field(default_factory=list)
    reasoning_rule: str = ""
    expected_outputs: List[str] = field(default_factory=list)

    # Evidence and previous analytical work
    available_evidence: Dict[str, Any] = field(default_factory=dict)
    prior_results: List[Dict[str, Any]] = field(default_factory=list)

    # Actual analytical outputs
    findings: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)

    # Quality / handoff
    confidence: Optional[float] = None
    next_framework: str = ""
    handoff_question: str = ""


def _parse_bullets_or_numbered(text: str) -> List[str]:
    """
    Convert a Markdown list into clean items.
    """

    if not text:
        return []

    items: List[str] = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
            continue

        if stripped.startswith("* "):
            items.append(stripped[2:].strip())
            continue

        if ". " in stripped:
            prefix, value = stripped.split(". ", 1)

            if prefix.isdigit():
                items.append(value.strip())

    return items


def prepare_framework_execution(
    framework: Dict[str, Any],
    business_problem: str = "",
    objective: str = "",
    available_evidence: Optional[Dict[str, Any]] = None,
    prior_results: Optional[List[Dict[str, Any]]] = None,
    next_framework: str = "",
) -> FrameworkExecutionResult:
    """
    Convert framework intelligence and case context into an
    executable framework contract.

    This function does not invent findings.

    Findings, decisions, risks, assumptions, and confidence remain
    empty until an actual execution mechanism populates them.
    """

    name = framework.get(
        "name",
        "Unknown Framework",
    )

    return FrameworkExecutionResult(
        framework=name,
        status="READY",
        business_problem=business_problem,
        objective=objective,
        inputs=list(
            framework.get(
                "required_inputs",
                [],
            )
        ),
        questions=list(
            framework.get(
                "key_questions",
                [],
            )
        ),
        analysis_steps=_parse_bullets_or_numbered(
            framework.get(
                "analysis_process",
                "",
            )
        ),
        reasoning_rule=framework.get(
            "framework_reasoning_rule",
            "",
        ),
        expected_outputs=_parse_bullets_or_numbered(
            framework.get(
                "expected_output",
                "",
            )
        ),
        available_evidence=available_evidence or {},
        prior_results=prior_results or [],
        next_framework=next_framework,
    )


def build_framework_execution_plan(
    framework_sequence: List[Dict[str, Any]],
    framework_intelligence: List[Dict[str, Any]],
    business_problem: str = "",
    objective: str = "",
    available_evidence: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Build an executable plan from an already ordered framework sequence.

    This creates the dependency structure for execution but does not
    invent findings or claim that any framework has been executed.
    """

    intelligence_by_name = {
        framework.get("name"): framework
        for framework in framework_intelligence
        if framework.get("name")
    }

    plan: List[Dict[str, Any]] = []

    for index, step in enumerate(
        framework_sequence
    ):
        framework_name = step.get(
            "framework",
            "",
        )

        framework = intelligence_by_name.get(
            framework_name
        )

        if framework is None:
            continue

        next_framework = ""

        if index + 1 < len(framework_sequence):
            next_framework = framework_sequence[
                index + 1
            ].get(
                "framework",
                "",
            )

        previous_framework = ""

        if index > 0:
            previous_framework = framework_sequence[
                index - 1
            ].get(
                "framework",
                "",
            )

        result = prepare_framework_execution(
            framework=framework,
            business_problem=business_problem,
            objective=objective,
            available_evidence=available_evidence,
            prior_results=[],
            next_framework=next_framework,
        )

        packet = execution_packet(result)

        packet["step"] = index + 1
        packet["depends_on"] = (
            [previous_framework]
            if previous_framework
            else []
        )

        packet["execution_status"] = "PENDING"

        plan.append(packet)

    return plan



def route_framework_handoff(
    completed_result: Dict[str, Any],
    completed_frameworks: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Validate and route a framework handoff.

    The framework registry is the execution capability boundary.

    A framework must:
        1. Exist in the canonical knowledge layer.
        2. Be registered as executable.
        3. Not have already been executed.
        4. Have a valid handoff question.
    """

    from .framework_registry import (
        get_capability,
        get_executable_frameworks,
    )

    completed_frameworks = completed_frameworks or []

    proposed_framework = str(
        completed_result.get(
            "next_framework",
            "",
        )
    ).strip()

    handoff_question = str(
        completed_result.get(
            "handoff_question",
            "",
        )
    ).strip()

    completed_normalized = {
        str(name).strip().lower()
        for name in completed_frameworks
        if str(name).strip()
    }

    # ---------------------------------------------------------------
    # 1. No handoff requested
    # ---------------------------------------------------------------

    if not proposed_framework:
        return {
            "status": "STOP",
            "next_framework": "",
            "handoff_question": handoff_question,
            "reason": "No next framework was proposed.",
            "candidate_frameworks": [],
        }

    # ---------------------------------------------------------------
    # 2. Handoff question is required
    # ---------------------------------------------------------------

    if not handoff_question:
        return {
            "status": "REJECT",
            "next_framework": "",
            "handoff_question": "",
            "reason": (
                "A next framework was proposed without "
                "a handoff question."
            ),
            "candidate_frameworks": [],
        }

    # ---------------------------------------------------------------
    # 3. Validate framework capability
    # ---------------------------------------------------------------

    capability = get_capability(
        proposed_framework
    )

    if capability is None:
        return {
            "status": "REJECT",
            "next_framework": "",
            "handoff_question": handoff_question,
            "reason": (
                "Proposed framework does not exist "
                "in the LOHITH OS framework knowledge layer."
            ),
            "candidate_frameworks": [],
        }

    if not capability.executable:
        return {
            "status": "REJECT",
            "next_framework": "",
            "handoff_question": handoff_question,
            "reason": (
                "Framework is known to LOHITH OS but is "
                "not currently executable."
            ),
            "candidate_frameworks": get_executable_frameworks()[:5],
        }

    framework_name = capability.name

    # ---------------------------------------------------------------
    # 4. Prevent framework repetition
    # ---------------------------------------------------------------

    if framework_name.lower() in completed_normalized:
        return {
            "status": "REJECT",
            "next_framework": "",
            "handoff_question": handoff_question,
            "reason": (
                "Proposed framework has already been executed."
            ),
            "candidate_frameworks": [],
        }

    # ---------------------------------------------------------------
    # 5. Valid handoff
    # ---------------------------------------------------------------

    return {
        "status": "APPROVE",
        "next_framework": framework_name,
        "handoff_question": handoff_question,
        "reason": (
            "Framework exists, is executable, has not been "
            "executed, and has a valid analytical handoff question."
        ),
        "candidate_frameworks": [],
    }


def attach_framework_result(
    next_packet: Dict[str, Any],
    completed_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Pass a completed framework result into the next framework.

    This function does not interpret or modify the findings.
    It only creates an explicit analytical handoff.
    """

    updated_packet = dict(next_packet)

    prior_results = list(
        updated_packet.get(
            "prior_results",
            [],
        )
    )

    prior_results.append(
        {
            "framework": completed_result.get(
                "framework",
                "",
            ),
            "status": completed_result.get(
                "status",
                "",
            ),
            "findings": completed_result.get(
                "findings",
                [],
            ),
            "decisions": completed_result.get(
                "decisions",
                [],
            ),
            "risks": completed_result.get(
                "risks",
                [],
            ),
            "assumptions": completed_result.get(
                "assumptions",
                [],
            ),
            "confidence": completed_result.get(
                "confidence",
            ),
            "next_framework": completed_result.get(
                "next_framework",
                "",
            ),
            "handoff_question": completed_result.get(
                "handoff_question",
                "",
            ),
        }
    )

    updated_packet["prior_results"] = prior_results

    return updated_packet



def execute_framework_with_model(
    packet: Dict[str, Any],
    model_callable,
) -> Dict[str, Any]:
    """
    Execute one framework through an injected model callable.

    The model callable must accept:
        prompt: str

    and return a dictionary containing:
        framework
        status
        findings
        decisions
        risks
        assumptions
        confidence

    This keeps model/provider-specific code outside the
    framework orchestration layer.
    """

    prompt = build_framework_reasoning_prompt(
        packet
    )

    model_result = model_callable(
        prompt
    )

    if not isinstance(
        model_result,
        dict,
    ):
        raise TypeError(
            "Model callable must return a dictionary."
        )

    result = dict(
        model_result
    )

    result.setdefault(
        "framework",
        packet.get(
            "framework",
            "",
        ),
    )

    result.setdefault(
        "status",
        "COMPLETE",
    )

    result.setdefault(
        "findings",
        [],
    )

    result.setdefault(
        "decisions",
        [],
    )

    result.setdefault(
        "risks",
        [],
    )

    result.setdefault(
        "assumptions",
        [],
    )

    result.setdefault(
        "confidence",
        None,
    )

    return validate_framework_result(
        result
    )



def local_framework_executor(
    packet: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Deterministic local executor for development and testing.

    This does NOT perform real consulting analysis.
    It creates a transparent placeholder result so the complete
    orchestration architecture can be tested without an API call.
    """

    framework = packet.get(
        "framework",
        "Unknown Framework",
    )

    missing_inputs = []

    for item in packet.get(
        "inputs",
        [],
    ):
        if item not in packet.get(
            "available_evidence",
            {},
        ):
            missing_inputs.append(item)

    findings = [
        (
            f"{framework} is ready for execution, "
            "but no model-based analytical findings have "
            "been generated yet."
        )
    ]

    decisions = [
        (
            "Collect the required evidence before making "
            "a substantive framework conclusion."
        )
    ]

    risks = []

    if missing_inputs:
        risks.append(
            "Required evidence is missing for: "
            + ", ".join(missing_inputs)
        )

    assumptions = [
        (
            "The available business description is "
            "insufficient to complete the framework "
            "without additional evidence."
        )
    ]

    return {
        "framework": framework,
        "status": "COMPLETE_LOCAL_PLACEHOLDER",
        "findings": findings,
        "decisions": decisions,
        "risks": risks,
        "assumptions": assumptions,
        "confidence": 0.10,
        "next_framework": "",
        "handoff_question": "",
    }



def build_framework_reasoning_prompt(
    packet: Dict[str, Any],
) -> str:
    """
    Build a model-ready reasoning prompt from a framework packet.

    This layer prepares the analytical instructions.
    It does not call a model.
    """

    prior_results = packet.get(
        "prior_results",
        [],
    )

    prior_context_parts: List[str] = []

    for result in prior_results:
        findings = result.get("findings", [])
        decisions = result.get("decisions", [])
        risks = result.get("risks", [])
        assumptions = result.get("assumptions", [])

        findings_text = (
            "\n".join(f"- {item}" for item in findings)
            if findings
            else "- None"
        )

        decisions_text = (
            "\n".join(f"- {item}" for item in decisions)
            if decisions
            else "- None"
        )

        risks_text = (
            "\n".join(f"- {item}" for item in risks)
            if risks
            else "- None"
        )

        assumptions_text = (
            "\n".join(f"- {item}" for item in assumptions)
            if assumptions
            else "- None"
        )

        prior_context_parts.append(
            "\n".join(
                [
                    f"FRAMEWORK: {result.get('framework', '')}",
                    f"STATUS: {result.get('status', '')}",
                    "",
                    "FINDINGS:",
                    findings_text,
                    "",
                    "DECISIONS:",
                    decisions_text,
                    "",
                    "RISKS:",
                    risks_text,
                    "",
                    "ASSUMPTIONS:",
                    assumptions_text,
                    "",
                    f"CONFIDENCE: {result.get('confidence')}",
                ]
            )
        )

    prior_context = (
        "\n\n".join(prior_context_parts)
        if prior_context_parts
        else "No prior framework results."
    )

    questions = "\n".join(
        f"{index}. {question}"
        for index, question in enumerate(
            packet.get("questions", []),
            start=1,
        )
    )

    analysis_steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(
            packet.get("analysis_steps", []),
            start=1,
        )
    )

    expected_outputs = "\n".join(
        f"- {item}"
        for item in packet.get(
            "expected_outputs",
            [],
        )
    )

    evidence_lines = []

    for key, value in packet.get(
        "available_evidence",
        {},
    ).items():
        evidence_lines.append(
            f"- {key}: {value}"
        )

    available_evidence = (
        "\n".join(evidence_lines)
        if evidence_lines
        else "- No additional evidence supplied."
    )

    required_inputs = "\n".join(
        f"- {item}"
        for item in packet.get(
            "inputs",
            [],
        )
    )

    prompt_sections = [
        f"You are executing the consulting framework: {packet.get('framework', '')}",
        "",
        "BUSINESS PROBLEM",
        packet.get("business_problem", ""),
        "",
        "OBJECTIVE",
        packet.get("objective", ""),
        "",
        "FRAMEWORK REASONING RULE",
        packet.get("reasoning_rule", ""),
        "",
        "REQUIRED INPUTS",
        required_inputs,
        "",
        "AVAILABLE EVIDENCE",
        available_evidence,
        "",
        "FRAMEWORK QUESTIONS",
        questions,
        "",
        "ANALYSIS PROCESS",
        analysis_steps,
        "",
        "EXPECTED OUTPUTS",
        expected_outputs,
        "",
        "PRIOR FRAMEWORK RESULTS",
        prior_context,
        "",
        "INSTRUCTIONS",
        "",
        "1. Apply the framework to the business problem.",
        "2. Follow the stated analysis process.",
        "3. Use the framework questions to guide the analysis.",
        "4. Distinguish observed evidence, inference, and untested assumptions.",
        "5. Never invent data, facts, measurements, sources, or business conditions.",
        "6. Explicitly identify missing evidence.",
        "7. Use prior framework results as analytical inputs, not unquestioned facts.",
        "8. Challenge prior assumptions when evidence contradicts them.",
        "9. Focus on decision-relevant findings.",
        "10. Identify material risks and assumptions.",
        "11. Provide a confidence score between 0 and 1.",
        "12. Prepare findings for the next analytical step.",
        "",
        "HANDOFF REASONING",
        "",
        "After completing this framework:",
        "13. Identify the most important unresolved analytical question created by your findings.",
        "14. Determine whether another framework is actually required to answer that question.",
        "15. If another framework is required, select the most appropriate next framework.",
        "16. Explain the analytical handoff through a specific handoff question.",
        "17. The next framework must follow from the findings, not merely from the original framework order.",
        "18. Never select a framework merely to continue the chain.",
        "19. If no additional framework is required, leave next_framework and handoff_question empty.",
        "20. Never invent a framework name. Use only frameworks available to LOHITH OS.",
        "",
        "RETURN STRUCTURE",
        "",
        "framework:",
        "status:",
        "findings:",
        "decisions:",
        "risks:",
        "assumptions:",
        "confidence:",
        "next_framework:",
        "handoff_question:",
        "",
        "The findings must be specific to this business problem.",
        "The handoff question must be directly supported by the findings.",
    ]

    return "\n".join(prompt_sections).strip()



def validate_framework_result(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate and normalize a completed framework result.

    This protects the reasoning chain from malformed executor output.
    It does not judge whether the analytical conclusions are correct.
    """

    if not isinstance(result, dict):
        raise TypeError(
            "Framework executor must return a dictionary."
        )

    normalized = dict(result)

    required_fields = [
        "framework",
        "status",
        "findings",
        "decisions",
        "risks",
        "assumptions",
        "confidence",
    ]

    for field_name in required_fields:
        if field_name not in normalized:
            raise ValueError(
                f"Framework result is missing required field: "
                f"{field_name}"
            )

    list_fields = [
        "findings",
        "decisions",
        "risks",
        "assumptions",
    ]

    for field_name in list_fields:
        if not isinstance(
            normalized[field_name],
            list,
        ):
            raise TypeError(
                f"Framework result field '{field_name}' "
                f"must be a list."
            )

    confidence = normalized["confidence"]

    if confidence is not None:
        if not isinstance(
            confidence,
            (int, float),
        ):
            raise TypeError(
                "Framework result confidence must be "
                "a number or None."
            )

        if not 0 <= confidence <= 1:
            raise ValueError(
                "Framework result confidence must be "
                "between 0 and 1."
            )

    # Handoff fields are optional because the final framework
    # in a chain may not need a successor.
    next_framework = normalized.get(
        "next_framework",
        "",
    )

    handoff_question = normalized.get(
        "handoff_question",
        "",
    )

    if not isinstance(next_framework, str):
        raise TypeError(
            "Framework result next_framework must be a string."
        )

    if not isinstance(handoff_question, str):
        raise TypeError(
            "Framework result handoff_question must be a string."
        )

    normalized["next_framework"] = next_framework.strip()
    normalized["handoff_question"] = handoff_question.strip()

    return normalized



def run_adaptive_framework_chain(
    state,
    executor,
    max_steps: int = 8,
):
    """
    Execute an adaptive reasoning chain using DecisionState
    as the canonical public interface.

    DecisionState is the source of truth.

    The reasoning router determines the next action.
    The framework execution layer only executes a framework
    selected by the router and validated by the handoff guard.
    """

    from core import DecisionState
    from core.reasoning_action import ReasoningActionType
    from core.reasoning_router import route_reasoning
    from core.reasoning_evaluator import evaluate_reasoning_step

    from .decision_state_adapter import (
        apply_framework_result_to_state,
        state_to_framework_packet,
    )

    if not isinstance(state, DecisionState):
        raise TypeError(
            "run_adaptive_framework_chain requires a DecisionState."
        )

    if max_steps < 1:
        raise ValueError(
            "max_steps must be at least 1."
        )

    completed_results: List[Dict[str, Any]] = []

    for step in range(max_steps):

        # -----------------------------------------------------------
        # 1. Diagnose the current DecisionState
        # -----------------------------------------------------------

        action = route_reasoning(state)

        # -----------------------------------------------------------
        # 2. Handle non-framework reasoning actions
        # -----------------------------------------------------------

        if action.type == ReasoningActionType.STOP:
            state.stop(
                reason=action.rationale
            )
            break

        if action.type != ReasoningActionType.FRAMEWORK:
            state.stop(
                reason=(
                    f"Reasoning router selected "
                    f"{action.type.value}: "
                    f"{action.description}"
                )
            )
            break

        # -----------------------------------------------------------
        # 3. Router must provide a framework target
        # -----------------------------------------------------------

        current_framework = action.target

        if not current_framework:
            state.stop(
                reason=(
                    "Reasoning router selected FRAMEWORK "
                    "without a framework target."
                )
            )
            break

        # -----------------------------------------------------------
        # 4. Validate router-selected framework
        # -----------------------------------------------------------

        validation = route_framework_handoff(
            {
                "next_framework": current_framework,
                "handoff_question": (
                    action.unresolved_question
                    or action.description
                ),
            },
            [
                result.get(
                    "framework",
                    "",
                )
                for result in completed_results
            ],
        )

        if validation["status"] != "APPROVE":
            state.stop(
                reason=(
                    "Router-selected framework rejected: "
                    + validation["reason"]
                )
            )
            break

        # -----------------------------------------------------------
        # 5. Build execution context from canonical DecisionState
        # -----------------------------------------------------------

        packet = state_to_framework_packet(
            state,
            framework=current_framework,
        )

        packet["execution_status"] = "RUNNING"
        packet["chain_step"] = step + 1

        packet["prior_results"] = list(
            completed_results
        )

        # -----------------------------------------------------------
        # 6. Execute the selected framework
        # -----------------------------------------------------------

        completed_packet = executor(
            packet
        )

        if not isinstance(
            completed_packet,
            dict,
        ):
            raise TypeError(
                "Framework executor must return a dictionary."
            )

        completed_packet = dict(
            completed_packet
        )

        completed_packet.setdefault(
            "framework",
            current_framework,
        )

        completed_packet.setdefault(
            "status",
            "COMPLETE",
        )

        completed_packet.setdefault(
            "findings",
            [],
        )

        completed_packet.setdefault(
            "decisions",
            [],
        )

        completed_packet.setdefault(
            "risks",
            [],
        )

        completed_packet.setdefault(
            "assumptions",
            [],
        )

        completed_packet.setdefault(
            "confidence",
            None,
        )

        completed_packet.setdefault(
            "next_framework",
            "",
        )

        completed_packet.setdefault(
            "handoff_question",
            "",
        )

        # -----------------------------------------------------------
        # 7. Validate framework result
        # -----------------------------------------------------------

        completed_packet = validate_framework_result(
            completed_packet
        )

        completed_results.append(
            completed_packet
        )

        # -----------------------------------------------------------
        # 8. Apply analytical outputs to DecisionState
        # -----------------------------------------------------------

        state_before_step = state.model_copy(
            deep=True
        )

        apply_framework_result_to_state(
            state,
            completed_packet,
        )

        # -----------------------------------------------------------
        # 9. Critic / evaluator quality gate
        # -----------------------------------------------------------

        evaluation = evaluate_reasoning_step(
            state_before_step,
            state,
        )

        if not evaluation.useful_progress:
            state.stop(
                reason=(
                    "Critic rejected the reasoning step: "
                    "no useful progress was detected."
                )
            )
            break

        if not evaluation.continue_reasoning:
            state.stop(
                reason=evaluation.stop_reason
            )
            break

        # -----------------------------------------------------------
        # 10. Continue through the reasoning router
        # -----------------------------------------------------------

        next_action = route_reasoning(
            state
        )

        if next_action.type == ReasoningActionType.STOP:
            state.stop(
                reason=next_action.rationale
            )
            break

        if next_action.type != ReasoningActionType.FRAMEWORK:
            state.stop(
                reason=(
                    f"Reasoning router selected "
                    f"{next_action.type.value}: "
                    f"{next_action.description}"
                )
            )
            break

        next_framework = next_action.target

        if not next_framework:
            state.stop(
                reason=(
                    "Reasoning router selected FRAMEWORK "
                    "without a framework target."
                )
            )
            break

        # -----------------------------------------------------------
        # 11. Validate the router's next framework before continuing
        # -----------------------------------------------------------

        next_validation = route_framework_handoff(
            {
                "next_framework": next_framework,
                "handoff_question": (
                    next_action.unresolved_question
                    or next_action.description
                ),
            },
            [
                result.get(
                    "framework",
                    "",
                )
                for result in completed_results
            ],
        )

        if next_validation["status"] != "APPROVE":
            state.stop(
                reason=(
                    "Next reasoning action rejected: "
                    + next_validation["reason"]
                )
            )
            break

        state.continue_reasoning(
            reason=(
                next_action.unresolved_question
                or next_action.description
            )
        )

    else:
        state.stop(
            reason=(
                "Maximum adaptive reasoning steps reached."
            )
        )

    return state


def run_framework_chain(
    execution_plan: List[Dict[str, Any]],
    executor,
) -> List[Dict[str, Any]]:
    """
    Execute an ordered framework chain.

    The executor is injected so this orchestration layer remains
    independent of any particular AI/model implementation.

    Expected executor contract:

        executor(packet) -> completed_packet

    The completed packet must contain:
        status
        findings
        decisions
        risks
        assumptions
        confidence

    No model-specific logic belongs in this function.
    """

    completed_results: List[Dict[str, Any]] = []

    for packet in execution_plan:
        current_packet = dict(packet)

        if completed_results:
            current_packet["prior_results"] = list(
                completed_results
            )

        current_packet["execution_status"] = "RUNNING"

        completed_packet = executor(
            current_packet
        )

        if not isinstance(
            completed_packet,
            dict,
        ):
            raise TypeError(
                "Framework executor must return a dictionary."
            )

        completed_packet = dict(
            completed_packet
        )

        completed_packet.setdefault(
            "framework",
            current_packet.get(
                "framework",
                "",
            ),
        )

        completed_packet.setdefault(
            "status",
            "COMPLETE",
        )

        completed_packet.setdefault(
            "findings",
            [],
        )

        completed_packet.setdefault(
            "decisions",
            [],
        )

        completed_packet.setdefault(
            "risks",
            [],
        )

        completed_packet.setdefault(
            "assumptions",
            [],
        )

        completed_packet.setdefault(
            "confidence",
            None,
        )

        completed_packet = validate_framework_result(
            completed_packet
        )

        completed_results.append(
            completed_packet
        )

    return completed_results



def execution_packet(
    result: FrameworkExecutionResult,
) -> Dict[str, Any]:
    """
    Convert an execution result into a serializable dictionary.
    """

    return {
        "framework": result.framework,
        "status": result.status,
        "business_problem": result.business_problem,
        "objective": result.objective,
        "inputs": result.inputs,
        "questions": result.questions,
        "analysis_steps": result.analysis_steps,
        "reasoning_rule": result.reasoning_rule,
        "expected_outputs": result.expected_outputs,
        "available_evidence": result.available_evidence,
        "prior_results": result.prior_results,
        "findings": result.findings,
        "decisions": result.decisions,
        "risks": result.risks,
        "assumptions": result.assumptions,
        "confidence": result.confidence,
        "next_framework": result.next_framework,
    }


if __name__ == "__main__":
    from consulting.framework_knowledge import get_framework

    framework = get_framework(
        "Process Mapping"
    )

    if framework is None:
        raise SystemExit(
            "Process Mapping framework could not be loaded."
        )

    intelligence = framework.to_dict()

    result = prepare_framework_execution(
        framework=intelligence,
        business_problem=(
            "A company spends hundreds of employee hours "
            "every month on a repetitive workflow."
        ),
        objective=(
            "Determine whether the workflow should be "
            "automated and what approach should be used."
        ),
        available_evidence={
            "task_frequency": "Daily",
            "time_spent": "High",
            "error_rate": "Unknown",
        },
        next_framework=(
            "AI Feasibility Assessment"
        ),
    )

    packet = execution_packet(result)

    print("\n" + "=" * 70)
    print(
        "LOHITH OS — FRAMEWORK EXECUTION LAYER V0.2"
    )
    print("=" * 70)

    print(
        f"\nFramework: {packet['framework']}"
    )
    print(
        f"Status: {packet['status']}"
    )

    print("\nBUSINESS PROBLEM")
    print(packet["business_problem"])

    print("\nOBJECTIVE")
    print(packet["objective"])

    print("\nQUESTIONS")
    for item in packet["questions"]:
        print(f"- {item}")

    print("\nAVAILABLE EVIDENCE")
    for key, value in packet[
        "available_evidence"
    ].items():
        print(f"- {key}: {value}")

    print("\nANALYSIS STEPS")
    for index, item in enumerate(
        packet["analysis_steps"],
        start=1,
    ):
        print(f"{index}. {item}")

    print("\nREASONING RULE")
    print(packet["reasoning_rule"])

    print("\nEXPECTED OUTPUTS")
    for item in packet[
        "expected_outputs"
    ]:
        print(f"- {item}")

    print(
        f"\nNEXT FRAMEWORK: "
        f"{packet['next_framework']}"
    )

    print(
        "\nPASS — Framework execution "
        "contract V0.2 created."
    )
