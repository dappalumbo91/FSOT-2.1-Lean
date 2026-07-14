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
    ("audit_founding_35_laws.py", "Audit 35 founding laws"),
    ("reconcile_founding_corpus.py", "Reconcile founding text corpus"),
    ("verify_founding_corpus.py", "Verify founding corpus gate"),
]


def main() -> int:
    for script, label in STEPS:
        print(f"\n=== {label} ===")
        rc = subprocess.call([PY, str(ROOT / "scripts" / script)], cwd=str(ROOT))
        if rc != 0:
            print(f"FAILED: {script}")
            return rc
    print("\n[OK] Founding pipeline complete (LLM training not run).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())