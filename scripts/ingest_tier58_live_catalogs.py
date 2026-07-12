#!/usr/bin/env python3
"""Tier 58 — optional live ingest for GWOSC (+ bundled fallback for portable clones)."""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "stellar_structures"
BUNDLED = VENDOR / "gwosc_public_events.json"
CACHE_NAME = "gwosc_live_cache.json"

GWOSC_URL = "https://www.gw-openscience.org/eventapi/json/"


def external_cache_root() -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    if raw:
        root = Path(raw).expanduser() / "tier58_live_catalogs"
    else:
        root = VENDOR / "live_cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _fetch_json(url: str) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tier58"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _event_row(name: str, row: dict) -> dict | None:
    chirp = (
        row.get("chirp_mass_source")
        or row.get("chirp_mass")
        or row.get("mass_1_source")
    )
    common = row.get("commonName") or name
    eid = str(common or name).split("-v")[0]
    if not eid:
        return None
    out: dict = {
        "id": eid,
        "chirp_mass_msun": float(chirp) if chirp is not None else None,
        "mass_ratio": row.get("mass_ratio"),
        "source": "GWOSC_live",
    }
    final_mass = row.get("final_mass_source") or row.get("final_mass")
    if final_mass is not None:
        out["final_mass_msun"] = float(final_mass)
    return out


def fetch_gwosc_events() -> list[dict]:
    """GWOSC event API v2 — nested catalog URLs with per-event JSON payloads."""
    payload = _fetch_json(GWOSC_URL)
    events: list[dict] = []
    seen: set[str] = set()

    def _ingest_event_dict(name: str, row: dict) -> None:
        rec = _event_row(name, row)
        if rec is None or rec["id"] in seen:
            return
        seen.add(rec["id"])
        events.append(rec)

    if isinstance(payload, list):
        for row in payload:
            if isinstance(row, dict):
                _ingest_event_dict(str(row.get("name") or row.get("id") or ""), row)
        return events

    if isinstance(payload, dict):
        flat = payload.get("events")
        if isinstance(flat, dict):
            for name, row in flat.items():
                if isinstance(row, dict):
                    _ingest_event_dict(str(name), row)
            return events
        if isinstance(flat, list):
            for row in flat:
                if isinstance(row, dict):
                    _ingest_event_dict(str(row.get("name") or row.get("id") or ""), row)
            return events

        catalog_keys = (
            "GWTC-4.1",
            "GWTC-4.0",
            "GWTC-3-confident",
            "GWTC-2.1-confident",
            "GWTC-2-confident",
            "GWTC-1-confident",
        )
        for key in catalog_keys:
            cat = payload.get(key)
            if not isinstance(cat, dict):
                continue
            sub_url = cat.get("url")
            if not sub_url:
                continue
            sub = _fetch_json(str(sub_url))
            sub_events = sub.get("events") if isinstance(sub, dict) else None
            if isinstance(sub_events, dict):
                for name, row in sub_events.items():
                    if isinstance(row, dict):
                        _ingest_event_dict(str(name), row)

    return [e for e in events if e.get("id")]


def load_bundled_events() -> list[dict]:
    if not BUNDLED.exists():
        return []
    doc = json.loads(BUNDLED.read_text(encoding="utf-8"))
    return list(doc.get("events") or [])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Copy bundled GWOSC summary only")
    args = parser.parse_args()
    events: list[dict]
    source = "bundled"
    if args.offline:
        events = load_bundled_events()
    else:
        try:
            events = fetch_gwosc_events()
            if not events:
                events = load_bundled_events()
                source = "bundled_fallback_empty_live"
            else:
                source = "GWOSC_live"
        except Exception as exc:
            print(f"Live GWOSC fetch failed ({exc}); using bundled fallback")
            events = load_bundled_events()
            source = "bundled_fallback"
    doc = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "event_count": len(events),
        "events": events,
    }
    cache_path = external_cache_root() / CACHE_NAME
    vendor_path = VENDOR / CACHE_NAME
    cache_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    vendor_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {cache_path} ({len(events)} events, source={source})")
    print(f"Wrote {vendor_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())