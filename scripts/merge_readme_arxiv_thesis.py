#!/usr/bin/env python3
"""
Assemble arXiv-tier GitHub thesis layout:

  README.md          — main body §I–X, short appendices, stubs (navigable)
  docs/THESIS_APPENDIX_XI.md  — full verification record
  docs/THESIS_APPENDIX_XII.md — full domain-by-domain coverage
  data/publication/FSOT_THESIS_MAIN.pdf — optional pandoc export

Run after domain chapters are built:
  python scripts/build_readme_domain_chapters.py
  python scripts/merge_readme_arxiv_thesis.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
GAPS = ROOT / "data" / "publication" / "readme_arxiv_gaps"
SECTIONS = ROOT / "data" / "publication" / "readme_sections"
CHAPTERS = ROOT / "data" / "publication" / "readme_domain_chapters"
DOCS_XI = ROOT / "docs" / "THESIS_APPENDIX_XI.md"
DOCS_XII = ROOT / "docs" / "THESIS_APPENDIX_XII.md"
PDF_OUT = ROOT / "data" / "publication" / "FSOT_THESIS_MAIN.pdf"

XI_ORDER = (
    ("cross_verification", "XI-A — Cross-Verification Metrics"),
    ("api_resources", "XI-B — Data Sources and API Resources"),
    ("literature", "XI-C — Literature and Citations"),
    ("domain_atlas", "XI-D — Domain Atlas"),
    ("formula_corpus", "XI-E — Formula Corpus and Observables"),
    ("contested_observables", "XI-F — Contested Observables"),
    ("verified_desktop", "XI-G — Verified Desktop Engineering Panels"),
)

XII_CHAPTER_ORDER = (
    "00_core_spine_35.md",
    "01_cosmology_fundamental.md",
    "02_space_geophysics.md",
    "03_genomics_medicine.md",
    "03_ecology_species.md",
    "03_biology_genomics.md",
    "04_fusion_fuels.md",
    "04_periodic_superheavy.md",
    "04_materials_engineering.md",
    "04_chemistry_molecular.md",
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
    "23_appendix_xii_e_formula_digest.md",
)

MARKER = {
    "toc": ("<!-- README_TOC_START -->", "<!-- README_TOC_END -->"),
    "related": ("<!-- README_RELATED_WORK_START -->", "<!-- README_RELATED_WORK_END -->"),
    "contributions": ("<!-- README_CONTRIBUTIONS_START -->", "<!-- README_CONTRIBUTIONS_END -->"),
    "epistemology": ("<!-- README_EPISTEMOLOGY_START -->", "<!-- README_EPISTEMOLOGY_END -->"),
    "prereg": ("<!-- README_PREREG_SUMMARY_START -->", "<!-- README_PREREG_SUMMARY_END -->"),
    "bubble_bleed": ("<!-- README_BUBBLE_BLEED_START -->", "<!-- README_BUBBLE_BLEED_END -->"),
    "vi_figures": ("<!-- README_VI_EXTRA_FIGURES_START -->", "<!-- README_VI_EXTRA_FIGURES_END -->"),
    "engineering": ("<!-- README_ENGINEERING_VIII_START -->", "<!-- README_ENGINEERING_VIII_END -->"),
    "obligation_map": ("<!-- README_OBLIGATION_MAP_START -->", "<!-- README_OBLIGATION_MAP_END -->"),
    "near_miss": ("<!-- README_NEAR_MISS_START -->", "<!-- README_NEAR_MISS_END -->"),
    "credibility": ("<!-- README_CREDIBILITY_HARDENING_START -->", "<!-- README_CREDIBILITY_HARDENING_END -->"),
    "circuitry": ("<!-- README_CIRCUITRY_ROADMAP_START -->", "<!-- README_CIRCUITRY_ROADMAP_END -->"),
    "practical_pipeline": ("<!-- README_PRACTICAL_PIPELINE_START -->", "<!-- README_PRACTICAL_PIPELINE_END -->"),
    "discussion_open": ("<!-- README_DISCUSSION_OPEN_WORK_START -->", "<!-- README_DISCUSSION_OPEN_WORK_END -->"),
    "appendix_c_extra": ("<!-- README_APPENDIX_C_EXTRA_START -->", "<!-- README_APPENDIX_C_EXTRA_END -->"),
    "methods": ("<!-- README_METHODS_FORMAL_START -->", "<!-- README_METHODS_FORMAL_END -->"),
    "xi_stub": ("<!-- README_APPENDIX_XI_STUB_START -->", "<!-- README_APPENDIX_XI_STUB_END -->"),
    "xii_stub": ("<!-- README_APPENDIX_XII_STUB_START -->", "<!-- README_APPENDIX_XII_STUB_END -->"),
    "notation": ("<!-- README_APPENDIX_NOTATION_START -->", "<!-- README_APPENDIX_NOTATION_END -->"),
    "xi_full": ("<!-- README_THESIS_EXPANSION_START -->", "<!-- README_THESIS_EXPANSION_END -->"),
    "xii_full": ("<!-- README_DOMAIN_CHAPTERS_START -->", "<!-- README_DOMAIN_CHAPTERS_END -->"),
}


def _read_gap(name: str) -> str:
    path = GAPS / name
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def _replace_block(text: str, start: str, end: str, body: str) -> str:
    block = f"{start}\n{body.rstrip()}\n{end}\n"
    if start in text and end in text:
        pattern = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}\n?", flags=re.DOTALL)
        return pattern.sub(lambda _m: block, text, count=1)
    return text


def _insert_after(text: str, anchor: str, block: str) -> str:
    if anchor not in text:
        return text
    return text.replace(anchor, anchor + "\n\n" + block.rstrip() + "\n", 1)


def _strip_block(text: str, start: str, end: str) -> str:
    if start not in text:
        return text
    return re.sub(rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?", "\n", text, flags=re.DOTALL)


def _section_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    return re.sub(r"^#+ [^\n]+\n+", "", text, count=1).strip()


def _assemble_appendix_xi(ts: str) -> str:
    parts = [
        "# Appendix XI — Full Verification Record",
        "",
        f"*Edition fragment · {ts} · "
        "[Return to main thesis](../README.md#appendix-xi--full-verification-record-summary)",
        "",
        "```bash",
        "python scripts/run_publication_verification_bundle.py --full-cross-proof",
        "python scripts/build_readme_thesis_expansion.py",
        "python scripts/merge_readme_thesis_expansion.py",
        "```",
        "",
    ]
    for slug, title in XI_ORDER:
        path = SECTIONS / f"{slug}.md"
        if not path.is_file():
            continue
        parts.extend([f"## {title}", "", _section_body(path), ""])
    return "\n".join(parts).rstrip() + "\n"


def _assemble_appendix_xii(ts: str) -> str:
    parts = [
        "# Appendix XII — Domain-by-Domain Scientific Coverage",
        "",
        f"*Edition fragment · {ts} · "
        "[Return to main thesis](../README.md#appendix-xii--domain-by-domain-scientific-coverage-summary)",
        "",
        f"Chapter index: [`data/publication/readme_domain_chapters/INDEX.md`]"
        f"(../data/publication/readme_domain_chapters/INDEX.md)",
        "",
        "```bash",
        "python scripts/build_readme_domain_chapters.py",
        "python scripts/merge_readme_domain_chapters.py",
        "```",
        "",
    ]
    for fname in XII_CHAPTER_ORDER:
        path = CHAPTERS / fname
        if not path.is_file():
            continue
        parts.append(_section_body(path))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def _patch_section_iii_equations(text: str) -> str:
    eq = _read_gap("equations_iii.md")
    if not eq:
        return text
    old = re.search(
        r"### 3\.1 The heartbeat\n\n.*?(?=\n### 3\.2 )",
        text,
        flags=re.DOTALL,
    )
    if old:
        return text[: old.start()] + eq.rstrip() + "\n\n" + text[old.end() :]
    return text


def _renumber_cite_appendix(text: str) -> str:
    text = text.replace("## Appendix D — How to Cite This Work", "## Appendix E — How to Cite This Work")
    return text


def _try_pdf(main_md: Path) -> None:
    html_out = PDF_OUT.with_suffix(".html")
    engines = [
        ["pandoc", str(main_md), "-o", str(PDF_OUT), "--pdf-engine=xelatex"],
        ["pandoc", str(main_md), "-o", str(PDF_OUT), "--pdf-engine=lualatex"],
        ["pandoc", str(main_md), "-o", str(html_out), "-s", "--metadata", "title=FSOT Thesis Main Body"],
    ]
    for cmd in engines:
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Wrote {cmd[-1]}")
            return
        except FileNotFoundError:
            print("pandoc not installed — skip PDF/HTML export")
            return
        except subprocess.CalledProcessError:
            continue
    print("pandoc PDF engines failed — no export written")


_GAP_FILES = {
    "contributions": "contributions.md",
    "epistemology": "epistemology.md",
    "prereg": "prereg_summary.md",
    "bubble_bleed": "bubble_bleed.md",
    "vi_figures": "vi_extra_figures.md",
    "obligation_map": "obligation_map.md",
    "near_miss": "near_miss.md",
    "credibility": "credibility_hardening.md",
    "circuitry": "circuitry_roadmap.md",
    "practical_pipeline": "practical_pipeline.md",
    "discussion_open": "discussion_open_work.md",
}


def _patch_inline_citations(text: str) -> str:
    """Tier C — weave authority citations into main-body prose."""
    replacements = (
        (
            "On contested sectors where ΛCDM and the Standard Model typically show ~15% baseline tension "
            "(H₀, σ₈, BBN proxies, hierarchy, dark-energy equation of state)",
            "On contested sectors where ΛCDM (Planck Collaboration 2018) and the Standard Model (PDG 2024) "
            "typically show ~15% baseline tension (H₀ per Riess et al. 2024; σ₈; BBN proxies; hierarchy; dark-energy equation of state)",
        ),
        (
            "**Design law:** we do not add a new dial every time a prediction fails.",
            "**Design law:** we do not add a new dial every time a prediction fails (contrast with ΛCDM's six-parameter extension; Planck Collaboration 2018).",
        ),
        (
            "Brain metabolic power `E_con` ≈ 21.79 W vs ~20 W measured (Raichle & Gusnard)",
            "Brain metabolic power `E_con` ≈ 21.79 W vs ~20 W measured (Raichle & Gusnard 2002)",
        ),
        (
            "Full atlas: [`data/publication/domain_atlas.csv`](data/publication/domain_atlas.csv) (402 rows)",
            "Full atlas: [`data/publication/domain_atlas.csv`](data/publication/domain_atlas.csv) (402 rows; measured targets per NIST, PDG, Planck-class surveys as cited per row)",
        ),
        (
            "- Measured: 67.36 ± 0.54 km/s/Mpc",
            "- Measured: 67.36 ± 0.54 km/s/Mpc (Planck Collaboration 2018)",
        ),
    )
    for old, new in replacements:
        if old in text and new not in text:
            text = text.replace(old, new, 1)
    return text


def _ensure_marker_block(text: str, key: str, anchor: str, before: bool = False) -> str:
    start, end = MARKER[key]
    gap_name = _GAP_FILES.get(key)
    if not gap_name:
        return text
    if start in text:
        return _replace_block(text, start, end, _read_gap(gap_name))
    body = _read_gap(gap_name)
    if not body or anchor not in text:
        return text
    block = f"\n\n{start}\n{body}\n{end}\n"
    if before:
        return text.replace(anchor, block + anchor)
    return text.replace(anchor, anchor + block)


def _reconcile_domain_counts(text: str) -> str:
    """402 routed = 35 core + 367 extension (authoritative navigator/atlas)."""
    replacements = (
        (r"\b403 scientific domains\b", "402 routed scientific domains (35 core + 367 extension)"),
        (r"\b403 domains\b", "402 routed domains"),
        (r"\b403-domain atlas\b", "402-domain atlas"),
        (r"\b403-domain verification table\b", "402-domain verification table"),
        (r"\(403 rows\)", "(402 rows)"),
        (r"\| Scientific domains \| 403 \|", "| Scientific domains | 402 |"),
        (r"over the 403-domain atlas", "over the 402-domain atlas"),
        (r"### 6\.3 Domain-by-domain coverage \(403 domains\)", "### 6.3 Domain-by-domain coverage (402 domains)"),
    )
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    return text


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    tier_c_scripts = (
        "build_mechanism_chain_derivation.py",
        "build_thesis_appendix_derivations.py",
        "build_verified_desktop_transporter_paper.py",
        "build_benchmark_near_miss_ledger.py",
        "build_obligation_map_figure.py",
        "build_contested_sector_watch.py",
        "build_skeptic_replication_kit.py",
        "build_monograph_abstract.py",
        "build_readme_arxiv_gaps.py",
        "build_circuit_component_atlas_scaffold.py",
        "build_wetlab_longevity_volume.py",
        "build_credibility_hardening_audit.py",
        "build_lean_route_credibility_expansion.py",
        "build_circuit_component_expansion_bundle.py",
        "build_practical_pipeline_bundle.py",
    )
    for script in tier_c_scripts:
        subprocess.run([sys.executable, str(ROOT / "scripts" / script)], check=False)

    DOCS_XI.parent.mkdir(parents=True, exist_ok=True)
    DOCS_XI.write_text(_assemble_appendix_xi(ts), encoding="utf-8")
    DOCS_XII.write_text(_assemble_appendix_xii(ts), encoding="utf-8")
    print(f"Wrote {DOCS_XI}")
    print(f"Wrote {DOCS_XII}")

    readme = README.read_text(encoding="utf-8")

    # Remove inlined full appendices from README
    readme = _strip_block(readme, *MARKER["xi_full"])
    readme = _strip_block(readme, *MARKER["xii_full"])

    # Insert / replace arXiv gap blocks
    readme = _replace_block(readme, *MARKER["toc"], _read_gap("toc.md"))
    readme = _replace_block(readme, *MARKER["related"], _read_gap("related_work.md"))
    readme = _replace_block(readme, *MARKER["methods"], _read_gap("methods_formal.md"))
    readme = _replace_block(readme, *MARKER["xi_stub"], _read_gap("xi_stub.md"))
    readme = _replace_block(readme, *MARKER["xii_stub"], _read_gap("xii_stub.md"))
    readme = _replace_block(readme, *MARKER["notation"], _read_gap("notation.md"))
    readme = _replace_block(readme, *MARKER["contributions"], _read_gap("contributions.md"))
    readme = _replace_block(readme, *MARKER["epistemology"], _read_gap("epistemology.md"))
    readme = _replace_block(readme, *MARKER["prereg"], _read_gap("prereg_summary.md"))
    readme = _replace_block(readme, *MARKER["bubble_bleed"], _read_gap("bubble_bleed.md"))
    readme = _replace_block(readme, *MARKER["vi_figures"], _read_gap("vi_extra_figures.md"))
    readme = _replace_block(readme, *MARKER["engineering"], _read_gap("engineering_viii.md"))
    readme = _replace_block(readme, *MARKER["obligation_map"], _read_gap("obligation_map.md"))
    readme = _replace_block(readme, *MARKER["near_miss"], _read_gap("near_miss.md"))
    readme = _replace_block(readme, *MARKER["credibility"], _read_gap("credibility_hardening.md"))
    readme = _replace_block(readme, *MARKER["circuitry"], _read_gap("circuitry_roadmap.md"))
    readme = _replace_block(readme, *MARKER["practical_pipeline"], _read_gap("practical_pipeline.md"))
    if MARKER["discussion_open"][0] in readme:
        readme = _replace_block(readme, *MARKER["discussion_open"], _read_gap("discussion_open_work.md"))
    if MARKER["appendix_c_extra"][0] in readme:
        readme = _replace_block(readme, *MARKER["appendix_c_extra"], _read_gap("appendix_c_extra.md"))

    # First-time inserts if markers missing
    if MARKER["toc"][0] not in readme:
        readme = _insert_after(
            readme,
            "The GitHub commit history is the edition record. Tagged releases are the volumes.\n\n---",
            f"\n\n{MARKER['toc'][0]}\n{_read_gap('toc.md')}\n{MARKER['toc'][1]}",
        )
    if MARKER["contributions"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "contributions",
            "(`predictions/preregistered_predictions_manifest.yaml`).\n\n---",
        )
    if MARKER["related"][0] not in readme:
        anchor = (
            "(`predictions/preregistered_predictions_manifest.yaml`).\n\n---\n\n## II. Why the Universe Exists"
        )
        if anchor in readme:
            readme = readme.replace(
                anchor,
                "(`predictions/preregistered_predictions_manifest.yaml`).\n\n---\n\n"
                f"{MARKER['related'][0]}\n{_read_gap('related_work.md')}\n{MARKER['related'][1]}\n\n"
                "## II. Why the Universe Exists",
            )
    if MARKER["epistemology"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "epistemology",
            "<!-- README_RELATED_WORK_END -->\n\n## II. Why the Universe Exists",
            before=True,
        )
    if MARKER["prereg"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "prereg",
            "If the engine fails a green gate, the ledger records it — no narrative escape hatch.\n\n---",
        )
    if MARKER["bubble_bleed"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "bubble_bleed",
            "![Contested FSOT vs ΛCDM](data/figures/contested_fsot_vs_lcdm.png)\n\n### 7.1 H₀ landscape",
            before=True,
        )
    if MARKER["vi_figures"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "vi_figures",
            "![Predicted vs measured scatter](data/figures/predicted_vs_measured_scatter.png)\n\n### 6.2 Representative domains",
        )
    if MARKER["engineering"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "engineering",
            "## VIII. Engineering Demonstrations",
        )
    if MARKER["credibility"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "credibility",
            "<!-- README_NEAR_MISS_END -->",
        )
    if MARKER["circuitry"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "circuitry",
            "<!-- README_CREDIBILITY_HARDENING_END -->",
        )
    if MARKER["practical_pipeline"][0] not in readme:
        readme = _ensure_marker_block(
            readme,
            "practical_pipeline",
            "<!-- README_CIRCUITRY_ROADMAP_END -->",
        )
    if MARKER["discussion_open"][0] not in readme:
        old_open = re.search(
            r"### 9\.3 Open work \(not model failures\)\n\n.*?(?=\n<!-- README_NEAR_MISS_START -->)",
            readme,
            flags=re.DOTALL,
        )
        if old_open:
            block = (
                f"{MARKER['discussion_open'][0]}\n{_read_gap('discussion_open_work.md')}\n"
                f"{MARKER['discussion_open'][1]}"
            )
            readme = readme[: old_open.start()] + block + readme[old_open.end() :]
    if MARKER["appendix_c_extra"][0] not in readme:
        anchor = "| [`predictions/reports/CONTESTED_SECTOR_WATCH.md`](predictions/reports/CONTESTED_SECTOR_WATCH.md) | Contested-sector living watch |"
        if anchor in readme:
            extra = _read_gap("appendix_c_extra.md").strip()
            readme = readme.replace(anchor, anchor + "\n" + extra)
            readme = readme.replace(
                anchor + "\n" + extra,
                anchor + "\n\n<!-- README_APPENDIX_C_EXTRA_START -->\n" + extra + "\n<!-- README_APPENDIX_C_EXTRA_END -->",
                1,
            )
    if MARKER["methods"][0] not in readme:
        readme = _insert_after(
            readme,
            "### 5.4 AI assistance — human responsibility",
            f"{MARKER['methods'][0]}\n{_read_gap('methods_formal.md')}\n{MARKER['methods'][1]}",
        )

    readme = _patch_section_iii_equations(readme)
    readme = _renumber_cite_appendix(text=readme)

    if MARKER["xi_stub"][0] not in readme:
        anchor = "## Appendix C — Further Reading"
        end_marker = "---\n\n\n\n<!-- README_APPENDIX_NOTATION_START -->"
        stub_block = (
            f"\n\n---\n\n{MARKER['xi_stub'][0]}\n{_read_gap('xi_stub.md')}\n{MARKER['xi_stub'][1]}\n\n"
            f"{MARKER['xii_stub'][0]}\n{_read_gap('xii_stub.md')}\n{MARKER['xii_stub'][1]}\n"
        )
        if end_marker in readme:
            readme = readme.replace(end_marker, stub_block + end_marker)
        elif anchor in readme:
            # Insert stubs after Appendix C body (before notation)
            parts = readme.split(anchor, 1)
            if len(parts) == 2:
                rest = parts[1]
                split = rest.split("\n---\n", 1)
                if len(split) == 2:
                    readme = parts[0] + anchor + split[0] + stub_block + "\n---\n" + split[1]

    if MARKER["notation"][0] not in readme:
        cite_anchor = "## Appendix E — How to Cite This Work"
        if cite_anchor not in readme:
            cite_anchor = "## Appendix D — How to Cite This Work"
        if cite_anchor in readme:
            readme = readme.replace(
                cite_anchor,
                f"{MARKER['notation'][0]}\n{_read_gap('notation.md')}\n{MARKER['notation'][1]}\n\n{cite_anchor}",
            )

    readme = _reconcile_domain_counts(readme)
    readme = _patch_inline_citations(readme)
    readme = re.sub(
        r"\*\*Edition:\*\* v[0-9]+\.[0-9]+[^\n]*",
        f"**Edition:** v2.6 — FluidLink archive, desktop observer loop, local bundle {ts}",
        readme,
        count=1,
    )

    # Update §6.3 appendix links to docs volumes
    readme = re.sub(
        r"\(#appendix-xii--domain-by-domain-scientific-coverage-[^\)]+\)",
        "(../docs/THESIS_APPENDIX_XII.md)",
        readme,
    )
    readme = re.sub(
        r"\(#appendix-xii-e--formula-exemplar-digest[^\)]*\)",
        "(../docs/THESIS_APPENDIX_XII.md#appendix-xii-e--formula-exemplar-digest-strict-empirical)",
        readme,
    )

    README.write_text(readme, encoding="utf-8")

    main_export = ROOT / "data" / "publication" / "FSOT_THESIS_MAIN.md"
    # Export main body only (through License) for PDF
    end = readme.find("## License")
    if end > 0:
        main_export.write_text(readme[:end].rstrip() + "\n", encoding="utf-8")
        _try_pdf(main_export)

    subprocess.run([sys.executable, str(ROOT / "scripts/build_thesis_completeness_audit.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/build_publication_supplementary_bundle.py")], check=False)

    lines = readme.count("\n") + 1
    print(f"README.md assembled: {lines:,} lines (was ~13,000 inlined)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())