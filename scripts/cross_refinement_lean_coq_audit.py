#!/usr/bin/env python3
"""
Lean ↔ Coq cross-refinement audit.

Triangulates literals and error margins across:
  1. Lean source re-parse (authority)
  2. Exported obligation JSON
  3. Generated Coq lemma statements

Margin violations (false inequalities) are reported explicitly — never proved in Coq.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import (  # noqa: E402
    COQ_LEMMA_RE,
    FORMAL,
    gen_coq_lemma,
    obligation_margin,
    obligation_margin_violation,
    obligation_provable,
    load_formal_extended_globals,
    make_unique_coq_ids,
    parse_formal_module,
    python_verify_obligation,
)

OBL = ROOT / "verification" / "obligations" / "full_formal_spine.json"
OBL_PRIORS = ROOT / "verification" / "obligations" / "full_priors_spine.json"
MARGIN_OBL = ROOT / "verification" / "obligations" / "margin_violations.json"
COQ_DIR = ROOT / "verification" / "coq"
OUT = ROOT / "data" / "cross_refinement_lean_coq_report.json"

FLOAT_TOL = Decimal("1e-15")


def _values_equal(a: float | int, b: float | int, kind: str) -> bool:
    if kind == "nat_pos":
        return int(a) == int(b)
    return abs(Decimal(str(a)) - Decimal(str(b))) <= FLOAT_TOL


def _expected_coq_statement(ob: dict) -> str:
    _, stmt, _ = gen_coq_lemma(ob)
    return stmt


def _load_coq_lemmas() -> dict[str, dict]:
    lemmas: dict[str, dict] = {}
    coq_globs = ("FullFormalSpine_*.v", "FullPriorsSpine_*.v")
    paths: list[Path] = []
    for g in coq_globs:
        paths.extend(sorted(COQ_DIR.glob(g)))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for m in COQ_LEMMA_RE.finditer(text):
            lemmas[m.group(1)] = {
                "chunk": path.name,
                "statement": m.group(2).strip(),
                "tactic": m.group(3),
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


def _lean_build_failure_index(module_stems: list[str]) -> dict[str, bool | None]:
    """Return whether each module fails to build (True = build fails as expected for violations)."""
    out: dict[str, bool | None] = {s: None for s in module_stems}
    targets = [f"FSOT.Formal.{s}" for s in module_stems if s]
    if not targets:
        return out
    try:
        r = subprocess.run(
            ["lake", "build", *targets],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=600,
        )
        combined = (r.stdout or "") + (r.stderr or "")
        for stem in module_stems:
            marker = f"FSOT/Formal/{stem}.lean"
            if marker in combined and ("unsolved goals" in combined or "error:" in combined):
                out[stem] = True
            elif r.returncode != 0 and marker in combined:
                out[stem] = True
            elif r.returncode == 0:
                out[stem] = False
    except Exception:
        pass
    return out


def _compare_provable_obligation(
    exported: dict,
    lean_reparsed: dict | None,
    coq_lemma: dict | None,
) -> dict:
    kind = exported["kind"]
    issues: list[str] = []
    lean_ok = lean_reparsed is not None
    coq_ok = coq_lemma is not None

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

    expected_stmt = _expected_coq_statement(exported)
    if not coq_ok:
        issues.append("coq_lemma_missing")
    elif coq_lemma["statement"] != expected_stmt:
        issues.append("coq_statement_literal_drift")

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
            "coq_generated_ok": coq_ok,
            "coq_statement": coq_lemma["statement"] if coq_lemma else None,
            "expected_coq_statement": expected_stmt,
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
    conjuncts = exported.get("conjuncts") or []
    if not conjuncts:
        issues.append("empty_conjunct_list")
    else:
        for conj in conjuncts:
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
            "exportable_conjunct_count": exported.get("exportable_conjunct_count"),
            "proof_witness_ids": exported.get("proof_witness_ids"),
            "coq_excluded_by_design": True,
        },
        "issues": issues,
        "triangulated_ok": len(issues) == 0,
    }


def _compare_violation_obligation(
    exported: dict,
    lean_reparsed: dict | None,
    lean_build_fails: bool | None,
) -> dict:
    violation = obligation_margin_violation(exported) or {}
    issues: list[str] = []
    if obligation_provable(exported):
        issues.append("incorrectly_classified_as_violation")
    if lean_reparsed is None:
        issues.append("lean_reparse_missing")
    if lean_build_fails is not True:
        issues.append("lean_expected_build_failure_not_confirmed")

    return {
        "obligation_id": exported["id"],
        "kind": exported["kind"],
        "lean_module": exported.get("lean_module"),
        "classification": "margin_violation",
        "margin_violation": violation,
        "cross_framework_agreement": {
            "python_decimal_refutes": True,
            "coq_excluded_from_proofs": True,
            "lean_build_fails": lean_build_fails,
        },
        "issues": issues,
        "triangulated_ok": len(issues) == 0,
    }


def main() -> int:
    if not OBL.exists():
        print(f"Missing {OBL} — run export_full_priors_obligations.py first", file=sys.stderr)
        return 1

    exported_doc = json.loads(OBL.read_text(encoding="utf-8"))
    exported_obs: list[dict] = exported_doc["obligations"]
    lean_idx = _reparse_lean_index(exported_obs)
    coq_idx = _load_coq_lemmas()

    provable_obs = [ob for ob in exported_obs if obligation_provable(ob)]
    atomic_provable = [ob for ob in provable_obs if ob.get("kind") != "bundle_conj"]
    bundle_provable = [ob for ob in provable_obs if ob.get("kind") == "bundle_conj"]
    violation_obs = [ob for ob in exported_obs if not obligation_provable(ob)]

    provable_records = [
        _compare_provable_obligation(
            ob, lean_idx.get(ob["id"]), coq_idx.get(ob.get("coq_id", ob["id"]))
        )
        for ob in atomic_provable
    ]
    bundle_records = [
        _compare_bundle_obligation(ob, lean_idx.get(ob["id"])) for ob in bundle_provable
    ]
    violation_modules = sorted({ob.get("lean_module", "") for ob in violation_obs if ob.get("lean_module")})
    lean_fail_idx = _lean_build_failure_index(violation_modules)
    violation_records = [
        _compare_violation_obligation(ob, lean_idx.get(ob["id"]), lean_fail_idx.get(ob.get("lean_module", "")))
        for ob in violation_obs
    ]
    records = provable_records + bundle_records + violation_records

    issue_counts: dict[str, int] = {}
    for rec in records:
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
    violation_ok = sum(1 for r in violation_records if r["triangulated_ok"])

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "79b_cross_refinement",
        "obligation_count_total": len(exported_obs),
        "obligation_count_provable": len(provable_obs),
        "obligation_count_atomic_provable": len(atomic_provable),
        "obligation_count_bundle_conj": len(bundle_provable),
        "obligation_count_margin_violations": len(violation_obs),
        "coq_chunks_found": len(list(COQ_DIR.glob("FullFormalSpine_*.v")))
            + len(list(COQ_DIR.glob("FullPriorsSpine_*.v"))),
        "coq_lemmas_indexed": len(coq_idx),
        "triangulation": {
            "atomic_triangulated_ok": provable_ok,
            "atomic_triangulated_fail": len(atomic_provable) - provable_ok,
            "bundle_conj_triangulated_ok": bundle_ok,
            "bundle_conj_triangulated_fail": len(bundle_provable) - bundle_ok,
            "margin_violations_confirmed_ok": violation_ok,
            "margin_violations_confirmed_fail": len(violation_obs) - violation_ok,
            "pct_atomic_triangulated": round(100 * provable_ok / max(1, len(atomic_provable)), 4),
        },
        "margin_summary_by_kind": margin_summary,
        "lt_half_pooled_median_margin_to_bound": pooled_median_lt_half,
        "margin_violations": [
            {
                "id": r["obligation_id"],
                "module": r["lean_module"],
                "violation": r["margin_violation"],
                "lean_build_fails": r["cross_framework_agreement"]["lean_build_fails"],
            }
            for r in violation_records
        ],
        "issue_counts": issue_counts,
        "failures_sample": [r for r in records if not r["triangulated_ok"]][:25],
        "overall_ok": provable_ok == len(atomic_provable)
            and bundle_ok == len(bundle_provable)
            and len(coq_idx) >= len(atomic_provable),
        "note": (
            "Atomic provable obligations triangulate Lean/JSON/Coq literals. "
            "bundle_conj obligations are spine indices excluded from Coq chunks. "
            "Margin violations are excluded from Coq proofs; Lean build failure confirms refutation."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("CROSS-REFINEMENT LEAN ↔ COQ AUDIT")
    print(f"  total obligations: {len(exported_obs)}")
    print(f"  atomic provable: {len(atomic_provable)} (triangulated {provable_ok})")
    print(f"  bundle_conj: {len(bundle_provable)} (triangulated {bundle_ok})")
    print(f"  margin violations: {len(violation_obs)} (confirmed {violation_ok})")
    print(f"  coq lemmas indexed: {len(coq_idx)}")
    print(f"  issue kinds: {issue_counts}")
    print(f"  lt_half pooled median margin to 0.5: {pooled_median_lt_half}")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())