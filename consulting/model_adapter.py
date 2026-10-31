"""
LOHITH OS — Consulting Model Adapter V1

Connects the Consulting Brain to the OpenAI Agents SDK.

The adapter:
- uses the configured OPENAI_MODEL
- requests structured Pydantic output
- returns plain dictionaries to the existing consulting pipeline
- keeps provider/model details outside the consulting logic
"""

import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, Runner

load_dotenv()


class FrameworkModelOutput(BaseModel):
    framework: str = ""
    status: str = "COMPLETE"
    findings: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    next_framework: str = ""
    handoff_question: str = ""


class SynthesisModelOutput(BaseModel):
    key_findings: list[str] = Field(default_factory=list)
    root_causes: list[str] = Field(default_factory=list)
    evidence_gaps: list[str] = Field(default_factory=list)
    options: list[str] = Field(default_factory=list)
    trade_offs: list[str] = Field(default_factory=list)
    recommendation: str = ""
    recommendation_rationale: str = ""
    risks: list[str] = Field(default_factory=list)
    critical_assumptions: list[str] = Field(default_factory=list)
    implementation_priorities: list[str] = Field(default_factory=list)
    kpis: list[str] = Field(default_factory=list)
    confidence: float = 0.0


def get_model_name() -> str:
    """Return the configured model name."""

    model_name = os.getenv(
        "OPENAI_MODEL",
        "",
    ).strip()

    if not model_name:
        raise ValueError(
            "OPENAI_MODEL is not configured."
        )

    return model_name


def _run_structured_agent(
    prompt: str,
    output_type: type[BaseModel],
    instructions: str,
    model: Optional[str] = None,
) -> BaseModel:
    """Run an Agents SDK agent and return validated structured output."""

    selected_model = (
        model.strip()
        if isinstance(model, str) and model.strip()
        else get_model_name()
    )

    agent = Agent(
        name="LOHITH OS Consulting Analyst",
        model=selected_model,
        instructions=instructions,
        output_type=output_type,
    )

    result = Runner.run_sync(
        agent,
        prompt,
    )

    output = result.final_output

    if not isinstance(
        output,
        output_type,
    ):
        raise TypeError(
            "Model did not return the expected structured output type."
        )

    return output


def run_framework_model(
    prompt: str,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute one consulting framework through the real model.
    """

    output = _run_structured_agent(
        prompt=prompt,
        output_type=FrameworkModelOutput,
        model=model,
        instructions=(
            "You are a senior management consultant executing one "
            "specific analytical framework inside LOHITH OS. "
            "Follow the supplied framework instructions exactly. "
            "Use only evidence provided in the prompt. "
            "Do not invent facts. "
            "Separate findings, decisions, risks and assumptions. "
            "After completing the framework, determine whether the "
            "current findings create an important unresolved analytical "
            "question that requires another framework. "
            "If another framework is genuinely required, select the "
            "most appropriate next framework from the LOHITH OS "
            "framework library and provide a specific handoff question "
            "that the next framework should answer. "
            "The next framework must follow from the findings of the "
            "current framework, not merely from a predetermined sequence. "
            "If no additional framework is required, leave "
            "next_framework and handoff_question empty. "
            "Never invent a framework name. "
            "Return the requested structured output."
        ),
    )

    return output.model_dump()


def run_synthesis_model(
    prompt: str,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute cross-framework consulting synthesis through the real model.
    """

    output = _run_structured_agent(
        prompt=prompt,
        output_type=SynthesisModelOutput,
        model=model,
        instructions=(
            "You are a senior strategy consultant synthesizing "
            "multiple analytical frameworks. "
            "Distinguish evidence, inference and assumption. "
            "Do not invent missing evidence. "
            "Resolve conflicts explicitly. "
            "Recommend only when the evidence supports a conclusion. "
            "Translate the conclusion into implementation priorities "
            "and measurable KPIs. "
            "Return the requested structured output."
        ),
    )

    return output.model_dump()


if __name__ == "__main__":
    print("=" * 70)
    print("LOHITH OS — CONSULTING MODEL ADAPTER V1")
    print("=" * 70)
    print()
    print("Configured model:")
    print(get_model_name())
    print()
    print("Framework output fields:")
    for field in FrameworkModelOutput.model_fields:
        print("-", field)
    print()
    print("Synthesis output fields:")
    for field in SynthesisModelOutput.model_fields:
        print("-", field)
    print()
    print("PASS — Structured model adapter loaded.")
