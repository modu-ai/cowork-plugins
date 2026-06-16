# Design System Registry — 56개 브랜드 카탈로그

본 레지스트리는 `design-system-library`의 56개 디자인 시스템에 대한 인덱스입니다. 
각 시스템의 상세 토큰은 `systems/<name>.md`에 있습니다. 
canvas 휘도(R+G+B 평균) 기반 자동 분류: `<100` dark · `<232` warm · 그 외 light.

---

## 상태 표기

- ✅ **완료** — `systems/<name>.md` 존재, frontmatter 토큰 파싱 완료

- ⚠️ **미분석** — 파일은 존재하나 frontmatter `colors` 구조가 표준(`canvas`/`primary`)과 상이해 자동 파싱 미적용 (8개: theverge · tesla · starbucks · spotify · mastercard · lovable · lamborghini · kraken). 수동 보완 예정.

---

## 기본 3테마 (Default)

| 시스템 | 분류 | 캔버스 | Primary | 폰트 |

|--------|------|--------|---------|------|

| [`claude`](anthropic-claude.md) **(default)** | light | `#faf9f5` | `#cc785c` | Copernicus |
| [`clickhouse`](clickhouse.md) **(default)** | dark | `#0a0a0a` | `#faff69` | Inter |
| [`clay`](clay.md) **(default)** | light | `#fffaf0` | `#0a0a0a` | Plain Black |

---

## 전체 56개 — 분류별

### LIGHT (33개) — 밝은 캔버스 — white/cream, 본문 near-black

| 시스템 | 분류 | 캔버스 | Primary | 폰트 |

|--------|------|--------|---------|------|

| [`claude`](anthropic-claude.md) **(default)** | light | `#faf9f5` | `#cc785c` | Copernicus |
| [`clay`](clay.md) **(default)** | light | `#fffaf0` | `#0a0a0a` | Plain Black |
| [`cohere`](cohere.md) | light | `#ffffff` | `#17171c` | CohereText |
| [`coinbase`](coinbase.md) | light | `#ffffff` | `#0052ff` | 'Coinbase Display' |
| [`cursor`](cursor.md) | light | `#f7f7f4` | `#f54e00` | 'CursorGothic' |
| [`elevenlabs`](elevenlabs.md) | light | `#f5f5f5` | `#292524` | 'Waldenburg' |
| [`expo`](expo.md) | light | `#ffffff` | `#000000` | 'Inter' |
| [`figma`](figma.md) | light | `#ffffff` | `#000000` | figmaSans |
| [`ibm`](ibm.md) | light | `#ffffff` | `#0f62fe` | IBM Plex Sans |
| [`intercom`](intercom.md) | light | `#f5f1ec` | `#111111` | Saans |
| [`meta`](meta.md) | light | `#ffffff` | `#0064e0` | Optimistic VF |
| [`minimax`](minimax.md) | light | `#ffffff` | `#0a0a0a` | DM Sans |
| [`mintlify`](mintlify.md) | light | `#ffffff` | `#0a0a0a` | Inter |
| [`miro`](miro.md) | light | `#ffffff` | `#1c1c1e` | Roobert PRO |
| [`mistral.ai`](mistral.ai.md) | light | `#ffffff` | `#fa520f` | PP Editorial Old |
| [`mongodb`](mongodb.md) | light | `#ffffff` | `#00ed64` | Euclid Circular A |
| [`nike`](nike.md) | light | `#ffffff` | `#111111` | Nike Futura ND |
| [`notion`](notion.md) | light | `#ffffff` | `#0075de` | NotionInter |
| [`nvidia`](nvidia.md) | light | `#ffffff` | `#76b900` | NVIDIA-EMEA |
| [`ollama`](ollama.md) | light | `#ffffff` | `#000000` | SF Pro Rounded |
| [`opencode.ai`](opencode.ai.md) | light | `#fdfcfc` | `#201d1d` | Berkeley Mono |
| [`pinterest`](pinterest.md) | light | `#ffffff` | `#e60023` | Pin Sans |
| [`posthog`](posthog.md) | light | `#eeefe9` | `#f7a501` | IBM Plex Sans Variable |
| [`renault`](renault.md) | light | `#ffffff` | `#ffed00` | NouvelR |
| [`replicate`](replicate.md) | light | `#f9f7f3` | `#ea2804` | rb-freigeist-neue |
| [`runwayml`](runwayml.md) | light | `#ffffff` | `#000000` | abcNormal |
| [`slack`](slack.md) | light | `#ffffff` | `#4a154b` | Salesforce-Avant-Garde |
| [`superhuman`](superhuman.md) | light | `#ffffff` | `#1b1938` | 'Super Sans VF' |
| [`together.ai`](together.ai.md) | light | `#ffffff` | `#000000` | The Future |
| [`uber`](uber.md) | light | `#ffffff` | `#000000` | UberMove |
| [`vodafone`](vodafone.md) | light | `#ffffff` | `#e60000` | Vodafone |
| [`wise`](wise.md) | light | `#ffffff` | `#9fe870` | Wise Sans |
| [`zapier`](zapier.md) | light | `#fffefb` | `#ff4f00` | Degular Display |

### WARM (2개) — 따뜻한 중간 톤

| 시스템 | 분류 | 캔버스 | Primary | 폰트 |

|--------|------|--------|---------|------|

| [`playstation`](playstation.md) | warm | `#0070d1` | `#0070d1` | PlayStation SST |
| [`revolut`](revolut.md) | warm | `#494fdf` | `#494fdf` | Aeonik Pro |

### DARK (13개) — 어두운 캔버스 — near-black/navy, 본문 white

| 시스템 | 분류 | 캔버스 | Primary | 폰트 |

|--------|------|--------|---------|------|

| [`clickhouse`](clickhouse.md) **(default)** | dark | `#0a0a0a` | `#faff69` | Inter |
| [`composio`](composio.md) | dark | `#0f0f0f` | `#0007cd` | 'abcDiatype' |
| [`discord`](discord.md) | dark | `#0a0d3a` | `#5865f2` | ABC Ginto Nord |
| [`ferrari`](ferrari.md) | dark | `#181818` | `#da291c` | 'FerrariSans' |
| [`framer`](framer.md) | dark | `#090909` | `#ffffff` | GT Walsheim Framer Medium |
| [`hashicorp`](hashicorp.md) | dark | `#000000` | `#000000` | hashicorpSans |
| [`raycast`](raycast.md) | dark | `#07080a` | `#ffffff` | Inter |
| [`resend`](resend.md) | dark | `#000000` | `#fcfdff` | Domaine Display |
| [`sanity`](sanity.md) | dark | `#0b0b0b` | `#0b0b0b` | waldenburgNormal |
| [`sentry`](sentry.md) | dark | `#150f23` | `#150f23` | Sentry Display |
| [`shopify`](shopify.md) | dark | `#000000` | `#000000` | NeueHaasGrotesk Display |
| [`spacex`](spacex.md) | dark | `#000000` | `#000000` | D-DIN-Bold |
| [`x.ai`](x.ai.md) | dark | `#0a0a0a` | `#ffffff` | universalSans |

### ? (8개) — 미분석 — colors 구조 상이

| 시스템 | 분류 | 캔버스 | Primary | 폰트 |

|--------|------|--------|---------|------|

| `kraken` | ? | `?` | `?` | ? |
| `lamborghini` | ? | `?` | `?` | ? |
| `lovable` | ? | `?` | `?` | ? |
| `mastercard` | ? | `?` | `?` | ? |
| `spotify` | ? | `?` | `?` | ? |
| `starbucks` | ? | `?` | `?` | ? |
| `tesla` | ? | `?` | `?` | ? |
| `theverge` | ? | `?` | `?` | ? |

---

## 통계

- **전체**: 56개 시스템

- **light**: 33개

- **dark**: 13개

- **warm**: 2개

- **미분석(?)**: 8개

- **기본(default)**: 3개 — claude · clickhouse · clay

- **원본 소스**: `/Users/goos/Downloads/DESIGN-<name>.md`

---

## 분류 기준

canvas hex의 R+G+B 평균 휘도:

- 평균 < 100 → **dark** (캔버스가 매우 어두움, 본문 white)

- 100 ≤ 평균 < 232 → **warm** (중간 따뜻한 톤)

- 평균 ≥ 232 → **light** (밝은 캔버스, 본문 near-black)


Tailwind 렌더 시 다크/라이트 자동 분기는 `mapping/tailwind.md` §5 참조.

---

## 변경 이력

| 날짜 | 변경 |
|------|------|

| 2026-06-16 | 2차 확장 완료 — 56개 전체 복사 + frontmatter 토큰 파싱 + 휘도 자동 분류(light 33/dark 13/warm 2/미분석 8). 기본 3테마(claude/clickhouse/clay) Tailwind 매핑 검증 완료 |

| 2026-06-16 | 초기 작성. 기본 3테마 Pilot |
