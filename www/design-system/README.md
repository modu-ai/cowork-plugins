# 디자인 시스템 (SSOT)

이 폴더는 **모두의AI Design System v2**의 단일 기준(SSOT)이다.
`www/static/moai-ds-*.css`는 이 기준의 **구현체**이며, 값이 어긋나면 언제나 `handoff/`가 이긴다.

## 구성

| 파일 | 역할 |
|---|---|
| `handoff/colors_and_type.css` | 색·타이포·자간·반경·여백·모션 토큰 원본 |
| `handoff/모두의코워크 사이트.dc.html` | 사이트 화면 설계 원본 — 헤더 64px, 문서 3단 셸(264/본문/200, gap 36), 히어로, 본문 블록 12종, 푸터의 측정값 |
| `handoff/MoAI-Cowork 문서.dc.html` | 문서 페이지 변형 설계 |
| `handoff/README.md` | 브랜드 보이스·비주얼 규칙·마스코트 사용 규칙 |
| `handoff/_ds_manifest.json` | Claude Design 프로젝트 매니페스트 |

출처: Claude Design 프로젝트 `MoAI-Cowork 온라인 문서 디자인` 핸드오프 (2026-07-27 내보내기).

## 핵심 규칙 요약

- **색**: 마스코트 포인트 그린 `#3d7d5f` 단일 강조 + 순수 무채색(hue 0%). 주황·퍼플·마젠타 금지.
- **폰트**: Pretendard(sans) · Inter(라틴) · JetBrains Mono(mono) — **전부 CDN**. 셀프호스팅 `@font-face` 금지.
  (핸드오프에 Pretendard OTF 9종이 동봉돼 있으나 용량 문제로 CDN으로 대체한다.)
- **반경**: sm 4 / md 8 / lg 16 / xl 24 / pill 32.
- **그림자**: outer only. 그라디언트 + shadow 동시 적용 금지.
- **카드 hover**: `translateY(-2px)` + `shadow-md`.
- **마스코트**: 히어로·빈 상태·404 같은 정서적 표면에만. 데이터 표·폼·결제 화면 금지.
- **이모지**: UI 카피에서 사용 금지 — 마스코트와 Lucide 아이콘이 대신한다.

세부 운용 규칙은 저장소 루트의 `CLAUDE.local.md` § 디자인 시스템 규칙 참조.
