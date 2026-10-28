from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MEMORY_FILE = PROJECT_ROOT / "data" / "memory" / "memory.md"
DECISION_FILE = PROJECT_ROOT / "brain" / "decisions.md"


def read_memory():
    """
    Read all long-term LOHITH OS memory.
    """
    if not MEMORY_FILE.exists():
        return ""

    return MEMORY_FILE.read_text(encoding="utf-8")


def add_memory(category, information):
    """
    Save a new long-term memory entry.
    """
    memory_entry = f"""

## Memory Entry

**Category:** {category}

**Information:**
{information}

"""

    with MEMORY_FILE.open("a", encoding="utf-8") as file:
        file.write(memory_entry)

    return "Memory saved successfully."


def clear_memory():
    """
    Clear all long-term memory.
    """
    MEMORY_FILE.write_text(
        "# LOHITH OS — MEMORY\n\n",
        encoding="utf-8"
    )

    return "Memory cleared."


def add_decision(decision, reason="", impact=""):
    """
    Save an important strategic decision.
    """
    decision_entry = f"""

## New Decision

**Decision:**
{decision}

**Reason:**
{reason}

**Impact:**
{impact}

"""

    with DECISION_FILE.open("a", encoding="utf-8") as file:
        file.write(decision_entry)

    return "Decision saved successfully."


if __name__ == "__main__":
    print("LOHITH OS — MEMORY TOOL")
    print("=" * 40)
    print()

    print("===== MEMORY =====")
    print(read_memory())