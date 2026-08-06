---
name: media-asset-production
description: |
  (구명칭 호환 스텁) 콘텐츠 캘린더는 `moai-marketer:content-editorial-calendar`, 유튜브·팟캐스트 기획은 `moai-marketer:marketing-youtube-podcast-planner`로 분리됨. 직접 호출하지 않는다.
user-invocable: false
version: "1.1.0"
---

# 미디어 프로덕션 (별칭 → 분리됨)

`media-asset-production` 스킬은 산출물 단위로 두 개의 스킬로 분리되었습니다.
요청 성격에 따라 아래 스킬을 사용하세요.

- **콘텐츠 발행 캘린더·일정 기획** → `moai-marketer:content-editorial-calendar`
  - "콘텐츠 캘린더 짜줘", "이번 달 발행 일정 만들어줘", "채널별 게시 주기 정해줘"
- **유튜브·팟캐스트 에피소드 기획** → `moai-marketer:marketing-youtube-podcast-planner`
  - "유튜브 영상 기획해줘", "팟캐스트 에피소드 구성해줘", "쇼노트 만들어줘", "유튜브 대본 아웃라인"
