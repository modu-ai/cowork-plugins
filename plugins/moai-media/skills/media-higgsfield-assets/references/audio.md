# audio.md — 오디오 생성 (효과음 · 앰비언스 · 음악 · TTS)

> `media-higgsfield-assets` | 텍스트에서 소리를 만드는 경로.
> 아래 값은 저술 시점 라이브 스냅샷이다. 호출 직전 `models_explore(action:'get')`으로 재확인한다.

**Evidence tier:** 1차 (라이브 `models_explore(action:'list', type:'audio')` 관측)

---

## 1. 용도로 모델 고르기

| 원하는 것 | 후보 | 비고 |
|---|---|---|
| 범용 오디오 — 효과음·앰비언스·폴리·환경음·음악풍 | `seed_audio` (ByteDance) | **기본값.** 참조 오디오·이미지도 받음 |
| 다국어 표현형 TTS | `qwen_audio_tts` (Alibaba) | `instruction`으로 감정·방언·속도 지시. 한국어 지원 |
| 엔진 선택형 TTS | `text2speech_v2` (Higgsfield) | `variant`로 ElevenLabs·MiniMax·Seed Speech·Vibe Voice·Cozy Voice 선택 |
| 프리셋 보이스 TTS | `inworld_text_to_speech` | 다국어 프리셋 보이스 목록 보유 |
| 음악 트랙 | `sonilo_music` | ⚠️ 라이브 스키마에 **게임 파이프라인 전용**으로 선언 |
| 효과음 (전용) | `mirelo_text_to_audio` | ⚠️ 라이브 스키마에 **게임 파이프라인 전용**으로 선언 |

**게임 파이프라인 표기 주의:** `sonilo_music`과 `mirelo_text_to_audio`는 라이브 설명에 "Game pipeline only"로 선언돼 있다. 공식 CLI 문서는 이 둘을 범용 음악/효과음 모델처럼 소개하지만, 라이브 스키마가 더 최신이고 더 좁다. 범용 요청에는 `seed_audio`를 기본으로 쓰고, 이 둘은 사용자가 명시하거나 게임 에셋 맥락일 때만 고른다.

---

## 2. `seed_audio` 파라미터

| 파라미터 | 기본 | 값 |
|---|---|---|
| `format` | `wav` | `wav` / `mp3` / `pcm` / `ogg_opus` |
| `sample_rate` | `24000` | 8000 / 16000 / 24000 / 32000 / 44100 / 48000 |
| `speech_rate` | `0` | -50 ~ 100 (양수가 빠름) |
| `loudness_rate` | `0` | -50 ~ 100 |
| `pitch_rate` | `0` | -12 ~ 12 |
| `voice_type` | — | `preset` / `element`. **`voice_id`와 반드시 함께 보낸다** |
| `voice_id` | — | `voice_type`에 대응하는 id. **`voice_type`과 반드시 함께 보낸다** |

미디어 입력은 `image_references` / `audio_references` role을 받는다.

`voice_type`과 `voice_id`는 **짝**이다. 하나만 보내면 오류다.

---

## 3. 한국어 음성 — 두 목록은 서로 다른 곳에서 온다

이 절은 실수하기 쉬운 지점이다. **보이스 목록이 한 곳에 모여 있지 않다.**

| 경로 | 어디서 고르나 | 한국어 |
|---|---|---|
| `seed_audio` · `text2speech_v2` | 보이스 조회 도구가 주는 `voice_id` + `voice_type` 짝 | ❌ 관측된 57종 전부 영어권 이름 |
| `inworld_text_to_speech` | **모델 자체의 `voice` enum** (`Hyunwoo (ko)`·`Minji (ko)`·`Seojun (ko)`·`Yoona (ko)`) | ✅ 4종 |
| `qwen_audio_tts` | `voice_type`+`voice_id`, 별도로 `language: ko` 힌트 | 언어 힌트 지원 |

**함정:** 한국어 음성을 찾겠다고 보이스 조회 도구만 뒤지면 못 찾는다 — 거기엔 없다. `inworld_text_to_speech`의 한국어는 `models_explore(action:'get')`로 그 모델의 `voice` 옵션 목록을 봐야 나온다.

두 목록 모두 고정이 아니므로 호출 직전에 각자의 출처에서 확인한다.

---

## 4. 필수 파라미터 요약

| 모델 | 필수 |
|---|---|
| `seed_audio` | `prompt` |
| `qwen_audio_tts` | `voice_type`, `voice_id` |
| `text2speech_v2` | `variant`, `voice_type`, `voice_id` |
| `inworld_text_to_speech` | `voice` |
| `sonilo_music` | `prompt`, `duration` |
| `mirelo_text_to_audio` | `prompt`, `duration` |

`sonilo_music`과 `mirelo_text_to_audio`는 미디어 입력을 받지 않는다.

---

## 5. 안티패턴

- **`voice_type`만 보내기** — `voice_id`와 짝이다. 하나만 보내면 오류.
- **범용 음악 요청에 `sonilo_music` 기본 사용** — 게임 파이프라인 전용 선언. `seed_audio`가 기본이다.
- **`duration` 누락** — `sonilo_music`·`mirelo_text_to_audio`는 필수다.
- **보이스 id 추측** — 조회 도구로 실제 목록을 확인한다.
- **타인 목소리 무단 복제** — 동의 없는 보이스 클로닝은 하지 않는다.
