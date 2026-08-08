"""MCP server entry point.

Importing :mod:`moai_mcp_cafe24.tools` populates the endpoint registry from every
category module; :func:`register_all` then compiles each record into a typed
FastMCP tool. ``main`` runs the stdio server.
"""

from __future__ import annotations

from . import tools  # noqa: F401 — import side effect: registry population
from ._app import mcp
from .tools._dispatch import register_all

_TOOLS_REGISTERED = register_all()


def main() -> None:
    """Run the Cafe24 MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
