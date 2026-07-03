#!/usr/bin/env python3
"""Fetch GFZ GravIS Greenland basin-averaged ice-mass ASCII into cache."""

from __future__ import annotations

import argparse
import json
import re
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "grace_cryosphere_manifest.yaml"
CACHE = ROOT / "data" / "grace_greenland_cache.json"


def _decimal_year_to_ym(dec_year: float) -> str:
    year = int(dec_year)
    frac = dec_year - year
    month = min(12, max(1, int(round(frac * 12)) + 1))
    return f"{year:04d}-{month:02d}"


def fetch_asc(url: str) -> list[dict]:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    text = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/grace"}),
        timeout=120,
        context=ctx,
    ).read().decode("utf-8", errors="replace")
    rows: list[dict] = []
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        parts = re.split(r"\s+", line.strip())
        if len(parts) < 2:
            continue
        try:
            dec_year = float(parts[0])
            mass_gt = float(parts[1])
        except ValueError:
            continue
        rows.append(
            {
                "decimal_year": dec_year,
                "month": _decimal_year_to_ym(dec_year),
                "mass_gt": mass_gt,
            }
        )
    return rows


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=CACHE)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    src = spec["source"]
    rows = fetch_asc(src["asc_url"])
    args.output.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": src,
                "record_count": len(rows),
                "records": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {args.output}")
    print(f"  GRACE Greenland months: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())