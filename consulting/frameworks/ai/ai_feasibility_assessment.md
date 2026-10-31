# AI Feasibility Assessment

## Category
AI / Automation

## Purpose
Determine whether AI can reliably perform enough of a business workflow at acceptable quality, risk, cost, and human oversight to justify implementation.

## Core Question
Can AI perform the target work reliably enough to create meaningful business value?

## Use When
- A business is considering AI automation.
- A repetitive workflow is being evaluated for AI suitability.
- Management needs to distinguish a genuine AI opportunity from AI hype.
- The process involves language, classification, prediction, generation, or decision support.
- The business needs to estimate realistic automation potential.

## Do NOT Use When
- A simple deterministic rule or traditional automation can solve the problem more effectively.
- The process has little measurable business value.
- Required data is unavailable or unusable.
- Failure consequences are unacceptable without adequate human controls.
- The primary question is which vendor to purchase rather than whether AI is feasible.

## Problem Types
- AI Automation
- Technology
- Operations
- Transformation
- Product

## Decision Types
- Decision
- Strategic
- Investment
- Implementation

## Key Questions
- What work is being performed?
- Which tasks are repetitive?
- Which tasks require human judgment?
- Which inputs are structured or unstructured?
- Is sufficient data available?
- Can success be objectively measured?
- What level of accuracy is required?
- What is the cost of failure?
- Can humans review uncertain outputs?
- What systems must the AI interact with?
- What percentage of the workflow could realistically be automated?
- What should happen when the AI is uncertain or wrong?

## Required Inputs
- Current workflow
- Task volume
- Task frequency
- Input types
- Output types
- Historical examples
- Error rates
- Accuracy requirements
- Human intervention points
- Risk requirements
- Compliance requirements
- Current process cost
- Expected automation value
- Available systems and integrations

## Analysis Process
1. Map the current workflow.
2. Decompose the workflow into individual tasks.
3. Classify each task by complexity and judgment requirement.
4. Determine whether AI is appropriate for each task.
5. Assess data availability and quality.
6. Define required reliability and accuracy.
7. Assess the consequences of failure.
8. Determine human oversight requirements.
9. Estimate realistic automation coverage.
10. Compare expected value with implementation and operating cost.
11. Identify technical, operational, and governance constraints.
12. Recommend a pilot, partial automation, full automation, or no automation.

## Expected Output
- Task-level AI feasibility assessment.
- Estimated automation coverage.
- Human oversight requirements.
- Key technical and operational risks.
- Pilot recommendation.
- Conditions required for deployment.

## Interpretation
AI feasibility is not binary. A workflow may be partially automatable even when full automation is inappropriate. The best solution maximizes business value while keeping errors, risk, and human oversight within acceptable limits.

## Limitations
- Model capabilities change over time.
- Test performance may differ from production performance.
- Historical examples may not represent future cases.
- Technical feasibility does not guarantee economic feasibility.
- Edge cases can create disproportionate risk.

## Common Mistakes
- Assuming AI should automate the entire workflow.
- Ignoring workflow redesign.
- Ignoring the cost of errors.
- Using generic model benchmarks instead of task-specific testing.
- Treating a successful demo as proof of production readiness.
- Ignoring human review.
- Failing to compare AI with simpler automation.

## Compatible Frameworks
- Process Mapping
- Human-in-the-Loop Analysis
- Agent Suitability Assessment
- Build vs Buy
- Automation Opportunity Assessment
- TCO
- Cost-Benefit Analysis

## Framework Sequence
- Before: Process Mapping, Automation Opportunity Assessment
- After: Human-in-the-Loop Analysis, Agent Suitability Assessment, Build vs Buy, TCO

## Decision Impact
High

## Consulting Judgment
Evaluate AI at the task level rather than assuming the entire workflow should be automated. A strong recommendation may be partial automation, human-in-the-loop decision support, conventional software, or no AI.

## Framework Reasoning Rule
Assess value, task complexity, data, reliability requirements, risk, and human oversight before concluding that AI is feasible.

## Framework Chain
Workflow
→ Process Mapping
→ Task Decomposition
→ AI Feasibility
→ Human Oversight
→ Economic Evaluation
→ Pilot
→ Scale or Stop

## Framework Combination Rules
- Use Process Mapping first when the workflow is poorly understood.
- Use Human-in-the-Loop Analysis when errors have meaningful consequences.
- Use Agent Suitability Assessment when autonomous multi-step execution is being considered.
- Use Build vs Buy after feasibility to determine implementation approach.
- Use TCO and Cost-Benefit Analysis to test economic viability.

## Framework Selection Hierarchy
1. Understand the workflow before evaluating AI.
2. Evaluate individual tasks rather than assuming end-to-end automation.
3. Evaluate reliability and human oversight alongside technical capability.
4. Evaluate economics before recommending investment.
5. Recommend a pilot when important uncertainty remains.

## Primary Question
Can AI perform the target work reliably enough to create meaningful business value?

## Trigger Conditions
- A business is considering AI automation.
- A repetitive workflow is being evaluated for AI suitability.
- Management needs to distinguish a genuine AI opportunity from AI hype.
- The process involves language, classification, prediction, generation, or decision support.
- The business needs to estimate realistic automation potential.

## Exclusion Conditions
- A simple deterministic rule or traditional automation can solve the problem more effectively.
- The process has little measurable business value.
- Required data is unavailable or unusable.
- Failure consequences are unacceptable without adequate human controls.
- The primary question is which vendor to purchase rather than whether AI is feasible.

## Selection Role
FEASIBILITY_EVALUATION

## Prerequisite Frameworks
- Process Mapping

## Downstream Frameworks
- Human-in-the-Loop Analysis
- Agent Suitability Assessment
- Build vs Buy

## Quality Standard
The assessment must clearly distinguish technical feasibility, operational feasibility, economic feasibility, and governance feasibility, with explicit assumptions and failure conditions.
