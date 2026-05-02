# moai-product

제품 혁신 플러그인 — PM 로드맵, UX 리서치, 제품 스펙, AI 전략, 정부 지원금.

프로덕트 매니저를 위한 PRD 작성부터 UX 리서치, 로드맵 관리, AI/ML 도입 전략, R&D 지원금 신청서까지 제품 혁신 전 과정을 지원합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [spec-writer](./skills/spec-writer/) | PRD, 기능 명세서, AI/ML 전략 보고서, 정부 지원금(R&D/SBIR) 기획 | 3 | ✅ |
| [roadmap-manager](./skills/roadmap-manager/) | 프로젝트 트래커, 마일스톤, 파트너십 개발, MOU, ESG/DEI 전략 | 4 | ✅ |
| [ux-researcher](./skills/ux-researcher/) | 사용자 인터뷰, 유저빌리티 테스트, 페르소나, VOC/NPS 분석 | 2 | ✅ |
| [ux-designer](./skills/ux-designer/) | UX 디자인 분석 — 휴리스틱 평가(Nielsen 10), 접근성 검토(WCAG 2.2), 사용자 플로우 분석 (병렬 처리) | 1 | ✅ |

## 사용 예시

```
신규 기능 PRD 작성해줘. AI 기반 추천 시스템, 모바일 앱, 3개월 개발 일정.
```

```
우리 앱 사용자 인터뷰 가이드 만들어줘. 이탈률이 높은 온보딩 화면 개선이 목적이야.
```

```
R&D 과제 신청서 초안 작성해줘. AI 기반 문서 자동화 기술.
```

## 주요 워크플로우 체인

```
신규 기능 PRD → 출시
  spec-writer(PRD) → roadmap-manager(마일스톤·일정) → ux-researcher(검증 인터뷰) → docx-generator

UX 개선 풀 사이클
  ux-researcher(인터뷰·VOC) → ux-designer(휴리스틱·접근성·플로우) → spec-writer(개선 PRD) → ai-slop-reviewer

R&D 정부 지원금 신청
  spec-writer(R&D 기획) → moai-research/grant-writer(NRF/IITP 양식) → docx-generator

ESG·DEI 전략 수립
  roadmap-manager(ESG 로드맵) → moai-legal/compliance-check(ESG 보고) → docx-generator
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 사업계획서·시장조사 | `moai-business/strategy-planner` |
| Figma·웹 디자인 구현 | (별도 디자인 도구 — 본 플러그인은 분석·기획) |
| 데이터 분석·KPI 시각화 | `moai-data/data-visualizer` |
| 학술 연구 R&D | `moai-research/paper-writer` |

## 한국 제품 환경 특화

- **WCAG 2.2 + 한국 KWCAG 2.2** 접근성 표준 동시 적용
- **PRD 한국어 양식**: 배경·문제·요구사항·검수 기준·일정·의존성
- **R&D 정부 지원금**: NRF·IITP·KIAT·KISA 한국 R&D 양식 호환 (PRD → 신청서 변환)
- **ESG 한국 양식**: K-ESG 가이드라인 기반 보고
- **사용자 조사 한국 표준**: NPS·CES·CSAT 한국 표본 가이드

## 설치

Settings > Plugins > cowork-plugins에서 `moai-product` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
