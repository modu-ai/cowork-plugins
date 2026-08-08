#!/usr/bin/env python3
# (c) moai-imweb — OpenAPI → FastMCP category-dispatch tool generator.
# DO NOT EDIT the generated tools/*.py by hand; re-run this generator instead.
#
# Design (B안 — category dispatch + typed body union): one MCP tool per OpenAPI tag.
#   imweb_<tag>(action: Literal[...], params=None, body=Union[<Action>Body,...]|None, paginate=False)
#
# Each `action` is a snake_cased operation key unique within its tag; the tool resolves
# the (method, path, path-params, query-params, has-body) tuple from a generated `_OPS`
# table and delegates to ImwebClient.
#
# Body typing rationale: Claude Code truncates a tool's DESCRIPTION and the server's
# INSTRUCTIONS at 2KB each, but it does NOT truncate the inputSchema. Earlier revisions
# packed the full action list + every body schema into the docstring, which blew past
# 2KB (order reached ~18KB → ~89% of actions invisible). This generator instead emits a
# per-action Pydantic model for every operation that has a request body and unions them
# into a single `Body` type. The inputSchema then carries the complete body structure
# (with exact per-action required fields) to the model untruncated, while the docstring
# stays short.
#
# Source of truth: tools/openapi.json
from __future__ import annotations

import json
import keyword
import re
from collections import defaultdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent  # mcp-servers/moai-mcp-imweb/tools/
ROOT = TOOLS_DIR.parent  # mcp-servers/moai-mcp-imweb/
SPEC_FILE = TOOLS_DIR / "openapi.json"
OUT_DIR = ROOT / "src" / "moai_mcp_imweb" / "tools"

# (OpenAPI tag, module slug, tool name, Korean label). Order = file emit order.
CATS = [
    ("Site-Info", "site_info", "imweb_site_info", "사이트 정보"),
    ("Member-Info", "member_info", "imweb_member_info", "회원 정보"),
    ("Community", "community", "imweb_community", "커뮤니티 (폼/Q&A/구매평)"),
    ("Promotion", "promotion", "imweb_promotion", "프로모션 (적립금/쿠폰)"),
    ("Product", "product", "imweb_product", "상품"),
    ("Order", "order", "imweb_order", "주문"),
    ("Script", "script", "imweb_script", "스크립트"),
    ("Payment", "payment", "imweb_payment", "결제"),
]
methods = ("get", "post", "patch", "put", "delete")

# OpenAPI (JSON Schema) primitive -> Python annotation.
PY_TYPE = {
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "string": "str",
    "array": "list",
    "object": "dict",
    "file": "str",
}


def load_spec():
    return json.loads(SPEC_FILE.read_text("utf-8"))


def split_ctrl(op_id: str) -> str:
    m = re.match(r"^[A-Za-z0-9]+Controller_(.+)$", op_id)
    return m.group(1) if m else op_id


def camel_to_snake(s: str) -> str:
    s = re.sub(r"(?<!^)(?=[A-Z][a-z])", "_", s)
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", s)
    return re.sub(r"_+", "_", s).lower().strip("_")


def resolve_ref(spec, sch):
    """Follow a single $ref; return the resolved schema dict (or sch unchanged)."""
    if isinstance(sch, dict) and "$ref" in sch:
        name = sch["$ref"].split("/")[-1]
        return spec.get("components", {}).get("schemas", {}).get(name) or sch
    return sch


def body_field_type(ps) -> str:
    """Map an OpenAPI property schema to a Python type annotation string."""
    if not isinstance(ps, dict) or not ps:
        return "str"
    if "$ref" in ps:
        return "dict"
    t = ps.get("type")
    if t == "array":
        inner = ps.get("items", {})
        return f"list[{body_field_type(inner)}]"
    if t == "object":
        return "dict"
    return PY_TYPE.get(t, "str")


def collect_body(spec, op) -> list[tuple[str, str, bool, str]]:
    """Return ordered (field_name, py_type, required, description) for an op's body, or []."""
    rb = op.get("requestBody")
    if not rb:
        return []
    content = rb.get("content", {})
    app = content.get("application/json") or content.get("multipart/form-data")
    if not app:
        return []
    sch = resolve_ref(spec, app.get("schema", {}) or {})
    if not isinstance(sch, dict):
        return []
    props = sch.get("properties") or {}
    req = sch.get("required") or []
    out = []
    for pn, ps in props.items():
        t = body_field_type(ps)
        desc = (ps.get("description") or "").strip().replace("\n", " ")
        out.append((pn, t, pn in req, desc))
    return out


def collect(spec):
    by_cat = defaultdict(list)
    for path, item in spec.get("paths", {}).items():
        if not isinstance(item, dict):
            continue
        for m in methods:
            if m in item:
                op = item[m]
                tag = (op.get("tags") or ["Untagged"])[0]
                if tag == "OAuth2.0":
                    continue  # authorize/token handled internally (env + auth.py)
                op_id = op.get("operationId") or f"{m}_{path}"
                action = camel_to_snake(split_ctrl(op_id))
                pparams = [p["name"] for p in op.get("parameters", []) if p.get("in") == "path"]
                qparams = [p["name"] for p in op.get("parameters", []) if p.get("in") == "query"]
                has_body = bool(op.get("requestBody"))
                summary = (op.get("summary") or "").strip() or f"{m.upper()} {path}"
                body_fields = collect_body(spec, op) if has_body else []
                by_cat[tag].append({
                    "action": action,
                    "method": m.upper(),
                    "path": path,
                    "pparams": pparams,
                    "qparams": qparams,
                    "has_body": has_body,
                    "summary": summary,
                    "body_fields": body_fields,
                })
    return by_cat


def model_name(action: str) -> str:
    """create_order_invoice -> CreateOrderInvoiceBody"""
    return "".join(p.capitalize() for p in action.split("_") if p) + "Body"


def safe_attr(name: str) -> tuple[str, str | None]:
    """Return (python_attr, alias_or_None). alias is set when attr != original name."""
    if name.isidentifier() and not name.startswith("model_") and not keyword.iskeyword(name):
        return name, None
    s = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if not s or s[0].isdigit():
        s = "f_" + s
    if s.startswith("model_") or keyword.iskeyword(s):
        s = "f_" + s
    return s, name


def render_body_field(pn, t, required, d):
    attr, alias = safe_attr(pn)
    ann = t if required else f"{t} | None"
    default = "..." if required else "None"
    d2 = (d[:160] + "…") if len(d) > 160 else d
    parts = [default]
    if alias:
        parts.append(f"alias={alias!r}")
    if d2:
        parts.append(f"description={d2!r}")
    return f"    {attr}: {ann} = Field({', '.join(parts)})"


def render_module(tag, slug, tool_name, label, ops):
    out = []
    out.append(f'"""Generated tools — {tag} ({label}). DO NOT EDIT; regenerate via tools/_generator.py."""')
    out.append("from __future__ import annotations")
    out.append("")

    body_ops = [o for o in ops if o["body_fields"]]
    if body_ops:
        out.append("from typing import Literal, Union")
        out.append("")
        out.append("from pydantic import BaseModel, ConfigDict, Field")
    else:
        out.append("from typing import Literal")
    out.append("")
    out.append("from .._app import mcp")
    out.append("from .._base import get_client")
    out.append("")

    # _OPS table — action -> (method, path, [path_params], [query_params], has_body)
    out.append("# action -> (method, path, path_params, query_params, has_body)")
    out.append("_OPS: dict[str, tuple] = {")
    for o in ops:
        out.append(
            f'    {o["action"]!r}: ({o["method"]!r}, {o["path"]!r}, {o["pparams"]!r}, {o["qparams"]!r}, {o["has_body"]!r}),'
        )
    out.append("}")
    out.append("")

    # per-action Body models (exact required fields each) + union
    if body_ops:
        for o in body_ops:
            out.append("")
            mn = model_name(o["action"])
            out.append(f"class {mn}(BaseModel):")
            req_fields = [f[0] for f in o["body_fields"] if f[2]]
            doc = f'    """요청 본문 (action={o["action"]!r} [{o["method"]} {o["path"]}]).'
            if req_fields:
                doc += f' 필수 필드: {", ".join(req_fields)}.'
            doc += '"""'
            out.append(doc)
            out.append('    model_config = ConfigDict(extra="allow", populate_by_name=True)')
            for (pn, t, required, d) in o["body_fields"]:
                out.append(render_body_field(pn, t, required, d))
            out.append("")
        model_names = [model_name(o["action"]) for o in body_ops]
        if len(model_names) == 1:
            out.append(f"Body = {model_names[0]}")
        else:
            out.append("Body = Union[" + ", ".join(model_names) + "]")
        out.append("")

    actions = [o["action"] for o in ops]
    literal = "Literal[" + ", ".join(f'"{a}"' for a in actions) + "]"

    # concise docstring — well under the 2KB truncate ceiling
    doc = [
        f"{label} 도구 — {len(ops)}개 action 을 디스패치합니다.",
        "",
        "Args:",
        f"    action: 수행 작업 키 (inputSchema enum 으로 {len(ops)}개 전체 공개).",
        '    params: path + query 파라미터 딕셔너리. 예: {"orderNo": "ORD123", "page": 1}.',
    ]
    if body_ops:
        doc.append(
            "    body: POST/PATCH/PUT 본문. action 별 Body 모델(inputSchema anyOf) 중 "
            "해당 action 의 필드만 채움 (모델명 = action 의 PascalCase + Body)."
        )
        body_param_ann = "Body | None"
    else:
        doc.append("    body: 미사용 (본문이 있는 action 없음).")
        body_param_ann = "dict | None"
    doc.append("    paginate: list 계열 GET 에서 전체 페이지 자동 집계 (기본 False = 단일 페이지).")
    doc.append("")
    doc.append("Returns: API JSON.")
    docstring = "\n".join(doc)

    out.append("@mcp.tool()")
    out.append(
        f"def {tool_name}(action: {literal}, params: dict | None = None, "
        f"body: {body_param_ann} = None, paginate: bool = False) -> dict:"
    )
    out.append('    r"""' + docstring + '"""')
    out.append("    _method, _path, _pp, _qp, _has_body = _OPS[action]")
    out.append("    _params = params or {}")
    out.append("    _pp_val = {k: _params[k] for k in _pp if k in _params}")
    out.append("    _qp_val = {k: _params[k] for k in _qp if k in _params}")
    out.append("    _client = get_client()")
    out.append('    if paginate and _method == "GET":')
    out.append("        return _client.list_all_pages(_path, params=_qp_val or None)")
    out.append("    _kw = {}")
    out.append('    if _pp_val:\n        _kw["path_params"] = _pp_val')
    out.append('    if _qp_val:\n        _kw["params"] = _qp_val')
    out.append("    if _has_body:")
    if body_ops:
        out.append("        _bd = body.model_dump(exclude_none=True, by_alias=True) if body else {}")
    else:
        out.append("        _bd = body or {}")
    out.append('        _kw["json_body"] = _bd')
    out.append("    return _client.request(_method, _path, **_kw)")
    out.append("")
    return "\n".join(out)


def main():
    spec = load_spec()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_cat = collect(spec)

    # action uniqueness within a tag
    collisions = []
    for tag, ops in by_cat.items():
        seen = set()
        for o in ops:
            if o["action"] in seen:
                collisions.append((tag, o["action"]))
            seen.add(o["action"])

    slugs = []
    total = 0
    for tag, slug, tool_name, label in CATS:
        ops = by_cat.get(tag, [])
        if not ops:
            continue
        slugs.append(slug)
        src = render_module(tag, slug, tool_name, label, ops)
        (OUT_DIR / f"{slug}.py").write_text(src + "\n", "utf-8")
        total += len(ops)

    # __init__.py imports every module so decorators register.
    init = ['"""Generated tools package — importing it registers all Imweb category tools."""']
    init.append("from __future__ import annotations")
    init.append("")
    for slug in slugs:
        init.append(f"from . import {slug}  # noqa: F401")
    init.append("")
    init.append("__all__ = [" + ", ".join(f'"{s}"' for s in slugs) + "]")
    (OUT_DIR / "__init__.py").write_text("\n".join(init) + "\n", "utf-8")

    # Per-category report
    print(f"generated {len(slugs)} category tools covering {total} actions")
    for tag, slug, _, label in CATS:
        n = len(by_cat.get(tag, []))
        if n:
            print(f"  {slug:12s} ({label}): imweb_{slug}({n} actions)")
    if collisions:
        print("ACTION COLLISIONS:", collisions)
    else:
        print("action keys unique per tag: OK")


if __name__ == "__main__":
    main()
