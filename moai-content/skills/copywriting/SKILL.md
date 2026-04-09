---
name: copywriting
description: >
  카피라이팅 — 마케팅 카피, 헤드라인, CTA, 광고 캠페인, 비주얼 스토리텔링 하네스. 카피, 헤드라인, 광고 문구, 설득 카피.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 카피라이팅 (Copywriting)

> moai-content | 마케팅 카피 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| copywriting | 카피라이팅 | 마케팅 카피, 헤드라인, CTA 전문 |
| advertising-campaign | 광고 캠페인 | 미디어 플랜, 크리에이티브 전략, 성과 분석 |
| visual-storytelling | 비주얼 스토리텔링 | 시각 내러티브, 인포그래픽, 스토리보드 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

카피, 카피라이팅, 헤드라인, CTA, 광고 문구, 설득 카피, 마케팅 문구, 광고 캠페인, 슬로건

## 실행 규칙

1. 사용자 요청 수신 → 카피 유형 판별
2. `references/{id}.md` 로드 → 가이드에 따라 실행
3. `--deepthink` 또는 복잡 창작 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
