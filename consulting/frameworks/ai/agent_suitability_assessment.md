# Agent Suitability Assessment

## Category
AI / Agents / Automation

## Purpose
Determine whether a business workflow is suitable for an AI agent capable of planning, using tools, making decisions, and executing multiple steps rather than simply generating information.

## Core Question
Is this workflow suitable for agentic execution, and what level of autonomy should the agent have?

## Use When
- A workflow requires multiple sequential steps.
- The system must make decisions between steps.
- The workflow requires tools, APIs, databases, or external systems.
- The process contains repeatable decision patterns.
- The business wants AI to execute work rather than only provide recommendations.
- Autonomous or semi-autonomous workflow execution is being considered.

## Do NOT Use When
- The task is a simple one-step generation task.
- A deterministic rule can reliably solve the problem.
- The workflow has no meaningful sequence or decision-making.
- The cost of autonomous failure is unacceptable without practical controls.
- Required tools, data, permissions, or system access are unavailable.
- Human judgment dominates almost every step.

## Problem Types
- AI Automation
- Technology
- Operations
- Transformation
- Product

## Decision Types
- Decision
- Implementation
- Strategic
- Automation

## Key Questions
- What is the complete workflow?
- How many meaningful steps are involved?
- Does the workflow require planning?
- Does the workflow require decisions between steps?
- Does the system need to use external tools?
- Does the system need persistent state or memory?
- Are the tools reliable and accessible?
- Can the workflow be decomposed into manageable tasks?
- Which steps are deterministic?
- Which steps require reasoning?
- Which steps require human approval?
- What happens when the agent makes an incorrect decision?
- Are actions reversible?
- What permissions would the agent require?
- How should the agent recover from failure?
- Can agent performance be measured?
- What degree of autonomy is appropriate?

## Required Inputs
- Current workflow
- Workflow steps
- Decision points
- Tool requirements
- System integrations
- Data sources
- Permissions
- Error rates
- Failure consequences
- Reversibility of actions
- Human approval requirements
- Expected task volume
- Success criteria
- Monitoring requirements

## Analysis Process
1. Map the complete workflow.
2. Decompose the workflow into individual tasks.
3. Identify decision points.
4. Identify required tools and systems.
5. Classify tasks as deterministic, reasoning-intensive, or human-dependent.
6. Assess whether an agent adds value over simpler automation.
7. Evaluate required permissions and system access.
8. Evaluate error consequences and reversibility.
9. Define human approval points.
10. Determine appropriate autonomy level.
11. Define failure recovery mechanisms.
12. Define monitoring and evaluation requirements.
13. Recommend no agent, copilot, supervised agent, or higher-autonomy agent.

## Expected Output
- Agent suitability assessment.
- Workflow suitability classification.
- Recommended autonomy level.
- Required tools and integrations.
- Human approval points.
- Failure and recovery requirements.
- Monitoring requirements.
- Pilot recommendation.

## Interpretation
Agent suitability depends on more than whether AI can perform individual tasks. The workflow should benefit from autonomous sequencing, tool use, decision-making, and state management. When those characteristics are absent, simpler automation or a copilot may be preferable.

## Limitations
- Agent performance can vary across edge cases.
- Tool failures can compound across multiple steps.
- Greater autonomy increases the consequences of mistakes.
- Agent behavior can be harder to predict than deterministic automation.
- Integration and permission complexity may outweigh the value of autonomy.

## Common Mistakes
- Calling every AI workflow an agent.
- Using an agent where a simple rule or script is sufficient.
- Giving an agent excessive permissions.
- Ignoring failure recovery.
- Ignoring human approval requirements.
- Measuring only individual task accuracy instead of end-to-end workflow success.
- Automating a poorly designed process.
- Assuming more autonomy always creates more value.

## Compatible Frameworks
- Process Mapping
- AI Feasibility Assessment
- Human-in-the-Loop Analysis
- Build vs Buy
- Automation Opportunity Assessment
- Technology Maturity
- Risk Analysis

## Framework Sequence
- Before: Process Mapping, AI Feasibility Assessment, Human-in-the-Loop Analysis
- After: Build vs Buy, Implementation Planning, Monitoring

## Decision Impact
High

## Consulting Judgment
Use an agent only when autonomous sequencing and decision-making create meaningful incremental value over simpler automation. The correct answer may be a copilot, supervised agent, or no agent at all.

## Framework Reasoning Rule
Choose the lowest level of autonomy that can deliver the required business value safely and reliably.

## Framework Chain
Workflow
→ Task Decomposition
→ AI Feasibility
→ Agent Suitability
→ Autonomy Level
→ Human Oversight
→ Tool Access
→ Pilot
→ Scale

## Framework Combination Rules
- Use Process Mapping to understand the actual workflow before evaluating agent suitability.
- Use AI Feasibility Assessment to determine whether AI can perform the underlying tasks.
- Use Human-in-the-Loop Analysis to design approval and escalation points.
- Use Build vs Buy to determine how the agent capability should be implemented.
- Use Risk Analysis when agent actions can have material consequences.

## Framework Selection Hierarchy
1. Understand the workflow.
2. Determine whether AI is feasible.
3. Determine whether agentic behavior adds value beyond simpler automation.
4. Select the lowest safe autonomy level.
5. Define permissions, human controls, recovery, and monitoring.
6. Pilot before increasing autonomy.

## Primary Question
Is this workflow suitable for agentic execution, and what level of autonomy should the agent have?

## Trigger Conditions
- A workflow requires multiple sequential steps.
- The system must make decisions between steps.
- The workflow requires tools, APIs, databases, or external systems.
- The process contains repeatable decision patterns.
- The business wants AI to execute work rather than only provide recommendations.
- Autonomous or semi-autonomous workflow execution is being considered.

## Exclusion Conditions
- The task is a simple one-step generation task.
- A deterministic rule can reliably solve the problem.
- The workflow has no meaningful sequence or decision-making.
- The cost of autonomous failure is unacceptable without practical controls.
- Required tools, data, permissions, or system access are unavailable.
- Human judgment dominates almost every step.

## Selection Role
AUTONOMY_EVALUATION

## Prerequisite Frameworks
- Process Mapping
- AI Feasibility Assessment

## Downstream Frameworks
- Human-in-the-Loop Analysis

## Quality Standard
The assessment must clearly demonstrate why agentic execution creates incremental value, specify the required autonomy level, identify tool and permission requirements, and define human controls and failure recovery.
