---
version: alpha
name: WIRED-design-analysis
description: 페이퍼 화이트·세리프 (getdesign.md 컬렉션 — 테마_컴포넌트_쇼케이스에서 추출한 경량 토큰. 풍부한 브랜드 분석·typography 스케일은 추후 보강.)

colors:
  primary: "#0000ee"
  primary-active: "#0000ee"
  ink: "#111111"
  body: "#111111"
  body-strong: "#111111"
  muted: "#666666"
  muted-soft: "#666666"
  hairline: "#e2e2e2"
  hairline-soft: "#e2e2e2"
  canvas: "#ffffff"
  surface-soft: "#f4f4f4"
  surface-card: "#f4f4f4"
  surface-strong: "#f4f4f4"
  on-primary: "#ffffff"
  success: "#22c55e"
  warning: "#f59e0b"
  error: "#ef4444"

typography:
  display-xl:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: 72px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -2.5px
  display-lg:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -2px
  display-md:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -1.5px
  title-lg:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: 24px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: -0.3px
  title-md:
    fontFamily: "Georgia, 'Times New Roman', serif"
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
  radius: 6px
  radius-button: 6px
  # 분류: light (canvas luminance 기반)
---

# WIRED 디자인 시스템

페이퍼 화이트·세리프. 본 파일은 `테마_컴포넌트_쇼케이스_전체.html`에서 추출한 경량 토큰이며, 풍부한 브랜드 분석과 typography 스케일은 추후 보강 예정입니다.

## 사용

`html-report` / `html-slide`에서 `design_system: wired` 지정 시 본 토큰이 로드됩니다.
