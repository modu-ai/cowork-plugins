---
name: sns-content
description: >
  SNS 콘텐츠 제작 — 네이버 블로그, 인스타그램, 카카오 채널 등 한국 SNS 최적화 콘텐츠 생성. 브랜드 아이덴티티, 브랜드 보이스, 퍼스널 브랜딩, 콘텐츠 재활용 하네스.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# SNS 콘텐츠 제작 (SNS Content)

> moai-marketing | SNS 콘텐츠 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| brand-identity | 브랜드 아이덴티티 | 브랜드 전략, 로고 컨셉, CI/BI 가이드 |
| brand-voice-guide | 브랜드 보이스 가이드 | 톤 & 매너, 메시지 프레임워크 |
| content-repurposer | 콘텐츠 재활용 | 원 콘텐츠 → 다채널 변환, 리퍼포징 |
| personal-branding | 퍼스널 브랜딩 | 개인 브랜드 구축, 온라인 프레즌스 |

→ 하네스 파일: `references/{id}.md`

## 실행 모듈

### SNS 콘텐츠 제작
네이버 블로그, 인스타그램, 카카오 채널 등 한국 SNS 최적화 콘텐츠.
- 가이드: `references/sns-content/guide.md`
- 참조: `references/sns-content-creator/guide.md`

## 트리거 키워드

SNS, 인스타그램, 네이버 블로그, 카카오, 콘텐츠, 브랜딩, 퍼스널 브랜딩, 브랜드 보이스

## 실행 규칙

1. 사용자 요청 수신 → 하네스/실행 모듈 판별
2. 하네스 요청 → `references/{id}.md` 로드 → 전략 가이드 실행
3. 콘텐츠 요청 → `references/sns-content/guide.md` 로드 → 콘텐츠 생성
4. `--deepthink` 또는 복잡 작업 → `mcp__sequential-thinking__sequentialthinking` 호출
5. 결과물 생성 후 사용자 검토 요청
