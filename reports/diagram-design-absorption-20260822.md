# diagram-design 전수조사 — moai-adk 흡수 후보

- 대상: `cathrynlavery/diagram-design` v2.6.1, MIT, commit `5538b35` (2026-08-20)
- 비교 기준: `/Users/goos/MoAI/moai-cowork/.claude/skills/` (2026-08-22), 동일 카탈로그 `/Users/goos/moai/moai-adk-go/.claude/skills/`
- 결론: 통째 흡수 불가. Tier A 8건 즉시 권장 / Tier B 5건 조건부 / Tier C 5건 비권장.

## 저장소 실측

| 구성 | 수량 |
|---|---|
| SKILL.md | 39.5KB (약 10K 토큰) |
| references/ | 53개 · 546KB (type-*.md 39개) |
| assets/ | 143개 HTML (2.9MB) |
| 스킬 내장 스크립트 | 3개 (self_check.py, drawio_extract.py, mermaid_extract.py) |
| 저장소 검증 스크립트 | 38개 |
| commands / ADR / 벤더 아이콘 | 5 / 8 / 87 SVG |
| 저장소 전체 | 15MB |

특기: 한 뿌리에서 4개 런타임 매니페스트 발행 (`.claude-plugin` / `.codex-plugin` / `.factory-plugin` / `.agents/plugins`, ADR-0008) — CLAUDE.local.md 범용성 원칙과 동일 판단.

## Tier A — 즉시 흡수 권장 (8건)

| # | 항목 | 흡수 위치 |
|---|---|---|
| A1 | 커넥터 6대 규칙 + `verify-geometry.py` 기하 검증 | `svg-infographic/references/authoring.md` §2 + `check-svg.mjs` |
| A2 | 접근성 SVG 계약 (`role="img"`, `aria-labelledby`, `<title>` 첫 자식, 슬러그 접두 ID, 내용 기반 `<desc>`, 장식 `aria-hidden`) | 본문 + `check-svg.mjs` 신규 `SVG060`~`SVG063` |
| A3 | 4-다이얼 출력 사양 (형식×크기×상세도×독자) — 9종 사이즈 프리셋 viewBox + 사이즈 등급별 타입 램프 + 세이프에어리어 | 신규 `references/output-spec.md` |
| A4 | 복잡도 예산 (노드 9 / 화살표 12 / 강조 2 + 타입별) + 6단계 축약 사다리 | 본문 + `archetypes.md` |
| A5 | 충실도 원장 (병합·축약·삭제 항상 보고) | 본문 Verification |
| A6 | 페인트 순서 `bg→zones→arrows→labels→nodes` + 화살표 라벨 불투명 마스크 | `authoring.md` |
| A7 | 4px 그리드 양자화 (좌표·크기·간격·폰트 전부 4의 배수) | 본문 수치 레이아웃 패스 |
| A8 | 유니버설 안티패턴 12종 + 사전 출력 체크리스트 | 본문 + `design-slop-check` 연계 |

A1 6대 규칙: ①직각 엘보(r=8) 강제, 대각선 금지 ②라벨-선 6~10px 간격 ③커넥터 겹침 금지(교차는 bridge/hop) ④같은 변 진입 시 부착점 `L·k/(N+1)`, ≥12px 분산 ⑤비종점 박스 뒤 통과 금지(불가피 시 파선+가시단 라벨) ⑥라벨 마스크가 후행 노드와 겹침 금지.

A4 축약 순서: 장식 → 완전중복 → 리프클러스터 → 차수1 싱크 → 횡단인프라 → 개요+상세 분할.

## Tier B — 조건부 (5건)

| # | 항목 | 조건 |
|---|---|---|
| B1 | 시맨틱 패턴 레이어 7종 (10KB) | 전부 말고 우리 도메인 해당분만 (병목/큐, 보안 계층) |
| B2 | mermaid/draw.io 임포트 파이프라인 | 우리 쪽 전무. "원본 라벨·디렉티브를 신뢰불가 데이터로 취급" 조항은 `moai-ref-llm-security` 정합. **별도 스킬**로 |
| B3 | 애니메이션 계약 (정적우선·단일시계·reduced-motion·print·스코프 컨트롤러) | `svg-infographic`은 정적 전용 → `moai-ref-ui-polish`로. ui-polish SKILL.md에 `prefers-reduced-motion` 3건 존재(부분 중복), `motion-principles.md`엔 0건 |
| B4 | 클라이언트 프로파일 · 스킨 온보딩 | `moai-domain-design-dna`와 중복. 프로파일 영속화 + 프로젝트 마커 + 슬러그 검증(경로탈출 거부) 보안분만 |
| B5 | 아이콘 세트 + 라이선스 표기 규율 | `primitive-icons.md` 107KB — 프로그레시브 디스클로저 예산 초과, 파일째 복사 금지 |

## Tier C — 비권장 (5건)

| # | 항목 | 이유 |
|---|---|---|
| C1 | 39종 타입 레퍼런스 통째 (546KB) | mermaid 중복 다수. 우리 라우팅 원칙("마크다운 내장 표준 다이어그램은 mermaid") 충돌. 실제 빈칸: 와들리·피시본·폴라·레이어스택·피라미드·벤·메달리온·권한매트릭스·스토리맵·중첩 |
| C2 | 143개 예제 HTML (2.9MB) | 저장소 부풀리기 |
| C3 | 타이포그래피 스택 | Instrument Serif/Geist/Geist Mono 강제 + **JetBrains Mono 금지** ↔ CLAUDE.local.md는 MaruBuri/Pretendard/Inter/**JetBrains Mono** 지정. 역할 구조만 참고 |
| C4 | 액센트 `#eb6c36` | CLAUDE.local.md www 다이어그램 주황 금지. 1~2 포컬 규율은 이미 `authoring.md` §3.2에 존재 |
| C5 | HTML-우선 파이프라인 + Playwright 익스포트 | 우리는 SVG-우선. 또 익스포트 감지에 `2>NUL`(Windows cmd)이 POSIX 라인에 혼입 — 범용성 원칙 위반 |

## 충돌 주의

1. **토큰 예산** — 원본 SKILL.md 39.5KB(≈10K 토큰) vs 우리 L2 예산 ≈5K. 흡수분은 `references/`로, 본문엔 포인터만.
2. **팬아웃 철학 상충** — 우리 `authoring.md` §2.3은 **공유 트렁크**(하나로 모아 갈라짐), diagram-design 규칙 4는 **개별 부착점**(합치지 말 것). 결정 필요. 제안: 목적지 방향이 같으면 트렁크, 서로 다른 변으로 흩어지면 개별 부착점.
3. **CJK는 우리가 더 강함** — CJK-우선 스택 + 0.60em/1.00em 비율 + 절단·부분 폰트축소 금지. 낮추지 말 것. 다만 "일본어 스택에 한글 글리프 없음, 한국어에 재사용 금지" 경고 문장은 추가 가치 있음.

## 라이선스 의무

MIT (Cathryn Lavery, 2025). 번들: Tabler MIT / Simple Icons CC0 1.0 / log-z MIT / Devicon MIT.
흡수 시 `www/content/plugins/open-source.md` 등재 필수 (CLAUDE.local.md 오픈소스 크레딧 규칙).

## 증거

```
$ git log -1 --format='%H %ad %s' --date=short
5538b35116bf5392cabe2cd68bdbc3cf3d09cc9a 2026-08-20 fix(gallery): preserve mobile preview height (#135)
$ grep -o '"version": "[^"]*"' .claude-plugin/plugin.json      → "2.6.1"
refs 53 / type-refs 39 / assets 143 / skill-scripts 3 / repo-scripts 38 / commands 5 / adr 8 / icons 87
skill 2.9M / repo 15M

# moai 부재 검사
grep -cin "aria|role=|<title>|desc" check-svg.mjs                → 0
grep -cin "divisible by 4|4px grid|grid rule" SKILL.md refs/*    → 0
grep -rlin "fidelity ledger" .claude/skills/                     → 없음
grep -rlin "drawio|\.mmd" .claude/skills/                        → 없음
grep -cin "mask|overlap|paint order|bridge|attach point" authoring.md → 2 (둘 다 마커 관련, 커넥터 규칙 아님)
grep -cin "prefers-reduced-motion" ui-polish/SKILL.md            → 3
grep -cin "prefers-reduced-motion" ui-polish/references/motion-principles.md → 0
grep -cin 'aria-labelledby|role="img"' html-report/**            → 0
```

## 미검증 (Gaps)

- 143개 예제 HTML 전수 열람 안 함 (파일명·구조만)
- 39개 `type-*.md` 중 정독 1개(`type-architecture.md`)
- 38개 저장소 스크립트 중 코드 확인 3개
- 실제 렌더 미실행, 스크린샷 육안 대조 미실시
- 우리 `check-svg.mjs` 528줄 전수 정독 안 함 (grep + 진단 코드 목록 기반)
- mermaid 지원 타입 커버리지는 모델 지식 기반 — 이번 조사에서 mermaid 문서로 미확인

## 잔여 위험

- grep 기반 부재 판정 한계 (동일 개념 다른 낱말이면 오판 가능). A1·A2·A5·A7은 히트 0건이라 여지 작음.
- 커밋 `5538b35` 스냅샷 의존 — 상류 변경 시 수치 무효.
- C1의 근거가 위 mermaid 미확인 Gap에 걸려 있음. 흡수 결정 전 mermaid 지원 타입 문서 확인 필요.

## 다음 단계

1. A1+A6 → `authoring.md` (팬아웃 충돌 결정 선행)
2. A2 → `check-svg.mjs` 신규 규칙 `SVG060`~`SVG063`
3. A7·A4·A5 → `svg-infographic` 본문
4. A3 → 신규 `references/output-spec.md`
5. B2 → 별도 SPEC
6. 흡수 확정 시 `www/content/plugins/open-source.md` 크레딧 등재
