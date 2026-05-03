# moai-commerce 커넥터 가이드

## MFDS (식품의약품안전처) — k-skill-proxy 경유, v2.0.0+

식약처 의약품·식품 안전 공식 OpenAPI를 NomaDamas의 hosted 프록시(`k-skill-proxy.nomadamas.org`) 경유로 조회합니다. 헬스/F&B 커머스 상품의 안전성 확인, 회수·부적합 이력 점검에 활용합니다.

### 사용 측 준비

- **사용자 측 시크릿 불필요** (프록시가 키를 보유)
- 인터넷 연결만 있으면 동작

### 환경변수 (선택)

```
KSKILL_PROXY_BASE_URL=https://k-skill-proxy.nomadamas.org   # 기본값. self-host 시 변경
```

### Self-host 시 추가 설정 (운영 측)

```
DATA_GO_KR_API_KEY=공공데이터포털_키        # 의약품 + 부적합 식품
FOODSAFETYKOREA_API_KEY=식품안전나라_키      # 건강기능식품 + 회수 live
```

발급:

- 공공데이터포털: [data.go.kr](https://www.data.go.kr) 회원가입 → 활용신청 → 자동승인
- 식품안전나라: [foodsafetykorea.go.kr](https://www.foodsafetykorea.go.kr) 회원가입 → OpenAPI 이용신청. 키 1개로 I-0040, I-0050, I0030, I0490, I2620 모두 사용

`FOODSAFETYKOREA_API_KEY`가 없으면 sample feed로 fallback 가능.

### 제공 데이터

| 카테고리 | 정보 |
|---|---|
| 의약품 | e약은요 (효능·사용법·주의사항·상호작용) + 안전상비의약품 |
| 건강기능식품 | 기능성 원료 인정현황 (I-0040), 개별인정형 (I-0050), 품목제조 신고 (I0030) |
| 검사부적합 | 국내 검사부적합 (I2620), 부적합 식품 |
| 회수·판매중지 | 식품안전나라 (I0490) |

### 활용 스킬

- `mfds-safety`: 의약품·식품 통합 안전 체크 (red flag 인터뷰 우선)
- `commerce-strategy`: 헬스/F&B 신상품 기획 시 안전성 검토
- `detail-page-copy`: 안전 정보 반영한 상세페이지 카피
- `marketplace-coupang`/`marketplace-naver`: 헬스/F&B 카테고리 상품 등록 시 안전성 검증

### Red Flag 정책 (HARD)

`mfds-safety` 스킬은 사용자가 증상·복용/섭취 상황을 말하면 **반드시 인터뷰로 먼저 되묻고**, red flag(`호흡곤란`, `의식저하`, `혈변`, `심한 탈수`, `심한 발진` 등)가 발견되면 API 조회보다 **즉시 119·응급실·의료진 안내**가 우선합니다. 진단·처방·복용 지시는 하지 않습니다.
