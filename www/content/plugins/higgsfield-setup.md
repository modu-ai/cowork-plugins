---
title: "Higgsfield MCP 설정"
weight: 20
description: "moai-media·moai-story·moai-designer 플러그인의 생성형 스킬(이미지·영상·3D·오디오·설명영상)이 쓰는 Higgsfield 호스티드 MCP의 OAuth 인증·크레딧·폴백 안내."
geekdocBreadcrumb: true
---

[Higgsfield](https://higgsfield.ai)는 이미지·영상·3D·오디오 생성 호스티드 MCP입니다. 세 플러그인이 이 MCP를 통해 생성하며, 최초 1회 OAuth 인증이 필요합니다.

| 플러그인 | 이 MCP를 쓰는 스킬 |
|---|---|
| `moai-media` | `media-higgsfield-image`(이미지) · `media-higgsfield-video`(영상) · `media-higgsfield-identity`(캐릭터 일관성 참조) · `media-higgsfield-assets`(3D·오디오·영상분석·후처리) · `media-higgsfield-explainer`(내레이션 설명영상) · `media-higgsfield-product`(제품 촬영 10모드). 호출 계약·비용 고지의 정본은 `media-higgsfield-core` |
| `moai-story` | `story-webtoon-art` · `story-conti` · `story-character-sheet` · `story-cover-art` · `story-previz` — 생성 실행은 `moai-media`에 위임 |
| `moai-designer` | `design-brand-visual`(브랜드 정합 비주얼) — 생성 실행은 `moai-media`에 위임 |

## 1. MCP 서버 연결

각 플러그인의 `.mcp.json`이 Higgsfield 공식 호스티드 엔드포인트(`https://mcp.higgsfield.ai/mcp`)를 가리킵니다. Claude Code가 플러그인을 로드할 때 자동으로 등록합니다.

## 2. OAuth 1회 인증

1. Claude Code → Settings → MCP Servers에서 Higgsfield 항목을 선택합니다.
2. 브라우저가 열리면 Higgsfield 계정으로 로그인합니다 (OAuth 2.0 커넥터 흐름).
3. 접근 권한을 허용하면 액세스 토큰이 발급되어 Higgsfield 서버에 보관됩니다. API 키를 직접 다룰 필요가 없습니다.
4. 토큰 만료 시 Claude Code가 자동으로 갱신합니다.

인증 완료 후 생성형 스킬이 MCP 도구를 호출해 결과물을 생성합니다.

## 3. 크레딧 안내

Higgsfield 작업은 크레딧을 소모합니다. 각 생성형 스킬은 생성 전 예상 크레딧을 사용자에게 고지하고 확인을 받습니다 (패널 약 2크레딧, 시네마틱 숏 약 20~50크레딧 등). 크레딧 잔액은 Higgsfield 웹(https://higgsfield.ai)에서 확인합니다.

이 사전 고지는 어림값이 아니라 **실제 청구액을 미리 조회한 값**입니다. 스킬은 생성 직전 비용 프리플라이트를 호출하는데, 이 조회 자체는 크레딧을 쓰지 않습니다. 실측 예: Soul 2.0 2K 이미지 1장은 프리플라이트가 `0.12` 크레딧을 예고했고 실제 차감도 정확히 `0.12`였습니다.

비용은 모델·해상도·옵션에 따라 크게 달라집니다. 3D의 텍스처·리깅·애니메이션은 각각 비용이 더해지고, 설명 영상은 블록 수에 비례해 1분(6블록)과 10분(60블록)이 10배 차이 납니다. 어림짐작하지 말고 스킬이 알려주는 프리플라이트 값을 보고 판단하세요.

## 4. MCP 미연결 폴백

Higgsfield MCP에 연결할 수 없을 때는 생성형 스킬이 프롬프트 온리 모드로 전환합니다. 완성 프롬프트를 텍스트로 출력하며 "Higgsfield 웹(https://higgsfield.ai)에 위 프롬프트를 붙여넣으세요" 안내를 추가합니다. 서버 과부하 시 잠시 대기 후 재시도하세요.

---

### Sources

- Higgsfield 공식: <https://higgsfield.ai>
- 마켓플레이스 진실 원본: [`/.claude-plugin/marketplace.json`](https://github.com/modu-ai/moai-cowork/blob/main/.claude-plugin/marketplace.json)
