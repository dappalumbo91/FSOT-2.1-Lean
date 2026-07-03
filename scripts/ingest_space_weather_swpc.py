#!/usr/bin/env python3
"""Fetch NOAA SWPC planetary K-index (Kp + Ap proxy) into cache."""

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
MANIFEST = ROOT / "data" / "space_weather_manifest.yaml"


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
            }
        )
    return rows


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    url = spec["source"]["swpc_kp_url"]
    cache_path = ROOT / spec["source"]["cache"]
    rows = fetch_kp(url)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source_url": url,
        "record_count": len(rows),
        "records": rows,
    }
    cache_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {cache_path}")
    print(f"  Kp records: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())