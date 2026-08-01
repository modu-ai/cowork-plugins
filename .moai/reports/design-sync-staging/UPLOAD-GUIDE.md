# Claude Design 업로드 가이드 (수동 폴백)

이 폴더(`design-sync-staging/`)는 **모두의AI 디자인 시스템**을 claude.ai/design에 등록하기 위한
스테이징 산출물이다. 자동 경로(DesignSync MCP)는 미인증 상태라 사용할 수 없으므로 수동으로 업로드한다.

## 경로 선택 사유 (자동 → 수동 강등)

- 감지 결과: DesignSync `list_projects` 호출 시 다음 에러 관측 →
  `DesignSync needs design-system authorization. Run /design-login to authorize it with your claude.ai account`
- 판정: **미인증 확정 → 자동 경로 포기 → 수동 폴백**. (미관측 인증을 성공으로 가정하지 않는다.)
- 이 폴더 전체를 사용자가 직접 claude.ai/design에 업로드한다.

## 대상 프로젝트

- **Design System 프로젝트 id**: `6fb4eb7f-4c8b-4814-a1ce-5b4deb0a7a37`
- 진입 경로: claude.ai/design → Organization settings → Design systems → 위 id의 프로젝트 선택
- 프로젝트 타입은 `PROJECT_TYPE_DESIGN_SYSTEM`이어야 하며, 쓰기 권한이 있어야 한다.

## 업로드 순서 (THIS 번들 기준)

1. **`DESIGN.md`** — 가장 먼저. 10섹션 디자인 시스템 요약(정체성·색·타이포·토큰 3계층·FROZEN 규칙·컴포넌트·자산).
2. **`tokens/`** — 아래 순서 유지:
   1. `tokens/02-tokens.json` — L1 DTCG SSOT (진실 원천)
   2. `tokens/colors_and_type.css` — L2 원시 CSS 변수
   3. `tokens/globals.css` — L3 shadcn semantic 롤 + Tailwind v4 `@theme` + `.dark`
3. **`assets/`** — 로고 변형 PNG (아래 매트릭스). 라이트/다크 쌍을 함께 올린다.
4. 참고 자산 — 이번 번들에는 별도 스테이징하지 않음(원본 `assets/reference/` 스크린샷은 민감정보는 아니나
   업로드 필수 아님).

> **모노레포 전체 업로드 금지** — 반드시 이 정리된 폴더만 올린다.

## 자산(로고) 변형 매트릭스

| 파일 | 변형 | 배경 | 용도 | v3.0 사용 여부 |
|---|---|---|---|---|
| `assets/moai-logo-4.png` | 가로형 | light | 헤더·네비 | 사용 |
| `assets/moai-logo-4-WH.png` | 가로형 화이트 녹아웃 | dark/gradient | 어두운 배경 헤더 | 사용 |
| `assets/moai-logo-1.png` | 정사각 | light | 파비콘·앱 아이콘·소셜 | 사용 |
| `assets/moai-logo-1-WH.png` | 정사각 화이트 녹아웃 | dark/gradient | 어두운 배경 정사각 | 사용 |
| `assets/moai-logo-2.png` | 카드 그라디언트 | light/gradient | 카드·공유 이미지 | 사용(보조) |
| `assets/moai-logo-2-1.png` | 카드 모노 | 임의 | 단색 카드·워터마크 | 사용(보조) |
| `assets/moai-logo-2-mono.png` | 카드 모노(e-ink 1비트) | e-ink/흑백 | e-ink·흑백 인쇄 | 사용(특수) |
| `assets/moai-logo-3.png` | 마스코트 메인 | soft | (v1.0) 히어로·빈상태·404 | **미사용(정체성 제거)** |
| `assets/moai-logo-5.png` | 마스코트 alt | soft | (v1.0) 마스코트 | **미사용** |
| `assets/moai-logo-6.png` | 글로벌 마스코트 | soft | (v1.0) 마스코트 | **미사용** |

- 마스코트 3종(logo-3/5/6)은 파일로 포함되어 있으나 **v3.0에서 사용하지 않는다**. 업로드 후 마스코트로
  해석·생성하지 않도록 DESIGN.md §9·§6의 정책을 함께 참고한다.
- 미제공 변형(예: SVG 벡터)은 "미제공"으로 두고 임의 생성하지 않는다.

## 폰트 라이선스 주의 (폰트 바이너리는 의도적으로 스테이징 제외)

- 이 폴더에는 **폰트 파일(.otf/.woff2)을 포함하지 않았다** — 라이선스 리스크 회피.
- 실제 폰트는 다음 경로로 로딩된다(코드에 이미 배선됨):
  - `Pretendard Variable` — jsDelivr CDN `orioncactus/pretendard@v1.3.9` dynamic-subset (SIL OFL)
  - `Inter Variable` — fontsource self-host / Google Fonts (SIL OFL)
  - `JetBrains Mono Variable` — fontsource self-host / Google Fonts (SIL OFL)
- claude.ai/design에는 **폰트 이름 + 로딩 방식(위)**만 전달하고 바이너리는 올리지 않는다. 셀프호스트가
  필요하면 각 폰트의 원 배포처에서 라이선스를 확인한 뒤 별도 반입한다.

## 민감 자산

- 이번 번들에는 고객 데이터·매출 수치가 박힌 자산이 없다(디자인 토큰·로고·문서만). 익명화 조치 불필요.

## Published 토글 절차

1. 위 순서로 폴더 업로드 후 **5–15분 분석 대기**(Claude Design이 자산을 흡수하는 시간).
2. UI 키트가 생성되면 테스트 프롬프트로 검증:
   - "AI 뉴스 상세 페이지를 디자인해 줘" (메뉴 3개·시그니처 그라디언트·4:5 카드 확인)
   - "AI 아카데미 강좌 상세 페이지" (CourseCard·청록 CTA 확인)
3. 결과가 브랜드와 일치하면 → **Published 토글 ON**.
4. 어긋나면 → Remix 하거나 누락 자산을 추가 업로드 후 재시도.
5. 검증 시 확인 포인트(FROZEN 위반 감지): `#000000`/`#ffffff` 배경 오용, 메뉴 4개 이상, 마스코트 등장,
   임의 그라디언트 각도 — 하나라도 나오면 DESIGN.md §6 규칙을 프롬프트에 재환기.

## 이후 자동 경로 전환

- Claude Code 터미널에서 `/design-login`으로 인증하면, 다음부터는 DesignSync MCP 자동 경로
  (`list/read → finalize_plan → write_files`)를 사용할 수 있다. 그 경우 이 수동 절차는 생략된다.

---

_수동 폴백 산출물 — `moai-designer:design-sync-upload` 템플릿 기준. 대상 프로젝트
`6fb4eb7f-4c8b-4814-a1ce-5b4deb0a7a37`._
