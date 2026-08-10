# 컨설턴트 (moai-consultant)

경영·창업 컨설팅 전담 AI 코워커입니다. 사업계획서, 비즈니스 모델, 시장 분석(TAM/SAM/SOM), 경영 진단 브리프, 정부 지원사업 매칭, 상권분석 보고서까지 전략 실무 스킬 6종을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

**이런 분께 추천**: 예비 창업자 · 소상공인 · 스타트업 운영자

## 설치

`modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. **Claude Cowork**와 **ChatGPT Work** 두 데스크톱 앱 모두 같은 방식입니다.

**가장 쉬운 방법** — 설정(Settings) 또는 플러그인(Plugins) 메뉴 → 마켓플레이스(Marketplace)에서 주소 `modu-ai/moai-cowork`를 추가한 뒤, 플러그인 목록에서 `moai-consultant`를 찾아 **Install**을 누르세요.

**터미널에 익숙하다면 (대안)**

```bash
# Claude Cowork CLI
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-consultant@moai-cowork

# ChatGPT Work CLI
codex plugin marketplace add modu-ai/moai-cowork
codex plugin add moai-consultant@moai-cowork
```

> 앱별 정확한 클릭 경로와 잘 안 될 때 대처법은 [플러그인 설치와 관리](https://cowork.mo.ai.kr/plugins/install/)에 정리해 두었습니다.

## 스킬 6종

호출 형식: `/moai-consultant:business-<스킬명>` — 예: `/moai-consultant:consult-market`. 자연어 요청("시장 규모 조사해줘")으로도 자동 매칭됩니다.

### 전략·계획 (3종)

| 스킬 | 역할 |
|------|------|
| `consult-strategy` | 사업계획서·비즈니스 모델·신시장 진출 전략 (SWOT·린 캔버스·블루오션·OKR 프레임워크) |
| `consult-startup` | 아이디어→사업계획서·BM 캔버스·피치덱·재무 모델·실행 로드맵 스타트업 종합 계획 |
| `consult-brief` | 현황 진단 + 30-60-90일 실행 계획을 담은 전문 컨설팅 제안서(브리프) |

### 분석·지원사업 (3종)

| 스킬 | 역할 |
|------|------|
| `consult-market` | 시장 규모(TAM/SAM/SOM)·경쟁사 분석·가격 전략 시장 분석 보고서 |
| `consult-gov-grant` | 정부·공공기관 지원사업 매칭 + 심사 기준 맞춤 사업계획서·신청서 초안 (Word·한글·Excel) |
| `consult-sbiz365` | 소상공인365 상권분석 PDF 기반 유동인구·경쟁 점포·예상 매출 창업 타당성 보고서 |

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `strategy-consultant` | worker | 사업계획서·시장 분석·컨설팅 브리프·지원사업 신청서·상권 타당성 보고서를 만드는 실무 에이전트. 목표 이해 → 계획 → business-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 시장 데이터 출처 인용·TAM/SAM/SOM 산정 근거 명시·타당성 판단은 의사결정 보조·가정과 하방 시나리오 명시를 HARD 규칙으로 준수 |
| `feasibility-auditor` | read-only audit | 시장 규모 산식 재계산, 수치-출처 정합성, 지원사업 자격요건 매핑, 타당성 판정-근거 일관성을 회의적으로 검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 이관 안내

이 스킬들은 기존 `moai-coworker` 플러그인의 business 카테고리에서 경영·창업 컨설팅 도메인만 분리해 이관한 것입니다. moai-coworker의 구 경로로 호출하던 워크플로우는 `moai-consultant:` 네임스페이스로 갱신하세요.

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
