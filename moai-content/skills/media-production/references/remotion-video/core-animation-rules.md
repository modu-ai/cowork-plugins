# 핵심 애니메이션 규칙 (Core Animation Rules)

**Remotion 공식 베스트 프랙티스 기반** — 원본: remotion-dev/skills

---

## 1. 애니메이션 기초 (Animations)

Remotion의 공식 문서에서는 모든 애니메이션이 `useCurrentFrame()` 훅으로 구동되어야 한다고 명시합니다. 개발자는 "초 단위로 애니메이션을 작성한 후 `useVideoConfig()`에서 얻은 `fps` 값으로 곱해야 한다"고 권장합니다.

제공된 코드 예시는 `interpolate` 함수를 사용하여 프레임 기반 애니메이션으로 2초에 걸쳐 불투명도를 0에서 1로 전환하는 페이드인(fade-in) 효과를 보여줍니다.

두 가지 중요한 제한 사항이 강조됩니다:

1. **CSS 전환/애니메이션은 금지됨** — Remotion에서 올바르게 렌더링되지 않습니다
2. **Tailwind 애니메이션 클래스는 금지됨** — 역시 올바르게 렌더링되지 않습니다

이 접근 방식은 브라우저 네이티브 애니메이션 메커니즘 대신 명시적 프레임 계산에 모든 동작을 연결하여 Remotion의 렌더링 파이프라인 내에서 애니메이션이 올바르게 작동하도록 보장합니다.

---

## 2. 타이밍과 보간 (Timing & Interpolation)

### 선형 보간 (Linear Interpolation)

기본 선형 보간은 `interpolate` 함수를 사용합니다:

```ts title="Going from 0 to 1 over 100 frames"
import { interpolate } from "remotion";

const opacity = interpolate(frame, [0, 100], [0, 1]);
```

기본적으로 값은 고정되지 않으므로 값이 [0, 1] 범위 밖으로 나갈 수 있습니다. 다음은 고정하는 방법입니다:

```ts title="Going from 0 to 1 over 100 frames with extrapolation"
const opacity = interpolate(frame, [0, 100], [0, 1], {
  extrapolateRight: "clamp",
  extrapolateLeft: "clamp",
});
```

### 스프링 애니메이션 (Spring Animations)

스프링 애니메이션은 더욱 자연스러운 움직임을 제공합니다. 시간에 따라 0에서 1로 전환됩니다.

```ts title="Spring animation from 0 to 1 over 100 frames"
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
});
```

#### 물리적 속성 (Physical Properties)

기본 설정은 `mass: 1, damping: 10, stiffness: 100`입니다. 이는 애니메이션이 정착하기 전에 약간의 바운스를 가지도록 합니다.

설정을 다음과 같이 덮어쓸 수 있습니다:

```ts
const scale = spring({
  frame,
  fps,
  config: { damping: 200 },
});
```

바운스 없이 자연스러운 움직임을 위한 권장 설정은 `{ damping: 200 }`입니다.

다음은 일반적인 설정입니다:

```tsx
const smooth = { damping: 200 }; // Smooth, no bounce (subtle reveals)
const snappy = { damping: 20, stiffness: 200 }; // Snappy, minimal bounce (UI elements)
const bouncy = { damping: 8 }; // Bouncy entrance (playful animations)
const heavy = { damping: 15, stiffness: 80, mass: 2 }; // Heavy, slow, small bounce
```

#### 지연 (Delay)

애니메이션은 기본적으로 즉시 시작됩니다. `delay` 파라미터를 사용하여 프레임 수만큼 애니메이션을 지연시킵니다.

```tsx
const entrance = spring({
  frame: frame - ENTRANCE_DELAY,
  fps,
  delay: 20,
});
```

#### 지속 시간 (Duration)

`spring()`은 물리적 속성을 기반으로 자연스러운 지속 시간을 가집니다. 애니메이션을 특정 지속 시간으로 확대하려면 `durationInFrames` 파라미터를 사용합니다.

```tsx
const spring = spring({
  frame,
  fps,
  durationInFrames: 40,
});
```

#### spring()과 interpolate() 조합하기

스프링 출력(0-1)을 커스텀 범위로 매핑합니다:

```tsx
const springProgress = spring({
  frame,
  fps,
});

// Map to rotation
const rotation = interpolate(springProgress, [0, 1], [0, 360]);

<div style={{ rotate: rotation + "deg" }} />;
```

#### 스프링 더하기 (Adding Springs)

스프링은 단순히 숫자를 반환하므로 수학 연산을 수행할 수 있습니다:

```tsx
const frame = useCurrentFrame();
const { fps, durationInFrames } = useVideoConfig();

const inAnimation = spring({
  frame,
  fps,
});
const outAnimation = spring({
  frame,
  fps,
  durationInFrames: 1 * fps,
  delay: durationInFrames - 1 * fps,
});

const scale = inAnimation - outAnimation;
```

### 이징 (Easing)

이징을 `interpolate` 함수에 추가할 수 있습니다:

```ts
import { interpolate, Easing } from "remotion";

const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

기본 이징은 `Easing.linear`입니다. 다른 여러 곡선이 있습니다:

- `Easing.in` — 느리게 시작하고 가속
- `Easing.out` — 빠르게 시작하고 느려짐
- `Easing.inOut` — 양쪽 끝에서 느림

그리고 곡선들(가장 선형에서 가장 곡선까지 정렬):

- `Easing.quad`
- `Easing.sin`
- `Easing.exp`
- `Easing.circle`

곡선 형태와 곡선을 이징 함수에 대해 결합해야 합니다:

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

3차 베지어 곡선도 지원됩니다:

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

---

## 3. 시퀀싱 패턴 (Sequencing Patterns)

이 섹션은 Remotion의 `<Sequence>`와 `<Series>` 컴포넌트를 포함한 타이밍 및 시퀀싱 패턴을 다룹니다.

### 핵심 컴포넌트 (Key Components)

**Sequence 컴포넌트**: `from` 프레임과 `durationInFrames`를 지정하여 요소가 나타나는 시간을 지연시킵니다. 문서에서 "기본적으로 이는 `layout="none"`을 사용하지 않는 한 절대 채움 요소에서 컴포넌트를 래핑합니다"라고 명시합니다.

**Series 컴포넌트**: 다중 요소를 간격 없이 순차적으로 재생하도록 배열합니다. 자식 시퀀스는 `durationInFrames` 프롭을 사용하는 `<Series.Sequence>`를 사용합니다.

### 중요한 개념 (Important Concepts)

- **미리 마운트 (Premounting)**: 가이드에서는 개발자가 `premountFor` 프롭을 사용하여 "항상 `<Sequence>`를 미리 마운트해야 한다"고 강조합니다. 이는 재생 전에 컴포넌트를 로드합니다.

- **로컬 프레임 참조 (Local Frame References)**: Sequence 내에서 `useCurrentFrame()`은 절대 타임라인 위치가 아닌 0부터 시작하는 로컬 프레임 수를 반환합니다.

- **겹치는 시퀀스 (Overlapping Sequences)**: 음수 `offset` 값은 시퀀스가 겹치도록 활성화하며, "-15"는 이전 시퀀스가 끝나기 15프레임 전에 시작합니다.

- **중첩 (Nesting)**: 복잡한 타이밍 배열을 위해 시퀀스와 전체 컴포지션을 중첩할 수 있습니다.

문서는 각 패턴의 구현을 보여주는 다중 코드 예시를 제공합니다.

---

## 4. 트리밍 패턴 (Trimming Patterns)

음수 `from` 값으로 `<Sequence>`를 사용하여 애니메이션의 시작을 트리밍합니다.

### 시작 부분 트리밍 (Trim the Beginning)

음수 `from` 값은 시간을 역으로 이동하여 애니메이션이 도중에 시작되게 합니다:

```tsx
import { Sequence, useVideoConfig } from "remotion";

const fps = useVideoConfig();

<Sequence from={-0.5 * fps}>
  <MyAnimation />
</Sequence>;
```

애니메이션은 진행 과정 15프레임 지점에 나타남 — 처음 15프레임이 잘려나감. `<MyAnimation>` 내에서 `useCurrentFrame()`은 0이 아닌 15부터 시작합니다.

### 끝 부분 트리밍 (Trim the End)

`durationInFrames`를 사용하여 지정된 지속 시간 후 콘텐츠를 마운트 해제합니다:

```tsx
<Sequence durationInFrames={1.5 * fps}>
  <MyAnimation />
</Sequence>
```

애니메이션은 45프레임 동안 재생된 후 컴포넌트가 마운트 해제됩니다.

### 트리밍과 지연 (Trim and Delay)

시퀀스를 중첩하여 시작을 트리밍하고 나타나는 시간을 지연시킵니다:

```tsx
<Sequence from={30}>
  <Sequence from={-15}>
    <MyAnimation />
  </Sequence>
</Sequence>
```

내부 시퀀스는 시작에서 15프레임을 트리밍하고, 외부 시퀀스는 결과를 30프레임 지연시킵니다.

---

## 5. 전환과 오버레이 (Transitions & Overlays)

이 페이지는 비디오 컴포지션에서 장면 전환과 오버레이를 생성하기 위한 Remotion의 `TransitionSeries` 컴포넌트를 문서화합니다.

### 핵심 컴포넌트 (Key Components)

문서에서는 두 가지 주요 개선 방법을 설명합니다:

**전환 (Transitions)** — "두 장면 사이에 크로스페이드 및 슬라이드 같은 시각 효과를 생성합니다. 두 장면이 전환 중에 동시에 재생되므로 타임라인이 단축됩니다."

**오버레이 (Overlays)** — "컷 지점 위에 효과를 렌더링할 수 있습니다. 타임라인을 단축하지 않습니다."

### 설치 (Installation)

기능에 필요: `npx remotion add @remotion/transitions`

### 사용 가능한 전환 (Available Transitions)

다섯 가지 내장 전환 유형이 문서화되어 있습니다:
- fade
- slide (방향 옵션 포함)
- wipe
- flip
- clockWipe

### 타이밍 제어 (Timing Control)

두 가지 타이밍 접근 방식을 사용할 수 있습니다: 일정한 속도의 선형 타이밍과 물리 기반 계산을 사용한 유기적 동작의 스프링 타이밍.

### 지속 시간 메커니즘 (Duration Mechanics)

중요한 구별: "전환은 인접한 장면을 겹치므로 전체 컴포지션 길이는 모든 시퀀스 지속 시간의 합보다 짧습니다. 오버레이는 전체 지속 시간에 영향을 주지 않습니다."

문서는 여러 전환이 적용될 때 컴포지션 지속 시간을 계산하는 상세한 예시를 포함하며, 전환 길이가 전체 타임라인 길이를 어떻게 줄이는지 보여줍니다.

### 제약 규칙 (Constraint Rules)

문서에서는 "오버레이는 전환 또는 다른 오버레이에 인접할 수 없습니다"라고 명시합니다. 그러나 오버레이와 전환은 적절하게 배열될 때 동일한 컴포넌트 내에서 공존할 수 있습니다.

---

## 6. 컴포지션 (Compositions)

문서에서는 일반적으로 `src/Root.tsx`에 배치된 Remotion의 `<Composition>` 컴포넌트를 사용하여 렌더링 가능한 비디오를 구조화하는 방법을 정의합니다.

### 핵심 컴포넌트 (Core Components)

**Composition**: 비디오의 컴포넌트, 치수, 프레임 속도, 지속 시간을 확립합니다. 필수 프롭에는 `id`, `component`, `durationInFrames`, `fps`, `width`, `height`가 포함됩니다.

**Still**: `durationInFrames` 또는 `fps` 파라미터가 필요 없는 단일 프레임 이미지를 생성합니다.

**Folder**: 문자, 숫자, 하이픈만 사용하여 사이드바에서 컴포지션을 정렬합니다.

### 핵심 기능 (Key Features)

**기본 프롭 (Default Props)**: `defaultProps` 속성은 컴포넌트에 초기 값을 제공합니다. 가이드에서 "값은 JSON 직렬화 가능해야 합니다(`Date`, `Map`, `Set`, `staticFile()`은 지원됩니다). 타입 안정성을 위해 인터페이스보다 타입 선언을 사용해야 합니다."라고 명시합니다.

**동적 메타데이터 (Dynamic Metadata)**: `calculateMetadata` 함수는 외부 데이터를 기반으로 치수, 지속 시간, 프롭이 조응하도록 합니다. 이 비동기 함수는 프롭과 중단 신호를 받아 렌더링이 시작하기 전에 수정된 메타데이터를 반환합니다.

**중첩된 컴포지션 (Nested Compositions)**: `width`와 `height` 프롭이 있는 `<Sequence>` 컴포넌트는 다른 컴포지션 내에서 컴포지션을 임베드할 수 있습니다.

---

## 참고 사항

이 문서는 Remotion의 공식 베스트 프랙티스를 기반으로 작성되었으며, 모든 코드 예시는 원본 문서에서 그대로 유지되었습니다. 한국어 설명을 통해 개발자가 아닌 사용자도 각 개념의 목적을 이해할 수 있도록 구성했습니다.
