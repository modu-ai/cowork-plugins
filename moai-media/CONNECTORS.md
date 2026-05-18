# moai-media 커넥터·API 가이드

## 개요

`moai-media`는 **4개 스킬**로 구성됩니다:

- **이미지 프롬프트 빌더 3종** (`gpt-image-2-prompt`·`gemini-3-image-prompt`·`midjourney-v8-prompt`) — 텍스트 프롬프트만 산출, API 키 불필요
- **음성 생성 1종** (`audio-gen`) — ElevenLabs MCP 호출, `ELEVENLABS_API_KEY` 1개만 필요

이미지·영상의 실제 렌더링은 **별도 MCP**가 처리합니다 (이 플러그인 책임 아님).

## API 키 등록

### ElevenLabs (`ELEVENLABS_API_KEY`) — `audio-gen` 전용

**용도**: TTS, 보이스 클로닝, 다국어 더빙, 효과음 생성

**발급**:
1. [elevenlabs.io](https://elevenlabs.io) 가입
2. [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)에서 키 생성
3. Free 티어: 월 10,000자 TTS 무료

**등록**:
```bash
# .moai/credentials.env
ELEVENLABS_API_KEY=sk_...
```

## MCP 서버 (자동 등록)

`moai-media/.mcp.json`이 ElevenLabs MCP 1개만 자동 등록합니다.

```json
{
  "elevenlabs": {
    "command": "/bin/bash",
    "args": ["-l", "-c", "exec uvx elevenlabs-mcp"],
    "env": { "ELEVENLABS_API_KEY": "${ELEVENLABS_API_KEY}" }
  }
}
```

- **uvx 자동 설치** — 최초 실행 시 `elevenlabs-mcp` 패키지 설치
- 사전 준비: `uv` 설치 (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [공식 MCP GitHub](https://github.com/elevenlabs/elevenlabs-mcp)

## 이미지·영상 렌더링은 별도 MCP가 담당

본 플러그인의 이미지 프롬프트 빌더 3종은 **텍스트 프롬프트만 생성**합니다. 실제 이미지·영상 렌더링은 사용자가 외부 도구 또는 별도 MCP에서 실행합니다.

| 영역 | 책임 |
|---|---|
| 이미지 텍스트 프롬프트 작성 | `moai-media` 빌더 3종 |
| 음성·TTS·더빙 생성 | `moai-media:audio-gen` (ElevenLabs MCP) |
| 이미지 렌더링 (실제 생성) | ChatGPT (GPT-image-2) / Google AI Studio (Gemini 3) / Discord `/imagine` (Midjourney) |
| 영상·립싱크·캐릭터 (시네마틱) | **Higgsfield MCP** (별도 설치 — Soul·DOP·말하는머리) |

## 스킬-도구 매핑

| 스킬 | 출력 | 사용자 다음 단계 |
|---|---|---|
| `gpt-image-2-prompt` | OpenAI 6-Block 프롬프트 텍스트 | ChatGPT·OpenAI API에 복붙 |
| `gemini-3-image-prompt` | Google 5-component 프롬프트 텍스트 | Google AI Studio·Gemini API에 복붙 |
| `midjourney-v8-prompt` | 키워드+`--파라미터` 프롬프트 텍스트 | Discord `/imagine` 또는 alpha.midjourney.com에 복붙 |
| `audio-gen` | MP3·WAV·OGG 음성 파일 | 직접 사용 (MCP가 자동 호출) |

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `uvx elevenlabs-mcp` 실패 | `uv` 미설치 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ElevenLabs 401 | API 키 오류 | 대시보드에서 키 재확인 |
| 음성 생성 안 됨 | Free 티어 한도 초과 | 유료 플랜 또는 다음 달 대기 |
| 프롬프트 빌더 결과가 안 좋음 | 입력 컨텍스트 부족 | AskUserQuestion 프리셋(제품샷·인물·일러스트·풍경) 재선택 |

## 비용 관리

- **이미지 프롬프트 빌더 3종**: 비용 0원 (텍스트 생성만)
- **`audio-gen`**: ElevenLabs 사용량 기반
  - Free: 월 10,000자 TTS
  - Starter ($5/월): 30,000자 + 음성 복제 10개
  - Creator ($22/월): 100,000자 + 더빙 30분
- 실제 이미지 생성 비용은 ChatGPT Plus·Gemini Advanced·Midjourney 구독에 포함
