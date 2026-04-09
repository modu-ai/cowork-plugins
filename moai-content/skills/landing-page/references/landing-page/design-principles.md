# 프론트엔드 디자인 원칙 레퍼런스

## Design Token 정의 템플릿

페이지 생성 전 반드시 아래 5가지를 먼저 결정한다:

### 1. Color Tokens
```css
:root {
  --bg: oklch(98% 0.01 240);       /* 배경 */
  --surface: oklch(95% 0.01 240);  /* 섹션/카드 배경 */
  --primary: oklch(20% 0.01 240);  /* 주요 텍스트 */
  --muted: oklch(55% 0.01 240);    /* 보조 텍스트 */
  --accent: oklch(55% 0.2 260);    /* 브랜드 / CTA */
}
```

### 2. Typography Roles
| 역할 | 크기 | 용도 |
|------|------|------|
| display | 3rem~4.5rem | 히어로 헤드라인 |
| headline | 1.5rem~2.5rem | 섹션 제목 |
| body | 1rem~1.125rem | 본문 |
| caption | 0.75rem~0.875rem | 보조 정보 |

### 3. Visual Thesis (한 문장)
```
"분위기, 재료, 에너지를 한 문장으로"
예: "깨끗한 화이트 위의 따뜻한 테라코타 액센트, 느린 페이드인으로 신뢰감"
예: "다크 배경의 네온 그린 포인트, 날카로운 타이포와 빠른 슬라이드인"
```

### 4. Content Plan
```
Hero    → 브랜드 약속 + 지배적 비주얼 + CTA
Support → [explain | prove | deepen | convert] 중 택 1
Detail  → [explain | prove | deepen | convert] 중 택 1 (Support와 다른 것)
CTA     → 전환 유도 + 최종 행동
```

### 5. Interaction Thesis (2~3개 모션)
```
예: "히어로 fade-up 시퀀스 → 섹션별 scroll-reveal → CTA pulse hover"
예: "히어로 parallax 배경 → 기능 카드 stagger 입장 → 버튼 spring hover"
```

---

## 히어로 구성 예산

### 허용
- 브랜드명/로고
- 헤드라인 1줄
- 보조 문구 1문장
- CTA 버튼 그룹 (최대 2개)
- 지배적 이미지/비디오

### 금지
- 통계 숫자 나열
- 이벤트 일정표
- 주소/위치 블록
- "이번 주 특가" 류 콜아웃
- 소셜 미디어 아이콘 줄
- 네비게이션 외 링크 목록

---

## Framer Motion 패턴 라이브러리

### Stagger Children (자식 순차 등장)
```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i} variants={item}>{i}</motion.li>
  ))}
</motion.ul>
```

### Scroll Progress Bar
```jsx
import { useScroll, motion } from "framer-motion";

function ProgressBar() {
  const { scrollYProgress } = useScroll();
  return (
    <motion.div
      style={{ scaleX: scrollYProgress }}
      className="fixed top-0 left-0 right-0 h-1 bg-accent origin-left z-50"
    />
  );
}
```

### Parallax Hero Background
```jsx
import { useScroll, useTransform, motion } from "framer-motion";

function ParallaxHero({ children }) {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, 150]);
  const opacity = useTransform(scrollY, [0, 300], [1, 0]);

  return (
    <div className="relative h-screen overflow-hidden">
      <motion.div
        style={{ y }}
        className="absolute inset-0 bg-cover bg-center"
      />
      <motion.div style={{ opacity }} className="relative z-10">
        {children}
      </motion.div>
    </div>
  );
}
```

---

## 웹 앱 UI 설계 (Linear 스타일)

앱 대시보드가 요청된 경우:

### 적용 원칙
- Calm surface hierarchy (차분한 표면 위계)
- 강력한 타이포그래피 + 넓은 간격
- 색상은 accent 1개만
- 조밀하지만 읽기 쉬운 정보
- 최소한의 크롬(장식)

### 피해야 할 것
- Dashboard card mosaics (카드 모자이크)
- 모든 곳의 두꺼운 border
- 장식용 gradient
- 여러 경쟁 accent 색상
