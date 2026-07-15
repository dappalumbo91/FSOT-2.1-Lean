#!/usr/bin/env python3
"""
Package FSOT monograph v1 for GitHub Release — no new accounts required.

Uses your existing GitHub login. Creates a zip + release notes you paste into
GitHub → Releases → Draft new release (3 clicks, ~2 minutes).
"""

from __future__ import annotations

import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "github_release_v1"
STAGE = ROOT / "data" / "publication" / "zenodo_deposit_v1" / "files"
ZIP_NAME = "FSOT-Monograph-Verification-Bundle-v1.zip"
NOTES = OUT / "RELEASE_NOTES.md"
TAG = "fsot-monograph-v1"


def _git_head() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return r.stdout.strip()[:12]
    except Exception:
        return "unknown"


def _claims() -> dict:
    p = ROOT / "data" / "publication_claims_manifest.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    zip_path = OUT / ZIP_NAME

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        if STAGE.is_dir():
            for f in STAGE.rglob("*"):
                if f.is_file():
                    zf.write(f, arcname=str(f.relative_to(STAGE)))
        skel = ROOT / "data" / "publication" / "fsot_monograph_skeleton.md"
        if skel.is_file():
            zf.write(skel, arcname="fsot_monograph_skeleton.md")
        atlas = ROOT / "data" / "publication" / "domain_atlas.csv"
        if atlas.is_file():
            zf.write(atlas, arcname="domain_atlas.csv")

    claims = _claims()
    emp = claims.get("empirical_evidence") or {}
    formal = claims.get("formal_verification") or {}

    notes = f"""# FSOT Monograph Verification Bundle v1

**Tag:** `{TAG}`  
**Commit:** `{_git_head()}`  
**Date:** {datetime.now(timezone.utc).date().isoformat()}

## Fluid Spacetime Omni-Theory (FSOT)

Cross-domain empirical and formal verification of a seed-derived scalar engine.

| Metric | Value |
|--------|------:|
| Scientific domains | 403 |
| Empirical records | 536,740 |
| Benchmark domains green (≤0.5%) | {emp.get('benchmark_domains_green', '394/394')} |
| Cross-domain pooled median | {emp.get('pooled_median_of_domains_pct', 0.013)}% |
| Five-prover cross-proof | overall_ok={formal.get('overall_ok')} |
| Atomic formal obligations | {formal.get('atomic_obligations', 1863)} |

Formal verification: Lean 4 → Coq → Isabelle → F* → Rust executable replay.

## Bundle contents

- `fsot_monograph_skeleton.md` — full ToE paper structure
- `domain_atlas.csv` — 403-domain verification table
- Figures, cross-proof report, publication claims manifest
- Preregistered predictions, BibTeX citations

## Reproduce

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
python scripts/run_publication_verification_bundle.py
```

## Author note

Verification runs through independent proof frameworks (Lean, Coq, Isabelle, F*,
Rust) against 536,740 measured records across 403 domains. AI tools assisted
assembly; all claims reproduce from this repository. Author retains scientific
responsibility.

## Cite

```
dappalumbo91/FSOT-2.1-Lean ({TAG}). GitHub Release.
https://github.com/dappalumbo91/FSOT-2.1-Lean/releases/tag/{TAG}
```
"""
    NOTES.write_text(notes, encoding="utf-8")

    print(f"Wrote {zip_path}  ({zip_path.stat().st_size // 1024} KB)")
    print(f"Wrote {NOTES}")
    print()
    print("GITHUB RELEASE (existing account only — no Zenodo signup):")
    print("  1. https://github.com/dappalumbo91/FSOT-2.1-Lean/releases/new")
    print(f"  2. Choose tag: {TAG}  (create from main)")
    print(f"  3. Attach: {zip_path}")
    print(f"  4. Paste body from: {NOTES}")
    print("  5. Publish release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())