# components/ — shadcn vanilla 컴포넌트 참조 마크업

이 디렉토리는 shadcn UI 컴포넌트를 React 없이 **vanilla HTML + Tailwind utility class**로 재현한 참조 마크업을 보관합니다. 단일 파일 HTML 산출물(html-report 등)에서 `design_system` 토큰과 함께 카드·버튼·테이블 등을 칠할 때 참조합니다.

## 현재 상태 (v2.22.0)

초기 릴리스에서는 본 디렉토리에 별도 마크업 파일을 두지 않고, **[`../SKILL.md`](../SKILL.md) § shadcn vanilla 컴포넌트**의 매핑 표(Card · Button · Badge · Table · Tabs · Alert → `div.rounded-lg.border.p-8` + token classes 형태)와 [`../samples/`](../samples/)의 렌더 샘플 3종(`status-claude` · `status-clickhouse` · `status-clay`)을 1차 참조원으로 사용합니다.

## 후속 확장 (예정)

브랜드 시스템별로 자주 쓰이는 컴포넌트(Card · Button · Badge · Table · Tabs · Alert · Input · Dialog)의 vanilla 마크업 스니펫을 개별 파일로 추가할 예정입니다. 토큰은 [`../systems/`](../systems/)의 YAML frontmatter(`colors` · `typography` · `rounded` · `spacing`)를, Tailwind 매핑 규칙은 [`../mapping/tailwind.md`](../mapping/tailwind.md)를 따릅니다.

## 원칙

- React · Vue · 빌드 단계 없이 **단일 파일 HTML** 안에서 동작하는 마크업만 둡니다
- Tailwind Play CDN(`cdn.tailwindcss.com`)을 전제로 한 utility class + token class 조합
- 0의존 self-contained 출력이 필요한 경우(이메일 첨부 · 오프라인 · 인쇄)는 `design_system`을 지정하지 않고 기존 html-report 0의존 템플릿을 사용하세요
