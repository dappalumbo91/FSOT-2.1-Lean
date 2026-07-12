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
        "FSOT_TIER80_DEEP",
        "FSOT_TIER81_DEEP",
        "FSOT_TIER82_DEEP",
        "FSOT_TIER84_DEEP",
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
            ("Live API health probe", [py, "scripts/live_api_health_check.py"]),
            ("WDS bundled panel expand", [py, "scripts/expand_wds_bundled_panel.py"]),
            ("Tier 38 public APIs", [py, "scripts/ingest_tier38_public_data.py", "--deep"]),
            ("Tier 58 GWOSC", [py, "scripts/ingest_tier58_live_catalogs.py"]),
            ("Tier 60 SIMBAD", [py, "scripts/ingest_tier60_live_astrometry.py", "--deep"]),
            ("Tier 62 Gaia DR3", [py, "scripts/ingest_tier62_live_astrometry.py", "--deep"]),
            ("Tier 68 live ingest", [py, "scripts/ingest_tier68_live_ingest.py", "--deep"]),
            ("Tier 79 STScI MAST", [py, "scripts/ingest_stsci_mast.py", "--deep"]),
            ("Tier 80 government open data", [py, "scripts/ingest_tier80_government_open_data.py", "--deep"]),
            ("Tier 81 public verifiable", [py, "scripts/ingest_tier81_public_verifiable.py", "--deep"]),
            ("Tier 82 scientific expansion", [py, "scripts/ingest_tier82_scientific_expansion.py", "--deep"]),
            ("Tier 84 scientific expansion", [py, "scripts/ingest_tier84_scientific_expansion.py", "--deep"]),
            ("Tier 85 scientific expansion", [py, "scripts/ingest_tier85_scientific_expansion.py", "--deep"]),
            ("Tier 86 scientific expansion", [py, "scripts/ingest_tier86_scientific_expansion.py", "--deep"]),
            ("Tier 87 scientific expansion", [py, "scripts/ingest_tier87_scientific_expansion.py", "--deep"]),
            ("Tier 88 application wiring", [py, "scripts/ingest_tier88_application_wiring.py", "--deep"]),
            ("Tier 89 The Well verification", [py, "scripts/ingest_tier89_the_well.py", "--deep"]),
            ("Tier 90 consciousness expansion", [py, "scripts/ingest_tier90_consciousness_expansion.py", "--deep"]),
            ("Tier 91 foundational ontology", [py, "scripts/ingest_tier91_foundational_ontology.py", "--deep"]),
            ("Tier 92 alternate base math", [py, "scripts/ingest_tier92_alternate_base_mathematics.py", "--deep"]),
            ("Tier 38 benchmarks", [py, "scripts/build_tier38_public_data_benchmarks.py"]),
            ("Tier 58 benchmarks", [py, "scripts/build_tier58_live_catalog_benchmarks.py"]),
            ("Tier 60 benchmarks", [py, "scripts/build_tier60_astrometry_benchmarks.py"]),
            ("Tier 62 benchmarks", [py, "scripts/build_tier62_astrometry_benchmarks.py"]),
            ("Tier 68 benchmarks", [py, "scripts/build_tier68_live_ingest_benchmarks.py"]),
            ("Tier 79 benchmarks", [py, "scripts/build_tier79_telescope_benchmarks.py"]),
            ("Tier 80 benchmarks", [py, "scripts/build_tier80_government_open_data_benchmarks.py", "--skip-ingest"]),
            ("Tier 81 benchmarks", [py, "scripts/build_tier81_public_verifiable_benchmarks.py", "--skip-ingest"]),
            ("Tier 82 benchmarks", [py, "scripts/build_tier82_scientific_expansion_benchmarks.py", "--skip-ingest"]),
            ("Tier 84 benchmarks", [py, "scripts/build_tier84_scientific_expansion_benchmarks.py", "--skip-ingest"]),
            ("Tier 85 benchmarks", [py, "scripts/build_tier85_scientific_expansion_benchmarks.py", "--skip-ingest"]),
            ("Tier 86 benchmarks", [py, "scripts/build_tier86_scientific_expansion_benchmarks.py", "--skip-ingest"]),
            ("Tier 87 benchmarks", [py, "scripts/build_tier87_scientific_expansion_benchmarks.py", "--skip-ingest"]),
            ("Tier 88 benchmarks", [py, "scripts/build_tier88_application_wiring_benchmarks.py", "--skip-ingest"]),
            ("Tier 89 benchmarks", [py, "scripts/build_tier89_the_well_benchmarks.py", "--skip-ingest"]),
            ("Tier 90 benchmarks", [py, "scripts/build_tier90_consciousness_expansion_benchmarks.py", "--skip-ingest"]),
            ("Tier 91 benchmarks", [py, "scripts/build_tier91_foundational_ontology_benchmarks.py", "--skip-ingest"]),
            ("Tier 92 benchmarks", [py, "scripts/build_tier92_alternate_base_mathematics_benchmarks.py", "--skip-ingest"]),
            ("Lean priors tier 38", [py, "scripts/gen_tier38_public_data_lean.py"]),
            ("Lean priors tier 68-70", [py, "scripts/gen_tiers_68_70_lean.py"]),
            ("Lean priors tier 79", [py, "scripts/gen_tier79_telescope_lean.py"]),
            ("Lean priors tier 80", [py, "scripts/gen_tier80_government_lean.py"]),
            ("Lean priors tier 81", [py, "scripts/gen_tier81_public_verifiable_lean.py"]),
            ("Lean priors tier 82", [py, "scripts/gen_tier82_scientific_expansion_lean.py"]),
            ("Lean priors tier 84", [py, "scripts/gen_tier84_scientific_expansion_lean.py"]),
            ("Lean priors tier 85", [py, "scripts/gen_tier85_scientific_expansion_lean.py"]),
            ("Lean priors tier 86", [py, "scripts/gen_tier86_scientific_expansion_lean.py"]),
            ("Lean priors tier 87", [py, "scripts/gen_tier87_scientific_expansion_lean.py"]),
            ("Lean priors tier 88", [py, "scripts/gen_tier88_application_wiring_lean.py"]),
            ("Lean priors tier 89", [py, "scripts/gen_tier89_the_well_lean.py"]),
            ("Lean priors tier 90", [py, "scripts/gen_tier90_consciousness_expansion_lean.py"]),
            ("Lean priors tier 91", [py, "scripts/gen_tier91_foundational_ontology_lean.py"]),
            ("Lean priors tier 92", [py, "scripts/gen_tier92_alternate_base_mathematics_lean.py"]),
            ("Core formula fractal sync", [py, "scripts/sync_core_formula_fractal_branches.py"]),
            ("C_thin panel upgrade", [py, "scripts/upgrade_c_thin_panels.py"]),
        ]
    )

    if not args.skip_verify:
        steps.append(("Extension domain verify", [py, "scripts/verify_extension_domains.py"]))
        steps.append(("Benchmark margin audit", [py, "scripts/audit_all_benchmark_margins.py"]))

    if not args.skip_cross_proof:
        steps.append(("Cross-proof verification", [py, "scripts/run_cross_proof_verification.py"]))

    failed: list[str] = []
    non_fatal = {"Live API health probe"}
    for label, cmd in steps:
        rc = _run(cmd, label=label)
        if rc != 0 and label not in non_fatal:
            failed.append(label)
        elif rc != 0:
            print(f"Warning (non-fatal): {label}", file=sys.stderr)

    if failed:
        print(f"\nPipeline completed with failures: {failed}", file=sys.stderr)
        return 1

    print("\nAll live API mega-deep expansions complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())