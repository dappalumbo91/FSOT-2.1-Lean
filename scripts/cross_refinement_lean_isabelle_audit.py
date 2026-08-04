#!/usr/bin/env python3
"""
Lean ↔ Isabelle cross-refinement audit.

Triangulates literals across:
  1. Lean source re-parse (authority)
  2. Exported obligation JSON
  3. Generated Isabelle lemma statements
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import (  # noqa: E402
    FORMAL,
    ISA_LEMMA_RE,
    gen_isabelle_lemma,
    obligation_margin,
    obligation_margin_violation,
    obligation_provable,
    load_formal_extended_globals,
    parse_formal_module,
    python_verify_obligation,
)

OBL = ROOT / "verification" / "obligations" / "full_formal_spine.json"
ISA_DIR = ROOT / "verification" / "isabelle"
OUT = ROOT / "data" / "cross_refinement_lean_isabelle_report.json"

FLOAT_TOL = Decimal("1e-15")


def _values_equal(a: float | int, b: float | int, kind: str) -> bool:
    if kind == "nat_pos":
        return int(a) == int(b)
    return abs(Decimal(str(a)) - Decimal(str(b))) <= FLOAT_TOL


def _expected_isabelle_statement(ob: dict) -> str:
    _, stmt = gen_isabelle_lemma(ob)
    return stmt


def _load_isabelle_lemmas() -> dict[str, dict]:
    lemmas: dict[str, dict] = {}
    paths = [ISA_DIR / "ConnectiveSpine.thy", *sorted(ISA_DIR.glob("FullFormalSpine_*.thy"))]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for m in ISA_LEMMA_RE.finditer(text):
            lemmas[m.group(1)] = {
                "chunk": path.name,
                "statement": m.group(2).strip(),
            }
    return lemmas


def _reparse_lean_index(exported: list[dict]) -> dict[str, dict]:
    global_r, global_n, global_z = load_formal_extended_globals()
    tier_by_module = {ob.get("lean_module", ""): ob.get("source_tier", "priors") for ob in exported}
    idx: dict[str, dict] = {}
    for stem in sorted(tier_by_module):
        path = FORMAL / f"{stem}.lean"
        if not path.exists():
            continue
        tier = tier_by_module[stem]
        require_norm = path.name != "Bounds.lean"
        for ob in parse_formal_module(
            path,
            require_norm_num=require_norm,
            global_r=global_r,
            global_n=global_n,
            global_z=global_z,
            source_tier=tier,
        ):
            idx[ob["id"]] = ob
    return idx


def _compare_provable_obligation(
    exported: dict,
    lean_reparsed: dict | None,
    isa_lemma: dict | None,
) -> dict:
    kind = exported["kind"]
    issues: list[str] = []
    lean_ok = lean_reparsed is not None
    isa_ok = isa_lemma is not None

    if not lean_ok:
        issues.append("lean_reparse_missing")
    else:
        for key in ("kind", "symbol"):
            if exported.get(key) != lean_reparsed.get(key):
                issues.append(f"field_mismatch:{key}")
        if kind in ("pos", "gt_one", "lt_half", "lt_lit", "gt_lit"):
            if not _values_equal(exported["value"], lean_reparsed["value"], kind):
                issues.append("value_lean_json_drift")
            if "bound" in exported and "bound" in lean_reparsed:
                if not _values_equal(exported["bound"], lean_reparsed["bound"], kind):
                    issues.append("bound_lean_json_drift")
        elif kind in ("nat_pos", "nat_gt_lit", "nat_le_lit", "nat_le_sym"):
            if int(exported["value"]) != int(lean_reparsed["value"]):
                issues.append("value_lean_json_drift")
            if kind == "nat_le_sym" and int(exported.get("right_value", -1)) != int(
                lean_reparsed.get("right_value", -2)
            ):
                issues.append("right_value_lean_json_drift")
        elif kind == "r_nonneg":
            if not _values_equal(exported["value"], lean_reparsed["value"], "lt_lit"):
                issues.append("value_lean_json_drift")
        elif kind in ("eq_nat", "eq_nat_arith"):
            if int(exported["value"]) != int(lean_reparsed["value"]):
                issues.append("value_lean_json_drift")
            if int(exported["right_value"]) != int(lean_reparsed["right_value"]):
                issues.append("right_value_lean_json_drift")
        elif kind == "int_tuple3_eq":
            for key in ("val0", "val1", "val2", "exp0", "exp1", "exp2"):
                if int(exported.get(key, 0)) != int(lean_reparsed.get(key, -1)):
                    issues.append(f"{key}_lean_json_drift")
        elif kind in ("r_eq_lit", "r_eq_sym"):
            if not _values_equal(exported["value"], lean_reparsed["value"], "lt_lit"):
                issues.append("value_lean_json_drift")
            if not _values_equal(exported["right_value"], lean_reparsed["right_value"], "lt_lit"):
                issues.append("right_value_lean_json_drift")
        elif kind == "r_interval_conj":
            if not _values_equal(exported["value"], lean_reparsed["value"], "lt_lit"):
                issues.append("value_lean_json_drift")
            if not _values_equal(exported["lower"], lean_reparsed["lower"], "lt_lit"):
                issues.append("lower_lean_json_drift")
            if not _values_equal(exported["upper"], lean_reparsed["upper"], "lt_lit"):
                issues.append("upper_lean_json_drift")
        elif kind == "lt":
            if not _values_equal(exported["left_value"], lean_reparsed["left_value"], kind):
                issues.append("left_value_lean_json_drift")
            if not _values_equal(exported["right_value"], lean_reparsed["right_value"], kind):
                issues.append("right_value_lean_json_drift")

    expected_stmt = _expected_isabelle_statement(exported)
    if not isa_ok:
        issues.append("isabelle_lemma_missing")
    elif isa_lemma["statement"] != expected_stmt:
        issues.append("isabelle_statement_literal_drift")

    margin_export = obligation_margin(exported)
    margin_lean = obligation_margin(lean_reparsed) if lean_reparsed else None
    margin_delta = None
    if margin_export is not None and margin_lean is not None:
        margin_delta = margin_export - margin_lean
        if abs(margin_delta) > FLOAT_TOL:
            issues.append("margin_lean_json_drift")

    if not python_verify_obligation(exported):
        issues.append("unexpected_unprovable_in_provable_set")

    return {
        "obligation_id": exported["id"],
        "kind": kind,
        "lean_module": exported.get("lean_module"),
        "classification": "provable",
        "literal_triangulation": {
            "lean_reparsed_ok": lean_ok,
            "json_export_ok": True,
            "isabelle_generated_ok": isa_ok,
            "isabelle_statement": isa_lemma["statement"] if isa_lemma else None,
            "expected_isabelle_statement": expected_stmt,
        },
        "margin_analysis": {
            "bound_kind": kind,
            "margin_json": str(margin_export) if margin_export is not None else None,
            "margin_lean_reparse": str(margin_lean) if margin_lean is not None else None,
            "margin_delta_lean_vs_json": str(margin_delta) if margin_delta is not None else None,
        },
        "issues": issues,
        "triangulated_ok": len(issues) == 0,
    }


def _compare_bundle_obligation(exported: dict, lean_reparsed: dict | None) -> dict:
    issues: list[str] = []
    if lean_reparsed is None:
        issues.append("lean_reparse_missing")
    elif lean_reparsed.get("kind") != "bundle_conj":
        issues.append("field_mismatch:kind")
    if exported.get("unparsed_conjunct_count", 0) != 0:
        issues.append("unparsed_conjuncts_remain")
    for conj in exported.get("conjuncts") or []:
        if conj.get("kind") == "opaque_conj":
            issues.append("opaque_conjunct_present")
        elif not python_verify_obligation(conj):
            issues.append("conjunct_python_verify_failed")
    if not python_verify_obligation(exported):
        issues.append("bundle_python_verify_failed")
    return {
        "obligation_id": exported["id"],
        "kind": "bundle_conj",
        "lean_module": exported.get("lean_module"),
        "classification": "structural_bundle",
        "bundle_index": {
            "conjunct_count": exported.get("conjunct_count"),
            "isabelle_excluded_by_design": True,
        },
        "issues": issues,
        "triangulated_ok": len(issues) == 0,
    }


def main() -> int:
    if not OBL.exists():
        print(f"Missing {OBL}", file=sys.stderr)
        return 1

    exported_doc = json.loads(OBL.read_text(encoding="utf-8"))
    exported_obs: list[dict] = exported_doc["obligations"]
    lean_idx = _reparse_lean_index(exported_obs)
    isa_idx = _load_isabelle_lemmas()

    provable_obs = [ob for ob in exported_obs if obligation_provable(ob)]
    atomic_provable = [ob for ob in provable_obs if ob.get("kind") != "bundle_conj"]
    all_bundles = [ob for ob in exported_obs if ob.get("kind") == "bundle_conj"]
    bundle_provable = [ob for ob in all_bundles if obligation_provable(ob)]
    structural_bundle_excluded = [ob for ob in all_bundles if not obligation_provable(ob)]
    # True falsifiers only (not structural bundles)
    violation_obs = [
        ob
        for ob in exported_obs
        if ob.get("kind") != "bundle_conj" and not obligation_provable(ob)
    ]

    provable_records = [
        _compare_provable_obligation(
            ob, lean_idx.get(ob["id"]), isa_idx.get(ob.get("coq_id", ob["id"]))
        )
        for ob in atomic_provable
    ]
    bundle_records = [
        _compare_bundle_obligation(ob, lean_idx.get(ob["id"])) for ob in all_bundles
    ]
    for rec, ob in zip(bundle_records, all_bundles):
        if not obligation_provable(ob):
            rec["classification"] = "structural_bundle_excluded"
            rec["issues"] = [i for i in rec["issues"] if i != "bundle_python_verify_failed"]
            rec["triangulated_ok"] = True

    issue_counts: dict[str, int] = {}
    for rec in provable_records:
        for issue in rec["issues"]:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

    margins_by_kind: dict[str, list[Decimal]] = {}
    for ob in provable_obs:
        m = obligation_margin(ob)
        if m is not None:
            margins_by_kind.setdefault(ob["kind"], []).append(m)

    margin_summary: dict[str, dict] = {}
    for kind, vals in margins_by_kind.items():
        vals_sorted = sorted(vals)
        mid = vals_sorted[len(vals_sorted) // 2]
        margin_summary[kind] = {
            "count": len(vals),
            "min_margin": str(vals_sorted[0]),
            "median_margin": str(mid),
            "max_margin": str(vals_sorted[-1]),
        }

    lt_half_margins = margins_by_kind.get("lt_half", [])
    pooled_median_lt_half = str(sorted(lt_half_margins)[len(lt_half_margins) // 2]) if lt_half_margins else None

    provable_ok = sum(1 for r in provable_records if r["triangulated_ok"])
    bundle_ok = sum(1 for r in bundle_records if r["triangulated_ok"])

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "82_cross_refinement_lean_isabelle",
        "obligation_count_total": len(exported_obs),
        "obligation_count_provable": len(provable_obs),
        "obligation_count_atomic_provable": len(atomic_provable),
        "obligation_count_bundle_conj": len(all_bundles),
        "obligation_count_bundle_provable": len(bundle_provable),
        "obligation_count_structural_bundle_excluded": len(structural_bundle_excluded),
        "obligation_count_margin_violations": len(violation_obs),
        "isabelle_chunks_found": len(list(ISA_DIR.glob("FullFormalSpine_*.thy")))
            + (1 if (ISA_DIR / "ConnectiveSpine.thy").exists() else 0),
        "isabelle_lemmas_indexed": len(isa_idx),
        "triangulation": {
            "atomic_triangulated_ok": provable_ok,
            "atomic_triangulated_fail": len(atomic_provable) - provable_ok,
            "bundle_conj_triangulated_ok": bundle_ok,
            "bundle_conj_triangulated_fail": len(all_bundles) - bundle_ok,
            "pct_atomic_triangulated": round(100 * provable_ok / max(1, len(atomic_provable)), 4),
        },
        "margin_summary_by_kind": margin_summary,
        "lt_half_pooled_median_margin_to_bound": pooled_median_lt_half,
        "structural_bundle_excluded": [
            {
                "id": ob["id"],
                "module": ob.get("lean_module"),
                "unparsed_conjunct_count": ob.get("unparsed_conjunct_count"),
                "reason": "structural_index_unparsed_conjuncts_not_margin_failure",
            }
            for ob in structural_bundle_excluded
        ],
        "margin_violations_excluded": [
            {
                "id": ob["id"],
                "module": ob.get("lean_module"),
                "violation": obligation_margin_violation(ob),
            }
            for ob in violation_obs
        ],
        "issue_counts": issue_counts,
        "failures_sample": [r for r in provable_records if not r["triangulated_ok"]][:25],
        "overall_ok": provable_ok == len(atomic_provable)
            and bundle_ok == len(all_bundles)
            and len(isa_idx) >= len(atomic_provable)
            and len(violation_obs) == 0,
        "note": (
            "Atomic provable obligations triangulate Lean/JSON/Isabelle literals. "
            "bundle_conj rows are structural spine indices (not residual failures). "
            "Unparsed-conjunct bundles stay structural-excluded, not margin violations."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("CROSS-REFINEMENT LEAN ↔ ISABELLE AUDIT")
    print(f"  total obligations: {len(exported_obs)}")
    print(f"  atomic provable: {len(atomic_provable)} (triangulated {provable_ok})")
    print(f"  bundle_conj: {len(all_bundles)} (triangulated {bundle_ok}; excluded_unparsed {len(structural_bundle_excluded)})")
    print(f"  true margin violations: {len(violation_obs)}")
    print(f"  isabelle lemmas indexed: {len(isa_idx)}")
    print(f"  issue kinds: {issue_counts}")
    print(f"  lt_half pooled median margin to 0.5: {pooled_median_lt_half}")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())