---
name: pptx-designer
description: >
  PPT 디자인 — Pretendard+명조 기반 한국형 PPT 디자인. pptxgenjs 코드 생성. 슬라이드, 발표자료, 보고서 생성. PPT, 파워포인트, 발표, 슬라이드, 보고서, 기안서.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "active"
  updated: "2026-04-09"
---

# PPT 디자이너 (pptx-designer)

> moai-office v1.0.0 | pptxgenjs 실행 모듈

## 참조 자료

- 디자인 가이드: `references/guide.md`
- 코드 패턴: `references/pptxgen-code-patterns.md`
- 보고서 하네스: `references/report-generator.md`

## 실행 규칙

1. 사용자 PPT 요청 수신
2. `references/guide.md` 로드 → Pretendard+명조 디자인 시스템 적용
3. `references/pptxgen-code-patterns.md` 참조 → pptxgenjs 코드 생성
4. 보고서 요청 시 `references/report-generator.md` 추가 로드
5. `--deepthink` 또는 복잡한 슬라이드 구성 → `mcp__sequential-thinking__sequentialthinking` 호출
6. 생성된 코드 및 미리보기 사용자 검토 요청

## 트리거 키워드

PPT, 파워포인트, 발표자료, 슬라이드, 프레젠테이션, 보고서, 기안서, 피칭 덱
