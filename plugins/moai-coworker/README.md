# 코워커 (moai-coworker)

실무 범용 코어 AI 코워커입니다. 브랜드·제안서·보고·협상·프로세스 관리 등 어느 업종에나 필요한 비즈니스 실무 스킬 30종을 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

**이런 분께 추천**: 1인 사업자 · 스타트업 운영자 · 실무 전반을 혼자 처리하는 분

## 전문가 플러그인으로의 분리 안내 (v6.0.0~v6.1.0)

기존 코워커의 전문 영역 스킬은 전문가 플러그인들로 이관되었습니다. 아래 표의 요청은 해당 플러그인을 설치하면 그대로 이어서 쓸 수 있습니다.

| 이런 요청은 | 이 플러그인으로 | 이관 스킬 |
|-------------|-----------------|-----------|
| 책·웹툰·웹소설·시나리오·IP | `moai-writer` (작가) | book-*, story-*, 한국어 윤문 (23종) |
| 캠페인·콘텐츠·SNS·미디어 생성 | `moai-marketer` (마케터) | marketing-*, content-*, media-* (28종) |
| 상세페이지·마켓·광고·CRM | `moai-seller` (셀러) | commerce-* (29종) |
| 오피스 문서·공공데이터·생산성 | `moai-officer` (사무관) | office-*, general 생활 (31종) |
| 계약·법령·판례·특허 | `moai-lawyer` (법무 담당) | legal-* (9종) |
| 재무제표·결산·세금·재테크 | `moai-accountant` (재무·세무 담당) | finance-* (11종) |
| 채용·스크리닝·평가·People Ops | `moai-recruiter` (인사·채용 담당) | business HR, 고용주 편 (6종) |
| 이력서·포트폴리오·면접 준비 | `moai-career` (커리어코치) | 구직자 편 커리어 (3종) |
| 커리큘럼·평가·논문 | `moai-tutor` (튜터) | education-* (11종) |
| 티켓 분류·응답 초안·에스컬레이션·지식베이스 | `moai-cs` (CS매니저) | 고객지원 business + commerce VOC (6종) |
| 사업계획·시장분석·지원사업·상권분석 | `moai-consultant` (컨설턴트) | 경영 컨설팅 business (6종) |
| Claude Design 브리프·시스템 준비·핸드오프 | `moai-designer` (디자이너) | cd-* (구 general-cd-* 5종) |

## 설치

`modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. **Claude Cowork**와 **ChatGPT Work** 두 데스크톱 앱 모두 같은 방식입니다.

**가장 쉬운 방법** — 설정(Settings) 또는 플러그인(Plugins) 메뉴 → 마켓플레이스(Marketplace)에서 주소 `modu-ai/moai-cowork`를 추가한 뒤, 플러그인 목록에서 `moai-coworker`를 찾아 **Install**을 누르세요.

**터미널에 익숙하다면 (대안)**

```bash
# Claude Cowork CLI
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-coworker@moai-cowork

# ChatGPT Work CLI
codex plugin marketplace add modu-ai/moai-cowork
codex plugin add moai-coworker@moai-cowork
```

> 앱별 정확한 클릭 경로와 잘 안 될 때 대처법은 [플러그인 설치와 관리](https://cowork.mo.ai.kr/plugins/install/)에 정리해 두었습니다.

## 스킬 30종

호출 형식: `/moai-coworker:<스킬명>` — 예: `/moai-coworker:collab-proposal`. 자연어 요청("제안서 써줘")으로도 자동 매칭됩니다.

### 전략·기획 (2종)

| 스킬 | 역할 |
|------|------|
| `collab-brand-identity` | 브랜드 아이덴티티 설계 |
| `collab-roadmap` | 로드맵·마일스톤 관리 |

### 문서·커뮤니케이션 (7종)

| 스킬 | 역할 |
|------|------|
| `collab-proposal` | 제안서 작성 |
| `collab-spec` | 요구사항·기획 명세 작성 |
| `collab-exec-summary` | 경영진 요약 보고 |
| `collab-status-report` | 진행 상황 보고 |
| `collab-pm-report` | PM 주간 보고 |
| `collab-productivity-report` | 생산성 주간 회고 |
| `collab-report-speak` | 보고 스피치 스크립트 |

### 고객·관계 관리 (5종)

| 스킬 | 역할 |
|------|------|
| `collab-conflict` | 갈등 상황 대응 |
| `collab-negotiation` | 1:1 협상 준비 |
| `collab-vendor` | 협력사·벤더 관리 |
| `collab-sales-playbook` | 영업 플레이북 |
| `collab-feedback-loop` | 피드백 수집·개선 루프 |

### 운영·UX (4종)

| 스킬 | 역할 |
|------|------|
| `collab-process` | 업무 프로세스 설계·개선 |
| `collab-meeting` | 회의 설계·퍼실리테이션 |
| `collab-ux-research` | UX 리서치 |
| `collab-ux-design` | UX 설계 |

### 품질·범용 도구 (7종)

| 스킬 | 역할 |
|------|------|
| `ai-slop-reviewer` | AI 티 나는 문장 검수 (모든 텍스트 산출물 마지막 단계) |
| `ai-diagnostic` | AI 산출물 품질 진단 |
| `meta-feedback` | 피드백 정리·반영 |
| `meta-skill-builder` | 커스텀 스킬 제작 |
| `meta-skill-template` | 스킬 템플릿 |
| `meta-skill-tester` | 스킬 테스트 |
| `ai-prompting-basics` | 클로드 프롬프팅 기본기 |

## MCP 연동 1종

| 서버 | 플랫폼 | 필요 환경변수 | 비고 |
|------|--------|---------------|------|
| `dart` | OpenDART 전자공시 (83 API → 15 도구) | `DART_API_KEY` | 시장·공시 분석에 사용 (`consult-market`는 `moai-consultant`로 이관됨). 키 발급: opendart.fss.or.kr (무료) |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
