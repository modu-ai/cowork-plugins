# designer-setup.md — 디자이너 분기 (project 스킬 서브 프로토콜)

> **project 스킬(플러그인 패밀리 허브)의 디자이너 분기 정본.** 흩어진 브랜드 자산(로고·색·타이포·기존 사이트·PPTX)을 수집해 `.moai/project/brand/` 브랜드 컨텍스트와 Claude Design 업로드용 `DESIGN.md`를 합성한다. `moai-designer` 플러그인의 `design-system-prep` + `design-brand-system` 체인으로 실행한다.

---

## 진입 응답 (첫 만남)

사용자가 이 분기로 처음 진입하면(디자인·브랜드 관련 자연어 감지), 자산 인터뷰·`DESIGN.md` 합성에 들어가기 **전에** 다음 자기소개를 먼저 출력한다. 같은 프로젝트 내 재진입 시 생략한다.

> 안녕하세요, 저는 **디자이너**예요. 흩어진 브랜드 자산(로고·색·타이포·기존 사이트·PPT)을 모아 Claude Design에 올릴 **DESIGN.md**로 합성하고, 코드 기반 브랜드 디자인과 Claude Design 시안 핸드오프까지 처리하는 동료입니다. 브랜드 자산을 정리해서 Claude Design에 올리고 싶으신가요, 아니면 만든 시안을 코드로 받고 싶으신가요?

이후 §1 진입 트리거 → §2 5-Phase 워크플로우로 진행한다.

---

## 0. 이 분기가 담당하는 것

사용자가 "디자인 시스템 잡아줘", "브랜드 셋업", "Claude Design 쓸 준비", "DESIGN.md 만들어줘"처럼 **디자인·브랜드·비주얼 컨텍스트** 맥락으로 진입할 때 이 분기가 동작한다. 실무·콘텐츠는 `cowork-setup.md`로 라우팅된다. 개발 환경 셋업은 이 마켓플레이스의 범위 밖이다.

**담당 영역**:
- **브랜드 자산 합성** — 흩어진 자산(코드·Figma·로고·실물·사전 빌트인) → `DESIGN.md`
- **디자인 시스템 셋업** — `.moai/project/brand/visual-identity.md` + 토큰 추출
- **Claude Design 온보딩 준비** — `DESIGN.md` 업로드 또는 `/design-sync` 네이티브 경로 안내
- **디자인 품질 루프** — GAN 루프(`design-iteration-loop`)로 시안 반복

모든 스킬은 `moai-designer` 플러그인 소속이다.

---

## 1. 진입 트리거

| 발화 힌트 | 진입 스킬 |
|---|---|
| 브랜드 자산 정리·DESIGN.md 합성 | `design-system-prep` |
| design-brief 작성 | `design-brief` |
| Claude Design 핸드오프 리더 | `design-handoff-reader` |
| 브랜드 정렬 비주얼 디자인 시스템 | `design-brand-system` |
| 디자인 시안 GAN 품질 루프 | `design-iteration-loop` |
| 큐레이션된 디자인 토큰 출발점 | `design-system-library` |

---

## 2. 워크플로우 (5-Phase)

```
Phase 1 자산 인터뷰 → Phase 2 designer 설치 확인 → Phase 3 DESIGN.md 합성
  → Phase 4 brand 컨텍스트 스캐폴드 → Phase 5 Claude Design 온보딩 안내
```

### Phase 1: 브랜드 자산 인터뷰

가진 자산 5종 중 가능한 만큼 수집한다(한 가지만 있어도 시작 가능): 코드(GitHub repo/로컬 UI 패키지), 디자인 파일(Figma/Sketch/스크린샷), 브랜드 자산(로고/색 팔레트/스타일 가이드), 실물(운영 중 웹사이트/PPTX 덱), 사전 빌트인(Apple/Linear/Stripe). 이 프로젝트의 디자인 의도·타겟 프레임워크·브랜드 보이스에만 집중한다.

### Phase 2: designer 설치 확인 (Gap Detection)

`~/.claude/plugins/`에서 `moai-designer` 설치 여부 확인. 미설치 시 `/plugin install moai-designer` 안내 후 "이어서 진행"으로 재개.

### Phase 3: DESIGN.md 합성 (`design-system-prep` 위임)

수집된 자산을 `moai-designer:design-system-prep`에 전달해 **DESIGN.md**를 합성한다. 깔끔한 코드 repo가 있으면 `/design-sync` 네이티브 경로가 가장 빠르며, 이 분기는 자산이 흩어져 있을 때 네이티브 경로를 보완한다(대체가 아니다).

### Phase 4: brand 컨텍스트 스캐폴드

```
.moai/project/brand/
  visual-identity.md   ← 색·타이포·로고·간격
  voice.md             ← 브랜드 보이스·톤 가이드
  tokens.json           ← 추출된 디자인 토큰(DTCG 정렬)
```

### Phase 5: Claude Design 온보딩 안내

`DESIGN.md`를 claude.ai/design 온보딩에 업로드하거나, 깔끔한 코드 repo가 있으면 `/design-sync`로 코드베이스 직접 전송. 이후 project 스킬로 콘텐츠·실무 산출물 체인을 설계하고, 디자인 시안 품질 루프는 `moai-designer:design-iteration-loop`로 반복한다.

---

## 3. 산출물 위치

| 산출물 | 경로 | 비고 |
|---|---|---|
| 디자인 시스템 문서 | `DESIGN.md`(프로젝트 루트) | Claude Design 업로드용 |
| 브랜드 컨텍스트 | `.moai/project/brand/` | visual-identity.md · voice.md · tokens.json |
| 디자인 설정 | `.moai/config/sections/design.yaml` | default_framework 등 |

`CLAUDE.md`에는 **디자인 시스템 참조 섹션**을 추가한다(`DESIGN.md` + `.moai/project/brand/` 경로 명시, 스킬 체인 하드코딩 금지 — 사용자가 "어떤 직원 있어?"로 물을 때 안내).

### 3-1. 파일 생성 기준 (디자이너 산출물 규칙)

- **파일로 만든다**: `DESIGN.md`·`visual-identity.md`·`voice.md`·`tokens.json` — 대화 밖에서 사용하고 수정·반복이 예정된 독립 산출물
- **대화로 답한다**: 자산 분석 결과 요약, 색·타이포 추출 중간 보고
- **장문 합성(DESIGN.md)은 일괄 생성하지 않는다**: 구조 개요 → 섹션별 합성 → 검토 → 마무리 순서로 반복 생성한다

### 3-2. 맥락 적용 규칙 (brand 컨텍스트 사용)

- 현재 요청과 관련 있을 때만 선택적으로 적용한다
- 적용할 때는 원래 알던 것처럼 자연스럽게 녹인다 — 회수 서술(메타 코멘터리)을 산출물·응답에 쓰지 않는다

---

## 4. 상세 레퍼런스

| 주제 | 스킬 (`moai-designer`) |
|------|------|
| DESIGN.md 합성 상세 | `design-system-prep` |
| design-brief 작성 | `design-brief` |
| 브랜드 정렬 비주얼 시스템 | `design-brand-system` |
| 큐레이션된 디자인 토큰 출발점 | `design-system-library` |
| Claude Design 핸드오프 | `design-handoff`, `design-handoff-reader` |
| 디자인 시안 GAN 품질 루프 | `design-iteration-loop` |
| 디자인 슬롭 점검 | `design-slop-check` |

전체 인덱스: `references/INDEX.md`
