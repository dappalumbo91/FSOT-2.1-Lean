#!/usr/bin/env python3
"""Build between-scale interconnect panel (five physical-condition gaps)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
from fsot_scale_interconnects import suite_rows  # noqa: E402
from tier_gap_fill_lib import _bench_v11, pooled_gate_passes  # noqa: E402

NDBC = ROOT / "vendor" / "public_verifiable" / "live_cache" / "noaa_ndbc_cache.json"
ENDF = ROOT / "data" / "endf_iaea_nuclear_open_benchmark.json"
OUT = ROOT / "data" / "between_scale_interconnect_benchmark.json"
OUTCOME = ROOT / "results" / "between_scale_interconnect_outcome.json"


def main() -> int:
    _, authority = load_fsot_compute()
    rows = suite_rows(ndbc_path=NDBC, endf_path=ENDF)
    tight = [r for r in rows if r.get("record_kind") == "scalar"]
    by_prop: dict[str, list[float]] = {}
    for r in tight:
        by_prop.setdefault(str(r["property"]), []).append(float(r["error_pct"]))
    channel_stats = [
        ("fsot_prediction", prop, errs) for prop, errs in sorted(by_prop.items()) if errs
    ]
    all_errs = [float(r["error_pct"]) for r in tight]
    doc = _bench_v11(
        domain="Between_Scale_Interconnects",
        material_records=rows,
        maps_to_lean=["acoustical", "energy", "particle", "cosmological", "nuclear"],
        d_eff=17,
        authority_path=str(authority).replace("\\", "/"),
        source=[
            "Dziewonski & Anderson 1981 PREM (PEPI)",
            "Christensen-class crustal vp/vs",
            "ISO/CRC 20C sound speeds; US Standard Atmosphere 1976",
            "NOAA NDBC buoy cache (pres, wtmp, wspd)",
            "IAEA/ENDF levels (He4 C12 O16 Si28 Fe56 Al27)",
            "vendor/fsot_scale_interconnects.py",
        ],
        channel_stats=channel_stats or [("fsot_prediction", "scale_interconnect", all_errs)],
        sota_baselines={
            "scale_interconnect": {
                "sota_typical_error_pct": 10.0,
                "sota_model": "Siloed domain panels with no κ_ij residual",
            }
        },
    )
    doc["tier"] = 51
    doc["policy"] = [
        "no_new_coefficient",
        "deep_PREM_is_phase_change_not_retune",
        "no_identity_pads",
        "zebrafish_genetics_owned_by_sibling",
    ]
    status = "GREEN" if pooled_gate_passes(doc.get("pooled_median_error_pct")) else "YELLOW"
    doc["interconnect_status"] = status
    doc["gap_fill"] = {
        "seismic_acoustic": "PREM+rocks vp/vs vs π/√3; deep mantle structural",
        "fluid_tanks": "γ from D=5; e+φ water/air; NDBC same buoys on Fluid/Ocean/Air",
        "thermo_cosmo": "Carnot COP dual-fold + |S_T/S_C| vs π/2",
        "nuclear_particle": "IAEA levels dual-fold Nuclear vs Particle",
        "qg_ceiling": "|S_QG/S_C| vs A_bleed; compact remainder vs 1",
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    def _med(errs: list[float]) -> float | None:
        if not errs:
            return None
        s = sorted(errs)
        return s[len(s) // 2]

    channel_med = {p: _med(e) for p, e in by_prop.items()}
    outcome = {
        "pin": "D1D38A",
        "status": status,
        "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
        "n_scalar": len(tight),
        "n_total": len(rows),
        "channel_median_error_pct": channel_med,
        "kill": (
            "tight-scalar median > 0.5%, or anyone fits Q / γ / Poisson, "
            "or anyone treats deep-PREM mismatch as a license for a new coefficient"
        ),
    }
    OUTCOME.parent.mkdir(parents=True, exist_ok=True)
    OUTCOME.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUTCOME}")
    print(f"  n_scalar={len(tight)} n_total={len(rows)} pooled={doc.get('pooled_median_error_pct')} {status}")
    for p, med in sorted(channel_med.items(), key=lambda kv: -(kv[1] or 0)):
        print(f"  {p}: median={med:.4f}% n={len(by_prop[p])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
