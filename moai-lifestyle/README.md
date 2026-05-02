# moai-lifestyle

라이프스타일 플러그인 — 여행 플래닝, 건강/식단, 웨딩/이벤트.

국내외 여행 일정 설계, 운동/식단 코칭, 웨딩/세미나/워크샵 기획까지 라이프스타일 전반을 지원합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [travel-planner](./skills/travel-planner/) | 여행 일정/맛집/숙소/예산, 개인 재무, 부동산 분석, 사이드 프로젝트 | 4 | ✅ |
| [wellness-coach](./skills/wellness-coach/) | 운동 프로그램, 식단 플래너, 육아 가이드, 시니어 케어 | 4 | ✅ |
| [event-planner](./skills/event-planner/) | 웨딩 준비(스드메/예산/타임라인), 세미나, 워크샵, 컨퍼런스 기획 | 2 | ✅ |

## 사용 예시

```
5박 6일 오사카-교토 여행 계획 짜줘. 예산 80만원, 맛집 위주.
```

```
30대 직장인 다이어트 8주 식단 + 운동 플랜 만들어줘
```

```
50명 규모 사내 워크샵 기획해줘. 팀빌딩 액티비티 포함.
```

## 주요 워크플로우 체인

```
여행 풀 패키지
  travel-planner(일정·맛집·숙소·예산) → docx-generator(여행 가이드 PDF/Word)

다이어트·건강 8주 프로그램
  wellness-coach(식단·운동) → xlsx-creator(주차별 식단표) → docx-generator(가이드)

웨딩 준비 체크리스트
  event-planner(스드메·예산·타임라인) → xlsx-creator(예산 트래커) → docx-generator

사내 워크샵·세미나 기획
  event-planner(프로그램·예산) → pptx-designer(세미나 자료) → ai-slop-reviewer
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 사내 교육 커리큘럼·강의 | `moai-education/curriculum-designer` |
| 비즈니스 컨퍼런스 마케팅 | `moai-marketing/campaign-planner` |
| 부동산·재테크 (정량 분석) | `moai-data/data-explorer` |
| 헬스케어 의료 자문 | (전문가 상담 권장) |

## 한국 라이프스타일 환경 특화

- **국내 여행**: 한국관광공사 데이터, 지역별 맛집·축제 캘린더 반영
- **건강검진**: 국민건강보험공단 무료 검진 일정 자동 안내
- **결혼 표준**: 한국 결혼식 평균 비용·스드메 패키지·웨딩홀 가격대 가이드
- **아이 발달**: 영유아 검진 시기, 유치원·어린이집 등록 절차
- **시니어 케어**: 노인장기요양보험·노인복지관 서비스 안내

## 설치

Settings > Plugins > cowork-plugins에서 `moai-lifestyle` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
