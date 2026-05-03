# moai-legal 커넥터 가이드

## korean-law (국가법령정보센터 MCP)

법제처 법령 원문, 판례, 행정규칙을 실시간 검색합니다.

### API 키 발급

1. [법제처 Open API](https://open.law.go.kr) 접속
2. 회원가입 후 로그인
3. 마이페이지 > API 인증키 신청
4. 발급된 OC(인증코드) 복사

### 환경변수 설정

```
KOREAN_LAW_OC=발급받은_인증코드
```

### 제공 도구 (14개)

| 도구 | 용도 |
|------|------|
| 법령 검색 | 법령명/키워드로 법률 검색 |
| 법령 조문 | 특정 법률의 조항 전문 조회 |
| 판례 검색 | 대법원/헌법재판소 판례 검색 |
| 행정규칙 | 고시, 훈령, 예규 검색 |
| 법령 연혁 | 법률 개정 이력 추적 |

### 요율 제한

- 일 1,000건 (무료)
- 초과 시 별도 신청 필요

### MCP 서버

korean-law-mcp는 [korean-law-mcp.fly.dev](https://korean-law-mcp.fly.dev)에서 호스팅되는 HTTP MCP 서버입니다. URL 파라미터에 OC를 포함하여 인증합니다.

### 활용 스킬

- `contract-review`: 계약 조항의 법적 근거 확인
- `compliance-check`: 규제 준수 여부의 법령 기반 검증
- `legal-risk`: 관련 판례 조회로 리스크 평가
- `nda-triage`: 영업비밀보호법 관련 조항 확인

---

## 인터넷등기소 (IROS, v2.0.0+)

대법원 인터넷등기소(`iros.go.kr`)에서 법인·부동산 등기부등본을 묶음 단위로 발급할 때 안전한 작업 순서와 로컬 자동화를 보조합니다.

### 사용 측 준비

- **에이전트는 로그인·결제를 직접 수행하지 않습니다** (보안 경계)
- Chrome/Chromium, Python 3.10+, Playwright 설치 가능 환경
- IROS 로그인 수단(아이디·공동인증서·간편인증) — 사용자가 브라우저에서 직접
- TouchEn nxKey 사전 설치 + 결제 카드

### upstream 참고 구현 (사용자 환경에 clone)

```bash
git clone https://github.com/challengekim/iros-registry-automation.git
cd iros-registry-automation
git checkout 7c6924b2ff88d693a12556659188cb91041e5097
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

업스트림 핀(SHA) 변경은 신뢰 경계 변경이므로 새 upstream diff 검토 후 같은 PR에서 갱신합니다.

### 환경변수 (선택)

본 스킬은 환경변수를 요구하지 않습니다. 사용자 입력은 모두 **저장소 밖** 안전 폴더(`mktemp -d`)에 둡니다.

### 활용 스킬

- `iros-registry-automation`: 법인·부동산 등기부등본 일괄 발급 보조
- `legal-risk`: 발급된 등기부등본 기반 법적 리스크 분석
- `compliance-check`: 등기 변경 이력 기반 준수 점검
