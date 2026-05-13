---
name: course-followup-sequence
description: |
  [책임 경계] 강의 후 30일 follow-up 시퀀스 — 후기 카피 5종 (D+1·D+3·D+7·D+14·D+30) + 인센티브·자산화 전담. 페어 moai-content:copywriting(일반 마케팅 카피)과 명확히 구분 — 본 스킬은 강의 30일 시퀀스 전용, 페어는 범용 마케팅 카피.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "강의 후기 카피 만들어줘", "D+1 후기 요청 카톡", "D+3 적용 인증 요청", "D+7 성과 수치 후기", "D+14 영상 후기 인센티브 안내", "D+30 심층 인터뷰 제안", "30일 후기 시퀀스", "강의 follow-up".
  체인: moai-content:copywriting → moai-core:ai-slop-reviewer → moai-content:korean-spell-check.
  v2.3.0 신규 (Wave 4 — moai-education 신규 활성화).
user-invocable: true
version: 2.5.0
---

# 강의 후 30일 Follow-up 시퀀스

## 개요

강의 종료 후 30일 동안 후기 수집·자산화를 자동화합니다. PDF §10 직접 인용:

> "강의 후에도 결과물·도구·후기 자산이 계속 흐르도록 30일 follow-up 시퀀스를 운영. 후기 카피 카톡 5종, SUNO BGM, MCP 직접 호출 가이드를 분리해 배포."

**체인 (REQ-FOLLOWUP-002, HARD)**
후기 카피 5종 생성 시: `moai-content:copywriting → moai-core:ai-slop-reviewer → moai-content:korean-spell-check`

체인 중 단계 누락 시 출력 거부합니다.

---

## 트리거 키워드

강의 후기 카피, D+1 후기 요청, D+3 적용 인증, D+7 성과 수치, D+14 영상 후기, D+30 심층 인터뷰, 30일 시퀀스, follow-up, 수강생 후기, 인센티브 안내, 후기 자산화

---

## 30일 시퀀스 전체 구성 (PDF §10.1 직접 인용)

| 시점 | 발송 콘텐츠 | 목적 | 인센티브 |
|------|-------------|------|----------|
| 당일 강의 종료 직후 | 감사 인사 + 결과물 zip 패키지 (Notion 공유 폴더) | 결과물 보관·복기 | — |
| D+1 | 후기 카피 카톡 5종 .md + 발송 가이드 | 후기 발송 자동화 | — |
| D+1 | 후기 요청 ① — 감사 + 첫 인상 후기 | 감정 정점에서 즉시 회수 | 우수 후기 다음 강의 노출 |
| D+3 | 후기 요청 ② — 적용 인증 사진·스크린샷 | 실제 사용 증거 | 추첨 1:1 코칭 30분권 |
| D+7 | 후기 요청 ③ — 성과 수치 공유 (시간·매출) | 정량 후기 | 다음 강의 5% 추가 할인 |
| D+14 | 후기 요청 ④ — 영상 후기 (1분 셀카) | 신뢰도 최상위 콘텐츠 | 다음 강의 10% 추가 할인 또는 멤버십 1개월 |
| D+30 | 후기 요청 ⑤ — 장기 변화 인터뷰 (지면) | 심층 사례 자산 | 차기 강의 무료 청강권 |
| D+7 (별도) | SUNO 광고 BGM 1편 만들기 가이드 + 디스코드 라이브 1회 | Day 3에서 빠진 옵션 보강 | — |
| D+14 (별도) | MoAI eCommerce MCP Phase 1 직접 호출 가이드 | V6 6개 도구 → MCP로 직접 | Phase 1 베타 테스터 우선 |

---

## 후기 카피 5종 톤·길이 가이드 (PDF §10.3 직접 인용)

| # | 시점 | 톤 | 목적 | 길이 |
|---|------|-----|------|------|
| ① | 당일 | 감사 + 따뜻한 | 즉시 후기 회수 | 3~5문장 |
| ② | D+3 | 격려 | 적용 인증 | 2~3문장 |
| ③ | D+7 | 자랑 유도 | 성과 수치 | 4~6문장 |
| ④ | D+14 | 인센티브 안내 | 영상 후기 | 3~4문장 |
| ⑤ | D+30 | 깊이 있는 인터뷰 제안 | 장기 변화 | 5~7문장 |

> **[HARD] 금지 (REQ-FOLLOWUP-009)**: 후기 카피에 시간 예측 표현 금지 — "2~3일 안에", "1주 후", "ASAP" 등. D+N 시퀀스 라벨(D+1, D+3, D+7, D+14, D+30)은 단계 식별자로 허용.

> **[HARD] PDF §10.3 운영 노트**: "사람이 보낸 메시지처럼 자연스럽게." ai-slop-reviewer 통과 필수 (REQ-FOLLOWUP-010).

---

## 워크플로우

### 호출 방법

```
/course-followup-sequence --day +1
/course-followup-sequence --day +3
/course-followup-sequence --day +7
/course-followup-sequence --day +14
/course-followup-sequence --day +30
/course-followup-sequence --day +14 --escalation premium   # 우수 후기 인센티브 강화
```

### 입력 슬롯

| 슬롯 | 필수 여부 | 기본값 | 설명 |
|------|-----------|--------|------|
| `--day` | 필수 | 없음 | D+N 시점 (+1, +3, +7, +14, +30) |
| `--course` | 선택 | 없음 | 강의명 (카피에 자동 삽입) |
| `--instructor` | 선택 | 없음 | 강사명 |
| `--escalation` | 선택 | 없음 | premium — 우수 후기 인센티브 강화 안내 포함 |

### 처리 체인 (HARD — REQ-FOLLOWUP-002)

```
Step 1: moai-content:copywriting → 시점별 톤·목적·길이 기준 후기 카피 초안 생성
Step 2: moai-core:ai-slop-reviewer → AI 패턴 제거, 자연스러운 사람 문체 검수
Step 3: moai-content:korean-spell-check → 맞춤법 검사
Step 4: .md 파일 저장 + 발송 가이드 출력
```

---

## 사용 예시

**예시 1 — D+1 후기 카피 생성**
> "강의 끝났어, D+1 후기 카피 만들어줘"

```
체인 실행: copywriting → ai-slop-reviewer → korean-spell-check
출력:
- followup-d1-review-request.md (후기 카피 ① 감사 + 따뜻한 톤, 3~5문장)
- 발송 가이드 (카톡 채널 / 알림톡 붙여넣기 형식)
```

**예시 2 — D+7 성과 수치 후기 + 인센티브**
> "D+7 후기 요청 카톡 만들어줘, 5% 할인 인센티브 포함"

```
체인 실행 → 자랑 유도 톤, 4~6문장, "다음 강의 5% 추가 할인" 인센티브 자동 포함
```

**예시 3 — D+14 영상 후기 (우수 후기 프리미엄)**
> "D+14 영상 후기 요청, 우수 후기 인센티브 강화해줘"

```
/course-followup-sequence --day +14 --escalation premium
→ "다음 강의 10% 추가 할인 또는 멤버십 1개월" 인센티브 자동 포함 (REQ-FOLLOWUP-007)
```

**예시 4 — D+7 별도 SUNO BGM 안내 (선택)**
> "D+7 SUNO BGM 가이드 같이 보내줘"

```
REQ-FOLLOWUP-011 옵션 활성화
→ "SUNO 광고 BGM 1편 만들기 가이드 + 디스코드 라이브 1회" 안내 카피 추가 출력
```

---

## 출력 형식

```markdown
# D+[N] 후기 요청 카피

## 카톡 발송용 (복사·붙여넣기)

[시점별 톤 적용 후기 요청 카피]

---

## 발송 가이드

- **채널**: [카톡 채널 / 알림톡 / 이메일]
- **발송 시점**: 강의 종료 후 D+[N]
- **인센티브**: [해당 인센티브 명시]
- **다음 시퀀스**: D+[N+] 시점에 [다음 후기 요청] 예정
```

저장 경로: `followup-d[N]-review-request.md`

---

## 합격 기준 (PDF §10.3)

| 항목 | 기준 |
|------|------|
| 후기 카피 ① (당일) | 감사 + 따뜻한 톤, 3~5문장 |
| 후기 카피 ② (D+3) | 격려 톤, 적용 인증 유도, 2~3문장 |
| 후기 카피 ③ (D+7) | 자랑 유도 톤, 성과 수치 포함, 4~6문장 |
| 후기 카피 ④ (D+14) | 인센티브 안내 톤, 영상 후기 유도, 3~4문장 |
| 후기 카피 ⑤ (D+30) | 인터뷰 제안 톤, 장기 변화 포착, 5~7문장 |
| 체인 통과 | copywriting → ai-slop-reviewer → korean-spell-check 3단계 완료 |
| 자연스러운 문체 | ai-slop-reviewer 통과 (사람이 쓴 것처럼) |
| AI 표현 금지 | 시간 예측 표현 없음 |

---

## 후기 자산 활용 (PDF §10.2)

- 우수 후기 → 다음 기수 모집 랜딩·블로그·SNS 1순위 자산
- 영상 후기 → 인스타·릴스·유튜브 쇼츠로 재가공 (`moai-media` 활용)
- 심층 인터뷰 → 블로그 사례 기사 (`moai-content:blog`) → SEO 누적

---

## 관련 스킬

- `moai-content:copywriting` — 체인 1단계: 후기 카피 초안 생성
- `moai-core:ai-slop-reviewer` — 체인 2단계: AI 패턴 후처리
- `moai-content:korean-spell-check` — 체인 3단계: 맞춤법 검사
- `moai-education:course-curriculum-design` — D-7 사전 준비물 메일 (선행 스킬)
- `moai-media` — D+30 영상 후기 재가공 (선택)
- `moai-content:blog` — D+30 심층 인터뷰 블로그 사례 기사 (선택)

---

## 이 스킬을 사용하지 말아야 할 때

- 강의와 무관한 일반 마케팅 후기·리뷰 카피 → `moai-content:copywriting` 직접 사용
- 강의 운영 매뉴얼·시간표·동선 설계 → `moai-education:course-curriculum-design` 사용
- 카톡 채널·알림톡 자동 발송 인프라 설정 → 외부 발송 도구 사용 (본 스킬은 카피·가이드 생성만)
- D+7 SUNO BGM 실제 생성 → SUNO MCP 도입 시 별도 스킬 (현재 안내 카피만 제공)
