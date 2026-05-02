# moai-media 커넥터·API 가이드

## 개요

moai-media는 **API 키 5개 + MCP 서버 3개**로 전체 미디어 생성을 커버합니다.

## API 키 등록 (5종)

### 1. Higgsfield AI (`HIGGSFIELD_API_KEY` + `HIGGSFIELD_SECRET`)

**용도**: `image-gen` (Soul 모델), `video-gen` (DOP 모델), `speech-video`, `character-mgmt` — 시네마틱 이미지·영상, 캐릭터 관리, 말하는 머리 영상

**발급**:
1. [higgsfield.ai](https://higgsfield.ai) 가입
2. 대시보드에서 API Key와 Secret 생성
3. 크레딧 충전 (Pay-as-you-go)

**등록**:
```bash
export HIGGSFIELD_API_KEY="hf_..."
export HIGGSFIELD_SECRET="hfsec_..."
```

**MCP 설치** (최초 1회):
```bash
pip install higgsfield-mcp
```

### 2. Google Gemini (`GEMINI_API_KEY`)

**용도**: `nano-banana` 스킬 — 한국어 타이포그래피 특화 이미지 생성 (Gemini 3 Image Preview)

**발급**:
1. [ai.google.dev](https://ai.google.dev/) 접속 → Google 계정 로그인
2. "Get API key" → 새 프로젝트 생성 또는 기존 선택
3. **Pay-as-you-go 결제 등록 필수**

**등록**:
```bash
export GEMINI_API_KEY="AIzaSy..."
```

**레거시 호환**: 기존 `NANO_BANANA_API_KEY` 환경변수도 자동 인식됩니다.

### 3. fal.ai (`FAL_KEY`)

**용도**: `image-gen`, `video-gen`, `fal-gateway` 스킬 — 1000+ 모델 통합 게이트웨이 (Flux, Ideogram, Kling, Hailuo, Luma, Pika, MiniMax Music)

**발급**:
1. [fal.ai](https://fal.ai/) 가입 (GitHub·Google OAuth 지원)
2. [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)에서 키 생성
3. 가입 시 **$5 무료 크레딧 자동 지급**

**등록**:
```bash
export FAL_KEY="fal-..."
```

### 4. ElevenLabs (`ELEVENLABS_API_KEY`)

**용도**: `audio-gen` 스킬 — TTS, 음성복제, 다국어 더빙, 사운드 이펙트

**발급**:
1. [elevenlabs.io](https://elevenlabs.io) 가입
2. [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)에서 키 생성
3. Free 티어: 월 10,000 char TTS 무료

**등록**:
```bash
export ELEVENLABS_API_KEY="sk_..."
```

## MCP 서버 (3종, 자동 등록)

플러그인 설치 시 `moai-media/.mcp.json`이 자동 적용됩니다.

### higgsfield (local MCP) — NEW

```json
{
  "higgsfield": {
    "command": "higgsfield-mcp",
    "env": {
      "HIGGSFIELD_API_KEY": "${HIGGSFIELD_API_KEY}",
      "HIGGSFIELD_SECRET": "${HIGGSFIELD_SECRET}"
    }
  }
}
```

- **pip 설치 필요**: `pip install higgsfield-mcp`
- 시네마틱 이미지(Soul), 영상(DOP), 말하는 머리 영상, 캐릭터 관리
- [Higgsfield AI 공식](https://higgsfield.ai)

### fal-ai (hosted MCP)

```json
{
  "fal-ai": {
    "type": "http",
    "url": "https://mcp.fal.ai/mcp",
    "headers": {
      "Authorization": "Bearer ${FAL_KEY}"
    }
  }
}
```

- **설치 불필요** — 원격 호스팅 MCP
- 1000+ 모델 통합 접근

### elevenlabs (local MCP)

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
- 사전 준비: `uv` 설치 필요 (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [공식 MCP GitHub](https://github.com/elevenlabs/elevenlabs-mcp)

## 스킬 라우팅 가이드

| 생성물 | 주력 스킬 | 백엔드 MCP |
|--------|-----------|-----------|
| 일반 이미지 (시네마틱·제품) | `image-gen` | Higgsfield Soul |
| 한국어 타이포 이미지 | `nano-banana` | Gemini 직접 API |
| 포토리얼리즘 이미지 | `image-gen` | fal-ai Flux |
| 벡터·로고 | `image-gen` → fal-gateway | fal-ai Recraft |
| 시네마틱 영상 (이미지→영상) | `video-gen` | Higgsfield DOP |
| 텍스트→영상, 립싱크 | `video-gen` | fal-ai Kling |
| 말하는 머리 영상 | `speech-video` | Higgsfield |
| 캐릭터 관리 | `character-mgmt` | Higgsfield |
| 음성·TTS | `audio-gen` | ElevenLabs |
| 기타 모델 (1000+) | `fal-gateway` | fal-ai |

## Cowork 공식 커넥터 (선택)

| 커넥터 | 활용 | 대상 스킬 |
|---|---|---|
| **Google Drive** | 생성된 미디어 파일 자동 저장·공유 | 전체 |
| **Canva** | AI 생성 이미지 → Canva 템플릿 합성 | `image-gen`, `nano-banana` |
| **Notion** | 포트폴리오·에셋 라이브러리 관리 | 전체 |
| **YouTube** (선택) | 영상 자동 업로드 | `video-gen` |

## 비용 관리 팁

- **시안 단계**: nano-banana-2 ($0.067), Hailuo Standard ($0.045/sec), Higgsfield Soul 기본
- **최종 단계**: nano-banana-pro ($0.134/2K), Kling Pro ($1.68/10s), Higgsfield DOP 고품질
- Higgsfield 캐릭터 생성 후 재사용 → 브랜드 일관성 + 비용 절감
- fal.ai 대시보드와 Google Cloud Billing에서 월 예산 한도 설정
- `num_images: 1` 기본 유지, A/B 테스트 시만 증가

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| Higgsfield MCP 연결 실패 | `higgsfield-mcp` 미설치 | `pip install higgsfield-mcp` |
| Higgsfield 401 | API 키·시크릿 불일치 | 대시보드에서 키 재확인 |
| Nano Banana 401 | 무료 티어 호출 | Gemini API Pay-as-you-go 활성화 |
| `uvx elevenlabs-mcp` 실패 | `uv` 미설치 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| fal.ai 402 | 무료 크레딧 소진 | [fal.ai/billing](https://fal.ai/billing)에서 충전 |
