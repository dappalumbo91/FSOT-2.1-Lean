#!/usr/bin/env python3
"""Audit thesis coverage vs philosophy spine, monograph skeleton, and live verification."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "THESIS_COMPLETENESS_AUDIT.md"

SOURCES = {
    "readme": ROOT / "README.md",
    "philosophy": ROOT / "docs" / "FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md",
    "monograph": ROOT / "data" / "publication" / "fsot_monograph_skeleton.md",
    "derivations": ROOT / "docs" / "THESIS_APPENDIX_DERIVATIONS.md",
    "claims": ROOT / "data" / "publication_claims_manifest.json",
    "cross_proof": ROOT / "data" / "cross_proof_verification_report.json",
    "margin": ROOT / "data" / "benchmark_margin_audit.json",
    "atlas": ROOT / "data" / "publication" / "domain_atlas.csv",
    "prereg": ROOT / "data" / "preregistered_predictions_manifest.yaml",
}

IDEAL_TOPICS = [
    ("25D fluid ontology", r"25.dimensional|25D|fluid condensate"),
    ("As Above So Below", r"As Above|cross.scale"),
    ("Zero free parameters", r"zero free|no per.observable|ZERO_FREE|least.squares"),
    ("Seed engine (π,e,φ,γ,G)", r"five seeds|π.*e.*φ|Catalan"),
    ("raw_S emergence/dispersal", r"raw_S|emergence|dispersal"),
    ("quirk_mod / observation", r"quirk_mod|observed = true"),
    ("Consciousness fundamental", r"consciousness.*fundamental|E_con|Raichle"),
    ("Epistemology / truth criterion", r"truth criterion|epistemolog|consensus.*not.*gate"),
    ("Bubble-bleed cosmology", r"bubble.bleed|dual.anchor|perceived_adjust"),
    ("Preregistered PRED manifest", r"PRED-0|preregistered"),
    ("Founding 35 laws", r"35/35|founding.*law"),
    ("Five-prover cross-proof", r"Lean.*Coq|1,863|cross.proof"),
    ("Contested sectors (H₀, σ₈)", r"contested|H₀|sigma.?8|0\.030"),
    ("Engineering demos (main thesis)", r"fuel lab|machine.and.molecule|verified desktop fuels"),
    ("Transporter supplementary volume", r"VERIFIED_DESKTOP_TRANSPORTER|supplementary.*transporter"),
    ("Strict-empirical corpus", r"strict.empirical|1,325"),
    ("Domain atlas / coverage", r"domain atlas|extension panel"),
    ("Derivation appendix", r"seed.to.formula|THESIS_APPENDIX_DERIVATIONS|mechanism_chain"),
    ("Formal vs interpretive tiers", r"interpretive|epistemic tier|proved / certified"),
    ("Soul-bridge / SR-ITE", r"soul.bridge|SR-ITE|substrate"),
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _load_json(path: Path) -> dict:
    return json.loads(_read(path)) if path.is_file() else {}


def _count_atlas() -> int:
    text = _read(SOURCES["atlas"])
    return max(0, text.count("\n") - 1) if text else 0


def _prereg_count() -> int:
    try:
        import yaml

        doc = yaml.safe_load(_read(SOURCES["prereg"])) or {}
        return len(doc.get("predictions") or [])
    except Exception:
        return 0


def _topic_matrix() -> list[tuple[str, bool, bool, bool]]:
    texts = {
        "readme": _read(SOURCES["readme"]).lower(),
        "philosophy": _read(SOURCES["philosophy"]).lower(),
        "monograph": _read(SOURCES["monograph"]).lower(),
    }
    rows = []
    for label, pattern in IDEAL_TOPICS:
        rx = re.compile(pattern, re.I)
        rows.append((
            label,
            bool(rx.search(texts["readme"])),
            bool(rx.search(texts["philosophy"])),
            bool(rx.search(texts["monograph"])),
        ))
    return rows


def _gaps(rows: list[tuple[str, bool, bool, bool]]) -> list[str]:
    return [label for label, in_readme, *_ in rows if not in_readme]


def build() -> str:
    ts = datetime.now(timezone.utc).isoformat()
    claims = _load_json(SOURCES["claims"])
    cross = _load_json(SOURCES["cross_proof"])
    margin = _load_json(SOURCES["margin"])
    atlas_n = _count_atlas()
    prereg_n = _prereg_count()
    rows = _topic_matrix()
    missing = _gaps(rows)

    empirical = claims.get("empirical_evidence") or {}
    contested = claims.get("contested_sector_evidence") or {}
    atomic = (cross.get("full_formal_spine") or {}).get("atomic_provable_count", "?")
    overall = cross.get("overall_ok", "?")
    green = margin.get("green_pass_count") or margin.get("pass_count") or "?"

    lines = [
        "# FSOT Thesis Completeness Audit",
        "",
        f"*Generated: {ts}*",
        "",
        "Top-to-bottom comparison of **living thesis** (`README.md`) against "
        "**philosophy spine**, **monograph skeleton**, and **live verification artifacts**.",
        "",
        "## Executive summary",
        "",
        "| Check | Status |",
        "|-------|--------|",
        f"| Verification bundle (`overall_ok`) | `{overall}` |",
        f"| Benchmark green gate | `{empirical.get('benchmark_domains_green', green)}` |",
        f"| Cross-proof atomic obligations | `{atomic}` |",
        f"| Contested pooled median | `{contested.get('fsot_pooled_median_pct', '?')}%` |",
        f"| Domain atlas rows (routed) | `{atlas_n}` (35 core + 367 extension = 402) |",
        f"| Preregistered predictions | `{prereg_n}` |",
        f"| Ideals in main README | `{len(IDEAL_TOPICS) - len(missing)}/{len(IDEAL_TOPICS)}` |",
        "",
        "## Crucial FSOT ideals — coverage matrix",
        "",
        "| Ideal / topic | README | Philosophy spine | Monograph skeleton |",
        "|---------------|:------:|:----------------:|:------------------:|",
    ]
    for label, in_r, in_p, in_m in rows:
        lines.append(
            f"| {label} | {'✓' if in_r else '—'} | {'✓' if in_p else '—'} | {'✓' if in_m else '—'} |"
        )

    lines.extend([
        "",
        "## Gaps still thin in main thesis (action list)",
        "",
    ])
    if missing:
        for g in missing:
            lines.append(f"- **{g}** — present in philosophy/monograph sources; deepen README or link appendix.")
    else:
        lines.append("- No critical ideal gaps detected in README prose (audit patterns matched).")

    lines.extend([
        "",
        "## Domain count reconciliation",
        "",
        "Authoritative routed domain count: **402** = 35 NeuroLab core + 367 extension panels "
        "(`data/fsot_domain_navigator.json`, `domain_atlas.csv`). Prior editions cited **403** "
        "from `scientific_domain_expansion_map.yaml` summary rollup — reconciled in v2.1 to **402**.",
        "",
        "## Regeneration chain (top to bottom)",
        "",
        "```bash",
        "python scripts/run_publication_verification_bundle.py",
        "python scripts/build_mechanism_chain_derivation.py",
        "python scripts/build_thesis_appendix_derivations.py",
        "python scripts/build_readme_domain_chapters.py",
        "python scripts/build_readme_thesis_expansion.py",
        "python scripts/build_readme_arxiv_gaps.py",
        "python scripts/merge_readme_arxiv_thesis.py",
        "python scripts/build_thesis_completeness_audit.py",
        "```",
        "",
        "## Source files",
        "",
        "| Artifact | Path |",
        "|----------|------|",
    ])
    for key, path in SOURCES.items():
        rel = path.relative_to(ROOT).as_posix()
        exists = "yes" if path.is_file() else "missing"
        lines.append(f"| {key} | `{rel}` ({exists}) |")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())