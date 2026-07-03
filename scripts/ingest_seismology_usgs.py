#!/usr/bin/env python3
"""Fetch USGS earthquake catalog into seismology cache."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "seismology_usgs_manifest.yaml"
CACHE = ROOT / "data" / "seismology_usgs_cache.json"
sys.path.insert(0, str(ROOT / "scripts"))
from seismology_usgs_lab import fetch_earthquakes  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    src = spec["source"]
    rows = fetch_earthquakes(
        starttime=src["starttime"],
        endtime=src["endtime"],
        minmagnitude=float(src["minmagnitude"]),
        limit=int(src["limit"]),
    )
    CACHE.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": src,
                "event_count": len(rows),
                "events": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {CACHE}")
    print(f"  USGS earthquakes: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())