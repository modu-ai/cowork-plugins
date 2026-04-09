---
name: assessment-creator
description: >
  평가 도구 제작 — 시험 대비, 문제 출제, 자격증 준비, 학습 평가 설계. 시험, 기출, 자격증, 수능, 문제 출제.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 평가 도구 제작 (Assessment Creator)

> moai-education | 시험/평가 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| exam-prep | 시험 대비 | 시험 전략, 학습 계획, 기출 분석 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

시험, 기출, 자격증, 수능, 문제 출제, 평가, 퀴즈, 학습 평가, 모의고사, TOEIC, TOEFL

## 실행 규칙

1. 사용자 요청 수신 → 시험/평가 유형 판별
2. `references/exam-prep.md` 로드 → 가이드에 따라 실행
3. `--deepthink` 또는 복잡 분석 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
