# Cohort Analysis

## Category
Growth / Customer Analytics

## Purpose
Analyze groups of customers that share a common starting point over time to identify differences in retention, revenue, engagement, or other customer outcomes.

## Core Question
How do comparable customer cohorts behave over time, and where does performance deteriorate?

## Use When
- Retention or churn is suspected.
- Customer quality appears to be changing.
- Newer customers may behave differently from older customers.
- Overall averages may be hiding customer lifecycle problems.
- Performance needs to be compared across acquisition periods, channels, products, or segments.
- Management needs to understand when customer behavior changes over the lifecycle.

## Do NOT Use When
- Reliable customer-level longitudinal data is unavailable.
- Customers cannot be grouped into meaningful cohorts.
- The problem is unrelated to customer behavior over time.
- The observation period is too short to capture the relevant lifecycle.
- The analysis would be treated as proof of causality.

## Problem Types
- Customer
- Growth
- Marketing
- Retention
- Diagnostic
- Profitability

## Decision Types
- Diagnostic
- Optimization
- Strategic

## Key Questions
- How should cohorts be defined?
- How does retention differ across cohorts?
- How does revenue per customer evolve?
- Are newer cohorts better or worse than older cohorts?
- When does retention or engagement deteriorate?
- Is deterioration concentrated in particular channels?
- Is deterioration concentrated in particular products or segments?
- Is the difference caused by customer mix or customer behavior?
- Which cohort differences are commercially meaningful?
- What intervention point appears most actionable?

## Required Inputs
- Customer identifier
- Cohort definition
- Acquisition or start date
- Activity or transaction history
- Revenue history
- Retention or churn events
- Product attributes
- Channel attributes
- Observation window

## Analysis Process
1. Define the cohort criterion.
2. Group customers into comparable cohorts.
3. Establish a common lifecycle timeline.
4. Measure retention, revenue, engagement, or another relevant outcome.
5. Compare cohorts at equivalent lifecycle stages.
6. Identify meaningful differences.
7. Segment important differences further where appropriate.
8. Form hypotheses explaining the differences.
9. Validate hypotheses using additional evidence.

## Expected Output
- Cohort retention analysis.
- Cohort revenue analysis.
- Lifecycle performance comparisons.
- Identification of strong and weak cohorts.
- Timing of performance deterioration.
- Hypotheses explaining major cohort differences.

## Interpretation
A meaningful cohort pattern shows systematic differences between comparable customer groups. Worsening performance among newer cohorts may indicate acquisition quality, onboarding, product, pricing, or channel issues.

## Limitations
- Cohort analysis is observational.
- External events can affect multiple cohorts.
- Small cohorts can create unstable results.
- Different cohort definitions can produce different conclusions.
- Cohort analysis alone cannot establish causality.

## Common Mistakes
- Comparing cohorts at different lifecycle ages.
- Ignoring cohort size.
- Treating correlation as causality.
- Ignoring acquisition-channel mix.
- Looking only at averages.
- Ignoring changes in product, pricing, or market conditions.

## Compatible Frameworks
- Revenue Decomposition
- Growth Driver Tree
- Customer Segmentation
- Customer Journey Mapping
- Growth Funnel
- Root Cause Analysis

## Framework Sequence
- Before: Revenue Decomposition, Growth Driver Tree
- After: Customer Segmentation, Root Cause Analysis, Customer Journey Mapping, Growth Funnel

## Decision Impact
High when retention, customer quality, or lifecycle economics are important.

## Consulting Judgment
Use cohorts when averages may hide deterioration. Always compare equivalent lifecycle periods and investigate whether cohort differences are caused by customer mix, acquisition source, product experience, or external conditions.

## Framework Reasoning Rule
Compare like-with-like customer groups over comparable lifecycle periods before concluding that overall customer performance has changed.

## Framework Chain
Retention Signal
→ Cohort Analysis
→ Identify Weak Cohort
→ Segment Cohort
→ Investigate Root Cause
→ Intervention
→ Retention KPI

## Framework Combination Rules
- Combine with Customer Segmentation to understand which customer types drive cohort differences.
- Combine with Growth Funnel to investigate acquisition-quality differences.
- Combine with Customer Journey Mapping to investigate lifecycle breakdowns.
- Combine with Revenue Decomposition when retention changes affect revenue.

## Framework Selection Hierarchy
1. Use when the problem involves customer behavior changing over time.
2. Define comparable cohorts before interpreting performance.
3. Investigate meaningful differences before creating additional segmentation.
4. Move to root-cause analysis after the divergence is identified.

## Primary Question
How do comparable customer cohorts behave over time, and where does performance deteriorate?

## Trigger Conditions
- Retention or churn is suspected.
- Customer quality appears to be changing.
- Newer customers may behave differently from older customers.
- Overall averages may be hiding customer lifecycle problems.
- Performance needs to be compared across acquisition periods, channels, products, or segments.
- Management needs to understand when customer behavior changes over the lifecycle.

## Exclusion Conditions
- Reliable customer-level longitudinal data is unavailable.
- Customers cannot be grouped into meaningful cohorts.
- The problem is unrelated to customer behavior over time.
- The observation period is too short to capture the relevant lifecycle.
- The analysis would be treated as proof of causality.

## Selection Role
TEMPORAL_CUSTOMER_ANALYSIS

## Prerequisite Frameworks
- NONE

## Downstream Frameworks
- NONE

## Quality Standard
Cohorts must be comparable, lifecycle timing must be aligned, cohort size must be considered, and conclusions must distinguish descriptive patterns from causal explanations.
