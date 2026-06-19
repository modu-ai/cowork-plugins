---
name: notebooklm-slide-prompt
description: |
  강연·강의·세미나 본문 마크다운을 입력받아 (1) NotebookLM Studio에 그대로 붙여 넣을 슬라이드 데크 생성 프롬프트와 (2) 슬라이드별 나노바나나(Gemini 3 Pro Image, a.k.a. Nano Banana Pro) 5-Component 이미지 프롬프트를 동시 산출하는 prompt-builder 스킬.

  NotebookLM Studio의 공식 4축(Format/Length/Output language/Prompt)을 정확히 매핑하고, 슬라이드별 시각 자료는 Google DeepMind 공식 가이드의 5-Component 구조(Style·Subject·Setting·Action·Composition)에 따라 작성한다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "NotebookLM 슬라이드 프롬프트", "NotebookLM 프롬프트", "NotebookLM 데크"
  - "강의 슬라이드 프롬프트", "강연 슬라이드 자료", "세션 슬라이드 프롬프트"
  - "Detailed Deck", "Presenter Slides", "프레젠터 슬라이드", "디테일드 데크"
  - "슬라이드 이미지 프롬프트", "나노바나나 슬라이드", "Nano Banana 슬라이드"
  - "본문 MD를 NotebookLM 프롬프트로 변환", "강연용 슬라이드 자료 만들어줘"
  - "PPT 발표 자료 프롬프트", "발표 슬라이드 통째로 생성"
user-invocable: true
version: 2.27.0
---

# notebooklm-slide-prompt — NotebookLM 슬라이드 데크 + 나노바나나 이미지 프롬프트 빌더

## 한 줄 요약

세션 본문 마크다운을 한 번 입력하면, **NotebookLM Studio에 붙여 넣는 슬라이드 데크 프롬프트**와 **각 슬라이드의 시각 자료를 위한 나노바나나(Gemini 3 Pro Image) 이미지 프롬프트**를 동시에 산출합니다.

## 이 스킬과 pptx-designer의 경계

같은 "발표자료"라도 산출물이 다릅니다. 호출 전 아래 표로 구분하세요.

| 구분 | notebooklm-slide-prompt | pptx-designer |
|---|---|---|
| 산출물 | NotebookLM 소스 정리 + Studio Prompt 텍스트 + 슬라이드별 이미지 프롬프트 | 편집 가능한 `.pptx` 파일 (pptxgenjs 코드) |
| 결과물을 어디서 보나 | NotebookLM Studio가 슬라이드를 생성 | PowerPoint·Keynote에서 바로 열림 |
| 입력 | 강연·강의 본문 MD | 보고서·기획 내용 + 디자인 요구 |
| 언제 쓰나 | "NotebookLM으로 발표자료 만들 프롬프트가 필요" | "지금 바로 열리는 PPT 파일이 필요" |

요약: **NotebookLM에 넣을 준비물(소스·대본·구조·이미지 프롬프트)을 만드는 빌더**가 이 스킬입니다. 실제 `.pptx` 파일이 필요하면 `moai-office:pptx-designer`를 호출하세요. "PPT 파일로 뽑아줘"는 `moai-office:pptx-designer`, "NotebookLM 슬라이드 프롬프트 만들어줘"는 이 스킬입니다.

## 트리거 키워드

다음 표현이 등장하면 본 스킬을 우선 호출:

- "NotebookLM 프롬프트", "NotebookLM 슬라이드", "NotebookLM 데크"
- "강의 슬라이드 프롬프트", "강연 슬라이드 자료", "세션 슬라이드 프롬프트"
- "Detailed Deck", "Presenter Slides", "프레젠터 슬라이드", "디테일드 데크"
- "슬라이드 이미지 프롬프트", "나노바나나 슬라이드", "Nano Banana 슬라이드"
- "MD를 NotebookLM에 넣을 프롬프트로 변환"
- "본문을 슬라이드로 만들 프롬프트 만들어줘"
- "강연용 발표자료 통째로 만들 프롬프트"

## 입력

### 필수

- **세션 본문 MD** — `.md` 파일 또는 본문 직접 첨부. 도입 → 핵심 → 데모 → 정리 4블록 구조면 이상적.

### 선택 (인터뷰로 보완)

- 슬라이드 매수 목표 (예: 12장 / 15장 / 20장)
- 포맷 선호 (`Detailed Deck` vs `Presenter Slides`)
- 길이 선호 (`short` / `default` / `long`)
- 출력 언어 (기본: 한국어)
- 청중·톤 (예: "입문~중급 개발자 + 학생, 솔직한 실무 회고체")
- 시각화 컨셉 (예: "미니멀 다이어그램 + 1컷 시네마틱 표지")
- 브랜드 제약 (폰트·컬러·로고 — 선택)

## 워크플로우 (Phase 1-4)

### Phase 1 — Intake & Interview

본문 MD가 첨부되어 있는지 확인. 없으면 한 줄로 요약된 주제·핵심 포인트라도 받는다. 누락된 선택 항목은 AskUserQuestion 한 라운드(3~4질문 이내)로 묶어서 묻는다:

1. 슬라이드 매수 목표는?
2. Detailed Deck vs Presenter Slides 중 어느 쪽?
3. 시각 자료의 톤은? — `references/slide-style-library.md`의 **49 스타일 × 8 카테고리** 라이브러리에서 발표 키워드에 맞는 카테고리 1~2개를 자동 추천한 뒤 사용자에게 그중 1~3 스타일 후보를 제시 (예: "AI·미래·혁신" 발표라면 카테고리 E의 7·22·43 후보)
4. 반드시 다뤘으면 하는 슬라이드 또는 메시지는?

### Phase 2 — NotebookLM 슬라이드 프롬프트 생성

NotebookLM Studio의 **공식 4축**에 정확히 매핑한다:

| 축 | 매핑 |
|---|---|
| **Format** | `Detailed Deck`(읽기용·풀텍스트) 또는 `Presenter Slides`(발표용·키 토킹 포인트) — 인터뷰 답변 기반 |
| **Length** | `short` / `default` / `long` — 슬라이드 매수 목표 기준 자동 매핑 (≤10 = short, 11~18 = default, ≥19 = long) |
| **Output language** | 기본 한국어. 청중이 다국어면 명시 |
| **Prompt 본문** | 아래 6블록 템플릿 |

#### NotebookLM Prompt 본문 6블록 템플릿

```
[1] 청중 & 사전 지식
   - 이 슬라이드를 볼 사람과 그들의 사전 지식 수준을 명시
   - 예: "클로드 코드 입문~중급 개발자 + 학생·취준생. 에이전틱 코딩 용어는 처음일 수 있음."

[2] 1순위 메시지 (The Single Takeaway)
   - 발표가 끝났을 때 청중이 한 줄로 기억할 메시지
   - 예: "하네스가 있어야 에이전트가 통제된 작품을 만든다."

[3] 슬라이드 구조 지침
   - 표지·도입·핵심·데모·정리·Q&A·다음 단계 — 어떤 흐름으로 배치할지
   - 매수 가이드 (예: "총 15장 ± 2장. 핵심 개념은 1슬라이드 1메시지.")

[4] 톤 & 스타일
   - 어조(예: "솔직한 실무 회고체, 클리셰 금지")
   - 시각 톤(예: "다이어그램 위주, 텍스트 60% 이내, 표지·섹션 구분만 풀이미지")

[5] 강조 슬라이드 (Must-Have Slides)
   - 절대 빠지면 안 되는 슬라이드와 그 슬라이드가 답해야 하는 질문

[6] 금지 / 제약
   - 다루지 말 것 · 피해야 할 표현 · 출처 표기 규칙
   - 예: "혁신적·차세대·재정의하는 같은 클리셰 금지. 코드 인용은 모노스페이스."
```

#### 산출물 형식 (NotebookLM 부분)

````markdown
## NotebookLM Studio 입력값

- Format: Presenter Slides
- Length: default
- Output language: 한국어

## NotebookLM Prompt (이 블록 전체를 Studio의 'Prompt' 칸에 그대로 붙여 넣으세요)

```
[1] 청중 & 사전 지식
…

[2] 1순위 메시지
…

[3] 슬라이드 구조 지침
…

[4] 톤 & 스타일
…

[5] 강조 슬라이드
- 슬라이드 3: "왜 하네스가 필요한가?" — …
- 슬라이드 7: "TRUST-5 다섯 가지 원칙" — …
…

[6] 금지 / 제약
…
```
````

> **공식 출처 사용 시 주의** — NotebookLM은 노트북에 업로드된 소스만 활용한다. 본문 MD를 노트북 **소스로 먼저 업로드**한 뒤, 위 Prompt를 Studio의 슬라이드 데크 Prompt 칸에 입력한다. Prompt 칸에 본문을 통째로 붙여 넣지 않는다.

### Phase 3 — 나노바나나 이미지 프롬프트 생성 (슬라이드별)

본문 MD에서 핵심 슬라이드를 추출한다. 기본 추출 대상:

- 표지 (1장)
- 섹션 구분 슬라이드 (보통 2~3장)
- Must-Have 슬라이드 (인터뷰에서 받은 강조 슬라이드)
- 정리·결론 (1장)

총 **5~8개 슬라이드**가 일반적이며, 각 슬라이드에 대해 **DeepMind 공식 5-Component 구조**를 채운 프롬프트를 생성한다.

#### 5-Component (필수)

| Component | 정의 | 작성 가이드 |
|---|---|---|
| **Style** | 일러스트/사진/수채화/시네마틱/플랫 다이어그램 등 | `references/slide-style-library.md`의 **49 스타일 카탈로그**에서 1개 선택해 영문 프롬프트 키워드를 그대로 사용 — "미니멀 등각 다이어그램(#39)", "시네마틱 우주 SF(#22)" 등 |
| **Subject** | 누가/무엇이 — 외모·복장·포즈까지 구체적으로 | 추상 개념은 의인화·오브제화 — 예: "에이전트는 헬멧을 쓴 작은 로봇" |
| **Setting** | 배경·시간대·분위기 | 강의 주제와 의미적으로 연결 — 예: "터미널 빛이 비치는 어두운 작업실" |
| **Action** | 어떤 동작이 일어나고 있나 | 정지 컷이라도 한 장면의 순간을 명시 — "키보드 위에 손이 올라가는 순간" |
| **Composition** | 앵글·프레이밍·종횡비 | 슬라이드용은 **16:9**, 표지는 **wide cinematic**, 섹션 구분은 **center-weighted** |

#### 추가 옵션 (선택)

- **텍스트 렌더링** — 큰따옴표로 정확한 문구 지정. 예: `the words "하네스 엔지니어링" rendered in a bold sans-serif font`
- **다이어그램 모드** — `a clean isometric diagram of an orchestrator-worker pattern, labeled arrows` 같이 정보 시각화 명시
- **종횡비 / 해상도** — `16:9 widescreen, upscale to 2K` 권장 (강연 슬라이드 기본 16:9)
- **시리즈 일관성** — 한 강연의 모든 시각 자료에 동일한 `Style` + `palette` + `lighting`을 강제. 캐릭터 등장 시 고정 이름 부여 (예: `the agent named "Trust-5"`)
- **세이프티** — 사람 얼굴은 가상 캐릭터·실루엣·후면샷 권장. 실존 인물 묘사 금지.

#### 산출물 형식 (이미지 부분)

```markdown
## 슬라이드별 나노바나나 이미지 프롬프트

### 슬라이드 1 — 표지: "클로드 코드로 시작하는 실전 에이전틱 코딩"

Style: cinematic minimal, dark teal palette with warm amber accents, soft volumetric light
Subject: a small humanoid agent figure made of brushed metal, mid-stride, holding a glowing harness in one hand
Setting: a dimly lit late-night workshop with terminal-blue holographic interface panels floating around
Action: the agent fastening the harness around a translucent code construct that hovers above the desk
Composition: 16:9 widescreen, low-angle hero shot, center-weighted, generous negative space on the right for the title overlay
Text render: the words "하네스 엔지니어링" in a bold sans-serif font, lower-right, no other on-image text
Aspect ratio: 16:9, upscale to 2K
Consistency tag: series="harness-lecture", palette="teal-amber-dim", lighting="volumetric-warm"

### 슬라이드 3 — "왜 하네스가 필요한가?"
…

### (이하 슬라이드별 반복)
```

### Phase 4 — 출력 통합 & 핸드오프

다음 단일 마크다운 파일 1개로 묶어서 산출한다:

- 권장 파일명: `prompts/S{n}-notebooklm-prompt.md` (사용자 프로젝트 경로 기준)
- 구조:
  1. 메타 (세션·청중·매수·포맷)
  2. **Part A — NotebookLM Studio 입력값 + Prompt 본문**
  3. **Part B — 슬라이드별 나노바나나 이미지 프롬프트 (5~8슬라이드)**
  4. 사용 절차 (NotebookLM에 본문 업로드 → Prompt 붙여넣기 → 생성 → 표지·핵심 슬라이드 이미지는 별도 Gemini/Nano Banana Pro로 생성 후 NotebookLM에서 revise로 교체)

체인 종료 직전 `moai-core:ai-slop-reviewer`를 호출해 클리셰·번역투를 제거한다.

## 사용 예시

### 예 1 — 첫 호출 (인터뷰 동반)

```
사용자: "S0 도입 본문을 NotebookLM 슬라이드 프롬프트로 만들어줘"
```

→ 본문 MD를 읽고 매수·포맷·시각 톤·강조 슬라이드 4가지를 AskUserQuestion 한 라운드로 묻는다.  
→ 답변 수신 후 Part A + Part B를 한 마크다운 파일로 산출.

### 예 2 — 매수·톤 직접 지정

```
사용자: "본문을 15장 Presenter Slides로, 시각은 미니멀 등각 다이어그램으로 가자"
```

→ 인터뷰 건너뛰고 즉시 산출. 표지·섹션 구분 슬라이드만 시네마틱, 나머지 다이어그램.

### 예 3 — 이미지 프롬프트만

```
사용자: "S2 슬라이드 7번(TRUST-5 다이어그램) 이미지 프롬프트만 다시"
```

→ Part B의 해당 슬라이드 블록만 재생성.

## 체크리스트 (산출 직전 자가검증)

- [ ] NotebookLM 4축(Format/Length/Language/Prompt)이 모두 명시되어 있는가?
- [ ] Prompt 6블록(청중·1순위 메시지·구조·톤·강조 슬라이드·금지)이 빠짐없는가?
- [ ] 1순위 메시지가 **한 문장**인가? (두 문장 이상이면 분리 실패)
- [ ] 5-Component(Style/Subject/Setting/Action/Composition)가 슬라이드마다 모두 채워졌는가?
- [ ] 모든 슬라이드 이미지가 **동일 series 태그**(palette·lighting·style)를 공유하는가?
- [ ] 종횡비가 16:9로 통일되었는가? (강연 슬라이드 기본)
- [ ] 실존 인물 얼굴, 저작권 캐릭터, 브랜드 로고가 직접 묘사되지 않았는가?
- [ ] 클리셰("혁신적", "차세대", "재정의하는", "결론적으로")가 NotebookLM Prompt에 없는가?
- [ ] AI 슬롭 후처리(ai-slop-reviewer) 실행 예정인가?

## 체이닝 권장

```
notebooklm-slide-prompt
  ↓
moai-core:ai-slop-reviewer
```

본 스킬은 텍스트 산출물이므로 체인 종료 직전 `moai-core:ai-slop-reviewer`로 후처리한다.

실제 이미지 생성은 별도 단계로 분리되어 있다. 사용자는 산출된 5-Component 프롬프트를 다음 도구 중 하나로 실행한다:

- Gemini 앱 (모바일·웹)
- Google AI Studio
- Vertex AI
- (MoAI 사용자) `moai-media:higgsfield-image` 스킬에 그대로 전달

## 안티패턴 (하지 말 것)

- ❌ NotebookLM Prompt 칸에 본문 텍스트를 통째로 붙여 넣는다 — 본문은 노트북 **소스**로 업로드해야 한다. Prompt 칸에는 "어떻게 만들어 달라"는 메타 지시만.
- ❌ 한 슬라이드에 두 개 이상의 핵심 메시지를 욱여넣는다 — 1슬라이드 1메시지 원칙.
- ❌ 슬라이드별 이미지 프롬프트의 Style이 서로 다르다 — 시리즈 일관성이 깨진다.
- ❌ Composition을 비워둔다 — 모델이 임의로 잘라낸 결과가 슬라이드 비율과 안 맞는다.
- ❌ 실존 인물·실재 브랜드·저작권 캐릭터를 직접 묘사한다 — 가상 캐릭터·실루엣·은유로 대체.
- ❌ Detailed Deck인데 텍스트를 줄이라고 지시한다 — 포맷과 길이 지시가 모순.

## 참조 자료 (Progressive Disclosure)

본 스킬은 본문에 모든 가이드를 담는 대신, 시각 스타일 라이브러리를 **별도 reference 파일**로 분리해 필요할 때만 로드합니다.

- **`references/slide-style-library.md`** — 49가지 시각 스타일 × 8 카테고리 라이브러리. Phase 1의 톤 결정 단계와 Phase 3의 5-Component `Style` 필드 작성 시 참조. 발표 키워드 → 스타일 자동 매칭 규칙, 시리즈 일관성 가드(Style·Palette·Lighting·Consistency tag), 안티패턴 카탈로그 내장.

스타일 선택 워크플로우:

```
[Phase 1 인터뷰] 사용자 발화에서 키워드 추출
        ↓
[references/slide-style-library.md "스타일 매칭 가이드"] 카테고리 매핑
        ↓
[AskUserQuestion] 카테고리 내 1~3 스타일 후보 제시 (영문 프롬프트 + 추천 상황 동봉)
        ↓
[Phase 3] 선택된 스타일의 영문 프롬프트 키워드를 모든 슬라이드 `Style:` 필드에 동일 적용
```

## 공식 출처

- NotebookLM Slide Deck 공식 문서 — Google Support  
  <https://support.google.com/notebooklm/answer/16757456>
- Nano Banana(Gemini Image) 프롬프트 작성 가이드 — Google DeepMind  
  <https://deepmind.google/models/gemini-image/prompt-guide/>
- Nano Banana Pro / Gemini 3 Pro Image 발표 — Google Blog  
  <https://blog.google/innovation-and-ai/products/higgsfield-image-pro/>
- Nano Banana 이미지 생성 — Google AI for Developers  
  <https://ai.google.dev/gemini-api/docs/image-generation>

## 참고

- 원본 프롬프트 빌더 설계는 Goos Kim의 "하네스 강연 프로젝트"(2026-05) 내부 자료에서 출발해 재구성된 자료입니다.
- 49가지 시각 스타일 분류(`references/slide-style-library.md`)는 공개된 옵시디언 publish 자료 "노트북 LM 슬라이드 가이드북"(이커머스 클래스, datawave)을 참고해 카테고리·매칭 규칙·일관성 가드를 재구성한 자료입니다.
