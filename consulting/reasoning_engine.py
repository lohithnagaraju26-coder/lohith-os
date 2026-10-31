"""
LOHITH OS — CONSULTING REASONING ENGINE V2

Purpose:
    Provide a structured consulting reasoning layer for LOHITH OS.

Core flow:

    BUSINESS PROBLEM
          ↓
       OBJECTIVE
          ↓
    CLASSIFICATION
          ↓
      HYPOTHESES
          ↓
     KEY QUESTIONS
          ↓
   FRAMEWORK SELECTION
          ↓
 FRAMEWORK INTELLIGENCE
          ↓
      EVIDENCE
          ↓
       ANALYSIS
          ↓
    ROOT CAUSE
          ↓
       OPTIONS
          ↓
   RECOMMENDATION
          ↓
    IMPLEMENTATION
          ↓
        KPIs
          ↓
      LEARNING

Important:
    This engine does not attempt to hard-code all consulting judgment.

    Instead, it combines:
        1. Problem-solving methodology
        2. Problem classification
        3. Framework selection
        4. Structured framework knowledge
        5. Evidence requirements
        6. Framework sequencing
        7. Hypothesis-driven reasoning

    The model layer will eventually provide deeper judgment,
    interpretation, synthesis, and recommendation.
"""

from __future__ import annotations

from typing import Any, Dict, List

from consulting.framework_selector import select_frameworks
from consulting.framework_knowledge import (
    get_framework,
    load_all_frameworks,
)
from consulting.framework_executor import (
    prepare_framework_execution,
    execution_packet,
    build_framework_execution_plan,
)


# ============================================================
# CONSULTING REASONING PRINCIPLES
# ============================================================

REASONING_PRINCIPLES = [
    "Start with the business decision, not the framework.",
    "Separate symptoms from root causes.",
    "Use hypotheses to focus analysis.",
    "Seek evidence that can confirm or disprove hypotheses.",
    "Use MECE as a quality-control principle where appropriate.",
    "Choose frameworks because they answer specific questions.",
    "Do not force a framework onto a problem.",
    "Use multiple frameworks only when each adds distinct analytical value.",
    "Prefer evidence over assumptions.",
    "Distinguish correlation from causation.",
    "Quantify impact whenever practical.",
    "Make trade-offs explicit.",
    "Recommendations must be actionable.",
    "Implementation must have owners, timing, dependencies, and KPIs.",
    "Capture learning so future decisions improve.",
]


# ============================================================
# GENERIC HYPOTHESIS GENERATION
# ============================================================

def generate_hypotheses(problem_type: str) -> List[str]:
    hypotheses = {
        "strategy": [
            "The current strategic position may be unattractive.",
            "The company may lack a sustainable competitive advantage.",
            "The current business model may be misaligned with market conditions.",
            "Resources may be allocated toward lower-value opportunities.",
            "The strategic choice may involve an underestimated trade-off.",
        ],
        "growth": [
            "Customer acquisition may be insufficient.",
            "Customer conversion may be weak.",
            "Customer retention may be declining.",
            "Average revenue per customer may be too low.",
            "The company may be targeting the wrong customer segments.",
        ],
        "profitability": [
            "Revenue may be insufficient.",
            "Costs may be too high.",
            "Unit economics may be unattractive.",
            "Pricing may not reflect customer value.",
            "Product or customer mix may be reducing margins.",
        ],
        "market_entry": [
            "The target market may not be sufficiently attractive.",
            "Customer demand may be weaker than expected.",
            "Competitive intensity may be too high.",
            "The company may lack the capabilities required to compete.",
            "The entry economics may not justify the investment.",
        ],
        "ai_automation": [
            "The workflow may contain repetitive manual work.",
            "The process may be suitable for partial automation.",
            "Poor process design may be the real problem rather than lack of AI.",
            "Data quality may limit automation.",
            "Human judgment may still be required at critical decision points.",
        ],
        "operations": [
            "The process may contain unnecessary steps.",
            "A bottleneck may be constraining throughput.",
            "Errors or rework may be creating hidden costs.",
            "Resources may be poorly allocated.",
            "The process may lack appropriate controls.",
        ],
        "customer": [
            "Different customer segments may have different needs.",
            "Customer experience may be deteriorating at specific journey stages.",
            "The product may not solve the highest-priority customer problem.",
            "Retention may be affected by unmet expectations.",
            "Customer value may differ significantly across segments.",
        ],
        "marketing": [
            "The company may be targeting the wrong audience.",
            "The value proposition may not be sufficiently differentiated.",
            "Marketing channels may be inefficient.",
            "Conversion may be weak at one or more funnel stages.",
            "Marketing spend may not be allocated toward the highest-return channels.",
        ],
        "product": [
            "The product may not solve a sufficiently important customer problem.",
            "Users may experience friction in the product journey.",
            "Feature priorities may not reflect customer value.",
            "Adoption may be constrained by poor onboarding.",
            "The product may lack differentiation.",
        ],
        "technology": [
            "The current technology may no longer support business requirements.",
            "The organization may be over-investing in technology.",
            "A build solution may not justify its cost versus buying.",
            "Integration complexity may be underestimated.",
            "Technology capability may be constraining business performance.",
        ],
    }

    return hypotheses.get(
        problem_type,
        [
            "The stated problem may have multiple underlying causes.",
            "The current understanding may be incomplete.",
            "The root cause may differ from the visible symptom.",
            "Additional evidence may materially change the conclusion.",
            "The problem may require multiple interventions rather than a single solution.",
        ],
    )


# ============================================================
# KEY QUESTIONS
# ============================================================

def generate_key_questions(problem: str, objective: str) -> List[str]:
    return [
        f"What exactly is happening with: {problem}?",
        "How large is the problem?",
        "When did the problem begin?",
        "Is the problem getting better or worse?",
        "Who or what is most affected?",
        "What evidence currently supports the problem?",
        "What evidence contradicts the current understanding?",
        "What are the most likely root causes?",
        "What alternative explanations should be considered?",
        "What data is required to test the hypotheses?",
        f"What decision must ultimately be made to achieve: {objective}?",
    ]


# ============================================================
# GENERIC EVIDENCE REQUIREMENTS
# ============================================================

def generate_evidence_requirements(problem_type: str) -> List[str]:
    evidence = {
        "growth": [
            "Revenue trends",
            "Customer acquisition",
            "Conversion rates",
            "Retention",
            "Average revenue per customer",
            "Channel performance",
        ],
        "ai_automation": [
            "Current workflow",
            "Task frequency",
            "Time spent",
            "Error rate",
            "Decision complexity",
            "Data availability",
            "Human intervention points",
            "Automation cost",
        ],
        "market_entry": [
            "Market size",
            "Market growth",
            "Customer demand",
            "Competitive intensity",
            "Regulatory environment",
            "Entry investment",
            "Expected economics",
        ],
        "profitability": [
            "Revenue",
            "Variable costs",
            "Fixed costs",
            "Contribution margin",
            "Customer economics",
            "Product economics",
        ],
        "operations": [
            "Process steps",
            "Cycle time",
            "Throughput",
            "Error rates",
            "Resource utilization",
            "Bottlenecks",
        ],
        "customer": [
            "Customer segments",
            "Customer feedback",
            "Retention",
            "Churn",
            "Customer journey data",
            "Customer value",
        ],
        "marketing": [
            "Audience data",
            "Channel performance",
            "Conversion rates",
            "CAC",
            "ROAS",
            "Campaign performance",
        ],
        "product": [
            "Usage data",
            "Activation",
            "Retention",
            "Feature adoption",
            "Customer feedback",
            "Conversion",
        ],
    }

    return evidence.get(
        problem_type,
        [
            "Current-state data",
            "Historical trends",
            "Customer or stakeholder evidence",
            "Financial impact",
            "Operational evidence",
            "External market evidence",
        ],
    )


# ============================================================
# ROOT CAUSE QUESTIONS
# ============================================================

def generate_root_cause_questions() -> List[str]:
    return [
        "What is the observable symptom?",
        "What directly causes the symptom?",
        "What causes those direct causes?",
        "Which causes are controllable?",
        "Which causes are external?",
        "Which causes have the strongest evidence?",
        "Which causes have the largest business impact?",
        "What would need to be true for this explanation to be correct?",
        "What evidence would disprove this explanation?",
    ]


# ============================================================
# ASSUMPTION CHECKS
# ============================================================

def generate_assumption_checks() -> List[str]:
    return [
        "What are we assuming?",
        "Which assumptions are critical?",
        "Which assumptions are untested?",
        "Could the opposite explanation be true?",
        "What evidence would change our conclusion?",
        "Are we confusing correlation with causation?",
        "Are we using outdated information?",
        "Are we optimizing the wrong metric?",
        "Could solving this problem create another problem?",
    ]


# ============================================================
# OPTION QUESTIONS
# ============================================================

def generate_option_questions() -> List[str]:
    return [
        "What are the realistic options?",
        "What is the minimum viable intervention?",
        "What is the highest-impact option?",
        "What is the lowest-risk option?",
        "What is the fastest option?",
        "What is the most scalable option?",
        "What are the costs of each option?",
        "What are the risks of each option?",
        "What capabilities are required?",
        "What happens if we do nothing?",
    ]


# ============================================================
# RECOMMENDATION QUESTIONS
# ============================================================

def generate_recommendation_questions() -> List[str]:
    return [
        "What should the business do?",
        "Why is this the best option?",
        "What evidence supports it?",
        "What alternatives were rejected?",
        "What are the major trade-offs?",
        "What are the major risks?",
        "What assumptions must remain true?",
        "What should happen first?",
    ]


# ============================================================
# IMPLEMENTATION QUESTIONS
# ============================================================

def generate_implementation_questions() -> List[str]:
    return [
        "What needs to happen first?",
        "What initiatives are required?",
        "Who should own each initiative?",
        "What resources are required?",
        "What dependencies exist?",
        "What could prevent execution?",
        "What should happen in the first 30 days?",
        "What should happen in 60–90 days?",
        "How will progress be measured?",
    ]


# ============================================================
# KPI QUESTIONS
# ============================================================

def generate_kpi_questions() -> List[str]:
    return [
        "What is the primary business outcome?",
        "Which KPI directly measures that outcome?",
        "Which leading indicators predict success?",
        "Which lagging indicators confirm success?",
        "What is the baseline?",
        "What is the target?",
        "How frequently should the KPI be monitored?",
        "What threshold should trigger intervention?",
    ]


# ============================================================
# FRAMEWORK INTELLIGENCE
# ============================================================

def build_framework_intelligence(
    selected_frameworks: List[Any],
) -> List[Dict[str, Any]]:
    """
    Retrieve the structured knowledge associated with each selected
    framework.

    This is the bridge between:
        Framework Selection
    and:
        Actual Consulting Reasoning
    """

    intelligence: List[Dict[str, Any]] = []

    for recommendation in selected_frameworks:
        framework_name = getattr(recommendation, "name", None)

        if not framework_name:
            continue

        framework = get_framework(framework_name)

        if framework is None:
            intelligence.append(
                {
                    "name": framework_name,
                    "knowledge_available": False,
                    "selection_reason": getattr(
                        recommendation,
                        "reason",
                        "",
                    ),
                    "priority": getattr(
                        recommendation,
                        "priority",
                        "",
                    ),
                    "category": getattr(
                        recommendation,
                        "category",
                        "",
                    ),
                }
            )
            continue

        intelligence.append(
            {
                "name": framework.name,
                "category": framework.category,
                "priority": getattr(
                    recommendation,
                    "priority",
                    "",
                ),
                "selection_reason": getattr(
                    recommendation,
                    "reason",
                    "",
                ),
                "knowledge_available": True,
                "purpose": framework.purpose,
                "core_question": framework.core_question,
                "use_when": framework.use_when,
                "do_not_use_when": framework.do_not_use_when,
                "problem_types": framework.problem_types,
                "decision_types": framework.decision_types,
                "key_questions": framework.key_questions,
                "required_inputs": framework.required_inputs,
                "analysis_process": framework.analysis_process,
                "expected_output": framework.expected_output,
                "interpretation": framework.interpretation,
                "limitations": framework.limitations,
                "common_mistakes": framework.common_mistakes,
                "compatible_frameworks": framework.compatible_frameworks,
                "framework_sequence": framework.framework_sequence,
                "decision_impact": framework.decision_impact,
                "consulting_judgment": framework.consulting_judgment,
                "framework_reasoning_rule": framework.framework_reasoning_rule,
                "framework_chain": framework.framework_chain,
                "framework_combination_rules": framework.framework_combination_rules,
                "framework_selection_hierarchy": framework.framework_selection_hierarchy,
                "quality_standard": framework.quality_standard,
            }
        )

    return intelligence


# ============================================================
# FRAMEWORK-SPECIFIC EVIDENCE
# ============================================================

def build_framework_evidence_requirements(
    framework_intelligence: List[Dict[str, Any]],
) -> List[str]:
    """
    Aggregate evidence requirements from selected frameworks.

    Duplicates are removed while preserving order.
    """

    evidence: List[str] = []

    for framework in framework_intelligence:
        for item in framework.get("required_inputs", []):
            if item not in evidence:
                evidence.append(item)

    return evidence


# ============================================================
# FRAMEWORK-SPECIFIC QUESTIONS
# ============================================================

def build_framework_questions(
    framework_intelligence: List[Dict[str, Any]],
) -> List[str]:
    """
    Aggregate framework-specific analytical questions.

    Each question retains the framework that generated it.
    """

    questions: List[str] = []

    for framework in framework_intelligence:
        name = framework.get("name", "Unknown Framework")

        for question in framework.get("key_questions", []):
            item = f"[{name}] {question}"

            if item not in questions:
                questions.append(item)

    return questions


# ============================================================
# FRAMEWORK SEQUENCE
# ============================================================

def build_framework_sequence(
    framework_intelligence: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Build a relationship-aware analytical sequence from framework metadata.

    The framework knowledge layer can specify:
        - Before: Framework A, Framework B
        - After: Framework C, Framework D

    Only relationships between frameworks actually selected for the current
    problem are applied. If a relationship is unavailable, the original
    selector order is preserved as the fallback.
    """

    if not framework_intelligence:
        return []

    names = [
        framework.get("name")
        for framework in framework_intelligence
        if framework.get("name")
    ]

    original_index = {
        name: index
        for index, name in enumerate(names)
    }

    # Graph: A -> B means A should be analyzed before B.
    edges: Dict[str, set[str]] = {
        name: set()
        for name in names
    }

    indegree: Dict[str, int] = {
        name: 0
        for name in names
    }

    selected_names = set(names)

    def parse_relationships(value: Any, prefix: str) -> List[str]:
        if isinstance(value, str):
            items = value.splitlines()
        elif isinstance(value, list):
            items = value
        else:
            return []

        matches: List[str] = []

        for item in items:
            if not isinstance(item, str):
                continue

            cleaned = item.strip()

            if cleaned.startswith("-"):
                cleaned = cleaned[1:].strip()

            if not cleaned.lower().startswith(prefix.lower()):
                continue

            if ":" not in cleaned:
                continue

            remainder = cleaned.split(":", 1)[1].strip()

            for candidate in remainder.split(","):
                candidate = candidate.strip()

                if candidate and candidate in selected_names:
                    matches.append(candidate)

        return matches

    # Build ordering constraints from framework knowledge.
    for framework in framework_intelligence:
        current = framework.get("name")

        if not current or current not in selected_names:
            continue

        sequence_rules = framework.get("framework_sequence", [])

        before_names = parse_relationships(
            sequence_rules,
            "Before",
        )

        after_names = parse_relationships(
            sequence_rules,
            "After",
        )

        # "Before: A, B" means A/B must come BEFORE the current framework.
        # Therefore: A -> current.
        for target in before_names:
            if target != current and current not in edges[target]:
                edges[target].add(current)
                indegree[current] += 1

        # "After: A, B" means the current framework must come BEFORE A/B.
        # Therefore: current -> A/B.
        for target in after_names:
            if target != current and target not in edges[current]:
                edges[current].add(target)
                indegree[target] += 1

    # Topological ordering with the selector's original ranking as tie-breaker.
    ordered_names: List[str] = []
    remaining = set(selected_names)

    while remaining:
        available = [
            name
            for name in remaining
            if indegree[name] == 0
        ]

        if not available:
            # A cycle exists. Preserve the original selector order for the
            # remaining frameworks rather than failing the analysis.
            available = sorted(
                remaining,
                key=lambda name: original_index[name],
            )

            for name in available:
                ordered_names.append(name)

            break

        available.sort(
            key=lambda name: original_index[name]
        )

        next_name = available[0]
        remaining.remove(next_name)
        ordered_names.append(next_name)

        for target in edges[next_name]:
            indegree[target] -= 1

    framework_by_name = {
        framework.get("name"): framework
        for framework in framework_intelligence
    }

    sequence: List[Dict[str, Any]] = []

    for index, name in enumerate(ordered_names, start=1):
        framework = framework_by_name[name]

        sequence.append(
            {
                "step": index,
                "framework": name,
                "why_now": framework.get(
                    "selection_reason",
                    "Selected as relevant to the problem.",
                ),
                "purpose": framework.get("purpose", ""),
                "core_question": framework.get(
                    "core_question",
                    "",
                ),
                "sequence_basis": framework.get(
                    "framework_sequence",
                    [],
                ),
            }
        )

    return sequence


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze_business_problem(
    problem: str,
    objective: str,
    problem_type: str,
    problem_structure: str,
) -> Dict[str, Any]:
    """
    Create a structured consulting analysis.

    Important:
        This function creates the analytical scaffold.

        It does not pretend that a real business recommendation
        can be produced without evidence.

        Future model/tool layers will perform:
            - evidence collection
            - quantitative analysis
            - hypothesis testing
            - interpretation
            - synthesis
            - recommendation
    """

    # --------------------------------------------------------
    # 1. Framework selection
    # --------------------------------------------------------

    selected_frameworks = select_frameworks(
        problem_text=problem,
        problem_type=problem_type,
        problem_structure=problem_structure,
    )

    # --------------------------------------------------------
    # 2. Retrieve framework knowledge
    # --------------------------------------------------------

    framework_intelligence = build_framework_intelligence(
        selected_frameworks
    )

    # --------------------------------------------------------
    # 3. Framework-specific evidence
    # --------------------------------------------------------

    generic_evidence = generate_evidence_requirements(
        problem_type
    )

    framework_evidence = build_framework_evidence_requirements(
        framework_intelligence
    )

    combined_evidence: List[str] = []

    for item in generic_evidence + framework_evidence:
        if item not in combined_evidence:
            combined_evidence.append(item)

    # --------------------------------------------------------
    # 4. Framework-specific questions
    # --------------------------------------------------------

    framework_questions = build_framework_questions(
        framework_intelligence
    )

    # --------------------------------------------------------
    # 5. Framework sequence
    # --------------------------------------------------------

    framework_sequence = build_framework_sequence(
        framework_intelligence
    )

    # --------------------------------------------------------
    # 6. Build executable framework plan
    # --------------------------------------------------------

    framework_execution_plan = build_framework_execution_plan(
        framework_sequence=framework_sequence,
        framework_intelligence=framework_intelligence,
        business_problem=problem,
        objective=objective,
    )

    # --------------------------------------------------------
    # 7. Return structured consulting case
    # --------------------------------------------------------

    return {
        "problem": problem,
        "objective": objective,
        "problem_type": problem_type,
        "problem_structure": problem_structure,

        "reasoning_principles": REASONING_PRINCIPLES,

        "reasoning_sequence": [
            "Understand the problem",
            "Clarify the objective",
            "Structure the problem",
            "Generate hypotheses",
            "Identify evidence requirements",
            "Select appropriate frameworks",
            "Understand why each framework fits",
            "Apply frameworks",
            "Analyze evidence",
            "Test hypotheses",
            "Challenge assumptions",
            "Identify root causes",
            "Generate strategic options",
            "Evaluate trade-offs",
            "Recommend action",
            "Create implementation plan",
            "Define KPIs",
            "Monitor results",
            "Capture learning",
        ],

        "hypotheses": generate_hypotheses(
            problem_type
        ),

        "key_questions": generate_key_questions(
            problem,
            objective,
        ),

        "recommended_frameworks": selected_frameworks,

        "framework_intelligence": framework_intelligence,

        "framework_questions": framework_questions,

        "framework_evidence_requirements": framework_evidence,

        "framework_sequence": framework_sequence,

        "framework_execution_plan": framework_execution_plan,

        "evidence_requirements": combined_evidence,

        "root_cause_questions": generate_root_cause_questions(),

        "assumption_checks": generate_assumption_checks(),

        "option_questions": generate_option_questions(),

        "recommendation_questions": (
            generate_recommendation_questions()
        ),

        "implementation_questions": (
            generate_implementation_questions()
        ),

        "kpi_questions": generate_kpi_questions(),

        "status": (
            "Consulting analysis scaffold created. "
            "Evidence and deeper reasoning required."
        ),
    }


# ============================================================
# PRINTING
# ============================================================

def print_analysis(
    analysis: Dict[str, Any],
) -> None:

    print("\n" + "=" * 70)
    print("LOHITH OS — CONSULTING REASONING ENGINE V2")
    print("=" * 70)

    print("\nPROBLEM")
    print("-" * 70)
    print(analysis["problem"])

    print("\nOBJECTIVE")
    print("-" * 70)
    print(analysis["objective"])

    print("\nCLASSIFICATION")
    print("-" * 70)
    print(f"Problem Type: {analysis['problem_type']}")
    print(
        f"Problem Structure: "
        f"{analysis['problem_structure']}"
    )

    print("\nREASONING PRINCIPLES")
    print("-" * 70)

    for principle in analysis["reasoning_principles"]:
        print(f"- {principle}")

    print("\nREASONING SEQUENCE")
    print("-" * 70)

    for index, step in enumerate(
        analysis["reasoning_sequence"],
        start=1,
    ):
        print(f"{index}. {step}")

    print("\nSTARTING HYPOTHESES")
    print("-" * 70)

    for hypothesis in analysis["hypotheses"]:
        print(f"- {hypothesis}")

    print("\nKEY QUESTIONS")
    print("-" * 70)

    for question in analysis["key_questions"]:
        print(f"- {question}")

    print("\nRECOMMENDED FRAMEWORKS")
    print("-" * 70)

    for framework in analysis["recommended_frameworks"]:
        print(
            f"- {framework.name} "
            f"[{framework.priority}] "
            f"({framework.category})"
        )
        print(
            f"  Why: {framework.reason}"
        )

    print("\nFRAMEWORK INTELLIGENCE")
    print("-" * 70)

    for framework in analysis["framework_intelligence"]:

        print(
            f"\n### {framework['name']}"
        )

        print(
            f"Knowledge Available: "
            f"{framework.get('knowledge_available')}"
        )

        if not framework.get("knowledge_available"):
            continue

        print(
            f"Category: "
            f"{framework.get('category', '')}"
        )

        print(
            f"Priority: "
            f"{framework.get('priority', '')}"
        )

        print(
            f"Purpose: "
            f"{framework.get('purpose', '')}"
        )

        print(
            f"Core Question: "
            f"{framework.get('core_question', '')}"
        )

        print("Use When:")

        for item in framework.get(
            "use_when",
            [],
        ):
            print(f"  - {item}")

        print("Do NOT Use When:")

        for item in framework.get(
            "do_not_use_when",
            [],
        ):
            print(f"  - {item}")

        print("Required Inputs:")

        for item in framework.get(
            "required_inputs",
            [],
        ):
            print(f"  - {item}")

        print("Key Questions:")

        for item in framework.get(
            "key_questions",
            [],
        ):
            print(f"  - {item}")

        print("Expected Output:")

        for item in framework.get(
            "expected_output",
            [],
        ):
            print(f"  - {item}")

        print("Interpretation:")

        for item in framework.get(
            "interpretation",
            [],
        ):
            print(f"  - {item}")

        print("Compatible Frameworks:")

        for item in framework.get(
            "compatible_frameworks",
            [],
        ):
            print(f"  - {item}")

        print("Framework Sequence:")

        for item in framework.get(
            "framework_sequence",
            [],
        ):
            print(f"  - {item}")

        print("Consulting Judgment:")

        for item in framework.get(
            "consulting_judgment",
            [],
        ):
            print(f"  - {item}")

    print("\nFRAMEWORK QUESTIONS")
    print("-" * 70)

    for question in analysis["framework_questions"]:
        print(f"- {question}")

    print("\nFRAMEWORK EVIDENCE REQUIREMENTS")
    print("-" * 70)

    for item in analysis[
        "framework_evidence_requirements"
    ]:
        print(f"- {item}")

    print("\nFRAMEWORK SEQUENCE")
    print("-" * 70)

    for step in analysis["framework_sequence"]:
        print(
            f"{step['step']}. "
            f"{step['framework']}"
        )

        print(
            f"   Why now: "
            f"{step['why_now']}"
        )

        print(
            f"   Purpose: "
            f"{step['purpose']}"
        )

        print(
            f"   Core question: "
            f"{step['core_question']}"
        )

    print("\nEVIDENCE REQUIRED")
    print("-" * 70)

    for item in analysis["evidence_requirements"]:
        print(f"- {item}")

    print("\nROOT-CAUSE CHECK")
    print("-" * 70)

    for item in analysis["root_cause_questions"]:
        print(f"- {item}")

    print("\nASSUMPTION CHECK")
    print("-" * 70)

    for item in analysis["assumption_checks"]:
        print(f"- {item}")

    print("\nOPTION GENERATION")
    print("-" * 70)

    for item in analysis["option_questions"]:
        print(f"- {item}")

    print("\nRECOMMENDATION")
    print("-" * 70)

    for item in analysis["recommendation_questions"]:
        print(f"- {item}")

    print("\nIMPLEMENTATION")
    print("-" * 70)

    for item in analysis["implementation_questions"]:
        print(f"- {item}")

    print("\nKPI / MEASUREMENT")
    print("-" * 70)

    for item in analysis["kpi_questions"]:
        print(f"- {item}")

    print("\nSTATUS")
    print("-" * 70)
    print(analysis["status"])

    print("\n" + "=" * 70)


# ============================================================
# TESTS
# ============================================================

def run_tests() -> None:

    print("\n" + "=" * 70)
    print("LOHITH OS — CONSULTING REASONING ENGINE V2 TESTS")
    print("=" * 70)

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    print("\nTEST 1: Revenue Decline")
    print("-" * 70)

    analysis = analyze_business_problem(
        problem=(
            "Revenue has declined by 20% "
            "over the last year."
        ),
        objective=(
            "Identify the major causes "
            "of the revenue decline."
        ),
        problem_type="growth",
        problem_structure="diagnostic",
    )

    print_analysis(analysis)

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    print("\nTEST 2: AI Automation")
    print("-" * 70)

    analysis = analyze_business_problem(
        problem=(
            "A company spends hundreds of "
            "employee hours every month "
            "on a repetitive workflow."
        ),
        objective=(
            "Determine whether the workflow "
            "should be automated and what "
            "approach should be used."
        ),
        problem_type="ai_automation",
        problem_structure="decision",
    )

    print_analysis(analysis)

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    print("\nTEST 3: Market Entry")
    print("-" * 70)

    analysis = analyze_business_problem(
        problem=(
            "A company is considering "
            "entering a new country."
        ),
        objective=(
            "Determine whether entering the "
            "market is attractive and "
            "strategically justified."
        ),
        problem_type="market_entry",
        problem_structure="decision",
    )

    print_analysis(analysis)

    # --------------------------------------------------------
    # TEST 4 — KNOWLEDGE LAYER
    # --------------------------------------------------------

    print("\nTEST 4: Framework Knowledge Layer")
    print("-" * 70)

    frameworks = load_all_frameworks()

    print(
        f"Frameworks discovered: "
        f"{len(frameworks)}"
    )

    for framework in frameworks:
        print(
            f"- {framework.name} "
            f"| {framework.category}"
        )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    print("\nVALIDATION")
    print("-" * 70)

    revenue = analyze_business_problem(
        problem="Revenue declined.",
        objective="Identify causes.",
        problem_type="growth",
        problem_structure="diagnostic",
    )

    if not revenue["framework_intelligence"]:
        raise AssertionError(
            "Framework intelligence is empty."
        )

    if not revenue[
        "framework_evidence_requirements"
    ]:
        raise AssertionError(
            "Framework evidence requirements are empty."
        )

    if not revenue["framework_questions"]:
        raise AssertionError(
            "Framework questions are empty."
        )

    if not revenue["framework_sequence"]:
        raise AssertionError(
            "Framework sequence is empty."
        )

    print(
        "PASS — Framework Knowledge Layer "
        "is connected to the Reasoning Engine."
    )

    print("\n" + "=" * 70)
    print("ALL REASONING ENGINE V2 TESTS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
