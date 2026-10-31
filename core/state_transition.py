from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from .decision_state import DecisionState
from .entities import StateTransition, utc_now


def transition_state(
    state: DecisionState,
    *,
    trigger: str,
    action: str,
    updates: Dict[str, Any],
    reasoning: str = "",
    metadata: Dict[str, Any] | None = None,
) -> StateTransition:
    if not trigger.strip():
        raise ValueError("trigger cannot be empty")

    if not action.strip():
        raise ValueError("action cannot be empty")

    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    valid_fields = set(type(state).model_fields.keys())

    invalid_fields = set(updates.keys()) - valid_fields

    if invalid_fields:
        raise ValueError(
            f"Invalid DecisionState fields: {sorted(invalid_fields)}"
        )

    before_version = state.version
    changed_fields: List[str] = []

    for field_name, value in updates.items():
        current_value = getattr(state, field_name)

        if current_value != value:
            setattr(state, field_name, value)
            changed_fields.append(field_name)

    state.touch()

    transition = StateTransition(
        id=str(uuid4()),
        timestamp=utc_now(),
        trigger=trigger,
        action=action,
        before_version=before_version,
        after_version=state.version,
        changed_fields=changed_fields,
        reasoning=reasoning or None,
        metadata=metadata or {},
    )

    state.history.append(transition)

    return transition
