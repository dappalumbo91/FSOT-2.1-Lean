#!/usr/bin/env python3
"""Ingest NOAA/WDC Kyoto hourly Dst (1998–2012) + SWPC rolling window."""

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
MANIFEST = ROOT / "data" / "kyoto_dst_manifest.yaml"
CACHE = ROOT / "data" / "kyoto_dst_historical_cache.json"

sys_path = ROOT / "scripts"
import sys

sys.path.insert(0, str(sys_path))
from kyoto_dst_lab import fetch_dst_year  # noqa: E402


def _fetch_rolling(url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/kyoto-dst"})
    doc = json.loads(urllib.request.urlopen(req, timeout=60).read())
    if not isinstance(doc, list):
        return []
    return [{"time_tag": row.get("time_tag"), "dst": row.get("dst")} for row in doc if row.get("time_tag")]


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=CACHE)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    src = spec["source"]
    year_start = int(src["year_start"])
    year_end = int(src["year_end"])

    by_tag: dict[str, int] = {}
    for year in range(year_start, year_end + 1):
        try:
            rows = fetch_dst_year(year)
        except Exception as exc:
            print(f"  skip {year}: {exc}")
            continue
        for row in rows:
            by_tag[row["time_tag"]] = int(row["dst"])
        print(f"  fetched {year}: {len(rows)} hours")

    rolling = _fetch_rolling(src["rolling_dst_url"])
    for row in rolling:
        tag = row.get("time_tag") or ""
        dst = row.get("dst")
        if tag and dst is not None:
            by_tag[tag] = int(dst)
    print(f"  rolling SWPC Dst: {len(rolling)} hours")

    records = [{"time_tag": tag, "dst": dst} for tag, dst in sorted(by_tag.items())]
    args.output.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": src,
                "record_count": len(records),
                "year_range": [year_start, year_end],
                "records": records,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {args.output}")
    print(f"  Kyoto Dst hours: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())