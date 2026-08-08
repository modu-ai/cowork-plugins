"""Imweb OPEN API HTTP client — shared by every generated tool.

Responsibilities:
  * inject the Bearer access token on every request
  * on ``401`` (GW.AUTHN / token expired), refresh once and retry
  * respect an optional inter-request delay (``IMWEB_REQUEST_DELAY``)
  * translate non-2xx Imweb error envelopes into :class:`ImwebApiError`
  * expose ``list_all_pages`` for transparent cursor/offset pagination when a
    list endpoint advertises ``page`` + ``limit`` (the caller may instead use the
    raw single-page tool; this helper is opt-in via the ``paginate`` flag).

The client is a thin wrapper; all domain logic lives in the generated tools.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Mapping, Optional

import httpx

from .auth import ImwebAuthError, refresh_access_token

if TYPE_CHECKING:
    from ._base import ImwebConfig


class ImwebApiError(RuntimeError):
    """Raised on a non-2xx response. Carries status, code, message, raw body."""

    def __init__(self, status: int, code: Optional[str], message: str, body: Any, url: str):
        self.status = status
        self.code = code
        self.message = message
        self.body = body
        self.url = url
        super().__init__(f"Imweb API 오류 (HTTP {status}) [{code}] {message}  @ {url}")


class ImwebClient:
    def __init__(self, config: "ImwebConfig"):
        from ._base import _persist_tokens  # local import to avoid cycle at module import

        self._config = config
        self._persist = _persist_tokens
        self._access = config.access_token
        self._refresh = config.refresh_token
        self._http = httpx.Client(base_url=config.api_base, timeout=config.timeout)
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

    def _headers(self) -> dict[str, str]:
        h = {"Accept": "application/json"}
        if self._access:
            h["Authorization"] = f"Bearer {self._access}"
        return h

    def _do_refresh(self) -> None:
        pair = refresh_access_token(self._config, client=self._http)
        self._access = pair.access_token
        self._refresh = pair.refresh_token
        # Rebuild a config snapshot for persistence with the new tokens.
        from dataclasses import replace

        new_cfg = replace(self._config, access_token=self._access, refresh_token=self._refresh)
        self._config = new_cfg
        self._persist(new_cfg.token_file, self._access, self._refresh)

    def request(
        self,
        method: str,
        path: str,
        *,
        path_params: Optional[Mapping[str, Any]] = None,
        params: Optional[Mapping[str, Any]] = None,
        json_body: Any = None,
        data: Any = None,
        files: Any = None,
        retry_on_401: bool = True,
    ) -> Any:
        """Perform a single API call. Returns parsed JSON (or raw text on non-JSON)."""
        if path_params:
            # str() every path param; None values are filled as empty — caller should not pass None.
            path = path.format(**{k: ("-" if v is None else _path_val(v)) for k, v in path_params.items()})
        clean_params = _drop_none(params)

        self._delay()
        resp = self._http.request(
            method.upper(),
            path,
            params=clean_params,
            json=json_body,
            data=data,
            files=files,
            headers=self._headers(),
        )

        # 401 → refresh once, retry once.
        if resp.status_code == 401 and retry_on_401 and self._config.can_refresh:
            try:
                self._do_refresh()
            except ImwebAuthError:
                raise
            return self.request(
                method, path, path_params=None, params=params, json_body=json_body,
                data=data, files=files, retry_on_401=False,
            )

        if resp.status_code >= 400:
            body = _safe_json(resp)
            code, message = _extract_imweb_error(body, resp.text)
            raise ImwebApiError(resp.status_code, code, message, body, str(resp.url))

        return _return_body(resp)

    # ------------------------------------------------------------ pagination
    def list_all_pages(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        page_size: int = 100,
        max_pages: int = 50,
        list_key: str = "list",
    ) -> dict[str, Any]:
        """Follow ``page``/``limit`` offset pagination, concatenating ``list_key``.

        Stops at the first page whose returned list is shorter than ``page_size``
        (heuristic end-of-data) or at ``max_pages``. Returns a dict with the
        aggregated ``list`` plus pagination metadata. The caller should usually
        prefer the single-page tool; this helper exists for "get everything"
        workflows.
        """
        aggregated: list[Any] = []
        base = dict(_drop_none(params) or {})
        meta: dict[str, Any] = {"page_size": page_size, "pages_fetched": 0}
        for page in range(1, max_pages + 1):
            p = {**base, "page": page, "limit": page_size}
            data = self.request("GET", path, params=p)
            rows = _extract_rows(data, list_key)
            aggregated.extend(rows)
            meta["pages_fetched"] = page
            if len(rows) < page_size:
                break
        meta["total_returned"] = len(aggregated)
        meta["truncated"] = meta["pages_fetched"] >= max_pages
        return {"list": aggregated, **{k: v for k, v in (data if isinstance(data, dict) else {}).items() if k != list_key}, "pagination": meta}

    def close(self) -> None:
        self._http.close()


# ---------------------------------------------------------------- helpers
def _path_val(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _drop_none(m: Optional[Mapping[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if not m:
        return out
    for k, v in m.items():
        if v is None:
            continue
        if isinstance(v, bool):
            out[k] = "Y" if v else "N"  # Imweb uses Y/N enums widely
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


def _extract_imweb_error(body: Any, text: str) -> tuple[Optional[str], str]:
    """Pull (code, message) from an Imweb error envelope.

    Imweb envelopes vary; common shapes: ``{"code": "...", "message": "..."}``,
    ``{"status": ..., "errorMessage": "..."}``, ``{"result": {"code": ...}}``.
    """
    if isinstance(body, dict):
        code = body.get("code") or body.get("errorCode")
        if not code and isinstance(body.get("result"), dict):
            code = body["result"].get("code")
        msg = body.get("message") or body.get("errorMessage") or body.get("msg")
        if not msg and isinstance(body.get("result"), dict):
            msg = body["result"].get("message")
        return (str(code) if code else None), (str(msg) if msg else text[:200])
    return None, text[:200]


def _extract_rows(data: Any, list_key: str) -> list[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if isinstance(data.get(list_key), list):
            return data[list_key]
        # Imweb frequently nests: {"result": {"list": [...]}}
        nested = data.get("result") if isinstance(data.get("result"), dict) else data.get("data")
        if isinstance(nested, dict) and isinstance(nested.get(list_key), list):
            return nested[list_key]
        if isinstance(nested, list):
            return nested
    return []
