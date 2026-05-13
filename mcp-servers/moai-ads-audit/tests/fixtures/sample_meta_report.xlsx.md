# sample_meta_report.xlsx — Fixture 사용법 문서

이 파일은 실제 .xlsx 파일 대신 테스트에서 인메모리 워크북을 생성하는 방법을 문서화합니다.

## 왜 실제 .xlsx 파일을 포함하지 않는가?

- **PIPA 준수** (REQ-AUDIT-MCP-019): 실제 광고 보고서 데이터는 인구통계 정보를 포함하므로 저장소에 포함 금지.
- **테스트 독립성**: 인메모리 워크북 생성으로 파일 시스템 의존성 제거.
- **openpyxl 단독** (HARD 규칙): pandas 의존성 없이 테스트 가능.

## 인메모리 픽스처 생성 패턴

```python
import io
import openpyxl

def make_xlsx_bytes(headers, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(headers)
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()
```

## 12 필수 컬럼 — 한국어 헤더 (SPEC §3.4)

| 표준 키 | 한국어 헤더 | 영어 헤더 |
|---------|------------|---------|
| reporting_starts | 보고 시작 | Reporting starts |
| reporting_ends | 보고 종료 | Reporting ends |
| ad_name | 광고 이름 | Ad name |
| placement | 노출 위치 | Placement |
| age | 연령 | Age |
| gender | 성별 | Gender |
| amount_spent | 지출 금액 | Amount spent |
| link_clicks | 링크 클릭 | Link clicks |
| ctr | CTR | CTR (link CTR) |
| cpc | CPC | CPC |
| purchases | 구매 | Purchases |
| purchase_conversion_value | 구매 전환값 | Purchase conversion value |
| purchase_roas | 구매 ROAS | Purchase ROAS |

## 샘플 데이터 행

```python
SAMPLE_DATA_ROW = [
    "2026-03-01", "2026-03-31", "테스트 광고 001", "Facebook Feed",
    "25-34", "여성", 150000, 300, 2.0,
    500, 15, 450000, 3.0,
]
```

필드 순서: 보고시작 / 보고종료 / 광고이름 / 노출위치 / 연령 / 성별 /
지출금액(₩) / 링크클릭 / CTR(%) / CPC(₩) / 구매수 / 구매전환값(₩) / 구매ROAS

## 정합성 검증 시나리오

| 체크 | 정상 사례 | 오류 사례 |
|------|----------|---------|
| 체크 1: 파일 수 | 1개 | 7개 이상 |
| 체크 2: 지출 합산 | rows 합계 일치 | 파일 간 합계 불일치 |
| 체크 4: 구매수 | ROAS × 지출 = 전환값 | 15% 이상 차이 |
| 체크 6: 통합/분리 | 단일 파일 → integrated | 인구통계 다수 → segmented |
