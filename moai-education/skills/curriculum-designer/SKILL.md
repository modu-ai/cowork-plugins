---
name: curriculum-designer
description: >
  커리큘럼 디자이너 — 강의 빌더, 어학 튜터, 역량 모델러 하네스. 커리큘럼 설계, 학습 목표, 온라인 강의 제작, 외국어 학습, 직무 역량 분석.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 커리큘럼 디자이너 (Curriculum Designer)

> moai-education | 교육 설계 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| course-builder | 강의 빌더 | 커리큘럼 설계, 학습 목표, 온라인 강의 제작 |
| competency-modeler | 역량 모델러 | 직무 역량 분석, 스킬 갭 파악, 성장 경로 |
| language-tutor | 어학 튜터 | 외국어 학습 전략, 회화 연습, 문법 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

강의, 커리큘럼, 온라인 교육, 학습 목표, 역량 모델, 스킬 갭, 외국어, 어학, 언어 학습

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 학술 분석 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
