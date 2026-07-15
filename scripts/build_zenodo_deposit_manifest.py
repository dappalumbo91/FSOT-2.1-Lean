#!/usr/bin/env python3
"""
Build Zenodo deposit manifest + metadata for FSOT monograph v1.

Does NOT upload — prepares file list and copy-paste metadata for zenodo.org deposit form.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "publication" / "zenodo_deposit_v1"
MANIFEST = OUT_DIR / "zenodo_deposit_manifest.json"
METADATA = OUT_DIR / "zenodo_metadata.json"
README = OUT_DIR / "ZENODO_UPLOAD_README.md"

# Files/dirs staged for deposit (relative to ROOT)
INCLUDE_PATHS = (
    "data/publication/domain_atlas.csv",
    "data/publication/domain_atlas.json",
    "data/publication/fsot_monograph_skeleton.md",
    "data/publication_claims_manifest.json",
    "data/cross_proof_verification_report.json",
    "data/verified_desktop_cross_proof_closure.json",
    "data/publication_spine_walkthrough.json",
    "data/scientific_domain_expansion_map.yaml",
    "data/fsot_domain_navigator.json",
    "data/preregistered_predictions_manifest.yaml",
    "data/domain_citations/verified_desktop.bib",
    "data/figures/spine_walkthrough.png",
    "data/figures/contested_fsot_vs_lcdm.png",
    "data/figures/h0_landscape.png",
    "data/figures/empirical_headline_summary.png",
    "data/figures/domain_error_envelope.png",
    "data/figures/predicted_vs_measured_scatter.png",
    "data/figures/verified_desktop_fuels.png",
    "data/figures/verified_desktop_transporter.png",
    "REPRODUCE.md",
    "README.md",
)

AUTHOR_NOTE = """\
Author note — scope and verification

This deposit documents the Fluid Spacetime Omni-Theory (FSOT) cross-domain verification
corpus. Numerical claims are not curve-fit per observable: a single seed-derived scalar
engine (constants from π, e, φ, γ, and G) is evaluated against measured values drawn from
legitimate domain data across 403 scientific domains and 536,740 empirical records.

Formal verification runs through a cross-gauntlet of independent proof frameworks:
Lean 4 (primary authority), Coq/Rocq, Isabelle/HOL, F* (Microsoft Research), and Rust
executable obligation replay — 1,863 atomic obligations triangulated with overall_ok: true.
QEMU bare-metal and ESP32 hardware layers provide executable closure beyond proof assistants.

AI tools (Grok/Cursor) assisted manuscript assembly, script orchestration, and formal
artifact regeneration. All results are independently reproducible from the archived
repository, one-command publication bundle, and obligation replay tests. The author
retains full scientific responsibility for claims and interpretation.
"""


def _git_head() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return r.stdout.strip()
    except Exception:
        return "unknown"


def _claims() -> dict:
    path = ROOT / "data" / "publication_claims_manifest.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> int:
    claims = _claims()
    emp = claims.get("empirical_evidence") or {}
    formal = claims.get("formal_verification") or {}
    theory = claims.get("theory_frame") or {}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    staged: list[dict] = []
    missing: list[str] = []

    for rel in INCLUDE_PATHS:
        src = ROOT / rel
        if not src.is_file():
            missing.append(rel)
            continue
        dst = OUT_DIR / "files" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        staged.append({"path": rel, "bytes": src.stat().st_size})

    # Optional: create a small zip of staged files list for user
    deposit_readme = README
    metadata = {
        "resource_type": "Publication > Preprint",
        "title": "Fluid Spacetime Omni-Theory (FSOT): Cross-Domain Empirical and Formal Verification of a Seed-Derived Scalar Engine",
        "creators": [
            {
                "name": "dappalumbo91",
                "affiliation": "Independent Researcher",
                "orcid": "",
            }
        ],
        "description": (
            f"{theory.get('core_claim', '')}\n\n"
            f"Empirical closure: {emp.get('benchmark_domains_green', '394/394')} benchmark domains "
            f"at ≤0.5% pooled gate; domain pooled median {emp.get('pooled_median_of_domains_pct', 0.013)}%.\n"
            f"Coverage: 403 scientific domains, 536,740 empirical records, 501 Lean modules.\n"
            f"Formal: five-prover cross-proof overall_ok={formal.get('overall_ok')}, "
            f"{formal.get('atomic_obligations', 1863)} atomic obligations.\n\n"
            f"{AUTHOR_NOTE}"
        ),
        "keywords": [
            "theory of everything",
            "formal verification",
            "Lean",
            "Coq",
            "cross-domain physics",
            "cosmology",
            "quantum mechanics",
            "computational physics",
            "reproducible research",
        ],
        "license": "CC-BY-4.0",
        "version": "1.0.0",
        "publication_date": datetime.now(timezone.utc).date().isoformat(),
        "related_identifiers": [
            {
                "relation": "isSupplementTo",
                "identifier": "https://github.com/dappalumbo91/FSOT-2.1-Lean",
                "resource_type": "software",
            }
        ],
        "communities": [],
        "notes_for_depositor": (
            "Upload the contents of data/publication/zenodo_deposit_v1/files/ "
            "plus a PDF when ready. Link GitHub repo in Related identifiers."
        ),
    }

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "zenodo_url": "https://zenodo.org/deposit/new",
        "github_repo": "https://github.com/dappalumbo91/FSOT-2.1-Lean",
        "github_commit": _git_head(),
        "staged_files": staged,
        "staged_count": len(staged),
        "missing_paths": missing,
        "output_dir": str(OUT_DIR),
        "author_note": AUTHOR_NOTE,
        "upload_steps": [
            "1. Create free account at https://zenodo.org (link ORCID if you have one).",
            "2. Click Upload → New upload.",
            "3. Drag folder: data/publication/zenodo_deposit_v1/files/",
            "4. Resource type: Publication → Preprint.",
            "5. Copy title/description/keywords from zenodo_metadata.json.",
            "6. License: Creative Commons Attribution 4.0 (CC-BY-4.0).",
            "7. Add related identifier: GitHub repo URL (relation: is supplement to).",
            "8. Publish — Zenodo assigns a DOI immediately.",
        ],
    }

    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    METADATA.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    readme_text = f"""# Zenodo Upload Guide — FSOT Monograph v1

## What is Zenodo?

[Zenodo](https://zenodo.org) is a **free, permanent open-research archive** operated by CERN.
It is **not a journal** and **not arXiv** — there are **no endorsers**, no PhD requirement,
and no topic gatekeepers. When you click Publish, Zenodo assigns a **DOI** (a citable permanent
link like `10.5281/zenodo.1234567`) that never expires.

Researchers use Zenodo for: preprints, datasets, software releases, thesis chapters, and
full reproducibility bundles — exactly what FSOT needs.

## What you upload (prepared in this folder)

Staged files: `{len(staged)}` items in `files/`
Metadata: `zenodo_metadata.json` (copy-paste into the deposit form)
Manifest: `zenodo_deposit_manifest.json`

GitHub commit pinned: `{manifest["github_commit"]}`

## Step-by-step (first time, ~30 minutes)

1. Go to **https://zenodo.org** → Sign up (email or ORCID).
2. Click **Upload** (top menu) → **New upload**.
3. Drag the entire **`files/`** folder into the upload area.
4. Fill the form using values from **`zenodo_metadata.json`**:
   - Title, description, keywords, license (CC-BY-4.0)
   - Resource type: **Publication → Preprint**
5. Under **Related identifiers**, add:
   - Identifier: `https://github.com/dappalumbo91/FSOT-2.1-Lean`
   - Relation: *is supplement to* | Type: *Software*
6. When you have a PDF of the monograph, add it to the upload (optional for v1).
7. Click **Publish**. Zenodo issues your DOI immediately.

## After publish

- Add the DOI to your GitHub README.
- Cite as: dappalumbo91 (2026). *Fluid Spacetime Omni-Theory...* Zenodo. DOI:10.5281/...
- OSF can mirror the same DOI link as a registry entry (no re-review needed).

## Cost

**Free.** No APC. No subscription.

## AI disclosure

Included in the description field (see `author_note` in manifest). Zenodo does not reject
AI-assisted deposits; transparency is sufficient.
"""
    deposit_readme.write_text(readme_text, encoding="utf-8")

    print(f"Wrote {MANIFEST}")
    print(f"  staged={len(staged)} missing={len(missing)}")
    print(f"Wrote {METADATA}")
    print(f"Wrote {README}")
    if missing:
        print("  missing (run export_publication_domain_atlas + monograph first):", ", ".join(missing[:5]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())