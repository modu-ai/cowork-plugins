---
title: "출처와 저작권 표기"
weight: 80
description: "모두의 코워크로 만든 결과물에 출처를 밝혀야 하는지, 어떤 스킬과 MCP가 표기 대상인지 상황별로 정리했습니다."
geekdocBreadcrumb: true
date: 2026-08-10T00:00:00+09:00
lastmod: 2026-08-10T00:00:00+09:00
---

"이걸로 만든 보고서를 회사에 제출해도 되나요?", "블로그에 올릴 때 출처를 적어야 하나요?" 자주 들어오는 질문입니다. 결론부터 말씀드리면 대부분의 경우 **적지 않으셔도 됩니다.** 다만 예외가 있고, 그 예외가 정확히 어디인지를 이 페이지에 정리했습니다.

![출처를 밝혀야 하는지 판단하는 흐름](/infographics/attribution-flow.png)

> 이 페이지는 법률 자문이 아니라 실무 안내입니다. 계약이나 분쟁이 걸린 사안은 전문가의 확인을 받으시기 바랍니다.

## 한눈에 보기

| 상황 | 출처 표기 | 이유 |
|---|---|---|
| 만든 결과물(문서·이미지·보고서)을 쓰거나 판매한다 | 불필요 | 산출물의 권리는 전적으로 사용자에게 있습니다 |
| 모두의 코워크 자체를 재배포하거나 스킬 파일을 가져다 쓴다 | 필수 | 참고한 오픈소스가 MIT 등 표기 의무 라이선스입니다 |
| 외부 데이터를 인용한 보고서를 공개한다 | 권장 | 데이터 제공처의 신뢰가 함께 걸립니다 |
| AI로 생성한 이미지·영상·음성을 공개한다 | 권장 | 생성 서비스와 게시 플랫폼의 정책을 함께 따릅니다 |

## 1. 표기 불필요 — 결과물을 그대로 쓰는 경우

여러분이 코워커에게 시켜서 만든 사업계획서, 상세페이지, 계약 검토 리포트, 이미지 같은 산출물은 **여러분 것**입니다. 상업적으로 팔아도 되고, 회사 이름으로 제출해도 되며, "모두의 코워크로 만들었다"고 밝힐 의무도 없습니다.

근거는 저장소의 [LICENSE-OUTPUT.md](https://github.com/modu-ai/moai-cowork/blob/main/LICENSE-OUTPUT.md)입니다. 산출물에는 플러그인의 Apache-2.0 라이선스가 따라붙지 않습니다.

대부분의 사용자는 여기서 끝입니다. 아래 2절과 3절은 특수한 경우입니다.

## 2. 표기 필수 — 스킬 자체를 가져다 쓰는 경우

모두의 코워크의 **스킬 파일을 복사해 다른 프로젝트에 넣거나**, 이 저장소를 포크해 재배포하는 경우에는 이야기가 달라집니다. 아래 스킬들은 MIT 라이선스 프로젝트의 방법론을 참고해 만들었고, MIT는 저작권 고지와 허가 문구를 함께 배포할 것을 요구합니다.

| 코워커 | 해당 스킬 | 참고한 프로젝트 | 라이선스 |
|---|---|---|---|
| 마케터 | 키워드 리서치 · 그로스 실험 · 리텐션 | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT |
| 마케터 | SNS 콘텐츠의 페이스북 채널 규격 | [social-media-skills/skills](https://github.com/social-media-skills/skills) | MIT |
| 마케터 | 메타 광고 진단 체크 매트릭스 | [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | MIT |
| 미디어 크리에이터 | GPT 이미지 프롬프트 빌더 | [openai/openai-cookbook](https://github.com/openai/openai-cookbook) | MIT |
| 작가 | 한국어 윤문 | [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) | MIT |
| 데이터 애널리스트 · 법무 · 작가 | 주식 · 법원경매 · 부동산 · 등기 · 식약처 · 맞춤법 스킬 | [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill) | MIT |
| 법무 담당 | 등기 열람 자동화 절차 | [challengekim/iros-registry-automation](https://github.com/challengekim/iros-registry-automation) | MIT |
| 데이터 애널리스트 | 부동산 데이터 | [tae0y/real-estate-mcp](https://github.com/tae0y/real-estate-mcp) | MIT |
| 사무관 | PDF 생성용 한글 폰트 | [notofonts/noto-cjk](https://github.com/notofonts/noto-cjk) | SIL OFL 1.1 |

MIT 항목의 저작권 문구와 허가 문구 전문은 저장소 루트의 [NOTICE](https://github.com/modu-ai/moai-cowork/blob/main/NOTICE) §1에 항목별로 들어 있습니다. 재배포하실 때 이 파일을 함께 가져가시면 표기 의무가 충족됩니다.

폰트는 사정이 조금 다릅니다. Noto Sans CJK KR의 바이너리는 저장소에 들어 있지 않고 스킬을 처음 실행할 때 내려받습니다. 따라서 내려받은 폰트를 산출물과 **함께 재배포할 때만** OFL 고지 의무가 생기며, 그 라이선스 전문은 `plugins/moai-officer/skills/doc-pdf/assets/fonts/LICENSE.txt`에 있습니다.

### 라이선스가 요구하지는 않지만 밝히는 것이 좋은 참고처

아래는 원저작자가 공개한 자료를 참고한 경우입니다. 표기가 법적 의무는 아니지만, 어디서 온 것인지 알 수 있어야 신뢰할 수 있다고 보아 함께 적어 둡니다.

| 코워커 | 해당 영역 | 참고한 프로젝트 |
|---|---|---|
| 미디어 크리에이터 · 디자이너 | Higgsfield 프롬프트 크래프트 | [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) |
| 미디어 크리에이터 | Codex 이미지 연동 | [wjb127/codex-image](https://github.com/wjb127/codex-image) |
| 사무관 | 한글 문서(HWPX) 처리 | [airmang/python-hwpx](https://github.com/airmang/python-hwpx) |
| 데이터 애널리스트 | 국내 주식 데이터 설계 참고 | [jjlabsio/korea-stock-mcp](https://github.com/jjlabsio/korea-stock-mcp) |
| 디자이너 | 한국 디자인 시스템 레퍼런스 | [daangn/seed-design](https://github.com/daangn/seed-design) · [kakao/kakao-font](https://github.com/kakao/kakao-font) · [KRDS-uiux/krds-uiux](https://github.com/KRDS-uiux/krds-uiux) |

## 3. 밝히기 권장 — 외부 데이터와 생성 서비스가 섞인 경우

코워커가 MCP를 통해 외부 서비스에서 가져온 데이터가 결과물에 들어갔다면, 그 데이터의 출처를 밝히는 편이 좋습니다. 법적 의무라서가 아니라 **읽는 사람이 숫자를 믿을 수 있어야 하기 때문**입니다. 공시 자료나 법령을 인용한 문서라면 특히 그렇습니다.

### 우리가 만들지 않은 제3자 MCP 서버

원저작자의 이름을 그대로 쓰는 것이 원칙입니다.

| 서버 | 만든 곳 | 연결된 코워커 | 라이선스·근거 |
|---|---|---|---|
| Higgsfield | Higgsfield AI | 미디어 크리에이터 · 디자이너 · 스토리 크리에이터 | 서비스 약관 |
| ElevenLabs | ElevenLabs | 미디어 크리에이터 | 서비스 약관 |
| korean-dart-mcp | chrisryugj | 재무·세무 담당 · 데이터 애널리스트 · 코워커 | MIT |
| kordoc | chrisryugj | 사무관 | MIT |
| korean-stats-mcp | chrisryugj | 데이터 애널리스트 | MIT |
| archhub-mcp | chrisryugj | 데이터 애널리스트 | MIT |
| korean-law-mcp | chrisryugj | 법무 담당 | MIT |
| Meta Ads · WordPress · Typefully · post-bridge | 각 서비스 | 마케터 | 각 서비스 약관 |

### 우리가 직접 만든 MCP 서버

공식 MCP가 없는 서비스만 직접 만듭니다. 이름은 `moai-mcp-` 로 시작합니다.

| 서버 | 연결된 코워커 | 연결 대상 |
|---|---|---|
| `moai-mcp-smartstore` · `moai-mcp-imweb` · `moai-mcp-cafe24` | 셀러 | 네이버 스마트스토어 · 아임웹 · 카페24 |
| `moai-mcp-threads-poster` | SNS 크리에이터 | Threads |

이 서버들은 저희가 만든 것이라 별도의 출처 표기 의무가 없습니다. 다만 서버가 접속하는 각 서비스의 **API 이용약관은 그대로 적용**되므로, 가져온 데이터를 외부에 공개할 때는 해당 서비스의 정책을 확인하시기 바랍니다.

## 표기 문구 예시

그대로 복사해 쓰셔도 됩니다.

보고서 각주에 데이터 출처를 밝힐 때:

```
데이터 출처: 국가법령정보센터, 국가통계포털(KOSIS), 금융감독원 전자공시시스템(DART)
조회 시점: 2026년 8월
```

생성한 이미지나 영상의 캡션에:

```
이미지 생성: Higgsfield · gpt-image-2
```

스킬을 포함한 프로젝트를 재배포할 때 README에:

```
이 프로젝트는 modu-ai/moai-cowork (Apache-2.0)의 스킬을 포함합니다.
제3자 저작물 고지는 NOTICE 파일을 참조하세요.
```

## 표기 대상이 아닌 것

디자이너 코워커의 **브랜드 디자인 시스템 참고 자료**는 Apache-2.0 적용 범위 밖입니다. 글로벌 브랜드의 디자인을 분석한 자료라 재배포 대상이 아니며, 따라서 표기 대상도 아닙니다. 자세한 내용은 [라이선스와 산출물 권리](../../plugins/license/)에 있습니다.

## 더 자세한 목록

이 페이지는 "무엇을 밝혀야 하는가"를 사용자 입장에서 정리한 것입니다. "모두의 코워크가 무엇에 빚졌는가"를 제작자 입장에서 빠짐없이 적은 목록은 따로 있습니다.

- [오픈소스 크레딧](../../plugins/open-source/) — 스킬·MCP·문서 사이트가 기대고 있는 오픈소스 전체 목록
- [라이선스와 산출물 권리](../../plugins/license/) — 산출물의 권리 범위와 상업적 사용
- [NOTICE](https://github.com/modu-ai/moai-cowork/blob/main/NOTICE) — MIT 라이선스 전문을 포함한 법적 고지 원문

빠뜨렸거나 잘못 적은 출처가 있다면 [이슈](https://github.com/modu-ai/moai-cowork/issues)로 알려 주세요. 확인하는 대로 고치겠습니다.
