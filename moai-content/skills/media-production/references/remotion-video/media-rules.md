# 미디어 처리 규칙 (Media Rules)

Remotion 공식 베스트 프랙티스 기반 — 원본: remotion-dev/skills

---

## 오디오 사용법 (Using Audio)

### 전제 조건

먼저 `@remotion/media` 패키지를 설치해야 합니다.

```bash
npx remotion add @remotion/media
```

### 오디오 임포트

`@remotion/media`의 `<Audio>` 컴포넌트는 음성을 추가합니다. 로컬 파일(staticFile() 사용)과 원격 URL 모두 지원합니다.

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Audio src={staticFile("audio.mp3")} />;
};
```

여러 오디오 트랙을 겹쳐서 사용할 수 있습니다.

### 트리밍

`trimBefore`와 `trimAfter` 속성으로 섹션을 제거합니다(프레임 단위로 측정).

```tsx
<Audio
  src={staticFile("audio.mp3")}
  trimBefore={2 * fps}
  trimAfter={10 * fps}
/>
```

오디오는 여전히 컴포지션 시작에서 시작하며, 지정된 부분만 재생됩니다.

### 딜레이

오디오를 `<Sequence>`로 감싸서 재생을 지연시킵니다.

```tsx
<Sequence from={1 * fps}>
  <Audio src={staticFile("audio.mp3")} />
</Sequence>
```

### 볼륨 제어

정적 볼륨(0-1)을 설정하거나 동적 콜백을 사용합니다.

```tsx
<Audio src={staticFile("audio.mp3")} volume={0.5} />
// 또는 동적:
<Audio
  src={staticFile("audio.mp3")}
  volume={(f) => interpolate(f, [0, 1 * fps], [0, 1])}
/>
```

### 음소거

`muted` 속성으로 오디오를 동적으로 음소거합니다.

```tsx
<Audio
  src={staticFile("audio.mp3")}
  muted={frame >= 2 * fps && frame <= 4 * fps}
/>
```

### 재생 속도

`playbackRate`로 재생을 조정합니다.

```tsx
<Audio src={staticFile("audio.mp3")} playbackRate={2} />
```

역재생은 지원되지 않습니다.

### 루핑

`loop` 속성을 사용하여 무한 반복하며, `loopVolumeCurveBehavior`로 프레임 카운팅 동작을 제어합니다.

### 피치

`toneFrequency` 속성(0.01-2 범위)으로 속도에 영향을 주지 않고 피치를 조정합니다. 이 기능은 서버 측 렌더링 중에만 작동하며 미리보기에서는 작동하지 않습니다.

---

## 비디오 사용법 (Using Videos)

### 전제 조건

먼저 @remotion/media 패키지를 설치합니다.

```bash
npx remotion add @remotion/media # npm을 사용하는 경우
bunx remotion add @remotion/media # bun을 사용하는 경우
yarn remotion add @remotion/media # yarn을 사용하는 경우
pnpm exec remotion add @remotion/media # pnpm을 사용하는 경우
```

`@remotion/media`에서 `<Video>` 컴포넌트를 사용하여 컴포지션에 비디오를 임베드합니다.

```tsx
import { Video } from "@remotion/media";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Video src={staticFile("video.mp4")} />;
};
```

원격 URL도 지원됩니다.

```tsx
<Video src="https://remotion.media/video.mp4" />
```

### 트리밍

`trimBefore`와 `trimAfter`를 사용하여 비디오의 일부를 제거합니다. 값은 프레임 단위입니다.

```tsx
const { fps } = useVideoConfig();

return (
  <Video
    src={staticFile("video.mp4")}
    trimBefore={2 * fps} // 처음 2초 스킵
    trimAfter={10 * fps} // 10초 마크에서 종료
  />
);
```

### 딜레이

비디오를 `<Sequence>`로 감싸서 표시되는 시간을 지연시킵니다.

```tsx
import { Sequence, staticFile } from "remotion";
import { Video } from "@remotion/media";

const { fps } = useVideoConfig();

return (
  <Sequence from={1 * fps}>
    <Video src={staticFile("video.mp4")} />
  </Sequence>
);
```

비디오는 1초 후에 표시됩니다.

### 크기 및 위치

`style` 속성을 사용하여 크기와 위치를 제어합니다.

```tsx
<Video
  src={staticFile("video.mp4")}
  style={{
    width: 500,
    height: 300,
    position: "absolute",
    top: 100,
    left: 50,
    objectFit: "cover",
  }}
/>
```

### 볼륨

정적 볼륨을 설정합니다(0~1).

```tsx
<Video src={staticFile("video.mp4")} volume={0.5} />
```

또는 현재 프레임을 기반으로 동적 볼륨을 위해 콜백을 사용합니다.

```tsx
import { interpolate } from "remotion";

const { fps } = useVideoConfig();

return (
  <Video
    src={staticFile("video.mp4")}
    volume={(f) =>
      interpolate(f, [0, 1 * fps], [0, 1], { extrapolateRight: "clamp" })
    }
  />
);
```

`muted`를 사용하여 비디오를 완전히 음소거합니다.

```tsx
<Video src={staticFile("video.mp4")} muted />
```

### 재생 속도

`playbackRate`를 사용하여 재생 속도를 변경합니다.

```tsx
<Video src={staticFile("video.mp4")} playbackRate={2} /> {/* 2배 속도 */}
<Video src={staticFile("video.mp4")} playbackRate={0.5} /> {/* 절반 속도 */}
```

역재생은 지원되지 않습니다.

### 루핑

`loop`를 사용하여 비디오를 무한 반복합니다.

```tsx
<Video src={staticFile("video.mp4")} loop />
```

루핑할 때 프레임 카운트 동작을 제어하려면 `loopVolumeCurveBehavior`를 사용합니다.

- `"repeat"`: 루프마다 프레임 카운트가 0으로 리셋됨(volume 콜백용)
- `"extend"`: 프레임 카운트가 계속 증가함

```tsx
<Video
  src={staticFile("video.mp4")}
  loop
  loopVolumeCurveBehavior="extend"
  volume={(f) => interpolate(f, [0, 300], [1, 0])} // 여러 루프에 걸쳐 페이드 아웃
/>
```

### 피치

`toneFrequency`를 사용하여 속도에 영향을 주지 않고 피치를 조정합니다. 값의 범위는 0.01~2입니다.

```tsx
<Video
  src={staticFile("video.mp4")}
  toneFrequency={1.5} // 더 높은 피치
/>
<Video
  src={staticFile("video.mp4")}
  toneFrequency={0.8} // 더 낮은 피치
/>
```

피치 시프트는 Remotion Studio 미리보기나 `<Player />`가 아닌 서버 측 렌더링 중에만 작동합니다.

---

## 이미지 사용법 (Using Images)

### `<Img>` 컴포넌트

이미지를 표시하려면 항상 `remotion`의 `<Img>` 컴포넌트를 사용합니다.

```tsx
import { Img, staticFile } from "remotion";

export const MyComposition = () => {
  return <Img src={staticFile("photo.png")} />;
};
```

### 중요한 제한사항

**반드시 `remotion`의 `<Img>` 컴포넌트를 사용해야 합니다.** 다음을 사용하지 마세요:

- 네이티브 HTML `<img>` 요소
- Next.js `<Image>` 컴포넌트
- CSS `background-image`

이 컴포넌트는 "비디오 내보내기 중 깜박임과 빈 프레임을 방지하여 이미지가 완전히 로드되도록 합니다."

### staticFile()을 사용한 로컬 이미지

이미지를 `public/` 폴더에 배치하고 `staticFile()`을 사용하여 참조합니다.

```
my-video/
├─ public/
│  ├─ logo.png
│  ├─ avatar.jpg
│  └─ icon.svg
├─ src/
├─ package.json
```

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("logo.png")} />;
```

### 원격 이미지

원격 URL은 `staticFile()`없이 직접 사용할 수 있습니다.

```tsx
<Img src="https://example.com/image.png" />
```

원격 이미지에 CORS가 활성화되어 있는지 확인하세요.

애니메이션 GIF의 경우 대신 `@remotion/gif`의 `<Gif>` 컴포넌트를 사용합니다.

### 크기 지정 및 배치

`style` 속성을 사용하여 크기와 위치를 제어합니다.

```tsx
<Img
  src={staticFile("photo.png")}
  style={{
    width: 500,
    height: 300,
    position: "absolute",
    top: 100,
    left: 50,
    objectFit: "cover",
  }}
/>
```

### 동적 이미지 경로

템플릿 리터럴을 사용하여 동적 파일 참조를 만듭니다.

```tsx
import { Img, staticFile, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();

// 이미지 시퀀스
<Img src={staticFile(`frames/frame${frame}.png`)} />

// Props를 기반으로 선택
<Img src={staticFile(`avatars/${props.userId}.png`)} />

// 조건부 이미지
<Img src={staticFile(`icons/${isActive ? "active" : "inactive"}.svg`)} />
```

이 패턴은 다음에 유용합니다.

- 이미지 시퀀스(프레임별 애니메이션)
- 사용자 특정 아바타 또는 프로필 이미지
- 테마 기반 아이콘
- 상태 종속 그래픽

### 이미지 치수 가져오기

`getImageDimensions()`을 사용하여 이미지 치수를 검색합니다.

```tsx
import { getImageDimensions, staticFile } from "remotion";

const { width, height } = await getImageDimensions(staticFile("photo.png"));
```

이 기능은 종횡비 계산 또는 컴포지션 크기 조정에 도움이 됩니다.

```tsx
import {
  getImageDimensions,
  staticFile,
  CalculateMetadataFunction,
} from "remotion";

const calculateMetadata: CalculateMetadataFunction = async () => {
  const { width, height } = await getImageDimensions(staticFile("photo.png"));
  return {
    width,
    height,
  };
};
```

---

## 애니메이션 이미지 사용법 (Using Animated Images)

### 기본 사용법

`<AnimatedImage>`를 사용하여 GIF, APNG, AVIF 또는 WebP 이미지를 Remotion의 타임라인과 동기화하여 표시합니다.

```tsx
import { AnimatedImage, staticFile } from "remotion";

export const MyComposition = () => {
  return (
    <AnimatedImage src={staticFile("animation.gif")} width={500} height={500} />
  );
};
```

원격 URL도 지원됩니다(CORS 활성화 필요).

```tsx
<AnimatedImage
  src="https://example.com/animation.gif"
  width={500}
  height={500}
/>
```

### 크기 조정 및 맞춤

`fit` 속성으로 이미지가 컨테이너에 채워지는 방식을 제어합니다.

```tsx
// 컨테이너를 채우도록 늘이기(기본값)
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="fill" />

// 종횡비 유지, 컨테이너 내에 맞추기
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="contain" />

// 컨테이너 채우기, 필요하면 자르기
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="cover" />
```

### 재생 속도

`playbackRate`를 사용하여 애니메이션 속도를 제어합니다.

```tsx
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} playbackRate={2} /> {/* 2배 속도 */}
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} playbackRate={0.5} /> {/* 절반 속도 */}
```

### 루핑 동작

애니메이션이 끝났을 때의 동작을 제어합니다.

```tsx
// 무한 반복(기본값)
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="loop" />

// 한 번 재생, 최종 프레임 표시
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="pause-after-finish" />

// 한 번 재생, 이후 캔버스 지우기
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="clear-after-finish" />
```

### 스타일링

추가 CSS를 위해 `style` 속성을 사용합니다(크기는 `width`와 `height` 속성 사용).

```tsx
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  style={{
    borderRadius: 20,
    position: "absolute",
    top: 100,
    left: 50,
  }}
/>
```

### GIF 지속 시간 가져오기

`@remotion/gif`에서 `getGifDurationInSeconds()`를 사용하여 GIF의 지속 시간을 가져옵니다.

```bash
npx remotion add @remotion/gif
```

```tsx
import { getGifDurationInSeconds } from "@remotion/gif";
import { staticFile } from "remotion";

const duration = await getGifDurationInSeconds(staticFile("animation.gif"));
console.log(duration); // 예: 2.5
```

이것은 GIF와 일치하도록 컴포지션 지속 시간을 설정할 때 유용합니다.

```tsx
import { getGifDurationInSeconds } from "@remotion/gif";
import { staticFile, CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction = async () => {
  const duration = await getGifDurationInSeconds(staticFile("animation.gif"));
  return {
    durationInFrames: Math.ceil(duration * 30),
  };
};
```

### 대체 방법

`<AnimatedImage>`가 작동하지 않는 경우(Chrome과 Firefox에서만 지원), 대신 `@remotion/gif`의 `<Gif>`를 사용할 수 있습니다.

```bash
npx remotion add @remotion/gif # npm을 사용하는 경우
bunx remotion add @remotion/gif # bun을 사용하는 경우
yarn remotion add @remotion/gif # yarn을 사용하는 경우
pnpm exec remotion add @remotion/gif # pnpm을 사용하는 경우
```

```tsx
import { Gif } from "@remotion/gif";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Gif src={staticFile("animation.gif")} width={500} height={500} />;
};
```

`<Gif>` 컴포넌트는 `<AnimatedImage>`와 동일한 속성을 가지지만 GIF 파일만 지원합니다.

---

## Lottie 애니메이션 사용법 (Using Lottie Animations)

### 전제 조건

먼저 @remotion/lottie 패키지를 설치합니다.

```bash
npx remotion add @remotion/lottie # npm을 사용하는 경우
bunx remotion add @remotion/lottie # bun을 사용하는 경우
yarn remotion add @remotion/lottie # yarn을 사용하는 경우
pnpm exec remotion add @remotion/lottie # pnpm을 사용하는 경우
```

### Lottie 파일 표시

Lottie 애니메이션을 임포트하려면:

- Lottie 자산을 가져옵니다
- 로딩 프로세스를 `delayRender()`와 `continueRender()`로 감싸습니다
- 애니메이션 데이터를 상태에 저장합니다
- `@remotion/lottie` 패키지의 `Lottie` 컴포넌트를 사용하여 Lottie 애니메이션을 렌더링합니다

```tsx
import { Lottie, LottieAnimationData } from "@remotion/lottie";
import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender } from "remotion";

export const MyAnimation = () => {
  const [handle] = useState(() => delayRender("Loading Lottie animation"));

  const [animationData, setAnimationData] =
    useState<LottieAnimationData | null>(null);

  useEffect(() => {
    fetch("https://assets4.lottiefiles.com/packages/lf20_zyquagfl.json")
      .then((data) => data.json())
      .then((json) => {
        setAnimationData(json);
        continueRender(handle);
      })
      .catch((err) => {
        cancelRender(err);
      });
  }, [handle]);

  if (!animationData) {
    return null;
  }

  return <Lottie animationData={animationData} />;
};
```

### 스타일링 및 애니메이션

Lottie는 `style` 속성을 지원하여 스타일과 애니메이션을 허용합니다.

```tsx
return (
  <Lottie animationData={animationData} style={{ width: 400, height: 400 }} />
);
```

---

## 에셋 임포트 (Importing Assets)

### public 폴더

프로젝트 루트의 `public/` 폴더에 에셋을 배치합니다.

### staticFile() 사용

`public/` 폴더의 파일을 참조하려면 **반드시** `staticFile()`을 사용해야 합니다.

```tsx
import { Img, staticFile } from "remotion";

export const MyComposition = () => {
  return <Img src={staticFile("logo.png")} />;
};
```

이 함수는 서브디렉토리에 배포할 때 올바르게 작동하는 인코딩된 URL을 반환합니다.

### 컴포넌트와 함께 사용

**이미지:**

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("photo.png")} />;
```

**비디오:**

```tsx
import { Video } from "@remotion/media";
import { staticFile } from "remotion";

<Video src={staticFile("clip.mp4")} />;
```

**오디오:**

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

<Audio src={staticFile("music.mp3")} />;
```

**폰트:**

```tsx
import { staticFile } from "remotion";

const fontFamily = new FontFace("MyFont", `url(${staticFile("font.woff2")})`);
await fontFamily.load();
document.fonts.add(fontFamily);
```

### 원격 URL

원격 URL은 `staticFile()`없이 직접 사용할 수 있습니다.

```tsx
<Img src="https://example.com/image.png" />
<Video src="https://remotion.media/video.mp4" />
```

### 중요한 참고사항

- Remotion 컴포넌트(`<Img>`, `<Video>`, `<Audio>`)는 렌더링을 시작하기 전에 에셋이 완전히 로드되도록 합니다
- 파일 이름의 특수 문자(`#`, `?`, `&`)는 자동으로 인코딩됩니다

---

## 폰트 사용법 (Using Fonts)

### @remotion/google-fonts를 사용한 Google Fonts

권장되는 Google Fonts 사용 방법입니다. 타입 안전하며 폰트가 준비될 때까지 렌더링을 자동으로 차단합니다.

#### 전제 조건

먼저 @remotion/google-fonts 패키지를 설치합니다.

```bash
npx remotion add @remotion/google-fonts # npm을 사용하는 경우
bunx remotion add @remotion/google-fonts # bun을 사용하는 경우
yarn remotion add @remotion/google-fonts # yarn을 사용하는 경우
pnpm exec remotion add @remotion/google-fonts # pnpm을 사용하는 경우
```

```tsx
import { loadFont } from "@remotion/google-fonts/Lobster";

const { fontFamily } = loadFont();

export const MyComposition = () => {
  return <div style={{ fontFamily }}>Hello World</div>;
};
```

파일 크기를 줄이기 위해 필요한 가중치와 부분집합만 지정합니다.

```tsx
import { loadFont } from "@remotion/google-fonts/Roboto";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "700"],
  subsets: ["latin"],
});
```

#### 폰트 로드 대기

폰트가 준비될 때를 알아야 하는 경우 `waitUntilDone()`을 사용합니다.

```tsx
import { loadFont } from "@remotion/google-fonts/Lobster";

const { fontFamily, waitUntilDone } = loadFont();

await waitUntilDone();
```

### @remotion/fonts를 사용한 로컬 폰트

로컬 폰트 파일의 경우 `@remotion/fonts` 패키지를 사용합니다.

#### 전제 조건

먼저 @remotion/fonts를 설치합니다.

```bash
npx remotion add @remotion/fonts # npm을 사용하는 경우
bunx remotion add @remotion/fonts # bun을 사용하는 경우
yarn remotion add @remotion/fonts # yarn을 사용하는 경우
pnpm exec remotion add @remotion/fonts # pnpm을 사용하는 경우
```

#### 로컬 폰트 로드

폰트 파일을 `public/` 폴더에 배치하고 `loadFont()`를 사용합니다.

```tsx
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

await loadFont({
  family: "MyFont",
  url: staticFile("MyFont-Regular.woff2"),
});

export const MyComposition = () => {
  return <div style={{ fontFamily: "MyFont" }}>Hello World</div>;
};
```

#### 여러 가중치 로드

동일한 family 이름으로 각 가중치를 별도로 로드합니다.

```tsx
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

await Promise.all([
  loadFont({
    family: "Inter",
    url: staticFile("Inter-Regular.woff2"),
    weight: "400",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("Inter-Bold.woff2"),
    weight: "700",
  }),
]);
```

#### 사용 가능한 옵션

```tsx
loadFont({
  family: "MyFont", // 필수: CSS에서 사용할 이름
  url: staticFile("font.woff2"), // 필수: 폰트 파일 URL
  format: "woff2", // 선택사항: 확장자에서 자동 감지됨
  weight: "400", // 선택사항: 폰트 가중치
  style: "normal", // 선택사항: normal 또는 italic
  display: "block", // 선택사항: font-display 동작
});
```

### 컴포넌트에서 사용

`loadFont()`를 컴포넌트의 최상위 레벨이나 일찍 임포트되는 별도의 파일에서 호출합니다.

```tsx
import { loadFont } from "@remotion/google-fonts/Montserrat";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "700"],
  subsets: ["latin"],
});

export const Title: React.FC<{ text: string }> = ({ text }) => {
  return (
    <h1
      style={{
        fontFamily,
        fontSize: 80,
        fontWeight: "bold",
      }}
    >
      {text}
    </h1>
  );
};
```

---

## 참고사항

이 참고 문서는 다음 Remotion 공식 문서를 기반으로 합니다:
- remotion-dev/skills repository
- Remotion 공식 API 문서

**수정 사항**: sound-effects.md 파일이 원본 디렉토리에 존재하지 않아 제외되었습니다.
