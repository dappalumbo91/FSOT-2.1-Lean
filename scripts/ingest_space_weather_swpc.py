#!/usr/bin/env python3
"""Fetch NOAA SWPC rolling Kp + merge GFZ historical chunks into unified cache."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "space_weather_manifest.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from space_weather_gfz_lab import dedupe_records, load_manifest, merge_year_chunks  # noqa: E402


def fetch_kp(url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/space-weather"})
    raw = json.loads(urllib.request.urlopen(req, timeout=30).read())
    rows: list[dict] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        if "Kp" not in item:
            continue
        try:
            kp = float(item["Kp"])
        except (TypeError, ValueError):
            continue
        ap = item.get("a_running")
        try:
            ap_f = float(ap) if ap is not None else None
        except (TypeError, ValueError):
            ap_f = None
        rows.append(
            {
                "time_tag": item.get("time_tag"),
                "kp": kp,
                "ap_running": ap_f,
                "station_count": item.get("station_count"),
                "source": "swpc_rolling",
            }
        )
    return rows


def merge_cache(spec: dict, rolling_rows: list[dict]) -> dict:
    hist = spec.get("historical") or {}
    cache_cfg = spec.get("cache") or {}
    cache_root = ROOT / cache_cfg.get("root", "data/space_weather_cache")
    y0 = int(hist.get("start_year", 2018))
    y1 = int(hist.get("end_year", 2024))
    historical = merge_year_chunks(cache_root, y0, y1)
    merged = dedupe_records(historical + rolling_rows, prefer_source="swpc_rolling")
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source_url": spec["source"]["swpc_kp_url"],
        "historical_source": hist.get("gfz_kp_url"),
        "historical_year_range": [y0, y1],
        "rolling_record_count": len(rolling_rows),
        "historical_record_count": len(historical),
        "record_count": len(merged),
        "records": merged,
    }


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--rolling-only", action="store_true")
    args = parser.parse_args()
    spec = load_manifest(args.manifest)
    url = spec["source"]["swpc_kp_url"]
    cache_path = ROOT / spec["source"]["cache"]
    rolling = fetch_kp(url)
    if args.rolling_only:
        doc = {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source_url": url,
            "record_count": len(rolling),
            "records": rolling,
        }
    else:
        doc = merge_cache(spec, rolling)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {cache_path}")
    print(f"  total Kp records: {doc['record_count']}")
    if not args.rolling_only:
        print(f"  historical: {doc.get('historical_record_count')}  rolling: {doc.get('rolling_record_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())