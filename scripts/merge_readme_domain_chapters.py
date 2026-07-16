#!/usr/bin/env python3
"""Merge domain chapters into README.md Appendix XII."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CHAPTERS = ROOT / "data" / "publication" / "readme_domain_chapters"
MANIFEST = ROOT / "data" / "publication" / "readme_domain_chapters_manifest.yaml"

MARKER_START = "<!-- README_DOMAIN_CHAPTERS_START -->"
MARKER_END = "<!-- README_DOMAIN_CHAPTERS_END -->"

CHAPTER_ORDER = (
    "00_core_spine_35.md",
    "01_cosmology_fundamental.md",
    "02_space_geophysics.md",
    "03_biology_genomics.md",
    "04_chemistry_materials.md",
    "05_consciousness_social.md",
    "06_engineering_propulsion.md",
    "07_mathematics_computation.md",
    "08_cybersecurity.md",
    "09_founding_laws.md",
    "10_live_ingest_astrometry.md",
    "11_fluid_spacetime_time.md",
    "12_finance_economics_logistics.md",
    "13_music_arts_creative.md",
    "14_government_open_data.md",
    "15_arxiv_meta_folding_spines.md",
    "16_prereg_scaffolds.md",
    "17_llm_agents_oracles.md",
    "18_public_biology_longevity.md",
    "19_physics_engineering_depth.md",
    "20_mathematics_formal_depth.md",
    "21_verification_infrastructure.md",
    "22_interdisciplinary_residual.md",
)


def _body(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    return re.sub(r"^#+ [^\n]+\n+", "", text, count=1).strip()


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    parts = [
        MARKER_START,
        f"## Appendix XII — Domain-by-Domain Scientific Coverage ({ts})",
        "",
        "Verbose verification record for every core domain and extension panel. "
        "Regenerate after verification bundle refresh:",
        "",
        "```bash",
        "python scripts/build_readme_domain_chapters.py",
        "python scripts/merge_readme_domain_chapters.py",
        "```",
        "",
        f"Chapter index: [`data/publication/readme_domain_chapters/INDEX.md`](data/publication/readme_domain_chapters/INDEX.md)",
        "",
    ]
    for fname in CHAPTER_ORDER:
        path = CHAPTERS / fname
        if not path.is_file():
            continue
        parts.append(_body(path))
        parts.append("")
    parts.append(MARKER_END)

    block = "\n".join(parts).rstrip() + "\n"
    readme = README.read_text(encoding="utf-8")

    if MARKER_START in readme:
        readme = re.sub(
            rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?",
            block,
            readme,
            flags=re.DOTALL,
        )
    else:
        anchor = "## Appendix D — How to Cite This Work"
        if anchor not in readme:
            print("Missing Appendix D anchor in README.md")
            return 1
        readme = readme.replace(anchor, block + "\n" + anchor)

    readme = re.sub(
        r"\*\*Edition:\*\* v1\.[0-9]+[^\n]*",
        f"**Edition:** v1.3 — domain chapters deepening {ts}",
        readme,
        count=1,
    )

    README.write_text(readme, encoding="utf-8")
    merged = sum(1 for f in CHAPTER_ORDER if (CHAPTERS / f).is_file())
    print(f"Merged {merged} domain chapters into {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())