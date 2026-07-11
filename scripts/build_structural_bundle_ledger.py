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


def _conjunct_key(c: dict) -> str:
    return f"{c.get('kind')}:{c.get('symbol', c.get('id', ''))}:{c.get('statement', '')}"


def _atomic_index(obligations: list[dict]) -> dict[str, list[str]]:
    idx: dict[str, list[str]] = {}
    for ob in obligations:
        if ob.get("kind") == "bundle_conj":
            continue
        keys = [
            f"{ob.get('kind')}:{ob.get('symbol', '')}:{ob.get('statement', '')}",
            f"{ob.get('kind')}:{ob.get('id', '')}",
        ]
        if ob.get("symbol"):
            keys.append(f"{ob.get('kind')}:{ob['symbol']}")
        for k in keys:
            if k.endswith(":") or k.endswith("::"):
                continue
            idx.setdefault(k, []).append(ob["id"])
    return idx


def build() -> dict:
    doc = json.loads(SPINE.read_text(encoding="utf-8"))
    obligations = doc.get("obligations") or []
    atomic_idx = _atomic_index(obligations)
    bundles = [ob for ob in obligations if ob.get("kind") == "bundle_conj"]
    rows: list[dict] = []
    total_conj = 0
    covered_conj = 0

    for ob in bundles:
        conjuncts = ob.get("conjuncts") or []
        conj_rows: list[dict] = []
        for c in conjuncts:
            if c.get("kind") == "opaque_conj" or c.get("opaque"):
                conj_rows.append(
                    {
                        "kind": "opaque_conj",
                        "atomic_coverage": False,
                        "note": "opaque structural witness",
                    }
                )
                total_conj += 1
                continue
            key = _conjunct_key(c)
            sym_key = f"{c.get('kind')}:{c.get('symbol', '')}" if c.get("symbol") else ""
            matches: list[str] = []
            for k in (key, sym_key, f"lt_half:{c.get('symbol', '')}" if c.get("kind") == "lt_half" else ""):
                if not k or k.endswith(":"):
                    continue
                for mid in atomic_idx.get(k, []):
                    if mid not in matches:
                        matches.append(mid)
            covered = bool(matches)
            if covered:
                covered_conj += 1
            total_conj += 1
            conj_rows.append(
                {
                    "kind": c.get("kind"),
                    "symbol": c.get("symbol"),
                    "statement": c.get("statement"),
                    "atomic_coverage": covered,
                    "matching_atomic_ids": matches[:5],
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
        "version": "1.0",
        "summary": {
            "bundle_conj_total": len(bundles),
            "structural_bundle_excluded": len(excluded),
            "provable_bundle_conj": len(provable_bundles),
            "total_conjuncts": total_conj,
            "conjuncts_with_atomic_coverage": covered_conj,
            "conjunct_atomic_coverage_pct": round(100.0 * covered_conj / total_conj, 2) if total_conj else 100.0,
            "design_note": (
                "bundle_conj rows are structural spine indices linking domain witness bundles. "
                "Atomic conjuncts are replayed separately on the cross-proof spine; bundles are "
                "excluded from Coq/Isabelle/Rust chunks by design — not margin failures."
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
        f"conjunct coverage={s['conjunct_atomic_coverage_pct']}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())