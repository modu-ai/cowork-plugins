# AI 이미지 생성기 (Nano Banana Image Generator)

자연어 프롬프트(한글/영문)로 고품질 AI 이미지를 생성합니다.
Google의 **Imagen 4** 모델을 활용하여 사진급 현실감의 이미지를 단 몇 초 안에 제공합니다.

## Overview

마케팅, 콘텐츠 제작, 디자인 작업에 필요한 이미지를 즉시 생성합니다.

**주요 용도:**
- 소셜미디어 콘텐츠 (카드뉴스, 게시물)
- 블로그 대표 이미지
- 제품/서비스 시각화
- 광고 배너
- 프리젠테이션 슬라이드
- 책/매거진 삽입 이미지

> **핵심**: 사용자가 "프리랜서 절세팁 인포그래픽 이미지 3개"라고 말하면,
> 3개의 고품질 이미지(각 3~4가지 스타일)를 3초 안에 받을 수 있어야 합니다.

---

## 이미지 생성 가능 범위

### ✅ 생성 가능 (권장)
```
- 풍경 (자연, 도시, 실내)
- 추상/그래픽 (기하학, 색상, 그래디언트)
- 제품 이미지 (일반적/상업적)
- 생활용품, 음식, 음료
- 텍스처 (목재, 직물, 돌, 물, 빛)
- 컨셉 일러스트 (회의 장면, 팀워크, 성공 등)
- 간단한 인포그래픽 (그래프, 다이어그램)
```

### ⚠️ 제약 (품질 저하 가능)
```
- 특정 유명인 (저품질, 부정확)
- 복잡한 문자/숫자 (왜곡 가능)
- 의료/기술 정확도가 중요한 이미지
- 실사 같은 손/얼굴 (부자연스러울 수 있음)
```

### ❌ 생성 불가 (정책 위반)
```
- 폭력, 혐오, 성인 콘텐츠
- 초상권/저작권 위반 (유명인 정확 재현)
- 기만적 콘텐츠 (가짜 뉴스)
- 불법 활동
```

---

## 프롬프트 작성 가이드

### 프롬프트 구조 (한글/영문 모두 지원)

```
[메인 피사체] [스타일] [분위기] [기술적 요소] [품질]
```

**예시:**

1. 단순형
```
프리랜서가 노트북으로 일하는 홈오피스, 밝고 현대적인 느낌, 고품질 사진
```

2. 상세형
```
홈오피스에서 노트북으로 일하는 젊은 프리랜서 여성, 
따뜻한 오후 햇빛, 식물과 책장 배경, 
전문적이고 영감을 주는 분위기,
상업용 사진 품질, 사진작가 촬영, 85mm 렌즈
```

3. 스타일 강조형
```
절세팁 인포그래픽, 
미니멀 디자인, 파스텔 색상 (블루/그린), 
명확한 아이콘, 깔끔한 타이포그래피,
현대적이고 전문적, 비즈니스 잡지 스타일
```

### 효과적인 프롬프트 팁

#### 1. 스타일 키워드
```
사진 스타일:
- "cinematic photography" (영화적)
- "commercial photography" (상업 사진)
- "high quality photo" (고품질)
- "professional product shot" (제품 사진)
- "studio lighting" (스튜디오 조명)

일러스트 스타일:
- "minimalist illustration" (미니멀)
- "flat design" (플랫 디자인)
- "3D illustration" (3D)
- "watercolor painting" (수채화)
- "vector art" (벡터)

기타:
- "infographic" (인포그래픽)
- "icon set" (아이콘)
- "abstract" (추상)
```

#### 2. 분위기 표현
```
긍정적:
- "bright, cheerful, inspiring"
- "warm, welcoming, friendly"
- "professional, modern, sleek"

부정적:
- "dark, mysterious, moody"
- "rustic, vintage, nostalgic"
- "futuristic, sci-fi"
```

#### 3. 기술적 디테일
```
카메라/렌즈:
- "50mm lens"
- "wide angle photography"
- "macro lens"
- "telephoto"

조명:
- "soft diffused light"
- "golden hour"
- "backlighting"
- "high contrast"

색감:
- "vibrant colors"
- "desaturated palette"
- "warm tones"
- "cool blue tones"
```

#### 4. 품질 향상 용어
```
- "high quality, detailed"
- "professional grade"
- "award-winning photography"
- "intricate details"
- "sharp focus, crisp"
- "4K resolution"
- "magazine cover quality"
```

---

## 이미지 생성 프로세스

### Step 1: 사용 목적 확인
```
- 플랫폼: SNS, 블로그, 광고, 프리젠테이션?
- 용도: 대표 이미지, 배경, 제품 시각화?
- 타겟: B2C, B2B, 특정 나이대?
```

### Step 2: 프롬프트 작성
```
주제 설명 → 스타일 정의 → 분위기 지정 → 기술 요소
```

### Step 3: 이미지 생성
```
(자동) Imagen 4 모델 처리 (3~10초)
→ 여러 배리에이션 생성 (다양성)
```

### Step 4: 결과 평가 및 선택
```
품질: 해상도, 선명도, 색감
관련성: 프롬프트와의 부합도
유용성: 실제 용도에 적합한가?

만족 → 저장 / 미만족 → 프롬프트 수정
```

---

## 생성 옵션 (고급)

### 이미지 수량
```
기본: 1개
선택 가능: 2~4개 (비용 증가)
추천: 3개 (다양한 컨셉)
```

### 이미지 크기 (비율)
```
인스타그램: 1:1 (정사각형), 4:5 (세로)
유튜브: 16:9 (가로)
블로그: 16:10, 3:2 (가로)
프리젠테이션: 16:9
인쇄: 3:4, 8:10

기본: 1:1 또는 4:5 (사용자 지정 가능)
```

---

## 출력 형식

### 이미지 파일
```
형식: PNG (투명도 필요) 또는 JPG (작은 용량)
해상도: 1024×1024, 1440×1440 등 (고해상도)
색상공간: sRGB (웹 기준)
용량: 500KB~2MB (압축됨)
```

### 메타데이터
```
파일명: imagegen_[번호]_[스타일].png
생성일: 자동 포함
프롬프트: 사용자 입력 프롬프트 기록
```

---

## 절대 규칙 (Hard Rules)

### 1. 저작권
```
생성된 이미지는 상업용, 개인용 모두 사용 가능
- 상업 광고: OK
- 책/잡지 출판: OK
- SNS 공유: OK
- 재배포 (이미지 재판매): 확인 필요
```

### 2. 한글 텍스트
```
이미지 내 텍스트 생성은 비추천:
- 한글/숫자가 왜곡될 수 있음
- 특수 형식(이모지) 미지원

대안:
1. 텍스트 없이 이미지만 생성
2. Figma/Photoshop에서 텍스트 추가
3. 영문 텍스트 포함 요청 (영문이 더 정확)
```

### 3. 배경 제거
```
투명 배경 필요 시:
- PNG 형식 사용
- "transparent background" 프롬프트 포함
- 또는 추후 Photoshop/Figma에서 제거
```

### 4. 재현성
```
같은 프롬프트로도 매번 다른 이미지 생성
→ 특정 이미지 재현 어려움
→ 원하는 스타일이면 생성 후 진행
```

---

## 워크플로우

```
사용 목적 확인
↓
프롬프트 작성 (명확하고 상세하게)
↓
이미지 생성 요청 (1~4개)
↓
결과 평가 (품질, 관련성)
↓
만족 → 다운로드 / 미만족 → 프롬프트 수정
↓
텍스트/편집 필요시 추가 작업
```

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| 이미지 품질 낮음 | 프롬프트 불충분 | "high quality", "professional" 추가 |
| 색감 이상 | 스타일 미지정 | 구체적 색상/분위기 명시 |
| 텍스트 왜곡 | 한글 포함 | 텍스트 없이 생성, 후 합성 |
| 배경 불필요 | 지정 안 함 | "transparent background" 추가 |
| 특정인물 부정확 | 저명인 재현 한계 | "person, no specific face" 수정 |
| 생성 안 됨 | 정책 위반 | 폭력/부적절 내용 제거 |

---

## 프롬프트 예시 모음

### 마케팅/비즈니스
```
1. 프리랜서 홈오피스
"freelancer working from home office, bright natural light, laptop and desk, 
modern minimalist aesthetic, professional photography, inspiring mood"

2. 팀 미팅
"diverse team in a bright meeting room discussing business strategy, 
modern office, collaborative atmosphere, professional photography, 
natural lighting, high quality"

3. 성공 컨셉
"person celebrating success with arms raised, office background, 
golden hour lighting, professional photography, triumphant mood"
```

### 라이프스타일
```
1. 모닝 루틴
"person having coffee at home in morning, natural window light, 
cozy aesthetic, warm tones, lifestyle photography, peaceful mood"

2. 운동 중
"person exercising at gym, energetic mood, bright gym equipment, 
professional fitness photography, dynamic lighting"
```

### 인포그래픽/추상
```
1. 절세팁 배너
"minimalist infographic background, blue and green color palette, 
flat design, clean typography, professional business design, 
no text overlay, high quality"

2. 성장 차트
"abstract growth chart visualization, upward arrows, graph elements, 
modern flat design, bright colors, business concept illustration"
```
