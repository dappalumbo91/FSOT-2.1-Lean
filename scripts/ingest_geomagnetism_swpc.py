#!/usr/bin/env python3
"""Fetch NOAA SWPC geomagnetic indices."""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "geomagnetism_manifest.yaml"
CACHE = ROOT / "data" / "geomagnetism_swpc_cache.json"


def fetch_json(url: str) -> list | dict:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/geomagnetism"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    src = spec["source"]
    dst = fetch_json(src["dst_url"])
    goes = fetch_json(src["goes_url"])
    wind = fetch_json(src["solar_wind_url"])
    CACHE.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "dst": dst,
                "goes_magnetometers": goes,
                "solar_wind_speed": wind,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {CACHE}")
    print(f"  Dst rows: {len(dst) if isinstance(dst, list) else 0}")
    print(f"  GOES rows: {len(goes) if isinstance(goes, list) else 0}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())