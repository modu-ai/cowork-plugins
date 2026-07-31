# NOTICE

## moai-smartstore-mcp

네이버 커머스(스마트스토어) 전 도메인 운영/관리 MCP 서버.

### 데이터 출처 및 규격

- **API 규격 출처**: 네이버 커머스 API 센터 공식 문서 및 `llms.txt` 인덱스
  - https://apicenter.commerce.naver.com
  - https://apicenter.commerce.naver.com/llms/llms.txt
  - https://apicenter.commerce.naver.com/docs/auth
- 본 MCP는 네이버 커머스 API 의 **클라이언트 래퍼** 다. API 규격(엔드포인트·파라미터·응답
  스키마)의 저작권은 네이버에 있으며, 본 패키지는 이를 호출하는 도구만 제공한다.
- 인증 전자서명 알고리즘(bcrypt + base64)은 공식 인증 문서의 코드 예시(Python/Java/Node/PHP)를
  Python 표준 라이브러리 + `bcrypt` 패키지로 구현했다.

### 참조 구현 패턴

- MCP 서버 구조(pyproject/manifest/server/tools 레이아웃, FastMCP + uvx 진입점)는
  동일 저장소의 `moai-ads-audit-mcp` 패턴을 준용했다.

### 라이선스

Apache-2.0 (모두의 코워크 저장소 정책 준용).

### 상표

"네이버", "네이버페이", "스마트스토어", "커머스API" 는 NAVER Corp. 의 상표다.
본 패키지는 네이버의 공식 제품이 아니며, 네이버와의 제휴·보증 관계가 없다.
