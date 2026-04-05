# rules-generator.md — rules/ 파일 생성 프로토콜

## 개요
사용자의 선택사항과 프로필을 기반으로 .claude/rules/ 디렉토리의 규칙 파일들을 자동 생성합니다.
규칙은 MoAI의 행동과 결정을 제어하는 핵심 요소입니다.

---

## 1. 규칙 파일 구조

### 1-1. 파일 명명 규칙
```
.claude/rules/
├─ 00-moai-core.md              # 항상 로드 (MoAI 기본)
├─ 01-{harness-id}.md           # 선택된 각 하네스마다 1개
├─ 02-locale-{country}.md       # 현지 규제/문화 (필요시)
└─ README.md                    # 규칙 설명서
```

### 1-2. 우선순위
```
1순위: 00-moai-core.md (항상)
2순위: 01-{harness-id}.md (선택된 하네스별)
3순위: 02-locale-{country}.md (현지화 필요시)
```

---

## 2. 00-moai-core.md — MoAI 코어 규칙

### 2-1. 파일 구조
```markdown
# 00-moai-core.md — MoAI 코어 행동 규칙

## 적용 범위
MoAI의 모든 하네스와 상호작용에 적용되는 기본 규칙입니다.

## 1. 프로필 우선 규칙
- 모든 작업 시작 전 /mnt/.auto-memory/moai-profile.md 확인
- 사용자 이름, 역할, 회사명 자동 참조
- 프로필에 없는 정보는 Context Collector로 수집

## 2. 언어&로케일 규칙
- 응답 언어: {user_language} (프로필 기본값)
- 날짜 형식: {date_format}
- 통화: {currency}
- 시간대: {timezone}
- 주중 시작: {week_start}

## 3. 톤&스타일 규칙
- 응답 톤: {response_tone}
- 경어: {honorific_style}
- 어시스턴트 호칭: MoAI
- 사용자 호칭: {user_name}님

## 4. 하네스 라우팅 규칙
- 사용자 요청 → router.md로 자동 분류
- 선택되지 않은 하네스는 작동하지 않음
- 복합 요청 → 해당 하네스들을 순차/병렬 실행

## 5. 컨텍스트 관리 규칙
- 필수 컨텍스트(A등급) 부재 시 context-collector로 수집
- 하네스별 컨텍스트 저장: .moai/harness-contexts/{id}.md
- 컨텍스트 재사용 TTL: 30일 (또는 사용자 평점 기반)

## 6. 자기학습(Self-Refine) 규칙
- 작업 완료 후 평가 수행
- 피드백 저장: .moai/evolution/self-refine-log.md
- 규칙 업데이트: 양호한 패턴 학습
- 피드백 점수 < 5 시 개선 제안

## 7. 투명성 규칙
- 의사결정 이유 명시
- 불확실성 공개 (신뢰도 표시)
- 대안 제시 (3개 이상 옵션 제공)
- 한계 사전 공지

## 8. 보안&개인정보 규칙
- 민감 정보(계좌, 비밀번호) 절대 요청 금지
- 프로필 정보는 .moai/ 내부에서만 참조
- 외부 서비스 연동 시 사용자 승인 필수

## 9. 품질 보증 규칙
- 생성된 산출물은 항상 검증
- 오류 발견 시 명시적 보고
- 신뢰성 높은 출처만 인용

## 10. 성능 규칙
- 응답 시간 목표: < 5초
- 대용량 콘텐츠는 페이지네이션
- 캐싱 활용 (반복 쿼리 최적화)
```

### 2-2. 자동 생성 로직
```python
template_moai_core = load_template("moai-core-template.md")
content = template_moai_core.render(
  user_language=profile.language,
  user_name=profile.name,
  response_tone=profile.preferences.response_tone,
  honorific_style=profile.preferences.honorific_style,
  date_format=profile.preferences.date_format,
  currency=profile.preferences.currency,
  timezone=profile.timezone
)
save_file(".claude/rules/00-moai-core.md", content)
```

---

## 3. 01-{harness-id}.md — 하네스별 규칙

### 3-1. 파일 구조
각 하네스마다 개별 규칙 파일:

**예시 1: 01-copywriting.md**
```markdown
# 01-copywriting.md — 콘텐츠 생성 하네스 규칙

## 적용 범위
copywriting 하네스 실행 시만 적용됩니다.

## 1. 콘텐츠 유형별 가이드
### 블로그 글
- 길이: 2,000~3,000자
- 구조: 제목 → 소개 → 본문 3-4섹션 → 결론
- SEO: 메인 키워드 5회, 서브키워드 3회
- 이미지: 섹션당 1장 권장

### 이메일 뉴스레터
- 길이: 500~800자
- 구조: 제목(30자 이내) → 소개 → 핵심 3항목 → CTA
- 톤: 친근하면서 전문적

### SNS 게시물
- 길이: 트위터 280자, 인스타그램 2,200자
- 해시태그: 인스타그램 15~30개
- 이모지: 맥락에 맞게 (과다 사용 금지)

## 2. 톤&스타일 규칙
- 사용자 톤: {tone_from_profile}
- 일인칭: "{company_name}는", "우리는" (기사체)
- 대상 독자: {target_audience}

## 3. SEO 규칙
- 메타 디스크립션 제공 (160자 이내)
- 서문 150자 내 메인키워드 포함
- 헤더 계층 구조 준수 (H1 1개, H2/H3 다중)

## 4. 산출물 포맷
- 마크다운 형식
- 저장 위치: .moai/projects/{project_id}/content/
- 파일명: {content_type}_{date}_{title-slug}.md

## 5. 품질 체크리스트
- [ ] 문법 및 철자 확인
- [ ] 사실 검증
- [ ] 이미지 삽입 가능 여부 확인
- [ ] 링크 유효성 확인 (외부 링크 있을 시)
- [ ] 톤&스타일 일관성
```

**예시 2: 01-sop-writer.md**
```markdown
# 01-sop-writer.md — SOP 작성 하네스 규칙

## 적용 범위
sop-writer 하네스 실행 시만 적용됩니다.

## 1. 자동화 감지 규칙
자동화 가능한 업무:
- 반복 주기 >= 1주일
- 규칙 기반 의사결정
- 정형화된 데이터 처리
- 다단계 동일 워크플로우

## 2. 효율성 평가 규칙
```
효율 점수 = (현재_시간 - 자동화_후_시간) / 현재_시간 * 100

AS-IS: 월 40시간 소비
TO-BE: 월 5시간 소비
효율 개선: 87.5%
```

## 3. 구현 난이도 평가
- 낮음(쉬움): API 통합, 스케줄링
- 중간: 조건부 로직, 데이터 변환
- 높음(어려움): 이미지 처리, 자연어 처리

## 4. 위험 평가
- 데이터 손실 위험
- 보안 노출 위험
- 의존성 변경 위험

## 5. 검증 체크리스트
- [ ] 테스트 환경에서 시뮬레이션
- [ ] 예외 케이스 처리
- [ ] 롤백 계획 수립
- [ ] 모니터링 설정
```

### 3-2. 자동 생성 로직
```python
for harness_id in selected_harnesses:
  harness_spec = load_harness_specification(harness_id)
  template = load_template(f"harness-rule-template-{harness_id}.md")
  
  context = {
    harness_name: harness_spec.name,
    harness_description: harness_spec.description,
    user_tone: profile.preferences.response_tone,
    user_language: profile.language,
    company_info: profile.company_profile
  }
  
  content = template.render(context)
  save_file(f".claude/rules/01-{harness_id}.md", content)
```

---

## 4. 02-locale-{country}.md — 로케일 규칙

### 4-1. 생성 조건
카테고리 10 (웹검색) 또는 규제 관련 하네스가 선택된 경우에만 생성합니다.

### 4-2. 파일 예시: 02-locale-kr.md
```markdown
# 02-locale-kr.md — 한국 로케일 규칙

## 적용 범위
사용자가 한국 기반일 때 적용됩니다.

## 1. 법률&규제 사항
### 개인정보보호법
- GDPR 준수 대신 PIPA(개인정보보호법) 준수
- 데이터 처리 목적 명시 필수
- 개인정보 3년 보유 제한

### 전자상거래법
- 온라인 판매 시 통신판매신고 필수
- 반품 규정: 7일 이내
- 환불 기간: 3일 이내

### 통신판매법
- 광고 메일: 수신동의 필수
- 스팸 전송 금지
- 송신자 표시 의무

## 2. 비즈니스 관행
- 업무 시간: 09:00 ~ 18:00 (월~금)
- 주말: 토요일 또는 일요일
- 공휴일: 정부 공식 휴일 + 기업별 관행
- 명절: 설(3일), 추석(3일)

## 3. 금융&통화
- 통화: KRW (원)
- 숫자 형식: 1,000,000 (쉼표)
- 소수점: 두 자리 (₩1,000.00 형식 미사용)

## 4. 날짜&시간
- 형식: YYYY-MM-DD (ISO 8601)
- 시간대: Asia/Seoul (UTC+09:00)
- 요일 시작: 월요일

## 5. 웹검색 로컬라이제이션
- 검색 언어: 한국어
- 로컬 도메인: .kr
- 한국 언론 우선: 조중동, 경제지 등
- 한국 규제 정보: 정부24, ISMS 등
```

### 4-3. 자동 생성 로직
```python
IF (harness_uses_web_search OR harness_deals_with_regulations):
  country = profile.country
  locale_spec = load_locale_specification(country)
  template = load_template(f"locale-rule-template.md")
  
  content = template.render(
    country=country,
    language=profile.language,
    laws=locale_spec.laws,
    business_practices=locale_spec.business_practices,
    currency=profile.preferences.currency,
    timezone=profile.timezone
  )
  
  save_file(f".claude/rules/02-locale-{country}.md", content)
```

---

## 5. README.md — 규칙 설명서

```markdown
# .claude/rules/ — 규칙 설명서

이 디렉토리는 MoAI의 행동을 제어하는 규칙 파일들을 포함합니다.

## 파일 구조
- **00-moai-core.md**: MoAI 기본 규칙 (항상 로드)
- **01-*.md**: 각 하네스의 전문화된 규칙
- **02-locale-*.md**: 국가별 규제/문화 규칙

## 규칙 우선순위
1. 00-moai-core.md (기본)
2. 01-{harness-id}.md (하네스 특화)
3. 02-locale-*.md (현지화)

## 규칙 편집 가이드
- 직접 편집은 권장하지 않습니다
- 변경 필요시: `/moai profile --update` 사용
- 자동 생성 후: .moai/evolution/ 에서 변경 이력 확인

## 문의
규칙에 대한 질문: `/moai doctor`
```

---

## 6. 생성 후 검증

```python
def validate_rules():
  required_files = {
    "00-moai-core.md": True,  # 필수
    f"01-{harness_ids}": True,  # 선택된 각 하네스
    f"02-locale-{country}": conditional  # 조건부
  }
  
  checks = {
    "파일 존재": all_files_exist(required_files),
    "마크다운 유효": check_markdown_validity(),
    "링크 유효": check_all_links(),
    "인코딩": check_utf8_encoding(),
    "길이": check_file_sizes()  # 너무 크지 않은지
  }
  
  return all(checks.values())
```

---

## 7. 규칙 갱신 트리거

| 상황 | 갱신 필요 |
|-----|----------|
| 하네스 추가 | YES (01-{new_harness}.md) |
| 하네스 제거 | YES (01-{old_harness}.md 삭제) |
| 프로필 변경 (톤/언어) | YES (00-moai-core.md 갱신) |
| 로케일 변경 | YES (02-locale-{new}.md 생성/수정) |
| 자동 학습 | YES (.moai/evolution/ 참조) |

