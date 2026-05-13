"""
uvx 진입점 — `uvx moai-ads-audit-mcp` 명령으로 stdio 실행.
REQ-AUDIT-MCP-001: uvx moai-ads-audit-mcp --version 정상 응답 가능.
"""
import argparse
import sys

from moai_ads_audit import __version__
from moai_ads_audit.server import mcp


def main() -> None:
    """CLI 진입점. --version 플래그 처리 후 MCP stdio 서버 시작."""
    # --version 플래그 처리 (REQ-AUDIT-MCP-001 검증 명령)
    parser = argparse.ArgumentParser(
        description="moai-ads-audit-mcp — Meta 광고 audit 전담 MCP 서버"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"moai-ads-audit-mcp {__version__}",
    )
    # 알 수 없는 인수는 MCP 런타임이 처리하도록 무시
    parser.parse_known_args()

    # stdio 트랜스포트로 MCP 서버 시작
    mcp.run()


if __name__ == "__main__":
    main()
