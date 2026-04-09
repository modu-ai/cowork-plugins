# profile-manager.md — 글로벌 프로필 관리

## 개요
/mnt/.auto-memory/moai-profile.md를 중심으로 사용자 글로벌 프로필을 관리하는 프로토콜입니다.
CRUD 작업, 스키마 관리, 버전 관리를 포함합니다.

---

## 1. 프로필 스키마

### 1-1. 기본 구조
```yaml
moai_profile:
  version: "1.0.0"
  created: "2026-04-04T10:30:00+09:00"
  last_updated: "2026-04-04T10:30:00+09:00"
  
  user_profile: {}
  role_industry: {}
  company_profile: {}
  preferences: {}
  context_depth: {}
```

---

## 2. User Profile 섹션

### 2-1. 필드 정의
```yaml
user_profile:
  name: "김철수"                    # 사용자 이름
  email: "kim@example.com"           # 이메일
  language: "korean"                 # 선호 언어 (한국어 고정)
  country: "KR"                      # 국가 코드 (ISO 3166-1)
  timezone: "Asia/Seoul"             # IANA 타임존
  preferred_pronouns: "he/him"       # 대명사 선호
  birth_year: 1985                   # 연생 (선택)
```

### 2-2. 검증 규칙
- name: 1~100자, 특수문자 제한
- email: RFC 5321 형식
- country: 정확히 2자 대문자
- timezone: IANA 데이터베이스 확인
- language: "korean" 고정

---

## 3. Role & Industry 섹션

### 3-1. 필드 정의
```yaml
role_industry:
  role: "마케팅 관리자"              # 직책
  role_category: "marketing"         # 카테고리: [marketing, pm, strategy, finance, tech, hr, sales, operations]
  industry: "IT테크"                # 산업
  industry_code: "61"                # NAICS 코드
  company_type: "B2B SaaS"          # 회사 타입
  experience_level: "senior"         # [entry, mid, senior, executive, freelancer]
  years_experience: 8                # 연차
  primary_skill: "Digital Marketing" # 주요 기술
  secondary_skills: ["Content Strategy", "Analytics"] # 부가 기술
```

### 3-2. 역할 카테고리 매핑
| 역할 | 카테고리 | 핵심 하네스 |
|-----|---------|----------|
| PM/Product Manager | pm | product-roadmap |
| 마케팅/CMO | marketing | ad-campaign |
| 경영/CEO/COO | strategy | product-roadmap |
| 재무/CFO | finance | financial-model |
| 기술/CTO | tech | technical-writer |
| HR/CHRO | hr | meeting-strategist |

---

## 4. Company Profile 섹션 ★

### 4-1. 필드 정의
```yaml
company_profile:
  company_name: "테크스타트업 Inc."   # 회사명
  business_type: "법인"              # [개인사업자, 법인, 프리랜서, 해당없음]
  registration_number: "123-45-67890" # 사업자번호
  industry: "IT소프트웨어"           # 산업 분류
  industry_code: "6201"              # NAICS 코드
  company_size: "11-50"              # [1인, 2-10, 11-50, 51-200, 200+]
  founded_year: 2015                 # 설립연도
  company_country: "KR"              # 본사 국가
  headquarters: "서울, 강남구"       # 본사 위치
  website: "https://techstartup.com" # 웹사이트
  fiscal_year_end: "12-31"           # 회계년도 말 (MM-DD)
  annual_revenue: "5B~10B"           # 연매출 범위
  primary_product: "SaaS Platform"   # 주 제품
  customer_segment: "SMB"            # [B2B, B2C, B2B2C, Enterprise, SMB]
```

### 4-2. 검증 규칙
- registration_number: 국가별 형식 검증
- industry_code: NAICS/GICS 표준 확인
- company_size: 조직 규모 범주 확정
- fiscal_year_end: MM-DD 형식
- website: URL 형식 + 접근 가능 확인

---

## 5. Preferences 섹션

### 5-1. 필드 정의
```yaml
preferences:
  response_tone: "professional"       # [formal, professional, casual, humorous]
  honorific_style: "존칭"            # [존칭, 반말, 중립]
  persona_name: "MoAI"               # 어시스턴트 호칭
  time_format: "24h"                 # [12h, 24h]
  date_format: "YYYY-MM-DD"          # ISO 8601 기준
  currency: "KRW"                    # 한국 원화 고정
  number_format: "1,000.00"          # 한국식 쉼표 형식
  week_start: "monday"               # 월요일 시작 (ISO)
  response_verbosity: "concise"       # [concise, standard, detailed]
  enable_web_search: true            # 웹 검색 활성화
  auto_save_context: true            # 자동 컨텍스트 저장
```

---

## 6. Context Depth 섹션

### 6-1. 필드 정의
```yaml
context_depth:
  collected_rounds: 3                # 총 수집 라운드
  last_collection_date: "2026-04-04" # 마지막 수집일
  sufficiency_score: 85              # 맥락 충분성 (%)
  a_grade_complete: true             # A등급 완료
  b_grade_percent: 85                # B등급 충족율 (%)
  c_grade_items: ["팀_규모", "트렌드"] # C등급 항목
  evolution_count: 2                 # 자기학습 횟수
  feedback_average: 8.2              # 평가 평균 (0~10)
  harness_usage: {                   # 하네스별 사용
    copywriting: 5,
    email-crafter: 3
  }
```

---

## 7. CRUD 작업

### 7-1. Create (신규 프로필)
```
POST /moai profile --create
  --name="Kim Chul Soo"
  --language="korean"
  --country="KR"
  --role="marketing"
  --industry="IT"

→ /mnt/.auto-memory/moai-profile.md 생성
→ MEMORY.md에 인덱스 추가
```

### 7-2. Read (조회)
```
GET /moai profile
  [--section=user_profile]
  [--format=json|yaml|text]

→ 전체 또는 섹션별 프로필 반환
```

### 7-3. Update (수정)
```
PUT /moai profile --update
  --company_name="NewCorp"
  --industry="금융"
  --company_size="51-200"

→ 해당 필드만 업데이트
→ last_updated 자동 갱신
```

### 7-4. Delete (삭제)
```
DELETE /moai profile --reset

경고: "프로필 삭제 시 모든 커스터마이징이 초기화됩니다."

[1] 확인
[2] 취소
[Other]

→ [1] 선택 시 프로필 초기화
```

---

## 8. MEMORY.md 인덱스 관리

### 8-1. 인덱스 엔트리
```markdown
- [MoAI User Profile (kim@example.com)](moai-profile.md)
  - User: Kim Chul Soo (한국, 마케팅, IT)
  - Company: TechStartup Inc. (법인, 11-50명)
  - Last Updated: 2026-04-04 10:30
  - Sufficiency: 85%
```

### 8-2. 인덱스 동기화
프로필 변경 시 자동 동기화:
```
on_profile_update():
  index_entry = generate_index_from_profile()
  update_memory_index(index_entry)
```

---

## 9. 버전 관리 및 백업

### 9-1. 버전 관리
```yaml
version: "1.0.0"
schema_version: "1.0"
changelog:
  - version: "1.0.0"
    date: "2026-04-04"
    changes: ["초기 생성"]
  - version: "1.0.1"
    date: "2026-04-10"
    changes: ["company_name 업데이트"]
```

### 9-2. 자동 백업
매 업데이트마다:
```
.moai/profile-backups/
├── moai-profile-2026-04-04-v1.yaml
├── moai-profile-2026-04-10-v2.yaml
└── moai-profile-current.yaml
```

---

## 10. 유효성 검증

### 10-1. 스키마 검증
```
validate_profile(profile):
  FOR each section in profile:
    check_required_fields(section)
    check_field_types(section)
    check_constraints(section)
    check_enum_values(section)
  
  IF errors:
    raise ValidationError(errors)
  ELSE:
    return True
```

### 10-2. 일관성 검증
```
validate_consistency():
  IF country != company_country:
    warn("개인 국가와 회사 본사 불일치")
  
  IF experience_level == "entry" but years_experience > 5:
    warn("경력 수준 불일치")
  
  IF industry != company_industry:
    warn("개인 산업과 회사 산업 불일치")
```

---

## 11. 성능 최적화

### 11-1. 캐싱
```
profile_cache = {
  data: load_profile(),
  timestamp: now(),
  ttl: 3600  # 1시간
}

GET_profile():
  IF cache.expired():
    cache.data = reload()
  RETURN cache.data
```

### 11-2. 크기 관리
- 프로필 파일 최대 크기: 50KB
- harness_usage 항목 수 제한: 100개
- changelog 항목 수 제한: 50개 (오래된 것 아카이브)

---

## 12. 마이그레이션

버전 업그레이드 시:
```
migrate_profile(old_version, new_version):
  IF old_version < new_version:
    FOR each migration_step:
      apply_step(profile)
      validate_profile(profile)
  
  update_version_field(new_version)
  save_backup(old_version)
```

