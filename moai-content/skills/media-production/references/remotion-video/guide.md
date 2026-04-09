# Remotion 비디오 생성 스킬

React 기반 프로그래밍 영상 제작 프레임워크 **Remotion**을 사용하여, 사용자의 자연어 요청을 완전히 실행 가능한 Remotion 프로젝트 코드로 변환한다.

> **핵심 원칙**: 비개발자도 "유튜브 인트로 영상 만들어줘"라고 말하면, 바로 실행 가능한 프로젝트 코드 + 실행 가이드를 받을 수 있어야 한다.

---

## 1. Remotion 개요

Remotion은 React 컴포넌트로 비디오를 프로그래밍하는 프레임워크다.

- **프레임 기반**: 모든 애니메이션은 `useCurrentFrame()` 훅으로 구동
- **React 컴포넌트**: 각 장면(Scene)이 React 컴포넌트
- **타임라인 제어**: `<Sequence>`, `<Series>`로 장면 순서/타이밍 제어
- **렌더링**: 브라우저에서 프리뷰 → CLI로 MP4/WebM 출력

---

## 2. 비개발자를 위한 실행 흐름

### Step 1: 사용자 요청 분석

사용자가 원하는 영상을 4가지 요소로 분해:

| 요소 | 확인 사항 | 예시 |
|------|----------|------|
| **영상 유형** | 인트로, 프로모션, 데이터 시각화, 교육, SNS 등 | "유튜브 채널 인트로" |
| **길이/해상도** | 초 단위 길이, 해상도 (1080p/4K) | "10초, 1920×1080" |
| **콘텐츠** | 텍스트, 이미지, 로고, 데이터, 음악 등 | "회사 로고 + 슬로건" |
| **스타일** | 미니멀, 다이내믹, 기업형, 네온, 레트로 등 | "깔끔하고 전문적인 느낌" |

누락 항목이 있으면 확인한다.

### Step 2: 프로젝트 코드 생성

완전한 Remotion 프로젝트 구조를 생성:

```
my-video/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── src/
│   ├── Root.tsx              ← Composition 정의
│   ├── Video.tsx             ← 메인 비디오 컴포넌트
│   ├── scenes/
│   │   ├── IntroScene.tsx    ← 인트로 장면
│   │   ├── MainScene.tsx     ← 메인 장면
│   │   └── OutroScene.tsx    ← 아웃트로 장면
│   └── components/
│       ├── AnimatedText.tsx  ← 재사용 컴포넌트
│       └── Logo.tsx
└── public/
    └── (사용자 에셋)
```

### Step 3: 실행 가이드 제공

```bash
# 1. 프로젝트 생성 (사용자 터미널에서)
npx create-video@latest my-video --template blank

# 2. 생성된 코드를 프로젝트에 복사

# 3. 프리뷰 실행
cd my-video && npm start

# 4. 최종 렌더링
npx remotion render src/index.ts MyVideo out/video.mp4
```

---

## 3. 절대 규칙 (Hard Rules)

### 3.1 애니메이션은 반드시 프레임 기반

```tsx
// ✅ 올바른 방법 — useCurrentFrame() + interpolate()
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
});

// ❌ 금지 — CSS transitions, CSS animations, Tailwind animate 클래스
// 이들은 Remotion 렌더링 파이프라인에서 작동하지 않는다
```

### 3.2 시간 계산은 항상 초 × fps

```tsx
const { fps } = useVideoConfig();
const twoSeconds = 2 * fps;  // 30fps → 60프레임
```

### 3.3 Composition은 반드시 Root.tsx에 정의

```tsx
// src/Root.tsx
export const RemotionRoot: React.FC = () => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={300}  // 10초 @ 30fps
    fps={30}
    width={1920}
    height={1080}
  />
);
```

### 3.4 에셋은 staticFile() 또는 import로

```tsx
import { staticFile, Img, Audio, Video } from "remotion";

// public/ 폴더의 파일
<Img src={staticFile("logo.png")} />

// 또는 import
import logo from "./assets/logo.png";
```

### 3.5 Spring 애니메이션 기본값

```tsx
const smooth = { damping: 200 };                    // 부드러운 진입
const snappy = { damping: 20, stiffness: 200 };     // 빠른 반응
const bouncy = { damping: 8 };                      // 통통 튀는 효과
const heavy  = { damping: 15, stiffness: 80, mass: 2 }; // 무거운 느낌
```

---

## 4. 영상 유형별 템플릿

### 4.1 유튜브 인트로 (5~10초)

```
구조: 로고 등장(spring) → 텍스트 페이드인 → 배경 효과
해상도: 1920×1080, 30fps
핵심 기법: spring(), <AbsoluteFill>, 텍스트 애니메이션
```

### 4.2 SNS 프로모션 (15~30초)

```
구조: 후킹 텍스트 → 제품 쇼케이스 → CTA
해상도: 1080×1080 (인스타) 또는 1080×1920 (릴스/숏츠)
핵심 기법: <Sequence>, <Series>, 장면 전환(transitions)
```

### 4.3 데이터 시각화 (10~60초)

```
구조: 타이틀 → 차트 빌드업 → 하이라이트 → 결론
해상도: 1920×1080
핵심 기법: interpolate()로 차트 값 애니메이션, SVG 패스
```

### 4.4 교육/설명 영상 (30초~3분)

```
구조: 인트로 → 섹션별 설명 + 자막 → 아웃트로
해상도: 1920×1080
핵심 기법: <Series>, 자막(subtitles), 보이스오버(TTS)
```

### 4.5 제품 런칭 (15~60초)

```
구조: 티저 → 제품 공개(spring bouncy) → 기능 하이라이트 → CTA
해상도: 1920×1080 또는 4K
핵심 기법: 3D(Three.js), light-leaks, 전환 효과
```

---

## 5. 핵심 API 레퍼런스 (Quick Reference)

### 프레임 & 타이밍

| API | 용도 |
|-----|------|
| `useCurrentFrame()` | 현재 프레임 번호 반환 |
| `useVideoConfig()` | fps, width, height, durationInFrames 반환 |
| `interpolate(frame, inputRange, outputRange, options?)` | 값 보간 |
| `spring({ frame, fps, config?, delay?, durationInFrames? })` | 스프링 애니메이션 (0→1) |
| `Easing.inOut(Easing.quad)` | 이징 커브 |

### 레이아웃 & 시퀀싱

| 컴포넌트 | 용도 |
|----------|------|
| `<Composition>` | 비디오 정의 (Root.tsx에서) |
| `<Sequence from={frame} durationInFrames={n}>` | 특정 시점에 자식 배치 |
| `<Series>` + `<Series.Sequence>` | 순차 배치 (자동 시작점 계산) |
| `<AbsoluteFill>` | 전체 화면 절대 위치 레이어 |
| `<Still>` | 단일 프레임 이미지 |

### 미디어

| 컴포넌트 | 용도 |
|----------|------|
| `<Video src={...} />` | 비디오 임베드 (trim, volume, playbackRate 지원) |
| `<Audio src={...} />` | 오디오 추가 |
| `<Img src={...} />` | 이미지 표시 |
| `<OffthreadVideo>` | 메모리 효율적 비디오 렌더링 |
| `staticFile("file.mp4")` | public/ 폴더 파일 참조 |

### 전환 효과

| 전환 | 효과 |
|------|------|
| `fade()` | 페이드 인/아웃 |
| `slide({ direction })` | 슬라이드 (left/right/top/bottom) |
| `wipe({ direction })` | 와이프 |
| `clockWipe()` | 시계방향 와이프 |
| `flip()` | 뒤집기 |

---

## 6. 코드 생성 규칙

1. **항상 TypeScript 사용** — `.tsx` 확장자, 타입 선언 필수
2. **Pretendard 웹폰트 적용** — 한글 텍스트 포함 시 `loadFont()` 또는 `@fontsource/pretendard`
3. **컴포넌트 분리** — 장면별 파일 분리 (`scenes/`), 재사용 요소 분리 (`components/`)
4. **defaultProps 정의** — 사용자가 나중에 값만 바꿔 재사용 가능하도록
5. **주석은 한글로** — 비개발자가 어떤 부분이 어떤 역할인지 이해할 수 있도록
6. **package.json 포함** — remotion, @remotion/cli 등 필요 패키지 명시
7. **실행 가이드 필수** — 코드 생성 후 반드시 설치/프리뷰/렌더링 명령어 안내

---

## 7. References 구조

상세 규칙은 references/ 하위 파일에서 on-demand로 로드:

| 파일 | 포함 룰 |
|------|---------|
| `core-animation-rules.md` | animations, timing, sequencing, trimming, transitions, compositions |
| `media-rules.md` | audio, video, images, GIFs, Lottie, assets, fonts, sound-effects |
| `advanced-rules.md` | 3D, charts, maps, light-leaks, transparent-videos, subtitles, voiceover, text-animations, audio-visualization |
| `utility-rules.md` | calculate-metadata, parameters, tailwind, ffmpeg, measuring-dom-nodes, measuring-text, extract-frames, can-decode, get-audio-duration, get-video-dimensions, get-video-duration |

> **로딩 전략**: 이 문서의 Quick Reference로 대부분 처리. 특정 기능이 필요할 때만 해당 reference 파일을 로드한다.
