#!/usr/bin/env python3
"""
Generate README thesis expansion sections from live verification artifacts.

Outputs under data/publication/readme_sections/ for incremental merge into README.md.
Tracks progress in data/publication/readme_expansion_manifest.yaml.

Run after: run_publication_verification_bundle.py
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "publication" / "readme_sections"
MANIFEST = ROOT / "data" / "publication" / "readme_expansion_manifest.yaml"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write(name: str, body: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / name
    p.write_text(body.rstrip() + "\n", encoding="utf-8")
    return p


def section_cross_verification() -> str:
    cross = _load_json(ROOT / "data/cross_proof_verification_report.json")
    closure = _load_json(ROOT / "data/verified_desktop_cross_proof_closure.json")
    spine = cross.get("full_formal_spine") or {}
    lines = [
        "## Cross-Verification Metrics (auto-generated)",
        "",
        f"*Generated: {datetime.now(timezone.utc).isoformat()}*",
        "",
        "### Five-prover formal spine",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| overall_ok | {cross.get('overall_ok')} |",
        f"| github_ready | {cross.get('github_ready')} |",
        f"| tier | {cross.get('tier', 'n/a')} |",
        f"| atomic provable obligations | {spine.get('atomic_provable_count', 'n/a')} |",
        f"| full spine obligations | {spine.get('obligation_count', 'n/a')} |",
        f"| margin violations | {spine.get('margin_violation_count', 0)} |",
        f"| seven_way_bare_metal | {cross.get('seven_way_bare_metal', 'n/a')} |",
        "",
        "Authoritative report: `data/cross_proof_verification_report.json`",
        "",
    ]
    if closure:
        lines.extend(
            [
                "### Verified desktop cross-proof closure",
                "",
                f"- verdict: **{closure.get('verdict')}**",
                f"- panels_closed: {len(closure.get('panels') or [])}",
                f"- generated_at: {closure.get('generated_at')}",
                "",
            ]
        )
    return "\n".join(lines)


def section_api_resources() -> str:
    api = _load_yaml(ROOT / "data/api_requirements.yaml")
    ext = _load_yaml(ROOT / "data/external_data_manifest.yaml")
    lines = [
        "## Data Sources and API Resources (auto-generated)",
        "",
        "Portable clone-and-verify uses bundled `vendor/` caches. Full live rebuild requires network.",
        "",
        "### Software requirements",
        "",
    ]
    sw = api.get("software_requirements") or {}
    if sw.get("lean"):
        lines.append(f"- **Lean:** `{sw['lean'].get('toolchain')}` — verify with `lake build`")
    if sw.get("python"):
        lines.append(f"- **Python:** ≥{sw['python'].get('min_version')}")
    lines.extend(["", "### Bundled authority paths", ""])
    for key, spec in (ext.get("bundled") or {}).items():
        if isinstance(spec, dict) and spec.get("path"):
            lines.append(f"- **{key}:** `{spec['path']}` — {spec.get('role', '')}")
    lines.extend(["", "### External API tiers (sample)", ""])
    for tier_key, tier in list((api.get("api_sources") or {}).items())[:8]:
        if not isinstance(tier, dict):
            continue
        lines.append(f"#### {tier_key}")
        if tier.get("ingest"):
            lines.append(f"- Ingest: `{tier['ingest']}`")
        if tier.get("build"):
            lines.append(f"- Build: `{tier['build']}`")
        for src in (tier.get("sources") or [])[:6]:
            if isinstance(src, dict):
                lines.append(f"- `{src.get('id')}`: {src.get('url', '')}")
        lines.append("")
    lines.append("Full registry: `data/api_requirements.yaml`, `data/external_data_manifest.yaml`")
    return "\n".join(lines)


def section_literature() -> str:
    bib = ROOT / "data/domain_citations/verified_desktop.bib"
    lines = [
        "## Literature and Citations (auto-generated)",
        "",
        "Domain-specific references are exported from the FSOT domain navigator and panel benchmarks.",
        "",
        "### Verified desktop BibTeX",
        "",
        f"Export command: `python scripts/export_domain_citations.py --bundle verified_desktop`",
        "",
    ]
    if bib.is_file():
        entries = bib.read_text(encoding="utf-8").count("@")
        lines.append(f"- **File:** `data/domain_citations/verified_desktop.bib` ({entries} entries)")
        preview = bib.read_text(encoding="utf-8").strip().splitlines()[:25]
        lines.extend(["", "```bibtex", *preview, "..."] if len(preview) >= 25 else ["", "```bibtex", *preview])
        lines.append("```")
    nav = _load_json(ROOT / "data/fsot_domain_navigator.json")
    route_count = len(nav.get("problem_routes") or nav.get("routes") or [])
    if route_count:
        lines.extend(["", f"Navigator routes with citation hooks: **{route_count}** (`data/fsot_domain_navigator.json`)"])
    return "\n".join(lines)


def section_domain_atlas_summary() -> str:
    atlas = ROOT / "data/publication/domain_atlas.csv"
    lines = [
        "## Domain Atlas Summary (auto-generated)",
        "",
        "Full 403-domain table: `data/publication/domain_atlas.csv`",
        "",
    ]
    if not atlas.is_file():
        lines.append("*Run `python scripts/export_publication_domain_atlas.py` to generate atlas.*")
        return "\n".join(lines)

    rows = list(csv.DictReader(atlas.read_text(encoding="utf-8").splitlines()))
    core = [r for r in rows if r.get("kind") == "core"]
    ext = [r for r in rows if r.get("kind") == "extension"]
    lines.extend(
        [
            f"| Kind | Domains |",
            f"|------|--------:|",
            f"| core | {len(core)} |",
            f"| extension | {len(ext)} |",
            f"| **total** | **{len(rows)}** |",
            "",
            "### Core domains (35 NeuroLab spine)",
            "",
            "| Domain | Records | Median err % | Tier |",
            "|--------|--------:|-------------:|------|",
        ]
    )
    for r in core[:35]:
        lines.append(
            f"| {r.get('domain','')} | {r.get('record_count','')} | {r.get('median_error_pct','')} | {r.get('coverage_tier','')} |"
        )
    lines.extend(["", "### Extension panels (first 40 of 367)", "", "| Domain | Records | Median err % | Tier |", "|--------|--------:|-------------:|------|"])
    for r in ext[:40]:
        lines.append(
            f"| {r.get('domain','')} | {r.get('record_count','')} | {r.get('median_error_pct','')} | {r.get('coverage_tier','')} |"
        )
    if len(ext) > 40:
        lines.append(f"| … | *{len(ext) - 40} more* | | |")
    return "\n".join(lines)


def section_formula_corpus() -> str:
    honesty = _load_json(ROOT / "data/formula_corpus_honesty_report.json")
    empirical = _load_json(ROOT / "data/empirical_accuracy_closure.json")
    lines = [
        "## Formula Corpus and Observables (auto-generated)",
        "",
        "Strict empirical path: `vendor/formula_corpus/strict_empirical.jsonl` (7,941 formulas)",
        "",
    ]
    if empirical:
        ev = empirical.get("headline") or empirical
        for k in ("strict_empirical_rows", "matched_rows", "within_2pct_rows", "pooled_median_pct"):
            if k in ev or k in empirical:
                val = ev.get(k, empirical.get(k))
                lines.append(f"- **{k}:** {val}")
    if honesty:
        lines.extend(["", "### Formula honesty report", ""])
        for k, v in list(honesty.items())[:12]:
            if k not in {"generated_at", "rows"}:
                lines.append(f"- {k}: {v}")
    lines.extend(
        [
            "",
            "Per-formula verification policy: `data/formula_verification_policy.yaml`",
            "Reproduce: `python scripts/run_numeric_eval_queue.py`",
        ]
    )
    return "\n".join(lines)


def section_contested_observables() -> str:
    contested = _load_json(ROOT / "data/contested_observables_closure.json")
    claims = _load_json(ROOT / "data/publication_claims_manifest.json")
    lines = [
        "## Contested Observables (auto-generated)",
        "",
    ]
    cs = claims.get("contested_sector_evidence") or {}
    if cs:
        lines.extend(
            [
                f"- Observable count: **{cs.get('observable_count')}**",
                f"- FSOT pooled median: **{cs.get('fsot_pooled_median_pct')}%**",
                f"- Typical ΛCDM/SM baseline: **{cs.get('lcdm_sm_typical_baseline_pct')}%**",
                f"- Verdict: {cs.get('verdict')}",
                "",
            ]
        )
    for row in (claims.get("h0_highlights") or [])[:8]:
        lines.append(
            f"- **{row.get('name')}:** FSOT err {row.get('fsot_error_pct')}% — ref `{row.get('reference')}`"
        )
    if contested.get("observables"):
        lines.extend(["", "### Closure detail", ""])
        for ob in contested["observables"][:15]:
            if isinstance(ob, dict):
                lines.append(f"- {ob.get('name', ob.get('id'))}: {ob.get('fsot_error_pct', ob.get('error_pct'))}%")
    return "\n".join(lines)


def section_verified_desktop() -> str:
    claims = _load_json(ROOT / "data/publication_claims_manifest.json")
    vd = claims.get("verified_desktop_evidence") or {}
    lines = [
        "## Verified Desktop Engineering Panels (auto-generated)",
        "",
        vd.get("fuel_lab_note", ""),
        "",
        vd.get("transporter_note", ""),
        "",
        "| Panel | Records | Pooled median % | Benchmark |",
        "|-------|--------:|----------------:|-----------|",
    ]
    for p in vd.get("panels") or []:
        lines.append(
            f"| {p.get('panel')} | {p.get('record_count')} | {p.get('pooled_median_error_pct')} | `{p.get('benchmark')}` |"
        )
    lines.extend(
        [
            "",
            "### FSOT-designed fuels",
            "",
            ", ".join(f"`{f}`" for f in (vd.get("fsot_designed_fuels") or [])),
            "",
            f"Gasoline baseline: `{vd.get('gasoline_baseline')}`",
            "",
            "Reproduce:",
            "```bash",
            "python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep",
            "python scripts/reproduce_domain_panel.py --panel Star_Trek_Transporter_Live_Panel --deep",
            "```",
        ]
    )
    return "\n".join(lines)


SECTION_BUILDERS = {
    "cross_verification": ("XI-A Cross-Verification Metrics", section_cross_verification),
    "api_resources": ("XI-B Data Sources and APIs", section_api_resources),
    "literature": ("XI-C Literature and Citations", section_literature),
    "domain_atlas": ("XI-D Domain Atlas", section_domain_atlas_summary),
    "formula_corpus": ("XI-E Formula Corpus", section_formula_corpus),
    "contested_observables": ("XI-F Contested Observables", section_contested_observables),
    "verified_desktop": ("XI-G Verified Desktop Panels", section_verified_desktop),
}


def main() -> int:
    import yaml

    written: list[dict] = []
    for sid, (title, builder) in SECTION_BUILDERS.items():
        fname = f"{sid}.md"
        content = builder()
        path = _write(fname, content)
        written.append(
            {
                "id": sid,
                "title": title,
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "status": "generated",
                "bytes": path.stat().st_size,
            }
        )

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Incremental README thesis expansion — merge sections into README.md Appendix XI",
        "sections": written,
        "merge_instructions": (
            "Append each file under data/publication/readme_sections/ to README.md "
            "between Appendix D and License as sections XI-A through XI-G. "
            "Re-run this script after each verification bundle refresh."
        ),
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {len(written)} sections to {OUT_DIR}")
    print(f"Manifest: {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())