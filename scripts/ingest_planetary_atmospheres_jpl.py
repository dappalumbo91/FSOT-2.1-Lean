#!/usr/bin/env python3
"""Fetch JPL Horizons atmosphere fields; embed NASA fact-sheet anchors."""

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
    NASA_ATMOSPHERE_ONLY_BODIES,
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
        ref = NASA_ATMOSPHERE_REFERENCE.get(name) or {}
        rows.append(
            {
                "name": name,
                "command": cmd,
                "center": center,
                "source": "JPL_Horizons",
                "horizons_text": text,
                "pressure_bar": atmo.get("pressure_bar"),
                "temperature_k": atmo.get("temperature_k"),
                "nasa_pressure_bar": ref.get("pressure_bar"),
                "nasa_temperature_k": ref.get("temperature_k"),
            }
        )
        print(f"  fetched {name}")
    for name in NASA_ATMOSPHERE_ONLY_BODIES:
        if any(row["name"] == name for row in rows):
            continue
        ref = NASA_ATMOSPHERE_REFERENCE[name]
        rows.append(
            {
                "name": name,
                "command": None,
                "center": None,
                "source": "NASA_Planetary_Fact_Sheet",
                "pressure_bar": ref["pressure_bar"],
                "temperature_k": ref["temperature_k"],
                "nasa_pressure_bar": ref["pressure_bar"],
                "nasa_temperature_k": ref["temperature_k"],
            }
        )
        print(f"  embedded {name} NASA reference")
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
    print(f"Wrote {CACHE} ({len(rows)} bodies)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())