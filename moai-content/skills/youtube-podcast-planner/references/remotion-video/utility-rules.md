# 유틸리티 규칙 (Utility Rules)

**Remotion 공식 베스트 프랙티스 기반 — 원본: remotion-dev/skills**

---

## 메타데이터 계산 (Calculate Metadata)

`calculateMetadata`를 `<Composition>`에서 사용하여 렌더링 전에 duration, dimensions, props을 동적으로 설정합니다.

```tsx
<Composition
  id="MyComp"
  component={MyComponent}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ videoSrc: "https://remotion.media/video.mp4" }}
  calculateMetadata={calculateMetadata}
/>
```

### 동영상 기준으로 duration 설정

`getVideoDuration`과 `getVideoDimensions` 유틸을 사용하여 동영상 duration과 dimensions을 가져옵니다:

```tsx
import { CalculateMetadataFunction } from "remotion";
import { getVideoDuration } from "./get-video-duration";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const durationInSeconds = await getVideoDuration(props.videoSrc);

  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
  };
};
```

### 동영상의 dimensions 맞추기

`getVideoDimensions` 유틸을 사용하여 동영상 dimensions을 가져옵니다:

```tsx
import { CalculateMetadataFunction } from "remotion";
import { getVideoDuration } from "./get-video-duration";
import { getVideoDimensions } from "./get-video-dimensions";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const dimensions = await getVideoDimensions(props.videoSrc);

  return {
    width: dimensions.width,
    height: dimensions.height,
  };
};
```

### 여러 동영상 기준으로 duration 설정

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const metadataPromises = props.videos.map((video) =>
    getVideoDuration(video.src),
  );
  const allMetadata = await Promise.all(metadataPromises);

  const totalDuration = allMetadata.reduce(
    (sum, durationInSeconds) => sum + durationInSeconds,
    0,
  );

  return {
    durationInFrames: Math.ceil(totalDuration * 30),
  };
};
```

### 기본 출력 파일명 설정

props 기반으로 기본 출력 파일명을 설정합니다:

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  return {
    defaultOutName: `video-${props.id}.mp4`,
  };
};
```

### Props 변환

렌더링 전에 데이터를 fetch하거나 props을 변환합니다:

```tsx
const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
  abortSignal,
}) => {
  const response = await fetch(props.dataUrl, { signal: abortSignal });
  const data = await response.json();

  return {
    props: {
      ...props,
      fetchedData: data,
    },
  };
};
```

`abortSignal`은 Studio에서 props이 변경될 때 stale requests를 취소합니다.

### 반환값

모든 필드는 optional입니다. 반환된 값은 `<Composition>` props을 override합니다:

- `durationInFrames`: 프레임 수
- `width`: Composition 너비 (픽셀)
- `height`: Composition 높이 (픽셀)
- `fps`: 초당 프레임 수
- `props`: 컴포넌트로 전달할 변환된 props
- `defaultOutName`: 기본 출력 파일명
- `defaultCodec`: 렌더링 기본 코덱

---

## 파라미터 (Parameters) — Zod를 사용한 매개변수화

Remotion compositions에 Zod schemas을 추가하여 매개변수화된 동영상을 만듭니다.

### 설치

먼저 패키지 관리자를 사용하여 Zod를 설치합니다:
- npm: `npm i zod`
- bun: `bun i zod`
- yarn: `yarn add zod`
- pnpm: `pnpm i zod`

### 기본 스키마 정의

컴포넌트와 함께 props의 구조를 정의하는 Zod schema를 생성합니다:

```tsx
import { z } from "zod";

export const MyCompositionSchema = z.object({
  title: z.string(),
});
```

### Composition에 등록

root 파일의 `Composition` 컴포넌트에 schema를 `schema` prop으로 전달하고, 스키마 구조와 일치하는 `defaultProps`를 포함합니다.

### 중요한 제약사항

"Remotion requires that the top-level type is a z.object(), because the collection of props of a React component is always an object."

### 색상 선택기 기능

`@remotion/zod-types`를 설치하고 `zColor()`를 import하여 스키마에 시각적 색상 선택기 컨트롤을 추가하고, 사용자가 sidebar interface에서 직접 색상을 편집할 수 있도록 활성화합니다.

---

## Tailwind CSS

Remotion에서 Tailwind CSS 사용 가이드입니다.

### 사용 가능성

프로젝트에 Tailwind CSS가 설치되어 있으면 Remotion에서 사용할 수 있고 사용해야 합니다.

### 중요 제약

`transition-*` 또는 `animate-*` 클래스를 사용하지 마세요. `useCurrentFrame()` hook을 사용하여 항상 애니메이션을 적용하세요.

### 설정

Tailwind는 먼저 Remotion 프로젝트에 설치 및 활성화되어야 합니다. 자세한 설정 지침은 https://www.remotion.dev/docs/tailwind 를 참조하세요.

---

## FFmpeg 및 FFprobe

Remotion에서 FFmpeg와 FFprobe를 사용합니다.

### FFmpeg 설치 불필요

`ffmpeg`과 `ffprobe`를 별도로 설치할 필요가 없습니다. `bunx remotion ffmpeg`과 `bunx remotion ffprobe`를 통해 이용 가능합니다:

```bash
bunx remotion ffmpeg -i input.mp4 output.mp3
bunx remotion ffprobe input.mp4
```

### 동영상 자르기 (Trimming)

동영상을 자르는 2가지 옵션이 있습니다:

1. FFmpeg 커맨드 라인을 사용합니다. 동영상 시작 부분의 frozen frames을 피하기 위해 **반드시 re-encode해야 합니다**:

```bash
# 정확한 프레임에서 re-encodes
bunx remotion ffmpeg -ss 00:00:05 -i public/input.mp4 -to 00:00:10 -c:v libx264 -c:a aac public/output.mp4
```

2. `<Video>` 컴포넌트의 `trimBefore`과 `trimAfter` props을 사용합니다. 이 방법의 장점은 non-destructive이며 언제든지 trim 값을 변경할 수 있다는 것입니다:

```tsx
import { Video } from "@remotion/media";

<Video
  src={staticFile("video.mp4")}
  trimBefore={5 * fps}
  trimAfter={10 * fps}
/>;
```

---

## DOM 노드 측정 (Measuring DOM Nodes)

Remotion에서 DOM 노드를 측정하는 방법입니다.

### 핵심 개념

Remotion은 비디오 컨테이너에 scaling transforms을 적용하여 `getBoundingClientRect()` 측정값에 영향을 줍니다. 정확한 dimensions을 얻으려면 `useCurrentScale()` hook을 사용해야 합니다.

### 접근 방식

현재 scale 값을 구하고 bounding client rectangle 측정값을 그 scale 인수로 나누는 패턴을 사용합니다. `getBoundingClientRect()`로 측정값을 얻은 후 width와 height를 scale로 나누어 unscaled 값을 얻습니다.

이 기법은 DOM 요소 측정값이 scaled 버전이 아닌 실제 dimensions을 반영하도록 보장하며, Remotion의 렌더링 시스템에서 scaling transforms이 컨테이너에 자동으로 적용되는 경우 필수적입니다.

---

## 텍스트 측정 (Measuring Text)

Remotion에서 텍스트를 측정합니다.

### 사전 요구사항

@remotion/layout-utils가 아직 설치되지 않았으면 설치합니다:

```bash
npx remotion add @remotion/layout-utils
```

### 텍스트 dimensions 측정

`measureText()`를 사용하여 텍스트의 너비와 높이를 계산합니다:

```tsx
import { measureText } from "@remotion/layout-utils";

const { width, height } = measureText({
  text: "Hello World",
  fontFamily: "Arial",
  fontSize: 32,
  fontWeight: "bold",
});
```

결과는 캐시됩니다. 중복 호출은 캐시된 결과를 반환합니다.

### 텍스트를 width에 맞추기

`fitText()`를 사용하여 컨테이너에 최적의 font size를 찾습니다:

```tsx
import { fitText } from "@remotion/layout-utils";

const { fontSize } = fitText({
  text: "Hello World",
  withinWidth: 600,
  fontFamily: "Inter",
  fontWeight: "bold",
});

return (
  <div
    style={{
      fontSize: Math.min(fontSize, 80), // 80px로 제한
      fontFamily: "Inter",
      fontWeight: "bold",
    }}
  >
    Hello World
  </div>
);
```

### 텍스트 overflow 확인

`fillTextBox()`를 사용하여 텍스트가 box를 초과하는지 확인합니다:

```tsx
import { fillTextBox } from "@remotion/layout-utils";

const box = fillTextBox({ maxBoxWidth: 400, maxLines: 3 });

const words = ["Hello", "World", "This", "is", "a", "test"];
for (const word of words) {
  const { exceedsBox } = box.add({
    text: word + " ",
    fontFamily: "Arial",
    fontSize: 24,
  });
  if (exceedsBox) {
    // 텍스트가 overflow, 적절히 처리
    break;
  }
}
```

### 베스트 프랙티스

**먼저 폰트를 로드하세요:** 폰트가 로드된 후에만 측정 함수를 호출합니다.

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily, waitUntilDone } = loadFont("normal", {
  weights: ["400"],
  subsets: ["latin"],
});

waitUntilDone().then(() => {
  // 이제 측정 가능
  const { width } = measureText({
    text: "Hello",
    fontFamily,
    fontSize: 32,
  });
});
```

**validateFontIsLoaded 사용:** 폰트 로딩 문제를 조기에 발견합니다:

```tsx
measureText({
  text: "Hello",
  fontFamily: "MyCustomFont",
  fontSize: 32,
  validateFontIsLoaded: true, // 폰트가 로드되지 않으면 throw
});
```

**폰트 속성 일치:** 측정과 렌더링에 동일한 속성을 사용합니다:

```tsx
const fontStyle = {
  fontFamily: "Inter",
  fontSize: 32,
  fontWeight: "bold" as const,
  letterSpacing: "0.5px",
};

const { width } = measureText({
  text: "Hello",
  ...fontStyle,
});

return <div style={fontStyle}>Hello</div>;
```

**padding과 border 피하기:** layout 차이를 방지하기 위해 `border` 대신 `outline`을 사용합니다:

```tsx
<div style={{ outline: "2px solid red" }}>Text</div>
```

---

## 동영상에서 프레임 추출 (Extract Frames)

Mediabunny를 사용하여 지정된 타임스탐프에서 동영상 프레임을 추출합니다.

### 핵심 함수

`extractFrames()` 함수는 동영상 소스 URL, 타임스탐프 배열 (또는 콜백 함수), 그리고 추출된 각 프레임을 VideoSample 객체로 처리하는 핸들러를 accept합니다.

### 주요 사용 사례

**기본 프레임 추출:** `[0, 1, 2, 3, 4]`와 같이 미리 정해진 초 단위에서 프레임을 pull하고 canvas 요소로 렌더링합니다.

**Filmstrip 생성:** 동영상 dimensions과 원하는 프레임 수를 기반으로 타임스탐프를 동적으로 계산하여 responsive thumbnail 스트립을 활성화하는 콜백 함수를 사용합니다.

**취소 지원:** AbortSignal을 구현하여 타임아웃 처리를 가능하게 하고, `setTimeout()` 또는 `Promise.race()`를 사용하여 지정된 기간 후에 작업을 중단할 수 있습니다.

### 구현 세부사항

함수는 비디오 트랙 가용성을 검증하고, 비디오 메타데이터(duration, dimensions, format)를 검색하며, 지정된 타임스탐프에서 샘플을 순회합니다. 각 샘플은 `displayWidth`, `displayHeight`, `timestamp`, 그리고 canvas 렌더링을 위한 `draw()` 메서드를 제공합니다.

문서는 `using` 문을 사용한 리소스 관리의 중요성과 중단된 작업에 대한 오류 처리 패턴을 강조합니다.

---

## 동영상 디코딩 가능 여부 확인 (Can Decode)

Mediabunny를 사용하여 동영상을 브라우저에서 디코딩할 수 있는지 확인합니다.

### Mediabunny 설치

먼저 올바른 버전의 Mediabunny를 설치합니다:

```bash
npx remotion add mediabunny
```

### canDecode() 함수

이 함수는 모든 프로젝트에 복사-붙여넣기할 수 있습니다.

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const canDecode = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  try {
    await input.getFormat();
  } catch {
    return false;
  }

  const videoTrack = await input.getPrimaryVideoTrack();
  if (videoTrack && !(await videoTrack.canDecode())) {
    return false;
  }

  const audioTrack = await input.getPrimaryAudioTrack();
  if (audioTrack && !(await audioTrack.canDecode())) {
    return false;
  }

  return true;
};
```

### 사용 예제

```tsx
const src = "https://remotion.media/video.mp4";
const isDecodable = await canDecode(src);

if (isDecodable) {
  console.log("Video can be decoded");
} else {
  console.log("Video cannot be decoded by this browser");
}
```

### Blob과 함께 사용

파일 업로드 또는 drag-and-drop의 경우 `BlobSource`를 사용합니다:

```tsx
import { Input, ALL_FORMATS, BlobSource } from "mediabunny";

export const canDecodeBlob = async (blob: Blob) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new BlobSource(blob),
  });

  // 위와 동일한 검증 로직
};
```

---

## 오디오 duration 구하기 (Get Audio Duration)

Mediabunny를 사용하여 오디오 파일의 duration을 초 단위로 추출합니다.

### 오디오 duration 구하기

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getAudioDuration = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  const durationInSeconds = await input.computeDuration();
  return durationInSeconds;
};
```

### 사용 예제

```tsx
const duration = await getAudioDuration("https://remotion.media/audio.mp3");
console.log(duration); // 예: 180.5 (초)
```

### Remotion에서 staticFile 사용

파일 경로를 `staticFile()`로 감싸세요:

```tsx
import { staticFile } from "remotion";

const duration = await getAudioDuration(staticFile("audio.mp3"));
```

### Node.js와 Bun에서

`UrlSource` 대신 `FileSource`를 사용합니다:

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // 입력 또는 drag-drop에서 File 객체
});
```

---

## 동영상 dimensions 구하기 (Get Video Dimensions)

Mediabunny를 사용하여 동영상 파일의 너비와 높이를 추출합니다.

### 동영상 dimensions 구하기

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getVideoDimensions = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  const videoTrack = await input.getPrimaryVideoTrack();
  if (!videoTrack) {
    throw new Error("No video track found");
  }

  return {
    width: videoTrack.displayWidth,
    height: videoTrack.displayHeight,
  };
};
```

### 사용 예제

```tsx
const dimensions = await getVideoDimensions("https://remotion.media/video.mp4");
console.log(dimensions.width); // 예: 1920
console.log(dimensions.height); // 예: 1080
```

### 로컬 파일과 함께 사용

`UrlSource` 대신 `FileSource`를 사용합니다:

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // 입력 또는 drag-drop에서 File 객체
});

const videoTrack = await input.getPrimaryVideoTrack();
const width = videoTrack.displayWidth;
const height = videoTrack.displayHeight;
```

### Remotion에서 staticFile 사용

```tsx
import { staticFile } from "remotion";

const dimensions = await getVideoDimensions(staticFile("video.mp4"));
```

---

## 동영상 duration 구하기 (Get Video Duration)

Mediabunny 라이브러리는 여러 JavaScript 환경에서 동영상 파일 duration을 추출하는 기능을 제공합니다.

### 핵심 기능

"Mediabunny can extract the duration of a video file" 이며 브라우저, Node.js, Bun 환경에서 작동합니다. 기본 방법은 format 지정과 소스 참조를 사용하여 Input 객체를 생성한 후 `computeDuration()`을 호출하여 초 단위 결과를 얻는 것입니다.

### 구현 접근 방식

**URL의 경우:** 원격 동영상 파일을 참조하기 위해 `UrlSource`를 사용합니다. 기본 예제는 숫자 값 (예: 10.5초)으로 duration을 반환합니다.

**로컬 공개 파일의 경우:** Remotion의 `staticFile()` 함수를 사용하여 파일 경로를 감싸서 적절한 해석을 보장합니다.

**Node.js/Bun의 경우:** 입력 요소 또는 drag-and-drop 작업으로 얻은 File 객체로 작업할 때 `UrlSource`를 `FileSource`로 교체합니다.

### 핵심 코드 패턴

모든 접근 방식은 일관된 구조를 따릅니다: `ALL_FORMATS`과 선택한 소스 유형으로 Input 객체를 인스턴스화한 후 `computeDuration()`을 호출하여 초 단위 숫자 값으로 duration을 검색합니다.
