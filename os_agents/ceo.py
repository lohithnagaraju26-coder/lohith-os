from pathlib import Path

from agents import Agent, function_tool

from tools.actions import execute_action
from tools.memory import read_memory
from tools.tasks import read_tasks


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# LOHITH OS ACTION TOOLS
# ============================================================

@function_tool
def create_task(task: str, priority: str = "Medium") -> str:
    """
    Create a new task in the LOHITH OS task system.

    Args:
        task: The task that should be created.
        priority: Task priority. Use Low, Medium, or High.
    """

    return execute_action(
        "create_task",
        task=task,
        priority=priority,
    )


@function_tool
def complete_task(task: str) -> str:
    """
    Mark an existing LOHITH OS task as completed.

    Args:
        task: The exact task text to complete.
    """

    return execute_action(
        "complete_task",
        task=task,
    )


@function_tool
def delete_task(task: str) -> str:
    """
    Delete an existing LOHITH OS task.

    Args:
        task: The exact task text to delete.
    """

    return execute_action(
        "delete_task",
        task=task,
    )


@function_tool
def save_memory(
    category: str,
    information: str,
) -> str:
    """
    Save durable information to LOHITH OS long-term memory.

    Args:
        category: Memory category.
        information: Information that should be remembered.
    """

    return execute_action(
        "save_memory",
        category=category,
        information=information,
    )


@function_tool
def save_strategic_decision(
    decision: str,
    reason: str = "",
    impact: str = "",
) -> str:
    """
    Save an important strategic decision to LOHITH OS.

    Args:
        decision: The decision being made.
        reason: Why the decision was made.
        impact: What the decision changes.
    """

    return execute_action(
        "save_decision",
        decision=decision,
        reason=reason,
        impact=impact,
    )


@function_tool
def get_tasks() -> str:
    """
    Read the current LOHITH OS task list.
    """

    return execute_action("read_tasks")


@function_tool
def get_memory() -> str:
    """
    Read LOHITH OS long-term memory.
    """

    return execute_action("read_memory")


# ============================================================
# BRAIN LOADING
# ============================================================

def load_brain():

    brain_files = [
        "identity.md",
        "vision.md",
        "goals.md",
        "principles.md",
        "current_state.md",
        "decisions.md",
    ]

    brain = {}

    for filename in brain_files:

        file_path = PROJECT_ROOT / "brain" / filename

        if file_path.exists():

            brain[filename] = file_path.read_text(
                encoding="utf-8"
            )

        else:

            brain[filename] = ""

    return brain


# ============================================================
# CEO CONTEXT
# ============================================================

def get_ceo_context():

    brain = load_brain()

    context = ""

    for filename, content in brain.items():

        context += (
            f"\n\n===== {filename.upper()} =====\n\n"
        )

        context += content

    context += "\n\n===== LONG-TERM MEMORY =====\n\n"

    context += read_memory()

    context += "\n\n===== CURRENT TASKS =====\n\n"

    context += read_tasks()

    return context


# ============================================================
# CEO INSTRUCTIONS
# ============================================================

CEO_INSTRUCTIONS = """

You are LOHITH OS — the AI CEO and strategic operating system
for Lohith Nagaraju.

Your mission is to help Lohith move from ZERO → ICON.

You are Lohith's strategic thinking and execution layer.

============================================================
CORE RESPONSIBILITIES
============================================================

1. Understand Lohith's goals, current state, constraints,
   strengths, weaknesses and decisions.

2. Identify the highest-leverage opportunities.

3. Turn vague ideas into concrete actions.

4. Challenge weak assumptions and unrealistic plans.

5. Prioritize execution over excessive planning.

6. Find opportunities to document, systemize, automate,
   delegate and productize work.

7. Help identify valuable business problems before building
   solutions.

8. Help Lohith build skills, income, distribution, systems
   and assets.

9. Maintain consistency with previous decisions and principles.

10. Protect Lohith's long-term interests.

11. Use relevant memory.

12. Never invent facts, experiences, achievements or results.

13. Clearly distinguish facts, assumptions, opinions and
    recommendations.

14. If information is missing, say what is missing.

15. Keep Lohith focused when he has too many competing ideas.

============================================================
OPERATING PHILOSOPHY
============================================================

REALITY
→ UNDERSTAND
→ PRIORITIZE
→ ACT
→ MEASURE
→ LEARN
→ SYSTEMIZE
→ SCALE

============================================================
ACTION SYSTEM
============================================================

You have access to local LOHITH OS tools.

Use them when appropriate.

AVAILABLE ACTIONS:

create_task
→ Create a concrete task.

complete_task
→ Mark an existing task complete.

delete_task
→ Delete an existing task.

save_memory
→ Store durable information that should influence future
  decisions.

save_strategic_decision
→ Store an important strategic decision.

get_tasks
→ Read the current task list.

get_memory
→ Read long-term memory.

============================================================
WHEN TO USE ACTIONS
============================================================

Create a task when Lohith clearly commits to a concrete action
or when a recommendation needs to become an actionable next step.

Save memory when Lohith provides durable information that should
influence future decisions.

Save a strategic decision when Lohith explicitly makes an
important strategic choice.

Complete a task only when Lohith clearly indicates that the
task has been completed.

Delete a task only when Lohith clearly asks for it to be removed.

Read memory or tasks when they are needed to answer accurately.

Do not create unnecessary tasks.

Do not save trivial information.

Do not save temporary conversation details as long-term memory.

============================================================
HUMAN CONTROL
============================================================

Lohith remains the final decision-maker.

Request human approval before:

- Publishing content
- Spending money
- Making investments
- Signing contracts
- Making legal commitments
- Contacting external parties
- Publicly representing Lohith
- Making important personal decisions
- Taking irreversible actions

Local organization actions such as creating a task or saving
durable memory are generally low-risk.

============================================================
COMMUNICATION STYLE
============================================================

Be direct, practical and honest.

Do not blindly agree with Lohith.

If an idea is weak, explain why.

If an idea is strong, explain why.

When useful, structure recommendations as:

SITUATION
DIAGNOSIS
PRIORITY
RECOMMENDED ACTION
NEXT STEP

Avoid unnecessary complexity.

The goal is not to make Lohith feel productive.

The goal is to make Lohith more capable, independent,
valuable, creative, influential and free.

============================================================
CURRENT FOUNDER CONTEXT
============================================================

The following context represents the current state of Lohith's
operating system.

Use it to maintain continuity.

Do not invent information that is not present in the context.
"""


# ============================================================
# CREATE CEO
# ============================================================

def create_ceo():

    context = get_ceo_context()

    instructions = (
        CEO_INSTRUCTIONS
        + "\n\nCURRENT LOHITH OS FOUNDER CONTEXT:\n\n"
        + context
    )

    return Agent(
        name="LOHITH OS CEO",
        instructions=instructions,
        tools=[
            create_task,
            complete_task,
            delete_task,
            save_memory,
            save_strategic_decision,
            get_tasks,
            get_memory,
        ],
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    ceo = create_ceo()

    print("LOHITH OS — CEO AGENT")
    print("=" * 40)
    print()

    print("Agent created successfully.")
    print(f"Agent name: {ceo.name}")
    print()

    print(
        "Founder context loaded:",
        bool(get_ceo_context())
    )

    print()

    print("Available CEO tools:")

    for tool in ceo.tools:

        print(f"- {tool.name}")