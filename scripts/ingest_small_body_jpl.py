#!/usr/bin/env python3
"""Fetch JPL Horizons small-body + Moon orbital elements."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "small_body_jpl_cache.json"
sys.path.insert(0, str(ROOT / "scripts"))
from jpl_horizons_lab import SMALL_BODY_COMMANDS, fetch_horizons  # noqa: E402


def main() -> int:
    rows: list[dict] = []
    for name, (cmd, center) in SMALL_BODY_COMMANDS.items():
        text = fetch_horizons(command=cmd, center=center)
        rows.append({"name": name, "command": cmd, "center": center, "horizons_text": text})
        print(f"  fetched {name}")
    CACHE.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": "JPL_Horizons_small_bodies",
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