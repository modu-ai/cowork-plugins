# moai-book

한국 출판사 제출용 원고 집필 풀스택 플러그인 — **도서 컨셉서 → 타깃 독자 → 목차 설계 → 저자 약력 → 출판 제안서 → 출판사 매칭 → 본문 챕터 집필 → 퇴고·교열**까지 8개 스킬로 출판 전 과정을 커버합니다.

[![버전](https://img.shields.io/badge/version-2.10.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-8-success)](#스킬)
[![장르](https://img.shields.io/badge/장르-4종-orange)](#장르-매트릭스)

**실용서·자기계발 · 인문·교양·에세이 · 기술·전문서·IT · 소설·문학** 4 장르를 모두 지원합니다. 각 스킬은 장르 프리셋으로 자동 분기하며, 한국출판문화산업진흥원(KPIPA) 통계·국립국어원 어문규범·도서정가제 등 한국 출판 컨텍스트를 내장합니다.

## 스킬

| 스킬 | 설명 | 단계 | 상태 |
|------|------|:----:|:----:|
| [book-concept-planner](./skills/book-concept-planner/) | 도서 컨셉서 — 한 줄/30자/300자/USP/시장 포지셔닝 | 1. 컨셉 | ✅ |
| [book-target-reader](./skills/book-target-reader/) | 타깃 독자 페르소나 + JTBD + 페인포인트 매트릭스 | 2. 독자 | ✅ |
| [book-outline-designer](./skills/book-outline-designer/) | 목차(부/장/꼭지) + 분량 배분 + 챕터 시놉시스 | 3. 목차 | ✅ |
| [book-author-bio](./skills/book-author-bio/) | 저자 약력 + 저자의 말 + SNS·강연 통합 | 4. 저자 | ✅ |
| [book-proposal-writer](./skills/book-proposal-writer/) | 출판사 투고용 제안서 (출판기획서 + 샘플 + 마케팅 플랜) | 5. 제안 | ✅ |
| [book-publisher-matcher](./skills/book-publisher-matcher/) | 한국 출판사 매칭 (장르·규모·계약·투고 채널) | 6. 매칭 | ✅ |
| [book-chapter-writer](./skills/book-chapter-writer/) | 챕터별 본문 초고 (꼭지 단위 집필·매수 관리·인용) | 7. 본문 | ✅ |
| [book-revision-coach](./skills/book-revision-coach/) | 퇴고·교열 (국립국어원 어문규범·문장 다듬기) | 8. 퇴고 | ✅ |

> ✅ v2.10.0 릴리스로 **8 스킬 풀 워크플로우 완성**. 모든 스킬 frontmatter v2.10.0 일관성 적용.

## 장르 매트릭스

각 스킬은 다음 4 장르 프리셋으로 자동 분기합니다.

| 장르 | 분기 지점 | 대표 출판사 | 본문 분량 가이드 |
|------|-----------|--------------|-----------------|
| **실용서·자기계발** | 시장 사이즈·경쟁작 분석·Q&A·실습 박스 | 웅진지식하우스·다산북스·길벗·메가스터디북스 | 250-350매 (200자 기준) |
| **인문·교양·에세이** | 서사·통일된 톤·서사 구조·인용·각주 | 민음사·문학동네·창비·은행나무·돌베개 | 300-500매 |
| **기술·전문서·IT** | 코드 예제·도표·실습 챕터·용어 사전 | 한빛미디어·인사이트·제이펍·길벗 IT | 400-800매 |
| **소설·문학** | 인물·플롯·시점·장면 묘사·문학상 응모 | 민음사·문학동네·창비·은행나무·문학과지성사 | 500-1500매 |

## 한국 출판사 매핑 요약

`book-publisher-matcher` 스킬이 제공하는 출판사 라이브러리(요약).

| 카테고리 | 출판사 예시 |
|----------|------------|
| IT·기술서 | 한빛미디어, 인사이트, 제이펍, 길벗 IT, 비제이퍼블릭, 영진닷컴 |
| 실용·자기계발 | 웅진지식하우스, 다산북스, 길벗, 메가스터디북스, 알에이치코리아, 흐름출판 |
| 인문·교양 | 민음사, 문학동네, 창비, 은행나무, 돌베개, 휴머니스트, 사계절, 푸른숲 |
| 문학·소설 | 민음사, 문학동네, 창비, 은행나무, 문학과지성사, 자음과모음, 안온북스 |
| 어린이·청소년 | 비룡소, 사계절, 창비, 문학동네 어린이, 길벗어린이 |

## 사용 예시

```
실용서 "30일 챌린지로 시작하는 부업" 도서 컨셉서 작성해줘
```

```
IT 입문서 "Next.js 15 + shadcn/ui 실전" 목차 설계해줘. 챕터 12개·분량 600매 기준.
```

```
민음사·문학동네에 투고할 에세이 출판 제안서 만들어줘. 샘플 챕터 1개 포함.
```

## 스킬 체이닝 권장 패턴

```
풀 워크플로우 (출판사 투고 준비)
  book-concept-planner → book-target-reader → book-outline-designer
  → book-author-bio → book-proposal-writer
  → book-publisher-matcher
  → moai-core:ai-slop-reviewer (제안서 검수)

본문 집필 + 퇴고
  book-chapter-writer (꼭지 단위 반복)
  → book-revision-coach
  → moai-content:korean-spell-check (맞춤법)
  → moai-content:humanize-korean (AI 티 제거)
  → moai-core:ai-slop-reviewer (최종 검수)
```

## 외부 참고 자료

| 출처 | URL | 용도 |
|------|-----|------|
| 한국출판문화산업진흥원(KPIPA) | [kpipa.or.kr](https://www.kpipa.or.kr) | 출판 통계·시장 동향·표준 양식 |
| 국립국어원 | [korean.go.kr](https://www.korean.go.kr) | 한글 맞춤법·외래어 표기·어문규범 |
| 교보문고 베스트셀러 | [kyobobook.co.kr](https://www.kyobobook.co.kr) | 장르별 시장 분석·경쟁작 조사 |
| 알라딘 도서 DB | [aladin.co.kr](https://www.aladin.co.kr) | 도서 메타데이터·ISBN |
| 도서정가제 안내 | [kpipa.or.kr](https://www.kpipa.or.kr) | 도서 가격·할인 규제 |

## 관련 플러그인 체이닝

- **moai-content:korean-spell-check** — 바른한글(부산대) 맞춤법 검수 (퇴고 후)
- **moai-content:humanize-korean** — AI 티 제거 정밀 윤문 (퇴고 후)
- **moai-content:blog** — 출간 기념 블로그 포스트
- **moai-marketing:campaign-planner** — 출간 마케팅 캠페인
- **moai-office:docx-generator** — 원고 DOCX 변환 (출판사 표준 포맷)
- **moai-office:pptx-designer** — 출간 기념 강연 슬라이드
- **moai-research:grant-writer** — 한국출판문화산업진흥원 지원사업 신청
- **moai-core:ai-slop-reviewer** — 모든 텍스트 산출물 마지막 검수 단계

## 설치

```
Settings > Plugins > cowork-plugins > moai-book
```

## 라이선스

MIT — `MoAI-Cowork-Plugins/LICENSE` 참조
