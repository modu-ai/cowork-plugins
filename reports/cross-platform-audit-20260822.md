# 크로스플랫폼 전수 조사 — 플러그인·스킬·MCP

조사일: 2026-08-22 · 대상: `main` @ `624a3a7d` · 방식: 정적 코드·문서 분석 (실제 Windows 실행 검증 없음)

## 조사 범위

| 항목 | 수량 |
|---|---|
| 플러그인 | 18 |
| 스킬 (SKILL.md) | 224 |
| 플러그인 `.mcp.json` | 12 |
| 자체 제작 MCP 서버 | 4 (+ 공유 코어 `moai-mcp-core` 1) |
| 에이전트 (`agents/*.md`) | 32 |

판정 기준: `CLAUDE.local.md` §범용성 원칙 — OS(macOS/Windows) × 런타임(Claude Cowork/ChatGPT Work) 4조합 동일 동작.

## 종합 판정

4조합 중 **macOS × Claude / macOS × Codex는 이상 없음**. Windows 축에서 실사용을 막는 결함 2건, 문서대로 따라 하면 실패하는 결함 2건 확인.

| 심각도 | 건수 | 영향 |
|---|---|---|
| 높음 | 2 | Windows에서 기능이 동작하지 않거나 설치 단계에서 막힘 |
| 중간 | 2 | Windows에서 문서대로 따라 하면 실패 |
| 낮음 | 4 | 동작 지장 없음 (정리·문서 대상) |

## 통과한 축 (근거 포함)

| 검사 | 결과 | 근거 |
|---|---|---|
| 매니페스트 쌍 (`.claude-plugin` ↔ `.codex-plugin`) | 18/18 양쪽 존재 | 파일 존재 전수 확인 |
| 플러그인 `.mcp.json` 런처 | `/bin/bash`·`sh -c` 0건 | `uv`/`uvx`/`npx`/원격 HTTP만 사용 |
| `args` 내 셸 연산자 (`&&`, 파이프, 백틱, `$(`) | 0건 | 12개 파일 grep 무매치 |
| 절대경로·`~`·`/tmp` 하드코딩 (`.mcp.json`) | 실행 필드 0건 | 유일 매치는 `moai-media` `$comment` 주석 |
| 자체 MCP 서버 경로 처리 | `pathlib.Path` + `Path.home()` | `moai_mcp_core/tokenstore.py:22`, `_base.py:28`/`:42` |
| 자체 MCP 서버 파일 인코딩 | `open()` 6건 전부 `encoding="utf-8"` | 명시율 6/6 |
| 자체 MCP 서버 `subprocess`/`shell=True` | 0건 | grep 무매치 |
| 자체 MCP 서버 경로 문자열 이어붙이기 | 0건 | 매치 3건은 스레드 번호(`f"{idx}/ "`), 경로 아님 |
| MCP 5축 작명 정합 | 4/4 일치 | 서버키·디렉터리·패키지명·모듈·엔트리포인트 |
| `hooks`/LSP/`output-styles` 생성 | 0건 | 데스크톱 앱 미지원 기능 미포함 |
| 스킬 224개 OS 전용 명령 | 3줄(1개 파일) | `doc-pdf/SKILL.md` 64·173·175 |
| `korean-humanize` CRLF 처리 | 명시적 정규화 구현 | `sanitize_text.py:91-93` |
| `uv` 설치 안내 Windows 커버 | 있음 (winget + PowerShell) | `www/content/plugins/mcp/install.md:27-39` |
| 토큰 저장 경로 OS별 안내 | 있음 | 같은 문서 113-115행 (`C:\Users\...\.moai\mcp\`) |

## 결함

### F-1 [높음] `doc-pdf` — Windows에서 PDF 렌더 실패

`weasyprint`는 Pango/GTK 네이티브 라이브러리에 의존한다. Windows는 GTK 런타임을 별도 설치해야 하는데 안내가 없다.

- 근거: `plugins/moai-officer/skills/doc-pdf/SKILL.md:175` — `cannot load library 'libpango...'` 대응 행이 Debian/Ubuntu·macOS 해법만 제시
- 근거: 같은 파일 `:64`, `:173` — CJK 폰트 설치 안내도 `brew` / `apt`만
- 영향: Windows 사용자가 "PDF로 만들어줘" 요청 시 모듈 로드 실패. 비개발자는 자가 진단 불가
- 조치: 트러블슈팅 표에 Windows 행 추가(GTK for Windows 런타임), 또는 Windows에서 headless Chromium 경로로 폴백

### F-2 [높음] Node.js 사전 준비 안내 부재

`npx`로 MCP 서버를 띄우는 플러그인 4종이 Node.js를 요구하나, 온라인 문서 어디에도 설치 안내가 없다.

- 해당 플러그인: `moai-accountant`, `moai-analyst`, `moai-coworker`, `moai-officer` (서버 `dart`, `kordoc`)
- 근거: `www/content` 전체 grep — `Node.js`/`nodejs.org` 매치는 `moai-agents/officer.md`와 아카이브 릴리스 노트뿐. 설치 문서 3종(`getting-started/install.md`, `plugins/install.md`, `plugins/mcp/install.md`) 모두 0건
- 대조: `uv`는 `plugins/mcp/install.md`에 macOS/Windows 양쪽 안내 완비 — 같은 수준의 Node.js 절이 없음
- 영향: Node.js 없는 머신에서 해당 MCP가 조용히 미기동. OS 축이 아닌 **양 OS 공통 결함**
- 조치: `plugins/mcp/install.md`에 "Node.js 설치" 절 추가(macOS: 공식 설치본, Windows: `winget install OpenJS.NodeJS.LTS`)

### F-3 [중간] `legal-iros-registry-automation` — POSIX 전용 명령

- 근거: `plugins/moai-lawyer/skills/legal-iros-registry-automation/SKILL.md:51` — `python3 -m venv .venv && source .venv/bin/activate`
- 문제 2가지: (a) `source .venv/bin/activate`는 POSIX 전용 — Windows는 `.venv\Scripts\activate`, (b) `python3` 명령명은 python.org Windows 설치본에 존재하지 않음(`python` / `py`)
- 조치: macOS/Windows 두 줄 병기

### F-4 [중간] `korean-humanize` SKILL.md — `python3` 5회

- 근거: `plugins/moai-writer/skills/korean-humanize/SKILL.md` 72·89·108·212·247행
- 문제: Windows python.org 설치본은 `python3.exe`를 만들지 않음 (Microsoft Store 배포본만 생성)
- 참고: 참조 스크립트 자체(`references/*.py` 6종)는 이식성 문제 없음 — `os.path` 기반, 인코딩 전부 명시, CRLF 정규화 구현
- 조치: `python3` → `python` (또는 `uv run python`)으로 통일

### F-5 [낮음] `doc-pdf` 폰트 `file://` URL 조립 — 잠복 결함

- 근거: `SKILL.md:81` — `f"src:url('file://{FONT_DIR}/NotoSansCJK-{n}.otf');}}"`
- 문제: Windows에서 `FONT_DIR`은 `C:\Users\...` 형태 → `file://C:\...`는 유효하지 않은 file URL(역슬래시, 슬래시 개수)
- 현재 미발화: `assets/fonts/`에 OTF 없음(`LICENSE.txt`·`README.md`뿐) → `.exists()` 가드가 항상 거짓
- 조치: 폰트를 번들하기 전에 `Path(...).as_uri()`로 교체

### F-6 [낮음] Codex 매니페스트가 `agents/`를 선언하지 않음 — 미검증

- 사실: 18개 플러그인 모두 `agents/*.md` 2개씩 보유(총 32개). `.codex-plugin/plugin.json`은 `"skills"`, `"mcpServers"`만 선언, `"agents"` 키 없음. `.claude-plugin/plugin.json`도 동일(Claude는 규약상 자동 탐지)
- **미검증**: Codex 런타임이 `agents/`를 자동 탐지하는지 실제 실행으로 확인하지 않음. 결함 여부 단정 불가
- 조치: Codex에서 플러그인 1종을 실제 로드해 에이전트 노출 여부 확인

### F-7 [낮음] `korean-slop-lint.sh` — 배포 패키지 내 bash 스크립트

- 근거: `plugins/moai-coworker/scripts/korean-slop-lint.sh` (실행 비트 있음, `#!/usr/bin/env bash`)
- 어떤 SKILL.md도 참조하지 않음 → 동작 영향 없음. 유지보수용 린트가 사용자 배포본에 포함된 상태
- 조치: 저장소 `scripts/`로 이동하거나 배포 제외

### F-8 [낮음] 문서 내 macOS 전용 표기 잔존

- `plugins/moai-media/.mcp.json:4` `$comment` — uv 설치 명령이 macOS/Linux 셸 형태만 (Windows 병기 없음)
- `plugins/moai-officer/skills/doc-html-slide/references/html-runtime.md:116` — `file:///...` 유닉스 형태 예시
- `plugins/moai-officer/skills/doc-html-slide/references/image-backend-policy.md:80` — `/tmp/hero.png`
- `plugins/moai-officer/skills/doc-html-report/references/design-tokens.md:10` — `/tmp/html-eff/`

## 참고 — 개발 저장소 한정 (사용자 영향 없음)

루트 `.mcp.json`의 `chrome-devtools`·`context7`·`playwright` 3종이 `command: "/bin/bash"` + `-l -c`를 사용한다. 이 파일은 개발 저장소 전용이며 마켓플레이스로 배포되지 않는다. 다만 §범용성 원칙 검사 명령이 이 파일에서 매치를 내므로, 검사 스코프를 `plugins/*/.mcp.json`으로 한정하거나 루트도 `npx` 직접 호출로 정리하면 검사 신호가 깨끗해진다.

## 미검증 (Gaps)

- 실제 Windows 머신에서의 설치·기동 검증 없음 — 전부 정적 분석
- Codex 런타임 실제 로드 검증 없음 (F-6 판정 보류 사유)
- 원격 HTTP MCP 8종(`higgsfield`, `meta-ads`, `korean-law`, `korean-stats`, `archhub`, `post-bridge`, `typefully`, `wordpress`) 실접속 미검증 — OS 무관하나 가용성은 확인 안 함
- 스킬 224개 전문을 읽지 않고 패턴 grep으로 스캔 — 패턴 밖 하자 존재 가능
- 제3자 MCP(`dart`, `kordoc`, `elevenlabs-mcp`)의 Windows 동작은 원저작자 책임 영역이며 검증하지 않음

## 잔여 위험

- `npx` 계열은 Node.js 유무에 따라 **조용히** 실패한다 — 에러 없이 도구 목록에서 빠지므로 사용자가 "이 기능이 원래 없나 보다"로 오인할 수 있음
- `uv`/`npx`는 첫 실행 시 패키지를 내려받으므로, 사내망·오프라인 환경에서는 OS와 무관하게 기동 실패

## 조치 우선순위

| 순서 | 항목 | 대상 |
|---|---|---|
| 1 | Node.js 설치 절 추가 | `www/content/plugins/mcp/install.md` |
| 2 | `doc-pdf` Windows 경로 보강 | `plugins/moai-officer/skills/doc-pdf/SKILL.md` |
| 3 | `python3` → `python` 통일 + venv 활성화 양 OS 병기 | `korean-humanize`, `legal-iros-registry-automation` |
| 4 | `file://` → `Path.as_uri()` | `doc-pdf/SKILL.md:81` |
| 5 | Codex `agents/` 탐지 실측 | 플러그인 1종 실제 로드 |
| 6 | 잔여 문서 표기 정리 | F-7, F-8 |
