"""
LOHITH OS — Framework Capability Registry

Defines the boundary between framework knowledge and framework
execution capability.

Framework knowledge answers:
    "What is this framework?"

The registry answers:
    "Can LOHITH OS currently execute this framework?"
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from .framework_knowledge import (
    FrameworkKnowledge,
    load_all_frameworks,
)


@dataclass(frozen=True)
class FrameworkCapability:
    """
    Execution capability for a known framework.
    """

    name: str
    executable: bool = False
    execution_mode: str = "ANALYZE"


# ---------------------------------------------------------------------------
# EXECUTION CAPABILITY CONFIGURATION
# ---------------------------------------------------------------------------

EXECUTABLE_FRAMEWORKS = {
    "Agent Suitability Assessment",
    "AI Feasibility Assessment",
    "Human-in-the-Loop Analysis",
    "Revenue Decomposition",
    "Scenario Analysis",
    "Sensitivity Analysis",
    "Cohort Analysis",
    "Growth Driver Tree",
    "Process Mapping",
    "Decision Matrix",
    "Issue Tree",
    "MECE",
    "PESTEL",
    "Porter's Five Forces",
    "Build vs Buy",
}


# ---------------------------------------------------------------------------
# REGISTRY
# ---------------------------------------------------------------------------

def _load_registry() -> Dict[str, FrameworkCapability]:
    """
    Build the capability registry from the canonical framework
    knowledge layer.
    """

    frameworks = load_all_frameworks()

    registry: Dict[str, FrameworkCapability] = {}

    for framework in frameworks:
        registry[framework.name.lower()] = FrameworkCapability(
            name=framework.name,
            executable=framework.name in EXECUTABLE_FRAMEWORKS,
            execution_mode="ANALYZE",
        )

    return registry


def get_capability(
    framework_name: str,
) -> Optional[FrameworkCapability]:
    """
    Return capability metadata for a known framework.
    """

    normalized = str(
        framework_name
    ).strip().lower()

    if not normalized:
        return None

    registry = _load_registry()

    return registry.get(normalized)


def is_known_framework(
    framework_name: str,
) -> bool:
    """
    Return True when framework knowledge exists.
    """

    return get_capability(framework_name) is not None


def is_executable_framework(
    framework_name: str,
) -> bool:
    """
    Return True when the framework is both known and executable.
    """

    capability = get_capability(
        framework_name
    )

    return bool(
        capability
        and capability.executable
    )


def get_known_frameworks() -> List[str]:
    """
    Return all frameworks discovered by the knowledge layer.
    """

    registry = _load_registry()

    return sorted(
        capability.name
        for capability in registry.values()
    )


def get_executable_frameworks() -> List[str]:
    """
    Return frameworks currently executable by LOHITH OS.
    """

    registry = _load_registry()

    return sorted(
        capability.name
        for capability in registry.values()
        if capability.executable
    )


def get_framework_knowledge(
    framework_name: str,
) -> Optional[FrameworkKnowledge]:
    """
    Return structured framework knowledge for a known framework.
    """

    normalized = str(
        framework_name
    ).strip().lower()

    if not normalized:
        return None

    for framework in load_all_frameworks():
        if framework.name.lower() == normalized:
            return framework

    return None


def validate_registry() -> None:
    """
    Validate that every configured executable framework exists
    in the canonical knowledge layer.
    """

    known = {
        name.lower()
        for name in get_known_frameworks()
    }

    missing = [
        name
        for name in EXECUTABLE_FRAMEWORKS
        if name.lower() not in known
    ]

    if missing:
        raise ValueError(
            "Executable framework configuration contains "
            "unknown frameworks: "
            + ", ".join(sorted(missing))
        )
