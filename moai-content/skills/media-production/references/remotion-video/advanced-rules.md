# 고급 기능 규칙 (Advanced Rules)

Remotion 공식 베스트 프랙티스 기반 — 원본: remotion-dev/skills

---

## 3D 콘텐츠 (Three.js & React Three Fiber)

Three.js와 React Three Fiber를 사용하여 Remotion에서 3D 콘텐츠를 생성합니다.

### 사전 요구사항

`@remotion/three` 패키지를 설치하세요:

```bash
npx remotion add @remotion/three # npm
bunx remotion add @remotion/three # bun
yarn remotion add @remotion/three # yarn
pnpm exec remotion add @remotion/three # pnpm
```

### ThreeCanvas 사용

모든 3D 콘텐츠는 반드시 `<ThreeCanvas>`로 감싸고 적절한 조명을 포함해야 합니다. 컴포넌트는 `width`와 `height` prop이 필요합니다:

```tsx
import { ThreeCanvas } from "@remotion/three";
import { useVideoConfig } from "remotion";

const { width, height } = useVideoConfig();

<ThreeCanvas width={width} height={height}>
  <ambientLight intensity={0.4} />
  <directionalLight position={[5, 5, 5]} intensity={0.8} />
  <mesh>
    <sphereGeometry args={[1, 32, 32]} />
    <meshStandardMaterial color="red" />
  </mesh>
</ThreeCanvas>;
```

### 애니메이션 요구사항

`useCurrentFrame()`으로 구동되는 애니메이션만 허용됩니다. React Three Fiber의 `useFrame()`은 렌더링 중 깜빡임을 방지하기 위해 금지됩니다.

현재 프레임 값을 활용하여 객체를 애니메이트하세요:

```tsx
const frame = useCurrentFrame();
const rotationY = frame * 0.02;

<mesh rotation={[0, rotationY, 0]}>
  <boxGeometry args={[2, 2, 2]} />
  <meshStandardMaterial color="#4a9eff" />
</mesh>;
```

### Sequence 레이아웃

`<ThreeCanvas>` 내의 모든 `<Sequence>`의 `layout` prop은 반드시 `none`으로 설정하세요:

```tsx
import { Sequence } from "remotion";
import { ThreeCanvas } from "@remotion/three";

const { width, height } = useVideoConfig();

<ThreeCanvas width={width} height={height}>
  <Sequence layout="none">
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#4a9eff" />
    </mesh>
  </Sequence>
</ThreeCanvas>;
```

---

## 차트 (Charts)

React 코드를 사용하여 차트를 생성합니다. HTML, SVG, D3.js가 모두 지원됩니다.

타사 라이브러리의 모든 애니메이션을 비활성화하세요(깜빡임을 유발합니다). 모든 애니메이션은 `useCurrentFrame()`으로 구동하세요.

### 막대 차트

```tsx
const STAGGER_DELAY = 5;
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const bars = data.map((item, i) => {
  const height = spring({
    frame,
    fps,
    delay: i * STAGGER_DELAY,
    config: { damping: 200 },
  });
  return <div style={{ height: height * item.value }} />;
});
```

### 원형 차트

stroke-dashoffset을 사용하여 세그먼트를 애니메이트하고, 12시 방향부터 시작하세요:

```tsx
const progress = interpolate(frame, [0, 100], [0, 1]);
const circumference = 2 * Math.PI * radius;
const segmentLength = (value / total) * circumference;
const offset = interpolate(progress, [0, 1], [segmentLength, 0]);

<circle
  r={radius}
  cx={center}
  cy={center}
  fill="none"
  stroke={color}
  strokeWidth={strokeWidth}
  strokeDasharray={`${segmentLength} ${circumference}`}
  strokeDashoffset={offset}
  transform={`rotate(-90 ${center} ${center})`}
/>;
```

### 꺾은선형 차트 / 경로 애니메이션

SVG 경로를 애니메이트하기 위해 `@remotion/paths`를 사용하세요(꺾은선형 차트, 주식 그래프, 서명).

설치: `npx remotion add @remotion/paths`
문서: https://remotion.dev/docs/paths.md

#### 데이터 포인트를 SVG 경로로 변환

```tsx
type Point = { x: number; y: number };

const generateLinePath = (points: Point[]): string => {
  if (points.length < 2) return "";
  return points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");
};
```

#### 애니메이션을 사용하여 경로 그리기

```tsx
import { evolvePath } from "@remotion/paths";

const path = "M 100 200 L 200 150 L 300 180 L 400 100";
const progress = interpolate(frame, [0, 2 * fps], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
  easing: Easing.out(Easing.quad),
});

const { strokeDasharray, strokeDashoffset } = evolvePath(progress, path);

<path
  d={path}
  fill="none"
  stroke="#FF3232"
  strokeWidth={4}
  strokeDasharray={strokeDasharray}
  strokeDashoffset={strokeDashoffset}
/>;
```

#### 경로를 따라 마커/화살표 이동

```tsx
import {
  getLength,
  getPointAtLength,
  getTangentAtLength,
} from "@remotion/paths";

const pathLength = getLength(path);
const point = getPointAtLength(path, progress * pathLength);
const tangent = getTangentAtLength(path, progress * pathLength);
const angle = Math.atan2(tangent.y, tangent.x);

<g
  style={{
    transform: `translate(${point.x}px, ${point.y}px) rotate(${angle}rad)`,
    transformOrigin: "0 0",
  }}
>
  <polygon points="0,0 -20,-10 -20,10" fill="#FF3232" />
</g>;
```

---

## 지도 애니메이션 (Mapbox)

Mapbox를 사용하여 Remotion 비디오에 지도 애니메이션을 추가합니다. [Mapbox 문서](https://docs.mapbox.com/mapbox-gl-js/api/)에서 API 참고사항을 확인하세요.

### 사전 요구사항

Mapbox와 `@turf/turf`를 설치해야 합니다.

패키지 매니저에 따라 올바른 명령을 실행하세요:

**package-lock.json이 있는 경우:**

```bash
npm i mapbox-gl @turf/turf @types/mapbox-gl
```

**bun.lock이 있는 경우:**

```bash
bun i mapbox-gl @turf/turf @types/mapbox-gl
```

**yarn.lock이 있는 경우:**

```bash
yarn add mapbox-gl @turf/turf @types/mapbox-gl
```

**pnpm-lock.yaml이 있는 경우:**

```bash
pnpm i mapbox-gl @turf/turf @types/mapbox-gl
```

사용자는 무료 Mapbox 계정을 생성하고 https://console.mapbox.com/account/access-tokens/에서 액세스 토큰을 생성해야 합니다.

Mapbox 토큰을 `.env` 파일에 추가하세요:

```txt title=".env"
REMOTION_MAPBOX_TOKEN=pk.your-mapbox-access-token
```

### 지도 추가

Remotion에서 기본 지도 예제입니다:

```tsx
import { useEffect, useMemo, useRef, useState } from "react";
import { AbsoluteFill, useDelayRender, useVideoConfig } from "remotion";
import mapboxgl, { Map } from "mapbox-gl";

export const lineCoordinates = [
  [6.56158447265625, 46.059891147620725],
  [6.5691375732421875, 46.05679376154153],
  [6.5842437744140625, 46.05059898938315],
  [6.594886779785156, 46.04702502069337],
  [6.601066589355469, 46.0460718554722],
  [6.6089630126953125, 46.0365370783104],
  [6.6185760498046875, 46.018420689207964],
];

mapboxgl.accessToken = process.env.REMOTION_MAPBOX_TOKEN as string;

export const MyComposition = () => {
  const ref = useRef<HTMLDivElement>(null);
  const { delayRender, continueRender } = useDelayRender();

  const { width, height } = useVideoConfig();
  const [handle] = useState(() => delayRender("Loading map..."));
  const [map, setMap] = useState<Map | null>(null);

  useEffect(() => {
    const _map = new Map({
      container: ref.current!,
      zoom: 11.53,
      center: [6.5615, 46.0598],
      pitch: 65,
      bearing: 0,
      style: "mapbox://styles/mapbox/standard",
      interactive: false,
      fadeDuration: 0,
    });

    _map.on("style.load", () => {
      // Hide all features from the Mapbox Standard style
      const hideFeatures = [
        "showRoadsAndTransit",
        "showRoads",
        "showTransit",
        "showPedestrianRoads",
        "showRoadLabels",
        "showTransitLabels",
        "showPlaceLabels",
        "showPointOfInterestLabels",
        "showPointsOfInterest",
        "showAdminBoundaries",
        "showLandmarkIcons",
        "showLandmarkIconLabels",
        "show3dObjects",
        "show3dBuildings",
        "show3dTrees",
        "show3dLandmarks",
        "show3dFacades",
      ];
      for (const feature of hideFeatures) {
        _map.setConfigProperty("basemap", feature, false);
      }

      _map.setConfigProperty("basemap", "colorTrunks", "rgba(0, 0, 0, 0)");

      _map.addSource("trace", {
        type: "geojson",
        data: {
          type: "Feature",
          properties: {},
          geometry: {
            type: "LineString",
            coordinates: lineCoordinates,
          },
        },
      });
      _map.addLayer({
        type: "line",
        source: "trace",
        id: "line",
        paint: {
          "line-color": "black",
          "line-width": 5,
        },
        layout: {
          "line-cap": "round",
          "line-join": "round",
        },
      });
    });

    _map.on("load", () => {
      continueRender(handle);
      setMap(_map);
    });
  }, [handle, lineCoordinates]);

  const style: React.CSSProperties = useMemo(
    () => ({ width, height, position: "absolute" }),
    [width, height],
  );

  return <AbsoluteFill ref={ref} style={style} />;
};
```

Remotion에서 중요한 사항:

- 애니메이션은 `useCurrentFrame()`으로 구동되어야 하며, Mapbox 자체가 가져오는 애니메이션은 비활성화해야 합니다. 예를 들어, `fadeDuration` prop은 `0`으로 설정하고, `interactive`는 `false`로 설정하세요.
- 지도 로드는 `useDelayRender()`를 사용하여 지연시켜야 하며, 로드될 때까지 지도를 `null`로 설정해야 합니다.
- ref를 포함하는 요소는 반드시 명시적 너비와 높이, `position: "absolute"`를 가져야 합니다.
- `_map.remove();` 정리 함수를 추가하지 마세요.

### 선 그리기

특별히 요청하지 않는 한 선에 글로우 효과를 추가하지 마세요.
특별히 요청하지 않는 한 선에 추가 포인트를 추가하지 마세요.

### 지도 스타일

기본적으로 `mapbox://styles/mapbox/standard` 스타일을 사용하세요.
기본 지도 스타일에서 레이블을 숨기세요.

별도의 요청이 없으면 Mapbox Standard 스타일에서 모든 기능을 제거하세요:

```tsx
// Hide all features from the Mapbox Standard style
const hideFeatures = [
  "showRoadsAndTransit",
  "showRoads",
  "showTransit",
  "showPedestrianRoads",
  "showRoadLabels",
  "showTransitLabels",
  "showPlaceLabels",
  "showPointOfInterestLabels",
  "showPointsOfInterest",
  "showAdminBoundaries",
  "showLandmarkIcons",
  "showLandmarkIconLabels",
  "show3dObjects",
  "show3dBuildings",
  "show3dTrees",
  "show3dLandmarks",
  "show3dFacades",
];
for (const feature of hideFeatures) {
  _map.setConfigProperty("basemap", feature, false);
}

_map.setConfigProperty("basemap", "colorMotorways", "transparent");
_map.setConfigProperty("basemap", "colorRoads", "transparent");
_map.setConfigProperty("basemap", "colorTrunks", "transparent");
```

### 카메라 애니메이션

선을 따라 카메라를 애니메이트하는 `useEffect` 훅을 추가할 수 있습니다. 이 훅은 현재 프레임에 따라 카메라 위치를 업데이트합니다.

요청하지 않는 한 카메라 각도 사이를 점프하지 마세요.

```tsx
import * as turf from "@turf/turf";
import { interpolate } from "remotion";
import { Easing } from "remotion";
import { useCurrentFrame, useVideoConfig, useDelayRender } from "remotion";

const animationDuration = 20;
const cameraAltitude = 4000;
```

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const { delayRender, continueRender } = useDelayRender();

useEffect(() => {
  if (!map) {
    return;
  }
  const handle = delayRender("Moving point...");

  const routeDistance = turf.length(turf.lineString(lineCoordinates));

  const progress = interpolate(
    frame / fps,
    [0.00001, animationDuration],
    [0, 1],
    {
      easing: Easing.inOut(Easing.sin),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const camera = map.getFreeCameraOptions();

  const alongRoute = turf.along(
    turf.lineString(lineCoordinates),
    routeDistance * progress,
  ).geometry.coordinates;

  camera.lookAtPoint({
    lng: alongRoute[0],
    lat: alongRoute[1],
  });

  map.setFreeCameraOptions(camera);
  map.once("idle", () => continueRender(handle));
}, [lineCoordinates, fps, frame, handle, map]);
```

주의사항:

중요: 기본적으로 카메라를 유지하여 북쪽이 위를 향하도록 하세요.
중요: 멀티 스텝 애니메이션의 경우 점프를 방지하기 위해 모든 단계에서 모든 속성(확대/축소, 위치, 선 진행)을 설정하세요. 초기 값을 재정의하세요.

- 진행률이 최소값으로 고정되어 선이 비어 있지 않도록 하여 turf 오류를 방지합니다.
- 시간 지정 옵션은 [Timing](./timing.md)을 참조하세요.
- 컴포지션의 치수를 고려하고 선을 충분히 두껍게, 라벨 글꼴 크기를 충분히 크게 만들어 컴포지션이 축소될 때 가독성이 유지되도록 하세요.

### 선 애니메이션

#### 직선 (선형 보간)

지도에 직선으로 나타나는 선을 애니메이트하려면 좌표 간에 선형 보간을 사용하세요. turf의 `lineSliceAlong` 또는 `along` 함수를 사용하지 마세요. 이 함수는 Mercator 투영에서 곡선으로 나타나는 측지선(대원) 계산을 사용합니다.

```tsx
const frame = useCurrentFrame();
const { durationInFrames } = useVideoConfig();

useEffect(() => {
  if (!map) return;

  const animationHandle = delayRender("Animating line...");

  const progress = interpolate(frame, [0, durationInFrames - 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });

  // Linear interpolation for a straight line on the map
  const start = lineCoordinates[0];
  const end = lineCoordinates[1];
  const currentLng = start[0] + (end[0] - start[0]) * progress;
  const currentLat = start[1] + (end[1] - start[1]) * progress;

  const lineData: GeoJSON.Feature<GeoJSON.LineString> = {
    type: "Feature",
    properties: {},
    geometry: {
      type: "LineString",
      coordinates: [start, [currentLng, currentLat]],
    },
  };

  const source = map.getSource("trace") as mapboxgl.GeoJSONSource;
  if (source) {
    source.setData(lineData);
  }

  map.once("idle", () => continueRender(animationHandle));
}, [frame, map, durationInFrames]);
```

#### 곡선 (측지선/대원)

두 지점 사이의 측지선(대원) 경로를 따르는 선을 애니메이트하려면 turf의 `lineSliceAlong`을 사용하세요. 이는 비행 경로 또는 지구상의 실제 최단 거리를 표시하는 데 유용합니다.

```tsx
import * as turf from "@turf/turf";

const routeLine = turf.lineString(lineCoordinates);
const routeDistance = turf.length(routeLine);

const currentDistance = Math.max(0.001, routeDistance * progress);
const slicedLine = turf.lineSliceAlong(routeLine, 0, currentDistance);

const source = map.getSource("route") as mapboxgl.GeoJSONSource;
if (source) {
  source.setData(slicedLine);
}
```

### 마커

적절한 곳에 레이블과 마커를 추가하세요.

```tsx
_map.addSource("markers", {
  type: "geojson",
  data: {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        properties: { name: "Point 1" },
        geometry: { type: "Point", coordinates: [-118.2437, 34.0522] },
      },
    ],
  },
});

_map.addLayer({
  id: "city-markers",
  type: "circle",
  source: "markers",
  paint: {
    "circle-radius": 40,
    "circle-color": "#FF4444",
    "circle-stroke-width": 4,
    "circle-stroke-color": "#FFFFFF",
  },
});

_map.addLayer({
  id: "labels",
  type: "symbol",
  source: "markers",
  layout: {
    "text-field": ["get", "name"],
    "text-font": ["DIN Pro Bold", "Arial Unicode MS Bold"],
    "text-size": 50,
    "text-offset": [0, 0.5],
    "text-anchor": "top",
  },
  paint: {
    "text-color": "#FFFFFF",
    "text-halo-color": "#000000",
    "text-halo-width": 2,
  },
});
```

충분히 크게 표시하세요. 컴포지션 치수를 확인하고 라벨을 그에 맞게 스케일하세요.
1920x1080 컴포지션 크기의 경우 라벨 글꼴 크기는 최소 40px이어야 합니다.

중요: `text-offset`을 충분히 작게 유지하여 마커에 가깝게 합니다. 마커 원 반경을 고려하세요. 원 반경이 40인 경우 이는 좋은 오프셋입니다:

```tsx
"text-offset": [0, 0.5],
```

### 3D 건물

3D 건물을 활성화하려면 다음 코드를 사용하세요:

```tsx
_map.setConfigProperty("basemap", "show3dObjects", true);
_map.setConfigProperty("basemap", "show3dLandmarks", true);
_map.setConfigProperty("basemap", "show3dBuildings", true);
```

### 렌더링

지도 애니메이션을 렌더링할 때 다음 플래그를 사용하여 렌더링하세요:

```
npx remotion render --gl=angle --concurrency=1
```

---

## 라이트 리크 효과 (Light Leaks)

### 개요

`@remotion/light-leaks`의 `<LightLeak>` 컴포넌트는 WebGL 기반 라이트 리크 효과를 제공하며, 지속 시간의 전반부에는 나타나고 후반부에는 축소됩니다.

### 설치

이 패키지를 추가하세요: `npx remotion add @remotion/light-leaks`

### 핵심 요구사항

이 기능은 Remotion 버전 4.0.415 이상이 필요합니다.

### 주요 사용 사례

이 컴포넌트는 일반적으로 `<TransitionSeries.Overlay>` 내에 배포되어 씬 전환 사이의 시각적 효과를 만듭니다.

### 구성 옵션

컴포넌트는 3개의 선택적 속성을 허용합니다:

- **durationInFrames**: 효과 타이밍 제어(기본값: 부모 지속 시간)
- **seed**: 다른 패턴 변형 생성(기본값: 0)
- **hueShift**: 색조를 0~360도로 조정(기본값: 0, 황-주황색)

### 구현 유연성

전환 사용 외에, 예를 들어 모든 컴포지션의 장식용 오버레이로 `<LightLeak>`을 `<TransitionSeries>` 외부에서 사용할 수 있습니다.

### 색상 변형

hueShift 매개변수는 사용자 정의를 활성화합니다: 120은 녹색 톤을 생성하고, 240은 파란색 변형을 만듭니다.

---

## 투명 비디오 렌더링 (Transparent Videos)

Remotion은 투명 비디오를 두 가지 방법으로 렌더링할 수 있습니다: ProRes 비디오 또는 WebM 비디오입니다.

### 투명 ProRes

비디오 편집 소프트웨어로 임포트할 때 이상적입니다.

**CLI:**

```bash
npx remotion render --image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444 MyComp out.mov
```

**Studio의 기본값 (변경 후 Studio를 다시 시작하세요):**

```ts
// remotion.config.ts
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("png");
Config.setPixelFormat("yuva444p10le");
Config.setCodec("prores");
Config.setProResProfile("4444");
```

**컴포지션에 대한 기본 내보내기 설정으로 설정** (`calculateMetadata` 사용):

```tsx
import { CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  return {
    defaultCodec: "prores",
    defaultVideoImageFormat: "png",
    defaultPixelFormat: "yuva444p10le",
    defaultProResProfile: "4444",
  };
};

<Composition
  id="my-video"
  component={MyVideo}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
  calculateMetadata={calculateMetadata}
/>;
```

### 투명 WebM (VP9)

브라우저에서 재생할 때 이상적입니다.

**CLI:**

```bash
npx remotion render --image-format=png --pixel-format=yuva420p --codec=vp9 MyComp out.webm
```

**Studio의 기본값 (변경 후 Studio를 다시 시작하세요):**

```ts
// remotion.config.ts
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("png");
Config.setPixelFormat("yuva420p");
Config.setCodec("vp9");
```

**컴포지션에 대한 기본 내보내기 설정으로 설정** (`calculateMetadata` 사용):

```tsx
import { CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  return {
    defaultCodec: "vp8",
    defaultVideoImageFormat: "png",
    defaultPixelFormat: "yuva420p",
  };
};

<Composition
  id="my-video"
  component={MyVideo}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
  calculateMetadata={calculateMetadata}
/>;
```

---

## 자막 및 캡션 (Subtitles & Captions)

모든 캡션은 `@remotion/captions`의 `Caption` 타입을 사용하여 JSON 형식으로 처리해야 합니다.

### 캡션 타입 정의

`Caption` 타입은 5개의 속성으로 구성됩니다:

- `text`: 캡션 콘텐츠
- `startMs`: 캡션이 시작될 때
- `endMs`: 캡션이 끝날 때
- `timestampMs`: 선택적 타임스탐프
- `confidence`: 선택적 신뢰도

### 3가지 주요 워크플로우

문서는 캡션 작업을 위한 3개의 보완적인 가이드를 참조합니다:

1. **전사**: 비디오 및 오디오 파일을 캡션으로 변환하는 지침
2. **디스플레이**: 비디오 내에서 캡션 렌더링 지침
3. **임포트**: .srt 파일에서 캡션을 로드하는 프로세스

각 워크플로우에는 자세한 구현 지침을 제공하는 전용 참조 문서가 있습니다.

---

## 음성 오버 추가 (AI Voiceover)

ElevenLabs TTS를 사용하여 씬별 음성 오디오를 생성한 다음, [`calculateMetadata`](./calculate-metadata)를 사용하여 동적으로 컴포지션 크기를 오디오와 일치하도록 조정합니다.

### 사전 요구사항

기본적으로 이 가이드는 TTS 제공자로 **ElevenLabs**를 사용합니다 (`ELEVENLABS_API_KEY` 환경 변수). 사용자는 오디오 파일을 생성할 수 있는 모든 TTS 서비스로 대체할 수 있습니다.

사용자가 TTS 제공자를 지정하지 않은 경우 ElevenLabs를 권장하고 API 키를 요청하세요.

생성 스크립트를 실행할 때 환경 변수를 사용 가능하게 하세요:

```bash
node --strip-types generate-voiceover.ts
```

### ElevenLabs로 오디오 생성

구성을 읽고, 각 씬에 대해 ElevenLabs API를 호출하고, MP3 파일을 `public/` 디렉토리에 작성하는 스크립트를 만들어 Remotion이 `staticFile()`을 통해 액세스할 수 있도록 합니다.

단일 씬에 대한 핵심 API 호출:

```ts title="generate-voiceover.ts"
const response = await fetch(
  `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
  {
    method: "POST",
    headers: {
      "xi-api-key": process.env.ELEVENLABS_API_KEY!,
      "Content-Type": "application/json",
      Accept: "audio/mpeg",
    },
    body: JSON.stringify({
      text: "Welcome to the show.",
      model_id: "eleven_multilingual_v2",
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75,
        style: 0.3,
      },
    }),
  },
);

const audioBuffer = Buffer.from(await response.arrayBuffer());
writeFileSync(`public/voiceover/${compositionId}/${scene.id}.mp3`, audioBuffer);
```

### calculateMetadata를 사용한 동적 컴포지션 지속 시간

[`calculateMetadata`](./calculate-metadata.md)를 사용하여 [오디오 지속 시간](./get-audio-duration.md)을 측정하고 컴포지션 길이를 그에 맞게 설정합니다.

```tsx
import { CalculateMetadataFunction, staticFile } from "remotion";
import { getAudioDuration } from "./get-audio-duration";

const FPS = 30;

const SCENE_AUDIO_FILES = [
  "voiceover/my-comp/scene-01-intro.mp3",
  "voiceover/my-comp/scene-02-main.mp3",
  "voiceover/my-comp/scene-03-outro.mp3",
];

export const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  const durations = await Promise.all(
    SCENE_AUDIO_FILES.map((file) => getAudioDuration(staticFile(file))),
  );

  const sceneDurations = durations.map((durationInSeconds) => {
    return durationInSeconds * FPS;
  });

  return {
    durationInFrames: Math.ceil(sceneDurations.reduce((sum, d) => sum + d, 0)),
  };
};
```

계산된 `sceneDurations`은 컴포넌트에 `voiceover` prop으로 전달되므로 컴포넌트는 각 씬이 얼마나 오래 지속되어야 하는지 알 수 있습니다.

컴포지션이 [`<TransitionSeries>`](./transitions.md)를 사용하는 경우 총 지속 시간에서 중복을 뺍니다: [./transitions.md#calculating-total-composition-duration](./transitions.md#calculating-total-composition-duration)

### 컴포넌트에서 오디오 렌더링

오디오 렌더링 방법에 대한 자세한 정보는 [audio.md](./audio.md)를 참조하세요.

### 오디오 시작 지연

오디오 시작 지연에 대한 자세한 정보는 [audio.md#delaying](./audio.md#delaying)을 참조하세요.

---

## 텍스트 애니메이션 (Text Animations)

### 개요

이 Remotion 문서는 타이포그래피 및 텍스트 애니메이션 패턴을 다루며, 특히 2가지 핵심 기술에 중점을 둡니다:

### 타이프라이터 효과

`useCurrentFrame()`을 기반으로 문자별로 문자열을 줄여 타이프라이터 효과를 만듭니다. 중요한 베스트 프랙티스가 강조됩니다: 타이프라이터 효과에는 항상 문자열 슬라이싱을 사용하세요. 결코 문자별 불투명도를 사용하지 마세요. 커서 애니메이션 및 문장 일시 중지가 있는 고급 예제가 참조됩니다.

### 단어 강조

문서는 단어 강조를 애니메이트하는 지침을 포함하며, 형광펜 효과와 유사하며, 전용 예제가 제공됩니다.

문서는 다음 태그로 지정됩니다: 타이포그래피, 텍스트, 타이프라이터, 형광펜.

---

## 오디오 시각화 (Audio Visualization)

### 사전 요구사항

```bash
npx remotion add @remotion/media-utils
```

### 오디오 데이터 로드

`useWindowedAudioData()`를 사용하여 오디오 데이터를 로드합니다:

```tsx
import { useWindowedAudioData } from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("podcast.wav"),
  frame,
  fps,
  windowInSeconds: 30,
});
```

### 스펙트럼 막대 시각화

`visualizeAudio()`를 사용하여 막대 차트를 위한 주파수 데이터를 얻습니다:

```tsx
import { useWindowedAudioData, visualizeAudio } from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("music.mp3"),
  frame,
  fps,
  windowInSeconds: 30,
});

if (!audioData) {
  return null;
}

const frequencies = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 256,
  optimizeFor: "speed",
  dataOffsetInSeconds,
});

return (
  <div style={{ display: "flex", alignItems: "flex-end", height: 200 }}>
    {frequencies.map((v, i) => (
      <div
        key={i}
        style={{
          flex: 1,
          height: `${v * 100}%`,
          backgroundColor: "#0b84f3",
          margin: "0 1px",
        }}
      />
    ))}
  </div>
);
```

주요 포인트:

- `numberOfSamples`는 2의 거듭제곱이어야 합니다 (32, 64, 128, 256, 512, 1024)
- 값의 범위는 0-1입니다. 배열의 왼쪽은 저음, 오른쪽은 고음입니다.
- Lambda 또는 높은 샘플 수의 경우 `optimizeFor: "speed"`를 사용합니다.

중요: `audioData`를 자식 컴포넌트에 전달할 때, 부모에서 `frame`도 전달하세요. 각 자식에서 `useCurrentFrame()`을 호출하지 마세요. `<Sequence>` 오프셋으로 시각화가 불연속적이 되는 것을 방지합니다.

### 파형 시각화

`visualizeAudioWaveform()`을 `createSmoothSvgPath()`와 함께 사용하여 오실로스코프 스타일 디스플레이를 만듭니다:

```tsx
import {
  createSmoothSvgPath,
  useWindowedAudioData,
  visualizeAudioWaveform,
} from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { width, fps } = useVideoConfig();
const HEIGHT = 200;

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("voice.wav"),
  frame,
  fps,
  windowInSeconds: 30,
});

if (!audioData) {
  return null;
}

const waveform = visualizeAudioWaveform({
  fps,
  frame,
  audioData,
  numberOfSamples: 256,
  windowInSeconds: 0.5,
  dataOffsetInSeconds,
});

const path = createSmoothSvgPath({
  points: waveform.map((y, i) => ({
    x: (i / (waveform.length - 1)) * width,
    y: HEIGHT / 2 + (y * HEIGHT) / 2,
  })),
});

return (
  <svg width={width} height={HEIGHT}>
    <path d={path} fill="none" stroke="#0b84f3" strokeWidth={2} />
  </svg>
);
```

### 저음-반응 효과

저음 주파수를 추출하여 비트 반응 애니메이션을 만듭니다:

```tsx
const frequencies = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 128,
  optimizeFor: "speed",
  dataOffsetInSeconds,
});

const lowFrequencies = frequencies.slice(0, 32);
const bassIntensity =
  lowFrequencies.reduce((sum, v) => sum + v, 0) / lowFrequencies.length;

const scale = 1 + bassIntensity * 0.5;
const opacity = Math.min(0.6, bassIntensity * 0.8);
```

### 볼륨 기반 파형

주파수 스펙트럼 대신 단순화된 볼륨 데이터를 위해 `getWaveformPortion()`을 사용합니다:

```tsx
import { getWaveformPortion } from "@remotion/media-utils";
import { useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const currentTimeInSeconds = frame / fps;

const waveform = getWaveformPortion({
  audioData,
  startTimeInSeconds: currentTimeInSeconds,
  durationInSeconds: 5,
  numberOfSamples: 50,
});

// Returns array of { index, amplitude } objects (amplitude: 0-1)
waveform.map((bar) => (
  <div key={bar.index} style={{ height: bar.amplitude * 100 }} />
));
```

### 후처리

저음 주파수는 자연스럽게 지배적입니다. 시각적 균형을 위해 로그 스케일링을 적용합니다:

```tsx
const minDb = -100;
const maxDb = -30;

const scaled = frequencies.map((value) => {
  const db = 20 * Math.log10(value);
  return (db - minDb) / (maxDb - minDb);
});
```
