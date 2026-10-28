from pathlib import Path

from tools.memory import read_memory
from tools.tasks import read_tasks


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def read_brain():
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
            brain[filename] = file_path.read_text(encoding="utf-8")
        else:
            brain[filename] = ""

    return brain


def get_context():
    brain = read_brain()

    return {
        "brain": brain,
        "memory": read_memory(),
        "tasks": read_tasks(),
    }


def local_ceo_response(question):
    context = get_context()

    current_state = context["brain"].get("current_state.md", "")
    goals = context["brain"].get("goals.md", "")
    principles = context["brain"].get("principles.md", "")
    decisions = context["brain"].get("decisions.md", "")
    tasks = context["tasks"]

    question_lower = question.lower()

    if any(
        phrase in question_lower
        for phrase in [
            "what should i focus",
            "what should i do",
            "what should i prioritize",
            "what is my priority",
            "what next",
            "what's next",
        ]
    ):
        return f"""
SITUATION

You are currently building from the ground up.

Your current LOHITH OS priority stack is:

1. Build useful skills
2. Build LOHITH OS
3. Build content distribution
4. Identify and validate business opportunities
5. Increase income
6. Build systems
7. Scale what works

DIAGNOSIS

Your biggest risk is not a lack of ideas.

Your bigger risk is spreading attention across too many ideas.

PRIORITY

Build one important system, make it work, document it, improve it, and then expand.

RECOMMENDED ACTION

Continue building LOHITH OS V0.1 rather than starting another major project.

NEXT STEP

Finish the current LOHITH OS milestone before adding another major system.

CURRENT TASKS

{tasks if tasks.strip() else "No active tasks."}
"""

    if any(
        phrase in question_lower
        for phrase in [
            "business idea",
            "business ideas",
            "should i build",
            "startup idea",
            "business opportunity",
        ]
    ):
        return """
SITUATION

You want to identify business opportunities.

DIAGNOSIS

An exciting idea is not automatically a valuable business.

PRIORITY

Validate the underlying problem before building the solution.

RECOMMENDED ACTION

Evaluate the opportunity using:

1. Pain
2. Money
3. Frequency
4. AI feasibility
5. Automation potential
6. Customer acquisition
7. Competition
8. Founder fit
9. Speed to validation
10. Long-term potential

NEXT STEP

Describe the specific problem and who experiences it.

Do not build yet.
"""

    if any(
        phrase in question_lower
        for phrase in [
            "content",
            "youtube",
            "what should i post",
            "video idea",
        ]
    ):
        return """
SITUATION

YouTube is currently the primary distribution channel.

DIAGNOSIS

The strongest content direction is documenting the actual journey rather than pretending the destination has already been reached.

PRIORITY

Document real experiments, progress, failures, learning, and results.

CONTENT PILLARS

BUILD
AI, businesses, experiments, systems and technology.

BECOME
Fitness, appearance, confidence, skills and transformation.

EXPERIENCE
Music, DJing, travel, events and experiences.

THINK
Business ideas, philosophy, opinions and observations.

CHARACTER
Humor, personality, ambition, mistakes and unexpected moments.

NEXT STEP

Choose one real thing you are currently building or experiencing and document it.
"""

    if any(
        phrase in question_lower
        for phrase in [
            "career",
            "job",
            "business analyst",
            "skills",
            "learn",
        ]
    ):
        return """
SITUATION

Your current professional direction is Business Analysis + AI + Automation.

DIAGNOSIS

The goal is not to collect courses.

The goal is to build useful capability that increases earning power and supports your long-term entrepreneurial direction.

PRIORITY

Develop:

- Business Analysis
- Excel
- SQL
- Power BI
- AI workflows
- Automation
- Process optimization
- AI product thinking
- Research
- Communication
- Problem solving

RECOMMENDED ACTION

Prioritize practical skill development and projects that demonstrate those skills.

NEXT STEP

Choose one skill and create a small practical project around it.
"""

    if any(
        phrase in question_lower
        for phrase in [
            "principles",
            "how should you think",
            "how should you decide",
            "decision",
        ]
    ):
        return """
LOHITH OS DECISION FRAMEWORK

Reality over hype.

Execution over planning.

Start small.

Maximum learning per unit of effort.

Protect attention.

One primary objective at a time.

Build assets.

Document everything worth repeating.

Automate carefully.

Never fake reality.

Challenge the founder.

Protect the long game.

Move quickly where mistakes are reversible.

Move slowly where mistakes are expensive or irreversible.

Core operating formula:

REALITY
→ UNDERSTAND
→ PRIORITIZE
→ ACT
→ MEASURE
→ LEARN
→ SYSTEMIZE
→ SCALE
"""

    return f"""
LOHITH OS LOCAL CEO

I understand the request, but the local CEO does not yet have a specific reasoning workflow for this type of question.

Because the live AI model is not connected, I will not pretend to provide AI reasoning that I cannot actually perform.

What I can currently use:

- Founder brain
- Current goals
- Principles
- Strategic decisions
- Long-term memory
- Current tasks

CURRENT STATE

{current_state[:2500]}

GOALS

{goals[:2500]}

IMPORTANT DECISIONS

{decisions[:2000]}

For a more specific answer, ask about your priorities, business ideas,
content, career, skills, or decision-making.
"""


if __name__ == "__main__":
    print(local_ceo_response("What should I focus on right now?"))