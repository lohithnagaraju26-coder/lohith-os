"""
LOHITH OS — Consulting Brain V1 Pipeline

End-to-end orchestration:
Business Problem
→ Reasoning
→ Framework Execution
→ Synthesis
→ CEO-ready Decision Package
"""

from typing import Any, Callable, Dict, Optional

from consulting.reasoning_engine import analyze_business_problem
from consulting.framework_executor import (
    run_framework_chain,
    execute_framework_with_model,
)
from consulting.synthesis_engine import (
    build_synthesis_packet,
    execute_synthesis_with_model,
    build_consulting_decision_package,
)

from consulting.model_adapter import (
    run_framework_model,
    run_synthesis_model,
)


def run_consulting_pipeline(
    business_problem: str,
    objective: str,
    problem_type: Optional[str] = None,
    structure: Optional[str] = None,
    evidence: Optional[Dict[str, Any]] = None,
    framework_model_callable: Optional[Callable] = None,
    synthesis_model_callable: Optional[Callable] = None,
) -> Dict[str, Any]:
    """Run the complete Consulting Brain V1 pipeline."""

    reasoning = analyze_business_problem(
        problem=business_problem,
        objective=objective,
        problem_type=problem_type or "multi_domain",
        problem_structure=structure or "decision",
    )

    execution_plan = reasoning.get(
        "framework_execution_plan",
        [],
    )

    if not execution_plan:
        raise ValueError(
            "Reasoning engine produced no framework execution plan."
        )

    if framework_model_callable is None:
        raise ValueError(
            "A framework_model_callable is required."
        )

    if synthesis_model_callable is None:
        raise ValueError(
            "A synthesis_model_callable is required."
        )

    def framework_executor(packet):
        result = execute_framework_with_model(
            packet,
            framework_model_callable,
        )

        # The orchestration layer is authoritative about which
        # framework is currently being executed.
        result["framework"] = packet.get(
            "framework",
            result.get("framework", ""),
        )

        return result

    framework_results = run_framework_chain(
        execution_plan,
        framework_executor,
    )

    synthesis_packet = build_synthesis_packet(
        business_problem=business_problem,
        objective=objective,
        framework_results=framework_results,
    )

    synthesis_result = execute_synthesis_with_model(
        synthesis_packet,
        synthesis_model_callable,
    )

    decision_package = build_consulting_decision_package(
        business_problem=business_problem,
        objective=objective,
        synthesis_result=synthesis_result,
    )

    return {
        "status": "CONSULTING_PIPELINE_COMPLETE",
        "business_problem": business_problem,
        "objective": objective,
        "reasoning": reasoning,
        "framework_execution_plan": execution_plan,
        "framework_results": framework_results,
        "synthesis_packet": synthesis_packet,
        "synthesis_result": synthesis_result,
        "decision_package": decision_package,
    }


def run_live_consulting_pipeline(
    business_problem: str,
    objective: str,
    problem_type: Optional[str] = None,
    structure: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the Consulting Brain using the configured real model adapter.

    This function performs a live model call and therefore requires
    valid API configuration and available API usage.
    """

    return run_consulting_pipeline(
        business_problem=business_problem,
        objective=objective,
        problem_type=problem_type,
        structure=structure,
        framework_model_callable=run_framework_model,
        synthesis_model_callable=run_synthesis_model,
    )


if __name__ == "__main__":
    print("=" * 70)
    print("LOHITH OS — CONSULTING BRAIN V1")
    print("=" * 70)
    print("PASS — Consulting pipeline module loaded successfully.")
