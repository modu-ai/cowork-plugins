# A/B Testing (harness-ab-testing)

> MoAI-Cowork V.0.1.3 Harness Reference

## Overview
A/B Testing provides marketing professionals and product managers with structured guidance for designing, executing, and analyzing marketing experiments. This harness helps formulate clear hypotheses, determine sample sizes, interpret statistical significance, and optimize conversion rates through evidence-based decision-making.

## Expert Roles

- **Hypothesis Architect**: Shapes clear, testable hypotheses grounded in user behavior and business objectives
  - **Hypothesis Formulation**: Develops SMART hypotheses that link specific changes to measurable outcomes
  - **Baseline Research**: Analyzes historical data to establish control group benchmarks
  - **Competitor Benchmarking**: Identifies industry-standard conversion rates for meaningful improvement targets
  - **Stakeholder Alignment**: Ensures hypotheses reflect business priorities and technical feasibility
  - **Success Metrics Definition**: Defines primary, secondary, and monitoring metrics

- **Experimental Design Engineer**: Determines sample sizes, test duration, and statistical validity requirements
  - **Sample Size Calculation**: Uses power analysis to determine participants needed for 80% statistical power
  - **Variance Estimation**: Forecasts population variance from historical cohorts
  - **Duration Planning**: Calculates test duration accounting for traffic, seasonality, and statistical significance thresholds
  - **Segmentation Strategy**: Identifies audience subgroups for stratified sampling or targeted tests
  - **Randomization Validation**: Ensures proper traffic allocation and control group integrity

- **Analytics Interpreter**: Translates statistical outputs into actionable business insights
  - **Significance Assessment**: Determines whether observed differences reach statistical thresholds (p < 0.05)
  - **Confidence Interval Analysis**: Communicates uncertainty ranges and practical significance
  - **Effect Size Evaluation**: Quantifies real-world impact beyond p-values
  - **Segment Performance Analysis**: Identifies differential impacts across customer cohorts
  - **Risk Assessment**: Flags anomalies, Simpson's Paradox, or confounding variables

- **Conversion Optimization Strategist**: Synthesizes findings into iterative improvement roadmaps
  - **Win Documentation**: Captures winning variation details, implementation requirements, and learnings
  - **Rollout Planning**: Designs phased deployment to monitor full-scale impact
  - **Iteration Roadmapping**: Prioritizes next tests based on confidence and potential ROI
  - **Cross-functional Alignment**: Aligns results with product, engineering, and marketing timelines
  - **Institutional Knowledge Building**: Creates reusable frameworks and pattern libraries

- **Compliance & Risk Manager**: Ensures ethical testing practices and regulatory adherence
  - **Statistical Integrity**: Prevents p-hacking, multiple comparison bias, and early stopping without adjustment
  - **User Privacy Compliance**: Ensures GDPR/CCPA compliance in segmentation and tracking
  - **Transparency Standards**: Validates that test setup and results reporting meet platform policies
  - **Bias Detection**: Identifies selection bias, observer bias, or self-selection threats
  - **Documentation Audit**: Maintains reproducible test records for regulatory review

## Workflow

### Phase 1: Context Gathering
1. **Collect Current State**: Gather existing conversion rates, traffic volumes, historical variance, and current optimization baseline
2. **Identify Change Candidates**: Document specific elements to test (copy, design, offer, funnel step, user segment)
3. **Clarify Business Objectives**: Define success criteria, risk tolerance, budget for test duration, and strategic priority
4. **Validate Technical Capability**: Confirm testing platform availability, traffic routing, and analytics integration
5. **Establish Stakeholder Consensus**: Secure agreement on hypothesis, success threshold, and decision rules from decision-makers

### Phase 2: Analysis & Production

| Order | Task | Owner | Depends On | Deliverable |
|-------|------|-------|------------|-------------|
| 1 | Formulate hypothesis with primary metric | Hypothesis Architect | Context | `hypothesis-statement.md` |
| 2 | Calculate sample size and test duration | Experimental Design Engineer | Hypothesis | `sample-size-calculator.xlsx` |
| 3 | Design control and variant specifications | Hypothesis Architect | Hypothesis | `test-design-spec.md` |
| 4 | Build statistical analysis framework | Analytics Interpreter | Sample Size | `analysis-framework.md` |
| 5 | Execute test and monitor daily metrics | Experimental Design Engineer | Design Spec | `daily-monitoring-dashboard.xlsx` |
| 6 | Analyze results at statistical completion | Analytics Interpreter | Test Execution | `statistical-results-report.md` |
| 7 | Document learnings and rollout strategy | Conversion Optimizer | Analysis Report | `rollout-plan.md` |

**Inter-agent Communication**: Design Engineer notifies Hypothesis Architect of validity threats; Analytics Interpreter flags early stopping decisions with Compliance Manager; Conversion Optimizer coordinates rollout timing with stakeholders.

### Phase 3: Review & Delivery
1. **Statistical Review**: Verify sample size adequacy, significance calculation method, and multiple comparison adjustments
2. **Business Interpretation**: Confirm effect size is practically meaningful and recommend go/no-go decision
3. **Rollout Authorization**: Obtain stakeholder approval before implementation; document expected impact
4. **Monitoring Setup**: Establish guardrails for post-launch performance tracking
5. **Institutional Capture**: Archive test design, results, and learnings in team knowledge base for future reference

## Deliverables
- **hypothesis-statement.md**: Clear hypothesis with expected effect size and rationale
- **sample-size-calculator.xlsx**: Power analysis with traffic requirements and test duration estimates
- **test-design-spec.md**: Control/variant specifications, traffic allocation rules, and measurement approach
- **analysis-framework.md**: Statistical methods, significance thresholds, and analysis timeline
- **statistical-results-report.md**: Raw results, significance assessment, confidence intervals, and segment breakdowns
- **rollout-plan.md**: Winning variation deployment schedule, monitoring metrics, and scaling considerations

## Extension Skills
- **Statistical Power Tutorial**: Explains Type I/II error, power, and sample size trade-offs for non-statisticians
- **Revenue Impact Modeling**: Estimates business value of conversion improvement across revenue streams
- **Multi-variant Testing**: Extends 2-variant methodology to factorial and multi-armed bandit designs

## Error Handling

| Error Type | Strategy |
|-----------|----------|
| Insufficient Traffic | Extend test duration, reduce minimum effect size threshold, or segment to higher-traffic cohorts |
| High Variance Data | Stratify by user segment, control for confounders, increase sample size by 20-30%, or use CUPED variance reduction |
| Directionality Flip | Hold second confirmation test; audit for Simpson's Paradox or segment-level reversals |
| Pragmatic vs. Statistical Significance Conflict | Document effect size and business context; escalate to decision-makers with both perspectives |
| Multiple Comparisons Inflation | Apply Bonferroni correction, pre-register segments and metrics, or use False Discovery Rate control |
| Early Stopping Temptation | Lock analysis plan before viewing results; use sequential testing if required to stop early |
