---
title: "Claude Cowork 한국어 문서"
description: "Claude Cowork 한국어 가이드 — 지식 근로자를 위한 설치·스킬·플러그인·쿡북 완전판. cowork-plugins 17종 카탈로그 포함."
geekdocNav: false
geekdocAlign: center
geekdocAnchor: false
geekdocBreadcrumb: false
---

# Claude Cowork 한국어 문서

**지식 근로자를 위한 Claude Code** — Claude Cowork의 공식 개념, 설치, 플러그인 활용법을 한국어로 정리한 커뮤니티 문서입니다.

원문은 [Anthropic 공식 문서](https://docs.claude.com)와 [`modu-ai/cowork-plugins`](https://github.com/modu-ai/cowork-plugins) 저장소이며, 본 사이트는 이를 쉽게 따라갈 수 있도록 한국어로 재구성했습니다.

> **15분 안에 첫 산출물, 2시간 안에 실무 체인, 1주 안에 사내 표준.**

## 당신은 어떤 학습자인가요?

{{< columns >}}

### P1 · 일반 지식 근로자

기획·마케팅·문서 업무 담당. Cowork가 처음이라면 8주 코스의 Week 1부터 시작하세요.

[**Cowork 소개부터 →**](cowork/intro/)

<--->

### P2 · 플러그인 파워 유저

Cowork 기본은 알고 있음. 스킬 체인 설계와 AI 슬롭 제거 루틴을 바로 익히세요.

[**스킬 체이닝 가이드 →**](cookbook/skill-chaining/)

<--->

### P3 · 팀 도입 담당자

IT·팀장·총무. 요금제·권한·감사 로그·도입 제안서 관점으로 훑어봅니다. (※ Cowork를 처음 쓴다면 P1 카드로 시작하세요.)

[**Team·Enterprise 관리 →**](cowork/enterprise/)

{{< /columns >}}

## 카탈로그로 바로 이동

{{< columns >}}

### Cowork 가이드

Cowork가 무엇인지, 설치·프로젝트·메모리·스킬·플러그인 기본을 한국어로 안내합니다.

[**가이드 보기 →**](cowork/intro/)

<--->

### 플러그인 카탈로그

`modu-ai/cowork-plugins`의 17개 플러그인과 73개 스킬을 도메인별로 모아봤습니다.

[**카탈로그 보기 →**](plugins/)

<--->

### 쿡북

사업계획서, IR 덱, 블로그 발행 파이프라인 같은 실전 예제를 스킬 체인으로 정리했습니다.

[**쿡북 보기 →**](cookbook/)

{{< /columns >}}

## 3분 요약

1. **Cowork란** — Claude Desktop 앱 안에서 작동하는 비개발자용 작업 자동화 환경입니다. 로컬 폴더에 접근해 문서를 읽고 결과물을 저장하며, 서브에이전트로 긴 작업을 분할 수행합니다.
2. **스킬과 플러그인** — 스킬(skill)은 "이런 상황에서는 이렇게 해라"라는 절차적 지침 묶음이고, 플러그인(plugin)은 스킬·커넥터·서브에이전트를 하나의 도메인으로 묶어 배포하는 단위입니다.
3. **cowork-plugins** — 한국 업무 환경에 최적화된 MoAI 플러그인 마켓플레이스로, 사업계획·마케팅·법무·재무·HR·콘텐츠·오피스·미디어 등 17개 도메인 플러그인을 제공합니다.
4. **스킬 체인** — 여러 스킬을 순서대로 엮어 한 요청을 처리하는 방식입니다. 예: `strategy-planner → docx-generator → ai-slop-reviewer`는 사업계획서 작성 → Word 저장 → AI 티 제거 파이프라인입니다. 자세한 구조는 [쿡북 › 스킬 체이닝 가이드](cookbook/skill-chaining/)에서 다룹니다.

## 5분 설치·실행

1. **Claude Desktop 설치** — [claude.com/download](https://claude.com/download)에서 Mac/Windows 앱 다운로드 후 로그인
2. **마켓플레이스 등록** — Cowork 좌측 하단 **사용자 지정 → 개인 플러그인 → 마켓플레이스 추가**에 `modu-ai/cowork-plugins` 입력
3. **`moai-core` 설치** — 목록에서 `moai-core`의 **+** 버튼 클릭. 이걸 먼저 설치해야 `/project init`과 AI 슬롭 검수가 동작합니다
4. **`/project init` 실행** — 작업 폴더와 연결한 뒤 대화창에 `/project init` 입력, 7단계 인터뷰 응답
5. **첫 요청** — `"SaaS Series A용 IR 덱 초안 만들어줘"` 같은 자연어 요청을 보내면 체인이 자동 실행됩니다

자세한 단계는 [플러그인 빠른 시작](plugins/quick-start/) 참고.

## 최근 업데이트

- **2026-04-23** Hugo + Geekdoc로 사이트 재구축, `cowork.mo.ai.kr` 도메인 연결 준비
- **2026-04-21** v0.2 커리큘럼형 전환 시작 — 페르소나 3카드, 용어집·FAQ·트러블슈팅·최종 프로젝트 신설
- **2026-04-20** 사이트 초안 공개 · Cowork 11페이지 · 플러그인 카탈로그(17) · 쿡북 7편

## 이 문서에 대하여

- 모든 페이지 하단에 **공식 원문 URL(Sources)**을 표기합니다.
- 한국어 용어는 공식 원어와 병기합니다: 스킬(skill), 플러그인(plugin), 워크플로우(workflow).
- 오류 제보·기여는 [GitHub Issues](https://github.com/modu-ai/cowork-plugins/issues)로 보내주세요.

---

### Sources

- [Claude Cowork 제품 페이지](https://claude.com/product/cowork)
- [Cowork research preview (blog)](https://claude.com/blog/cowork-research-preview)
- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
