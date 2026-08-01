---
title: "Higgsfield MCP 설정"
weight: 20
description: "moai-media·moai-story 플러그인의 생성형 스킬(이미지·영상)이 쓰는 Higgsfield 호스티드 MCP의 OAuth 인증·크레딧·폴백 안내."
geekdocBreadcrumb: true
---

[Higgsfield](https://higgsfield.ai)는 이미지·영상 생성 호스티드 MCP입니다. `moai-media`의 `media-higgsfield-image`·`media-higgsfield-video` 스킬과 `moai-story`의 `story-webtoon-art`·`story-conti`·`story-character-sheet`·`story-cover-art`·`story-previz` 스킬이 이 MCP를 통해 생성합니다. 최초 1회 OAuth 인증이 필요합니다.

## 1. MCP 서버 연결

각 플러그인의 `.mcp.json`이 Higgsfield 공식 호스티드 엔드포인트(`https://mcp.higgsfield.ai/mcp`)를 가리킵니다. Claude Code가 플러그인을 로드할 때 자동으로 등록합니다.

## 2. OAuth 1회 인증

1. Claude Code → Settings → MCP Servers에서 Higgsfield 항목을 선택합니다.
2. 브라우저가 열리면 Higgsfield 계정으로 로그인합니다 (OAuth 2.0 커넥터 흐름).
3. 접근 권한을 허용하면 액세스 토큰이 발급되어 Higgsfield 서버에 보관됩니다. API 키를 직접 다룰 필요가 없습니다.
4. 토큰 만료 시 Claude Code가 자동으로 갱신합니다.

인증 완료 후 생성형 스킬이 MCP 도구를 호출해 이미지·영상을 생성합니다.

## 3. 크레딧 안내

Higgsfield 작업은 크레딧을 소모합니다. 각 생성형 스킬은 생성 전 예상 크레딧을 사용자에게 고지하고 확인을 받습니다 (패널 약 2크레딧, 시네마틱 숏 약 20~50크레딧 등). 크레딧 잔액은 Higgsfield 웹(https://higgsfield.ai)에서 확인합니다.

## 4. MCP 미연결 폴백

Higgsfield MCP에 연결할 수 없을 때는 생성형 스킬이 프롬프트 온리 모드로 전환합니다. 완성 프롬프트를 텍스트로 출력하며 "Higgsfield 웹(https://higgsfield.ai)에 위 프롬프트를 붙여넣으세요" 안내를 추가합니다. 서버 과부하 시 잠시 대기 후 재시도하세요.

---

### Sources

- Higgsfield 공식: <https://higgsfield.ai>
- 마켓플레이스 진실 원본: [`/.claude-plugin/marketplace.json`](https://github.com/modu-ai/moai-cowork/blob/main/.claude-plugin/marketplace.json)
