# moai-media 커넥터·API 가이드

## 개요

`moai-media`는 **4개 스킬 + 2개 MCP 번들**로 구성됩니다:

- **이미지 프롬프트 빌더 3종** (`gpt-image-2-prompt`·`gemini-3-image-prompt`·`midjourney-v8-prompt`) — 텍스트 프롬프트만 산출, API 키 불필요
- **음성 생성 1종** (`audio-gen`) — ElevenLabs MCP 호출, `ELEVENLABS_API_KEY` 1개 필요

**번들 MCP 2종** (`moai-media/.mcp.json`에 자동 등록):
- **Higgsfield MCP** (hosted, `https://mcp.higgsfield.ai/mcp`) — 이미지·영상 생성 30+ 모델
- **ElevenLabs MCP** (uvx stdio) — 음성·TTS·더빙

## MCP 번들 (자동 등록)

`moai-media` 플러그인 설치 시 `.mcp.json`의 2개 MCP가 Cowork에 자동 등록됩니다.

### Higgsfield (hosted MCP, OAuth)

```json
{
  "higgsfield": {
    "type": "http",
    "url": "https://mcp.higgsfield.ai/mcp"
  }
}
```

**첫 연결 절차**:
1. moai-media 설치 후 Cowork에서 "Higgsfield" 커넥터가 보입니다
2. **Connect** 버튼 클릭 → 브라우저가 Higgsfield 로그인 페이지로 이동
3. Higgsfield 계정으로 로그인 (없으면 [higgsfield.ai](https://higgsfield.ai)에서 가입)
4. 권한 승인 → Cowork로 자동 복귀
5. 1회만 인증하면 이후 모든 호출이 본인 계정·잔액으로 처리됨

**API 키 별도 발급 불필요**. Higgsfield 계정의 OAuth 토큰으로 인증·요금이 처리됩니다.

**지원 모델 (30+)**:
- 이미지: Soul · Nano Banana · Seedream · Flux · Cinema Studio
- 영상: Sora 2 · Veo 3 · Kling 3.0 · Minimax Hailuo · Seedance · Wan
- 특수: DOP (Director of Photography) · Speak (말하는 머리) · Character (캐릭터 일관성)

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

**MCP 자동 등록 설정** ([공식 GitHub](https://github.com/elevenlabs/elevenlabs-mcp) 기준):

```json
{
  "ElevenLabs": {
    "command": "uvx",
    "args": ["elevenlabs-mcp"],
    "env": { "ELEVENLABS_API_KEY": "${ELEVENLABS_API_KEY}" }
  }
}
```

- **uvx 자동 설치** — 최초 실행 시 `elevenlabs-mcp` 패키지 자동 설치
- 사전 준비: `uv` 설치 (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- `which uvx` 결과가 비어 있으면 PATH에 추가 필요 (`~/.local/bin` 등)
- Windows 사용자: Claude Desktop "Help → Enable Developer Mode" 활성화 필요
- [공식 MCP GitHub](https://github.com/elevenlabs/elevenlabs-mcp)

**옵션 환경변수** (필요 시 추가):

| 변수 | 기본 | 용도 |
|---|---|---|
| `ELEVENLABS_API_KEY` | 필수 | API 인증 |
| `ELEVENLABS_MCP_BASE_PATH` | `~/Desktop` | 파일 출력 디렉토리 |
| `ELEVENLABS_MCP_OUTPUT_MODE` | `files` | files / resources / both |
| `ELEVENLABS_API_RESIDENCY` | `us` | 데이터 거주지 |

**로그 위치** (트러블슈팅):
- macOS: `~/Library/Logs/Claude/mcp-server-elevenlabs.log`
- Windows: `%APPDATA%\Claude\logs\mcp-server-elevenlabs.log`

**대체 설치 방법** (pip):
```bash
pip install elevenlabs-mcp
python -m elevenlabs_mcp --api-key=${ELEVENLABS_API_KEY}
```

## 스킬-도구 매핑

| 스킬 | 출력·동작 | 사용 MCP |
|---|---|---|
| `gpt-image-2-prompt` | OpenAI 6-Block 프롬프트 텍스트 | (직접 호출 X) — ChatGPT 등에 사용자가 복붙 |
| `gemini-3-image-prompt` | Google 5-component 프롬프트 텍스트 | (직접 호출 X) — Google AI Studio에 복붙 또는 Higgsfield MCP로 호출 (Nano Banana 모델) |
| `midjourney-v8-prompt` | 키워드+`--파라미터` 텍스트 | (직접 호출 X) — Discord `/imagine` 또는 alpha.midjourney.com에 복붙 |
| `audio-gen` | MP3·WAV·OGG 음성 파일 | **ElevenLabs MCP** 자동 호출 |
| (이미지·영상 직접 생성) | 결과 파일 | **Higgsfield MCP** 자동 호출 (30+ 모델) |

## Higgsfield MCP 활용 패턴

### 패턴 1 — 카드뉴스·SNS 이미지

```
"카드뉴스 4장 만들어 줘" 또는 "인스타 비주얼 생성"
→ card-news 스킬로 프롬프트 생성
→ Higgsfield MCP의 Soul 또는 Nano Banana 모델로 자동 렌더링
```

### 패턴 2 — 광고 영상 (피드·릴스)

```
"제품 광고 30초 영상 만들어 줘"
→ 스토리보드·컷 설계
→ Higgsfield MCP의 Veo 3 또는 Sora 2 모델 호출
```

### 패턴 3 — 인물·캐릭터 일관성

```
"같은 모델로 다양한 포즈 5컷"
→ Higgsfield Character 모델 + 시드 고정
```

### 패턴 4 — 카메라 무브먼트

```
"줌인·트래킹 영상 효과로"
→ Higgsfield DOP (Director of Photography) 모델
```

### 패턴 5 — 말하는 머리·립싱크

```
"이 스크립트를 인물이 말하는 영상으로"
→ Higgsfield Speak 모델 + ElevenLabs TTS 음성 결합
```

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| Higgsfield MCP "Not connected" | OAuth 인증 미완료 | Cowork → 설정 → MCP → Higgsfield → Connect 클릭 |
| Higgsfield 모델 호출 실패 | 워크스페이스 잔액 부족 | higgsfield.ai → Billing에서 충전 |
| `uvx elevenlabs-mcp` 실패 | `uv` 미설치 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ElevenLabs 401 | API 키 오류 | 대시보드에서 키 재확인 |
| ElevenLabs Free 한도 초과 | 월 10,000자 소진 | 유료 플랜 또는 다음 달 대기 |
| Higgsfield 응답 느림 | 영상 모델은 30-60초 소요 정상 | 대기 (Sora·Veo는 1-2분도 가능) |
| 프롬프트 빌더 결과가 안 좋음 | 입력 컨텍스트 부족 | AskUserQuestion 프리셋(제품샷·인물·일러스트·풍경) 재선택 |

## 비용 관리

- **이미지 프롬프트 빌더 3종**: 비용 0원 (텍스트 생성만)
- **`audio-gen`** (ElevenLabs):
  - Free: 월 10,000자 TTS
  - Starter ($5/월): 30,000자 + 음성 복제 10개
  - Creator ($22/월): 100,000자 + 더빙 30분
- **Higgsfield** (이미지·영상):
  - Free: 약간의 무료 크레딧 (가입 시)
  - 유료 플랜: higgsfield.ai/pricing
  - 모델별 크레딧 소비량 다름 (영상이 이미지보다 큼)

## Higgsfield CLI (옵션)

MCP 외에 Higgsfield CLI를 별도로 쓸 수도 있습니다. CLI는 .mcp.json과 무관하게 터미널에서 직접 호출:

```bash
# Higgsfield CLI 설치
curl -LsSf https://higgsfield.ai/cli/install.sh | sh

# 이미지 생성
higgsfield generate image "...prompt..."

# 영상 생성
higgsfield generate video "...prompt..."
```

CLI는 MCP를 대체하지 않고 보조입니다. MCP가 통합 워크플로우에 더 적합합니다.

## 자료 출처

- [Higgsfield 공식 MCP](https://higgsfield.ai/mcp) — hosted MCP 서버 안내
- [Higgsfield 공식 사이트](https://higgsfield.ai) — 계정·요금·모델
- [ElevenLabs MCP GitHub](https://github.com/elevenlabs/elevenlabs-mcp)
- [Higgsfield CLI](https://higgsfield.ai/cli)
