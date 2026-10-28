from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TASK_FILE = PROJECT_ROOT / "data" / "tasks.md"


def add_task(task, priority="Medium"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    task_entry = f"""
- [ ] {task}
  - Priority: {priority}
  - Created: {timestamp}
"""

    with TASK_FILE.open("a", encoding="utf-8") as file:
        file.write(task_entry)

    return "Task added successfully."


def read_tasks():
    if not TASK_FILE.exists():
        return ""

    return TASK_FILE.read_text(encoding="utf-8")


def complete_task(task_text):
    if not TASK_FILE.exists():
        return "No task file found."

    content = TASK_FILE.read_text(encoding="utf-8")

    old_text = f"- [ ] {task_text}"
    new_text = f"- [x] {task_text}"

    if old_text not in content:
        return "Task not found."

    content = content.replace(old_text, new_text, 1)

    TASK_FILE.write_text(content, encoding="utf-8")

    return "Task completed successfully."


def delete_task(task_text):
    if not TASK_FILE.exists():
        return "No task file found."

    content = TASK_FILE.read_text(encoding="utf-8")

    lines = content.splitlines()

    new_lines = []
    skip_next_lines = 0
    found = False

    for line in lines:
        if skip_next_lines > 0:
            skip_next_lines -= 1
            continue

        if line == f"- [ ] {task_text}" or line == f"- [x] {task_text}":
            found = True
            skip_next_lines = 2
            continue

        new_lines.append(line)

    if not found:
        return "Task not found."

    TASK_FILE.write_text(
        "\n".join(new_lines) + "\n",
        encoding="utf-8"
    )

    return "Task deleted successfully."


if __name__ == "__main__":
    print("LOHITH OS — TASK SYSTEM")
    print("=" * 40)
    print()
    print(read_tasks())