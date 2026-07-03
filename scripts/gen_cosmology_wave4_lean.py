#!/usr/bin/env python3
"""Generate deprecated CosmologyWave4.lean shim → CosmologyWave4Priors."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHIM = ROOT / "FSOT" / "Formal" / "CosmologyWave4.lean"
GEN_PRIORS = ROOT / "scripts" / "gen_cosmology_wave_lean.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=SHIM)
    args = parser.parse_args()
    if GEN_PRIORS.exists():
        subprocess.run(
            [sys.executable, str(GEN_PRIORS), "--wave", "4"],
            cwd=ROOT,
            check=False,
        )
    args.output.write_text(SHIM.read_text(encoding="utf-8") if SHIM.exists() else "", encoding="utf-8")
    print(f"Wrote deprecation shim {args.output} (imports CosmologyWave4Priors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())