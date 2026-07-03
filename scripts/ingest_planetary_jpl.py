#!/usr/bin/env python3
"""Fetch JPL Horizons physical + orbital data for major planets."""

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
CACHE = ROOT / "data" / "planetary_jpl_cache.json"
sys.path.insert(0, str(ROOT / "scripts"))
from jpl_horizons_lab import EXTENDED_BODY_COMMANDS, PLANET_COMMANDS, fetch_horizons  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    rows: list[dict] = []
    for name, cmd in PLANET_COMMANDS.items():
        physical_text = fetch_horizons(command=cmd, ephem_type="ELEMENTS")
        rows.append({"name": name, "command": cmd, "center": "@10", "horizons_text": physical_text})
        print(f"  fetched {name}")
    for name, (cmd, center) in EXTENDED_BODY_COMMANDS.items():
        physical_text = fetch_horizons(command=cmd, center=center, ephem_type="ELEMENTS")
        rows.append({"name": name, "command": cmd, "center": center, "horizons_text": physical_text})
        print(f"  fetched {name}")
    CACHE.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": "JPL_Horizons",
                "body_count": len(rows),
                "bodies": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {CACHE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())