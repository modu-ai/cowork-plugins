# AI Strategy (harness-ai-strategy)

> MoAI-Cowork V.0.1.3 Harness Reference

## Overview
AI Strategy guides business leaders and product teams through structured AI adoption planning. This harness helps evaluate use cases, prioritize implementation roadmaps, assess vendor solutions, quantify ROI, and manage organizational change required for successful AI transformation across departments.

## Expert Roles

- **AI Opportunity Scout**: Identifies high-impact use cases aligned with business strategy and technical feasibility
  - **Process Audit**: Maps current workflows, pain points, manual handoffs, and decision bottlenecks
  - **Use Case Generation**: Brainstorms AI applications across customer service, operations, marketing, and finance
  - **Baseline Metrics**: Establishes current process costs, cycle times, error rates, and quality benchmarks
  - **Cross-functional Alignment**: Validates use cases with operations, compliance, and line-of-business stakeholders
  - **ROI Hypothesization**: Estimates labor savings, revenue uplift, and risk reduction for each candidate use case

- **Vendor Assessment Engineer**: Evaluates commercial and open-source AI solutions against business requirements
  - **Requirements Specification**: Translates business priorities into technical requirements (latency, accuracy, scalability)
  - **Competitive Landscape Mapping**: Catalogs available vendors, open-source alternatives, and custom development trade-offs
  - **Proof-of-Concept Design**: Plans limited-scope testing to validate vendor claims in real environment
  - **Cost Analysis**: Models licensing, infrastructure, integration, and ongoing operational costs
  - **Risk Assessment**: Evaluates vendor stability, data residency, security certifications, and lock-in risk

- **Implementation Roadmap Designer**: Sequences use case rollouts to balance learning, resource availability, and business impact
  - **Prioritization Framework**: Ranks use cases by strategic fit, implementation complexity, and expected ROI
  - **Resource Planning**: Estimates engineering, data science, and business operations headcount by phase
  - **Integration Architecture**: Designs data pipelines, API connections, and legacy system interfaces
  - **Pilot Planning**: Structures limited deployments to validate assumptions before full-scale rollout
  - **Timeline Estimation**: Identifies critical path, dependencies, and realistic delivery milestones

- **Change Management Lead**: Prepares organization for AI adoption, builds capability, and manages resistance
  - **Stakeholder Mapping**: Identifies champions, resisters, and neutral parties; tailors engagement by group
  - **Capability Building**: Designs training programs for AI literacy, tool usage, and process changes
  - **Communication Planning**: Develops messaging that connects AI to employee benefits and organizational goals
  - **Workflow Redesign**: Redefines roles, decision authorities, and KPIs to leverage AI-enabled processes
  - **Success Metrics**: Establishes adoption metrics (usage rates, workflow completion, user satisfaction)

- **Financial Modeling Specialist**: Quantifies AI investments and benefits for executive decision-making
  - **Cost Structure Modeling**: Builds detailed cost models for infrastructure, licensing, staffing, and maintenance
  - **Benefit Quantification**: Monetizes labor savings, revenue growth, risk mitigation, and customer satisfaction gains
  - **Sensitivity Analysis**: Tests assumptions (adoption rates, cost escalation, benefit realization delays)
  - **Payback Period Calculation**: Identifies when cumulative benefits exceed total investment
  - **Scenario Planning**: Models best-case, base-case, and worst-case outcomes for board presentations

## Workflow

### Phase 1: Context Gathering
1. **Define Strategic Context**: Clarify organizational priorities, budget constraints, and AI maturity current state
2. **Scope Business Areas**: Identify departments, customer segments, or products that are AI transformation candidates
3. **Assess Data Readiness**: Evaluate data availability, quality, governance, and infrastructure foundation
4. **Audit Current Capabilities**: Inventory existing AI tools, data science expertise, and integration infrastructure
5. **Establish Governance Framework**: Define decision authority, budget allocation, and oversight structure for AI initiatives

### Phase 2: Analysis & Production

| Order | Task | Owner | Depends On | Deliverable |
|-------|------|-------|------------|-------------|
| 1 | Identify AI-ready use cases | Opportunity Scout | Context | `use-case-inventory.md` |
| 2 | Conduct baseline metrics analysis | Opportunity Scout | Use Cases | `baseline-metrics-report.xlsx` |
| 3 | Evaluate vendor and build options | Vendor Assessment | Use Cases | `vendor-evaluation-matrix.xlsx` |
| 4 | Design implementation roadmap | Roadmap Designer | Vendor Evaluation | `ai-adoption-roadmap.md` |
| 5 | Model financial impact | Financial Modeler | Roadmap | `financial-model.xlsx` |
| 6 | Plan organizational change | Change Lead | Roadmap | `change-management-plan.md` |
| 7 | Create business case | Financial Modeler | All Above | `ai-business-case.md` |

**Inter-agent Communication**: Opportunity Scout shares use case details with Roadmap Designer; Vendor Assessment alerts Roadmap Designer to integration constraints; Change Lead coordinates timing with Roadmap Designer; Financial Modeler validates benefit assumptions with Opportunity Scout.

### Phase 3: Review & Delivery
1. **Viability Assessment**: Confirm technical feasibility, resource availability, and financial impact across all scenarios
2. **Stakeholder Validation**: Obtain buy-in from finance, IT, operations, and affected business units
3. **Governance Approval**: Secure executive sponsorship and budget authorization for Phase 1 implementation
4. **Infrastructure Readiness**: Confirm data, security, and cloud infrastructure required for pilot launch
5. **Launch Planning**: Finalize vendor contracts, resource allocation, and go/no-go decision criteria for pilot

## Deliverables
- **use-case-inventory.md**: Prioritized list of AI use cases with business context and success criteria
- **baseline-metrics-report.xlsx**: Current process metrics and benchmarks for measuring AI impact
- **vendor-evaluation-matrix.xlsx**: Comparison of solutions on functionality, cost, security, and technical fit
- **ai-adoption-roadmap.md**: Phased implementation plan with dependencies, milestones, and resource requirements
- **financial-model.xlsx**: Cost projections, benefit quantification, and ROI scenarios
- **change-management-plan.md**: Stakeholder communication, training programs, and success metrics
- **ai-business-case.md**: Executive summary with strategic rationale, financial impact, and risk mitigation

## Extension Skills
- **Data Governance & Ethics**: Establishes data quality standards, bias mitigation, and responsible AI principles
- **Vendor Negotiation**: Guides contract terms, SLAs, pricing structures, and data ownership clauses
- **Post-Implementation Optimization**: Monitors adoption, retrains models, and identifies next-wave use cases

## Error Handling

| Error Type | Strategy |
|-----------|----------|
| Unrealistic Benefit Projections | Anchor to published case studies; stress-test with conservative assumptions; pilot-validate before rollout |
| Vendor Over-promising | Reference existing customer deployments; require proof-of-concept in your environment; structure payments by milestones |
| Data Quality Gaps | Invest in data cleansing first; plan phased rollout starting with highest-quality datasets |
| Stakeholder Resistance | Address fear of displacement; highlight augmentation benefits; involve resisters in design; show early wins |
| Hidden Infrastructure Costs | Conduct IT infrastructure assessment early; budget 20-30% contingency for integration work |
| Organizational Capability Gaps | Hire AI talent early; partner with implementation firms; stagger rollout to allow learning curve |
