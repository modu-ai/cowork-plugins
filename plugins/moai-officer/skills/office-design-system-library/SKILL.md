---
name: office-design-system-library
description: |
  75개 글로벌 브랜드 디자인 시스템(Claude · ClickHouse · Clay 포함)의 토큰(색·타이포·radius·spacing·컴포넌트)을 단일 파일 HTML 산출물에 적용합니다.
  본 스킬은 moai-designer 플러그인의 정본(canonical)을 가리키는 포인터입니다 — 실제 시스템 토큰·컴포넌트 정의·샘플은 `moai-designer:design-system-library`에서 관리합니다(cowork 중복 사본은 경계 계약 "산출물=cowork, 체계=design"에 따라 제거됨).
  다음과 같은 요청 시 사용하세요:
  - "Claude 스타일로 HTML 보고서 만들어줘" / "브랜드 디자인 시스템 골라서 HTML로"
  - "Claude Design에 올릴 디자인 시스템 자료 정리"
version: "1.0.0"
---

# office-design-system-library — moai-designer 정본 포인터

본 스킬(`moai-officer:office-design-system-library`)은 **moai-designer 플러그인의 정본**을 가리키는 포인터입니다.

## 왜 포인터인가

디자인 시스템의 체계(systems) 관리는 design 플러그인의 책임입니다(경계 계약: "산출물=cowork, 체계=design"). 따라서 75개 브랜드 토큰의 정본(canonical) SSOT는 `moai-designer:design-system-library`에 있으며, 본 cowork 스킬은 하위 호환 라우팅/발견성만 담당합니다.

## 사용 방법

design_system 토큰이 필요하면 **`moai-designer:design-system-library`** 스킬을 직접 호출하세요. 토큰의 색·타이포·radius·spacing·컴포넌트 정의와 Tailwind Play CDN config 매핑, getdesign.md 상세 페이지 링크 모두 그곳에 있습니다.

## 연결

- 정본: `moai-designer:design-system-library` (75개 시스템 토큰 SSOT)
- 적용처: `moai-officer:office-html-report` · `moai-officer:office-html-slide` (design_system 파라미터로 토큰 로드)
- Claude Design 핸드오프: DESIGN.md 지침 소스는 정본에서 제공
