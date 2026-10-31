# Human-in-the-Loop Analysis

## Category
AI / Automation / Governance

## Purpose
Determine where and how humans should remain involved in an AI-enabled workflow to balance automation, quality, risk, accountability, and efficiency.

## Core Question
Which parts of the workflow should AI perform autonomously, which require human review, and where should humans retain decision authority?

## Use When
- AI is being considered for a business workflow.
- AI outputs could create meaningful business, financial, legal, operational, or customer risk.
- Human judgment may be required for exceptions or high-impact decisions.
- The business needs to determine the appropriate level of human oversight.
- Full automation may be technically possible but operationally inappropriate.
- AI uncertainty varies significantly across tasks or cases.

## Do NOT Use When
- The workflow has no meaningful human or AI decision component.
- The process is fully deterministic and does not require judgment.
- Human involvement has no effect on quality, risk, or accountability.
- The objective is only to evaluate technical model performance.
- No meaningful consequences result from workflow errors.

## Problem Types
- AI Automation
- Technology
- Operations
- Risk
- Transformation

## Decision Types
- Decision
- Implementation
- Strategic
- Risk

## Key Questions
- Which tasks can AI perform reliably?
- Which tasks require human judgment?
- Which decisions have high consequences if wrong?
- Which cases should automatically pass to a human?
- What confidence or risk threshold should trigger review?
- What information should the human receive before reviewing an AI output?
- Can the human meaningfully correct the AI?
- Who owns the final decision?
- How should exceptions be handled?
- How should AI errors be monitored?
- What happens if the human reviewer disagrees with the AI?
- How much human review is economically justified?
- Can the human reviewer become a bottleneck?
- What audit trail is required?

## Required Inputs
- Workflow
- Task-level AI capabilities
- Error rates
- Confidence or uncertainty indicators
- Business impact of errors
- Human decision requirements
- Human review time
- Exception frequency
- Compliance requirements
- Accountability requirements
- Escalation rules
- Audit requirements

## Analysis Process
1. Map the workflow and decision points.
2. Classify tasks by AI capability and business risk.
3. Identify tasks suitable for autonomous execution.
4. Identify tasks requiring human review.
5. Identify decisions where humans must retain authority.
6. Define escalation and exception rules.
7. Define review thresholds.
8. Estimate human review workload.
9. Test whether human review creates a new bottleneck.
10. Define monitoring and audit mechanisms.
11. Validate the operating model through a controlled pilot.

## Expected Output
- Human-in-the-loop operating model.
- Task-level autonomy classification.
- Human review points.
- Escalation rules.
- Decision ownership.
- Review workload estimate.
- Monitoring requirements.

## Interpretation
The objective is not to maximize automation. The objective is to find the right balance between automation and human oversight based on task reliability, business risk, decision complexity, and economics.

## Limitations
- Thresholds may need adjustment after production evidence.
- Human reviewers can introduce their own errors or bias.
- Excessive review can eliminate the economic benefit of automation.
- Too little review can expose the business to unacceptable risk.
- Human behavior may change as trust in AI increases.

## Common Mistakes
- Keeping humans in every step without measuring whether review adds value.
- Removing humans from high-risk decisions simply because AI accuracy appears high.
- Failing to define escalation rules.
- Creating a human review queue that becomes the new bottleneck.
- Assuming human reviewers will always catch AI errors.
- Failing to assign decision accountability.
- Ignoring audit and traceability requirements.

## Compatible Frameworks
- AI Feasibility Assessment
- Process Mapping
- Agent Suitability Assessment
- Automation Opportunity Assessment
- Risk Analysis
- Build vs Buy

## Framework Sequence
- Before: Process Mapping, AI Feasibility Assessment
- After: Agent Suitability Assessment, Implementation Planning, Monitoring

## Decision Impact
High

## Consulting Judgment
Human oversight should be designed around risk and decision importance, not around a blanket preference for either automation or manual work. High-impact decisions generally require stronger controls than low-risk repetitive tasks.

## Framework Reasoning Rule
Assign autonomy according to reliability, risk, reversibility, and decision importance.

## Framework Chain
AI Capability
→ Task Risk
→ Autonomy Level
→ Human Review
→ Escalation
→ Decision Ownership
→ Monitoring

## Framework Combination Rules
- Combine with Process Mapping to identify exactly where human decisions occur.
- Combine with AI Feasibility Assessment to determine whether AI can perform the task reliably.
- Combine with Agent Suitability Assessment when autonomous multi-step execution is being considered.
- Combine with Risk Analysis for high-consequence workflows.
- Combine with Cost-Benefit Analysis to ensure human review remains economically justified.

## Framework Selection Hierarchy
1. Identify decision points before deciding where humans should remain.
2. Evaluate task reliability and business risk.
3. Assign the minimum human involvement required for acceptable quality and risk.
4. Test review workload during a pilot.
5. Adjust autonomy thresholds using production evidence.

## Primary Question
Which parts of the workflow should AI perform autonomously, which require human review, and where should humans retain decision authority?

## Trigger Conditions
- AI is being considered for a business workflow.
- AI outputs could create meaningful business, financial, legal, operational, or customer risk.
- Human judgment may be required for exceptions or high-impact decisions.
- The business needs to determine the appropriate level of human oversight.
- Full automation may be technically possible but operationally inappropriate.
- AI uncertainty varies significantly across tasks or cases.

## Exclusion Conditions
- The workflow has no meaningful human or AI decision component.
- The process is fully deterministic and does not require judgment.
- Human involvement has no effect on quality, risk, or accountability.
- The objective is only to evaluate technical model performance.
- No meaningful consequences result from workflow errors.

## Selection Role
CONTROL_DESIGN

## Prerequisite Frameworks
- Process Mapping
- AI Feasibility Assessment

## Downstream Frameworks
- NONE

## Quality Standard
The operating model must clearly specify task-level autonomy, human review points, escalation rules, decision ownership, monitoring, and the economic impact of human oversight.
