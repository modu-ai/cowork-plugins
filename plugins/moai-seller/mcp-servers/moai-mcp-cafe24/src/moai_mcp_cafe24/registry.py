"""Declarative endpoint registry — the single source of truth for all tools.

Instead of hand-writing one function per Cafe24 endpoint (300+), each endpoint
is described as an :class:`Endpoint` data record. The dispatcher
(:mod:`moai_mcp_cafe24.tools._dispatch`) compiles every record into a fully-typed
FastMCP tool at startup.

Why declarative:
  * keeps the 300+ surface area auditable against the official docs (one row per
    documented operation)
  * uniform error handling, auth, pagination, and envelope unwrapping
  * adding an endpoint = appending one record, not writing a function

Schema notes:
  * ``path`` may contain ``{name}`` placeholders; those names become required
    tool arguments (stringified at request time).
  * ``query_params`` become optional typed arguments.
  * ``takes_body`` endpoints expose a ``body: dict`` argument; the dispatcher
    wraps it as ``{body_key: body}`` (default ``body_key = resource_key``).
  * ``list_endpoint`` endpoints additionally expose ``paginate`` / ``max_pages``
    to opt into transparent offset pagination.
  * Every tool auto-exposes an optional ``shop_no`` argument; when supplied it
    is merged into query params (GET/DELETE) or the request body (POST/PUT),
    matching Cafe24's universal ``shop_no`` semantics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Param:
    """A query/path parameter declaration."""

    name: str
    type: str = "str"  # "str" | "int" | "float" | "bool"
    required: bool = False
    description: str = ""
    default: Optional[object] = None


@dataclass(frozen=True)
class Endpoint:
    """One Cafe24 API operation → one MCP tool."""

    name: str  # unique tool name, e.g. "cafe24_product_list"
    category: str  # logical group, e.g. "product"
    method: str  # GET | POST | PUT | DELETE
    path: str  # e.g. "/api/v2/admin/products/{product_no}/variants"
    surface: str = "admin"  # "admin" | "analytics"
    summary: str = ""  # one-line summary (Korean or English per docs)
    description: str = ""  # longer description
    scope: str = ""  # e.g. "mall.read_product"
    resource_key: str = ""  # response wrapper key (singular), e.g. "product"
    body_key: Optional[str] = "resource_key"  # request wrapper; "resource_key"=inherit, None=raw
    takes_body: bool = False  # POST/PUT accept a body dict
    list_endpoint: bool = False  # advertises offset/limit pagination
    query_params: tuple[Param, ...] = field(default_factory=tuple)
    notes: str = ""  # caveats (cursor limits, specific-client-only, etc.)

    def __post_init__(self) -> None:
        # Coerce a stray bare Param (missing trailing comma in a 1-tuple) to a
        # tuple. Catches the classic ``query_params=(Param(...))`` slip before it
        # surfaces as a confusing "Param is not iterable" at signature-build time.
        qp = self.query_params
        if isinstance(qp, Param):
            object.__setattr__(self, "query_params", (qp,))
        elif not isinstance(qp, tuple):
            object.__setattr__(self, "query_params", tuple(qp))

    @property
    def path_param_names(self) -> tuple[str, ...]:
        """Auto-detect ``{name}`` placeholders from the path."""
        out: list[str] = []
        for seg in self.path.split("/"):
            if seg.startswith("{") and seg.endswith("}"):
                out.append(seg[1:-1])
        return tuple(out)

    @property
    def resolved_body_key(self) -> Optional[str]:
        if self.body_key is None:
            return None
        if self.body_key == "resource_key":
            return self.resource_key or None
        return self.body_key


class Registry:
    """Append-only registry of endpoints."""

    def __init__(self) -> None:
        self._endpoints: list[Endpoint] = []
        self._names: set[str] = set()

    def add(self, ep: Endpoint) -> None:
        if ep.name in self._names:
            raise ValueError(f"Duplicate tool name in registry: {ep.name}")
        self._names.add(ep.name)
        self._endpoints.append(ep)

    def extend(self, eps: "Registry | list[Endpoint] | tuple[Endpoint, ...]") -> None:
        items = eps._endpoints if isinstance(eps, Registry) else list(eps)
        for ep in items:
            self.add(ep)

    def all(self) -> list[Endpoint]:
        return list(self._endpoints)

    def by_category(self) -> dict[str, list[Endpoint]]:
        out: dict[str, list[Endpoint]] = {}
        for ep in self._endpoints:
            out.setdefault(ep.category, []).append(ep)
        return out

    def __len__(self) -> int:
        return len(self._endpoints)


# Process-wide registry populated by ``tools.*`` modules at import time.
REGISTRY = Registry()


def register(*endpoints: Endpoint) -> None:
    """Module-level convenience: REGISTRY.register(*endpoints)."""
    for ep in endpoints:
        REGISTRY.add(ep)
