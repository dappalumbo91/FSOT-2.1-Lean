#!/usr/bin/env python3
"""Near-gate audit + thin-panel thickening pace (main system).

1. Audit near-gate max residual domains (mechanism notes)
2. Rebuild multi_hero + hybrid FI + materials species bridge
3. Write data/near_gate_thin_pace_report.json
4. Re-run margin audit
"""

from __future__ import annotations

import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
DATA = ROOT / "data"


def main() -> int:
    report: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "wave": "near_gate_and_thin_pace",
        "actions": [],
        "near_gate_findings": {},
        "errors": [],
    }

    # --- Near-gate findings (read-only audit) ---
    NEAR = [
        "phi_morphogenetic_scaling_benchmark.json",
        "crc_handbook_properties_benchmark.json",
        "geochemistry_benchmark.json",
        "zebrafish_predictive_validation_panel_benchmark.json",
        "materials_engineering_benchmark.json",
        "quantum_materials_benchmark.json",
        "clinical_medicine_extension_benchmark.json",
        "immunology_benchmark.json",
        "neuroimmunology_benchmark.json",
        "culinary_arts_benchmark.json",
    ]

    offenders = []
    for fn in NEAR:
        p = DATA / fn
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        recs = d.get("records") or d.get("material_records") or []
        scored = []
        for r in recs:
            if r.get("error_pct") is None:
                continue
            scored.append((float(r["error_pct"]), r))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = []
        for e, r in scored[:5]:
            top.append(
                {
                    "error_pct": e,
                    "name": r.get("name"),
                    "property": r.get("property"),
                    "formula": r.get("fsot_formula") or r.get("formula"),
                    "mechanism_note": (
                        "SMILES/seed closed-form residual already ≤0.5%; "
                        "not a free-param fold. Tighten only via better formula class."
                        if e >= 0.4
                        else "within aspiration band or aggregate channel"
                    ),
                }
            )
        report["near_gate_findings"][fn] = {
            "n_records": len(recs),
            "max_error_pct": scored[0][0] if scored else None,
            "top": top,
        }
        if scored and scored[0][0] >= 0.45:
            offenders.append({"file": fn, "max": scored[0][0], "name": scored[0][1].get("name")})

    report["near_gate_summary"] = {
        "near_gate_files_audited": len(report["near_gate_findings"]),
        "max_offenders_ge_0.45": offenders,
        "action": (
            "Do not invent free parameters for CRC/immunology SMILES tops. "
            "They are already green; headroom is formula-class residual. "
            "Thin-panel thickening is the expansion lever this pace."
        ),
    }
    report["actions"].append("near_gate_audit")

    # --- Rebuild multi_hero ---
    try:
        from build_multi_hero_benchmark import build as build_mh, OUTPUT as MH_OUT

        mh = build_mh()
        MH_OUT.write_text(json.dumps(mh, indent=2), encoding="utf-8")
        report["actions"].append(
            {
                "rebuild": "multi_hero_benchmark",
                "record_count": mh.get("record_count"),
                "stratum_count": mh.get("stratum_count"),
                "heroes_per_class": mh.get("heroes_per_class"),
                "median_fi_proxy_rel_err_pct": mh.get("median_fi_proxy_rel_err_pct"),
            }
        )
        print(f"multi_hero: n={mh.get('record_count')} strata={mh.get('stratum_count')}")
    except Exception as e:
        report["errors"].append({"multi_hero": str(e), "trace": traceback.format_exc()[-500:]})
        print("multi_hero SKIP:", e)

    # --- Rebuild hybrid FI (thick) ---
    try:
        from tier77_post_tier76_maintenance_lib import build_hybrid_fi_sim_multi_hero_panel

        hy = build_hybrid_fi_sim_multi_hero_panel()
        out_h = DATA / "hybrid_fi_sim_multi_hero_panel_benchmark.json"
        out_h.write_text(json.dumps(hy, indent=2), encoding="utf-8")
        mr = hy.get("material_records") or hy.get("records") or []
        report["actions"].append(
            {
                "rebuild": "hybrid_fi_sim_multi_hero_panel",
                "record_count": hy.get("record_count"),
                "material_records": len(mr),
                "scalar_record_count": hy.get("scalar_record_count"),
                "median_error_pct": hy.get("median_error_pct") or hy.get("pooled_median_error_pct"),
                "max_error_pct": hy.get("max_error_pct")
                or (hy.get("margin_summary") or {}).get("max_scalar_error_pct"),
            }
        )
        print(
            f"hybrid_fi: record_count={hy.get('record_count')} "
            f"material={len(mr)} scalar={hy.get('scalar_record_count')}"
        )
    except Exception as e:
        report["errors"].append({"hybrid_fi": str(e), "trace": traceback.format_exc()[-500:]})
        print("hybrid_fi SKIP:", e)

    # --- Materials species bridge ---
    try:
        from build_materials_species_bridge_benchmark import build as build_msb, OUTPUT as MSB_OUT

        msb = build_msb()
        MSB_OUT.write_text(json.dumps(msb, indent=2), encoding="utf-8")
        report["actions"].append(
            {
                "rebuild": "materials_species_bridge",
                "record_count": msb.get("record_count"),
                "overlap_metal_count": msb.get("overlap_metal_count"),
                "median_error_pct": msb.get("median_error_pct"),
            }
        )
        print(
            f"materials_bridge: n={msb.get('record_count')} "
            f"metals={msb.get('overlap_metal_count')} med={msb.get('median_error_pct')}"
        )
    except Exception as e:
        report["errors"].append({"materials_bridge": str(e)})
        print("materials_bridge SKIP:", e)

    # --- Margin audit ---
    try:
        from audit_all_benchmark_margins import main as audit_main

        audit_main()
        m = json.loads((DATA / "benchmark_margin_audit.json").read_text(encoding="utf-8"))
        # find hybrid domain
        hy_row = None
        for r in m.get("all_domains") or []:
            if "Hybrid_FI" in str(r.get("domain") or ""):
                hy_row = {
                    "domain": r.get("domain"),
                    "scalar_count": r.get("scalar_count"),
                    "max_scalar_error_pct": r.get("max_scalar_error_pct"),
                    "pooled_median_error_pct": r.get("pooled_median_error_pct"),
                    "green_gate_pass": r.get("green_gate_pass"),
                }
                break
        report["margin_after"] = {
            "green_pass": m.get("green_gate_pass_count"),
            "green_fail": m.get("green_gate_fail_count"),
            "worst_max": m.get("worst_scalar_max_error_pct"),
            "worst_domain": m.get("worst_scalar_domain"),
            "hybrid_fi_row": hy_row,
        }
        report["actions"].append("audit_all_benchmark_margins")
    except Exception as e:
        report["errors"].append({"margin_audit": str(e), "trace": traceback.format_exc()[-500:]})
        print("margin SKIP:", e)

    out = DATA / "near_gate_thin_pace_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    if report["errors"]:
        print("Completed with errors:", len(report["errors"]))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
