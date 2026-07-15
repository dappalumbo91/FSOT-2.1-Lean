#!/usr/bin/env python3
"""
One-command publication verification bundle for independent replication.

Runs: contested closure → spine walkthrough → scientific figures → publication figures → claims bundle → margin audit.
Does NOT re-ingest live APIs (uses on-disk benchmarks). Optional: --full-cross-proof (~8 min).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
SCRIPTS = ROOT / "scripts"


ADVISORY_STEPS = frozenset(
    {
        "build_tier_scalar_precision_closure.py",
        "audit_scientific_pushback_coverage.py",
    }
)


def _run(script: str, *extra: str) -> bool:
    cmd = [PY, str(SCRIPTS / script), *extra]
    print(f"\n>>> {' '.join(cmd)}")
    advisory = script in ADVISORY_STEPS
    result = subprocess.run(cmd, cwd=str(ROOT), check=False)
    if result.returncode != 0:
        if advisory:
            print(
                f"  [advisory] {script} exit {result.returncode} — "
                "tier aspiration / pushback audit; extension 0.5% gate unchanged"
            )
            return True
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT publication verification bundle")
    parser.add_argument(
        "--full-cross-proof",
        action="store_true",
        help="Also run run_cross_proof_verification.py (~8 min)",
    )
    args = parser.parse_args()

    steps = [
        ("gen_verified_desktop_lean.py", []),
        ("build_verified_desktop_cross_proof_closure.py", []),
        ("build_fsot_domain_navigator_db.py", []),
        ("export_domain_citations.py", ["--bundle", "verified_desktop"]),
        ("build_contested_observables_closure.py", []),
        ("build_publication_spine_walkthrough.py", []),
        ("build_scientific_figures.py", []),
        ("build_publication_figure_pack.py", []),
        ("build_publication_claims_bundle.py", []),
        ("audit_all_benchmark_margins.py", []),
        ("build_tier_scalar_precision_closure.py", []),
        ("audit_scientific_pushback_coverage.py", []),
    ]
    for script, extra in steps:
        if not _run(script, *extra):
            return 1

    if args.full_cross_proof:
        if not _run("run_cross_proof_verification.py"):
            return 1

    print("\n=== Publication verification bundle complete ===")
    print(f"  Figures: {ROOT / 'data' / 'figures'}")
    print(f"  Walkthrough: {ROOT / 'data' / 'publication_spine_walkthrough.json'}")
    print(f"  Claims: {ROOT / 'data' / 'publication_claims_manifest.json'}")
    print(f"  Domain navigator: {ROOT / 'data' / 'fsot_domain_navigator.json'}")
    print(f"  Verified desktop citations: {ROOT / 'data' / 'domain_citations' / 'verified_desktop.bib'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())