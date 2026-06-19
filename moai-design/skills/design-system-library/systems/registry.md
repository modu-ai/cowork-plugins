# Design System Registry — 75개 브랜드 카탈로그

본 레지스트리는 `design-system-library`의 75개 디자인 시스템에 대한 인덱스입니다. 
각 시스템의 상세 토큰은 `systems/<name>.md`에 있습니다. 
canvas 휘도(R+G+B 평균) 기반 자동 분류: `<100` dark · `<232` warm · 그 외 light.

---

## 상태 표기

- ✅ **완료** — `systems/<name>.md` 존재, frontmatter 토큰 파싱 완료. **전체 75개 분류 완료** (56 풍부 분석 + 19 경량 토큰: 2026-06-19 테마_컴포넌트_쇼케이스에서 추출).
- ⚙️ **경량** — 19개(airbnb·airtable·apple·binance·bmw·bmw-m·bugatti·cal·dell-1996·hp·linear.app·nintendo-2001·stripe·supabase·vercel·voltagent·warp·webflow·wired)는 `테마_컴포넌트_쇼케이스_전체.html`에서 추출한 경량 토큰. 풍부한 브랜드 분석·typography 스케일은 추후 보강.

---

## 기본 3테마 (Default)

| 시스템 | 분류 | 캔버스 | Primary | 폰트 |

|--------|------|--------|---------|------|

| [`claude`](anthropic-claude.md) **(default)** | light | `#faf9f5` | `#cc785c` | Copernicus |
| [`clickhouse`](clickhouse.md) **(default)** | dark | `#0a0a0a` | `#faff69` | Inter |
| [`clay`](clay.md) **(default)** | light | `#fffaf0` | `#0a0a0a` | Plain Black |

---

## 전체 75개 — 분류별

### LIGHT (48개) — 밝은 캔버스 — white/cream, 본문 near-black

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
| [`kraken`](kraken.md) | light | `#ffffff` | `#7132f5` | Kraken-Brand |
| [`lovable`](lovable.md) | light | `#f7f4ed` | `#1c1c1c` | Camera Plain |
| [`mastercard`](mastercard.md) | light | `#f3f0ee` | `#cf4500` | MarkForMC |
| [`starbucks`](starbucks.md) | light | `#f2f0eb` | `#00754a` | SoDoSans |
| [`tesla`](tesla.md) | light | `#ffffff` | `#3e6ae1` | Universal Sans |
| [`airbnb`](airbnb.md) ⚙️ | light | `#ffffff` | `#ff5a5f` | 시스템 산세리프 |
| [`airtable`](airtable.md) ⚙️ | light | `#ffffff` | `#2d7ff9` | 시스템 산세리프 |
| [`apple`](apple.md) ⚙️ | light | `#ffffff` | `#0071e3` | 시스템 산세리프 |
| [`cal`](cal.md) ⚙️ | light | `#ffffff` | `#111827` | 시스템 산세리프 |
| [`dell-1996`](dell-1996.md) ⚙️ | light | `#ffffff` | `#007db8` | 시스템 산세리프 |
| [`hp`](hp.md) ⚙️ | light | `#ffffff` | `#0096d6` | 시스템 산세리프 |
| [`nintendo-2001`](nintendo-2001.md) ⚙️ | light | `#ffffff` | `#e60012` | 시스템 산세리프 |
| [`stripe`](stripe.md) ⚙️ | light | `#ffffff` | `#635bff` | 시스템 산세리프 |
| [`webflow`](webflow.md) ⚙️ | light | `#ffffff` | `#146ef5` | 시스템 산세리프 |
| [`wired`](wired.md) ⚙️ | light | `#ffffff` | `#0000ee` | Georgia(세리프) |

### WARM (2개) — 따뜻한 중간 톤

| 시스템 | 분류 | 캔버스 | Primary | 폰트 |

|--------|------|--------|---------|------|

| [`playstation`](playstation.md) | warm | `#0070d1` | `#0070d1` | PlayStation SST |
| [`revolut`](revolut.md) | warm | `#494fdf` | `#494fdf` | Aeonik Pro |

### DARK (25개) — 어두운 캔버스 — near-black/navy, 본문 white

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
| [`lamborghini`](lamborghini.md) | dark | `#000000` | `#ffc000` | LamboType |
| [`spotify`](spotify.md) | dark | `#121212` | `#1ed760` | SpotifyMixUI |
| [`theverge`](theverge.md) | dark | `#131313` | `#3cffd0` | Manuka |
| [`binance`](binance.md) ⚙️ | dark | `#161619` | `#f0b90b` | 시스템 산세리프 |
| [`bmw`](bmw.md) ⚙️ | dark | `#161619` | `#1c69d4` | 시스템 산세리프 |
| [`bmw-m`](bmw-m.md) ⚙️ | dark | `#161619` | `#1c69d4` | 시스템 산세리프 |
| [`bugatti`](bugatti.md) ⚙️ | dark | `#161619` | `#1f4fa0` | 시스템 산세리프 |
| [`linear.app`](linear.app.md) ⚙️ | dark | `#16161a` | `#7c84ec` | 시스템 산세리프 |
| [`supabase`](supabase.md) ⚙️ | dark | `#1c1c1c` | `#3ecf8e` | 시스템 산세리프 |
| [`vercel`](vercel.md) ⚙️ | dark | `#000000` | `#ffffff` | 시스템 산세리프 |
| [`voltagent`](voltagent.md) ⚙️ | dark | `#161619` | `#00d992` | 시스템 산세리프 |
| [`warp`](warp.md) ⚙️ | dark | `#161619` | `#01a2ff` | 시스템 산세리프 |

---

## 통계

- **전체**: 75개 시스템 (56 풍부 + 19 경량 ⚙️)

- **light**: 48개 (38 + 10 ⚙️)

- **dark**: 25개 (16 + 9 ⚙️)

- **warm**: 2개

- **기본(default)**: 3개 — claude · clickhouse · clay

- **원본 소스**: 풍부 56개 — `/Users/goos/Downloads/DESIGN-<name>.md` · 경량 19개 — `테마_컴포넌트_쇼케이스_전체.html`(getdesign.md 74종 컬렉션)

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

| 2026-06-19 | 19개 경량 시스템 추가(⚙️) — `테마_컴포넌트_쇼케이스_전체.html`의 getdesign.md 74종 컬렉션에서 추출(airbnb·airtable·apple·binance·bmw·bmw-m·bugatti·cal·dell-1996·hp·linear.app·nintendo-2001·stripe·supabase·vercel·voltagent·warp·webflow·wired) → 전체 75개(light 48/dark 25/warm 2) |

| 2026-06-16 | 3차 정합 — 8개 시스템(kraken · tesla · starbucks · mastercard · lovable · spotify · theverge · lamborghini) frontmatter `colors` 블록 추가 → 전체 56개 분류 완료(light 38/dark 16/warm 2) |

| 2026-06-16 | 2차 확장 완료 — 56개 전체 복사 + frontmatter 토큰 파싱 + 휘도 자동 분류(light 33/dark 13/warm 2/미분석 8). 기본 3테마(claude/clickhouse/clay) Tailwind 매핑 검증 완료 |

| 2026-06-16 | 초기 작성. 기본 3테마 Pilot |
