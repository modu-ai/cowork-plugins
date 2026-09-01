---
title: "오픈소스 크레딧"
weight: 50
description: "모두의 코워크가 어깨를 빌린 오픈소스 프로젝트 목록입니다. 스킬이 참고한 방법론, 함께 쓰는 MCP 서버, 문서 사이트를 떠받치는 도구까지 전부 밝힙니다."
geekdocBreadcrumb: true
date: 2026-08-08T00:00:00+09:00
lastmod: 2026-09-01T00:00:00+09:00
---

모두의 코워크는 처음부터 끝까지 혼자 만든 물건이 아닙니다. 남이 먼저 정리해 둔 방법론을
참고했고, 남이 만든 서버에 연결하고, 남이 만든 도구 위에서 돌아갑니다.

이 페이지는 **그 빚을 전부 적어 두는 자리**입니다. 라이선스가 요구해서가 아니라, 어디서 온
것인지 알 수 있어야 신뢰할 수 있다고 보기 때문입니다.

법적 고지 원문(MIT 라이선스 전문 등)은 저장소의
[`NOTICE`](https://github.com/modu-ai/moai-cowork/blob/main/NOTICE) 파일에 있습니다. 이 페이지는
그것을 사람이 읽을 수 있게 정리한 것입니다.

## 스킬이 참고한 오픈소스

방법론·체계·프롬프트 설계를 참고한 프로젝트입니다. 그대로 복사한 것이 아니라 모두의 코워크
환경에 맞게 다시 썼지만, 출발점이 어디였는지는 밝혀 둡니다.

| 프로젝트 | 라이선스 | 어디에 쓰였나 |
|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | 마케터 — 키워드 리서치 · 그로스 실험 · 리텐션 |
| [social-media-skills/skills](https://github.com/social-media-skills/skills) | MIT | 마케터 — SNS 콘텐츠의 페이스북 채널 규격 |
| [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | MIT | 마케터 — 메타 광고 진단 체크 매트릭스 |
| [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | 원저작자 공개 | 미디어 · 디자이너 — Higgsfield 프롬프트 크래프트 전반 |
| [openai/openai-cookbook](https://github.com/openai/openai-cookbook) | MIT | 미디어 — GPT 이미지 프롬프트 빌더 |
| [wjb127/codex-image](https://github.com/wjb127/codex-image) | 원저작자 공개 | 미디어 — Codex 이미지 연동 |
| [airmang/python-hwpx](https://github.com/airmang/python-hwpx) | 원저작자 공개 | 사무관 — 한글 문서(HWPX) 처리 |
| [notofonts/noto-cjk](https://github.com/notofonts/noto-cjk) | SIL OFL 1.1 | 사무관 — PDF 생성용 한글 폰트 |
| [challengekim/iros-registry-automation](https://github.com/challengekim/iros-registry-automation) | MIT | 법무 — 등기 열람 자동화 절차 |
| [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill) | MIT | 데이터 애널리스트 · 법무 · 작가 — 한국 실무 스킬 6종의 포팅 원본 |
| [tae0y/real-estate-mcp](https://github.com/tae0y/real-estate-mcp) | MIT | 데이터 애널리스트 — 부동산 데이터 |
| [jjlabsio/korea-stock-mcp](https://github.com/jjlabsio/korea-stock-mcp) | 원저작자 공개 | 데이터 애널리스트 — 국내 주식 데이터 |
| [daangn/seed-design](https://github.com/daangn/seed-design) · [kakao/kakao-font](https://github.com/kakao/kakao-font) · [KRDS-uiux/krds-uiux](https://github.com/KRDS-uiux/krds-uiux) | 각 프로젝트 라이선스 | 디자이너 — 한국 디자인 시스템 레퍼런스 |
| [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) | MIT | 작가 — 한국어 윤문(`korean-humanize`)의 원본 계보 |

위 표에서 MIT로 표기된 항목은 라이선스가 저작권 고지를 요구하므로, 저작권 문구와 허가
문구 전문이 저장소 루트 [`NOTICE`](https://github.com/modu-ai/moai-cowork/blob/main/NOTICE)
§1에 항목별로 들어 있습니다. 각 스킬 본문에도 원본 링크와 NOTICE 절 번호를 함께 적어
두었습니다.

## 함께 쓰는 제3자 MCP 서버

우리가 만들지 않았고, 원저작자의 이름을 그대로 쓰는 서버입니다. 자체 제작 서버와 구분하기
위해 **이름을 바꾸지 않는 것이 원칙**입니다.

| 서버 | 만든 곳 | 연결한 코워커 |
|---|---|---|
| [Higgsfield](https://mcp.higgsfield.ai/mcp) | Higgsfield AI | 미디어 · 디자이너 · 스토리 |
| [ElevenLabs](https://github.com/elevenlabs/elevenlabs-mcp) | ElevenLabs | 미디어 |
| [korean-dart-mcp](https://github.com/chrisryugj/korean-dart-mcp) | chrisryugj (MIT) | 재무·세무 · 데이터 애널리스트 · 코워커 |
| [kordoc](https://github.com/chrisryugj/kordoc) | chrisryugj (MIT) | 사무관 |
| [korean-stats-mcp](https://github.com/chrisryugj/korean-stats-mcp) | chrisryugj (MIT) | 데이터 애널리스트 |
| [archhub-mcp](https://github.com/chrisryugj/archhub-mcp) | chrisryugj (MIT) | 데이터 애널리스트 |
| korean-law-mcp | chrisryugj (MIT) | 법무 |
| Meta Ads · WordPress · Typefully | 각 서비스 | 마케터 |
| [Context7](https://github.com/upstash/context7) | Upstash | 개발 저장소 전용 |

## 자체 제작 MCP 서버가 쓰는 것

공식 MCP가 없는 서비스만 직접 만듭니다. 그 서버들이 올라가 있는 토대입니다.

| 라이브러리 | 역할 |
|---|---|
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | 서버 기반 (FastMCP) |
| [httpx](https://www.python-httpx.org/) | HTTP 클라이언트 |
| [pydantic](https://docs.pydantic.dev/) | 입출력 스키마 검증 |
| [anyio](https://anyio.readthedocs.io/) | 비동기 실행 |
| [bcrypt](https://github.com/pyca/bcrypt) | 네이버 커머스 전자서명 |
| [uv](https://docs.astral.sh/uv/) · [hatchling](https://hatch.pypa.io/) | 의존성·빌드 |
| [pytest](https://docs.pytest.org/) · [ruff](https://docs.astral.sh/ruff/) | 테스트·정적 검사 |

## 이 문서 사이트를 떠받치는 것

지금 보고 계신 이 페이지도 오픈소스 위에 있습니다.

| 프로젝트 | 역할 | 라이선스 |
|---|---|---|
| [Hugo](https://gohugo.io/) | 정적 사이트 생성 | Apache-2.0 |
| [Hugo Geekdoc](https://github.com/thegeeklab/hugo-geekdoc) | 문서 테마 (구조만 차용, 스타일은 자체 디자인 시스템) | MIT |
| [Lucide](https://lucide.dev/) | 아이콘 | ISC |
| [Pretendard](https://github.com/orioncactus/pretendard) | 본문 서체 | SIL OFL 1.1 |
| [MaruBuri](https://hangeul.naver.com/font) | 제목 부리체 | 네이버 한글한글 아름답게 |
| [Inter](https://rsms.me/inter/) · [JetBrains Mono](https://www.jetbrains.com/lp/mono/) | 숫자·코드 서체 | SIL OFL 1.1 |
| [Mermaid](https://mermaid.js.org/) | 다이어그램 | MIT |
| [Chroma](https://github.com/alecthomas/chroma) | 코드 하이라이트 | MIT |

## 지금은 사라진 스킬의 출처

과거에 참고했지만 해당 스킬이 지금은 없는 경우도 남겨 둡니다. 기록이 사라지면 나중에 같은
자리를 다시 만들 때 출처를 잃습니다.

| 프로젝트 | 라이선스 | 관계 |
|---|---|---|
| [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | MIT | 과거 draw.io 도식 스킬의 영감 원본. 해당 스킬은 현재 제공하지 않음 |

## 라이선스가 적용되지 않는 부분

디자이너 코워커의 브랜드 디자인 시스템 참고 자료는 **Apache-2.0 적용 범위 밖**입니다.
글로벌 브랜드의 디자인을 분석한 자료라 재배포 대상이 아닙니다. 자세한 내용은
[라이선스와 산출물 권리](../license/) 페이지를 보세요.

## 빠진 게 있다면 알려 주세요

출처를 빠뜨렸거나 잘못 적었다면
[이슈](https://github.com/modu-ai/moai-cowork/issues)로 알려 주세요. 확인하는 대로 고치겠습니다.
표기 방식에 대한 요청(이름 표기·링크 주소·라이선스 명시)도 원저작자 쪽 의사를 따릅니다.
