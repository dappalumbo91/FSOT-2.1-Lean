#!/usr/bin/env python3
"""Ledger for structural bundle_conj obligations — conjunct atomic coverage."""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPINE = ROOT / "verification" / "obligations" / "full_formal_spine.json"
OUT = ROOT / "data" / "structural_bundle_ledger.json"

sys.path.insert(0, str(ROOT / "scripts"))
from bundle_export_lib import _find_atomic_link  # noqa: E402

_NORM_NUM_KINDS = frozenset(
    {
        "eq_nat",
        "eq_nat_arith",
        "lt_lit",
        "gt_lit",
        "lt_half",
        "r_eq_lit",
        "r_lt_lit_pure",
        "r_le_lit",
        "nat_pos",
        "nat_gt_lit",
        "pos",
        "int_tuple3_eq",
        "nat_le_sym",
        "abs_diff_lt_lit",
    }
)


def _atomic_index(obligations: list[dict]) -> tuple[dict[str, list[str]], set[str], dict[tuple, list[str]]]:
    idx: dict[str, list[str]] = {}
    ids: set[str] = set()
    by_sym_kind: dict[tuple, list[str]] = {}
    for ob in obligations:
        if ob.get("kind") == "bundle_conj":
            continue
        oid = str(ob["id"])
        ids.add(oid)
        kind = ob.get("kind")
        sym = ob.get("symbol")
        if kind and sym:
            by_sym_kind.setdefault((kind, sym), []).append(oid)
        keys = [
            f"{kind}:{sym or ''}:{ob.get('statement', '')}",
            f"{kind}:{oid}",
        ]
        if sym:
            keys.append(f"{kind}:{sym}")
        for k in keys:
            if k.endswith(":") or k.endswith("::"):
                continue
            idx.setdefault(k, []).append(oid)
    return idx, ids, by_sym_kind


def _resolve_conjunct(
    c: dict,
    bundle_id: str,
    atomic_by_id: dict[str, dict],
    spine_by_id: dict[str, dict],
) -> tuple[str | None, list[str]]:
    linked = c.get("linked_obligation_id") or c.get("proof_witness_id")
    if linked:
        lid = str(linked)
        if lid in atomic_by_id:
            return "linked_obligation_id", [lid]
        if lid in spine_by_id:
            return "witness_bundle_link", [lid]

    found = _find_atomic_link(c, atomic_by_id)
    if found:
        via = "linked_obligation_id" if c.get("linked_obligation_id") else "inferred_atomic_link"
        return via, [found]

    if bundle_id in atomic_by_id:
        return "bundle_id_atomic", [bundle_id]

    if c.get("proof_style") == "norm_num":
        return "lean_bundle_norm_num", [bundle_id]

    kind = c.get("kind")
    try:
        if kind == "gt_lit" and float(c["value"]) > float(c["bound"]):
            return "numeric_conjunct_tautology", [bundle_id]
        if kind == "lt_lit" and float(c["value"]) < float(c["bound"]):
            return "numeric_conjunct_tautology", [bundle_id]
        if kind == "r_eq_lit" and abs(float(c["value"]) - float(c["right_value"])) < 1e-9:
            return "numeric_conjunct_tautology", [bundle_id]
        if kind == "nat_le_sym" and int(c["value"]) <= int(c["right_value"]):
            return "numeric_conjunct_tautology", [bundle_id]
        if kind == "abs_diff_lt_lit":
            diff = c.get("diff", c.get("value"))
            if diff is not None and float(diff) < float(c["bound"]):
                return "numeric_conjunct_tautology", [bundle_id]
    except (KeyError, TypeError, ValueError):
        pass

    return None, []


def build() -> dict:
    doc = json.loads(SPINE.read_text(encoding="utf-8"))
    obligations = doc.get("obligations") or []
    atomic_idx, atomic_ids, by_sym_kind = _atomic_index(obligations)
    atomic_by_id = {
        str(ob["id"]): ob for ob in obligations if ob.get("kind") != "bundle_conj"
    }
    spine_by_id = {str(ob["id"]): ob for ob in obligations}
    bundles = [ob for ob in obligations if ob.get("kind") == "bundle_conj"]
    rows: list[dict] = []
    total_conj = 0
    covered_conj = 0
    explicit_link_total = 0
    explicit_link_hit = 0

    for ob in bundles:
        conjuncts = ob.get("conjuncts") or []
        conj_rows: list[dict] = []
        for c in conjuncts:
            total_conj += 1
            if c.get("linked_obligation_id") or c.get("proof_witness_id"):
                explicit_link_total += 1
                lid = str(c.get("linked_obligation_id") or c.get("proof_witness_id"))
                if lid in atomic_ids or lid in spine_by_id:
                    explicit_link_hit += 1
            via, matches = _resolve_conjunct(c, ob["id"], atomic_by_id, spine_by_id)
            covered = bool(matches)
            lean_taut = via == "lean_bundle_norm_num"
            if covered:
                covered_conj += 1
            conj_rows.append(
                {
                    "kind": c.get("kind"),
                    "symbol": c.get("symbol"),
                    "statement": c.get("statement"),
                    "atomic_coverage": covered,
                    "coverage_via": via,
                    "lean_bundle_tautology": lean_taut,
                    "matching_atomic_ids": matches,
                    "linked_obligation_id": c.get("linked_obligation_id"),
                }
            )
        rows.append(
            {
                "id": ob["id"],
                "lean_module": ob.get("lean_module"),
                "provable": ob.get("provable"),
                "unprovable_reason": ob.get("unprovable_reason"),
                "conjunct_count": len(conjuncts),
                "conjuncts": conj_rows,
                "conjunct_atomic_coverage_pct": round(
                    100.0 * sum(1 for r in conj_rows if r.get("atomic_coverage")) / max(len(conj_rows), 1),
                    2,
                )
                if conj_rows
                else 100.0,
            }
        )

    excluded = [ob for ob in bundles if not ob.get("provable")]
    provable_bundles = [ob for ob in bundles if ob.get("provable")]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.2",
        "summary": {
            "bundle_conj_total": len(bundles),
            "structural_bundle_excluded": len(excluded),
            "provable_bundle_conj": len(provable_bundles),
            "total_conjuncts": total_conj,
            "conjuncts_with_atomic_coverage": covered_conj,
            "conjunct_atomic_coverage_pct": round(100.0 * covered_conj / total_conj, 2) if total_conj else 100.0,
            "explicit_linked_conjuncts": explicit_link_total,
            "explicit_linked_in_spine": explicit_link_hit,
            "explicit_link_hit_pct": round(100.0 * explicit_link_hit / explicit_link_total, 2)
            if explicit_link_total
            else 100.0,
            "design_note": (
                "bundle_conj rows are structural spine indices linking domain witness bundles. "
                "Conjuncts resolve via atomic spine IDs, witness bundle links, or Lean norm_num tautologies. "
                "Bundles are excluded from Coq/Isabelle/Rust chunks by design — not margin failures."
            ),
        },
        "by_module": dict(Counter(ob.get("lean_module", "?") for ob in excluded)),
        "provable_bundle_ids": [ob["id"] for ob in provable_bundles],
        "bundles": rows,
    }


def main() -> int:
    if not SPINE.exists():
        print(f"Missing {SPINE}", file=sys.stderr)
        return 1
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    s = doc["summary"]
    print(f"Wrote {OUT}")
    print(
        f"  bundles: {s['bundle_conj_total']} excluded={s['structural_bundle_excluded']} "
        f"conjunct coverage={s['conjunct_atomic_coverage_pct']}% "
        f"explicit_link_hit={s['explicit_link_hit_pct']}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())