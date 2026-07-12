#!/usr/bin/env python3
"""Mega-deep expansion of every FSOT live API ingest + full verification pipeline.

Sets FSOT_API_MEGA_DEEP=1 and runs all tier ingest scripts, benchmark rebuilds,
Lean prior regeneration, and cross-proof verification.

Usage:
  python scripts/expand_all_live_apis.py
  python scripts/expand_all_live_apis.py --skip-pubchem
  python scripts/expand_all_live_apis.py --skip-verify
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _env() -> dict[str, str]:
    env = os.environ.copy()
    for key in (
        "FSOT_API_MEGA_DEEP",
        "FSOT_TIER38_DEEP",
        "FSOT_TIER60_DEEP",
        "FSOT_TIER62_DEEP",
        "FSOT_TIER68_DEEP",
        "FSOT_TIER79_DEEP",
    ):
        env[key] = "1"
    return env


def _run(cmd: list[str], *, label: str) -> int:
    print(f"\n=== {label} ===")
    print(" ".join(cmd))
    rc = subprocess.call(cmd, cwd=ROOT, env=_env())
    if rc != 0:
        print(f"FAILED ({rc}): {label}", file=sys.stderr)
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand all live API ingests (mega-deep)")
    parser.add_argument("--skip-pubchem", action="store_true")
    parser.add_argument("--skip-verify", action="store_true")
    parser.add_argument("--skip-cross-proof", action="store_true")
    args = parser.parse_args()

    py = sys.executable
    steps: list[tuple[str, list[str]]] = []

    if not args.skip_pubchem:
        steps.append(("PubChem auto-discovery", [py, "scripts/expand_pubchem_panel.py"]))

    steps.extend(
        [
            ("Tier 38 public APIs", [py, "scripts/ingest_tier38_public_data.py", "--deep"]),
            ("Tier 58 GWOSC", [py, "scripts/ingest_tier58_live_catalogs.py"]),
            ("Tier 60 SIMBAD", [py, "scripts/ingest_tier60_live_astrometry.py", "--deep"]),
            ("Tier 62 Gaia DR3", [py, "scripts/ingest_tier62_live_astrometry.py", "--deep"]),
            ("Tier 68 live ingest", [py, "scripts/ingest_tier68_live_ingest.py", "--deep"]),
            ("Tier 79 STScI MAST", [py, "scripts/ingest_stsci_mast.py", "--deep"]),
            ("Tier 38 benchmarks", [py, "scripts/build_tier38_public_data_benchmarks.py"]),
            ("Tier 58 benchmarks", [py, "scripts/build_tier58_live_catalog_benchmarks.py"]),
            ("Tier 60 benchmarks", [py, "scripts/build_tier60_astrometry_benchmarks.py"]),
            ("Tier 62 benchmarks", [py, "scripts/build_tier62_astrometry_benchmarks.py"]),
            ("Tier 68 benchmarks", [py, "scripts/build_tier68_live_ingest_benchmarks.py"]),
            ("Tier 79 benchmarks", [py, "scripts/build_tier79_telescope_benchmarks.py"]),
            ("Lean priors tier 38", [py, "scripts/gen_tier38_public_data_lean.py"]),
            ("Lean priors tier 68-70", [py, "scripts/gen_tiers_68_70_lean.py"]),
            ("Lean priors tier 79", [py, "scripts/gen_tier79_telescope_lean.py"]),
        ]
    )

    if not args.skip_verify:
        steps.append(("Extension domain verify", [py, "scripts/verify_extension_domains.py"]))
        steps.append(("Benchmark margin audit", [py, "scripts/audit_all_benchmark_margins.py"]))

    if not args.skip_cross_proof:
        steps.append(("Cross-proof verification", [py, "scripts/run_cross_proof_verification.py"]))

    failed: list[str] = []
    for label, cmd in steps:
        if _run(cmd, label=label) != 0:
            failed.append(label)

    if failed:
        print(f"\nPipeline completed with failures: {failed}", file=sys.stderr)
        return 1

    print("\nAll live API mega-deep expansions complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())