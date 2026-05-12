---
name: proposal-writer
description: |
  한국 B2B 영업 제안서 본문을 RFP·고객 요구사항 기반으로 자동 생성합니다.
  12섹션 표준 목차(표지·Executive Summary·회사 소개·시장 이해·솔루션·기술 스펙·일정·운영·레퍼런스·가격·리스크·부록)와
  Three C's(Compliant·Complete·Compelling) 원칙을 적용해 컴플라이언스 체크리스트와 함께 제공합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "B2B 영업 제안서 작성", "RFP 답변 만들어줘", "고객사 제안서"
  - "솔루션 제안서 초안", "[고객사명] 제안서", "이 RFP 답변 초안"
  - "B2B SaaS 제안서", "엔터프라이즈 영업 제안서", "수주 제안서"

  주의: 정부 지원사업 신청서는 `kr-gov-grant`(moai-business)를 사용하세요. 본 스킬은 **B2B 영업 고객 대상** 제안서만 다룹니다.
  투자자 IR 자료는 `investor-relations`(moai-business)를 사용하세요.
user-invocable: true
version: 2.4.0
---

# Proposal Writer — B2B 영업 제안서 자동 생성

> moai-sales | 한국 B2B 영업 워크플로우 첫 스킬

## 개요

한국 B2B 영업 환경에서 RFP 답변·솔루션 제안·수주 제안서 본문을 자동 생성합니다. HubSpot Breeze RFP Agent의 Three C's(Compliant·Complete·Compelling) 원칙과 한국 비즈니스 관행(격식체, 12섹션 표준 목차, 결재선 안내)을 결합했습니다.

**핵심 가치**: AI가 빠르게 초안을 만들고, 사용자가 핵심 가치 제안에 집중. 모든 산출물은 사람이 검토 후 발송 (Human-in-the-Loop).

## 트리거 키워드

B2B 제안서 RFP 답변 영업 제안서 솔루션 제안 수주 제안서 고객사 제안서 엔터프라이즈 영업 SaaS 영업 제안

## 워크플로우

### 1단계: 입력 자료 수집

다음 정보를 사용자로부터 확인합니다 (모두 필수는 아님, 가용 자료 기반):

- **RFP 문서 또는 고객 요구사항** (텍스트/PDF/메일 본문)
- **자사 회사·솔루션 소개** (회사 소개서, 제품 명세, 기술 문서)
- **과거 수주 제안서** (선택, content library로 활용)
- **딜 정보** (선택): 고객사명, 산업, 규모, 의사결정자 직책, 예상 계약 규모, 검토 기간

자료가 부족하면 12섹션 중 채울 수 있는 섹션부터 작성하고, 미충족 섹션은 `[추가 정보 필요: ...]` 플레이스홀더로 표시합니다.

### 2단계: RFP 컴플라이언스 분석 (Compliant)

RFP가 제공된 경우, 모든 필수 항목을 추출해 체크리스트화합니다:

- **형식 요구**: 페이지 수 한도, 폰트, 제출 마감, 제출 방식
- **필수 첨부**: 사업자등록증, 보안 인증(ISO 27001 등), 재무제표, 도입 사례
- **자격 요건**: 매출 규모, 업력, 인력, 보유 자격증
- **응답 양식**: 항목별 답변 표, 점수 산정 기준

체크리스트는 출력 마지막에 별도 섹션으로 첨부하며, **누락 항목은 빨간색 `❌` 마커**로 강조합니다.

### 3단계: 12섹션 본문 생성 (Complete)

표준 한국 B2B 제안서 12섹션 구조:

| # | 섹션 | 핵심 내용 |
|---|---|---|
| 1 | 표지 | 제안일·고객사·자사·담당자 |
| 2 | Executive Summary | 1페이지, 핵심 가치 제안 + 정량 ROI |
| 3 | 회사 소개 | 연혁·미션·핵심 인력 |
| 4 | 시장·고객 이해 | 고객 도전 과제 인용 + 시장 데이터 |
| 5 | 솔루션 개요 | 우리가 어떻게 푸는가 (1페이지) |
| 6 | 세부 기능·기술 스펙 | 기능별 상세 + 아키텍처 |
| 7 | 도입·구축 일정 | 단계별 마일스톤 (priority labels, 시간 단위 금지) |
| 8 | 운영·유지보수 계획 | SLA, 지원 채널, 업데이트 정책 |
| 9 | 레퍼런스·도입 사례 | 동종업계 사례 + 정량 효과 |
| 10 | 가격·라이선스 모델 | VAT 별도/포함 명시, 결제 조건 |
| 11 | 위험·완화 방안 | 도입 리스크 + 대응 전략 |
| 12 | 부록·참고자료 | 자격증, 인증서, 추가 자료 |

### 4단계: 한국 격식·톤 적용

- 기본 어미: "~합니다", "~드립니다", "~로 판단됩니다"
- 직급 호칭: 대표님/팀장님/부장님/차장님 (자동 매칭)
- 결재선 안내: 본 제안의 검토 일정 가이드 (예: "검토 후 7영업일 내 회신")
- 사인란: 자사 담당 + 고객사 결재자 2-3인 슬롯

### 5단계: Compelling 강화

- Executive Summary에 **정량 ROI 강제 삽입** (% 또는 원/시간 단위, 출처 명시)
- 출처 없는 수치는 `[추정]` 태그 강제
- 경쟁사 비교 시 객관 수치 인용 (가격, 기능 매트릭스)
- 고객사 도전 과제 → 자사 솔루션 직접 매핑

### 6단계: 후처리 가이드

산출 직후 다음 후속 단계를 사용자에게 안내합니다:

1. `ai-slop-reviewer`로 본문 검수 (CLAUDE.local.md §3-2 강제)
2. `docx-generator`(워드/PDF) 또는 `pptx-designer`(슬라이드) 출력
3. 견적서 분리 발행 시 `quote-generator` 호출
4. 발송 전 **반드시 사람이 최종 검토** (HubSpot Best Practice: Human-in-the-Loop)

## 출력 형식

```markdown
# [고객사명] 대상 [솔루션명] 도입 제안서

## 1. 표지
...
## 2. Executive Summary
...
## 12. 부록
...

---

## 📋 RFP 컴플라이언스 체크리스트
- [x] 페이지 한도 30p 이내
- [x] ISO 27001 인증서 첨부
- [ ] ❌ 보안 감사 보고서 (별도 첨부 필요)
- ...

## 🔍 다음 단계
1. ai-slop-reviewer로 본문 검수
2. docx-generator로 PDF 출력
3. 견적서 분리 발행 시 quote-generator
```

## 사용 예시

**예시 1 — RFP 답변 (전체 파이프라인)**
```
사용자: "이 RFP 답변 초안 만들어줘. 고객사는 ABC물류, 우리는 AcmeAI WMS 솔루션. 예산 5000만원/년."
→ proposal-writer 가 RFP 분석 + 12섹션 초안 + 컴플라이언스 체크리스트 생성
→ 이어서 ai-slop-reviewer → docx-generator 체이닝 안내
```

**예시 2 — 솔루션 제안서 (RFP 없이 자유 제안)**
```
사용자: "스타트업 XYZ에 우리 데이터 분석 SaaS 제안서 써줘. 가격 월 200만원."
→ proposal-writer 가 RFP 없이도 12섹션 표준 구조로 본문 생성
→ Executive Summary에 정량 ROI 자동 산정
```

## 주의사항

- **법적 책임 면제**: 본 스킬은 제안서 초안 보조이며, 최종 발송 전 사람이 검토해야 합니다
- **VAT 명시 필수**: 가격 섹션에 부가세 별도/포함 여부 자동 표시
- **NDA 정보 주의**: 고객사 NDA 대상 정보 포함 시 `nda-triage`(moai-legal) 체이닝 권고
- **AI 수치 검증**: 정량 데이터(ROI·시장 규모) 출처 없으면 `[추정]` 태그 강제
- **시간 추정 금지**: "1주 내 도입", "2-3개월 소요" 등 직접 시간 추정은 priority labels(P0/P1)로 변환

## 관련 스킬

**Before (입력 prep)**:
- `moai-business/market-analyst` — 고객사 산업·시장 분석 자료 prep

**After (출력 후처리)**:
- `moai-core/ai-slop-reviewer` — 본문 AI slop 검수 (필수)
- `moai-office/docx-generator` — Word/PDF 출력
- `moai-office/pptx-designer` — 슬라이드 출력
- `moai-sales/quote-generator` — 견적서 별도 발행

**Alternative (대체 스킬)**:
- `moai-business/investor-relations` — 투자자 대상 IR (B2B 고객 아님)
- `moai-business/kr-gov-grant` — 정부 지원사업 신청서 (B2B 영업 아님)

## 관련 커맨드

- `/harness` — 본 스킬 자체의 추가 개선·재생성
- (CLAUDE.local.md §3-3 등록 체인)
  - B2B 영업 제안서: `market-analyst → proposal-writer → ai-slop-reviewer → docx-generator`
  - B2B 영업 슬라이드: `market-analyst → proposal-writer → ai-slop-reviewer → pptx-designer`
  - 견적서 분리: `proposal-writer → quote-generator → xlsx-creator`

## 출처

- [HubSpot RFP Agent 가이드](https://knowledge.hubspot.com/ai-tools/set-up-and-use-the-request-for-proposal-rfp-agent) — Three C's, 콘텐츠 라이브러리 위생, Human-in-the-Loop
- [Inventive AI — Top 15 RFP Software 2026](https://www.inventive.ai/blog-posts/top-rfp-software-use) — 베스트 프랙티스 8개
- [GPTfy — Salesforce RFP AI 5-Phase](https://gptfy.ai/blog/improve-rfp-in-salesforce-with-ai) — Intake/Analysis/Preparation/Review/Approval
- [국세청 전자세금계산서 안내](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2460&cntntsId=7786) — VAT 표기 표준
- [Mordor Intelligence — 한국 B2B SaaS 2026-2031](https://www.mordorintelligence.kr/industry-reports/b2b-saas-market) — 시장 데이터