#!/usr/bin/env python3
"""Audit founding 35 laws against FSOT 2.1 strict_empirical + extension panels."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
LAWS_SEED = ROOT / "data" / "founding_35_laws_seed.yaml"
STRICT = ROOT / "vendor" / "formula_corpus" / "by_domain" / "strict_empirical.jsonl"
EXT_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
OUT_JSON = ROOT / "data" / "founding_law_audit.json"
OUT_MD = ROOT / "docs" / "FOUNDING_35_LAWS_AUDIT.md"


def _load_strict() -> list[dict]:
    rows = []
    if not STRICT.exists():
        return rows
    for line in STRICT.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _load_extension_domains() -> list[dict]:
    if yaml is None or not EXT_MANIFEST.exists():
        return []
    data = yaml.safe_load(EXT_MANIFEST.read_text(encoding="utf-8"))
    domains = data.get("extension_domains") or data.get("domains") or data
    if isinstance(domains, dict):
        out = []
        for name, spec in domains.items():
            if isinstance(spec, dict):
                out.append({"name": name, **spec})
        return out
    return domains if isinstance(domains, list) else []


def _search_strict(keywords: list[str], rows: list[dict], limit: int = 8) -> list[dict]:
    hits = []
    for row in rows:
        blob = " ".join([
            str(row.get("concept_name", "")),
            str(row.get("formula_canonical", "")),
            str(row.get("project", "")),
            str(row.get("fsot_physics_explanation", "")),
        ]).lower()
        score = sum(1 for kw in keywords if kw.replace("_", " ") in blob or kw in blob)
        if score > 0:
            outcome = row.get("outcome") or {}
            hits.append({
                "concept_name": row.get("concept_name"),
                "formula": row.get("formula_canonical"),
                "error_pct": outcome.get("error_pct"),
                "matched": outcome.get("matched"),
                "score": score,
            })
    hits.sort(key=lambda h: (-h["score"], float(h.get("error_pct") or 999)))
    return hits[:limit]


def _search_panels(
    keywords: list[str],
    domains: list[dict],
    *,
    law_id: str | None = None,
    limit: int = 5,
) -> list[dict]:
    hits = []
    for dom in domains:
        founding_ids = dom.get("founding_law_ids") or []
        if law_id and law_id in founding_ids:
            hits.append({
                "panel": dom.get("name"),
                "lean_module": dom.get("lean_module"),
                "benchmark_data": dom.get("benchmark_data"),
                "score": 100,
                "match": "founding_law_id",
            })
            continue
        name = str(dom.get("name", "")).lower()
        note = str(dom.get("note", "")).lower()
        bench = str(dom.get("benchmark_data", "")).lower()
        blob = f"{name} {note} {bench}"
        score = sum(1 for kw in keywords if kw.replace("_", " ") in blob or kw in blob)
        if score > 0:
            hits.append({
                "panel": dom.get("name"),
                "lean_module": dom.get("lean_module"),
                "benchmark_data": dom.get("benchmark_data"),
                "score": score,
                "match": "keyword",
            })
    hits.sort(key=lambda h: (-h["score"], str(h.get("panel") or "")))
    return hits[:limit]


def _classify(law: dict, strict_hits: list[dict], panel_hits: list[dict]) -> str:
    matched_strict = [h for h in strict_hits if str(h.get("matched")).lower() == "true"]
    if matched_strict:
        return "verified_strict_empirical"
    if panel_hits:
        return "verified_extension_panel"
    if law.get("domain_hint") in ("consciousness", "cross_domain"):
        return "philosophy_scaffold"
    if strict_hits:
        return "partial_formula_match_unverified"
    return "founding_unmapped"


def audit_laws(
    seed_path: Path = LAWS_SEED,
    out_json: Path = OUT_JSON,
    out_md: Path = OUT_MD,
) -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required")

    seed = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
    strict_rows = _load_strict()
    ext_domains = _load_extension_domains()

    results = []
    counts: dict[str, int] = {}

    for law in seed.get("laws") or []:
        keywords = law.get("keywords") or []
        strict_hits = _search_strict(keywords, strict_rows)
        panel_hits = _search_panels(keywords, ext_domains, law_id=law.get("id"))
        status = _classify(law, strict_hits, panel_hits)
        counts[status] = counts.get(status, 0) + 1

        results.append({
            **law,
            "audit_status": status,
            "founding_accuracy_trusted": False,
            "strict_empirical_hits": strict_hits,
            "extension_panel_hits": panel_hits,
            "recommendation": _recommendation(status),
        })

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "law_count": len(results),
        "strict_empirical_corpus_size": len(strict_rows),
        "extension_domain_count": len(ext_domains),
        "status_counts": counts,
        "policy": (
            "Founding-era accuracy percentages are never trusted without individual "
            "FSOT 2.1 strict_empirical or extension panel verification."
        ),
        "laws": results,
    }

    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    out_md.write_text(_render_md(report), encoding="utf-8")
    print(f"Audit: {out_json}")
    print(f"Summary: {out_md}")
    print(f"Status counts: {counts}")
    return report


def _recommendation(status: str) -> str:
    return {
        "verified_strict_empirical": "Safe to cite as measured FSOT 2.1 result.",
        "verified_extension_panel": "Cite extension benchmark; run panel build if stale.",
        "philosophy_scaffold": "Retain as interpretive; link to consciousness panels.",
        "partial_formula_match_unverified": "Re-derive formula and add to strict_empirical.",
        "founding_unmapped": "Founding law only — needs new benchmark or retire from claims.",
    }.get(status, "Review manually.")


def _render_md(report: dict) -> str:
    lines = [
        "# Founding 35 Laws — FSOT 2.1 Audit",
        "",
        f"*Generated: {report['generated_at']}*",
        "",
        report["policy"],
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Laws audited | {report['law_count']} |",
        f"| Strict empirical corpus | {report['strict_empirical_corpus_size']} |",
        f"| Extension domains | {report['extension_domain_count']} |",
        "",
        "### Status counts",
        "",
    ]
    for status, n in sorted(report["status_counts"].items()):
        lines.append(f"- **{status}**: {n}")
    lines.extend(["", "## Law-by-law", ""])
    for law in report["laws"]:
        lines.append(f"### {law['id']}: {law['name']}")
        lines.append(f"- **Audit status:** `{law['audit_status']}`")
        lines.append(f"- **Founding accuracy trusted:** {law['founding_accuracy_trusted']}")
        lines.append(f"- **Recommendation:** {law['recommendation']}")
        if law["strict_empirical_hits"]:
            lines.append("- **Strict empirical matches:**")
            for h in law["strict_empirical_hits"][:3]:
                lines.append(
                    f"  - `{h['concept_name']}` error={h.get('error_pct')}% matched={h.get('matched')}"
                )
        if law["extension_panel_hits"]:
            lines.append("- **Extension panels:**")
            for h in law["extension_panel_hits"][:3]:
                lines.append(f"  - `{h['panel']}` → {h.get('lean_module')}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=Path, default=LAWS_SEED)
    ap.add_argument("--out-json", type=Path, default=OUT_JSON)
    ap.add_argument("--out-md", type=Path, default=OUT_MD)
    args = ap.parse_args()
    audit_laws(args.seed, args.out_json, args.out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())