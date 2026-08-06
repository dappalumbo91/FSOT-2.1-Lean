#!/usr/bin/env python3
"""Build fsot-monograph-v2.1 supplementary zip + release notes."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "fsot-monograph-v2.1"
OUT_DIR = ROOT / "data" / "publication" / f"github_release_{TAG.replace('.', '_')}"
ZIP_NAME = f"FSOT-Monograph-Supplementary-{TAG}.zip"

INCLUDE = (
    "README.md",
    "REPRODUCE.md",
    "docs/THESIS_APPENDIX_XI.md",
    "docs/THESIS_APPENDIX_XII.md",
    "docs/THESIS_APPENDIX_DERIVATIONS.md",
    "docs/SKEPTIC_REPLICATION_KIT.md",
    "docs/VERIFIED_DESKTOP_TRANSPORTER.md",
    "data/publication/FSOT_THESIS_MAIN.md",
    "data/publication/domain_atlas.csv",
    "data/publication_claims_manifest.json",
    "data/cross_proof_verification_report.json",
    "data/contested_observables_closure.json",
    "data/publication/BENCHMARK_NEAR_MISS_LEDGER.md",
    "predictions/reports/CONTESTED_SECTOR_WATCH.md",
    "data/publication/THESIS_COMPLETENESS_AUDIT.md",
    "predictions/preregistered_predictions_manifest.yaml",
    "data/figures/spine_walkthrough.png",
    "data/figures/obligation_map_five_provers.png",
    "data/figures/empirical_headline_summary.png",
    "data/figures/contested_fsot_vs_lcdm.png",
    "data/figures/h0_landscape.png",
    "data/figures/verified_desktop_fuels.png",
)


def _git_head() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT), capture_output=True, text=True, check=True)
        return r.stdout.strip()[:12]
    except Exception:
        return "unknown"


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/build_monograph_abstract.py")], check=True, cwd=str(ROOT))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = OUT_DIR / ZIP_NAME
    missing: list[str] = []

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in INCLUDE:
            src = ROOT / rel
            if src.is_file():
                zf.write(src, arcname=rel)
            else:
                missing.append(rel)
        skel = ROOT / "data/publication/fsot_monograph_skeleton.md"
        if skel.is_file():
            zf.write(skel, arcname="data/publication/fsot_monograph_skeleton.md")

    claims = json.loads((ROOT / "data/publication_claims_manifest.json").read_text(encoding="utf-8"))
    emp = claims.get("empirical_evidence") or {}
    notes = f"""# FSOT Monograph Supplementary Bundle {TAG}

**Tag:** `{TAG}`  
**Commit:** `{_git_head()}`  
**Date:** {datetime.now(timezone.utc).date().isoformat()}

## Contents

Main thesis (`README.md`), appendices XI/XII, derivations, skeptic kit, domain atlas, verification reports, contested-sector watch, near-miss ledger, key figures.

## Headline metrics

| Metric | Value |
|--------|------:|
| Benchmark green | {emp.get('benchmark_domains_green', '394/394')} |
| Pooled median | {emp.get('pooled_median_of_domains_pct', 0.013)}% |
| Routed domains | 402 (35 + 367) |

## Reproduce

```bash
python scripts/run_publication_verification_bundle.py --full-cross-proof
```

## GitHub release

https://github.com/dappalumbo91/FSOT-2.1-Lean/releases/new — attach `{ZIP_NAME}`, tag `{TAG}`.

Missing optional files: {', '.join(missing) if missing else 'none'}
"""
    (OUT_DIR / "RELEASE_NOTES.md").write_text(notes, encoding="utf-8")
    print(f"Wrote {zip_path} ({zip_path.stat().st_size // 1024} KB)")
    print(f"Wrote {OUT_DIR / 'RELEASE_NOTES.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())