---
name: hwpx-writer
description: >
  한글 문서 생성 — OWPML 기반 한글(HWPX) 문서 생성/편집. python-hwpx + lxml 사용. 한글, hwpx, 아래한글, 한컴, 공문서, 기안서, 보고서.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "active"
  updated: "2026-04-09"
---

# 한글 문서 작성자 (hwpx-writer)

> moai-office v1.0.0 | python-hwpx 실행 모듈

## 참조 자료

- 작성 가이드: `references/guide.md`
- OWPML 스펙: `references/owpml-spec.md`

## 실행 스크립트

- `${CLAUDE_SKILL_DIR}/scripts/create_hwpx.py` — HWPX 생성
- `${CLAUDE_SKILL_DIR}/scripts/extract_text.py` — 텍스트 추출
- `${CLAUDE_SKILL_DIR}/scripts/extract_hwp.py` — HWP 변환
- `${CLAUDE_SKILL_DIR}/scripts/pack.py` — HWPX 패킹
- `${CLAUDE_SKILL_DIR}/scripts/unpack.py` — HWPX 언패킹
- `${CLAUDE_SKILL_DIR}/scripts/validate.py` — HWPX 검증

## 실행 규칙

1. 사용자 한글 문서 요청 수신
2. `references/guide.md` 로드 → python-hwpx 방법론 확인
3. `references/owpml-spec.md` 참조 → OWPML 구조 검증
4. 적절한 스크립트 실행 → HWPX 생성/편집
5. `--deepthink` 또는 복잡한 문서 구조 → `mcp__sequential-thinking__sequentialthinking` 호출
6. 결과물 생성 후 사용자 검토 요청

## 트리거 키워드

한글, hwpx, 아래한글, 한컴, 공문서, 기안서, HWP 변환, 한글 문서 생성
