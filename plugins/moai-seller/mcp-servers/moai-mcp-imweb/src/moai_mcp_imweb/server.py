"""moai-imweb MCP server — entry point.

Importing :mod:`moai_mcp_imweb.tools` triggers decorator-based registration of all
138 generated tools onto the shared :data:`moai_mcp_imweb._app.mcp` instance. This
module then runs the server over stdio (the transport Claude Code expects for a
``command:`` MCP server).
"""

from __future__ import annotations

from . import tools  # noqa: F401  (side effect: registers every @mcp.tool)
from ._app import mcp


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
