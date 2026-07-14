#!/usr/bin/env python3
"""Run full founding corpus pipeline (PDF → audit → reconcile → verify). No LLM training."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable

STEPS = [
    ("ingest_founding_pdfs.py", "Extract founding PDFs"),
    ("build_founding_unmapped_laws_benchmark.py", "Build Tier 96 founding-law panels"),
    ("gen_tier96_founding_laws_lean.py", "Generate Lean priors for founding laws"),
    ("audit_founding_35_laws.py", "Audit 35 founding laws"),
    ("reconcile_founding_corpus.py", "Reconcile founding text corpus"),
    ("verify_founding_corpus.py", "Verify founding corpus gate"),
]

CROSS_PROOF_EXPORT = [
    ("export_full_formal_obligations.py", "Export founding bundles to formal spine"),
    ("generate_structural_proof_artifacts.py", "Regenerate Coq/Isabelle structural proofs"),
    ("generate_rust_obligation_replay.py", "Regenerate Rust obligation replay"),
]


def main() -> int:
    import argparse

    archive_check = ROOT / "scripts" / "assert_canonical_archive.py"
    if archive_check.exists():
        rc = subprocess.call([PY, str(archive_check)])
        if rc != 0:
            return rc

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--cross-proof",
        action="store_true",
        help="Also export founding-law bundles to Coq/Isabelle/Rust obligation spine",
    )
    args = ap.parse_args()

    for script, label in STEPS:
        print(f"\n=== {label} ===")
        rc = subprocess.call([PY, str(ROOT / "scripts" / script)], cwd=str(ROOT))
        if rc != 0:
            print(f"FAILED: {script}")
            return rc

    if args.cross_proof:
        for script, label in CROSS_PROOF_EXPORT:
            print(f"\n=== {label} ===")
            rc = subprocess.call([PY, str(ROOT / "scripts" / script)], cwd=str(ROOT))
            if rc != 0:
                print(f"FAILED: {script}")
                return rc
        print("\n=== Verify founding-law cross-proof spine ===")
        rc = subprocess.call([PY, str(ROOT / "scripts" / "verify_founding_laws_cross_proof.py")], cwd=str(ROOT))
        if rc != 0:
            return rc

    print("\n[OK] Founding pipeline complete (LLM training not run).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())