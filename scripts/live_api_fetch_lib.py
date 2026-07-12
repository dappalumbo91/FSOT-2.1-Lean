"""Shared HTTP helpers for FSOT live API ingests — SSL, retries, backoff."""

from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def ssl_context(*, insecure_fallback: bool = True) -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    try:
        import certifi  # noqa: WPS433

        ctx.load_verify_locations(certifi.where())
        return ctx
    except Exception:
        if not insecure_fallback:
            raise
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_bytes(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 120,
    retries: int = 4,
    backoff_s: float = 2.0,
    retry_codes: frozenset[int] = frozenset({429, 500, 502, 503, 504}),
) -> bytes:
    """GET with exponential backoff on transient HTTP failures."""
    hdrs = {"User-Agent": "FSOT-2.1-Lean/live-api", **(headers or {})}
    ctx = ssl_context()
    last_exc: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code not in retry_codes or attempt >= retries - 1:
                raise
            time.sleep(backoff_s * (2**attempt))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_exc = exc
            if attempt >= retries - 1:
                raise
            time.sleep(backoff_s * (2**attempt))
    raise last_exc or RuntimeError("fetch_bytes failed")


def fetch_json(url: str, **kwargs: Any) -> object:
    return json.loads(fetch_bytes(url, **kwargs).decode("utf-8"))


def post_json(
    url: str,
    data: dict[str, str],
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 120,
    retries: int = 4,
    backoff_s: float = 2.0,
    retry_codes: frozenset[int] = frozenset({429, 500, 502, 503, 504}),
) -> object:
    """POST form body with same retry policy as fetch_bytes."""
    body = urllib.parse.urlencode(data).encode("utf-8")
    hdrs = {
        "User-Agent": "FSOT-2.1-Lean/live-api",
        "Content-Type": "application/x-www-form-urlencoded",
        **(headers or {}),
    }
    ctx = ssl_context()
    last_exc: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code not in retry_codes or attempt >= retries - 1:
                raise
            time.sleep(backoff_s * (2**attempt))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_exc = exc
            if attempt >= retries - 1:
                raise
            time.sleep(backoff_s * (2**attempt))
    raise last_exc or RuntimeError("post_json failed")