# init-protocol.md — /moai init 전체 플로우

## 개요
사용자의 MoAI 초기화 프로세스를 정의한다.
글로벌 프로필 구축 → 카테고리 선택 → 하네스 선택 → 맥락 수집 → CLAUDE.md 맞춤 생성까지 5단계.

**v0.2.0 핵심 변경:**
- `.claude/rules/` 생성 제거 → CLAUDE.md에 모든 내용 통합
- 언어 선택 Phase 제거 → 한국어 전용
- 로케일 Phase 제거 → 한국 전용
- CLAUDE.md에 하네스 전체 내용 복사 (축약 금지)

---

## Phase 0: 글로벌 프로필 감지

```
/mnt/.auto-memory/moai-profile.md 확인
├── [없음] → Phase 1로
└── [있음] → AskUserQuestion (1질문, 3옵션) ✅
    ┌─────────────────────────────┐
    │ header: "프로필"             │
    │ "기존 프로필을 발견했습니다.   │
    │  📌 이름: {name}            │
    │  📌 회사: {company}         │
    │  📌 역할: {role}            │
    │  어떻게 하시겠습니까?"       │
    │                             │
    │  ○ 재사용 (권장)             │
    │  ○ 업데이트                  │
    │  ○ 신규 생성                 │
    │  + Other                    │
    └─────────────────────────────┘
```

---

## Phase 1: 기본 프로필 수집

### Phase 1-A: 개인 프로필

AskUserQuestion 호출 (4질문) ✅

```
Q1 [역할]     "주요 역할은?"
  ○ 기획/PM  ○ 마케팅/콘텐츠  ○ 경영/전략  ○ 연구/분석
  + Other

Q2 [산업]     "산업 분야는?"
  ○ IT/테크  ○ 금융/핀테크  ○ 이커머스/리테일  ○ 교육/연구
  + Other

Q3 [사업형태] "사업 형태는?"
  ○ 개인사업자  ○ 법인  ○ 프리랜서  ○ 해당 없음
  + Other

Q4 [규모]     "조직 규모는?"
  ○ 1인  ○ 2~50인  ○ 51~200인  ○ 200인+
  + Other
```

→ 텍스트 대화로 추가 세부정보 수집 (이름, 회사명 등)

### Phase 1-B: 회사 프로필 (사업형태가 "해당 없음"이 아닌 경우)

AskUserQuestion 호출 (3질문) ✅

```
Q1 [업종]     "주요 업종은?"
  ○ 서비스업  ○ 제조업  ○ 유통/물류  ○ 기타
  + Other

Q2 [경력]     "해당 분야 경력은?"
  ○ 1년 미만  ○ 1~5년  ○ 5~10년  ○ 10년+
  + Other

Q3 [호칭]     "선호하는 호칭 스타일은?"
  ○ 격식 (존칭)  ○ 캐주얼  ○ 전문가 톤
  + Other
```

→ moai-profile.md 생성 + MEMORY.md 인덱스 등록

---

## Phase 2: 카테고리 선택 (2단계 분기)

### 대분류

AskUserQuestion (1질문, 4옵션) ✅

```
"어떤 분야의 전문가가 필요한가요?"

○ 콘텐츠 & 마케팅 (①콘텐츠 + ③마케팅)
○ 비즈니스 & 전략 (②비즈니스 + ⑨재무)
○ 전문 & 규제 (⑤법률 + ⑧운영 + ⑩제품)
○ 라이프 & 커뮤니케이션 (④교육 + ⑥라이프 + ⑦문서)
+ Other
```

### 소분류

선택된 대분류에 따라 AskUserQuestion (1질문, 2~4옵션) ✅

[예: "콘텐츠 & 마케팅" 선택 시]
```
"세부 분야는?"
○ 콘텐츠 & 크리에이티브 (유튜브, 영상, 카드뉴스)
○ 마케팅 & 성장 (SNS, 브랜딩, 이미지생성)
+ Other
```

---

## Phase 3: 하네스 선택 (페이지네이션)

선택된 스킬의 하네스를 4개씩 표시:

AskUserQuestion (1질문, 4옵션, multiSelect) ✅

```
[예: content-creative 선택 시]
"설치할 하네스를 선택하세요 (복수 선택 가능)"

☑ 유튜브 프로덕션 — 채널 운영 전과정
☐ 뉴스레터 엔진 — 뉴스레터 기획~발행
☐ 카피라이팅 — 마케팅 카피 전문
☐ 팟캐스트 스튜디오 — 팟캐스트 기획~배포
+ Other ("다른 하네스 더 보기")
```

하네스가 4개 초과 시 페이지네이션:
- Other → "더 보기" → 다음 4개 표시
- 전체 선택 완료 시 확인

---

## Phase 4: 심층 맥락 수집

AskUserQuestion (하네스별, 최대 4질문/호출) ✅
→ 참조: `context-collector.md`

[유튜브 프로덕션 예시]
```
Q1 [주제] "채널 주제는?"
  ○ 테크/리뷰  ○ 교육/강의  ○ 엔터/브이로그  ○ 비즈니스/재테크
  + Other

Q2 [규모] "현재 구독자 규모는?"
  ○ 0~1K  ○ 1K~10K  ○ 10K~100K  ○ 100K+
  + Other

Q3 [빈도] "업로드 빈도는?"
  ○ 주 1회  ○ 주 2~3회  ○ 월 2~3회  ○ 비정기
  + Other

Q4 [톤] "선호하는 소통 톤은?"
  ○ 격식/전문  ○ 캐주얼/친근  ○ 유머/재미  ○ 교육적/차분
  + Other
```

맥락 충분성 < 80% → 추가 호출 (최대 7회)

---

## Phase 5: CLAUDE.md 맞춤 생성 ★

### 생성 대상
```
<프로젝트>/
├── .claude/
│   └── CLAUDE.md          ← 맞춤형 (≤ 500라인)
└── .moai/
    ├── config.json        ← 하네스 ID, 버전, 설치일
    ├── context.md         ← 수집된 맥락
    └── evolution/
        ├── history.json
        └── reflections/
```

### CLAUDE.md 생성 규칙
1. **500라인 이내** — 맞춤형 지침 + 스킬 라우팅만 포함
2. **하네스 전체 복사 금지** — 하네스의 핵심 역할/목적을 2~3줄로 요약
3. 실행 시 해당 스킬의 `references/harness/{id}.md`를 **런타임에 로드**하여 상세 지침 확인
4. 사용자 프로필 정보를 페르소나에 반영
5. Phase 4에서 수집한 맥락을 도메인 맥락 섹션에 포함
6. 스킬 라우팅 테이블 포함 (어떤 작업 → 어떤 스킬)
7. sequential-thinking 사용 조건 명시

→ 참조: `claudemd-generator.md`

### config.json 예시
```json
{
  "harness_id": "youtube-production",
  "harness_version": "1.0.0",
  "installed_skill": "content-creative",
  "global_profile_ref": "/mnt/.auto-memory/moai-profile.md",
  "installed_at": "2026-04-08T15:30:00+09:00",
  "moai_version": "0.2.0",
  "context_sufficiency": "B",
  "evolution": {
    "cycle_count": 0,
    "last_evolved": null
  }
}
```

---

## --harness 옵션 (바로 설치)

```
/moai init --harness youtube-production
```

Phase 0 (프로필 감지) → Phase 2-3 스킵 → Phase 4 (맥락 수집) → Phase 5 (CLAUDE.md 생성)

---

## AskUserQuestion 제약 준수 요약

| Phase | 질문 수 | 옵션 수 | 제약 준수 |
|-------|---------|---------|----------|
| Phase 0 | 1 | 3 | ✅ |
| Phase 1-A | 4 | 4 | ✅ |
| Phase 1-B | 3 | 3~4 | ✅ |
| Phase 2 대분류 | 1 | 4 | ✅ |
| Phase 2 소분류 | 1 | 2~4 | ✅ |
| Phase 3 | 1 | 4 (multiSelect) | ✅ |
| Phase 4 | 최대 4 | 4 | ✅ |
