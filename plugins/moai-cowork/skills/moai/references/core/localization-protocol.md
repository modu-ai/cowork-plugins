# localization-protocol.md — 로캘 현지화 프로토콜

## 개요
MoAI는 **전세계 모든 국가**를 지원한다. 사용자의 근무 국가를 `/moai init` Phase 1-A Q2에서
입력받아, 웹검색 기반으로 해당 국가의 규제·문화·비즈니스 관행 데이터를 실시간 수집한다.

**핵심 원칙**: 플러그인에 한국(KR) 기본 데이터만 내장하고, 나머지 국가는 웹검색으로 동적 생성한다.

---

## 0. 기존 데이터 재사용 원칙

locale-context.md는 `/mnt/.auto-memory/` (auto-memory)에 저장하여 **세션 간 영구 재사용**한다.
한 번 생성되면 `/moai init` 재실행 시에도 로케일 설문(Q2)을 건너뛰고 기존 데이터를 자동 로딩한다.

```
IF /mnt/.auto-memory/locale-context.md 존재:
  → 로케일 수집 SKIP, 기존 데이터 재사용
  → "기존 로케일 데이터를 재사용합니다." 메시지 출력

IF 존재하지 않음:
  → 아래 1~5 프로세스 정상 진행
```

**수동 갱신**: 사용자가 근무 국가가 변경되었거나 데이터 갱신을 원하면,
`/mnt/.auto-memory/locale-context.md`를 삭제 후 `/moai init`을 재실행한다.

---

## 1. 로케일 결정 흐름

```
사용자 근무 국가 입력 (Phase 1-A Q2)
  │
  ├─ 한국(KR) → references/locale/kr/index.md 로딩 (내장 데이터)
  │
  └─ 그 외 전세계 → 웹검색 기반 실시간 수집
       │
       ├─ cultural-adaptation-guide.md 참조 (수집 항목 템플릿)
       ├─ 웹검색 5개 카테고리 수행
       └─ 결과를 /mnt/.auto-memory/locale-context.md에 저장
```

---

## 2. 로케일 구성 (모든 국가 공통)

```yaml
locale_config:
  country: "{ISO 3166-1 alpha-2}"   # 예: KR, US, JP, DE, VN...
  language: "{ISO 639-1}"           # 예: ko, en, ja, de, vi...
  locale_string: "{lang}_{country}" # 예: ko_KR, en_US
  timezone: "{IANA timezone}"       # 예: Asia/Seoul, America/New_York
  currency: "{ISO 4217}"            # 예: KRW, USD, JPY
  week_start: "{monday|sunday|saturday}"
  number_format: "{1,000.00|1.000,00|1 000,00}"
  date_format: "{YYYY-MM-DD|DD/MM/YYYY|MM/DD/YYYY}"
  time_format: "{12h|24h}"
```

---

## 3. 웹검색 기반 로케일 데이터 수집

### 3-1. 수집 카테고리 (5개)

근무 국가가 한국 외인 경우, 아래 5개 카테고리를 웹검색으로 수집한다:

| # | 카테고리 | 웹검색 쿼리 패턴 | 수집 항목 |
|---|---------|-----------------|----------|
| 1 | 세법 | "{country} tax law basics {year}" | VAT/GST 세율, 소득세 구간, 법인세율, 주요 신고일정 |
| 2 | 노동법 | "{country} labor law employment rules {year}" | 근무시간, 최저임금, 유급휴가, 해고 규정, 사회보험 |
| 3 | 데이터보호법 | "{country} data protection privacy law" | 주요 법률명, 동의 요건, 보관기한, 위반 벌칙 |
| 4 | 비즈니스 관행 | "{country} business culture etiquette" | 호칭, 회의 문화, 관계 형성, 의사결정 방식 |
| 5 | 형식 표준 | "{country} date currency number format standard" | 날짜, 시간, 통화, 숫자, 주소, 전화번호 형식 |

### 3-2. 수집 프로세스

```
FOR each category in [세법, 노동법, 데이터보호법, 비즈니스 관행, 형식 표준]:
  1. 웹검색 실행 (쿼리 = category별 패턴 + 근무 국가 + 현재 연도)
  2. 상위 3-5개 결과에서 핵심 정보 추출
  3. 공식 출처 (정부 사이트, .gov) 우선
  4. 최신 정보 우선 (1년 이내)
  5. 추출 결과를 locale-context.md 형식에 맞춰 저장
```

### 3-3. 결과 저장

```markdown
# locale-context.md (저장 위치: /mnt/.auto-memory/locale-context.md)

## 로케일 기본정보
- country: {country_code}
- language: {language}
- timezone: {timezone}
- currency: {currency}
- date_format: {date_format}

## 세법 요약
{웹검색 수집 결과}

## 노동법 요약
{웹검색 수집 결과}

## 데이터보호법 요약
{웹검색 수집 결과}

## 비즈니스 관행
{웹검색 수집 결과}

## 형식 표준
{웹검색 수집 결과}

---
수집일: {timestamp}
출처: {검색에 사용된 주요 URL 목록}
```

---

## 4. 한국(KR) 내장 데이터

한국은 플러그인에 내장된 `references/locale/kr/index.md`를 사용한다.
이 파일에는 세법, 노동법, 데이터보호법, 비즈니스 관행, 형식 표준이 포함되어 있다.

웹검색이 불가능한 오프라인 환경에서도 한국 로케일은 완전하게 동작한다.

---

## 5. 하네스 실행 시 로케일 적용

### 5-1. 모든 하네스 공통 적용

하네스 실행 시 `/mnt/.auto-memory/locale-context.md`를 로딩하여:

- **화폐 표기**: 해당 국가 통화 기호 + 형식 사용
- **날짜 표기**: 해당 국가 날짜 형식 사용
- **법적 고지**: 해당 국가 규제 반영 (개인정보, 광고 규제 등)
- **비즈니스 톤**: 해당 국가 문화에 맞는 어조와 호칭

### 5-2. 규제 민감 하네스 (법률, 세무, HR 등)

카테고리 8-10의 하네스는 로케일 데이터를 **필수적으로** 참조한다:
- `contract-review`: 해당 국가 계약법 기준
- `accounting-tax`: 해당 국가 세법 기준
- `labor-hr`: 해당 국가 노동법 기준
- `compliance`: 해당 국가 데이터보호법 기준
- `regulatory`: 해당 국가 산업별 규제 기준

### 5-3. 규제 데이터 갱신

```
로케일 데이터 유효기간: 90일 (권장)

갱신 트리거:
1. /moai init 재실행 시 자동 갱신
2. /moai doctor 실행 시 갱신 여부 확인
3. 규제 민감 하네스 실행 시 90일 초과면 갱신 권고
```

---

## 6. 로캘별 페르소나 적응

근무 국가에 따라 MoAI의 페르소나(호칭, 톤)를 자동 조정한다:

```
IF country == "KR": 호칭 = "{이름}님", 톤 = 격식-친근 (존댓말)
IF country == "JP": 호칭 = "{성}さん", 톤 = 정중-격식
IF country in ["US","GB","AU","CA"]: 호칭 = "Hi {이름}!", 톤 = 전문-캐주얼
IF country == "DE": 호칭 = "Herr/Frau {성}", 톤 = 전문
IF country == "FR": 호칭 = "Monsieur/Madame {성}", 톤 = 전문-따뜻
IF country == "BR": 호칭 = "{이름}", 톤 = 캐주얼-친근
IF country == "VN": 호칭 = "Anh/Chị {이름}", 톤 = 정중-친근
IF country == "TH": 호칭 = "คุณ{이름}", 톤 = 정중-따뜻
ELSE: 웹검색으로 해당 국가 비즈니스 호칭/톤 파악 → 적용
```

---

## 7. 다중 로케일 처리

### 7-1. 다국가 조직
```
회사가 다국가 운영 시:
primary_locale: "{개인 근무 국가}"
secondary_locales: ["{회사 본사 국가}", ...]

규칙: 개인 근무 국가 우선, 회사 요구 시 조정
```

### 7-2. 일시적 로케일 전환
```
/moai {harness} --locale=en_US
→ 일시적으로 해당 로케일로 작업
→ 프로젝트 종료 후 원래 로케일 복귀
```

---

## 8. Graceful Degradation

| 상황 | 대응 |
|------|------|
| 웹검색 완전 실패 | 사용자에게 직접 주요 규제/관행 입력 요청 |
| 웹검색 부분 실패 | 수집된 항목만 저장, 누락 항목 명시 |
| 한국(KR) 선택 | 내장 데이터 사용 (웹검색 불필요) |
| 90일 초과 데이터 | 갱신 권고 메시지, 기존 데이터로 계속 동작 |
| 로케일 미설정 | `/moai init` 안내 |
