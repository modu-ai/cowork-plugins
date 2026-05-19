---
title: "내보내기와 핸드오프"
weight: 50
description: "6가지 출력 형식(PDF·PPTX·HTML·Canva·ZIP·Claude Code 핸드오프 번들) 상세. 번들 내부 구조, 핸드오프 시점, 코드로 빌드하는 절차."
geekdocBreadcrumb: true
---
> 시안이 마음에 들면 어디로 내보낼지 결정해야 합니다. 발표용이면 PPTX·PDF, 마케팅 협업이면 Canva, 정적 호스팅이면 HTML, **프로덕션 코드로 갈 거면 Claude Code 핸드오프 번들**. 6가지 형식의 차이와 핸드오프 절차를 정리합니다.

## 출력 형식 6종 — 한눈에 비교

| 형식 | 결과물 | 편집 가능성 | 인터랙티브 보존 | 추천 시점 |
|---|---|---|---|---|
| **조직 URL** | 내부 링크 | Edit 권한 시 가능 | ✓ | 사내 리뷰·승인 회람 |
| **PDF** | 단일 PDF 파일 | 어려움 | ✗ | 외부 발송용 정적 산출물 |
| **PPTX** | PowerPoint 파일 | PowerPoint·Keynote에서 가능 | ✗ (간소화됨) | 발표 직전 최종 손질 |
| **표준 HTML** | 자립 HTML 폴더 | 코드 편집기에서 | ✓ | 단발성 랜딩·이벤트 사이트 |
| **Canva** | Canva 디자인 | Canva에서 풍부하게 | ✗ | 마케팅 팀 후속 편집 |
| **ZIP archive** | 모든 자산 압축 | — | ✓ | 백업·아카이브 |
| **Claude Code 핸드오프** | spec 번들 | Claude Code에서 코드로 | ✓ | 프로덕션 코드 빌드 |

## 형식별 상세

### 조직 URL

가장 빠른 공유 방법. 같은 조직 멤버에게 링크만 보내면 됩니다.

```
장점: 즉시 공유, 인터랙티브 보존, Edit 권한 시 협업
단점: 같은 조직 안에서만, 외부 발송 불가
```

[협업·공유 페이지](../collaboration/)에서 권한 모델 참고.

### PDF

외부 발송에 가장 안전한 형식.

```
장점: 어디서나 열림, 폰트 임베드, 정적 보존
단점: 인터랙티브 손실, 수정 어려움
권장 시나리오: 투자자에게 피치덱 발송, 클라이언트 시안 회람
```

내보내기 시 페이지 사이즈·여백을 미리 설정. A4·Letter·16:9 슬라이드 비율 등을 선택.

### PPTX

발표 직전 최종 손질이 필요할 때.

```
장점: PowerPoint·Keynote에서 편집 가능, 발표자 노트 포함
단점: 캔버스 HTML 버전보다 레이아웃이 간소화됨 — 배경 요소가 잘 안 옮겨짐
권장 시나리오: 임원 보고, 외부 미팅, 강의 자료
```

{{< hint type="warning" >}}
**PPTX는 HTML 캔버스 버전보다 간소화됩니다.** 특히 배경 그라데이션·복잡한 일러스트·인터랙티브 요소는 정적 이미지로 평탄화되거나 누락될 수 있습니다. 정밀한 발표 자료가 필요하면 PDF + HTML 두 형식을 함께 받아 비교하세요.
{{< /hint >}}

### 표준 HTML

자립 HTML 폴더로 내보내 정적 호스팅 또는 사내 인트라넷에 게시.

```
장점: 인터랙티브 보존, Vercel·Netlify·S3에 즉시 배포 가능
단점: SEO·라우팅 같은 프레임워크 기능 없음
권장 시나리오: 이벤트 랜딩, 캠페인 마이크로사이트, 사내 가이드
포함 파일: index.html · styles.css · scripts.js · assets/
```

### Canva

마케팅 팀이 후속 편집·공동 작업해야 할 때.

```
장점: Canva의 풍부한 편집 기능, 협업·버전 관리, 템플릿화 가능
단점: Claude Design의 코드 의도가 옅어짐, 자유로운 수정으로 일관성 깨질 위험
권장 시나리오: SNS 캠페인 비주얼, 이벤트 포스터, 멀티 채널 변형
```

Canva 전송 후에는 **편집·협업이 가능**합니다. Canva의 자체 공유 링크로 외부 공유도 가능합니다 (Canva 정책 적용).

### ZIP archive

전체 백업·아카이브 용도.

```
포함: 모든 디자인 파일, 토큰, 자산, README
용도: 핸드오프 전 백업, 분기별 아카이브, 클라이언트 인도
권장: 핸드오프나 큰 변경 전 한 번 받아 두기
```

### Claude Code 핸드오프 번들 — 핵심

프로덕션 코드로 빌드할 때 사용하는 **가장 강력한 형식**. 별도 섹션에서 상세히 다룹니다.

## Claude Code 핸드오프 번들 — 상세

Claude Design이 시안을 만든 같은 시스템(Anthropic)이 핸드오프 번들도 작성합니다. 그래서 **Claude Code가 픽셀에서 의도를 추론할 필요가 없습니다** — 이미 구조화된 spec을 받습니다.

### 번들에 포함되는 것

```
handoff-bundle/
├── README.md             ← Claude Code가 가장 먼저 읽는 파일
├── design-tokens.json    ← 캔버스에서 실제로 사용한 토큰
├── components.json       ← 컴포넌트 트리 (machine-readable spec)
├── layout-hierarchy.json ← 레이아웃·간격·반응형 정보
├── chat-history.md       ← 디자인 과정의 결정 맥락
└── assets/               ← 이미지·SVG·폰트 등 참조 자산
```

### 번들이 일반 Figma 핸드오프와 다른 점

| 항목 | Figma → 개발자 | Claude Design → Claude Code |
|---|---|---|
| 형식 | 픽셀·디자인 도구 표현 | 구조화된 spec (JSON) |
| 의도 전달 | 디자이너가 따로 설명 필요 | 채팅 히스토리에 자동 보존 |
| 컴포넌트 매칭 | 개발자가 수동 매핑 | 기존 코드베이스 컴포넌트 자동 인식 |
| 토큰 | 디자인 도구 토큰 → 코드 토큰 변환 필요 | 처음부터 코드 토큰 사용 |
| 생산자·소비자 | 다른 시스템(Figma · IDE) | 같은 회사 모델(Anthropic) |

## 핸드오프 절차 — 실제 단계

### 1. 핸드오프 직전 점검

```
□ 시안이 발표 수준 완성도인가 (5라운드 한계 안에서)
□ 의도된 사용자 플로우가 모두 디자인되어 있는가
□ 엣지 상태(empty · error · loading)가 디자인되어 있는가
□ 반응형 변형이 필요한 화면은 디자인되어 있는가
□ 컴포넌트 이름이 코드베이스와 일치하는가
□ 백업 ZIP을 한 번 받아 두었는가
```

### 2. Export → Hand off to Claude Code

캔버스 우상단 **Export** 버튼 → 옵션 중 선택:

| 옵션 | 사용 시점 |
|---|---|
| **Hand off to Claude Code** | 로컬 터미널에서 Claude Code를 쓰는 경우 |
| **Hand off to Claude Code Web** | 브라우저에서 Claude Code Web을 쓰는 경우 |

### 3. 받은 프롬프트를 Claude Code에 붙여넣기

Export 후 Claude Design이 **준비된 프롬프트**를 보여줍니다. 그대로 복사해 Claude Code에 붙여넣습니다.

**전형적인 프롬프트 예시**:

```
이 디자인 핸드오프 번들을 받아서 코드로 구현해 줘.
번들 URL: [자동 생성 URL]
참고:
- README.md 먼저 읽고 의도와 컴포넌트 매핑을 파악
- 기존 코드베이스의 React 컴포넌트 라이브러리를 활용
- design-tokens.json의 토큰을 그대로 사용
- chat-history.md에 디자인 결정의 맥락이 있음
구현 후 로컬에서 미리보기 가능하게 설정.
```

Claude Code Web을 쓰면 위 절차가 한 번의 클릭으로 자동화됩니다.

### 4. Claude Code의 작업

```mermaid
sequenceDiagram
    autonumber
    participant U as 사용자
    participant CC as Claude Code
    participant FS as 로컬 코드베이스
    participant LIB as UI 컴포넌트 라이브러리

    U->>CC: 핸드오프 번들 URL + 지시
    CC->>CC: README.md · design-tokens.json · components.json 읽음
    CC->>FS: 기존 코드베이스 스캔
    CC->>LIB: 기존 컴포넌트 라이브러리 식별 (Button·Card·Modal 등)
    CC->>CC: 디자인 의도 → 기존 컴포넌트 매핑
    CC->>FS: 페이지·컴포넌트·스타일 생성
    CC-->>U: 로컬 미리보기 명령
    U->>FS: npm run dev 등으로 확인
    U->>CC: 수정 요청 (자연어)
```

### 5. 핸드오프 이후의 원칙

| 원칙 | 이유 |
|---|---|
| **핸드오프 시점을 명확한 체크포인트로** | 이후 디자인 수정은 코드와 어긋남 |
| **수정은 가급적 코드에서** | Claude Code가 같은 디자인 시스템을 알고 있어 일관성 유지 |
| **큰 디자인 변경이 필요하면 새 핸드오프** | 이전 코드를 일부 유지하면서 새 시안 가져오기 |
| **스크린샷 피드백 루프** | 코드 결과를 캡처해 Claude Design에 다시 입력해 비교·수정 |

## 핸드오프 실패 — 자주 겪는 문제

| 증상 | 원인 | 복구 |
|---|---|---|
| Claude Code가 컴포넌트를 못 찾음 | 코드베이스 연결 없이 디자인했음 | 디자인 시스템에 GitHub repo 추가 → 다시 핸드오프 |
| 컴포넌트 이름이 어긋남 | 디자인에서 임의 이름 사용 | 코드 컴포넌트 이름과 일치시킨 후 다시 핸드오프 |
| 토큰이 어긋남 | 디자인 시스템에 등록된 토큰과 캔버스에서 쓴 값이 다름 | Remix로 시스템 정리 후 다시 디자인 |
| 인터랙티브가 단순화됨 | 디자인 단계의 복잡한 애니메이션이 코드로 안 옮겨감 | Claude Code에 추가 지시: "이 버튼에 hover 시 0.2s 페이드" |
| ZIP 백업 없이 핸드오프 후 실패 | 되돌리기 어려움 | 다음부터는 핸드오프 직전 ZIP 백업 필수 |

## 양방향(디자인 ↔ 코드) — 현재 제약

핸드오프는 **디자인 → 코드** 한 방향이 강합니다. 반대 방향(코드 → 디자인 동기화)은 현재 제한적입니다.

**대안 패턴**:

1. **스크린샷 피드백**: 코드에서 빌드한 결과를 캡처해 Claude Design에 다시 입력
2. **부분 영역 재디자인**: 특정 페이지·섹션만 새 프로젝트로 다시 디자인 → 새 번들로 부분 핸드오프
3. **디자인을 원본으로 유지**: 코드 변경이 클 때마다 디자인을 먼저 수정하고 다시 핸드오프

## 한국 환경 메모

| 영역 | 메모 |
|---|---|
| 한글 폰트 | Pretendard·Noto Sans KR 등이 코드베이스에 있으면 자동 인식 |
| PPTX 한글 | 한글 폰트 임베드 — 발표 PC에 폰트 없을 때 깨짐 방지 위해 PPTX에 폰트 임베드 |
| Canva 한글 | Canva에서 한글 폰트 옵션 제한적 — 폰트 통일성을 위해 PDF 권장 |
| Pretty Print URL | 표준 HTML 호스팅 시 한글 URL은 인코딩 — 별도 alias 권장 |

## 다음 단계

- **다음 페이지**: [역할별 사용 사례](../use-cases/) — 핸드오프가 실제 워크플로우에서 어떻게 쓰이는지
- 참고: [디자인 시스템](../design-system/) — 핸드오프 품질은 시스템 셋업이 좌우
- 깊이: [베스트 프랙티스](../best-practices/) — 핸드오프 직전 체크리스트

---

### Sources

- [Using Claude Design for prototypes and UX (Anthropic Tutorial)](https://claude.com/resources/tutorials/using-claude-design-for-prototypes-and-ux)
- [Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs)
- [Claude Design to Claude Code: AI Design Handoff (ClaudeFast)](https://claudefa.st/blog/guide/mechanics/claude-design-handoff)
- [Claude Design handoff example (GitHub)](https://github.com/az9713/claude-design-handoff)
- [Claude Design Starter Guide (Claudia + AI)](https://claudiaplusai.substack.com/p/claude-design-starter-guide-and-examples)
