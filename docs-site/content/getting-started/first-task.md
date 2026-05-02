---
title: "첫 작업"
weight: 20
description: "5분 만에 완료하는 IR 덱 생성 체험 예제"
geekdocBreadcrumb: true
---

# 첫 작업: IR 덱 생성 체험

이 가이드는 MoAI Cowork Plugins을 사용하여 실제 비즈니스 문제를 해결하는 전체 과정을 5분 만에 체험할 수 있도록 설계되었습니다. Series A IR 덱을 생성하는 전체 워크플로우를 직접 경험해 보세요.

## 목표

**5분 안에 완료할 수 있는 작업:**
- SaaS Series A IR 덱 초안 생성
- 전문가 스킬 체인 자동 실행
- 결과물 파일로 확인

## 실행 절차

### 1단계: 프로젝트 생성 및 폴더 연결

{{< hint "note" >}}
**준비물**: 시스템에 Claude Desktop이 설치되어 있고, 작업할 빈 폴더가 필요합니다.
{{< /hint >}}

1. 새 폴더를 생성하고 Claude Desktop에 연결
2. Cowork 모드에서 해당 폴더 선택
3. 새 프로젝트가 생성되었음을 확인

### 2단계: 프로젝트 초기화

`/project init` 명령어로 프로젝트를 초기화합니다:

```bash
/project init
```

**7단계 인터뷰 진행**:
1. 프로젝트 이름 입력: "SaaS IR Deck Project"
2. 주요 도메인 선택: "business", "finance"
3. 사용자 정보 입력: 본인의 이름/회사
4. 문서 언어 선택: "korean"
5. 출력 형식 선택: "presentation"
6. 추가 기능 선택: "investor-relations"
7. 최종 확인: "yes" 입력

{{< hint "tip" >}}
**팁**: 인터뷰 중 "ai-slop-reviewer"와 "investor-relations" 스킬을 선택하면 IR 덱 생성에 최적화된 설정이 적용됩니다.
{{< /hint >}}

### 3단계: 첫 작업 요청

자연어로 Series A IR 덱 생성을 요청합니다:

```
"SaaS Series A IR 덱 초안 만들어줘"
```

**요청 상세 내용**:
- 비즈니스 모델: SaaS 플랫폼
- 투자 단계: Series A
- 대상 투자사: 벤처 캐피털
- 포함 내용: 시장 분석, 재무 모델, 성장 전략

### 4단계: 스킬 체인 자동 실행

요청을 받은 MoAI가 자동으로 전문 스킬 체인을 실행합니다:

1. **investor-relations 스킬** 실행:
   - 투자자 대상 IR 자료 생성
   - 시장 분석 및 경쟁사 대비 분석
   - 재무 모델 및 성장 지표 설정

2. **pptx-designer 스킬** 실행:
   - 생성된 내용을 기반으로 PPTX 디자인
   - 전문적인 IR 덱 레이아웃 적용
   - 데이터 시각화 및 차트 생성

3. **ai-slop-reviewer 스킬** 실행:
   - 전체 텍스트 품질 검수
   - AI 생성 패턴 검증 및 개선
   - 최종 결과물 다듬기

{{< hint "note" >}}
**스킬 체인**: 세 개의 전문 스킬이 순차적으로 실행되어 고품질의 결과물을 생성합니다. 각 스킬은 특정 도메인의 전문성을 가집니다.
{{< /hint >}}

### 5단계: 결과물 확인

작업이 완료되면 다음과 같이 결과물을 확인할 수 있습니다:

#### 생성된 파일
- `SaaS_Series_A_IR_Deck.pptx` - 최종 IR 덱 파일
- `analysis_report.md` - 분석 보고서
- `financial_model.xlsx` - 재무 모델 파일

#### 결과물 품질
- **전문적 구조**: Series A 투자 표준에 맞는 구조
- **데이터 시각화**: 그래프와 차트를 통한 명확한 데이터 전달
- **투자자 중심**: 투자사의 관심사를 반영한 내용
- **브랜딩**: 일관된 디자인 및 톤앤매너

## 실제 화면 예시

{{< hint "note" >}}
**스크린샷**: 실제 실행 시 화면은 Claude Desktop의 Cowork 모드에서 확인할 수 있습니다. 각 스킬 실행 시 진행 상황이 실시간으로 표시됩니다.
{{< /hint >}}

### 실행 전 상태
- 프로젝트 폴더: 비어있음
- 활성 스킬: 없음
- 생성 파일: 없음

### 실행 중 상태
- 스킬 체인 실행 표시
- 진행률: investor-relations → pptx-designer → ai-slop-reviewer
- 실시간 로그 표시

### 실행 후 상태
- 최종 파일: `SaaS_Series_A_IR_Deck.pptx`
- 파일 크기: 약 15-20MB
- 완료 메시지: "IR 덱 생성이 완료되었습니다!"

## 성공 요소

### 왜 이 방식이 효과적인가?

1. **전문성**: 각 스킬이 특정 도메인의 전문성을 제공
2. **자동화**: 수동 단계 없이 자동으로 최종 결과물 생성
3. **품질 보증**: ai-slop-reviewer로 고품질 결과물 보장
4. **일관성**: 표준화된 템플릿과 프로세스 적용

### 비교 표

| 방식 | 시간 | 품질 | 전문성 | 자동화 |
|------|------|------|--------|--------|
| 수동 제작 | 2-3일 | 중간 | 제한적 | 낮음 |
| 일반 AI 도구 | 30분 | 중간 | 일반적 | 중간 |
| **MoAI 체인** | **5분** | **높음** | **전문적** | **완전 자동** |

## 확장 활용

이 체인을 응용하여 다양한 작업을 자동화할 수 있습니다:

### 다양한 유형의 IR 덱
- Pre-seed 덱: 초기 단위 투자 대상
- Series B 덱: 성장 단계 투자
- IPO 준비 덱: 상장 준비 자료

### 다른 스킬 체인
- 블로그 생성: `blog` → `ai-slop-reviewer` → `nano-banana`
- 사업 계획서: `strategy-planner` → `pptx-designer` → `ai-slop-reviewer`
- 랜딩 페이지: `copywriting` → `landing-page` → `ai-slop-reviewer`

## 다음 단계

첫 작업을 성공적으로 완료했다면 이제 더 깊은 기능을 탐색할 준비가 되었습니다:

- [빠른 시작 가이드](../quick-start/) - 모든 주요 스킬 숙지하기
- [릴리스 정보](../releases/) - 최신 기능 업데이트 확인하기
- [기여하기](../contributing/) - 직접 스킬 개발하기

### Sources
- GitHub 저장소: [https://github.com/modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- investor-relations 스킬: [../plugins/moai-business/](../plugins/moai-business/)
- pptx-designer 스킬: [../plugins/moai-office/](../plugins/moai-office/)
- ai-slop-reviewer 스킬: [../plugins/moai-core/](../plugins/moai-core/)