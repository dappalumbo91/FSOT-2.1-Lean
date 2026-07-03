#!/usr/bin/env python3
"""Fetch PB2002 plate boundaries GeoJSON."""

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
MANIFEST = ROOT / "data" / "tectonics_manifest.yaml"
CACHE = ROOT / "data" / "tectonics_plates_cache.json"


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    url = spec["source"]["plates_url"]
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tectonics"})
    doc = json.loads(urllib.request.urlopen(req, timeout=60).read())
    features = doc.get("features") or []
    CACHE.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source_url": url,
                "feature_count": len(features),
                "features": features,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {CACHE}")
    print(f"  plate boundary features: {len(features)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())