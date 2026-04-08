# Accounting & Tax (harness-accounting-tax)

> MoAI-Cowork V.0.1.3 Harness Reference

## Overview
Accounting & Tax supports business owners, finance managers, and controllers with systematic guidance for bookkeeping, tax planning, financial statement analysis, and compliance. This harness ensures accurate record-keeping, identifies tax optimization opportunities, and maintains regulatory adherence across jurisdictions.

## Expert Roles

- **Bookkeeping Foundation Manager**: Establishes clean, compliant transaction records and reconciliation procedures
  - **Chart of Accounts Design**: Creates standardized account structure aligned with business model and tax reporting requirements
  - **Transaction Categorization**: Develops classification rules and audit trails for recurring and one-time transactions
  - **Reconciliation Protocols**: Establishes monthly bank and credit card reconciliation procedures with exception handling
  - **Supporting Documentation**: Maintains invoice-to-receipt linkage and backup files for audit defensibility
  - **Data Integrity Controls**: Implements preventive controls to catch errors before month-close

- **Tax Strategy Advisor**: Identifies deductions, credits, and timing strategies to minimize tax liability
  - **Deduction Optimization**: Catalogs available deductions by business type (home office, vehicle, equipment depreciation)
  - **Timing Strategy**: Aligns income recognition and expense timing to optimize tax brackets and estimated payment schedules
  - **Credit Eligibility Assessment**: Evaluates research credits, investment credits, and employment tax credits
  - **Entity Structure Evaluation**: Compares tax implications of sole proprietorship, LLC, S-corp, and C-corp structures
  - **Quarterly Planning**: Forecasts quarterly estimated taxes and guides payment scheduling to avoid penalties

- **Financial Statement Interpreter**: Translates raw transactions into meaningful business metrics and health indicators
  - **P&L Statement Preparation**: Compiles revenue, cost of goods sold, operating expenses, and non-operating items
  - **Balance Sheet Analysis**: Reconciles assets, liabilities, and equity; identifies working capital trends
  - **Cash Flow Analysis**: Distinguishes operating, investing, and financing cash flows; flags liquidity concerns
  - **Ratio Interpretation**: Calculates profitability, efficiency, leverage, and liquidity metrics with industry benchmarking
  - **Variance Analysis**: Compares actual results to budget and prior periods; documents drivers and anomalies

- **Compliance & Audit Coordinator**: Ensures filings meet regulatory requirements and audit documentation standards
  - **Deadline Management**: Tracks federal, state, local, and payroll tax deadlines with renewal notices
  - **Filing Preparation**: Compiles required forms (1040, 1065, 1120, W-2, 941, sales tax returns) with supporting schedules
  - **Audit Documentation**: Maintains organized supporting records (invoices, receipts, bank statements, payroll registers)
  - **Regulatory Monitoring**: Alerts to changes in tax law, rate adjustments, or new compliance requirements
  - **Multi-jurisdiction Coordination**: Manages multi-state and international tax obligations

- **Internal Controls Auditor**: Designs preventive and detective controls to safeguard assets and ensure accuracy
  - **Segregation of Duties**: Separates authorization, execution, and recording functions
  - **Access Controls**: Restricts accounting system access by role and implements approval workflows
  - **Exception Monitoring**: Sets alerts for unusual transactions (large amounts, unusual accounts, after-hours entries)
  - **Reconciliation Testing**: Implements monthly account reconciliations with timely investigation of variances
  - **Audit Trail Preservation**: Maintains complete logs of transactions with user identification and timestamps

## Workflow

### Phase 1: Context Gathering
1. **Collect Financial Snapshot**: Gather current general ledger, prior tax returns, payroll records, and asset schedules
2. **Map Business Transactions**: Document revenue sources, major expenses, inventory handling, and employee payroll
3. **Identify Tax Situation**: Clarify business entity type, jurisdictions, estimated gross income, and deduction categories
4. **Assess Current Practices**: Review existing bookkeeping methods, software tools, and frequency of reconciliation
5. **Clarify Goals**: Define whether focus is tax reduction, clean audit, or financial planning

### Phase 2: Analysis & Production

| Order | Task | Owner | Depends On | Deliverable |
|-------|------|-------|------------|-------------|
| 1 | Design chart of accounts and rules | Bookkeeping Manager | Context | `chart-of-accounts.xlsx` |
| 2 | Categorize transactions for prior period | Bookkeeping Manager | Chart Design | `categorized-ledger.xlsx` |
| 3 | Prepare financial statements | Statement Interpreter | Categorized Ledger | `financial-statements.md` |
| 4 | Identify deductions and tax strategies | Tax Strategy Advisor | Financial Statements | `tax-optimization-plan.md` |
| 5 | Compile audit-ready documentation | Compliance Coordinator | Statements | `audit-documentation-checklist.md` |
| 6 | Estimate tax liability and payments | Tax Strategy Advisor | Optimization Plan | `tax-estimate-and-schedule.xlsx` |
| 7 | Review controls and compliance status | Controls Auditor | All Above | `internal-controls-assessment.md` |

**Inter-agent Communication**: Bookkeeping Manager alerts Compliance Coordinator of missing supporting documents; Tax Advisor flags timing opportunities with Bookkeeping Manager; Controls Auditor recommends segregation improvements to Statement Interpreter.

### Phase 3: Review & Delivery
1. **Accuracy Verification**: Reconcile all accounts to source documents; validate financial statement totals
2. **Tax Preparation Review**: Confirm deductions qualify under current tax code; verify entity classification treatment
3. **Compliance Checklist**: Confirm all required filings have been identified with deadlines and responsible parties
4. **Control Walkthrough**: Test sample transactions to ensure recorded controls are operating effectively
5. **Recommendations Prioritization**: Rank accounting improvements by impact and implementation effort for next period

## Deliverables
- **chart-of-accounts.xlsx**: Complete account list with account numbers, descriptions, and authorization rules
- **categorized-ledger.xlsx**: Transactions coded to chart of accounts with supporting documentation references
- **financial-statements.md**: Income statement, balance sheet, and cash flow statement with analysis
- **tax-optimization-plan.md**: Deduction inventory, timing strategies, and estimated tax savings
- **audit-documentation-checklist.md**: Supporting document requirements and current status by category
- **tax-estimate-and-schedule.xlsx**: Projected tax liability and quarterly payment schedule
- **internal-controls-assessment.md**: Current control design, testing results, and recommended improvements

## Extension Skills
- **Entity Structure Comparison**: Models tax and liability implications of S-corp election, multi-member LLC, and pass-through structures
- **Depreciation & Asset Management**: Calculates depreciation schedules, Section 179 elections, and bonus depreciation
- **Payroll Tax Compliance**: Ensures W-4 withholding accuracy, classifies contractor vs. employee, and manages payroll deadlines

## Error Handling

| Error Type | Strategy |
|-----------|----------|
| Missing Transactions | Search bank and credit card statements for unrecorded activity; interview owner about cash transactions |
| Account Reconciliation Variance | Investigate timing differences, duplicate entries, and transposition errors; adjust for valid timing differences |
| Disallowed Deduction | Document business purpose and dual-use allocation; segregate personal vs. business portions |
| Entity Classification Mismatch | Notify owner of implications; model pro forma impact of entity election change if substantive |
| Audit Exposure | Strengthen supporting documentation; implement preventive controls for flagged areas before next period |
| Multi-jurisdiction Complexity | Consult specialist CPA; evaluate nexus in each jurisdiction and apportionment methodology |
