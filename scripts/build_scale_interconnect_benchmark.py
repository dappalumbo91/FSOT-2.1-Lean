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
from fsot_scale_interconnects import perception_summary, suite_rows  # noqa: E402
from tier_gap_fill_lib import _bench_v11, pooled_gate_passes  # noqa: E402

NDBC = ROOT / "vendor" / "public_verifiable" / "live_cache" / "noaa_ndbc_cache.json"
ENDF = ROOT / "data" / "endf_iaea_nuclear_open_benchmark.json"
ECON = ROOT / "data" / "economics_gap_fill_benchmark.json"
BIO = ROOT / "data" / "biology_strict_empirical.json"
OUT = ROOT / "data" / "between_scale_interconnect_benchmark.json"
OUTCOME = ROOT / "results" / "between_scale_interconnect_outcome.json"


def main() -> int:
    _, authority = load_fsot_compute()
    rows = suite_rows(ndbc_path=NDBC, endf_path=ENDF, econ_path=ECON, bio_path=BIO)
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
        maps_to_lean=["acoustical", "energy", "particle", "cosmological", "nuclear", "geological", "biological"],
        d_eff=17,
        authority_path=str(authority).replace("\\", "/"),
        source=[
            "Dziewonski & Anderson 1981 PREM (PEPI) vp/vs + density",
            "Christensen-class crustal vp/vs",
            "ISO/CRC 20C sound speeds; US Standard Atmosphere 1976",
            "NOAA NDBC buoy cache (pres, wtmp, wspd)",
            "IAEA/ENDF levels (He4 C12 O16 Si28 Fe56 Al27)",
            "World Bank YoY dual-fold Economics/Neuroscience",
            "NCBI NC_012920.1 mt-operon lengths; CRC/IUPAC amino-acid MW",
            "CODATA electron/proton mass",
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
        "live_S_ratio_vs_1_is_not_a_0p5_central",
        "perception_t1_view_is_identity_check_not_median_pad",
    ]
    pv = perception_summary(rows)
    pooled_ok = pooled_gate_passes(doc.get("pooled_median_error_pct"))
    t3_ok = bool(pv.get("t3_leftover_ok"))
    status = "GREEN" if pooled_ok and t3_ok else "YELLOW"
    doc["interconnect_status"] = status
    doc["perception_view"] = pv
    doc["gap_fill"] = {
        "seismic_acoustic": "PREM+rocks vp/vs vs π/√3; deep mantle structural",
        "fluid_tanks": "γ from D=5; e+φ water/air; NDBC same buoys on Fluid/Ocean/Air",
        "thermo_cosmo": "Carnot COP dual-fold + |S_T/S_C| vs π/2",
        "nuclear_particle": "IAEA levels dual-fold Nuclear vs Particle",
        "qg_ceiling": "|S_QG/S_C| vs A_bleed; compact remainder vs 1",
        "social_tanks": "World Bank YoY on Economics and Neuroscience; |S_E/S_N| vs 5/4",
        "seis_geo": "PREM lithosphere density dual-fold; |S_seis|/|S_geo| vs φ/2",
        "mat_opt": "CRC n_D dual-fold Optics; density dual-fold Materials; ice n vs φ²/2. S-ratio vs PhysChem/Chem look-split (vs 1 is the wrong object).",
        "opt_qo": "CRC n_D dual-fold Optics and Quantum_Optics; |S_opt|/|S_qo| vs 1 (same C=π/e, adjacent D=10/11).",
        "qm_atomic": "Adjacent D=6/7 at shared δψ=1 vs 1; NIST H–Ca IE / a0 / Rydberg dual-fold. Live mixed S vs 1 is the δψ look, not stuffed.",
        "em_opt": "Adjacent D=9/10 at shared δψ=0.6 vs 1; CRC n on Optics, n² on EM (Maxwell). Ice n² vs (φ²/2)². Live mixed vs 1 retired.",
        "bio_biochem": "Dark same-look D=12/13 vs 1. NCBI mt-operon + AA MW dual-fold. Not Genetics 0.13 Å. Do not flip Biology observed.",
        "atomic_hep": "Same D=7 look-split 0.85/0.95 folded onto QM D=6. CODATA m_e/m_p + IE_H dual-fold. vs 1 retired.",
        "chem_pc": "Same D=8 0.5/0.6 look vs mat-opt. CRC rho/MW on Chemistry, Tm/Tb on PhysChem.",
        "chem_mol": "Adjacent D=8/9 at shared δψ=0.6 vs 1. CRC MW dual-fold. Live mixed vs 1 retired.",
        "physchem_mol": "Adjacent D=8/9 both δψ=0.5 vs 1. CRC Tm on PhysChem, MW on Mol.",
        "ac_opt": "Same D=10 look 0.3/0.6 folded onto D=9. CRC c vs n. vs 1 retired.",
        "ac_mat": "Same D=10 look 0.3/0.5 folded onto D=9. CRC c vs ρ. vs 1 retired.",
        "mol_ac": "Adjacent D=9/10 at δψ=0.5 vs 1. CRC MW vs c. Live mixed vs 1 retired.",
        "cm_thermo": "Adjacent D=14/15 at δψ=0.5 vs 1. CRC metal ρ vs Tm. Live mixed vs 1 retired.",
        "em_mat": "Adjacent D=9/10 at δψ=0.5 vs 1. CRC n² on EM, ρ on Materials. Live mixed vs 1 retired.",
        "biochem_neuro": "Adjacent D=13/14 at δψ=0.7 vs 1. Transmitter AA MW. Not social-tank GDP. Live mixed vs 1 retired.",
        "atomic_chem": "Adjacent D=7/8 at δψ=0.6 vs 1. NIST IE on Atomic, CRC MW on Chemistry.",
        "atomic_pc": "Adjacent D=7/8 at δψ=0.5 vs 1. NIST IE on Atomic, CRC Tm on PhysChem.",
        "hep_chem": "Adjacent D=7/8 at δψ=0.6 vs 1. NIST IE on HEP, CRC MW on Chemistry.",
        "hep_pc": "Adjacent D=7/8 at δψ=0.5 vs 1. NIST IE on HEP, CRC Tm on PhysChem.",
        "pc_em": "Adjacent D=8/9 at δψ=0.5 vs 1. CRC Tm on PhysChem, n² on EM.",
        "em_mol": "Same D=9 0.7/0.5 folded onto D=8. CRC n² vs MW. vs 1 retired.",
        "mol_mat": "Adjacent D=9/10 both δψ=0.5 vs 1. CRC MW vs density.",
        "mol_opt": "Adjacent D=9/10 at δψ=0.5 vs 1. CRC MW vs n. Live mixed vs 1 retired.",
        "ac_qo": "Adjacent D=10/11 at δψ=0.6 vs 1. CRC c vs n photon. Live mixed vs 1 retired.",
        "mat_qo": "Adjacent D=10/11 at δψ=0.5 vs 1. CRC ρ vs n photon. Live mixed vs 1 retired.",
        "nuclear_thermo": "Same D=15 1/0.9 look folded onto D=14. ENDF keV + Carnot dual-route.",
        "fluid_thermo": "Same D=15; Fluid stays dark. Carnot COP dual-route. Live vs 1 is observed mix.",
        "meteo_atm": "Dark same-look D=16/17 at δψ=0.8. NDBC pressure dual-route. Do not flip dark.",
        "biochem_cm": "Adjacent D=13/14 at δψ=0.5 vs 1. CRC AA MW on Biochem, metal ρ on CM.",
        "cm_neuro": "Same D=14 look 0.5/0.7 folded onto D=13. CRC ρ vs transmitter AA. vs 1 retired.",
        "cm_fluid": "Ice ρ on CM, water ρ on Fluid. Fluid stays dark. Live vs 1 is observed mix.",
        "cm_nuclear": "Adjacent D=14/15 at δψ=0.5 vs 1. CRC metal ρ + ENDF keV dual-route.",
        "neuro_thermo": "Adjacent D=14/15 at δψ=0.7 hits=1 vs 1. Transmitter AA vs Carnot. Not GDP.",
        "fluid_nuclear": "Same D=15; Fluid stays dark. Carnot + ENDF dual-route. Live vs 1 is observed mix.",
        "fluid_meteo": "Dark same-look D=15/16 at δψ=0.8 hits=2. NDBC pressure. Do not flip dark.",
        "perception_view": "|1+T1_i|/|1+T1_j| vs live |S_i|/|S_j| (T3 leftover). vs 1 is the same-view question, not a 0.5% central. Not a median pad.",
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
        "perception_view": pv,
        "kill": (
            "tight-scalar median > 0.5%, or T3 leftover on perception_view_t1 > 0.5%, "
            "or anyone fits Q / γ / Poisson, "
            "or anyone treats deep-PREM mismatch as a license for a new coefficient, "
            "or anyone stuffs live |S_i|/|S_j| vs 1 into 0.5%"
        ),
    }
    OUTCOME.parent.mkdir(parents=True, exist_ok=True)
    OUTCOME.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUTCOME}")
    print(f"  n_scalar={len(tight)} n_total={len(rows)} pooled={doc.get('pooled_median_error_pct')} {status}")
    print(
        f"  perception_view n={pv.get('n_pairs')} "
        f"max_t3_leftover={pv.get('max_t3_leftover_pct')} "
        f"max_live_vs_1={pv.get('max_live_vs_1_pct')} "
        f"t3_ok={pv.get('t3_leftover_ok')}"
    )
    for p, med in sorted(channel_med.items(), key=lambda kv: -(kv[1] or 0)):
        print(f"  {p}: median={med:.4f}% n={len(by_prop[p])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
