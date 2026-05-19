---
title: "제한 사항과 로드맵"
weight: 90
description: "Research Preview 상태, 웹 전용, 큰 코드베이스 ingestion 지연, Figma 대체 불가의 정확한 위치, 향후 로드맵 추정, 경쟁 도구(v0·Lovable·Figma Make) 비교."
geekdocBreadcrumb: true
---
> Claude Design은 출시 직후 단계의 Research Preview 제품입니다. 현재 무엇이 안 되는지, 무엇이 곧 될 것 같은지, 대안 도구가 더 나은 경우는 언제인지를 정확히 정리합니다.

## 현재 상태 한눈에

| 차원 | 상태 |
|---|---|
| 출시 단계 | **Research Preview** (2026-04-17 출시) |
| 사용 가능 디바이스 | 웹 전용 — claude.ai/design |
| 모바일 앱 지원 | 미지원 |
| 데스크톱 앱 지원 | 미지원 |
| 데이터 거주지 | 미지원 |
| 감사 로그 | 미제공 |
| 사용량 대시보드 | 제한적 |
| 외부 공개 링크 | 없음 |
| API 접근 | 없음 (UI 전용) |
| SSO | Anthropic 일반 정책 (별도 기능 아님) |

## 제한 사항 9가지

### 1. 웹 전용

Claude·Cowork 데스크톱 앱과 모바일 앱에서는 작동하지 않습니다. 브라우저(Chrome·Safari·Firefox·Edge 최신)에서만 사용.

**영향**:
- 오프라인·이동 중 작업 불가
- 모바일에서 빠른 시안 확인 어려움
- 데스크톱 앱 사용자는 브라우저 별도 실행 필요

**대안**: 결과물 PDF·PPTX·HTML로 내보내 모바일에서 확인.

### 2. 큰 코드베이스 ingestion 지연

```
증상: 모노레포 전체 또는 enterprise 규모 코드베이스 연결 시 5분 이상 지연
원인: 디자인 시스템 추출 과정에서 모든 파일을 스캔
```

**복구**:
- UI 패키지 디렉토리만 연결 (예: `packages/ui`)
- `.git`·`node_modules`·`dist`·`build` 제외 확인
- DESIGN.md를 Claude Code에서 사전 합성 후 업로드

### 3. Research Preview의 점진 롤아웃

가입자 모두에게 즉시 활성화되지 않습니다.

| 가입 유형 | 일반적 활성화 시점 |
|---|---|
| 신규 Pro 가입자 | 가입 직후 또는 며칠 내 |
| 기존 Pro 사용자 | 점진 — 기준 비공개 |
| Enterprise | 관리자 활성화 필수 |
| 신규 지역 | 미국·EU 우선, 다른 지역은 후속 |

가입 직후 보이지 않더라도 **며칠 기다리거나 Anthropic 지원 문의**.

### 4. 3D · 음성 · 비디오 초기 단계

```
가능한 것: 정적 UI, 인터랙티브 프로토타입, 마이크로 인터랙션, CSS 애니메이션
초기 단계: 3D 요소, 음성 인터페이스, 실제 비디오 출력
미지원: 복잡한 게임 로직, 실시간 데이터 시각화, AR/VR
```

비디오 "옵션"이 있지만 실제로는 ZIP·HTML·PDF·PPTX로 출력되고 진짜 비디오 파일이 아니라는 사용자 보고가 있습니다.

### 5. Figma 대체가 아님

```
Figma가 더 강한 영역:
- 디자이너 협업·실시간 공동 작업
- 정교한 디자인 시스템 운영 (variables, components, libraries)
- 디자인 ↔ 코드 양방향 (Dev mode)
- 플러그인 생태계
- 외부 공개 링크·프로토타입 공유
- 전문 디자이너 워크플로우 (vector edit·constraints·prototyping)
```

Figma는 UI/UX 디자인 시장의 80-90%를 차지하며 디자인 시스템 운영의 표준입니다. Claude Design은 **저변 확대 도구** (디자이너가 아닌 사람도 시각 자료를 만들 수 있게)로 위치합니다.

### 6. 디자인 ↔ 코드 양방향 약함

```
강함: 디자인 → 코드 (Claude Code 핸드오프 번들)
약함: 코드 → 디자인 (코드 수정 후 디자인 동기화)
```

**현재 우회**: 코드에서 빌드한 결과를 스크린샷으로 캡처해 Claude Design에 다시 입력.

### 7. 사용량 추적·감사 로그 미제공

| 운영 기능 | 상태 |
|---|---|
| 멤버별 사용량 대시보드 | 제한적 |
| 감사 로그 (누가 무엇을 만들었는가) | 미제공 |
| 프로젝트별 토큰 사용량 | 미제공 |
| 사용량 알림 (임계치 도달 시) | 미제공 |

엄격한 거버넌스가 필요한 조직(금융·정부)은 도입 시 이 점을 고려.

### 8. 데이터 거주지 미지원

EU·한국 등 지역 데이터 거주지 요구가 있는 산업에는 적합하지 않습니다.

- 개인정보·금융·의료 데이터는 업로드 자체를 피해야 함
- Enterprise DPA는 서명 가능하지만 데이터 거주지 보장은 아님
- 자세한 데이터 처리 정책은 Anthropic Trust Center 또는 Sales 문의

### 9. PPTX 변환의 한계

```
증상: PPTX 내보내기 시 캔버스 HTML 버전보다 레이아웃이 간소화됨
특히: 배경 그라데이션·복잡한 일러스트·인터랙티브 요소가 단순화 또는 누락
```

**대응**: 정밀한 발표 자료가 필요하면 PDF + HTML을 함께 받아 비교.

## 추가 알려진 이슈 (사용자 보고 기반)

| 이슈 | 빈도 | 우회 |
|---|---|---|
| 인라인 코멘트가 처리 전에 사라짐 | 가끔 | 코멘트 내용을 채팅에 복사·붙여넣기 |
| Compact 뷰에서 저장 에러 | 가끔 | Full 뷰로 전환 |
| 사용량이 대시보드보다 빠르게 소진 | 자주 (사용자 인지) | 디자인 시스템 자체 생성 비용 의식 |
| 큰 시안에서 인터랙션 누락 | 가끔 | 인터랙션을 별도 라운드로 분리 요청 |

## 향후 로드맵 — 추정

Anthropic이 공식 로드맵을 공개하지 않았지만, 출시 공지·인터뷰·사용자 피드백을 종합하면 다음이 단기 우선순위로 보입니다.

| 영역 | 추정 우선순위 |
|---|---|
| 활성화 점진 롤아웃 → 전면 가용 | 가장 빠를 가능성 |
| 데스크톱 앱 통합 | 중기 |
| 감사 로그·사용량 대시보드 | 엔터프라이즈 도입 가속에 필요 → 중기 |
| 데이터 거주지 | EU·아시아 도입 가속에 필요 → 중기 |
| 모바일 앱 | 후순위 (디자인 작업이 모바일에 부적합) |
| 3D·음성·비디오 강화 | 장기 |
| API 접근 | 장기 |
| 디자인 → 코드 양방향 | 장기 (복잡도 큼) |

**중요**: 이 표는 외부 추정이며 Anthropic 공식 약속이 아닙니다. 실제 로드맵은 Anthropic 공식 채널을 확인하세요.

## 경쟁·대체 도구 비교

### Figma Make · v0 · Lovable · Bolt와의 차이

| 도구 | 강점 | 약점 | Claude Design 대비 |
|---|---|---|---|
| **Figma** | 디자이너 협업·시스템 운영 | 프로토타입에서 코드까지 손이 많이 감 | 디자이너 협업·정교한 운영은 Figma, 빠른 시안·핸드오프는 Claude Design |
| **Figma Make** | Figma 내장, 디자이너 친숙 | 별도 디자인 도구와 분리, Figma 안에서 동작 | Figma 사용자에게 Make가 자연스럽지만, 핸드오프·다양한 출력은 Claude Design |
| **v0 (Vercel)** | Next.js·shadcn 컴포넌트, 코드 출력 직접 | UI 위주, 정교한 디자인 시스템 약함 | v0는 빠른 코드·앱 배포, Claude Design은 디자인 단계 탐색·핸드오프 |
| **Lovable** | 한 번에 배포 가능한 앱 | 코드 품질·디자인 시스템 약함 | Lovable은 즉시 배포, Claude Design은 우리 코드베이스·시스템과 통합 |
| **Bolt** | 빠른 풀스택 앱 생성 | 디자인 변형 탐색 약함 | Bolt는 같은 날 배포, Claude Design은 디자인 탐색·발표 자료 |

### 언제 어떤 도구를 쓰나

```
디자이너 협업 + 정교한 시스템 운영           → Figma
빠른 디자인 탐색 + Claude Code 핸드오프       → Claude Design ★
같은 날 풀스택 앱 배포                       → Lovable·Bolt·v0
마케팅 비주얼 다량 생산                      → Canva
프로토타입 → 본격 디자인 도구로 옮기기        → Claude Design → Figma
```

## 보안·규제 관점 위치 정리

| 산업·맥락 | 권장 사용 범위 |
|---|---|
| 일반 SaaS·이커머스 | 자유롭게 사용 가능 |
| 마케팅·미디어 | 자유롭게 사용 가능 |
| 한국 일반 스타트업 | 자유롭게 사용 가능 (개인정보 익명화 후) |
| 한국 핀테크 | 마케팅 자료까지만, 결제·고객 정보는 더미로 |
| 한국 헬스케어 | 환자 데이터·임상 자료 업로드 금지, 일반 마케팅까지만 |
| 정부·공공 | 데이터 거주지·감사 로그 요구 충족 안 됨 — 도입 보류 권장 |
| 군사·국방 | 도입 부적합 |

## Research Preview 동안의 운영 권장

```
□ 모든 결과물에 백업 ZIP을 따로 유지
□ 디자인 시스템 변경 이력을 별도 기록 (감사 로그 없음)
□ 멤버별 사용량을 자율 보고 채널로 추적
□ Anthropic 공지·도움말을 분기 1회 점검 (기능 변동 가능)
□ 외부 발송용 자료에 대해 별도 리뷰 경로
□ "이게 안 된다"는 단점이 발견되면 사내 위키에 기록 — 다음 도입자가 참고
```

## 정말 안 되는 것 — 도입 전 결정 사항

이 중 하나라도 핵심 요구사항이면 **현재 Claude Design은 적합하지 않습니다**.

```
✗ 데이터 거주지 보장이 필요한가
✗ 감사 로그·접근 추적이 엄격하게 요구되는가
✗ 디자이너 협업이 핵심이며 Figma 같은 양방향 도구가 필수인가
✗ 모바일·태블릿에서 디자인 작업이 필요한가
✗ 외부 공개 링크가 필요한가 (PR·이벤트 페이지를 공개 URL로)
✗ 3D·AR·VR 콘텐츠가 주요 산출물인가
✗ API로 디자인 생성을 자동화해야 하는가
```

위 7가지가 모두 No이면 도입 진행 가능. 1개라도 Yes이면 도입 보류·대안 검토.

## 다음 단계

- 참고: [요금제·한도](../pricing-limits/) — Research Preview 단계의 운영 한계
- 참고: [협업·공유](../collaboration/) — 거버넌스 기능 부재 대응
- 섹션 홈: [클로드 디자인 개요](../) — 전체 학습 경로

---

### Sources

- [Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs)
- [Claude Design admin guide for Team and Enterprise plans](https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans)
- [Anthropic launches Claude Design (TechCrunch)](https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/)
- [Claude Design Starter Guide (Claudia + AI)](https://claudiaplusai.substack.com/p/claude-design-starter-guide-and-examples)
- [Claude Design: Complete Guide for Non-Designers (BuildFastWithAI)](https://www.buildfastwithai.com/blogs/claude-design-anthropic-guide-2026)
- [Using Claude Design for prototypes and UX (Anthropic Tutorial)](https://claude.com/resources/tutorials/using-claude-design-for-prototypes-and-ux)
