"""GFZ Kp/ap historical ingest helpers — year-chunked cache."""

from __future__ import annotations

import json
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

GFZ_KP_URL = "http://www-app3.gfz-potsdam.de/kp_index/Kp_ap_since_1932.txt"
HEADER_LINES = 30


def load_manifest(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML required") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def chunk_key(year: int) -> str:
    return str(year)


def chunk_path(cache_root: Path, year: int) -> Path:
    return cache_root / "chunks" / f"{year}.json"


def load_state(state_path: Path) -> dict:
    if not state_path.exists():
        return {"completed_chunks": [], "failed_chunks": []}
    return json.loads(state_path.read_text(encoding="utf-8"))


def save_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _parse_gfz_line(line: str) -> dict[str, Any] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = line.split()
    if len(parts) < 10:
        return None
    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        hour = float(parts[3])
        kp = float(parts[8])
        ap = int(parts[9])
    except (TypeError, ValueError):
        return None
    if kp < 0 or ap < 0:
        return None
    hour_i = int(hour)
    return {
        "time_tag": f"{year:04d}-{month:02d}-{day:02d}T{hour_i:02d}:00:00",
        "kp": kp,
        "ap_running": float(ap),
        "source": "gfz_kp_ap",
        "definitive": parts[10] == "1" if len(parts) > 10 else True,
    }


def stream_gfz_rows(url: str = GFZ_KP_URL):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/space-weather-historical"})
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        for i, raw in enumerate(resp):
            if i < HEADER_LINES:
                continue
            row = _parse_gfz_line(raw.decode("utf-8", errors="replace"))
            if row is not None:
                yield row


def write_year_chunk(path: Path, year: int, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "year": year,
        "record_count": len(records),
        "records": records,
        "written_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def merge_year_chunks(cache_root: Path, start_year: int, end_year: int) -> list[dict]:
    merged: list[dict] = []
    for year in range(start_year, end_year + 1):
        chunk = chunk_path(cache_root, year)
        if not chunk.exists():
            continue
        doc = json.loads(chunk.read_text(encoding="utf-8"))
        merged.extend(doc.get("records") or [])
    merged.sort(key=lambda r: r.get("time_tag") or "")
    return merged


def dedupe_records(records: list[dict], *, prefer_source: str = "swpc_rolling") -> list[dict]:
    order = {"swpc_rolling": 2, "gfz_kp_ap": 1}
    by_tag: dict[str, dict] = {}
    for row in records:
        tag = row.get("time_tag")
        if not tag:
            continue
        src = row.get("source") or "gfz_kp_ap"
        existing = by_tag.get(tag)
        if existing is None:
            by_tag[tag] = {**row, "source": src}
            continue
        if order.get(src, 0) >= order.get(existing.get("source") or "", 0):
            by_tag[tag] = {**row, "source": src}
    return sorted(by_tag.values(), key=lambda r: r["time_tag"])