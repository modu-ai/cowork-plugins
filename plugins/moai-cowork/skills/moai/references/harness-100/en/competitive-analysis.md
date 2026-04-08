# Competitive Analysis (harness-competitive-analysis)

> MoAI-Cowork V.0.1.3 Harness Reference

## Overview
Competitive Analysis provides product, strategy, and marketing teams with systematic intelligence on competitor positioning, capabilities, strengths, weaknesses, and strategic moves. This harness helps identify competitive threats and opportunities, develop differentiation strategies, and make informed decisions about market positioning and resource allocation.

## Expert Roles

- **Competitive Universe Mapper**: Identifies and classifies all direct, indirect, and emerging competitive threats
  - **Competitor Identification**: Catalogs direct competitors (same offering, same customer), indirect (different offering, same need), and emerging (adjacent markets)
  - **Competitive Clustering**: Groups competitors by market segment, geographic focus, business model, and strategic approach
  - **Market Share Estimation**: Researches revenue, customer count, or market penetration by competitor through public data and surveys
  - **Threat Assessment**: Prioritizes competitors by capability, market presence, and strategic threat to core business
  - **Ecosystem Mapping**: Places competitors in broader market ecosystem showing supplier, partner, and substitution relationships

- **Competitor Intelligence Specialist**: Gathers and synthesizes detailed information about competitor products, pricing, and go-to-market
  - **Product Capability Analysis**: Documents competitor feature sets, limitations, roadmap hints, and technology platform
  - **Pricing Research**: Catalogs list prices, discount structures, bundling, payment terms, and pricing strategy shifts
  - **Go-to-Market Intelligence**: Tracks marketing spend, sales team size, channel strategy, and customer acquisition approach
  - **Customer Feedback Analysis**: Synthesizes customer reviews, support forums, analyst reports, and customer interviews about competitors
  - **Talent Intelligence**: Monitors competitor hiring patterns, leadership changes, and organizational restructuring

- **SWOT & Positioning Analyst**: Evaluates competitive strengths, weaknesses, market positioning, and strategic implications
  - **SWOT Development**: Documents competitor strengths (capability, brand, relationships), weaknesses (cost, speed), opportunities (market growth, partnerships), threats (technology shift, new entrants)
  - **Competitive Positioning Map**: Creates visual maps showing competitors on dimensions relevant to customer choice (ease of use, price, capability, support)
  - **Advantage Identification**: Pinpoints sustainable competitive advantages (network effects, switching costs, proprietary technology, brand)
  - **Vulnerability Analysis**: Identifies competitor exposure to disruption, changing customer needs, or regulatory shifts
  - **Strategic Implication**: Translates competitive analysis into strategic recommendations for product, pricing, and positioning

- **Feature & Capability Comparator**: Builds detailed matrices comparing products, features, performance, and service levels
  - **Feature Matrix Development**: Creates comprehensive comparison of core, advanced, and missing features across competitors
  - **Performance Benchmarking**: Documents speed, scalability, reliability, and support quality claims with third-party validation
  - **Integration Capability**: Maps which external systems/platforms each competitor integrates with
  - **Service & Support Levels**: Compares SLAs, response times, support channels, and customer success approaches
  - **Total Cost of Ownership**: Models end-user costs accounting for licensing, implementation, training, and ongoing support

- **Strategy & Trend Forecaster**: Predicts competitive moves, market shifts, and strategic implications
  - **Strategic Intent Modeling**: Infers competitor strategy from hiring, partnerships, technology investments, and product decisions
  - **Market Shift Anticipation**: Identifies industry trends (consolidation, platform shifts, new segments) and how competitors position
  - **Competitive Move Forecasting**: Predicts likely competitor responses to market changes or company initiatives
  - **Scenario Planning**: Models best/worst case competitive landscape evolution over 2-3 year horizon
  - **Strategic Recommendation**: Proposes proactive competitive strategies (differentiation, pricing, partnerships, R&D focus)

## Workflow

### Phase 1: Context Gathering
1. **Define Competitive Scope**: Clarify target customer segments, product categories, and geographic markets for analysis
2. **Identify Information Needs**: Determine which competitive data is most valuable for strategic decisions
3. **Data Source Planning**: Identify where competitive information will be sourced (public data, customers, analysts, trial experience)
4. **Stakeholder Alignment**: Confirm which competitive questions are highest priority for leadership and product teams
5. **Historical Context**: Review past competitive analyses to identify trends and validate assumptions

### Phase 2: Analysis & Production

| Order | Task | Owner | Depends On | Deliverable |
|-------|------|-------|------------|-------------|
| 1 | Map competitive universe | Universe Mapper | Scope Definition | `competitor-landscape.md` |
| 2 | Gather competitor intelligence | Intelligence Specialist | Landscape Map | `competitor-intelligence-dossiers.md` |
| 3 | Build feature comparison matrix | Feature Comparator | Intelligence | `feature-comparison-matrix.xlsx` |
| 4 | Develop SWOT and positioning | SWOT Analyst | Intelligence + Features | `competitive-positioning-analysis.md` |
| 5 | Forecast competitive strategy | Strategy Forecaster | SWOT Analysis | `competitive-strategy-forecast.md` |
| 6 | Conduct TCO analysis | Feature Comparator | Intelligence | `total-cost-of-ownership.xlsx` |
| 7 | Synthesize strategic implications | Strategy Forecaster | All Above | `competitive-strategy-recommendations.md` |

**Inter-agent Communication**: Universe Mapper briefs Intelligence Specialist on priority competitors; Feature Comparator validates product claims with Intelligence Specialist; SWOT Analyst coordinates positioning dimensions with Universe Mapper; Strategy Forecaster synthesizes insights from all analysts.

### Phase 3: Review & Delivery
1. **Data Quality Check**: Validate competitive information accuracy through multiple sources and cross-checks
2. **Stakeholder Review**: Present analysis to product, marketing, and strategy teams to confirm relevance and completeness
3. **Bias Assessment**: Check for blind spots or assumption errors that might skew recommendations
4. **Action Planning**: Identify specific competitive responses (product features, pricing moves, messaging) and prioritize by impact
5. **Monitoring Setup**: Establish process for ongoing competitive intelligence collection and quarterly reassessment

## Deliverables
- **competitor-landscape.md**: Map of competitive universe with direct, indirect, and emerging competitors
- **competitor-intelligence-dossiers.md**: Detailed profiles of priority competitors including products, pricing, and go-to-market
- **feature-comparison-matrix.xlsx**: Comprehensive feature-by-competitor matrix with capability ratings
- **competitive-positioning-analysis.md**: SWOT analysis, positioning maps, and advantage/vulnerability assessment
- **competitive-strategy-forecast.md**: Anticipated competitive moves and market evolution scenarios
- **total-cost-of-ownership.xlsx**: End-user cost analysis comparing total ownership costs across competitors
- **competitive-strategy-recommendations.md**: Strategic recommendations for product, pricing, positioning, and partnerships

## Extension Skills
- **Win/Loss Analysis**: Catalogs recent sales wins and losses with reasons; identifies competitive displacement patterns
- **Customer Switch Analysis**: Models why customers switch between competitors; identifies dissatisfaction drivers
- **Pricing Strategy Benchmarking**: Analyzes competitor pricing philosophy and recommends optimal pricing strategy

## Error Handling

| Error Type | Strategy |
|-----------|----------|
| Incomplete Competitor List | Expand search to adjacent market segments, indirect substitutes, and emerging players; solicit customer input on competitive alternatives |
| Outdated Intelligence | Establish quarterly refresh cycle; set up alerts for competitor announcements; conduct periodic customer interviews |
| Feature Comparison Bias | Validate feature claims through direct trial or customer feedback; separate marketing claims from actual capability |
| SWOT Over-generalization | Segment SWOT by target customer segment and use case; avoid treating all competitors equally |
| Missing Strategic Context | Research competitor funding, leadership, and stated strategy; infer intent from hiring, partnerships, and investment |
| Analysis Paralysis | Establish decision deadline; identify highest-impact questions; create focused analysis rather than comprehensive coverage |
