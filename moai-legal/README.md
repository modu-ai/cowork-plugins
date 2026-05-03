# moai-legal

법률 플러그인 — 계약서 검토(민법/상법), 개인정보보호법 컴플라이언스, NDA, 지적재산권.

> **주의**: AI 보조 법률 분석 도구입니다. 중요한 법적 결정은 반드시 법률 전문가와 상담하십시오.

국가법령정보센터 MCP 연동으로 법령 원문과 판례를 실시간으로 검색하며, 2026년 개정 법률을 반영합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [contract-review](./skills/contract-review/) | 민법/상법 기반 10대 리스크 패턴 분석, 이용약관, 개인정보처리방침, SLA | 3 | ✅ |
| [compliance-check](./skills/compliance-check/) | 규제 준수 갭 분석, ESG 보고, 내부 감사, 인허가 서류 | 4 | ✅ |
| [legal-risk](./skills/legal-risk/) | 판례/법령 리서치, 특허/상표/저작권 IP 포트폴리오, 법령 변화 영향 분석 | 2 | ✅ |
| [nda-triage](./skills/nda-triage/) | 비밀유지계약서 신속 검토, 영업비밀보호법 기준 위험도 평가, 수정 권고 | 0 | ✅ |
| [iros-registry-automation](./skills/iros-registry-automation/) | 인터넷등기소(IROS) 법인·부동산 등기부등본 일괄 발급 보조. 로그인·결제 사용자 직접, 장바구니·열람·저장 자동화 (v2.0.0+) | 0 | ✅ |

## MCP 커넥터

| 서버 | 용도 |
|------|------|
| korean-law | 국가법령정보센터 — 법령 원문 및 판례 실시간 검색 (`KOREAN_LAW_OC` 필요) |

## 사용 예시

```
아래 용역 계약서에서 위험 조항 찾아줘. 특히 손해배상 범위와 IP 귀속 조항 확인해줘.
```

```
개인정보보호법 기준으로 우리 서비스 개인정보처리방침 검토해줘
```

```
이 NDA 검토해줘. 비밀유지 기간이랑 위약금 조항 위주로.
```

## 주요 워크플로우 체인

```
NDA 일괄 검토
  nda-triage(분류·위험도) → contract-review(조항별 정밀 검토) → legal-risk(IP 영향) → docx-generator → ai-slop-reviewer

이용약관·개인정보처리방침 작성
  contract-review(조항 설계) → compliance-check(개인정보보호법) → docx-generator → ai-slop-reviewer

기업 컴플라이언스 감사
  compliance-check(규제 갭 분석) → docx-generator(감사 보고서) → ai-slop-reviewer

특허 출원 전 FTO 분석
  legal-risk(특허/상표 검토) → moai-research/patent-search(선행기술 조사) → docx-generator
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| B2B 영업 제안서(고객사 대상) | `moai-sales/proposal-writer` |
| 특허 검색·분석(KIPRIS) | `moai-research/patent-search` |
| 근로계약서 작성(노무 관점) | `moai-hr/draft-offer` |
| 정부 입찰 약관 | `moai-operations/process-manager` |

## 한국 법률 환경 특화

- **국가법령정보센터 MCP**: 법령 원문·판례 실시간 검색 (`KOREAN_LAW_OC` 필요)
- **민법·상법 10대 리스크 패턴**: 손해배상 캡, 해지권, IP 귀속, 손해배상 한도 등
- **개인정보보호법(PIPA)·정보통신망법** 기준 적용
- **영업비밀보호법 §2** (비밀관리성·경제성·비공지성) NDA 검토 자동 적용
- **2026년 개정**: AI 기본법, 디지털 자산 기본법 반영

## 설치

Settings > Plugins > cowork-plugins에서 `moai-legal` 선택

## 참고자료

| 항목 | URL | 용도 |
|------|-----|------|
| [korean-law-mcp](https://korean-law-mcp.fly.dev/) | MCP 서버 | 법령/판례 검색 |
| [국가법령정보센터](https://www.law.go.kr/) | 공식 | 법령/판례 원문 |
