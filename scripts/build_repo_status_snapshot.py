#!/usr/bin/env python3
"""Build live repo status snapshot + docs/CURRENT_STATUS.md for expansion sync.

Run after densify / new panels / multiprover so README and docs can point at
authoritative numbers instead of drifting hand-edits.

  python scripts/build_repo_status_snapshot.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from c_thin_depth_lib import _tier  # noqa: E402

OUT_JSON = ROOT / "data" / "repo_status_snapshot.json"
OUT_MD = ROOT / "docs" / "CURRENT_STATUS.md"


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def build() -> dict:
    margin = _load(ROOT / "data" / "benchmark_margin_audit.json")
    xproof = _load(ROOT / "data" / "cross_proof_verification_report.json")
    empirical = _load(ROOT / "data" / "empirical_accuracy_closure.json")
    densify = _load(ROOT / "data" / "false_densify_remediation_report.json")
    coq_ref = _load(ROOT / "data" / "cross_refinement_lean_coq_report.json")
    formula = _load(ROOT / "data" / "formula_authority_closure.json")
    mathlib = _load(ROOT / "data" / "mathlib_rederivation_campaign_report.json")
    params = _load(ROOT / "data" / "parameter_count_audit.json")
    toe = _load(ROOT / "data" / "toe_gap_closure_report.json")
    toe_ev = toe.get("evaluation") or {}

    compute = ROOT / "vendor" / "fsot_compute.py"
    sha = hashlib.sha256(compute.read_bytes()).hexdigest().upper() if compute.is_file() else ""
    pin_ok = sha.startswith("D1D38A")

    tiers: Counter[str] = Counter()
    for p in (ROOT / "data").glob("*benchmark*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        rec = int(d.get("record_count") or 0)
        med = d.get("pooled_median_error_pct")
        if med is None:
            med = d.get("median_error_pct")
        if med is None or rec == 0:
            continue
        tiers[_tier(float(med), rec)] += 1

    green = int(margin.get("green_gate_pass_count") or 0)
    fail = int(margin.get("green_gate_fail_count") or 0)
    active = int(margin.get("benchmark_file_count") or green + fail)

    formal = xproof.get("full_formal_spine") or {}
    catalog = xproof.get("scientific_catalog_spine") or {}
    frameworks = xproof.get("frameworks") or {}
    depth = mathlib.get("depth_gates") or {}
    corpus = mathlib.get("corpus") or {}

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "edition_stamp": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "authority": {
            "pin_prefix": "D1D38A",
            "fsot_compute_sha256": sha,
            "pin_match": pin_ok,
            "path": "vendor/fsot_compute.py",
            "formula_authority_verdict": formula.get("verdict"),
            "formula_authority_all_ok": bool(formula.get("all_ok")),
            "parameter_verdict": params.get("verdict") or params.get("audit_verdict"),
        },
        "empirical": {
            "green_gate_pass_count": green,
            "green_gate_fail_count": fail,
            "benchmark_file_count": active,
            "green_gate_pct": 0.5,
            "tier_distribution": dict(tiers),
            "median_of_medians_pct": (empirical.get("benchmark_envelope") or {}).get(
                "pooled_median_of_domains_pct"
            )
            or empirical.get("median_of_medians_pct"),
            "total_scalar_records": (empirical.get("benchmark_envelope") or {}).get(
                "total_scalar_records"
            ),
        },
        "mathlib": {
            "verdict": mathlib.get("verdict"),
            "engine_core_closed": bool(mathlib.get("engine_core_closed")),
            "full_corpus_closed": bool(mathlib.get("full_corpus_closed")),
            "theorem_count": corpus.get("theorem_count"),
            "mathlib_depth_count": corpus.get("mathlib_depth_count"),
            "mathlib_depth_pct": corpus.get("mathlib_depth_pct")
            or depth.get("corpus_mathlib_pct"),
            "engine_mathlib_pct": depth.get("engine_mathlib_pct"),
            "corpus_l1_count": depth.get("corpus_l1_count"),
            "engine_l1_count": depth.get("engine_l1_count"),
        },
        "multiprover": {
            "overall_ok": bool(xproof.get("overall_ok")),
            "github_ready": bool(xproof.get("github_ready")),
            "seven_way_bare_metal": bool(xproof.get("seven_way_bare_metal")),
            "eight_way_hardware": bool(xproof.get("eight_way_hardware")),
            "atomic_provable": formal.get("atomic_provable_count")
            or coq_ref.get("obligation_count_atomic_provable"),
            "full_formal_obligations": formal.get("obligation_count"),
            "catalog_obligations": catalog.get("obligation_count")
            or (catalog.get("python_decimal") or {}).get("total"),
            "catalog_domains": catalog.get("domain_count"),
            "true_margin_violations": formal.get("margin_violation_count")
            if formal.get("margin_violation_count") is not None
            else coq_ref.get("obligation_count_margin_violations"),
            "structural_bundle_excluded": formal.get("structural_bundle_excluded_count")
            if formal.get("structural_bundle_excluded_count") is not None
            else coq_ref.get("obligation_count_structural_bundle_excluded"),
            "frameworks_passed": sorted(
                k
                for k, v in frameworks.items()
                if isinstance(v, dict) and v.get("status") == "passed"
            ),
        },
        "toe_labels": {
            "label_A_empirical_framework": bool(toe_ev.get("label_A_empirical_framework")),
            "label_B_classical_toe": bool(toe_ev.get("label_B_classical_toe")),
            "report": "data/toe_gap_closure_report.json",
        },
        "expansion_highlights": {
            "dzhanibekov_panel": "data/dzhanibekov_intermediate_axis_fsot_panel_benchmark.json",
            "dzhanibekov_doc": "docs/DZHANIBEKOV_FSOT_RESPONSE.md",
            "proper_densify_policy": "docs/FSOT_PROPER_DENSIFY_POLICY.md",
            "multiprover_debt_clarified": "docs/MULTIPROVER_DESIGN_DEBT_CLARIFIED.md",
            "hardware_depth": "docs/HARDWARE_DEPTH_CACHE_INTERCONNECT.md",
            "breakthroughs": "docs/RECENT_BREAKTHROUGH_EXPANSION.md",
            "empirical_claim_evidence": "docs/EMPIRICAL_CLAIM_EVIDENCE.md",
            "mathlib_campaign": "docs/MATHLIB_REDERIVATION_CAMPAIGN.md",
            "false_densify_remediated": bool(densify),
            "reality_os_sibling": "https://github.com/dappalumbo91/FSOT-Reality-OS",
        },
        "sync_rule": (
            "After any densify / new panel / multiprover / Mathlib run: "
            "python scripts/build_repo_status_snapshot.py && "
            "python scripts/build_skeptic_replication_kit.py then update README headlines "
            "if green count or multiprover flags change. See docs/REPO_SYNC_AND_EXPANSION_CHECKLIST.md"
        ),
    }
    return doc


def write_md(doc: dict) -> str:
    emp = doc["empirical"]
    mp = doc["multiprover"]
    auth = doc["authority"]
    ml = doc.get("mathlib") or {}
    toe = doc.get("toe_labels") or {}
    hi = doc["expansion_highlights"]
    lines = [
        "# FSOT repo — current status (generated)",
        "",
        f"**Generated:** `{doc['generated_at']}`  ",
        f"**Edition stamp:** {doc['edition_stamp']}  ",
        f"**Regenerate:** `python scripts/build_repo_status_snapshot.py`",
        "",
        "> Authoritative live numbers for expansion. Prefer this file over hand-edited counts in README when they disagree.",
        "",
        "## Authority",
        "",
        "| Item | Value |",
        "|------|-------|",
        f"| Pin | **{auth['pin_prefix']}** |",
        f"| Match | **{auth['pin_match']}** |",
        f"| SHA-256 | `{auth['fsot_compute_sha256'][:16]}…` |",
        f"| Path | `{auth['path']}` |",
        f"| Formula authority | **{auth.get('formula_authority_verdict')}** (all_ok={auth.get('formula_authority_all_ok')}) |",
        f"| Parameters | **{auth.get('parameter_verdict')}** |",
        "",
        "## Empirical green gate",
        "",
        "| Item | Value |",
        "|------|-------|",
        f"| Green pass | **{emp['green_gate_pass_count']} / {emp['benchmark_file_count']}** |",
        f"| Fail | **{emp['green_gate_fail_count']}** |",
        f"| Gate | ≤ {emp['green_gate_pct']}% pooled median |",
        f"| Median-of-medians | {emp.get('median_of_medians_pct')}% |",
        f"| Scalar records (envelope) | {emp.get('total_scalar_records')} |",
        f"| Tiers | `{emp.get('tier_distribution')}` |",
        "",
        "## Mathlib re-derivation (Formal corpus)",
        "",
        "| Item | Value |",
        "|------|-------|",
        f"| Verdict | **{ml.get('verdict')}** |",
        f"| Theorems | **{ml.get('mathlib_depth_count')} / {ml.get('theorem_count')}** ({ml.get('mathlib_depth_pct')}%) |",
        f"| Engine Mathlib % | {ml.get('engine_mathlib_pct')} (L1={ml.get('engine_l1_count')}) |",
        f"| Corpus L1 left | {ml.get('corpus_l1_count')} |",
        f"| Engine core closed | {ml.get('engine_core_closed')} |",
        f"| Full corpus closed | {ml.get('full_corpus_closed')} |",
        "",
        "## Multiprover",
        "",
        "| Item | Value |",
        "|------|-------|",
        f"| overall_ok | **{mp['overall_ok']}** |",
        f"| github_ready | **{mp['github_ready']}** |",
        f"| seven_way_bare_metal | {mp['seven_way_bare_metal']} |",
        f"| eight_way_hardware | {mp['eight_way_hardware']} |",
        f"| Atomic provable | {mp.get('atomic_provable')} |",
        f"| Full formal obligations | {mp.get('full_formal_obligations')} |",
        f"| Catalog obligations | {mp.get('catalog_obligations')} (domains {mp.get('catalog_domains')}) |",
        f"| True margin violations | **{mp.get('true_margin_violations')}** |",
        f"| Structural bundle excluded | {mp.get('structural_bundle_excluded')} |",
        "",
        "Frameworks passed: " + ", ".join(f"`{x}`" for x in (mp.get("frameworks_passed") or [])),
        "",
        "## ToE labels (frozen checklist)",
        "",
        "| Item | Value |",
        "|------|-------|",
        f"| Label A (empirical framework) | **{toe.get('label_A_empirical_framework')}** |",
        f"| Label B (classical T1–T6) | **{toe.get('label_B_classical_toe')}** |",
        f"| Report | `{toe.get('report')}` |",
        "",
        "## Claim evidence (kill commands)",
        "",
        f"- Machine map for skeptics / dismissals: [`EMPIRICAL_CLAIM_EVIDENCE.md`](EMPIRICAL_CLAIM_EVIDENCE.md)",
        f"- Mathlib campaign: [`MATHLIB_REDERIVATION_CAMPAIGN.md`](MATHLIB_REDERIVATION_CAMPAIGN.md)",
        f"- Skeptic kit: [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md)",
        "",
        "## Expansion highlights (recent)",
        "",
        f"- Dzhanibekov / intermediate-axis vacuum flip: [`{hi['dzhanibekov_doc']}`](DZHANIBEKOV_FSOT_RESPONSE.md)",
        f"- Proper densify (formula + real data only): [`{hi['proper_densify_policy']}`](FSOT_PROPER_DENSIFY_POLICY.md)",
        f"- Multiprover debt clarified: [`{hi['multiprover_debt_clarified']}`](MULTIPROVER_DESIGN_DEBT_CLARIFIED.md)",
        f"- Hardware depth: [`{hi['hardware_depth']}`](HARDWARE_DEPTH_CACHE_INTERCONNECT.md)",
        f"- Breakthroughs / QCE: [`{hi['breakthroughs']}`](RECENT_BREAKTHROUGH_EXPANSION.md)",
        f"- Reality OS sibling (FSOT-native kernel lab): {hi.get('reality_os_sibling')}",
        "",
        "## Sync rule",
        "",
        doc["sync_rule"],
        "",
        "Checklist: [`REPO_SYNC_AND_EXPANSION_CHECKLIST.md`](REPO_SYNC_AND_EXPANSION_CHECKLIST.md)",
        "",
        "Machine JSON: [`data/repo_status_snapshot.json`](../data/repo_status_snapshot.json)",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    OUT_MD.write_text(write_md(doc), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"  green={doc['empirical']['green_gate_pass_count']}/{doc['empirical']['benchmark_file_count']} "
        f"overall_ok={doc['multiprover']['overall_ok']} pin={doc['authority']['pin_match']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
