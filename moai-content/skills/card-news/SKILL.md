---
name: card-news
description: >
  인스타 카드뉴스 — AI 이미지 생성 기반 캐러셀 카드뉴스 제작. 잡지 SOP, 디자인 가이드, AI 글쓰기 방지 기법 적용. 카드뉴스, 캐러셀, 인스타그램.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 카드뉴스 (Card News)

> moai-content | 인스타 카드뉴스 전문 스킬

## 실행 모듈

### 인스타 카드뉴스
AI 이미지 생성 기반 캐러셀 카드뉴스 제작.
- 가이드: `references/card-news/guide.md`
- 참조: `references/card-news/anti-ai-writing.md`, `references/card-news/magazine-sop.md`, `references/card-news/design-guide.md`
- 스크립트: `${CLAUDE_SKILL_DIR}/scripts/card-news/generate_image.py`

## 트리거 키워드

카드뉴스, 캐러셀, 인스타그램 카드, 슬라이드, AI 이미지, 카드 디자인, 인포그래픽 카드

## 실행 규칙

1. 사용자 요청 수신 → 카드뉴스 요청 확인
2. `references/card-news/guide.md` 로드 → SOP에 따라 실행
3. AI 이미지 생성 필요 시 → `scripts/card-news/generate_image.py` 활용
4. `--deepthink` 또는 복잡 작업 → `mcp__sequential-thinking__sequentialthinking` 호출
5. 결과물 생성 후 사용자 검토 요청
