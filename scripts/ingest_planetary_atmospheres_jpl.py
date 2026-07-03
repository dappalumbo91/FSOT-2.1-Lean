#!/usr/bin/env python3
"""Fetch JPL Horizons atmosphere fields for Mars/Venus; embed Titan NASA reference."""

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
MANIFEST = ROOT / "data" / "planetary_atmospheres_manifest.yaml"
CACHE = ROOT / "data" / "planetary_atmospheres_cache.json"
sys.path.insert(0, str(ROOT / "scripts"))
from jpl_horizons_lab import (  # noqa: E402
    ATMOSPHERE_BODY_COMMANDS,
    NASA_ATMOSPHERE_REFERENCE,
    fetch_horizons,
    parse_atmosphere_block,
)


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    rows: list[dict] = []
    for name, (cmd, center) in ATMOSPHERE_BODY_COMMANDS.items():
        text = fetch_horizons(command=cmd, ephem_type="ELEMENTS", center=center)
        atmo = parse_atmosphere_block(text)
        rows.append(
            {
                "name": name,
                "command": cmd,
                "center": center,
                "source": "JPL_Horizons",
                "horizons_text": text,
                "pressure_bar": atmo.get("pressure_bar"),
                "temperature_k": atmo.get("temperature_k"),
            }
        )
        print(f"  fetched {name}")
    titan_ref = NASA_ATMOSPHERE_REFERENCE["Titan"]
    rows.append(
        {
            "name": "Titan",
            "command": "606",
            "center": "@699",
            "source": "NASA_Planetary_Fact_Sheet",
            "pressure_bar": titan_ref["pressure_bar"],
            "temperature_k": titan_ref["temperature_k"],
        }
    )
    print("  embedded Titan NASA reference")
    CACHE.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
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