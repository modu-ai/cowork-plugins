# logo-principles.md — 로고 5원칙 · 스케일러빌리티 · 한계 · 정합 검증

> `design-logo` 참조 파일. 정합 검증과 기대치 설정에 연다.

## 로고 디자인 5원칙 (Jacob Cass, Just Creative)

업계에서 가장 널리 인용되는 프레임워크.

| 원칙 | 핵심 |
|---|---|
| **Simple** (단순) | 복잡할수록 인지 비용이 크고 기억에 안 남는다 |
| **Memorable** (기억성) | 로고가 브랜드를 즉시 떠오르게 해야 한다 |
| **Timeless** (영속성) | 트렌드를 따르면 트렌드가 죽을 때 같이 죽는다 |
| **Versatile** (다용도성) | 모든 화면·매체·크기에서 작동 (scalability 포함) |
| **Appropriate** (적절성) | 브랜드 정체성을 드러내면서 업종을 암시 |

> 원문: *"your logo could become outdated when the trend loses popularity"* (Jacob Cass)

## SMART 변형 — R은 Resizable (Logogeek)

같은 다섯 가지를 약어로 묶은 변형. AI 로고 작업에서는 R(Resizable)이 가장 실용적이다: *"from pen to building"* — 벡터 포맷으로 디자인할 것.

Paul Rand의 경고: *"a design that is complex, fussy, or obscure harbors a self-destructive mechanism"* — 복잡한 디자인은 자멸 메커니즘을 품는다.

## AI 생성 로고에서 가장 중요한 3가지

Simple, Memorable, Versatile(Resizable). AI 모델은 복잡한 디테일(그라디언트, 미세 텍스처, 얇은 라인)을 잘 표현하지만, 정작 이것들은 **작은 크기에서 깨지고 인쇄에서 망가진다**. 따라서 프롬프트에 의도적으로 단순화 지시어(flat colors only, no gradients, no shadows)를 넣어야 5원칙을 만족한다.

## 스케일러빌리티 — 왜 벡터인가

래스터(JPG/PNG)는 픽셀 단위라 유한한 크기를 갖고, 확대하면 흐려진다. 프로 로고는 AI/SVG/EPS/PDF 같은 수학적 곡선 기반 벡터 — 무한히 확장해도 선명하다.

- 전형적 AI 생성 JPG: 1000-1500px → 고품질 인쇄 시 3-4인치가 한계.
- 벡터 로고: 1인치든 100피트든 완벽하게 보인다.

**Recraft는 SVG 같은 벡터 포맷을 지원** — 이것이 Recraft를 로고에 선택하는 주요 이유. 생성 위임 시 벡터 출력 가능 여부를 `models_explore`로 확인한다.

## 변형 시스템 (산출물)

하나의 로고는 여러 변형이 필요하다:
- **컬러 버전** (풀 컬러)
- **흑백 버전** (grayscale)
- **단색 실루엣** (단색 배경에 얹기 위함 — 인식의 진짜 시험)
- **앱 아이콘 / 파비콘** (작은 크기)
- **수직/수평 락업** (콤비네이션인 경우)

단색 실루엣으로 변형해도 인식되지 않으면, 로고가 형태가 아니라 색/디테일에 의존하는 것이다 — 단순화가 필요하다.

## AI 생성의 한계 (반드시 사용자에게 알릴 것)

### 1. 복잡 디테일의 인쇄/재구성 문제
AI 생성 로고는 흔히 tiny textures, shadows, highlights, gradients를 포함한다. 이것들을 벡터로 변환하려면 metallic effects, tiny patterns, stacked shadows, beveled edges, hyper-thin linework를 손으로 다시 만들어야 한다.

> *"re-creating an AI logo exactly can take more time than designing an original professional logo from scratch"* (Corwin Design)

### 2. 텍스트 렌더링
Recraft는 텍스트 렌더링을 강점으로 홍보하지만, 철자 오류는 여전히 모니터링 필수. 일반 AI 모델에서는 스크램블된 단어, 문자 추가/누락이 흔하다.

### 3. 컨셉 단계 산출물
AI 로고는 "90%-complete result"로 목표하고, 벡터/SVG로 내보낸 뒤 일러스트레이터에서 수동 다듬기를 전제한다. 이 스킬은 컨셉 생성까지 담당한다 — 최종 마스터(SVG)는 후처리 단계다.

## 정합 검증 체크리스트

받은 로고를 이 기준으로 점검한다. 하나라도 어긋나면 제약 강화 후 재생성.

- [ ] **스케일러빌리티**: 16px(파비콘)로 축소해도 형태가 살아있는가
- [ ] **단순성**: 불필요한 디테일/텍스처가 없는가
- [ ] **실루엣 내성**: 단색으로 변형해도 인식되는가
- [ ] **팔레트 정합**: 브랜드 팔레트를 벗어나는가
- [ ] **텍스트 정확**: 워드마크/레터마크 철자·레터링이 정확한가
- [ ] **Timeless**: 트렌드에 의존하지 않는가
- [ ] **적절성**: 업종/브랜드 정체성과 맞는가

## Recraft 품질 평가 5항목 (공식)

1. **Brand Alignment** — 회사 가치/사명 반영
2. **Design Principles** — 색 이론·타이포·구성의 효과적 사용
3. **Scalability** — 명함에서 빌보드까지 선명도
4. **Versatility** — 다양한 배경/색에 적응
5. **Uniqueness** — 커스터마이즈로 고유성

## 라이선스 주의 (상업 로고)

- **Free tier** — 생성 이미지가 Recraft 커뮤니티 갤러리에 포함됨 (상업 사용 제약)
- **Subscription (Basic/Advanced/Pro)** — full ownership + 상업 권리

상업 로고 작업 시 서브스크션이 필요함을 사용자에게 명시한다.

## 출처
- Jacob Cass (Just Creative) — 5 Principles of Effective Logo Design — https://www.justcreative.com/logo-design-principles/ (WebFetch 검증)
- Logogeek.uk — SMART Logo Design Principles — https://logogeek.uk/logo-design/smart-principles/ (WebFetch 검증)
- Corwin Design — Why AI-Generated Logos Don't Work — https://corwindesign.com/ai-generated-logos-dont-work/ (WebFetch 검증)
- Recraft — AI Logo Maker Guide — https://www.recraft.ai/blog/ai-logo-maker-guide (WebFetch 검증)
