from pathlib import Path

from os_agents.ceo import create_ceo
from os_agents.local_ceo import local_ceo_response
from tools.memory import add_memory, read_memory, add_decision
from tools.tasks import (
    read_tasks,
    add_task,
    complete_task,
    delete_task,
)

PROJECT_ROOT = Path(__file__).resolve().parent


def read_decisions():
    decision_file = PROJECT_ROOT / "brain" / "decisions.md"

    if not decision_file.exists():
        return ""

    return decision_file.read_text(encoding="utf-8")


def read_brain():
    brain_files = [
        "identity.md",
        "vision.md",
        "goals.md",
        "principles.md",
        "current_state.md",
        "decisions.md",
    ]

    brain = ""

    for filename in brain_files:
        file_path = PROJECT_ROOT / "brain" / filename

        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

            brain += f"\n\n===== {filename.upper()} =====\n\n"
            brain += content

    return brain


def show_help():
    print("\n===== LOHITH OS COMMANDS =====\n")

    print("/brain")
    print("  Show the complete LOHITH OS brain.")

    print("\n/tasks")
    print("  Show current tasks.")

    print("\n/decisions")
    print("  Show strategic decisions.")

    print("\n/memories")
    print("  Show long-term memory.")

    print("\n/addtask <task>")
    print("  Create a new task.")

    print("\n/complete <task>")
    print("  Mark a task as completed.")

    print("\n/delete <task>")
    print("  Delete a task.")

    print("\n/memory <category> | <information>")
    print("  Save long-term memory.")

    print("\n/decision <decision> | <reason> | <impact>")
    print("  Save a strategic decision.")

    print("\n/help")
    print("  Show available commands.")

    print("\nexit")
    print("  Shut down LOHITH OS.")

    print()


def handle_command(question):
    command = question.strip()

    # --------------------------------------------------
    # SHOW TASKS
    # --------------------------------------------------

    if command.lower() == "/tasks":

        print("\n===== CURRENT TASKS =====\n")

        tasks = read_tasks()

        if tasks.strip():
            print(tasks)
        else:
            print("No tasks found.")

        print()

        return True

    # --------------------------------------------------
    # SHOW DECISIONS
    # --------------------------------------------------

    if command.lower() == "/decisions":

        print("\n===== STRATEGIC DECISIONS =====\n")

        decisions = read_decisions()

        if decisions.strip():
            print(decisions)
        else:
            print("No decisions found.")

        print()

        return True

    # --------------------------------------------------
    # SHOW MEMORY
    # --------------------------------------------------

    if command.lower() == "/memories":

        print("\n===== LONG-TERM MEMORY =====\n")

        memory = read_memory()

        if memory.strip():
            print(memory)
        else:
            print("No memory found.")

        print()

        return True

    # --------------------------------------------------
    # SHOW BRAIN
    # --------------------------------------------------

    if command.lower() == "/brain":

        print("\n===== LOHITH OS BRAIN =====\n")

        brain = read_brain()

        if brain.strip():
            print(brain)
        else:
            print("Brain is empty.")

        print()

        return True

    # --------------------------------------------------
    # ADD TASK
    # --------------------------------------------------

    if command.lower().startswith("/addtask"):

        task = command[len("/addtask"):].strip()

        if not task:
            print("\nUsage:")
            print("/addtask <task>\n")
            return True

        result = add_task(task, "Medium")

        print(f"\nACTION > {result}")
        print(f"TASK > {task}")
        print("PRIORITY > Medium\n")

        return True

    # --------------------------------------------------
    # COMPLETE TASK
    # --------------------------------------------------

    if command.lower().startswith("/complete"):

        task = command[len("/complete"):].strip()

        if not task:
            print("\nUsage:")
            print("/complete <task>\n")
            return True

        result = complete_task(task)

        print(f"\nACTION > {result}\n")

        return True

    # --------------------------------------------------
    # DELETE TASK
    # --------------------------------------------------

    if command.lower().startswith("/delete"):

        task = command[len("/delete"):].strip()

        if not task:
            print("\nUsage:")
            print("/delete <task>\n")
            return True

        result = delete_task(task)

        print(f"\nACTION > {result}\n")

        return True

    # --------------------------------------------------
    # SAVE MEMORY
    # --------------------------------------------------

    if command.lower().startswith("/memory"):

        content = command[len("/memory"):].strip()

        if "|" not in content:
            print("\nUsage:")
            print("/memory <category> | <information>\n")
            return True

        category, information = content.split("|", 1)

        category = category.strip()
        information = information.strip()

        if not category or not information:
            print("\nBoth category and information are required.\n")
            return True

        result = add_memory(category, information)

        print(f"\nACTION > {result}")
        print(f"CATEGORY > {category}")
        print(f"MEMORY > {information}\n")

        return True

    # --------------------------------------------------
    # SAVE DECISION
    # --------------------------------------------------

    if command.lower().startswith("/decision"):

        content = command[len("/decision"):].strip()

        parts = [part.strip() for part in content.split("|")]

        if len(parts) < 1 or not parts[0]:
            print("\nUsage:")
            print("/decision <decision> | <reason> | <impact>\n")
            return True

        decision = parts[0]

        reason = parts[1] if len(parts) > 1 else ""
        impact = parts[2] if len(parts) > 2 else ""

        result = add_decision(
            decision=decision,
            reason=reason,
            impact=impact,
        )

        print(f"\nACTION > {result}")
        print(f"DECISION > {decision}")

        if reason:
            print(f"REASON > {reason}")

        if impact:
            print(f"IMPACT > {impact}")

        print()

        return True

    # --------------------------------------------------
    # HELP
    # --------------------------------------------------

    if command.lower() == "/help":

        show_help()

        return True

    return False


def main():

    print("=" * 50)
    print("        LOHITH OS — CEO")
    print("=" * 50)
    print()

    ceo = create_ceo()

    print("CEO initialized successfully.")
    print(f"Agent: {ceo.name}")
    print()

    print("LOHITH OS is ready.")
    print("Local CEO mode: ACTIVE")
    print("Action system: ACTIVE")
    print("Type '/help' for commands.")
    print("Type 'exit' to close.")
    print()

    while True:

        question = input("YOU > ").strip()

        if question.lower() == "exit":

            print("\nLOHITH OS shutting down.")

            break

        if not question:
            continue

        if handle_command(question):
            continue

        print("\nCEO >")

        print(local_ceo_response(question))

        print()


if __name__ == "__main__":
    main()