#!/usr/bin/env python3
"""Ingest real observables for tier gap-fill wave (G: Seagate cache)."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-root", default=r"G:\FSOT-PublicData")
    parser.add_argument("--skip-tier38", action="store_true")
    parser.add_argument("--skip-weather", action="store_true")
    args = parser.parse_args()

    os.environ["FSOT_EXTERNAL_DATA_ROOT"] = args.external_root
    Path(args.external_root).mkdir(parents=True, exist_ok=True)
    print(f"External data root: {args.external_root}")

    if not args.skip_tier38:
        cmd = [sys.executable, str(ROOT / "scripts" / "ingest_tier38_public_data.py"), "--deep"]
        print("Running Tier 38 deep ingest...")
        subprocess.run(cmd, check=True, cwd=ROOT)

    if not args.skip_weather:
        cmd = [sys.executable, str(ROOT / "scripts" / "fetch_weather_observed_benchmark.py")]
        print("Fetching Open-Meteo weather observed benchmark...")
        subprocess.run(cmd, check=True, cwd=ROOT)

    from tier_gap_fill_lib import _ensure_fermentation_reference, _ensure_pk_reference  # noqa: E402

    _ensure_pk_reference()
    _ensure_fermentation_reference()
    print("PK + fermentation reference observables ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())