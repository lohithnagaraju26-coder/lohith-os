"""
LOHITH OS — Consulting Synthesis Engine V0.1

Combines completed framework results into a structured synthesis packet.

This layer does NOT make unsupported business conclusions.
It prepares the evidence and decision structure required for
a later synthesis/recommendation model.
"""

from typing import Any, Dict, List


def build_synthesis_packet(
    business_problem: str,
    objective: str,
    framework_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Build a structured synthesis packet from completed framework results.
    """

    findings: List[Dict[str, Any]] = []
    decisions: List[Dict[str, Any]] = []
    risks: List[Dict[str, Any]] = []
    assumptions: List[Dict[str, Any]] = []

    for result in framework_results:
        framework = result.get(
            "framework",
            "Unknown Framework",
        )

        for item in result.get(
            "findings",
            [],
        ):
            findings.append(
                {
                    "framework": framework,
                    "finding": item,
                }
            )

        for item in result.get(
            "decisions",
            [],
        ):
            decisions.append(
                {
                    "framework": framework,
                    "decision": item,
                }
            )

        for item in result.get(
            "risks",
            [],
        ):
            risks.append(
                {
                    "framework": framework,
                    "risk": item,
                }
            )

        for item in result.get(
            "assumptions",
            [],
        ):
            assumptions.append(
                {
                    "framework": framework,
                    "assumption": item,
                }
            )

    return {
        "business_problem": business_problem,
        "objective": objective,
        "framework_count": len(
            framework_results
        ),
        "framework_results": framework_results,
        "findings": findings,
        "decisions": decisions,
        "risks": risks,
        "assumptions": assumptions,

        "synthesis_questions": [
            "What are the most important findings across all frameworks?",
            "Which findings are supported by multiple frameworks?",
            "Which findings conflict with one another?",
            "Which findings are observations versus inferences?",
            "What evidence is still missing?",
            "What assumptions materially affect the conclusion?",
            "What are the true root causes?",
            "Which causes are controllable?",
            "Which causes have the greatest business impact?",
            "What options are realistically available?",
            "What are the trade-offs between the options?",
            "What should the business do?",
            "Why is that recommendation superior to the alternatives?",
            "What risks could overturn the recommendation?",
            "What should happen first?",
            "Which KPIs should determine whether the recommendation is working?",
        ],

        "status": (
            "Synthesis packet created. "
            "Cross-framework interpretation required."
        ),
    }


def validate_synthesis_result(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate and normalize a synthesis result.
    """

    if not isinstance(result, dict):
        raise TypeError(
            "Synthesis model must return a dictionary."
        )

    required_fields = [
        "key_findings",
        "root_causes",
        "evidence_gaps",
        "options",
        "trade_offs",
        "recommendation",
        "recommendation_rationale",
        "risks",
        "critical_assumptions",
        "implementation_priorities",
        "kpis",
        "confidence",
    ]

    for field_name in required_fields:
        if field_name not in result:
            raise ValueError(
                "Synthesis result is missing required field: "
                + field_name
            )

    list_fields = [
        "key_findings",
        "root_causes",
        "evidence_gaps",
        "options",
        "trade_offs",
        "risks",
        "critical_assumptions",
        "implementation_priorities",
        "kpis",
    ]

    normalized = dict(result)

    for field_name in list_fields:
        if not isinstance(
            normalized[field_name],
            list,
        ):
            raise TypeError(
                f"Synthesis field '{field_name}' "
                "must be a list."
            )

    if not isinstance(
        normalized["recommendation"],
        str,
    ):
        raise TypeError(
            "Synthesis recommendation must be a string."
        )

    if not isinstance(
        normalized["recommendation_rationale"],
        str,
    ):
        raise TypeError(
            "Synthesis recommendation rationale "
            "must be a string."
        )

    confidence = normalized["confidence"]

    if not isinstance(
        confidence,
        (int, float),
    ):
        raise TypeError(
            "Synthesis confidence must be a number."
        )

    if not 0 <= confidence <= 1:
        raise ValueError(
            "Synthesis confidence must be between 0 and 1."
        )

    return normalized


def execute_synthesis_with_model(
    packet: Dict[str, Any],
    model_callable,
) -> Dict[str, Any]:
    """
    Execute cross-framework synthesis through an injected model callable.
    """

    prompt = build_synthesis_prompt(
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
            "Synthesis model callable must return a dictionary."
        )

    return validate_synthesis_result(
        model_result
    )



def build_synthesis_prompt(
    packet: Dict[str, Any],
) -> str:
    """
    Build a model-ready prompt for cross-framework synthesis.

    No model call occurs here.
    """

    framework_sections: List[str] = []

    for result in packet.get(
        "framework_results",
        [],
    ):
        framework_sections.append(
            "\n".join(
                [
                    f"FRAMEWORK: {result.get('framework', '')}",
                    f"STATUS: {result.get('status', '')}",
                    "",
                    "FINDINGS:",
                    (
                        "\n".join(
                            f"- {item}"
                            for item in result.get(
                                "findings",
                                [],
                            )
                        )
                        or "- None"
                    ),
                    "",
                    "DECISIONS:",
                    (
                        "\n".join(
                            f"- {item}"
                            for item in result.get(
                                "decisions",
                                [],
                            )
                        )
                        or "- None"
                    ),
                    "",
                    "RISKS:",
                    (
                        "\n".join(
                            f"- {item}"
                            for item in result.get(
                                "risks",
                                [],
                            )
                        )
                        or "- None"
                    ),
                    "",
                    "ASSUMPTIONS:",
                    (
                        "\n".join(
                            f"- {item}"
                            for item in result.get(
                                "assumptions",
                                [],
                            )
                        )
                        or "- None"
                    ),
                    "",
                    f"CONFIDENCE: {result.get('confidence')}",
                ]
            )
        )

    framework_context = (
        "\n\n".join(
            framework_sections
        )
        if framework_sections
        else "No framework results available."
    )

    questions = "\n".join(
        f"{index}. {question}"
        for index, question in enumerate(
            packet.get(
                "synthesis_questions",
                [],
            ),
            start=1,
        )
    )

    return "\n".join(
        [
            "You are synthesizing a consulting case after multiple analytical frameworks have been applied.",
            "",
            "BUSINESS PROBLEM",
            packet.get(
                "business_problem",
                "",
            ),
            "",
            "OBJECTIVE",
            packet.get(
                "objective",
                "",
            ),
            "",
            "FRAMEWORK RESULTS",
            framework_context,
            "",
            "SYNTHESIS QUESTIONS",
            questions,
            "",
            "SYNTHESIS RULES",
            "1. Do not treat every finding as equally important.",
            "2. Distinguish evidence from inference and assumption.",
            "3. Reconcile contradictory findings explicitly.",
            "4. Do not invent missing evidence.",
            "5. Identify the strongest evidence-supported root causes.",
            "6. Identify meaningful options rather than superficial alternatives.",
            "7. Make trade-offs explicit.",
            "8. Recommend only when the evidence supports a conclusion.",
            "9. State what remains uncertain.",
            "10. Translate the recommendation into implementation priorities and measurable KPIs.",
            "",
            "RETURN STRUCTURE",
            "",
            "key_findings:",
            "root_causes:",
            "evidence_gaps:",
            "options:",
            "trade_offs:",
            "recommendation:",
            "recommendation_rationale:",
            "risks:",
            "critical_assumptions:",
            "implementation_priorities:",
            "kpis:",
            "confidence:",
        ]
    )


def build_consulting_decision_package(
    business_problem: str,
    objective: str,
    synthesis_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert a validated synthesis result into a CEO-ready
    consulting decision package.

    This layer does not create new conclusions.
    It organizes the validated synthesis into a structured
    decision and execution package.
    """

    validated = validate_synthesis_result(
        synthesis_result
    )

    return {
        "business_problem": business_problem,
        "objective": objective,
        "recommendation": validated["recommendation"],
        "recommendation_rationale": validated[
            "recommendation_rationale"
        ],
        "key_findings": validated["key_findings"],
        "root_causes": validated["root_causes"],
        "options": validated["options"],
        "trade_offs": validated["trade_offs"],
        "evidence_gaps": validated["evidence_gaps"],
        "critical_assumptions": validated[
            "critical_assumptions"
        ],
        "risks": validated["risks"],
        "implementation_priorities": validated[
            "implementation_priorities"
        ],
        "kpis": validated["kpis"],
        "confidence": validated["confidence"],
        "decision_required": True,
        "status": "READY_FOR_CEO_REVIEW",
    }


if __name__ == "__main__":
    packet = build_synthesis_packet(
        business_problem=(
            "A company spends hundreds of employee hours "
            "every month on a repetitive workflow."
        ),
        objective=(
            "Determine whether the workflow should be "
            "automated and what approach should be used."
        ),
        framework_results=[],
    )

    prompt = build_synthesis_prompt(
        packet
    )

    print("\n" + "=" * 70)
    print(
        "LOHITH OS — SYNTHESIS ENGINE V0.1"
    )
    print("=" * 70)

    print("\nFramework count:")
    print(packet["framework_count"])

    print("\nSynthesis questions:")
    for index, question in enumerate(
        packet["synthesis_questions"],
        start=1,
    ):
        print(f"{index}. {question}")

    print("\nPrompt generated:")
    print(
        f"{len(prompt)} characters"
    )

    print(
        "\nPASS — Synthesis packet and prompt created."
    )
