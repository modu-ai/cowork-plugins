"""Verify generator output: 8 category tools, 136 actions, uniform signature."""

from __future__ import annotations

import asyncio

import moai_mcp_imweb.tools  # noqa: F401  (registers tools)
from moai_mcp_imweb._app import mcp

EXPECTED_TOOLS = 8
EXPECTED_ACTIONS = 136  # 138 operations minus 2 OAuth2 (authorize/token) handled internally


def _list():
    return asyncio.run(mcp.list_tools())


def _enum_values(prop: dict) -> list:
    if "enum" in prop:
        return prop["enum"]
    if "const" in prop:  # Pydantic serialises a single-value Literal as `const`
        return [prop["const"]]
    for branch in prop.get("anyOf", []):
        if "enum" in branch:
            return branch["enum"]
        if "const" in branch:
            return [branch["const"]]
    return []


def test_tool_count():
    assert len(_list()) == EXPECTED_TOOLS


def test_total_actions():
    total = sum(len(_enum_values(t.inputSchema["properties"]["action"])) for t in _list())
    assert total == EXPECTED_ACTIONS


def test_uniform_signature():
    for t in _list():
        props = t.inputSchema["properties"]
        assert {"action", "params", "body", "paginate"} <= set(props), t.name
        assert t.inputSchema["properties"]["paginate"]["default"] is False


def test_no_oauth_tools():
    assert all(not t.name.startswith("imweb_oauth") for t in _list())


def test_every_tool_has_actions_and_description():
    for t in _list():
        assert t.description, f"{t.name} missing description"
        assert len(_enum_values(t.inputSchema["properties"]["action"])) >= 1, t.name
