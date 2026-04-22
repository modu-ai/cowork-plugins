---
title: "쿡북 홈"
weight: 1
description: "Cowork와 moai 플러그인을 실제 업무에 엮는 쿡북 — 시나리오·체인·프롬프트를 한곳에서."
geekdocBreadcrumb: true
tags: [cookbook]
---

# Cowork 쿡북

> Claude Cowork와 moai 플러그인을 **실제 업무에 어떻게 엮는지** 시나리오 묶음으로 정리한 쿡북입니다.

## 공통 포맷

각 예제는 다음 구성으로 제공합니다.

- **목표** — 최종 산출물
- **준비물** — 필요한 플러그인·API 키·입력 파일
- **스킬 체인** — 순서대로 호출되는 스킬
- **단계별 프롬프트** — 복붙 가능한 지시 예시
- **자주 겪는 이슈** — 실패 케이스와 우회법

## 먼저 읽으면 좋은 글

- [스킬 체이닝 가이드](./skill-chaining/) — 쿡북 전반에서 공통으로 쓰는 체인 패턴 입문
- [플러그인 빠른 시작](../plugins/quick-start/) — 마켓플레이스 등록부터 첫 호출까지

## 예제 목록

- [스킬 체이닝 가이드](./skill-chaining/) — 체인 설계 기초
- [베스트 프랙티스](./best-practices/) — 실패 패턴 10선, 프롬프트 점검표
- [자동화 레시피](./automation-recipes/) — 바로 쓰는 20개 체인 모음
- [블로그 파이프라인](./blog-pipeline/) — 초안→검수→썸네일
- [주간 보고서 자동화](./report-automation/) — 상태 집계→XLSX→DOCX
- [마케팅 트랙](./track-marketing/) — 브랜딩·SEO·캠페인 8주
- [문서 트랙](./track-documents/) — Office 산출물 자동화 8주
- [데이터 트랙](./track-data/) — 분석·공공데이터 8주
- [사업계획서 자동화](./business-plan/) — 전략→산업분석→PPT
- [IR 덱 제작](./ir-deck/) — 투자자 관점 슬라이드
- [계약서 검토 리포트](./contract-review/) — NDA 트리아지·리스크 점검
- [AI 사원 설계](./ai-employee-design/) — 역할→체인→KPI
- [AI 사원 실습 1 — 재무](./ai-employee-lab-1/) — 월말 마감 자동화
- [AI 사원 실습 2 — 품질·SCM](./ai-employee-lab-2/) — 이상 감지 알림
- [트러블슈팅](./troubleshooting/) — 체인 실패 진단·재시도
- [최종 프로젝트](./final-project/) — 본인 업무 1건을 체인으로

## 공통 원칙

- **텍스트 산출물은 무조건 `ai-slop-reviewer`로 마무리합니다.** 보고서·블로그·이메일·자소서·계약서 수정안이 모두 해당합니다.
- **숫자·차트·코드는 `ai-slop-reviewer`를 생략합니다.** 재무제표 엑셀, 차트 HTML, 스크립트는 검수 대상이 아닙니다.
- **포맷 변환은 `moai-office`에 위임합니다.** 내용 생성 스킬은 초안만 만들고 `docx-generator` / `xlsx-creator` / `pptx-designer` / `hwpx-writer`가 실제 파일을 만듭니다.
- **Windows 사용자는 파일명을 짧게 유지합니다.** MAX_PATH(260자) 제한 때문에 `보고서.docx`처럼 짧은 한글 이름을 권장합니다.

---

### Sources
- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [docs.claude.com — Cowork](https://docs.claude.com)
