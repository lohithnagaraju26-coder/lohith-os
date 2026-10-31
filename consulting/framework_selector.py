"""
LOHITH OS — Framework Selection Engine

Purpose:
    Select appropriate consulting frameworks based on:
    - problem type
    - problem structure
    - business objective
    - decision to be made

Important:
    This is a V0.1 rule-based selection engine.

    It does NOT try to solve the business problem.
    It identifies useful analytical tools that should be
    considered before deeper analysis.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class FrameworkRecommendation:
    name: str
    reason: str
    priority: str
    category: str


# -------------------------------------------------------------------
# FRAMEWORK DATABASE
# -------------------------------------------------------------------

FRAMEWORKS = {
    "SWOT": {
        "categories": ["strategy"],
        "problem_types": ["strategy"],
        "structures": ["strategic"],
        "keywords": [
            "strategy",
            "competitive advantage",
            "positioning",
            "strategic position",
        ],
    },

    "PESTEL": {
        "categories": ["strategy"],
        "problem_types": ["strategy", "market_entry"],
        "structures": ["strategic", "predictive"],
        "keywords": [
            "market entry",
            "new market",
            "regulation",
            "macro",
            "external environment",
            "country",
        ],
    },

    "Porter's Five Forces": {
        "categories": ["strategy", "market_entry"],
        "problem_types": ["strategy", "market_entry"],
        "structures": ["strategic"],
        "keywords": [
            "competition",
            "industry",
            "competitor",
            "market attractiveness",
            "competitive pressure",
        ],
    },

    "Value Chain Analysis": {
        "categories": ["strategy", "operations"],
        "problem_types": ["strategy", "operations", "profitability"],
        "structures": ["diagnostic", "strategic"],
        "keywords": [
            "value chain",
            "competitive advantage",
            "activities",
            "cost structure",
            "where value is created",
        ],
    },

    "Ansoff Matrix": {
        "categories": ["strategy", "growth"],
        "problem_types": ["strategy", "growth"],
        "structures": ["strategic"],
        "keywords": [
            "growth",
            "expansion",
            "new product",
            "new market",
            "market development",
            "diversification",
        ],
    },

    "Business Model Analysis": {
        "categories": ["strategy", "product"],
        "problem_types": ["strategy", "growth", "transformation"],
        "structures": ["strategic", "diagnostic"],
        "keywords": [
            "business model",
            "revenue model",
            "value proposition",
            "business model redesign",
        ],
    },

    "Growth Driver Tree": {
        "categories": ["growth", "profitability"],
        "problem_types": ["growth", "profitability"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "growth",
            "revenue decline",
            "revenue growth",
            "sales decline",
            "sales growth",
        ],
    },

    "TAM / SAM / SOM": {
        "categories": ["growth", "market_entry"],
        "problem_types": ["growth", "market_entry", "strategy"],
        "structures": ["strategic", "predictive"],
        "keywords": [
            "market size",
            "market opportunity",
            "tam",
            "sam",
            "som",
            "market potential",
        ],
    },

    "Growth Funnel": {
        "categories": ["growth", "marketing", "customer", "product"],
        "problem_types": ["growth", "marketing", "customer", "product"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "conversion",
            "funnel",
            "drop off",
            "acquisition",
            "activation",
            "retention",
        ],
    },

    "Cohort Analysis": {
        "categories": ["growth", "customer", "product"],
        "problem_types": ["growth", "customer", "product"],
        "structures": ["diagnostic", "predictive"],
        "keywords": [
            "retention",
            "churn",
            "cohort",
            "customer behavior",
            "customer retention",
        ],
    },

    "Profitability Tree": {
        "categories": ["profitability", "finance"],
        "problem_types": ["profitability"],
        "structures": ["diagnostic"],
        "keywords": [
            "profit",
            "profitability",
            "margin",
            "profit decline",
            "margin decline",
        ],
    },

    "Cost Tree": {
        "categories": ["profitability", "operations"],
        "problem_types": ["profitability", "operations"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "cost",
            "cost reduction",
            "expenses",
            "spending",
            "operating cost",
        ],
    },

    "Unit Economics": {
        "categories": ["profitability", "finance", "growth"],
        "problem_types": ["profitability", "growth"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "unit economics",
            "cac",
            "ltv",
            "customer economics",
            "per customer",
        ],
    },

    "Break-Even Analysis": {
        "categories": ["profitability", "finance"],
        "problem_types": ["profitability", "strategy"],
        "structures": ["predictive", "decision"],
        "keywords": [
            "break even",
            "break-even",
            "breakeven",
            "minimum sales",
            "fixed cost",
        ],
    },

    "STP": {
        "categories": ["marketing", "customer"],
        "problem_types": ["marketing", "customer", "growth"],
        "structures": ["strategic"],
        "keywords": [
            "segmentation",
            "targeting",
            "positioning",
            "target customer",
        ],
    },

    "Marketing Funnel": {
        "categories": ["marketing", "growth"],
        "problem_types": ["marketing", "growth"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "marketing funnel",
            "leads",
            "campaign",
            "conversion",
            "marketing performance",
        ],
    },

    "CAC Analysis": {
        "categories": ["marketing", "finance", "growth"],
        "problem_types": ["marketing", "growth", "profitability"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "customer acquisition cost",
            "cac",
            "acquisition cost",
            "cost to acquire",
        ],
    },

    "ROAS Analysis": {
        "categories": ["marketing", "finance"],
        "problem_types": ["marketing", "growth"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "roas",
            "advertising return",
            "ad spend",
            "advertising spend",
        ],
    },

    "Customer Segmentation": {
        "categories": ["customer", "marketing"],
        "problem_types": ["customer", "marketing", "growth"],
        "structures": ["diagnostic", "strategic"],
        "keywords": [
            "customer segment",
            "customers",
            "segments",
            "target audience",
            "customer groups",
        ],
    },

    "Customer Journey Mapping": {
        "categories": ["customer", "marketing", "operations"],
        "problem_types": ["customer", "marketing", "operations"],
        "structures": ["diagnostic"],
        "keywords": [
            "customer experience",
            "customer journey",
            "journey",
            "service experience",
            "touchpoint",
        ],
    },

    "Customer Lifetime Value": {
        "categories": ["customer", "finance", "growth"],
        "problem_types": ["customer", "growth", "profitability"],
        "structures": ["diagnostic", "predictive"],
        "keywords": [
            "lifetime value",
            "ltv",
            "customer value",
            "retention value",
        ],
    },

    "Jobs-to-be-Done": {
        "categories": ["customer", "product"],
        "problem_types": ["customer", "product", "growth"],
        "structures": ["diagnostic", "strategic"],
        "keywords": [
            "customer need",
            "job to be done",
            "why customers buy",
            "customer problem",
            "customer need",
        ],
    },

    "Process Mapping": {
        "categories": ["operations", "transformation"],
        "problem_types": ["operations", "transformation", "ai_automation"],
        "structures": ["diagnostic", "implementation"],
        "keywords": [
            "process",
            "workflow",
            "manual process",
            "process improvement",
            "workflow improvement",
        ],
    },

    "Root Cause Analysis": {
        "categories": ["operations", "quality"],
        "problem_types": [
            "operations",
            "profitability",
            "customer",
            "implementation",
        ],
        "structures": ["diagnostic"],
        "keywords": [
            "why",
            "root cause",
            "problem",
            "failure",
            "error",
            "recurring",
        ],
    },

    "Pareto Analysis": {
        "categories": ["operations", "quality"],
        "problem_types": [
            "operations",
            "customer",
            "profitability",
        ],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "largest causes",
            "major causes",
            "complaints",
            "errors",
            "defects",
        ],
    },

    "Bottleneck Analysis": {
        "categories": ["operations"],
        "problem_types": ["operations", "transformation"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "bottleneck",
            "constraint",
            "capacity",
            "slowest step",
            "throughput",
        ],
    },

    "Value Stream Mapping": {
        "categories": ["operations", "transformation"],
        "problem_types": ["operations", "transformation"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "waste",
            "cycle time",
            "value stream",
            "lean",
            "process waste",
        ],
    },

    "RICE": {
        "categories": ["product", "implementation"],
        "problem_types": ["product", "growth", "implementation"],
        "structures": ["optimization", "decision"],
        "keywords": [
            "feature prioritization",
            "product roadmap",
            "feature priority",
            "initiative priority",
        ],
    },

    "MoSCoW": {
        "categories": ["product", "implementation"],
        "problem_types": ["product", "implementation"],
        "structures": ["optimization"],
        "keywords": [
            "requirements",
            "scope",
            "must have",
            "prioritize requirements",
        ],
    },

    "Kano Model": {
        "categories": ["product", "customer"],
        "problem_types": ["product", "customer"],
        "structures": ["strategic", "optimization"],
        "keywords": [
            "customer satisfaction",
            "feature satisfaction",
            "product features",
        ],
    },

    "Capability Mapping": {
        "categories": ["organization", "strategy", "transformation"],
        "problem_types": ["organization", "strategy", "transformation"],
        "structures": ["strategic", "diagnostic"],
        "keywords": [
            "capabilities",
            "capability gap",
            "organizational capability",
            "future capabilities",
        ],
    },

    "RACI": {
        "categories": ["organization", "implementation"],
        "problem_types": ["organization", "implementation", "transformation"],
        "structures": ["implementation"],
        "keywords": [
            "ownership",
            "responsibility",
            "accountability",
            "who owns",
            "roles",
        ],
    },

    "Skills Gap Analysis": {
        "categories": ["organization", "transformation"],
        "problem_types": ["organization", "transformation"],
        "structures": ["diagnostic", "implementation"],
        "keywords": [
            "skills",
            "talent",
            "skill gap",
            "workforce",
            "capabilities",
        ],
    },

    "Build vs Buy": {
        "categories": ["technology", "ai"],
        "problem_types": ["technology", "ai_automation", "strategy"],
        "structures": ["decision"],
        "keywords": [
            "build or buy",
            "build vs buy",
            "vendor",
            "internal build",
            "purchase technology",
        ],
    },

    "Total Cost of Ownership": {
        "categories": ["technology", "finance"],
        "problem_types": ["technology", "profitability"],
        "structures": ["decision", "predictive"],
        "keywords": [
            "total cost",
            "technology cost",
            "lifecycle cost",
            "ownership cost",
        ],
    },

    "Technology Maturity Assessment": {
        "categories": ["technology", "transformation"],
        "problem_types": ["technology", "transformation"],
        "structures": ["diagnostic"],
        "keywords": [
            "technology maturity",
            "technology capability",
            "legacy systems",
            "technology environment",
        ],
    },

    "Automation Opportunity Assessment": {
        "categories": ["ai", "operations"],
        "problem_types": ["ai_automation", "operations", "transformation"],
        "structures": ["diagnostic", "optimization"],
        "keywords": [
            "automation",
            "automate",
            "manual work",
            "repetitive task",
            "workflow automation",
        ],
    },

    "AI Feasibility Assessment": {
        "categories": ["ai", "technology"],
        "problem_types": ["ai_automation", "technology"],
        "structures": ["decision"],
        "keywords": [
            "ai feasibility",
            "use ai",
            "artificial intelligence",
            "ai solution",
            "ai project",
        ],
    },

    "Human-in-the-Loop Analysis": {
        "categories": ["ai", "organization"],
        "problem_types": ["ai_automation", "transformation"],
        "structures": ["decision", "implementation"],
        "keywords": [
            "human approval",
            "human in the loop",
            "human oversight",
            "ai oversight",
        ],
    },

    "Agent Suitability Assessment": {
        "categories": ["ai", "technology"],
        "problem_types": ["ai_automation", "technology"],
        "structures": ["decision"],
        "keywords": [
            "agent",
            "ai agent",
            "agentic ai",
            "agent automation",
            "autonomous workflow",
        ],
    },

    "Revenue Decomposition": {
        "categories": ["finance", "growth"],
        "problem_types": ["growth", "profitability"],
        "structures": ["diagnostic"],
        "keywords": [
            "revenue",
            "sales",
            "revenue decline",
            "sales decline",
            "revenue growth",
        ],
    },

    "Contribution Margin": {
        "categories": ["finance", "profitability"],
        "problem_types": ["profitability", "strategy"],
        "structures": ["diagnostic", "decision"],
        "keywords": [
            "contribution margin",
            "variable cost",
            "product economics",
            "product mix",
        ],
    },

    "Scenario Analysis": {
        "categories": ["finance", "strategy"],
        "problem_types": [
            "strategy",
            "profitability",
            "market_entry",
            "transformation",
        ],
        "structures": ["predictive", "decision"],
        "keywords": [
            "scenario",
            "uncertainty",
            "future",
            "base case",
            "upside",
            "downside",
        ],
    },

    "Sensitivity Analysis": {
        "categories": ["finance", "strategy"],
        "problem_types": [
            "profitability",
            "strategy",
            "market_entry",
        ],
        "structures": ["predictive", "decision"],
        "keywords": [
            "sensitivity",
            "assumptions",
            "what if",
            "variable changes",
        ],
    },

    "Gap Analysis": {
        "categories": ["implementation", "transformation"],
        "problem_types": [
            "implementation",
            "transformation",
            "organization",
            "technology",
        ],
        "structures": ["diagnostic", "implementation"],
        "keywords": [
            "current state",
            "future state",
            "gap",
            "target state",
        ],
    },

    "Implementation Roadmap": {
        "categories": ["implementation", "transformation"],
        "problem_types": ["implementation", "transformation"],
        "structures": ["implementation"],
        "keywords": [
            "roadmap",
            "implementation",
            "execution",
            "rollout",
            "milestones",
        ],
    },

    "Decision Matrix": {
        "categories": ["strategy", "implementation"],
        "problem_types": [
            "strategy",
            "market_entry",
            "technology",
            "implementation",
        ],
        "structures": ["decision"],
        "keywords": [
            "which option",
            "which should",
            "choose",
            "alternative",
            "options",
        ],
    },

    "Benchmarking": {
        "categories": ["strategy", "operations", "finance"],
        "problem_types": [
            "strategy",
            "operations",
            "profitability",
        ],
        "structures": ["diagnostic", "predictive"],
        "keywords": [
            "benchmark",
            "competitor performance",
            "industry standard",
            "best performer",
        ],
    },
}


# -------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Normalize text for simple matching.
    """
    return " ".join(text.lower().strip().split())


def keyword_score(problem_text: str, keywords: List[str]) -> int:
    """
    Count how many framework-specific keywords appear
    in the problem description.
    """
    normalized = normalize_text(problem_text)

    score = 0

    for keyword in keywords:
        if keyword.lower() in normalized:
            score += 1

    return score


def framework_score(
    framework_data: dict,
    problem_type: str | None,
    problem_structure: str | None,
    problem_text: str,
) -> int:
    """
    Calculate a simple rule-based score.

    Scoring:
        +5  primary problem type matches
        +3  problem structure matches
        +2  keyword match
    """

    score = 0

    if problem_type:
        if problem_type.lower() in framework_data["problem_types"]:
            score += 5

    if problem_structure:
        if problem_structure.lower() in framework_data["structures"]:
            score += 3

    score += min(
        keyword_score(problem_text, framework_data["keywords"]) * 2,
        4,
    )

    return score


# -------------------------------------------------------------------
# MAIN SELECTION FUNCTION
# -------------------------------------------------------------------

def select_frameworks(
    problem_text: str,
    problem_type: str | None = None,
    problem_structure: str | None = None,
    limit: int = 5,
) -> List[FrameworkRecommendation]:
    """
    Select the most relevant frameworks.

    Parameters:
        problem_text:
            Description of the business problem.

        problem_type:
            Primary problem classification.

        problem_structure:
            Diagnostic, predictive, strategic, optimization,
            decision, implementation, or transformation.

        limit:
            Maximum number of frameworks to return.
    """

    recommendations = []

    for name, framework_data in FRAMEWORKS.items():

        score = framework_score(
            framework_data,
            problem_type,
            problem_structure,
            problem_text,
        )

        if score <= 0:
            continue

        if score >= 9:
            priority = "High"
        elif score >= 6:
            priority = "Medium"
        else:
            priority = "Low"

        reason_parts = []

        if problem_type and problem_type.lower() in framework_data["problem_types"]:
            reason_parts.append(
                f"matches the {problem_type} problem type"
            )

        if (
            problem_structure
            and problem_structure.lower() in framework_data["structures"]
        ):
            reason_parts.append(
                f"fits the {problem_structure} problem structure"
            )

        if keyword_score(problem_text, framework_data["keywords"]) > 0:
            reason_parts.append(
                "matches important signals in the problem description"
            )

        reason = "; ".join(reason_parts)

        recommendations.append(
            (
                score,
                FrameworkRecommendation(
                    name=name,
                    reason=reason,
                    priority=priority,
                    category=framework_data["categories"][0],
                ),
            )
        )

    recommendations.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        recommendation
        for _, recommendation in recommendations[:limit]
    ]


# -------------------------------------------------------------------
# DISPLAY FUNCTION
# -------------------------------------------------------------------

def print_framework_recommendations(
    problem_text: str,
    problem_type: str | None = None,
    problem_structure: str | None = None,
    limit: int = 5,
):
    """
    Print framework recommendations in a human-readable format.
    """

    recommendations = select_frameworks(
        problem_text=problem_text,
        problem_type=problem_type,
        problem_structure=problem_structure,
        limit=limit,
    )

    print()
    print("LOHITH OS — FRAMEWORK SELECTION")
    print("=" * 50)
    print()
    print(f"Problem: {problem_text}")

    if problem_type:
        print(f"Problem type: {problem_type}")

    if problem_structure:
        print(f"Problem structure: {problem_structure}")

    print()

    if not recommendations:
        print("No strong framework matches found.")
        print("LOHITH OS should gather more information before selecting a framework.")
        return

    print("Recommended frameworks:")
    print()

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        print(f"{index}. {recommendation.name}")
        print(f"   Category: {recommendation.category}")
        print(f"   Priority: {recommendation.priority}")
        print(f"   Reason: {recommendation.reason}")
        print()


# -------------------------------------------------------------------
# TESTS
# -------------------------------------------------------------------

def run_tests():
    """
    Basic tests for the framework selection engine.
    """

    print("LOHITH OS — FRAMEWORK SELECTION TESTS")
    print("=" * 50)
    print()

    test_cases = [
        {
            "problem": "Revenue has fallen by 20% and management wants to understand why.",
            "problem_type": "growth",
            "problem_structure": "diagnostic",
        },
        {
            "problem": "Should the company enter a new country?",
            "problem_type": "market_entry",
            "problem_structure": "decision",
        },
        {
            "problem": "The company wants to automate a repetitive manual workflow using AI.",
            "problem_type": "ai_automation",
            "problem_structure": "decision",
        },
        {
            "problem": "Customers are leaving after the first three months.",
            "problem_type": "customer",
            "problem_structure": "diagnostic",
        },
    ]

    for index, test_case in enumerate(test_cases, start=1):

        print(f"TEST {index}")
        print("-" * 50)

        print_framework_recommendations(
            problem_text=test_case["problem"],
            problem_type=test_case["problem_type"],
            problem_structure=test_case["problem_structure"],
            limit=3,
        )

        print()


if __name__ == "__main__":
    run_tests()