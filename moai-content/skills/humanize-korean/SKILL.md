---
name: humanize-korean
description: |
  AI(ChatGPT·Claude·Gemini 등)가 쓴 한국어 텍스트의 "AI 티"를 정밀하게 제거해 사람이 쓴 글처럼 윤문하는 한국어 특화 스킬입니다. 번역투(~를 통해/~에 있어서/이중 피동), 영어 인용 과다, 기계적 병렬(첫째·둘째·셋째), AI 특유 관용구(결론적으로/시사하는 바가 크다/혁신적인), 피동태 남용, 문두 접속사 남발, 형식명사 과다, 이모지·불릿·볼드 남용 등 10대 카테고리 × 40+ 패턴을 S1/S2/S3 심각도로 탐지·윤문하고, 의미는 한 글자도 건드리지 않습니다(고유명사·수치·날짜·인용 100% 보존, 변경률 30% 초과 시 경고·50% 초과 시 강제 중단).

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "AI 티 없애줘", "GPT 문체 제거해줘", "ChatGPT 티 제거"
  - "사람이 쓴 것처럼 윤문해줘", "AI 같은 글 자연스럽게"
  - "한글 AI 윤문", "AI 글 사람처럼", "AI 글 티 안 나게"
  - "번역투 제거", "영어 인용 많은 글 윤문"
  - "휴머나이저", "humanize Korean", "AI detector bypass 한글"
  - 후속 작업: "특정 카테고리만 다시", "이 문단만", "2차 윤문", "강도 조정", "장르 바꿔서"

  적용 대상 — 모든 한국어 텍스트 산출물(블로그·뉴스레터·카피·사업계획서·제안서·보고서·이메일·랜딩 카피·칼럼·리포트). ai-slop-reviewer가 1차 일반 후처리를 마친 뒤 2차 한국어 정밀 윤문으로 호출하는 것을 권장합니다.

  적용 제외 — 단순 맞춤법·오탈자 교정(직접 처리), 번역(번역 스킬), 내용 추가·삭제 동반 재작성(별도 집필 스킬), 코드·JSON·CSV·차트·표.

  Adapted from epoko77-ai/im-not-ai (MIT, ⭐937) v1.6.1 — humanize-monolith Fast 모드 단일 스킬 변형.
user-invocable: true
version: 2.3.0
---

# Humanize Korean — 한국어 AI 티 제거 (Fast 모드)

## 개요

이 스킬은 한국어 텍스트에서 AI가 쓴 흔적을 **수술적으로** 제거합니다. **내용은 한 글자도 건드리지 않고** 문체·리듬·표현만 자연스러운 한국어로 되돌립니다. 영어권 humanizer(QuillBot·Hix·Undetectable AI)가 약한 한국어 고유 패턴 — 번역투, 영어 인용 과다, 결말 공식, hedging, 형식명사 — 을 정량 메트릭과 SSOT 분류 체계로 처리합니다.

## 4대 철칙 (위반 시 즉시 롤백)

1. **의미 불변** — 사실·주장·수치·고유명사·직접 인용은 100% 원문 보존
2. **근거 기반** — 탐지된 span에만 수술적 수정. 탐지 없는 구간은 건드리지 않음
3. **장르 유지** — 칼럼을 문학으로, 리포트를 에세이로 옮기지 않음
4. **과윤문 금지** — 변경률 30% 초과 시 경고, 50% 초과 시 강제 중단

## Phase 0: 컨텍스트 확인

작업 시작 시 가장 먼저 다음 한 줄을 출력합니다.

```
humanize-korean v2.1 — fast 모드 / run_id: {YYYY-MM-DD-NNN}
```

### run_id 결정

- 모든 경로는 **cwd 기준**. `_workspace/{YYYY-MM-DD-NNN}/`에 산출물 누적
- 기존 시퀀스 확인은 **`Glob` 도구**로:
  - `Glob(pattern="_workspace/YYYY-MM-DD-*/01_input.txt")` → 결과에서 폴더명 추출 후 NNN 최댓값 + 1
  - 당일 폴더가 없으면 NNN = 001
  - 디렉토리 자체는 Glob으로 매칭 안 됨 — 반드시 `01_input.txt` 표지 파일을 매칭
- 8,000자 초과 입력은 처리는 가능하지만 정밀 검증이 필요할 수 있음 → summary.md에 "정밀 모드(strict-pipeline-spec) 권장" 한 줄 표기

### 옵션 (인자 끝에 자연어로)

- `장르: 칼럼|리포트|블로그|공적` — 장르 명시(생략 시 첫 300자로 자동 추정)
- `강도: 보수|기본|적극` — 윤문 강도(기본값: 기본)
- `최소심각도: S1|S2|S3` — 탐지 임계값(기본값: S2)

## Phase 1: 입력 저장

1. cwd 기준 `_workspace/{run_id}/` 디렉토리 생성
2. 입력 텍스트를 **`01_input.txt`**에 그대로 저장 (한 글자도 변형하지 않음)
3. 첫 300자로 장르 자동 추정 (사용자 명시 시 우선)
   - 칼럼: 1인칭 의견·논평·결말 공식
   - 리포트: 객관적 서술·수치·인용
   - 블로그: 캐주얼·친근체·이모지 허용
   - 공적: 격식체·공문체

## Phase 2: 사전 메트릭 측정

정량 베이스라인을 먼저 잡습니다. `references/metrics.py`를 호출:

```bash
python3 moai-content/skills/humanize-korean/references/metrics.py \
  --input "_workspace/{run_id}/01_input.txt" \
  --genre {칼럼|리포트|블로그|공적} \
  --output "_workspace/{run_id}/00_metrics.json"
```

산출물 `00_metrics.json`에는 다음이 포함됩니다(원본 metrics.py v1.6 명세):
- 문장 수, 평균 문장 길이, 길이 표준편차(E-1 균일성 신호)
- 연결어미+쉼표 빈도(C-11 KatFish 시그널)
- 한자어 명사화 -성/-적/-화 밀도(F-4)
- 종결어미 분포(I 카테고리)
- 문두 접속사 빈도(H-1)

표준 라이브러리만 사용하므로 별도 의존 설치는 없습니다(Python 3.13+ 권장).

## Phase 3: 인라인 탐지·윤문·자체검증

**핵심 단계**. 이 단계에서 다음을 한 번에 수행합니다.

### 3-1. 룰북 로드

다음 두 파일을 메모리로 로드:
- `references/quick-rules.md` — S1·S2 핵심 패턴 + 자체검증 6항(슬림 룰북)
- `references/ai-tell-taxonomy.md` — 10대 카테고리 × 40+ 서브 패턴 SSOT(필요 시 참조)

`00_metrics.json`의 정량 신호를 우선순위로 활용합니다(예: stdev<8이면 E-1 우선, -성/-적/-화 12+이면 F-4 우선).

### 3-2. Do-NOT 리스트 (탐지·윤문 모두 제외)

- 고유명사·제품명·모델명·기관명
- 수치·날짜·단위
- 큰따옴표 안 직접 인용
- 법률 조문, 수학·화학·통계 표기
- 영어 약어(LLM·GPU·MCP·API 등 업계 표준)

### 3-3. 카테고리별 처방 적용 우선순위

**S1 (결정적 — 무조건 제거)**:
- A-1/A-2/A-3 번역투(~를 통해/~에 대해/~에 있어서)
- A-7/A-8 가지고 있다 / 이중 피동
- C-5 이모지 남발(칼럼·리포트 한정)
- C-10 콜론 부제 헤딩 반복
- C-11 연결어미 뒤 쉼표
- D-1~D-6 결산 피벗·시사하는 바·본질적으로·hype 어휘·의인화 추상 주어·결말 공식
- H-1/H-3 문두 접속사 5+회 / 메타 진입 3+회
- I-1 ~인 것이다/한 것이다 결말
- J-2 따옴표 강조 5+회

**S2 (강함 — 1~2회 허용, 3+ 시 제거)**:
- A-4/A-5/A-6/A-9/A-10/A-11/A-15
- B-1/B-2 영어 인용 과다
- C-7/C-8/C-9 구조 패턴
- D-7 변환 공식 X에서 Y로
- E-1 리듬 균일성
- F-4/F-5 한자어 -성/-적/-화 밀도
- G-1/G-2/G-3 hedging
- H-4 즉 남발
- I-2/I-3/I-4 형식명사
- J-1/J-3 헤딩 강조 / 불릿 리스트

자세한 처방 레시피는 `references/rewriting-playbook.md` 참조.

### 3-4. 윤문 실행 (Edit 도구)

탐지된 span별로 Edit 도구로 **수술적** 치환. 탐지되지 않은 구간은 절대 수정하지 않습니다.

- 격식체 입력 → 격식체 출력 (register 보존)
- 평어체 입력 → 평어체 출력
- 변경 누적분이 30% 초과 시 경고 메시지를 summary 후보에 기록, 50% 초과 시 즉시 중단·전체 롤백

### 3-5. 자체검증 6항 점검 (윤문 직후 5초 내)

윤문 직후 다음을 자가 점검합니다. 한 항목이라도 위반이면 해당 edit 롤백:

1. **고유명사·수치·날짜·인용 100% 보존** — 원문 대비 한 글자도 다르지 않은가
2. **변경률** — 30% 이하인가
3. **장르 이탈 없음** — 칼럼이 에세이·문학으로 변하지 않았는가
4. **register 보존** — 원문 격식체면 결과도 격식체
5. **잔존 S1 패턴 0건** — D-1~D-7, A-8, C-5, C-10, C-11, H-1, I-1, J-2가 남아있지 않은가
6. **인공 표현 자제** — 원문에 없던 비유·수사·문학적 표현을 임의 추가하지 않았는가

위반 시: edit 롤백 → 다시 윤문 → 재점검. **자체 루프 최대 1회.** 여전히 미해결이면 결과를 출력하되 `summary.md`에 "자가검증 미통과 항목 N건"을 표기합니다.

## Phase 4: 사후 메트릭 + 산출물 작성

### 4-1. 사후 메트릭

```bash
python3 moai-content/skills/humanize-korean/references/metrics.py \
  --input "_workspace/{run_id}/final.md" \
  --genre {장르} \
  --output "_workspace/{run_id}/06_metrics_after.json"
```

before/after 비교로 카테고리별 개선율(%)을 계산합니다.

### 4-2. final.md 작성

`_workspace/{run_id}/final.md`에 윤문본 + HTML 주석 블록(메트릭·탐지 before/after·자체검증 6항·등급·주요 변경 하이라이트)을 작성합니다. HTML 주석이라 마크다운 뷰어·웹 게시·복사 시 본문에만 노출됩니다.

```markdown
{윤문본 본문}

<!-- HUMANIZE-SUMMARY
모드: fast / run_id: {run_id}
변경률: X%
등급: A|B|C|D
자체검증: N/6 통과
카테고리 탐지 (before → after):
  A 번역투: 12 → 1
  D AI 관용구: 5 → 0
  ...
-->
```

### 4-3. summary.md 작성

`_workspace/{run_id}/summary.md`에 메트릭 표·자체검증 결과·등급·하이라이트 요약을 정리합니다.

## Phase 5: 등급 판정

| 등급 | 조건 |
|---|---|
| **A** | S1 잔존 0, S2 잔존 ≤2, 변경률 10~25%, 자체검증 6/6 |
| **B** | S1 잔존 0, S2 잔존 ≤4, 자체검증 5/6 이상 |
| **C** | S1 잔존 1~2 또는 자체검증 ≤4 — 사용자에게 정밀 검증 권고 |
| **D** | S1 잔존 3+ 또는 변경률 50% 초과 — 작업 중단 권고 |

## Phase 6: 사용자에게 결과 반환

다음 4개를 사용자에게 전달:

1. **한 줄 상태**: `완료. 변경률 X% / 등급 Y / 자체검증 N/6 통과`
2. **윤문본 본문**: 마크다운 블록 형태로
3. **summary.md 핵심 표**: 메트릭 + 카테고리 탐지 + 자체검증
4. **등급 B 이하 시 안내**: "더 정밀한 검증이 필요하면 `references/strict-pipeline-spec.md`의 5인 파이프라인 명세를 참조해 별도 워크플로로 실행하시기 바랍니다."

## 부분 재실행 / 후속 명령

| 사용자 신호 | 처리 |
|---|---|
| "특정 카테고리만 다시" | 해당 카테고리 finding만 Phase 3 재실행, 기존 run_id 재사용 |
| "이 문단만" | 해당 문단만 입력으로 새 run_id 생성 |
| "2차 윤문" | 기존 run_id의 `final.md`를 새 입력으로 Phase 1부터 재실행 |
| "윤문 강도 조정" | `최소심각도` 옵션 변경 후 Phase 2부터 재실행 |
| "장르 바꿔서" | `genre_hint` 변경 후 Phase 2부터 재실행 |

## ai-slop-reviewer와의 관계

이 스킬은 `moai-core:ai-slop-reviewer`의 **2차 한국어 정밀 윤문** 단계로 설계되었습니다. 권장 체인:

```
한국어 텍스트 산출물(블로그·뉴스레터·카피 등)
  ↓
moai-core:ai-slop-reviewer  ── 1차 일반 AI 슬롭 후처리(영어 표현 정리, 일반 패턴)
  ↓
moai-content:humanize-korean ── 2차 한국어 정밀 윤문(40+ 패턴 SSOT, 등급)
  ↓
최종 산출물
```

ai-slop-reviewer만으로 충분한 경우(영어 비중 높은 텍스트, 캐주얼 블로그)는 humanize-korean을 생략해도 됩니다.

## 주의 사항

- **의미 불변이 최상위 불문율** — 위반 즉시 롤백
- **수치·고유명사·직접 인용은 탐지·윤문 대상 아님** — Do-NOT 리스트 엄수
- **장르 이탈 금지** — 칼럼이 에세이로, 에세이가 문학으로 옮겨가지 않음
- **register 보존** — AI 티는 문법·수사이지 격식 자체가 아님
- **변경률 30% 초과 → 경고, 50% 초과 → 강제 중단·전체 롤백**
- **자동 로드 금지** — 프로젝트 CLAUDE.md 등 다른 파일을 자동 파싱해 옵션 추론하지 않음

## 참고 자료

- 슬림 룰북(이 스킬 핵심): [`references/quick-rules.md`](references/quick-rules.md) — S1·S2 핵심 패턴 + 자체검증 체크리스트
- 분류 체계 SSOT: [`references/ai-tell-taxonomy.md`](references/ai-tell-taxonomy.md) — 10대분류 × 40+ 패턴 전수
- 윤문 처방: [`references/rewriting-playbook.md`](references/rewriting-playbook.md) — 카테고리별 치환 레시피·장르별 허용 표
- 정량 메트릭: [`references/metrics.py`](references/metrics.py) — Python 3.13+ 표준 라이브러리만, CLI 호출
- 베이스라인: [`references/baseline.json`](references/baseline.json) — 카테고리별 임계값
- 정밀 모드 명세(향후 확장용): [`references/strict-pipeline-spec.md`](references/strict-pipeline-spec.md) — 7인 에이전트 파이프라인(현재 스킬에서는 미사용, 별도 워크플로로 실행 시 참조)
- 웹 서비스 확장(옵션): [`references/web-service-spec.md`](references/web-service-spec.md) — Next.js + Vercel 확장 시 참조

---

**Adapted from**: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) v1.6.1 (MIT License, ⭐937).
원본은 7인 에이전트 + Fast/Strict 듀얼 모드 오케스트레이터 스킬입니다. 이 cowork 변형은 Fast 모드를 단일 스킬로 압축하고, Strict 5인 파이프라인 명세는 `references/strict-pipeline-spec.md`에 보존했습니다. 분류 체계(taxonomy)·룰북(quick-rules·playbook)·메트릭(metrics.py·baseline.json)·테스트(test_metrics.py)는 모두 원본 그대로 가져왔습니다.
