from tools.memory import add_memory, add_decision, read_memory
from tools.tasks import (
    add_task,
    complete_task,
    delete_task,
    read_tasks,
)


def create_task(task, priority="Medium"):
    """
    Create a new LOHITH OS task.
    """
    return add_task(task, priority)


def complete_existing_task(task):
    """
    Mark an existing task as completed.
    """
    return complete_task(task)


def delete_existing_task(task):
    """
    Delete an existing task.
    """
    return delete_task(task)


def save_memory(category, information):
    """
    Save information to long-term LOHITH OS memory.
    """
    return add_memory(category, information)


def save_strategic_decision(
    decision,
    reason="",
    impact="",
):
    """
    Save an important strategic decision.
    """
    return add_decision(
        decision=decision,
        reason=reason,
        impact=impact,
    )


def get_memory():
    """
    Read LOHITH OS long-term memory.
    """
    return read_memory()


def get_tasks():
    """
    Read all current LOHITH OS tasks.
    """
    return read_tasks()


def execute_action(action_type, **kwargs):
    """
    Central action dispatcher for LOHITH OS.

    Supported actions:

    - create_task
    - complete_task
    - delete_task
    - save_memory
    - save_decision
    - read_memory
    - read_tasks
    """

    if action_type == "create_task":
        return create_task(
            kwargs["task"],
            kwargs.get("priority", "Medium"),
        )

    if action_type == "complete_task":
        return complete_existing_task(
            kwargs["task"]
        )

    if action_type == "delete_task":
        return delete_existing_task(
            kwargs["task"]
        )

    if action_type == "save_memory":
        return save_memory(
            kwargs["category"],
            kwargs["information"],
        )

    if action_type == "save_decision":
        return save_strategic_decision(
            kwargs["decision"],
            kwargs.get("reason", ""),
            kwargs.get("impact", ""),
        )

    if action_type == "read_memory":
        return get_memory()

    if action_type == "read_tasks":
        return get_tasks()

    return f"Unknown action: {action_type}"


if __name__ == "__main__":

    print("LOHITH OS — ACTION LAYER")
    print("=" * 40)
    print()

    print("Supported actions:")
    print()
    print("- create_task")
    print("- complete_task")
    print("- delete_task")
    print("- save_memory")
    print("- save_decision")
    print("- read_memory")
    print("- read_tasks")