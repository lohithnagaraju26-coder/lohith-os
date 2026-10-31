"""
LOHITH OS — Framework Knowledge Layer

Loads consulting framework definitions from Markdown files
and converts them into structured framework knowledge.

Architecture:

    Markdown Framework Files
            ↓
    Framework Knowledge Loader
            ↓
    Structured Framework Objects
            ↓
    Reasoning Engine

The loader is responsible for KNOWLEDGE RETRIEVAL.

It does not decide which framework should be used.
That remains the responsibility of the reasoning layer.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FRAMEWORKS_DIR = PROJECT_ROOT / "consulting" / "frameworks"

SUPPORTING_FILES = {
    "framework_library.md",
    "framework_schema.md",
}


# ---------------------------------------------------------------------------
# FRAMEWORK METADATA
# ---------------------------------------------------------------------------

@dataclass
class FrameworkKnowledge:
    """
    Structured representation of a consulting framework.
    """

    name: str
    category: str = ""
    purpose: str = ""
    core_question: str = ""

    use_when: List[str] = field(default_factory=list)
    do_not_use_when: List[str] = field(default_factory=list)

    problem_types: List[str] = field(default_factory=list)
    decision_types: List[str] = field(default_factory=list)

    key_questions: List[str] = field(default_factory=list)
    required_inputs: List[str] = field(default_factory=list)

    analysis_process: str = ""
    expected_output: str = ""
    interpretation: str = ""
    limitations: str = ""

    common_mistakes: List[str] = field(default_factory=list)
    compatible_frameworks: List[str] = field(default_factory=list)

    framework_sequence: str = ""
    decision_impact: str = ""
    consulting_judgment: str = ""

    framework_reasoning_rule: str = ""
    framework_chain: str = ""
    framework_combination_rules: str = ""

    framework_selection_hierarchy: str = ""

    # Explicit machine-readable framework-selection metadata.
    # These fields make framework specialization and sequencing
    # available to the reasoning engine without hardcoded
    # framework-specific routing rules.
    primary_question: str = ""
    trigger_conditions: List[str] = field(default_factory=list)
    exclusion_conditions: List[str] = field(default_factory=list)
    selection_role: str = ""
    prerequisite_frameworks: List[str] = field(default_factory=list)
    compatible_frameworks: List[str] = field(default_factory=list)
    downstream_frameworks: List[str] = field(default_factory=list)

    quality_standard: str = ""

    source_path: str = ""
    raw_content: str = ""

    def to_dict(self) -> Dict:
        """
        Convert the framework into a serializable dictionary.
        """

        return {
            "name": self.name,
            "category": self.category,
            "purpose": self.purpose,
            "core_question": self.core_question,
            "use_when": self.use_when,
            "do_not_use_when": self.do_not_use_when,
            "problem_types": self.problem_types,
            "decision_types": self.decision_types,
            "key_questions": self.key_questions,
            "required_inputs": self.required_inputs,
            "analysis_process": self.analysis_process,
            "expected_output": self.expected_output,
            "interpretation": self.interpretation,
            "limitations": self.limitations,
            "common_mistakes": self.common_mistakes,
            "compatible_frameworks": self.compatible_frameworks,
            "framework_sequence": self.framework_sequence,
            "decision_impact": self.decision_impact,
            "consulting_judgment": self.consulting_judgment,
            "framework_reasoning_rule": self.framework_reasoning_rule,
            "framework_chain": self.framework_chain,
            "framework_combination_rules": self.framework_combination_rules,
            "framework_selection_hierarchy": self.framework_selection_hierarchy,
            "primary_question": self.primary_question,
            "trigger_conditions": self.trigger_conditions,
            "exclusion_conditions": self.exclusion_conditions,
            "selection_role": self.selection_role,
            "prerequisite_frameworks": self.prerequisite_frameworks,
            "compatible_frameworks": self.compatible_frameworks,
            "downstream_frameworks": self.downstream_frameworks,
            "quality_standard": self.quality_standard,
            "source_path": self.source_path,
        }


# ---------------------------------------------------------------------------
# FILE DISCOVERY
# ---------------------------------------------------------------------------

def discover_framework_files() -> List[Path]:
    """
    Discover individual framework Markdown files.

    Supporting files such as framework_library.md and
    framework_schema.md are excluded.
    """

    if not FRAMEWORKS_DIR.exists():
        return []

    files = []

    for path in FRAMEWORKS_DIR.rglob("*.md"):

        if path.name in SUPPORTING_FILES:
            continue

        files.append(path)

    return sorted(files)


# ---------------------------------------------------------------------------
# MARKDOWN PARSING HELPERS
# ---------------------------------------------------------------------------

def _clean_heading(line: str) -> str:
    """
    Convert a Markdown heading into normalized text.
    """

    return line.lstrip("#").strip()


def _normalize_section_name(section: str) -> str:
    """
    Normalize section names so the parser can map them
    to FrameworkKnowledge fields.
    """

    section = section.strip()

    if ". " in section:
        section = section.split(". ", 1)[1]

    return section.strip().lower()


def _is_section_heading(line: str) -> bool:
    """
    Determine whether a line represents a top-level framework section.
    """

    stripped = line.strip()

    return (
        stripped.startswith("## ")
        and not stripped.startswith("### ")
    )


def parse_sections(content: str) -> Dict[str, str]:
    """
    Parse the framework Markdown document into sections.

    Example:

        ## 3. Purpose

        Some text...

    becomes:

        {
            "purpose": "Some text..."
        }
    """

    lines = content.splitlines()

    sections: Dict[str, List[str]] = {}

    current_section: Optional[str] = None

    for line in lines:

        if _is_section_heading(line):

            heading = _clean_heading(line)

            current_section = _normalize_section_name(
                heading
            )

            sections[current_section] = []

            continue

        if current_section is not None:
            sections[current_section].append(line)

    return {
        key: "\n".join(value).strip()
        for key, value in sections.items()
    }


def _parse_list_items(text: str) -> List[str]:
    """
    Extract bullet/list items from a Markdown section.

    Supports:

        - item
        * item
        1. item
        2. item
    """

    if not text:
        return []

    items = []

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

        # Numbered list
        if ". " in stripped:
            prefix, value = stripped.split(". ", 1)

            if prefix.isdigit():
                items.append(value.strip())

    return items


def _section(
    sections: Dict[str, str],
    name: str,
) -> str:
    """
    Safely retrieve a section.
    """

    return sections.get(name.lower(), "").strip()


def _list_section(
    sections: Dict[str, str],
    name: str,
) -> List[str]:
    """
    Safely retrieve a section as list items.
    """

    return _parse_list_items(
        _section(sections, name)
    )


# ---------------------------------------------------------------------------
# FRAMEWORK NAME
# ---------------------------------------------------------------------------

def _extract_framework_name(
    content: str,
    path: Path,
) -> str:
    """
    Extract framework name from:

        # Issue Tree

    Falls back to filename.
    """

    for line in content.splitlines():

        stripped = line.strip()

        if stripped.startswith("# ") and not stripped.startswith("## "):

            return stripped[2:].strip()

    return path.stem.replace("_", " ").title()


# ---------------------------------------------------------------------------
# FRAMEWORK PARSER
# ---------------------------------------------------------------------------

def parse_framework(
    path: Path,
) -> FrameworkKnowledge:
    """
    Load and parse one framework definition.
    """

    content = path.read_text(
        encoding="utf-8"
    )

    sections = parse_sections(content)

    framework = FrameworkKnowledge(

        name=_extract_framework_name(
            content,
            path,
        ),

        category=_section(
            sections,
            "Category",
        ),

        purpose=_section(
            sections,
            "Purpose",
        ),

        core_question=_section(
            sections,
            "Core Question",
        ),

        use_when=_list_section(
            sections,
            "Use When",
        ),

        do_not_use_when=_list_section(
            sections,
            "Do NOT Use When",
        ),

        problem_types=_list_section(
            sections,
            "Problem Types",
        ),

        decision_types=_list_section(
            sections,
            "Decision Types",
        ),

        key_questions=_list_section(
            sections,
            "Key Questions",
        ),

        required_inputs=_list_section(
            sections,
            "Required Inputs",
        ),

        analysis_process=_section(
            sections,
            "Analysis Process",
        ),

        expected_output=_section(
            sections,
            "Expected Output",
        ),

        interpretation=_section(
            sections,
            "Interpretation",
        ),

        limitations=_section(
            sections,
            "Limitations",
        ),

        common_mistakes=_list_section(
            sections,
            "Common Mistakes",
        ),


        framework_sequence=_section(
            sections,
            "Framework Sequence",
        ),

        decision_impact=_section(
            sections,
            "Decision Impact",
        ),

        consulting_judgment=_section(
            sections,
            "Consulting Judgment",
        ),

        framework_reasoning_rule=_section(
            sections,
            "Framework Reasoning Rule",
        ),

        framework_chain=_section(
            sections,
            "Framework Chain",
        ),

        framework_combination_rules=_section(
            sections,
            "Framework Combination Rules",
        ),

        framework_selection_hierarchy=_section(
            sections,
            "Framework Selection Hierarchy",
        ),

        # Explicit machine-readable framework-selection metadata.
        primary_question=_section(
            sections,
            "Primary Question",
        ),

        trigger_conditions=_list_section(
            sections,
            "Trigger Conditions",
        ),

        exclusion_conditions=_list_section(
            sections,
            "Exclusion Conditions",
        ),

        selection_role=_section(
            sections,
            "Selection Role",
        ),

        prerequisite_frameworks=_list_section(
            sections,
            "Prerequisite Frameworks",
        ),

        compatible_frameworks=_list_section(
            sections,
            "Compatible Frameworks",
        ),


        downstream_frameworks=_list_section(
            sections,
            "Downstream Frameworks",
        ),

        quality_standard=_section(
            sections,
            "Quality Standard",
        ),

        source_path=str(path),

        raw_content=content,
    )

    return framework


# ---------------------------------------------------------------------------
# LOAD ALL FRAMEWORKS
# ---------------------------------------------------------------------------

def load_all_frameworks() -> List[FrameworkKnowledge]:
    """
    Discover and parse every framework definition.
    """

    return [
        parse_framework(path)
        for path in discover_framework_files()
    ]


# ---------------------------------------------------------------------------
# FRAMEWORK RETRIEVAL
# ---------------------------------------------------------------------------

def get_framework(
    framework_name: str,
) -> Optional[FrameworkKnowledge]:
    """
    Retrieve a framework by name.

    Matching is case-insensitive.
    """

    target = framework_name.strip().lower()

    for framework in load_all_frameworks():

        if framework.name.lower() == target:
            return framework

    return None


# ---------------------------------------------------------------------------
# SEARCH
# ---------------------------------------------------------------------------

def search_frameworks(
    query: str,
) -> List[FrameworkKnowledge]:
    """
    Perform lightweight keyword search across framework knowledge.

    This is deliberately simple.

    It will later be replaced or supplemented by semantic retrieval.
    """

    query_words = {
        word.lower()
        for word in query.split()
        if word.strip()
    }

    if not query_words:
        return []

    scored_results = []

    for framework in load_all_frameworks():

        searchable_text = "\n".join(
            [
                framework.name,
                framework.category,
                framework.purpose,
                framework.core_question,
                framework.raw_content,
            ]
        ).lower()

        score = sum(
            1
            for word in query_words
            if word in searchable_text
        )

        if score > 0:
            scored_results.append(
                (
                    score,
                    framework,
                )
            )

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        framework
        for _, framework in scored_results
    ]


# ---------------------------------------------------------------------------
# CATALOG
# ---------------------------------------------------------------------------

def print_framework_catalog() -> None:
    """
    Print a concise catalog of available frameworks.
    """

    frameworks = load_all_frameworks()

    print(
        "\nLOHITH OS — FRAMEWORK KNOWLEDGE CATALOG"
    )

    print("=" * 60)

    if not frameworks:

        print(
            "No framework definitions found."
        )

        return

    for framework in frameworks:

        print(
            f"\n{framework.name}"
        )

        print(
            f"  Category: {framework.category}"
        )

        print(
            f"  Purpose: "
            f"{framework.purpose[:120]}"
        )

        print(
            f"  Source: "
            f"{framework.source_path}"
        )

    print(
        f"\nTotal frameworks: "
        f"{len(frameworks)}"
    )


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def run_tests() -> None:
    """
    Run Framework Knowledge Layer tests.
    """

    print(
        "\nTEST 1 — Discover framework files"
    )

    print("-" * 60)

    files = discover_framework_files()

    for path in files:
        print(path)

    print(
        f"\nDiscovered: {len(files)} framework files"
    )

    # ------------------------------------------------------------------

    print(
        "\nTEST 2 — Parse framework definitions"
    )

    print("-" * 60)

    frameworks = load_all_frameworks()

    for framework in frameworks:

        print(
            f"\nFramework: {framework.name}"
        )

        print(
            f"Category: {framework.category}"
        )

        print(
            f"Purpose: {framework.purpose[:100]}"
        )

        print(
            f"Use When: "
            f"{len(framework.use_when)} items"
        )

        print(
            f"Key Questions: "
            f"{len(framework.key_questions)} items"
        )

        print(
            f"Compatible Frameworks: "
            f"{len(framework.compatible_frameworks)} items"
        )

    print(
        f"\nParsed: {len(frameworks)} frameworks"
    )

    # ------------------------------------------------------------------

    print(
        "\nTEST 3 — Retrieve Issue Tree"
    )

    print("-" * 60)

    issue_tree = get_framework(
        "Issue Tree"
    )

    if issue_tree:

        print(
            f"Name: {issue_tree.name}"
        )

        print(
            f"Category: {issue_tree.category}"
        )

        print(
            f"Core Question: "
            f"{issue_tree.core_question}"
        )

        print(
            f"Use When: "
            f"{len(issue_tree.use_when)} items"
        )

    else:

        print(
            "Issue Tree not found."
        )

    # ------------------------------------------------------------------

    print(
        "\nTEST 4 — Retrieve MECE"
    )

    print("-" * 60)

    mece = get_framework(
        "MECE"
    )

    if mece:

        print(
            f"Name: {mece.name}"
        )

        print(
            f"Category: {mece.category}"
        )

        print(
            f"Core Question: "
            f"{mece.core_question}"
        )

        print(
            f"Use When: "
            f"{len(mece.use_when)} items"
        )

    else:

        print(
            "MECE not found."
        )

    # ------------------------------------------------------------------

    print(
        "\nTEST 5 — Framework search"
    )

    print("-" * 60)

    results = search_frameworks(
        "problem structure"
    )

    for framework in results[:5]:

        print(
            f"- {framework.name}"
        )

    # ------------------------------------------------------------------

    print(
        "\nTEST 6 — Framework dictionary"
    )

    print("-" * 60)

    if issue_tree:

        data = issue_tree.to_dict()

        print(
            f"Dictionary fields: "
            f"{len(data)}"
        )

        print(
            f"Framework name: "
            f"{data['name']}"
        )

        print(
            f"Category: "
            f"{data['category']}"
        )

    print(
        "\nFramework Knowledge Layer tests complete."
    )


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_tests()