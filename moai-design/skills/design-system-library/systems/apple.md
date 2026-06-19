---
version: alpha
name: Apple-design-analysis
description: 프리미엄 여백·블루·필 버튼 (getdesign.md 컬렉션 — 테마_컴포넌트_쇼케이스에서 추출한 경량 토큰. 풍부한 브랜드 분석·typography 스케일은 추후 보강.)

colors:
  primary: "#0071e3"
  primary-active: "#0071e3"
  ink: "#1d1d1f"
  body: "#1d1d1f"
  body-strong: "#1d1d1f"
  muted: "#6e6e73"
  muted-soft: "#6e6e73"
  hairline: "#d2d2d7"
  hairline-soft: "#d2d2d7"
  canvas: "#ffffff"
  surface-soft: "#f5f5f7"
  surface-card: "#f5f5f7"
  surface-strong: "#f5f5f7"
  on-primary: "#ffffff"
  success: "#22c55e"
  warning: "#f59e0b"
  error: "#ef4444"

typography:
  display-xl:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 72px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -2.5px
  display-lg:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -2px
  display-md:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -1.5px
  title-lg:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 24px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: -0.3px
  title-md:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0px
  body-lg:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0px
  body-md:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0px
  body-sm:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0px

rounded:
  radius: 12px
  radius-button: 22px
  # 분류: light (canvas luminance 기반)
---

# Apple 디자인 시스템

프리미엄 여백·블루·필 버튼. 본 파일은 `테마_컴포넌트_쇼케이스_전체.html`에서 추출한 경량 토큰이며, 풍부한 브랜드 분석과 typography 스케일은 추후 보강 예정입니다.

## 사용

`html-report` / `html-slide`에서 `design_system: apple` 지정 시 본 토큰이 로드됩니다.
