---
name: course-followup-sequence
description: |
  [책임 경계] 강사·교수·교사 대상 강의·수업·연수·워크숍·정규 강좌 종료 후 30일 follow-up 시퀀스 — 후기 카피 5종 (D+1·D+3·D+7·D+14·D+30) + 인센티브·자산화 전담. 페어 moai-content:copywriting(일반 마케팅 카피)과 명확히 구분 — 본 스킬은 수강생 후기 30일 시퀀스 전용, 페어는 범용 마케팅 카피.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "수강생 후기 카피 만들어줘", "D+1 후기 요청", "D+3 적용 인증 요청", "D+7 성과 수치 후기", "D+14 영상 후기 인센티브 안내", "D+30 심층 인터뷰 제안", "강의 후 30일 시퀀스", "수업 follow-up", "연수 후기 자산화".
  체인: moai-content:copywriting → moai-core:ai-slop-reviewer → moai-content:korean-spell-check.
user-invocable: true
version: 2.12.3
---

# 강의 종료 후 30일 Follow-up 시퀀스

## 개요

강사·교수·교사가 운영한 강의·수업·연수·워크숍이 끝난 뒤 **30일 동안 수강생 후기 수집·자산화**를 자동화합니다. 감정 정점에서 시작해 적용 인증, 성과 수치, 영상 후기, 심층 인터뷰까지 단계별로 회수해 다음 회차 모집·SEO·신뢰도 자산으로 누적합니다.

지원 범위:
- 단기 특강·워크숍 (1-3일)
- 사내 연수·집체교육
- 8-16주 정규 강좌
- 온라인 라이브·녹화 강의
- 대학·대학원 수업, 평생교육원·HRD 과정

**체인 (REQ-FOLLOWUP-002, HARD)**
후기 카피 5종 생성 시: `moai-content:copywriting → moai-core:ai-slop-reviewer → moai-content:korean-spell-check`

체인 중 단계 누락 시 출력 거부합니다.

---

## 트리거 키워드

수강생 후기 카피, 강의 후기 카피, D+1 후기 요청, D+3 적용 인증, D+7 성과 수치, D+14 영상 후기, D+30 심층 인터뷰, 30일 시퀀스, follow-up, 인센티브 안내, 후기 자산화, 수업 후기, 연수 후기

---

## 30일 시퀀스 전체 구성

| 시점 | 발송 콘텐츠 | 목적 | 인센티브 예시 |
|------|-------------|------|----------|
| 당일 강의 종료 직후 | 감사 인사 + 산출물·자료 공유 폴더 | 결과물 보관·복기 | — |
| D+1 | 후기 카피 5종 .md + 발송 가이드 | 후기 발송 자동화 | — |
| D+1 | 후기 요청 ① — 감사 + 첫 인상 후기 | 감정 정점에서 즉시 회수 | 우수 후기 차기 모집 페이지 노출 |
| D+3 | 후기 요청 ② — 적용 인증 사진·스크린샷 | 실제 사용 증거 | 추첨 1:1 코칭·멘토링 30분권 |
| D+7 | 후기 요청 ③ — 성과 수치 공유 (시간·매출·학습 효과) | 정량 후기 | 차기 강의 5% 추가 할인 |
| D+14 | 후기 요청 ④ — 영상 후기 (1분 셀카) | 신뢰도 최상위 콘텐츠 | 차기 강의 10% 추가 할인 또는 멤버십 1개월 |
| D+30 | 후기 요청 ⑤ — 장기 변화 인터뷰 (지면) | 심층 사례 자산 | 차기 강의 무료 청강권 |

> 인센티브 예시는 강좌 운영자가 자유롭게 커스터마이즈할 수 있습니다 (`--escalation premium` 등).

---

## 후기 카피 5종 톤·길이 가이드

| # | 시점 | 톤 | 목적 | 길이 |
|---|------|-----|------|------|
| ① | 당일 | 감사 + 따뜻한 | 즉시 후기 회수 | 3-5문장 |
| ② | D+3 | 격려 | 적용 인증 | 2-3문장 |
| ③ | D+7 | 자랑 유도 | 성과 수치 | 4-6문장 |
| ④ | D+14 | 인센티브 안내 | 영상 후기 | 3-4문장 |
| ⑤ | D+30 | 깊이 있는 인터뷰 제안 | 장기 변화 | 5-7문장 |

> **[HARD] 금지 (REQ-FOLLOWUP-009)**: 후기 카피에 시간 예측 표현 금지 — "2-3일 안에", "1주 후", "ASAP" 등. D+N 시퀀스 라벨(D+1, D+3, D+7, D+14, D+30)은 단계 식별자로 허용.

> **[HARD] 운영 노트**: "사람이 보낸 메시지처럼 자연스럽게." ai-slop-reviewer 통과 필수 (REQ-FOLLOWUP-010).

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
| `--course` | 선택 | 없음 | 강의·수업·연수 명칭 (카피에 자동 삽입) |
| `--instructor` | 선택 | 없음 | 강사·교수명 |
| `--channel` | 선택 | kakao | kakao / email / sms / discord — 발송 채널 |
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
- 발송 가이드 (채널별 붙여넣기 형식)
```

**예시 2 — D+7 성과 수치 후기 + 인센티브**
> "D+7 후기 요청 카톡 만들어줘, 5% 할인 인센티브 포함"

```
체인 실행 → 자랑 유도 톤, 4~6문장, "차기 강의 5% 추가 할인" 인센티브 자동 포함
```

**예시 3 — D+14 영상 후기 (우수 후기 프리미엄)**
> "D+14 영상 후기 요청, 우수 후기 인센티브 강화해줘"

```
/course-followup-sequence --day +14 --escalation premium
→ "차기 강의 10% 추가 할인 또는 멤버십 1개월" 인센티브 자동 포함 (REQ-FOLLOWUP-007)
```

**예시 4 — 사내 연수 D+3 (이메일 채널)**
> "사내 AI 연수 D+3 적용 인증 메일 만들어줘"

```
/course-followup-sequence --day +3 --course "사내 AI 연수" --channel email
→ 격려 톤 2-3문장 + 이메일 형식 가이드
```

---

## 출력 형식

```markdown
# D+[N] 후기 요청 카피

## 발송용 (복사·붙여넣기)

[시점별 톤 적용 후기 요청 카피]

---

## 발송 가이드

- **채널**: [카카오 / 알림톡 / 이메일 / 디스코드]
- **발송 시점**: 강의·과정 종료 후 D+[N]
- **인센티브**: [해당 인센티브 명시]
- **다음 시퀀스**: D+[N+] 시점에 [다음 후기 요청] 예정
```

저장 경로: `followup-d[N]-review-request.md`

---

## 합격 기준

| 항목 | 기준 |
|------|------|
| 후기 카피 ① (당일) | 감사 + 따뜻한 톤, 3-5문장 |
| 후기 카피 ② (D+3) | 격려 톤, 적용 인증 유도, 2-3문장 |
| 후기 카피 ③ (D+7) | 자랑 유도 톤, 성과 수치 포함, 4-6문장 |
| 후기 카피 ④ (D+14) | 인센티브 안내 톤, 영상 후기 유도, 3-4문장 |
| 후기 카피 ⑤ (D+30) | 인터뷰 제안 톤, 장기 변화 포착, 5-7문장 |
| 체인 통과 | copywriting → ai-slop-reviewer → korean-spell-check 3단계 완료 |
| 자연스러운 문체 | ai-slop-reviewer 통과 (사람이 쓴 것처럼) |
| AI 표현 금지 | 시간 예측 표현 없음 |

---

## 후기 자산 활용

- 우수 후기 → 차기 모집 랜딩·블로그·SNS 1순위 자산
- 영상 후기 → 인스타·릴스·유튜브 쇼츠로 재가공 (`moai-media` 활용)
- 심층 인터뷰 → 블로그 사례 기사 (`moai-content:blog`) → SEO 누적
- 정량 후기 → 사업계획서·IR·강의 소개서 신뢰 지표 (`moai-business:strategy-planner`)

---

## 관련 스킬

- `moai-content:copywriting` — 체인 1단계: 후기 카피 초안 생성
- `moai-core:ai-slop-reviewer` — 체인 2단계: AI 패턴 후처리
- `moai-content:korean-spell-check` — 체인 3단계: 맞춤법 검사
- `moai-education:course-curriculum-design` — 강의 운영 매뉴얼 (선행 스킬)
- `moai-media` — D+30 영상 후기 재가공 (선택)
- `moai-content:blog` — D+30 심층 인터뷰 블로그 사례 기사 (선택)

---

## 이 스킬을 사용하지 말아야 할 때

- 강의와 무관한 일반 마케팅 후기·리뷰 카피 → `moai-content:copywriting` 직접 사용
- 강의 운영 매뉴얼·시간표·동선 설계 → `moai-education:course-curriculum-design` 사용
- 카톡·알림톡·이메일 자동 발송 인프라 설정 → 외부 발송 도구 사용 (본 스킬은 카피·가이드 생성만)
- 학습 평가·시험 채점 → `moai-education:assessment-creator` 사용
