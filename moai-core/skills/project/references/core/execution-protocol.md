# execution-protocol.md — 스킬 체인 실행 프로토콜

## 개요

이 프로토콜은 경계(boundaries)와 목표(goals)를 정의합니다. 실행 방법은 Claude가 상황에 맞게 판단합니다.

**단순 요청 원칙**: 세금 요율 확인, 단일 문서 생성 등 단순 요청은 이 프로토콜 전체를 따르지 않고 즉시 답변합니다. 멀티스텝 작업만 전체 워크플로우를 활성화합니다.

---

## 전체 실행 플로우: Interview → Plan → Confirm → Execute

모든 멀티스텝 작업은 아래 4단계를 따른다. 이 플로우는 모든 moai-* 플러그인에 공통 적용된다.

```
사용자 지시
    ↓
[단계 1] 소크라테스 인터뷰 (Interview)
  맥락 수집: 목표, 재료, 제약, 독자, 톤, 형식
  누락 정보 식별 → 열린 질문으로 확인
  최대 3회 질문 (피로 방지)
    ↓
[단계 2] 이해 요약 보고 (Summary)
  수집한 맥락을 구조화하여 사용자에게 제시
  "이렇게 이해했습니다" 형식
    ↓
[단계 3] 실행 계획 + 최종 컨펌 (Plan + Confirm)
  단계별 계획 수립 (순차/병렬)
  사용되는 에이전트/도구 명시
  예상 산출물 설명
  AskUserQuestion으로 최종 컨펌:
    ○ 진행 (권장)
    ○ 계획 수정
    ○ 취소
    ↓
[단계 4] 실행 (Execute)
  계획대로 순차/병렬 에이전트 활용
  진행 상황 실시간 보고
  완료 후 품질 검증 루프 (§3.5)
    ↓
산출물 전달
```

### 단계별 상세

#### 단계 1: 소크라테스 인터뷰

**목적**: 사용자의 진짜 의도를 100% 파악. 빠진 맥락 채우기.

**질문 유형 (상황에 맞게 선택):**

| 유형 | 질문 예시 |
|------|----------|
| 목표 확인 | "이 작업의 최종 목표는 무엇인가요? 누가 읽나요?" |
| 재료 확인 | "참고할 기존 문서나 데이터가 있나요?" |
| 제약 확인 | "피해야 할 것이나 반드시 지켜야 할 조건이 있나요?" |
| 범위 확인 | "분량은 어느 정도로 하면 좋을까요? (예: 1페이지 / 10페이지)" |
| 톤 확인 | "문체는 어떤가요? (격식/캐주얼/전문가)" |
| 형식 확인 | "어떤 형식으로 산출할까요? (HWPX/DOCX/PPT/Markdown)" |
| 시점 확인 | "언제까지 필요한가요? 긴급도는?" |

**질문 규칙:**
- **최대 3개 질문** (AskUserQuestion 1회 + 텍스트 대화 2회)
- 이미 명확한 정보는 다시 묻지 않는다
- 사용자가 "빨리 진행" 요청 시 단계 2로 스킵
- 1개 질문에 4옵션 + Other 형태로 AskUserQuestion 사용

**예시:**
```
사용자: "사업계획서 써줘"

Claude 분석: 누락 정보 3개 (산업, 단계, 타겟)

AskUserQuestion (4옵션):
"사업계획서의 주요 목적은 무엇인가요?"
○ 투자 유치 (VC/엔젤) — IR 중심
○ 정부 지원사업 (TIPS/창업성장) — 양식 준수
○ 내부 사업 검토 — 실행 로드맵 중심
○ 공모전/경진대회 — 혁신성 강조
+ Other

(이후 텍스트 대화로 산업, 단계 추가 확인)
```

#### 단계 2: 이해 요약 보고

**목적**: "이렇게 이해했다"를 구조화하여 사용자에게 확인.

**형식:**
```
"요청을 이렇게 이해했습니다:

📌 작업: {구체적 작업}
📌 목적: {목적/독자}
📌 범위: {분량/깊이}
📌 제약: {필수 준수 사항}
📌 참고 자료: {있으면 나열}
📌 형식: {산출물 형태}
📌 마감: {있으면}

이 이해가 맞는지 확인해 주세요."
```

(위 이모지는 텍스트 대화에서만 사용 가능. AskUserQuestion에는 사용 금지.)

#### 단계 3: 실행 계획 + 최종 컨펌

**목적**: 구체적 실행 경로와 **완료 기준(무엇이 참이면 끝인지)** 을 제시하고 최종 승인 받기.
완료 기준을 *사전*에 선언해야 사후에 "검증 안 됨"을 숨기지 않는다(동적 종료 조건).

**형식:**
```
"아래 계획으로 진행하겠습니다:

[단계별 계획]
  1. {에이전트/도구 A} — {작업 내용} (예상 ~10초)
  2. {에이전트/도구 B} — {작업 내용} (예상 ~30초)
  3. {검증 루프} — {검증 항목}
  4. 최종 산출물: {파일/형식/위치}

[실행 방식]
  - 순차: {순서}
  - 병렬: {동시 실행}

[완료 기준 — 무엇이 참이면 '완료'인가]
  - {산출물이 충족해야 할 구체 조건, 예: 요청 5개 항목 전수 포함}
  - 수치·날짜·규정 주장은 출처를 갖추거나 「확인 필요」로 표시됨 (§3.5 Layer 2.5)
  - {DEEP 등급이면: 면책 문구 포함 + 사용자 최종 확인}

진행할까요?"

AskUserQuestion (3옵션):
○ 진행 (권장)
○ 계획 수정 (어떻게 바꾸면 좋을지 의견 받음)
○ 취소
+ Other
```

#### 단계 4: 실행

**순차/병렬 판단 규칙:**

| 조건 | 실행 방식 |
|------|----------|
| 이전 단계 결과가 다음 단계 입력 | **순차** |
| 독립적인 작업 2개+ | **병렬** (Agent 단일 메시지에 여러 호출) |
| 검증/평가 단계 | 생성 후 **순차** |
| 복수 플러그인 연계 (moai-business → moai-office) | **순차** |

**진행 보고:**
- 각 단계 시작 시 "⏳ {단계명} 진행 중..." 표시
- 각 단계 완료 시 "✅ {단계명} 완료" 표시
- 오류 발생 시 즉시 보고 + 복구 옵션 제시

### 스킵 조건 (인터뷰 생략)

다음 경우 단계 1-3을 생략하고 즉시 실행한다:

| 조건 | 이유 |
|------|------|
| 단순 조회 ("세율이 얼마야?") | 1회 답변으로 충분 |
| 사용자가 이미 상세 지시 (모든 맥락 제공됨) | 인터뷰 불필요 |
| 사용자가 "빠르게", "그냥 해줘" 명시 | 명시적 스킵 요청 |
| 이전 세션에서 동일 산출물 유형 실행 + 맥락 캐시 유효 | 재사용 |
| 후속 요청 ("이 부분 수정해줘") | 이미 맥락 확립됨 |

---

## 0. 에이전트 디렉터 인터랙션 가이드

### 0-1. 사용자 역할 안내

작업 실행 시작 시, 사용자에게 3단계 협업 모델을 안내한다:

```
"사용자가 방향을 잡고, MoAI 에이전트 팀이 실행합니다.

 ① 목표를 알려주세요 (What & Why)
   → 어떤 결과물이 왜 필요한가요?
 ② 재료를 주세요
   → 참고 문서, 데이터, 기존 자료가 있으면 공유해 주세요.
 ③ 초안을 검토해 주세요
   → MoAI가 만든 초안에 여러분만의 관점을 더해주세요.

 사용자가 지시하고, MoAI 에이전트 팀이 수행합니다."
```

### 0-2. 안내 표시 조건

| 조건 | 동작 |
|------|------|
| 최초 작업 실행 (해당 프로젝트에서 첫 실행) | 전체 안내 표시 |
| 2회 이상 실행 | 간략 안내만 ("목표와 재료를 알려주세요") |
| 사용자가 이미 구체적 지시를 제공한 경우 | 안내 생략 |

---

## 1. 실행 전 준비 (Pre-Execution)

### 1-1. 스킬/체인 식별 및 로딩

```
Phase 1: 요청 분석 → 스킬/체인 식별
  → bare /project 진입 또는 자연어 요청
  → router.md에서 적합한 플러그인/스킬(또는 스킬 체인) 식별

Phase 2: 스킬 워크플로우 로드
  선택된 스킬의 SKILL.md가 정의하는
  워크플로우·출력형식을 따른다.
  → 복수 스킬이면 체인 순서대로 연결

Phase 3: 맥락 수집 (있으면)
  IF 맥락 부족:
    → context-collector.md 실행
```

### 1-2. 복잡도 판단 및 Sequential Thinking

```
스킬 체인 실행 전 복잡도를 판단한다:

IF 다음 조건 중 하나 이상 충족:
  - 복합 요청 (2개 이상 플러그인/스킬 관련)
  - 다중 조건 분석 필요 (규제, 법률, 세무 등)
  - 의존적 실행 (Phase A 결과가 Phase B 입력)
  - 전략적 판단 필요 (비즈니스 의사결정, 투자 분석 등)

THEN:
  → 문제를 단계별로 분해
  → 각 단계의 입력/출력 정의
  → 실행 순서 및 의존성 확인
  → 위험/불확실성 식별
  → 구조화된 계획을 기반으로 스킬 체인 실행 진입
```

<!-- 1-3. 페르소나 채택 제거: Claude(Opus 4.6)가 프로필 맥락을 자연스럽게 반영하므로 명시적 주입 불필요 -->

### 1-3. 소크라테스식 전제 검증 (규제/전략 산출물)

규제·법률·전략 산출물 작성 시, 사용자의 전제가 산출물 품질에 직접 영향을 미친다.
잘못된 전제에 기반한 산출물은 위험하므로, 실행 전 열린 질문으로 전제를 검증한다.

```
대상 도메인 (전제 검증 필수):
  규제·법률·세무·재무·전략 산출물
  (예: 계약서 검토, 컴플라이언스, 세무 판단, 재무 분석,
   시장 진입·가격 전략, IR)

검증 질문 패턴 (텍스트 대화, 최대 2개):

  [전제 확인]  "이 판단의 근거가 되는 핵심 전제는 무엇인가요?"
  [반대 검증]  "반대 사례나 예외 상황은 어떤 게 있을까요?"
  [범위 확인]  "이 결과가 적용되는 범위(시간/지역/대상)는 어디까지인가요?"
  [리스크 인식] "이 방향으로 진행했을 때 가장 우려되는 점은 무엇인가요?"

적용 규칙:
  - 위 대상 도메인 산출물에만 적용 (다른 산출물은 스킵)
  - 사용자가 명확한 지시를 이미 제공한 경우 스킵
  - 검증 결과를 산출물 서두 "전제 조건" 섹션에 명시
  - Sequential Thinking과 병행 가능 (복잡도 높을 시)
```

---

## 2. 워크플로우 실행

### 2-1. 스킬별 워크플로우 예시

**카피라이팅 산출물 예**
```
입력: 주제, 길이, 톤, 타겟 독자

Step 1: 아웃라인 생성
  → 제목 + 3-4개 섹션 제목

Step 2: 각 섹션 작성
  → 500-750자/섹션

Step 3: SEO 최적화
  → 메타 디스크립션
  → 키워드 배치

Step 4: 검수
  → 문법, 사실 검증
  → 톤 일관성 확인

출력: 마크다운 파일
```

**SOP 문서 예**
```
입력: 프로세스 설명, 대상 업무, 담당자

Step 1: 현 상태(AS-IS) 분석
  → 단계별 현황
  → 소요 시간
  → 병목 지점

Step 2: 목표 상태(TO-BE) 설계
  → 표준화 대상 확인
  → 도구/시스템 선택
  → 예상 효율 계산

Step 3: SOP 문서 작성
  → 단계별 절차서
  → 체크리스트
  → 예외 처리 가이드

Step 4: 검증 및 배포 계획
  → KPI 정의
  → 교육 자료
  → 피드백 수집 절차

출력: SOP 문서 + 체크리스트
```

### 2-2. 에러 처리
```
IF 실행_중_오류:
  1. 오류 유형 식별
  2. 사용자에게 명시적 보고
  3. 대안 제시
  4. 롤백 또는 재시도
  
예:
"죄송합니다. API 호출 실패(404 Not Found)
 대안: [1] 다른 도구 사용 [2] 수동 설정 [3] 취소"
```

---

## 3. 산출물 전달

<!-- 섹션 3-1-3-3 (저장 구조, metadata.yaml, 파일 포맷 규칙) 제거:
     강제 디렉터리 구조는 오버헤드를 유발. Claude가 상황에 맞게 판단. -->
<!-- 섹션 4 (computer:// 링크, export 명령어) 제거:
     Cowork 환경에서 computer:// 링크 불필요. 파일 저장은 사용자 요청 시 수행. -->

산출물은 마크다운으로 직접 응답한다. 파일 저장이 필요하면 사용자가 요청할 때 수행한다.

초안 전달 시 아래 안내를 포함한다:
```
"초안이 완성되었습니다.
 이 결과물은 AI가 생성한 초안입니다.
 검토하시고, 수정이 필요하면 말씀해 주세요."
```

법률/재무/의료 산출물은 추가 면책:
```
"[주의] 본 내용은 참고용 초안이며, 법률/재무/의료 관련 사항은
 반드시 해당 분야 전문가의 검토를 거치시기 바랍니다."
```

---

## 3.5 산출물 품질 검증 루프 (자동)

모든 산출물은 생성 후 3단계 검증을 거친다.
검증은 **기본 활성화**이며, 사용자가 "빠르게" 등 요청 시에만 스킵한다.

```
산출물 생성 완료
    ↓
[Layer 1] 파일 유효성 (기계적)
  HWPX: unzip -t, mimetype, section0.xml 존재
  DOCX: unzip -t, word/document.xml 존재
  PPTX: unzip -t, 슬라이드 수 확인
  XLSX: unzip -t, sheet1.xml 존재
  텍스트: 길이 > 100자, 빈 파일 아님
    ↓ NG → 즉시 재생성
    ↓ OK
[Layer 1.5] 마크다운 렌더링 버그
  **텍스트** → 별표 그대로 노출 시 FAIL
  *이탤릭* → 별표 노출 시 FAIL
  `코드` → 백틱 노출 시 FAIL
  수정: 마크다운 제거 후 스타일 API로 서식 직접 적용
    ↓ NG → 마크다운 제거 + 볼드/이탤릭 재적용
    ↓ OK
[Layer 1.6] AI 작문 패턴
  슬롭 단어: 혁신적, 패러다임, 획기적, 선도적, 차세대, 최첨단 등
  패턴: ~합니다 3연속, 느낌표 과다, 추상적 찬사
  수정: 대체 표현으로 교체
    ↓ NG → 슬롭 단어/패턴 교체 후 재검증
    ↓ OK
[Layer 2] 내용 완전성 (AI 판단)
  사용자 요청 항목 전수 대조
  누락 항목, 미완성 섹션, 사실 오류 확인
    ↓ NG → 수정 후 Layer 1부터 재검증
    ↓ OK
[Layer 2.5] 근거 검증 (grounding) — NORMAL/DEEP 등급만 (§6-4)
  수치·날짜·규정·통계 등 외부 사실 주장의 출처 확인
  출처 없는 구체 수치를 사실로 단정 시 FAIL
    ↓ NG → 출처 보강 또는 「확인 필요」 표시 후 재검증
    ↓ OK
[Layer 3] 품질 평가 (quality-evaluator)
  정확성, 완전성, 실용성, 톤, 도메인 적합성
  PASS → 사용자에게 전달
  FAIL → 구체적 수정 지시 반환
    ↓ FAIL
  수정 지시 기반 재생성
    ↓
  Layer 1부터 재검증 (최대 3회 반복)
    ↓ 3회 후 FAIL
  현재 최선본 + 문제점을 사용자에게 보고
```

### 검증 의무 (HARD)

| 산출물 유형 | Layer 1 | Layer 2 | Layer 2.5 근거 | Layer 3 |
|-----------|---------|---------|---------|---------|
| 파일 생성 (HWPX/DOCX/PPTX/XLSX) | **필수** | **필수** | 수치 포함 시 | **필수** |
| 텍스트 산출물 (보고서, 분석) | 필수 | 필수 | 필수 | 선택 |
| 데이터 분석 (차트, 테이블) | 필수 | 필수 | **필수** | 선택 |
| 법률/재무/규제 산출물 | 필수 | 필수 | **필수** | **필수** |

> Layer 2.5(근거 검증)는 §6-4 검증 깊이 등급을 따른다 — QUICK은 스킵, NORMAL·DEEP은 활성.

### Office 문서 심층 검증 (moai-office 전용)

moai-office 스킬(hwpx-writer, docx-generator, pptx-designer, xlsx-creator)이
파일을 생성한 후, **생성된 파일을 다시 열어서 내용을 검증**한다.

```
생성 완료 → 파일 저장
    ↓
[재오픈 검증] 생성된 파일을 python-hwpx/python-docx/openpyxl로 다시 열기
    ↓
[구조 검증] 요구사항과 실제 내용 대조
    ↓ 불일치 → 수정 후 재생성
    ↓ 일치 → PASS
```

#### HWPX 재오픈 검증

```python
from hwpx import HwpxDocument

doc = HwpxDocument.open("output.hwpx")

# 1. 단락 수 검증
actual_paras = len(doc.paragraphs)
assert actual_paras >= expected_paras, f"단락 수 부족: {actual_paras}/{expected_paras}"

# 2. 표 구조 검증
table_map = doc.get_table_map()
tables = table_map.get("tables", [])
for i, expected in enumerate(expected_tables):
    actual = tables[i]
    assert actual["rows"] == expected["rows"], f"T{i} 행 수 불일치"
    assert actual["cols"] == expected["cols"], f"T{i} 열 수 불일치"

# 3. 텍스트 내용 검증
text = doc.export_text()
for keyword in required_keywords:
    assert keyword in text, f"필수 키워드 누락: {keyword}"

# 4. 머리글/바닥글 검증
headers = doc.headers
# 머리글 내용 확인

doc.close()
```

#### DOCX (Word) 재오픈 검증

```python
from docx import Document

doc = Document("output.docx")

# 1. 단락 수 + 내용 검증
paras = [p.text for p in doc.paragraphs if p.text.strip()]
assert len(paras) >= expected_count

# 2. 표 구조 검증
for i, table in enumerate(doc.tables):
    assert len(table.rows) == expected_rows[i]
    assert len(table.columns) == expected_cols[i]
    # 셀 내용 검증
    for r, row in enumerate(table.rows):
        for c, cell in enumerate(row.cells):
            if expected_cells.get((i, r, c)):
                assert cell.text == expected_cells[(i, r, c)]

# 3. 스타일 검증
for p in doc.paragraphs:
    if p.text == title_text:
        assert p.runs[0].bold == True, "제목 볼드 미적용"
    if p.text in italic_texts:
        assert p.runs[0].italic == True, "이탤릭 미적용"

# 4. 머리글/바닥글 검증
for section in doc.sections:
    header_text = section.header.paragraphs[0].text
    footer_text = section.footer.paragraphs[0].text
```

#### PPTX 재오픈 검증

```python
from pptx import Presentation
from pptx.util import Pt, Inches, Emu

prs = Presentation("output.pptx")

# 1. 슬라이드 수
assert len(prs.slides) >= expected_slides

# 2. 각 슬라이드 제목 + 본문
for i, slide in enumerate(prs.slides):
    shapes = [s for s in slide.shapes if s.has_text_frame]
    texts = [s.text_frame.text for s in shapes]
    assert any(expected_titles[i] in t for t in texts), f"슬라이드 {i} 제목 누락"

# 3. 폰트 크기 검증
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.font.size:
                        size_pt = run.font.size.pt
                        # 제목은 24pt 이상, 본문은 14pt 이상
                        if para == shape.text_frame.paragraphs[0]:
                            assert size_pt >= 20, f"제목 폰트 너무 작음: {size_pt}pt"

# 4. 레이아웃 검증 (텍스트 영역 이탈 방지)
slide_width = prs.slide_width
slide_height = prs.slide_height
for slide in prs.slides:
    for shape in slide.shapes:
        right = shape.left + shape.width
        bottom = shape.top + shape.height
        assert right <= slide_width + Inches(0.5), f"shape 오른쪽 이탈"
        assert bottom <= slide_height + Inches(0.5), f"shape 아래 이탈"

# 5. 디자인 일관성 검증
colors_used = set()
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.font.color and run.font.color.rgb:
                        colors_used.add(str(run.font.color.rgb))
# 색상 3개 이하 = 일관성 좋음
assert len(colors_used) <= 5, f"색상 너무 다양: {len(colors_used)}개"

# 6. 빈 슬라이드 검증
for i, slide in enumerate(prs.slides):
    has_content = any(
        s.has_text_frame and s.text_frame.text.strip()
        for s in slide.shapes
    )
    assert has_content, f"슬라이드 {i+1} 내용 없음"
```

#### XLSX 재오픈 검증

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, Border, PatternFill

wb = load_workbook("output.xlsx")
ws = wb.active

# 1. 행/열 수
assert ws.max_row >= expected_rows
assert ws.max_column >= expected_cols

# 2. 헤더 검증 (내용 + 스타일)
for c, expected in enumerate(expected_headers, 1):
    cell = ws.cell(1, c)
    assert cell.value == expected, f"헤더 불일치: {cell.value}"
    # 헤더 볼드 확인
    assert cell.font.bold, f"헤더 볼드 미적용: 열 {c}"
    # 헤더 배경색 확인
    if cell.fill and cell.fill.start_color:
        pass  # 배경색 있으면 OK

# 3. 데이터 타입 검증
for r in range(2, ws.max_row + 1):
    for c in numeric_columns:
        val = ws.cell(r, c).value
        assert isinstance(val, (int, float)), f"({r},{c}) 숫자 아님: {val}"

# 4. 숫자 포맷 검증 (통화, 퍼센트)
for r in range(2, ws.max_row + 1):
    for c in currency_columns:
        fmt = ws.cell(r, c).number_format
        assert '₩' in fmt or '#,##0' in fmt, f"({r},{c}) 통화 포맷 미적용"

# 5. 테두리 검증
for r in range(1, ws.max_row + 1):
    for c in range(1, ws.max_column + 1):
        cell = ws.cell(r, c)
        if cell.value is not None:
            border = cell.border
            has_border = any([
                border.left.style, border.right.style,
                border.top.style, border.bottom.style
            ])
            # 데이터 영역은 테두리 있어야 함
            assert has_border, f"({r},{c}) 테두리 없음"

# 6. 열 너비 검증 (내용 잘림 방지)
for col in ws.columns:
    col_letter = col[0].column_letter
    width = ws.column_dimensions[col_letter].width
    max_len = max((len(str(cell.value or '')) for cell in col), default=0)
    if max_len > 0:
        assert width >= max_len * 1.1, f"열 {col_letter} 너비 부족"

# 7. 수식 검증
if formula_cells:
    for cell_ref, expected_type in formula_cells.items():
        cell = ws[cell_ref]
        assert cell.value is not None

# 8. 시트명 검증
assert ws.title != "Sheet1" or len(wb.sheetnames) == 1, "시트명 미설정"
```

### 검증 체크리스트 요약

| 항목 | HWPX | DOCX | PPTX | XLSX |
|------|------|------|------|------|
| **내용** | | | | |
| 단락/셀 수 | paragraphs | paragraphs | slides | max_row |
| 표 구조 (행x열) | get_table_map | doc.tables | - | max_column |
| 텍스트 내용 | export_text | paragraph.text | shape.text | cell.value |
| 머리글/바닥글 | headers | section.header | - | - |
| 이미지 | list_images | inline_shapes | slide.shapes | - |
| 수식 | - | - | - | cell.value |
| **스타일** | | | | |
| 볼드/이탤릭 | char_property | run.bold/italic | run.font.bold | cell.font.bold |
| 폰트 크기 | fontSize | run.font.size | run.font.size | cell.font.size |
| 색상 | textColor | run.font.color | run.font.color | cell.font.color |
| **레이아웃** | | | | |
| 페이지/슬라이드 크기 | secPr.pageSize | section.page_* | slide_width/height | - |
| 여백 | secPr.pageMar | section.margin | shape 위치 | column_dimensions |
| 정렬 | paraPr.align | paragraph.alignment | paragraph.alignment | cell.alignment |
| **디자인** | | | | |
| 테두리 | borderFill | table cell borders | shape.line | cell.border |
| 배경색 | - | shading | shape.fill | cell.fill |
| 색상 일관성 | - | - | colors ≤ 5 | - |
| 열 너비/잘림 | - | - | shape 이탈 확인 | width ≥ 내용 |

### 원칙

- **생성 후 반드시 재오픈**: 파일을 저장한 뒤 다시 열어서 내용 확인
- **요구사항 대조**: 사용자 요청의 모든 항목이 실제 파일에 존재하는지 확인
- **자동 수정**: 불일치 발견 시 구체적으로 무엇이 틀렸는지 식별 후 재생성
- **3회 제한**: 최대 3회 재생성 후 사용자에게 보고

---

## 5. 사후 처리 (Post-Execution)

산출물 전달 후, 사용자가 수정을 요청하면 반영한다. 별도 자동 평가 절차 없음.

<!-- 섹션 5-1-5-3 (자동반성 0-100% 스코어링, 반성 기록, 강제 피드백 수집) 제거:
     Claude(Opus 4.6)가 자기평가를 자연스럽게 수행. 강제 점수화는 레거시 보상 패턴. -->
<!-- 피드백 수집은 /project evolve 실행 시에만 트리거됨 (evaluation-protocol 참조) -->

---

## 6. 실행 경로 선택

### 6-1. 빠른 실행 (Quick Mode)
```
조건:
- 맥락 완전 (모든 정보 제공됨)
- 사용자가 명시적으로 요청

프로세스:
- 인터뷰/검증/피드백 수집 스킵
- 즉시 산출물 제공
```

### 6-2. 대화형 실행 (Interactive Mode, 기본)
```
bare /project 진입 워크플로우의 기본 모드

프로세스:
- 부족한 맥락 수집 (소크라테스 인터뷰)
- 워크플로우 단계마다 확인 기회
- 결정론적 검증 수행
```

### 6-3. 배치 실행 (Batch Mode)
```
config: {
  chains: [
    [copywriting, ai-slop-reviewer],
    [email-crafter, ai-slop-reviewer]
  ],
  inputs: [input_001, input_002]
}

결과:
- 모든 입력 동시 처리
- 통합 결과 요약 생성
```

### 6-4. 검증 깊이 사다리 (위험 비례)

위 실행 모드(6-1~6-3)와 별개로, **검증 깊이**는 요청의 위험 수준에 비례한다.
quick/normal/deep 분류를 비즈니스 산출물에 재매핑한 것으로, 저위험 작업에 과한 검증을, 고위험 작업에 부족한 검증을 거는 것을 둘 다 막는다.

| 등급 | 대상 | 검증 범위 |
|------|------|----------|
| **QUICK** | 단순 조회·요약·재구성·아이디어 (예: "세율 얼마야", "이 문단 줄여줘") | Layer 1만. 근거 게이트(§3.5 Layer 2.5) 스킵 |
| **NORMAL** (기본) | 일반 보고서·카피·문서·기획 | Layer 1~2.5. 근거 게이트 활성 |
| **DEEP** | 규제·법률·세무·재무·정부지원·계약·의료, 또는 2개+ 플러그인 체인 | 전체 Layer 1~3 + 근거 게이트 필수 + §3 면책 문구 필수 + 전달 전 AskUserQuestion 확인 |

**DEEP 자동 트리거 키워드 (seed — 분류기 아님, 최종 판단은 맥락으로):**
법률·계약·NDA·약관·개인정보·컴플라이언스·정부지원·공고·세무·부가세·종소세·재무제표·IR·투자·의료·규제 + 산출물이 2개+ 플러그인 체인에 걸칠 때.

**적용 규칙:**
- DEEP 등급은 §1-3 소크라테스식 전제 검증(규제/전략 도메인) 대상과 일치 — 전제 검증도 함께 수행
- 사용자가 "빠르게"·"그냥" 명시 시 QUICK으로 강등하되, DEEP 도메인은 위험 고지 후에만 강등
- 키워드는 seed일 뿐 — 트리거 단어 없이 표현된 고위험 요청을 놓치지 않도록 맥락 판단을 우선한다

<!-- 섹션 7 (캐싱/병렬 처리 성능 최적화) 제거: Claude가 컨텍스트 내에서 자연스럽게 처리 -->
<!-- 섹션 8 (모니터링/로깅) 제거: 운영 오버헤드. 필요 시 별도 구성 -->

---

## 7. 코드 실행 활용

데이터 검증, 포맷 변환, 결과 필터링 등은 bash/Python 스크립트로 처리한다.
모든 결과를 컨텍스트에 로드하지 않고, 최종 결과만 반환한다.

예시:
- 세무 계산: Python으로 정확한 수치 계산 후 결과만 보고
- 문서 변환: scripts/ 스크립트 실행 후 파일 경로만 전달
- 데이터 분석: bash 파이프로 필터링 후 요약만 컨텍스트에 포함
