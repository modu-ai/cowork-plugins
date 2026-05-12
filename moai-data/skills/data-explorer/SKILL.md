---
name: data-explorer
description: >
  CSV/Excel 데이터 탐색과 프로파일링을 수행합니다.
  '이 데이터 분석해줘', 'CSV 요약해줘', '이상값 찾아줘', '데이터 품질 체크해줘'라고 요청할 때 사용하세요.
  컬럼 요약, 결측값/이상값 탐지, 상관관계 분석, 데이터 품질 보고서를 생성합니다.
user-invocable: true
version: 2.4.0
---

# 데이터 탐색기 (Data Explorer)

## 역할
CSV/Excel 파일을 받아 데이터 프로파일링, 품질 검사, 기초 분석을 수행하는 전문가.

## 워크플로우

### Step 1: 데이터 로딩
- 파일 형식 감지 (CSV, XLSX, TSV)
- 인코딩 자동 감지 (UTF-8, CP949, EUC-KR)
- 행/열 수, 데이터 타입 추론

### Step 2: 프로파일링
- 각 컬럼별: 타입, 유니크 수, 결측률, 최소/최대/평균/중앙값
- 범주형 컬럼: 상위 5개 빈도
- 수치형 컬럼: 분포 요약 (왜도, 첨도)

### Step 3: 품질 검사
- 결측값 패턴 (MCAR/MAR/MNAR 추론)
- 이상값 탐지 (IQR 방법, Z-score)
- 중복 행 식별
- 데이터 타입 불일치

### Step 4: 상관관계 분석
- 수치 컬럼 간 피어슨/스피어만 상관계수
- 높은 상관(|r| > 0.7) 하이라이트
- 범주-수치 간 관계 (ANOVA F-test)

### Step 5: 인사이트 + 분석 방향 제안
- 핵심 발견 3가지 요약
- 분석 방향 3가지 제안 (AskUserQuestion)

## 산출물
- 데이터 프로파일 보고서 (마크다운)
- 품질 점수 (0~100)
- 분석 방향 추천

## 도구 사용
- Bash: Python pandas 스크립트 실행 (프로파일링)
- Read: CSV/Excel 파일 직접 읽기
- 시각화 필요 시: moai-data:data-visualizer로 연계

## 이 스킬을 사용하지 말아야 할 때
- **차트/그래프 생성** → moai-data:data-visualizer 사용
- **공공데이터 조회** → moai-data:public-data 사용
- **PPT/Word 변환** → moai-office 플러그인 사용