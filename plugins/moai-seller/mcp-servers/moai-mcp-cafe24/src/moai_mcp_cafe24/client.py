"""Cafe24 HTTP client — shared by every registry-driven tool.

Responsibilities:
  * route each call to the correct surface (Admin vs Analytics base host)
  * inject ``Authorization: Bearer`` + ``X-Cafe24-Api-Version`` headers
  * on ``401`` (token expired), refresh once and retry (persisting the ROTATED
    refresh token — Cafe24 invalidates the old one)
  * respect an optional inter-request delay (``CAFE24_REQUEST_DELAY``)
  * honour the dual rate-limit: on ``429`` (or usage headers >= 100%), back off
    with capped exponential sleep, preferring the ``X-Cafe24-Call-Remain`` /
    ``X-Cafe24-Time-Remain`` hint (seconds) when present
  * translate non-2xx Cafe24 error envelopes (``{"error": {"code","message"}}``)
    into :class:`Cafe24ApiError`
  * unwrap Cafe24 response envelopes and expose :meth:`list_paginated` for
    transparent offset/limit pagination when a list endpoint advertises it

The client is a thin transport; all domain logic lives in the registry/dispatch.
"""

from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING, Any, Mapping, Optional

import httpx

from .auth import refresh_access_token

if TYPE_CHECKING:
    from ._base import Cafe24Config

# Surfaces — which base host + whether paths carry the /api/v2/admin prefix.
SURFACE_ADMIN = "admin"
SURFACE_ANALYTICS = "analytics"

_MAX_429_RETRIES = 4  # -> up to 5 attempts total (1 + 4 backoffs)


class Cafe24ApiError(RuntimeError):
    """Raised on a non-2xx response. Carries status, code, message, raw body."""

    def __init__(self, status: int, code: Optional[str], message: str, body: Any, url: str):
        self.status = status
        self.code = code
        self.message = message
        self.body = body
        self.url = url
        super().__init__(f"Cafe24 API 오류 (HTTP {status}) [{code}] {message}  @ {url}")


class Cafe24Client:
    def __init__(self, config: "Cafe24Config"):
        from ._base import _persist_tokens

        self._config = config
        self._persist = _persist_tokens
        self._access = config.access_token
        self._refresh = config.refresh_token
        # Single httpx client; full URLs are built per call from the surface base.
        self._http = httpx.Client(timeout=config.timeout)
        self._last_request_ts = 0.0

    # ------------------------------------------------------------------ core
    def _delay(self) -> None:
        if self._config.request_delay <= 0:
            return
        elapsed = time.monotonic() - self._last_request_ts
        remaining = self._config.request_delay - elapsed
        if remaining > 0:
            time.sleep(remaining)
        self._last_request_ts = time.monotonic()

    def _base_url(self, surface: str) -> str:
        if surface == SURFACE_ANALYTICS:
            return self._config.analytics_base
        return self._config.admin_base

    def _headers(self, with_body: bool) -> dict[str, str]:
        h: dict[str, str] = {
            "Accept": "application/json",
            "X-Cafe24-Api-Version": self._config.api_version,
            # Cafe24 requires client_id on every Admin API call when using an
            # access token issued by an app; harmless on Analytics.
            "X-Cafe24-Client-Id": self._config.client_id,
        }
        if with_body:
            h["Content-Type"] = "application/json"
        if self._access:
            h["Authorization"] = f"Bearer {self._access}"
        return h

    def _do_refresh(self) -> None:
        pair = refresh_access_token(self._config, client=self._http)
        self._access = pair.access_token
        self._refresh = pair.refresh_token
        from dataclasses import replace

        new_cfg = replace(self._config, access_token=self._access, refresh_token=self._refresh)
        self._config = new_cfg
        # Persist the ROTATED refresh token — the old one is now dead.
        self._persist(new_cfg.token_file, self._access, self._refresh)

    def _backoff(self, attempt: int, hint_seconds: Optional[float]) -> None:
        # Exponential backoff with jitter, capped at 30s. Prefer the server hint.
        if hint_seconds and hint_seconds > 0:
            sleep = min(float(hint_seconds), 30.0)
        else:
            base = min(2 ** attempt, 16)
            sleep = base + random.uniform(0, 1)
        time.sleep(sleep)

    def request(
        self,
        method: str,
        path: str,
        *,
        surface: str = SURFACE_ADMIN,
        path_params: Optional[Mapping[str, Any]] = None,
        params: Optional[Mapping[str, Any]] = None,
        json_body: Any = None,
        retry_on_401: bool = True,
        _attempt: int = 0,
    ) -> Any:
        """Perform a single API call. Returns parsed JSON (or raw text on non-JSON)."""
        if path_params:
            path = path.format(**{k: _path_val(v) for k, v in path_params.items()})
        clean_params = _drop_none(params)
        url = f"{self._base_url(surface)}{path}"

        self._delay()
        resp = self._http.request(
            method.upper(),
            url,
            params=clean_params,
            json=json_body,
            headers=self._headers(with_body=json_body is not None),
        )

        # 401 → refresh once, retry once.
        if resp.status_code == 401 and retry_on_401 and self._config.can_refresh:
            self._do_refresh()
            return self.request(
                method, path, surface=surface, path_params=None, params=params,
                json_body=json_body, retry_on_401=False, _attempt=_attempt,
            )

        # 429 → backoff + retry (honour X-Cafe24-*-Remain hint).
        if resp.status_code == 429 and _attempt < _MAX_429_RETRIES:
            self._backoff(_attempt, _usage_remain_hint(resp))
            return self.request(
                method, path, surface=surface, path_params=None, params=params,
                json_body=json_body, retry_on_401=retry_on_401, _attempt=_attempt + 1,
            )

        if resp.status_code >= 400:
            body = _safe_json(resp)
            code, message = _extract_cafe24_error(body, resp.text)
            raise Cafe24ApiError(resp.status_code, code, message, body, str(resp.url))

        return _return_body(resp)

    # ------------------------------------------------------------ pagination
    def list_paginated(
        self,
        path: str,
        *,
        surface: str = SURFACE_ADMIN,
        params: Optional[Mapping[str, Any]] = None,
        page_size: int = 100,
        max_pages: int = 50,
        list_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """Follow ``offset``/``limit`` pagination, concatenating the list rows.

        Stops at the first page whose returned list is shorter than ``page_size``
        (heuristic end-of-data) or at ``max_pages``. ``list_key`` is auto-detected
        from the response when omitted (Cafe24 lists are keyed by the plural
        resource name, e.g. ``"products"``). Returns a dict with the aggregated
        list plus pagination metadata.

        Note: some Cafe24 endpoints cap ``offset`` (e.g. products at 5000,
        orders at 15000) and require a cursor param (``since_product_no`` etc.)
        to enumerate beyond. For those, prefer the single-page tool with the
        cursor param rather than this auto-paginator.
        """
        aggregated: list[Any] = []
        base = dict(_drop_none(params) or {})
        meta: dict[str, Any] = {"page_size": page_size, "pages_fetched": 0}
        last_data: Any = {}
        for page in range(max_pages):
            offset = page * page_size
            p = {**base, "limit": page_size, "offset": offset}
            last_data = self.request("GET", path, surface=surface, params=p)
            rows, detected_key = _extract_rows(last_data, list_key)
            if list_key is None and detected_key:
                list_key = detected_key
            aggregated.extend(rows)
            meta["pages_fetched"] = page + 1
            if len(rows) < page_size:
                break
        meta["total_returned"] = len(aggregated)
        meta["truncated"] = meta["pages_fetched"] >= max_pages
        out: dict[str, Any] = {list_key or "list": aggregated, "pagination": meta}
        # Carry through any non-list siblings (e.g. "meta") from the last page.
        if isinstance(last_data, dict):
            for k, v in last_data.items():
                if k != (list_key or "list") and k != "pagination":
                    out.setdefault(k, v)
        return out

    def close(self) -> None:
        self._http.close()

    @property
    def config(self) -> "Cafe24Config":
        """Current config (tokens may rotate after refresh)."""
        return self._config


# ---------------------------------------------------------------- helpers
def _path_val(v: Any) -> str:
    if isinstance(v, bool):
        return "T" if v else "F"
    return str(v)


def _drop_none(m: Optional[Mapping[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if not m:
        return out
    for k, v in m.items():
        if v is None:
            continue
        if isinstance(v, bool):
            out[k] = "T" if v else "F"  # Cafe24 uses T/F enums widely
        elif isinstance(v, (list, tuple)):
            out[k] = ",".join(_path_val(x) for x in v)  # Cafe24 supports comma OR lists
        else:
            out[k] = v
    return out


def _safe_json(resp: httpx.Response) -> Any:
    try:
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
    except Exception:
        pass
    return {"_raw": resp.text}


def _return_body(resp: httpx.Response) -> Any:
    ct = resp.headers.get("content-type", "")
    if ct.startswith("application/json"):
        try:
            return resp.json()
        except Exception:
            return resp.text
    return resp.text


def _extract_cafe24_error(body: Any, text: str) -> tuple[Optional[str], str]:
    """Pull (code, message) from a Cafe24 error envelope: ``{"error": {...}}``."""
    if isinstance(body, dict):
        err = body.get("error")
        if isinstance(err, dict):
            code = err.get("code")
            msg = err.get("message") or err.get("more_info")
            return (str(code) if code else None), (str(msg) if msg else text[:200])
        code = body.get("code")
        msg = body.get("message")
        if code or msg:
            return (str(code) if code else None), (str(msg) if msg else text[:200])
    return None, text[:200]


def _usage_remain_hint(resp: httpx.Response) -> Optional[float]:
    """Read the seconds-until-renewal hint from Cafe24 usage-limit headers.

    ``X-Cafe24-Call-Remain`` / ``X-Cafe24-Time-Remain`` report the remaining
    cooldown in seconds when usage hits 100%. Present only when throttled.
    """
    for h in ("x-cafe24-time-remain", "x-cafe24-call-remain"):
        raw = resp.headers.get(h)
        if raw:
            try:
                val = float(raw)
                if val > 0:
                    return val
            except ValueError:
                continue
    return None


def _extract_rows(data: Any, list_key: Optional[str]) -> tuple[list[Any], Optional[str]]:
    """Return (rows, detected_key). Cafe24 lists are top-level plural keys."""
    if isinstance(data, list):
        return data, list_key
    if isinstance(data, dict):
        if list_key and isinstance(data.get(list_key), list):
            return data[list_key], list_key
        # Auto-detect: the only list-valued top-level key (besides none).
        for k, v in data.items():
            if isinstance(v, list) and k != "pagination":
                return v, k
    return [], list_key
