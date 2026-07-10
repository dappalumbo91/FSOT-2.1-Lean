#!/usr/bin/env python3
"""Tier 60 — SIMBAD TAP ingest with bundled fallback."""

from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "stellar_structures"
BUNDLED = VENDOR / "simbad_stellar_identity_sample.json"
CACHE_NAME = "simbad_live_cache.json"

SIMBAD_TAP = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
ADQL = (
    "SELECT TOP 25 main_id, otype, sp_type, plx_value, "
    "SQRT(pmra*pmra + pmdec*pmdec) AS pm_total "
    "FROM basic WHERE otype IN ('SB*','**') AND plx_value > 5"
)


def external_cache_root() -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    if raw:
        root = Path(raw).expanduser() / "tier60_live_astrometry"
    else:
        root = VENDOR / "live_cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def fetch_simbad() -> list[dict]:
    params = urllib.parse.urlencode(
        {"request": "doQuery", "lang": "adql", "format": "json", "query": ADQL}
    )
    url = f"{SIMBAD_TAP}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tier60"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    rows = payload.get("data") or []
    out: list[dict] = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 5:
            continue
        out.append(
            {
                "main_id": str(row[0]),
                "otype": str(row[1]),
                "sptype": str(row[2]) if row[2] is not None else None,
                "plx_mas": float(row[3]) if row[3] is not None else None,
                "pm_total_masyr": float(row[4]) if row[4] is not None else None,
                "source": "SIMBAD_TAP_live",
            }
        )
    return out


def load_bundled() -> list[dict]:
    if not BUNDLED.exists():
        return []
    doc = json.loads(BUNDLED.read_text(encoding="utf-8"))
    return [{**o, "source": "SIMBAD_bundled"} for o in doc.get("objects") or []]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    if args.offline:
        objects = load_bundled()
        source = "bundled"
    else:
        try:
            objects = fetch_simbad()
            source = "SIMBAD_TAP_live" if objects else "bundled_fallback_empty"
            if not objects:
                objects = load_bundled()
        except Exception as exc:
            print(f"SIMBAD fetch failed ({exc}); bundled fallback")
            objects = load_bundled()
            source = "bundled_fallback"
    doc = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "object_count": len(objects),
        "objects": objects,
    }
    for path in (external_cache_root() / CACHE_NAME, VENDOR / CACHE_NAME):
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"Wrote {path} ({len(objects)} objects)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())