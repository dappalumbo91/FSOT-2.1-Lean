#!/usr/bin/env python3
"""One-shot seed for NASA NEO bundled fallback panel."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier80_government_open_data_lib import _neo_row_from_api  # noqa: E402
from live_api_fetch_lib import fetch_json  # noqa: E402

OUT = ROOT / "vendor" / "government_open_data" / "nasa_neo_bundled.json"


def main() -> int:
    time.sleep(15)
    url = (
        "https://api.nasa.gov/neo/rest/v1/feed?"
        "start_date=2025-06-01&end_date=2025-06-07&api_key=DEMO_KEY"
    )
    payload = fetch_json(url, timeout=60)
    neos = []
    for day_rows in (payload.get("near_earth_objects") or {}).values():
        for row in day_rows:
            neos.append(_neo_row_from_api(row))
    doc = {"source": "nasa_neows_seed", "neo_count": len(neos), "neos": neos}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(neos)} neos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())