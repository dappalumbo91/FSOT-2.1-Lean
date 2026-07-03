#!/usr/bin/env python3
"""Ingest NOAA SWPC RTSW 1-minute solar wind magnetic field."""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "solar_wind_rtsw_manifest.yaml"
CACHE = ROOT / "data" / "solar_wind_rtsw_cache.json"


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=CACHE)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    src = spec["source"]
    prefer_active = bool(src.get("prefer_active", True))

    req = urllib.request.Request(src["url"], headers={"User-Agent": "FSOT-2.1-Lean/rtsw"})
    doc = json.loads(urllib.request.urlopen(req, timeout=90).read())
    records: list[dict] = []
    for row in doc:
        bz = row.get("bz_gsm")
        if bz is None or bz == -9999:
            continue
        if prefer_active and not row.get("active", True):
            continue
        records.append(
            {
                "time_tag": row.get("time_tag"),
                "source": row.get("source"),
                "active": row.get("active"),
                "bt": row.get("bt"),
                "bz_gsm": float(bz),
                "bx_gsm": row.get("bx_gsm"),
                "by_gsm": row.get("by_gsm"),
            }
        )

    args.output.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": src,
                "record_count": len(records),
                "records": records,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {args.output}")
    print(f"  RTSW 1-min records: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())