---
name: media-production
description: >
  미디어 프로덕션 — Remotion 영상 제작, 유튜브 프로덕션, 팟캐스트 스튜디오, 출판 기획, 콘텐츠 캘린더 하네스. 영상, 유튜브, 팟캐스트, 전자책.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 미디어 프로덕션 (Media Production)

> moai-content | 영상/팟캐스트/출판 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| youtube-production | 유튜브 프로덕션 | 채널 기획, 콘텐츠 전략, 촬영/편집 가이드, 알고리즘 최적화 |
| podcast-studio | 팟캐스트 스튜디오 | 팟캐스트 기획, 녹음, 편집, 배포 |
| book-publishing | 출판 기획 | 원고 기획, 출판 프로세스, 전자책 |
| content-calendar | 콘텐츠 캘린더 | 월간/주간 콘텐츠 일정 수립 및 관리 |

→ 하네스 파일: `references/{id}.md`

## 실행 모듈

### Remotion 영상 제작
React 기반 프로그래매틱 영상 생성 프레임워크.
- 가이드: `references/remotion-video/guide.md`
- 참조: `references/remotion-video/core-animation-rules.md`, `references/remotion-video/advanced-rules.md`, `references/remotion-video/media-rules.md`, `references/remotion-video/utility-rules.md`

## 트리거 키워드

영상, 유튜브, 팟캐스트, Remotion, 출판, 전자책, 콘텐츠 캘린더, 미디어 제작, 동영상

## 실행 규칙

1. 사용자 요청 수신 → 하네스/실행 모듈 판별
2. 하네스 요청 → `references/{id}.md` 로드 → 전략 가이드 실행
3. Remotion 요청 → `references/remotion-video/guide.md` 로드 → 코드 생성
4. `--deepthink` 또는 복잡 작업 → `mcp__sequential-thinking__sequentialthinking` 호출
5. 결과물 생성 후 사용자 검토 요청
