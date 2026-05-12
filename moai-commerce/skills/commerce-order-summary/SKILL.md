---
name: commerce-order-summary
description: |
  [책임 경계] MCP order_summary_today 호출로 스마트스토어·카페24·아임웹 채널 통합 신규 주문을 대시보드 5개 → 1줄 통합 전담. 페어 moai-commerce:commerce-morning-brief(4개 영역 아침 브리핑)와 명확히 구분 — 본 스킬은 신규 주문 채널 통합 특화, 페어는 주문·문의·트렌드·ROAS 4개 영역 종합.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "신규 주문 통합해줘", "스마트스토어 카페24 아임웹 주문 합쳐줘", "채널별 주문 한눈에", "오늘 주문 몇 개야", "대시보드 5개 왔다갔다 그만하고 싶어", "order_summary_today", "채널 통합 주문 요약".
  ai-slop-reviewer 체이닝 제외 (MCP 채널 통합 숫자·데이터 1줄 통합 스킬).
  v2.3.0 신규 (Wave 3 — Day 1 S4·S5 라이브 시연).
user-invocable: true
version: 2.3.0
---

# 채널 통합 신규 주문 요약

## 개요

`order_summary_today` MCP 도구를 1회 호출하여 스마트스토어·카페24·아임웹 채널의 신규 주문을 통합 요약합니다. 대시보드 5개를 왔다갔다 하던 수고를 1줄로 압축하는 Day 1 라이브 시연 스킬입니다 (PDF §4.3 S4, REQ-SETUP-005).

**시연 매핑**
- Day 1 S4 14:25–14:45: 강사 라이브 충격 시연 (대시보드 5개 → 1줄)
- Day 1 S5 15:30–15:45: 수강생 실습 (본인 매장 ID로 직접 호출)

**합격 기준 (PDF §4.4 ④)**
채널 통합 신규 주문 1줄 요약 + .png 또는 .md 저장 확인.

---

## 트리거 키워드

신규 주문 통합, 채널 통합 주문, 스마트스토어 카페24 아임웹, order_summary_today, 대시보드 통합, 오늘 주문, 채널별 주문 합산, 주문 1줄 요약

---

## 워크플로우

### 입력 슬롯

| 슬롯 | 필수 여부 | 기본값 | 설명 |
|------|-----------|--------|------|
| `seller_id` | 필수 | 없음 | 셀러 매장 ID (Cowork 연결 매장) |
| `channels` | 선택 | 전체 채널 | 특정 채널만 조회 시 명시 (smartstore, cafe24, imweb) |
| `date` | 선택 | 오늘 날짜 (자동) | 조회 기준 날짜 |

### MCP 호출

```
MCP: order_summary_today
입력: { seller_id: "[매장_ID]" }
출력: 스마트스토어 + 카페24 + 아임웹 채널 통합 신규 주문 요약
```

### 처리 단계

1. `order_summary_today` MCP 1회 호출
2. 3채널 신규 주문 데이터 수신
3. 채널별 + 합산 집계
4. 1줄 통합 요약 생성
5. .md (또는 .png 스크린샷) 저장

> **ai-slop-reviewer**: 수치 데이터 스킬이므로 후처리 제외. 주문 건수·금액은 원본 데이터 보존.

### MCP Phase 1 미출시 상태 (REQ-SETUP-007)

MoAI eCommerce MCP Phase 1이 미출시 상태일 때:

> 현재 MoAI eCommerce MCP Phase 1은 출시 준비 중입니다.  
> 강사 사전 녹화 영상(5분)을 함께 시청해 주세요.  
> 수강생 베타 테스터 우선 배정 신청 가능합니다.

---

## 사용 예시

**예시 1 — 기본 호출**
> "오늘 주문 통합해줘"

```
MCP order_summary_today 호출 → 오늘 날짜 자동 설정
출력:
[2026-05-12 신규 주문 통합]
스마트스토어: 18건 · 카페24: 9건 · 아임웹: 5건 = 합계 32건 (₩4,820,000)
→ order-summary-20260512.md 저장
```

**예시 2 — 특정 채널만**
> "카페24 주문만 보여줘"

```
MCP order_summary_today 호출 → channels: ["cafe24"]
출력: 카페24 채널 신규 주문 요약
```

**예시 3 — 수강생 실습 (Day 1 S5)**
> "내 매장 ID shop_abc123 주문 통합 보여줘"

```
MCP order_summary_today 호출 → seller_id: "shop_abc123"
출력: 3채널 신규 주문 통합 1줄 → .md 저장
```

---

## 출력 형식

```markdown
# [날짜] 채널 통합 신규 주문

| 채널 | 신규 주문 | 금액 |
|------|-----------|------|
| 스마트스토어 | N건 | ₩N,NNN,NNN |
| 카페24 | N건 | ₩N,NNN,NNN |
| 아임웹 | N건 | ₩N,NNN,NNN |
| **합계** | **N건** | **₩N,NNN,NNN** |

> [1줄 요약]: 오늘 3채널 합산 N건, 총 ₩N,NNN,NNN
```

저장 경로: `본인_폴더/order-summary-YYYYMMDD.md`

---

## 합격 기준 (PDF §4.4 ④ + §3.2)

- 스마트스토어 + 카페24 + 아임웹 3채널 합산 요약 포함
- 대시보드 5개 → 1줄 통합 요약 형식
- .png 또는 .md 저장 확인

---

## 관련 스킬

- `moai-core:mcp-connector-setup` — 선행 조건: 3채널 OAuth 인증 완료 필요
- `moai-commerce:commerce-morning-brief` — 주문 외 문의·트렌드·ROAS까지 종합 브리핑
- `moai-commerce:commerce-integrated-strategy` — 주문 데이터 기반 운영 전략 수립

---

## 이 스킬을 사용하지 말아야 할 때

- 주문 외 문의·트렌드·ROAS 등 종합 매장 현황이 필요한 경우 → `moai-commerce:commerce-morning-brief` 사용
- 광고 채널(Facebook Ads, Google Ads) 전환 데이터가 필요한 경우 → 광고 분석 스킬 사용
- MCP 커넥터 인증이 완료되지 않은 경우 → `moai-core:mcp-connector-setup` 먼저 실행
- 외부 뉴스·시장 정보가 필요한 경우 → `moai-business:daily-briefing` 사용
