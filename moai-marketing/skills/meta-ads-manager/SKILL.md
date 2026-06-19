---
name: meta-ads-manager
description: |
  페이스북·인스타그램 광고를 자연어로 직접 만들고 켜고 끄고 예산까지 조정해 드립니다. Meta 공식 광고 AI 커넥터에 브라우저 로그인 한 번으로 연결되며, 신규 광고는 항상 꺼진(PAUSED) 상태로 만들고 켜기 전에 꼭 확인을 받습니다.
  다음과 같은 요청 시 사용하세요:
  - "메타 광고 만들어줘", "인스타 광고 캠페인 생성해줘"
  - "광고세트 추가해줘", "새 광고 소재 등록해줘"
  - "일예산 5만원으로 올려줘", "광고 예산 변경해줘"
  - "광고 켜줘", "광고 꺼줘", "캠페인 일시정지해줘"
  - "Meta 광고 운영해줘", "AI 커넥터로 광고 관리해줘"
  - "전환 픽셀 캠페인에 연결해줘", "광고 타겟이랑 소재 수정해줘"
  실제 계정에 변경을 적용하는 라이브 운영 스킬이라, 쓰기·예산·결제 동작은 실행 전에 항상 사용자 확인을 거칩니다.
  [책임 경계] vs meta-ads-analyzer·pixel-audit·campaign-planner: 이 스킬=실제 광고 생성·수정·온오프(쓰기), 저 스킬=보고서 분석·픽셀 설치 검증·캠페인 기획.
user-invocable: true
version: 2.27.0
---

# Meta 광고 운영 (Meta Ads AI Connectors)

Meta 공식 **Meta Ads AI Connectors**(한글: Meta 광고 AI 커넥터)에 연결해, 자연어로 Meta 광고를 직접 운영합니다. Ads MCP 서버와 Ads CLI로 구성되며 2026-04-29 오픈 베타로 공개되었습니다.

**책임 한 줄**: 이 스킬은 Meta 광고의 **라이브 운영(생성·수정·예산·온오프)** 만 담당합니다. 보고서 분석·진단·설치검증·기획은 형제 스킬이 맡습니다(아래 "형제 스킬 페어 분리" 참고).

---

## 1. 연결 / 셋업

### 1-1. OAuth 2.0 커넥터 흐름 (1차 · 권장)

공식 기본 인증 경로입니다. 앱 생성·앱 심사·토큰 수동 복사가 **필요 없습니다**. 클라이언트(Claude)가 Meta Business OAuth 로그인을 브라우저에서 수행하고 액세스 토큰을 자동 발급합니다.

- **엔드포인트**: `https://mcp.facebook.com/ads`
- **표준**: RFC 9728 Protected Resource Metadata + RFC 6750 Bearer
- **OAuth scope**: `ads_management ads_read catalog_management business_management pages_show_list`

#### A. Claude Cowork / Desktop (비개발자 1차 경로)

1. Settings → Connectors → **Add custom connector**
2. 이름 입력 + URL `https://mcp.facebook.com/ads` 입력
3. 브라우저가 열리며 **Meta Business OAuth 로그인** 진행
4. 광고 계정 / 페이지 선택 + 권한 등급 선택
5. 자연어 프롬프트로 연결 확인 (예: "내 광고 계정 목록 보여줘")

#### B. Claude Code (`.mcp.json`)

정적 Authorization 헤더를 넣지 않습니다. OAuth 커넥터 흐름이 인증을 처리합니다.

```json
{
  "mcpServers": {
    "meta-ads": {
      "type": "http",
      "url": "https://mcp.facebook.com/ads"
    }
  }
}
```

### 1-2. 정적 토큰 (Fallback · 강등됨)

OAuth가 불가한 개발 환경의 **fallback 전용** 경로입니다. 개발자/시스템 유저 토큰을 Graph API Explorer에서 발급해 `META_ACCESS_TOKEN` Bearer로 주입합니다. OAuth 보호 엔드포인트에는 일반 정적 Bearer가 403을 반환할 수 있으므로 **항상 OAuth를 먼저** 시도하고, 이 경로는 우선순위가 낮습니다.

- 토큰을 코드·SKILL.md에 **하드코딩 금지**
- 환경변수는 `${META_ACCESS_TOKEN}` 구문으로만 주입

---

## 2. 권한 등급

OAuth 로그인 중 사용자가 등급을 선택합니다. 쓰기·결제 동작은 **실행할 때마다 사용자 승인**이 필요합니다.

| 등급 | 범위 | 권장 |
|---|---|---|
| read-only | 조회·성과 분석만 | 시작 등급(권장) |
| read+write | 캠페인·광고세트·광고 생성/수정, 예산 조정 | 운영 시 |
| financial | 결제·청구 관련 동작 | 필요 시에만 |

권한 회수: Meta Business Suite에서 커넥터 접근을 철회합니다.

---

## 3. 워크플로우

1. **연결 확인** — read-only로 시작해 광고 계정·페이지 목록을 조회하고 대상을 확정한다.
2. **운영 의도 수집** — 목표(전환/트래픽/도달), 대상 광고 계정, 예산, 기간, 소재를 자연어로 받는다.
3. **생성/수정 제안** — 캠페인 → 광고세트 → 광고 구조로 변경안을 표로 제시한다. 신규 리소스는 **PAUSED** 상태로 만든다.
4. **사용자 승인** — 쓰기·예산·결제 동작은 실행 전 사용자에게 확인받는다(아래 안전 가드).
5. **실행** — 승인된 동작만 MCP로 실행하고 결과 ID·상태를 회신한다.
6. **검증/체이닝** — 필요 시 한국 시장 audit 또는 분석 스킬로 넘긴다(§7).

### 운영 가능 동작

- 캠페인 / 광고세트 / 광고 생성·관리·수정 (자연어)
- 예산 설정·조정 (일예산/총예산)
- 광고 소재(크리에이티브) 등록·교체
- 전환 픽셀 연결
- 성과 분석: spend / impressions / CTR / ROAS + breakdown

---

## 4. 안전 가드 (HARD)

| 가드 | 규칙 |
|---|---|
| 기본 PAUSED | 자연어로 생성한 신규 캠페인·광고세트·광고는 **항상 PAUSED**로 만든다. 자동 활성화 금지. |
| 활성화 승인 | 광고를 켜거나 지출을 시작하기 전 사용자 명시 확인을 받는다. |
| 쓰기 승인 | 모든 쓰기·예산·financial 동작은 실행 전 사용자 확인을 거친다(MCP도 동작별 승인 요구). |
| 토큰 비노출 | 토큰을 코드·SKILL.md·로그에 절대 출력·저장하지 않는다. |

승인 없는 자동 활성화·예산 증액·결제는 어떤 경우에도 수행하지 않습니다.

---

## 5. 트리거 키워드

라이브 운영 동사 중심입니다(분석·진단·검증·기획은 제외).

- 생성: "메타 광고 만들어줘", "캠페인 생성", "광고세트 추가", "새 광고 등록"
- 수정: "광고 타겟 수정", "소재 교체", "광고세트 변경"
- 예산: "예산 변경", "일예산 올려/내려"
- 온오프: "광고 켜줘", "광고 꺼줘", "일시정지", "캠페인 활성화/중지"
- 운영 일반: "Meta 광고 운영", "AI 커넥터로 광고 관리", "전환 픽셀 연결"

---

## 6. 입력 / 출력

**입력**
- 목표(전환/트래픽/도달/참여), 대상 광고 계정·페이지
- 예산(일/총), 기간, 타겟 조건, 소재(이미지·영상·문구)
- 권한 등급(read-only / read+write / financial)

**출력**
- 변경안 표(캠페인→광고세트→광고, 예산, 상태=PAUSED)
- 실행 결과: 생성된 리소스 ID·상태, 적용된 변경 요약
- 성과 조회 시: spend/impressions/CTR/ROAS + breakdown 표

---

## 7. 체이닝

- 마지막 단계에서 한국 시장 audit이 필요하면 **`moai-ads-audit` MCP**(자체 50-check) 또는 **`moai-marketing:meta-ads-analyzer`** 스킬로 체이닝.
- 운영 결과를 진단 텍스트 산출물로 정리하면 **`moai-core:ai-slop-reviewer` → `moai-content:humanize-korean`** 체이닝으로 AI 패턴 검수 + 한국어 AI 티 제거. (수치·대시보드 산출물은 대상 아님)

권장 체인 예:
```
meta-ads-manager (생성·운영)
  → moai-marketing:meta-ads-analyzer / moai-ads-audit MCP (진단)
  → moai-core:ai-slop-reviewer (진단 텍스트 검수)
  → moai-content:humanize-korean (한국어 AI 티 제거)
```

---

## 8. 형제 스킬 페어 분리

| 스킬 | 담당(책임) | 동사 성격 | 겹치지 않게 |
|---|---|---|---|
| **meta-ads-manager** (본 스킬) | Meta 광고 **라이브 운영** (공식 MCP) | 생성·수정·예산·온오프 | 운영 동사만 |
| meta-ads-analyzer | Meta 광고 보고서 **분석·진단** (read/report) | 분석·해석·리포트 | "분석/진단/리포트" 요청은 analyzer로 |
| pixel-audit | 픽셀·CAPI **설치 검증** | 점검·검증 | "픽셀 설치 확인"은 pixel-audit로 |
| campaign-planner | 캠페인 **기획**(인지편향) | 기획·설계 | "캠페인 기획/전략"은 planner로 |

판단 기준: "실제로 만들거나 바꾸거나 켜고 끄는가?"(=manager) vs "읽고 해석·검증·기획하는가?"(=형제 스킬).

---

## 9. 출처

- [Meta Business Help — Meta Ads AI Connectors](https://www.facebook.com/business/help/1456422242197840)
- [Meta for Developers — Introducing the Ads CLI (2026-04-29)](https://developers.facebook.com/blog/post/2026/04/29/introducing-ads-cli/)
- [Meta Business News — Meta Ads AI Connectors](https://www.facebook.com/business/news/meta-ads-ai-connectors/)
