#!/usr/bin/env python3
"""Granular Tier 95 accuracy report — per-record residuals, not pooled median."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

PANELS = [
    "Zebrafish_Cell_Tracking_Panel_benchmark.json",
    "Zebrafish_Developmental_Mechanics_Panel_benchmark.json",
    "Zebrafish_Longevity_Genetics_Coupling_Panel_benchmark.json",
]


def rel_err(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def main() -> int:
    report: dict = {"panels": []}
    for fn in PANELS:
        doc = json.loads((DATA / fn).read_text(encoding="utf-8"))
        recs = list(doc.get("material_records") or [])
        rows = []
        for r in recs:
            comp = float(r["computed"])
            meas = float(r["measured"])
            abs_res = abs(comp - meas)
            rel = rel_err(comp, meas)
            rows.append(
                {
                    "dataset": r.get("name"),
                    "property": r.get("property"),
                    "measured": meas,
                    "computed": comp,
                    "abs_residual": abs_res,
                    "rel_error_pct": round(rel, 8),
                    "reported_error_pct": r.get("error_pct"),
                    "eval_kind": r.get("eval_kind"),
                }
            )
        unique_err = len({round(x["reported_error_pct"], 9) for x in rows if x["reported_error_pct"] is not None})
        panel = {
            "domain": doc["domain"],
            "record_count": len(rows),
            "unique_reported_error_pct_values": unique_err,
            "rel_error_median_pct": round(median([x["rel_error_pct"] for x in rows]), 8) if rows else 0.0,
            "rel_error_max_pct": round(max(x["rel_error_pct"] for x in rows), 8) if rows else 0.0,
            "abs_residual_median": round(median([x["abs_residual"] for x in rows]), 6) if rows else 0.0,
            "abs_residual_max": round(max(x["abs_residual"] for x in rows), 6) if rows else 0.0,
            "worst_5_by_rel_error": sorted(rows, key=lambda x: x["rel_error_pct"], reverse=True)[:5],
            "records": rows,
        }
        report["panels"].append(panel)
        print(f"=== {doc['domain']} ===")
        print(f"records={len(rows)} unique reported error_pct values={unique_err}")
        print(f"rel error median={panel['rel_error_median_pct']}% max={panel['rel_error_max_pct']}%")
        print(f"abs residual median={panel['abs_residual_median']} max={panel['abs_residual_max']}")
        for w in panel["worst_5_by_rel_error"]:
            print(
                f"  {w['dataset']}/{w['property']}: "
                f"meas={w['measured']:.6g} comp={w['computed']:.6g} "
                f"abs={w['abs_residual']:.6g} rel={w['rel_error_pct']:.8f}%"
            )
        print()

    out = DATA / "tier95_granular_accuracy_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())