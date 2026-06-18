# MoAI-ADK Third-Party Notices

> **본 저장소(저작물)의 라이선스**: MoAI Cowork Plugins 라이선스 — 비상업·변경금지(NC-ND) v1.0 ([LICENSE](LICENSE)).
> 아래에 열거된 제3자 구성요소는 **각자의 원 라이선스**가 적용되며, NC-ND 라이선스의 적용을 받지 아니합니다(LICENSE 제7조). 충돌이 발생하는 경우 해당 구성요소에 관하여는 제3자 라이선스가 우선합니다.

This product includes software developed by revfactory/harness and redistributed under the Apache License 2.0.

## Apache License 2.0

The following source material is licensed under Apache License 2.0:

**Source Repository**: https://github.com/revfactory/harness  
**License**: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)

### Imported Components

The following reference documents from `revfactory/harness` (imported 2026-04-26) are incorporated into MoAI-ADK as pattern cookbook rules:

1. `agent-design-patterns.md` → `.claude/rules/moai/development/agent-patterns.md`
2. `qa-agent-guide.md` → `.claude/rules/moai/quality/boundary-verification.md`
3. `skill-testing-guide.md` → `.claude/rules/moai/development/skill-ab-testing.md`
4. `team-examples.md` → `.claude/rules/moai/workflow/team-pattern-cookbook.md`
5. `orchestrator-template.md` → `.claude/rules/moai/development/orchestrator-templates.md`
6. `skill-writing-guide.md` → `.claude/rules/moai/development/skill-writing-craft.md`

### Phase 2: Harness Methodology Implementation (2026-04-30)

The following deliverables implement harness's 6-Phase skill generation workflow and testing methodology as standalone cowork skills and rules:

7. `skill-writing-guide.md` (6-Phase workflow) → `moai-core/skills/skill-builder/SKILL.md` (v1.5.x: renamed from `skill-forge`)
8. `skill-testing-guide.md` (A/B + regression) + `qa-agent-guide.md` (rubric) + Pipeline (chain testing) → `moai-core/skills/skill-tester/SKILL.md` (v1.5.x: rubric + chain protocol internalized)
9. `skill-writing-guide.md` (template system) → `moai-core/skills/skill-template/SKILL.md`
10. `qa-agent-guide.md` (scoring rubric) → `.claude/rules/harness/quality/skill-scoring-rubric.md`
11. `team-examples.md` (chain testing) → `.claude/rules/harness/quality/chain-testing.md`

Supporting scripts:
- `scripts/skill-lint.sh` — SKILL.md frontmatter and structure validation
- `scripts/skill-test-runner.sh` — Test case execution and report generation

### Attribution

This product includes software developed by revfactory/harness contributors. The original works and any modifications are provided under the terms of the Apache License 2.0.

The imported documents have been adapted for MoAI-ADK terminology and 16-language neutrality while preserving the original technical content and design patterns. Original source authorship is retained.

### Full Apache License 2.0 Text

For the complete Apache License 2.0 text, visit: https://www.apache.org/licenses/LICENSE-2.0

---

## Karpathy Coding Principles

The following reference material is derived from Andrej Karpathy's coding philosophy:

**Source Repository**: https://github.com/forrestchang/andrej-karpathy-skills

### Imported Concepts

The following concepts from Karpathy's 4 coding principles and anti-pattern catalog (imported 2026-04-28) are incorporated into MoAI-ADK:

1. **4 Coding Principles** → `.claude/rules/moai/development/karpathy-quickref.md`
   - Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution
   - Mapped to MoAI's 6 Agent Core Behaviors with checkpoint questions

2. **Anti-Pattern Catalog (8 categories)** → `.claude/skills/moai/references/anti-patterns.md`
   - Premature Abstraction, Over-Engineering, Drive-By Refactoring, Style Drift
   - Silent Assumption, Guessing Over Clarifying, Sycophantic Agreement, Claiming Without Evidence
   - Adapted with Go/Python/TypeScript code examples for MoAI agent context

3. **Constitution Amendments (3 additions)** → `.claude/rules/moai/core/moai-constitution.md`
   - Behavior 4: Quantitative LOC trigger (Simplicity First)
   - Behavior 5: Style-matching directive (Surgical Changes)
   - Behavior 6: Goal-to-test pattern (Goal-Driven Execution)

### Attribution

Andrej Karpathy's coding principles are shared publicly as educational material. The `forrestchang/andrej-karpathy-skills` repository packages these principles into a structured reference. MoAI-ADK has adapted the concepts, mapped them to existing Agent Core Behaviors, and created concrete code examples specific to MoAI's orchestration context.

---

## NomaDamas k-skill (MIT)

The following skills are adapted from `NomaDamas/k-skill` (imported 2026-05-04, v2.0.0):

**Source Repository**: https://github.com/NomaDamas/k-skill
**License**: MIT

### Imported Skills (v2.0.0, 6 skills)

1. `iros-registry-automation` → `moai-legal/skills/iros-registry-automation/` — 인터넷등기소 등기부등본 발급 보조 (원 저작자: `challengekim/iros-registry-automation`)
2. `real-estate-search` → `moai-business/skills/real-estate-search/` — MOLIT 실거래가/전월세 (원 저작자 참고: `tae0y/real-estate-mcp`)
3. `mfds-drug-safety` + `mfds-food-safety` → `moai-commerce/skills/mfds-safety/` — 식약처 의약품·식품 안전 (통합)
4. `court-auction-notice-search` → `moai-finance/skills/court-auction-search/` — 법원경매 매각공고 조회
5. `korean-spell-check` → `moai-content/skills/korean-spell-check/` — 바른한글(부산대) 맞춤법 검사
6. `korean-stock-search` → `moai-finance/skills/korean-stock-search/` — KRX 종목 검색·시세 (원 저작자 참고: `jjlabsio/korea-stock-mcp`)

### Attribution

`NomaDamas/k-skill`은 한국인을 위한 Claude Code 스킬 모음입니다. cowork에 포팅하면서 MoAI 컨벤션(SKILL.md frontmatter v1.3.0 정책 — `metadata:` 블록 제거, `user-invocable: true`)에 맞춰 재작성했습니다. 원본의 `k-skill-proxy.nomadamas.org` hosted proxy 의존성과 원 저작자 링크는 보존됩니다. 4개 스킬(real-estate, mfds-safety, court-auction, korean-stock)은 NomaDamas 운영 프록시를 경유합니다 — self-host가 필요하면 `KSKILL_PROXY_BASE_URL` 환경변수로 대체 가능합니다.

### Full MIT License Text

For the complete MIT License text, visit: https://opensource.org/licenses/MIT

---

## agricidaniel/claude-ads (MIT)

The following audit methodology and scoring system is referenced from `agricidaniel/claude-ads` v1.5.1 when building MoAI-ADK's Meta Ads audit MCP server (`mcp-servers/moai-ads-audit/`, SPEC-MOAI-ADS-AUDIT-MCP-001):

**Source Repository**: https://github.com/AgriciDaniel/claude-ads
**License**: MIT
**Reference Version**: v1.5.1 (4,815 stars, 2026-05-13)

### Referenced Concepts (methodology only, no direct code copy)

1. **Meta 50-check audit matrix** → SPEC-MOAI-ADS-AUDIT-MCP-001 audit tools
   - Pixel/CAPI Health (M01-M10): event_id, EMQ tiered targets, dedup rate ≥90%, AEM top 8 events
   - Creative Diversity & Fatigue (M25-M32 + M-CR1-4): Andromeda Similarity <60%, frequency thresholds
   - Account Structure (M11-M18 + M33-M40 + M-ST1-2): Learning Limited <30%, CBO/ABO decision
   - Audience & Targeting (M19-M24 + M-TH1): audience overlap <20%, Lookalike seed quality
   - Andromeda & Platform Changes (M-AN1, M-AT1, M-IA1, M-TH1): 2026 Meta platform updates

2. **Weighted Scoring Algorithm** → SPEC-MOAI-ADS-AUDIT-MCP-001 scoring engine
   - Formula: `S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100`
   - Severity multipliers: Critical 5.0× / High 3.0× / Medium 1.5× / Low 0.5×
   - Result mapping: PASS=full, WARNING=0.5, FAIL=0, N/A=excluded
   - A-F grading: A(90+) / B(75-89) / C(60-74) / D(40-59) / F(<40)

3. **Quick Wins logic** → SPEC-MOAI-ADS-AUDIT-MCP-001 action prioritization
   - Critical/High severity + estimated remediation <15min → Quick Win flag

4. **EMQ optimization tiers** → SPEC-META-ADS-001 EMQ 진단 모듈
   - Tiered targets: Purchase ≥8.5, AddToCart ≥6.5, PageView ≥5.5
   - Key parameters: em(+4.0), ph(+3.0), external_id, fbp, fbc

### Korean Market Adaptation (7 areas localized)

| Area | claude-ads (Original) | MoAI-ADK (Korean adapted) |
|------|----------------------|---------------------------|
| Benchmarks | WordStream/Triple Whale (US) | Korean market: CPC ₩500-1,500, ROAS 1.5-2.5, 케어밀 1.80 reference |
| Industry classification | 11 templates | 8 카테고리 (식품/음료·패션/뷰티·건강기능식품·IT/디지털·가정용품·교육·B2B·기타) |
| Regulations | GDPR/CCPA/Special Ad Categories | 한국 개인정보보호법(PIPA)·정보통신망법(ITNA)·전자상거래법·표시광고법·식약처 광고 심의 |
| User groups | 11 industry templates | 3 사용자 그룹 (인하우스·대행사·소규모) |
| Expression style | PASS/WARNING/FAIL + score | 🟢🟡🔴 강도별 액션 옵션 + 운영 철학 분기 |
| Output formats | PDF only | HTML/DOCX/PPTX/MD (4 formats) |
| Analysis dimensions | 4 categories | 9 modules + 4D demographic cross-analysis (광고×지면×연령×성별) |

### Attribution

`agricidaniel/claude-ads` v1.5.1 is a comprehensive paid advertising audit skill for Claude Code by Daniel Agrici (agricidaniel.com / AI Marketing Hub). MoAI-ADK references its Meta audit checklist, weighted scoring algorithm, and Quick Wins logic when building Korean-market-specific Meta Ads audit MCP. Reference does not include direct code copying; only methodology and check matrix structure are adapted to Korean ecommerce context (케어밀 사례 통합).

### Full MIT License Text

For the complete MIT License text, visit: https://opensource.org/licenses/MIT

---

## moai-cowork 커뮤니티 자체 제작 교재 (Internal Course Material)

The following skills reference moai-cowork 캠프 자체 제작 교재 (PDF 매뉴얼):

| Skill | Reference |
|---|---|
| `moai-education/skills/course-operations-manual/SKILL.md` | "PDF §8" — moai-cowork 캠프 운영 실무 매뉴얼 |
| `moai-education/skills/course-followup-sequence/SKILL.md` | "PDF §10" — 동일 매뉴얼 |

These materials are developed internally by the moai-cowork community. Skills may be redistributed under MoAI-ADK MIT; the underlying PDF remains community-internal.

---

**Import Date (harness Phase 1)**: 2026-04-26
**Import Date (harness Phase 2)**: 2026-04-30
**Import Date (Karpathy)**: 2026-04-28
**Import Date (k-skill)**: 2026-05-04 (v2.0.0)
**Reference Date (claude-ads)**: 2026-05-13 (v1.5.1, methodology adaptation only)
**Main Work License**: MoAI Cowork Plugins License — Non-Commercial No-Derivatives (NC-ND) v1.0 (see LICENSE)
**Prior Releases**: MIT (see LICENSE.MIT) — applies to releases distributed before the NC-ND transition (LICENSE §11)
**Third-Party Components**: governed solely by their own licenses listed above (Apache License 2.0 / MIT / SIL OFL 1.1). The NC-ND license does not modify, restrict, or supersede them; where a conflict arises, the third-party license controls for that component.
