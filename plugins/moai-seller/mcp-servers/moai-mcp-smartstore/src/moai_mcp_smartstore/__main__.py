"""
uvx 진입점 — `uvx moai-mcp-smartstore` 명령으로 stdio MCP 서버 실행.

--version 플래그로 설치/버전 검증 가능하다.
"""
import argparse

from moai_mcp_smartstore import __version__
from moai_mcp_smartstore.server import mcp


def main() -> None:
    """CLI 진입점. --version 처리 후 MCP stdio 서버 시작."""
    parser = argparse.ArgumentParser(
        description="moai-mcp-smartstore — 네이버 커머스(스마트스토어) 운영/관리 MCP 서버"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"moai-mcp-smartstore {__version__}",
    )
    # MCP 런타임이 사용할 수도 있는 미지정 인수는 무시.
    parser.parse_known_args()

    # stdio 트랜스포트로 MCP 서버 시작.
    mcp.run()


if __name__ == "__main__":
    main()
