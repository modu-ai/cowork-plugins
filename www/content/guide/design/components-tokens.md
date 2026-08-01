---
title: "컴포넌트·토큰 생성"
weight: 90
---

# 컴포넌트·토큰 생성

Claude Design이 디자인 시스템에서 색·타이포그래피·간격·컴포넌트를 자동 추출해 JSON으로 만듭니다. 이것이 "on-brand"를 유지하는 기계적 기반입니다.

## 핵심 토큰 종류

- **색상 토큰** (color tokens) — 브랜드 색을 코드로 쓸 수 있는 값으로 (예: `color-primary: #1a73e8`)
- **타이포그래피 규칙** (typography rules) — 글꼴·크기·줄간격
- **간격 토큰** (spacing tokens) — 여백 체계 (예: `spacing-md: 16px`)
- **재사용 가능한 컴포넌트** (버튼 등) — 코드로 직접 내보낼 수 있는 단위

## 토큰이 코드로 어떻게 쓰이나

추출된 토큰은 **이름→값 매핑의 JSON 구조**로 저장됩니다. Claude Design이 UI를 생성할 때 이 토큰을 참조하므로 브랜드 색·간격·글꼴이 모든 산출물에서 일관되게 유지됩니다. 이것이 "stays on brand"의 작동 원리입니다.

## 추출·편집 워크플로

1. 브랜드 자산·코드베이스·디자인 파일에서 디자인 시스템 **가져오기(import)**
2. Claude Design이 토큰·컴포넌트를 **자동 추출**
3. 미리보기 페이지에서 색견본·타이포그래피·JSON 컴포넌트 **검토**
4. 필요하면 값을 **편집(override)** 하거나 리믹스
5. 최종 시스템을 프로젝트에 **적용·내보내기**

## 컴포넌트 내보내기

재사용 컴포넌트(버튼·카드 등)는 코드 단위로 내보낼 수 있으며 Claude Code 핸드오프 시 토큰과 함께 전달되어 구현 단계에서 그대로 쓰입니다.

## Sources

- [Set up your design system in Claude Design (EN)](https://support.claude.com/en/articles/14604397)
- [Claude Design에서 디자인 시스템 설정하기 (KO)](https://support.claude.com/ko/articles/14604397)
