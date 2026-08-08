"""
moai-mcp-smartstore — 네이버 커머스(스마트스토어) 전 도메인 운영/관리 MCP 서버.

네이버 커머스 API 센터(https://apicenter.commerce.naver.com)의 공식 API 를
MCP(Model Context Protocol) 도구로 노출하여, Cowork/Claude Code 환경에서
스마트스토어 상품·주문·정산·문의·물류·판매자정보·커머스솔루션·통계 운영을
자연어로 수행할 수 있게 한다.

인증은 OAuth2 Client Credentials Grant + bcrypt 전자서명 방식. 자격증명은
반드시 환경변수로만 주입한다 (CONNECTORS.md 참고).
"""
__version__ = "0.1.0"
