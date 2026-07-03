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
from jpl_horizons_lab import PLANET_COMMANDS, fetch_horizons  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    bodies = list(PLANET_COMMANDS.keys())
    rows: list[dict] = []
    for name in bodies:
        cmd = PLANET_COMMANDS[name]
        physical_text = fetch_horizons(command=cmd, ephem_type="ELEMENTS")
        rows.append({"name": name, "command": cmd, "horizons_text": physical_text})
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