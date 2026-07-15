#!/usr/bin/env python3
"""Merge data/publication/readme_sections/*.md into README.md Appendix XI."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SECTIONS = ROOT / "data" / "publication" / "readme_sections"

ORDER = (
    ("cross_verification", "XI-A — Cross-Verification Metrics"),
    ("api_resources", "XI-B — Data Sources and API Resources"),
    ("literature", "XI-C — Literature and Citations"),
    ("domain_atlas", "XI-D — Domain Atlas"),
    ("formula_corpus", "XI-E — Formula Corpus and Observables"),
    ("contested_observables", "XI-F — Contested Observables"),
    ("verified_desktop", "XI-G — Verified Desktop Engineering Panels"),
)

MARKER_START = "<!-- README_THESIS_EXPANSION_START -->"
MARKER_END = "<!-- README_THESIS_EXPANSION_END -->"


def _section_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    # Drop auto-generated H2; content becomes ### blocks under Appendix XI
    text = re.sub(r"^## [^\n]+\n+", "", text, count=1)
    return text.strip()


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    parts = [
        MARKER_START,
        f"## Appendix XI — Full Verification Record (expansive run {ts})",
        "",
        "This appendix is regenerated from live verification artifacts after each full cross-proof pass.",
        "",
        "```bash",
        "python scripts/run_publication_verification_bundle.py --full-cross-proof",
        "python scripts/build_readme_thesis_expansion.py",
        "python scripts/merge_readme_thesis_expansion.py",
        "```",
        "",
    ]
    for slug, title in ORDER:
        path = SECTIONS / f"{slug}.md"
        if not path.is_file():
            print(f"Missing section: {path}")
            return 1
        parts.append(f"### {title}")
        parts.append("")
        parts.append(_section_body(path))
        parts.append("")
    parts.append(MARKER_END)

    block = "\n".join(parts).rstrip() + "\n"
    readme = README.read_text(encoding="utf-8")

    # Replace existing expansion block or legacy Appendix E
    if MARKER_START in readme:
        readme = re.sub(
            rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?",
            block,
            readme,
            flags=re.DOTALL,
        )
    else:
        legacy = re.search(
            r"## Appendix E — Thesis Expansion Run.*?(?=\n## Appendix D|\n## License|\Z)",
            readme,
            flags=re.DOTALL,
        )
        if legacy:
            readme = readme[: legacy.start()] + block + readme[legacy.end() :]
        else:
            insert_before = "## Appendix D — How to Cite This Work"
            if insert_before not in readme:
                print("Could not find insertion point in README.md")
                return 1
            readme = readme.replace(insert_before, block + "\n" + insert_before)

    # Update edition stamp
    readme = re.sub(
        r"\*\*Edition:\*\* v1\.0[^\n]*",
        f"**Edition:** v1.1 — expansive run {ts} (full cross-proof)",
        readme,
        count=1,
    )

    README.write_text(readme, encoding="utf-8")
    print(f"Merged {len(ORDER)} sections into {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())