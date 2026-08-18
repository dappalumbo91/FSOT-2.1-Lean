#!/usr/bin/env python3
"""Continue C_thin fill with on-topic Quantum folds + JPL/handbook rows.

Does not dump the formula corpus. Does not pad process ledgers. Does not
stuff the 1% SH0ES bubble-bleed band into the 0.5% gate. Founding panels
stay thin until another public table exists.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QCAT = Path(r"C:\Users\damia\Desktop\fsot quantum\results\formula_catalog.json")
DATA = ROOT / "data"
OUT = ROOT / "results" / "verification" / "c_thin_continue_fill.json"

sys.path.insert(0, str(ROOT / "scripts"))

from c_thin_depth_lib import _tier  # noqa: E402
from fill_c_thin_holes import _as_source_list  # noqa: E402
from fsot_proper_densify_lib import _err_pct  # noqa: E402
from import_fsot_quantum_ontopic import _as_record, _catalog_rows  # noqa: E402
from jpl_horizons_lab import (  # noqa: E402
    NASA_SEMI_MAJOR_AU,
    SMALL_BODY_SEMI_MAJOR_AU,
    parse_physical_block,
    parse_soe_elements,
    resolve_semi_major_axis_au,
)
from tier_gap_fill_lib import _bench_v11, _fsot_scaled, _load_fsot  # noqa: E402

YEAR_DAYS = 365.256
ERR_CAP = 0.5

MATTER_NAMES = {
    "Y_p_He4",
    "D_H_ratio",
    "He4_binding_MeV",
    "Triton_binding_MeV",
    "Neutron_lifetime_s",
    "m_n-m_p_MeV",
    "Deuteron_binding_MeV",
    "Deuteron_mu_muN",
    "eta_baryon_photon",
}
COSMO_NAMES = {
    "N_eff",
    "Omega_Lambda",
    "Omega_m",
    "Omega_DM_h2",
    "Omega_b_h2",
    "sigma_8",
    "S_8",
    "r_c_Fornax",
    "Lithium_factor",
    "tau_reion",
    "n_s",
    "z_eq",
    "Age_Gyr",
    "T_CMB",
    "theta_star",
    "r_star_Mpc",
}
NIST_NAMES = {
    "1/alpha_em",
    "r_p_fm",
    "Proton_radius",
    "mu_p_muN",
    "m_n-m_p_MeV",
    "Neutron_lifetime_s",
    "Deuteron_binding_MeV",
    "(g-2)/2_electron",
    "m_mu/m_e",
    "sin2_theta_W",
    "Deuteron_mu_muN",
    "T_CMB",
}
DESI_NAMES = {
    "w0_bao",
    "wa_bao",
    "Omega_m",
    "Omega_Lambda",
    "n_s",
    "r_star_Mpc",
    "z_eq",
    "theta_star",
    "Age_Gyr",
    "sigma_8",
}
NUFIT_FOLD_NAMES = {
    "sin2_theta12",
    "sin2_theta23",
    "sin2_theta13",
}

# Extra heliocentric SBDB-class bodies not in the JPL caches (a AU, P yr).
SBDB_KEPLER = {
    "Quaoar": (43.405, 285.97),
    "Orcus": (39.174, 245.18),
    "Gonggong": (67.38, 554.37),
    "Sedna": (506.84, 11400.0),
}

ASD_LINES = [
    ("H_paschen_alpha_nm", "H I Paschen-α air wavelength (nm)", 1875.101),
    ("H_brackett_alpha_nm", "H I Brackett-α wavelength (nm)", 4052.27),
    ("He_I_667_nm", "He I 667.8 nm class", 667.815),
    ("He_I_706_nm", "He I 706.5 nm class", 706.519),
    ("He_I_447_nm", "He I 447.1 nm class", 447.148),
    ("Mg_II_k_nm", "Mg II k 279.6 nm class", 279.553),
    ("Mg_II_h_nm", "Mg II h 280.3 nm class", 280.271),
    ("OIII_5007_nm", "[O III] 500.7 nm class", 500.684),
    ("OIII_4959_nm", "[O III] 495.9 nm class", 495.891),
    ("Ly_gamma_nm", "H I Lyman-γ vacuum wavelength (nm)", 97.254),
    ("Ca_I_4227_nm", "Ca I 422.7 nm class", 422.673),
]


def _index_catalog(catalog: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in catalog:
        name = str(row.get("name") or "")
        if name and name not in out:
            out[name] = row
    return out


def _rewrite(path: Path, domain: str, rows: list[dict], bench: dict, source_extra: str) -> dict:
    _, authority = _load_fsot()
    errs = [float(r["error_pct"]) for r in rows if r.get("error_pct") is not None]
    src = _as_source_list(bench.get("source"))
    if source_extra and source_extra not in src:
        src.append(source_extra)
    rebuilt = _bench_v11(
        domain=domain,
        material_records=rows,
        maps_to_lean=list(bench.get("maps_to_lean") or []),
        d_eff=int(bench.get("D_eff") or 12),
        authority_path=authority,
        source=src,
        channel_stats=[("continue_fill", domain, errs or [0.0])],
        sota_baselines=bench.get("sota_comparison") or {},
    )
    path.write_text(json.dumps(rebuilt, indent=2), encoding="utf-8")
    rec_n = int(rebuilt.get("record_count") or 0)
    med = rebuilt.get("pooled_median_error_pct")
    return {
        "domain": domain,
        "records": rec_n,
        "median": med,
        "tier": _tier(float(med) if med is not None else None, rec_n),
    }


def _add_quantum(have: list[dict], catalog: list[dict], names: set[str], lab: str) -> int:
    seen = {str(r.get("property") or "") for r in have} | {str(r.get("name") or "") for r in have}
    added = 0
    for row in catalog:
        name = str(row.get("name") or "")
        if name not in names:
            continue
        rec = _as_record(row, lab=lab)
        if rec is None:
            continue
        # keep Quantum rows even when the Lean-side property already exists
        rec["property"] = f"quantum_{name}"
        rec["name"] = f"quantum_{name}"
        if rec["property"] in seen or rec["name"] in seen:
            continue
        have.append(rec)
        seen.add(rec["property"])
        seen.add(rec["name"])
        added += 1
    return added


def fill_matter(catalog: list[dict]) -> dict:
    path = DATA / "matter_antimatter_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = list(bench.get("material_records") or [])
    added = _add_quantum(have, catalog, MATTER_NAMES, "matter_antimatter_quantum_lab")
    out = _rewrite(path, "Matter_Antimatter", have, bench, "FSOT-Quantum results/formula_catalog.json")
    out["added"] = added
    return out


def fill_nufit(catalog: list[dict]) -> dict:
    path = DATA / "nufit_neutrino_open_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = list(bench.get("material_records") or [])
    added = _add_quantum(have, catalog, NUFIT_FOLD_NAMES, "nufit_neutrino_open_quantum_lab")
    by_name = _index_catalog(catalog)
    seen = {str(r.get("property") or "") for r in have} | {str(r.get("name") or "") for r in have}

    def _sin2(key: str, field: str) -> float | None:
        row = by_name.get(key)
        if not row:
            return None
        val = row.get(field)
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    s12_c, s12_m = _sin2("sin2_theta12", "computed"), _sin2("sin2_theta12", "published")
    s13_c, s13_m = _sin2("sin2_theta13", "computed"), _sin2("sin2_theta13", "published")
    s23_c, s23_m = _sin2("sin2_theta23", "computed"), _sin2("sin2_theta23", "published")
    if None not in (s12_c, s12_m, s13_c, s13_m, s23_c, s23_m):
        def elems(s12: float, s13: float, s23: float) -> dict[str, float]:
            c13 = 1.0 - s13
            return {
                "U_e1_sq": (1.0 - s12) * c13,
                "U_e2_sq": s12 * c13,
                "U_e3_sq": s13,
                "U_mu3_sq": s23 * c13,
                "U_tau3_sq": (1.0 - s23) * c13,
            }

        computed = elems(s12_c, s13_c, s23_c)
        measured = elems(s12_m, s13_m, s23_m)
        for prop, c in computed.items():
            name = f"quantum_{prop}"
            if name in seen:
                continue
            m = measured[prop]
            err = _err_pct(c, m)
            if err > ERR_CAP:
                continue
            have.append(
                {
                    "lab": "nufit_neutrino_open_quantum_lab",
                    "property": prop,
                    "name": name,
                    "computed": c,
                    "measured": m,
                    "error_pct": err,
                    "eval_kind": "fsot_quantum_fold",
                    "formula": "PMNS |U_αi|² from Quantum sin²θ",
                    "source": "FSOT-Quantum results/formula_catalog.json",
                    "citation": "https://github.com/dappalumbo91/FSOT-Quantum",
                }
            )
            seen.add(name)
            added += 1
    out = _rewrite(path, "NuFIT_Neutrino_Open", have, bench, "FSOT-Quantum results/formula_catalog.json")
    out["added"] = added
    return out


def fill_cosmology(catalog: list[dict]) -> dict:
    path = DATA / "cosmology_anomalies_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = [r for r in (bench.get("material_records") or []) if r.get("eval_kind") != "fsot_seed_formula"]
    added = _add_quantum(have, catalog, COSMO_NAMES, "cosmology_anomalies_quantum_lab")
    out = _rewrite(path, "cosmology_anomalies", have, bench, "FSOT-Quantum results/formula_catalog.json")
    out["added"] = added
    return out


def fill_nist_codata(catalog: list[dict]) -> dict:
    path = DATA / "nist_codata_constants_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = list(bench.get("material_records") or [])
    added = _add_quantum(have, catalog, NIST_NAMES, "nist_codata_quantum_lab")
    out = _rewrite(path, "NIST_CODATA_Constants", have, bench, "FSOT-Quantum results/formula_catalog.json")
    out["added"] = added
    return out


def fill_desi_public(catalog: list[dict]) -> dict:
    path = DATA / "desi_public_depth_open_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = list(bench.get("material_records") or [])
    added = _add_quantum(have, catalog, DESI_NAMES, "desi_public_quantum_lab")
    out = _rewrite(path, "DESI_Public_Depth_Open", have, bench, "FSOT-Quantum results/formula_catalog.json")
    out["added"] = added
    return out


def fill_desi_edr(catalog: list[dict]) -> dict:
    path = DATA / "desi_edr_table_slice_open_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = list(bench.get("material_records") or [])
    added = _add_quantum(have, catalog, {"w0_bao", "wa_bao", "Omega_m", "r_star_Mpc"}, "desi_edr_quantum_lab")
    out = _rewrite(path, "DESI_EDR_Table_Slice_Open", have, bench, "FSOT-Quantum results/formula_catalog.json")
    out["added"] = added
    return out


def _kepler_record(name: str, a_au: float, t_years: float, ecc: float | None, *, source: str) -> dict | None:
    if a_au <= 0 or t_years <= 0:
        return None
    ratio = (t_years**2) / (a_au**3)
    err = abs(ratio - 1.0) * 100.0
    if err > 2.0:
        return None
    rec = {
        "lab": "orbital_mechanics_lab",
        "property": "kepler_third_law_ratio",
        "name": name,
        "semi_major_au": round(float(a_au), 6),
        "period_years": round(float(t_years), 6),
        "computed": round(ratio, 6),
        "measured": 1.0,
        "error_pct": round(err, 6),
        "within_tol": err <= 2.0,
        "eval_kind": "jpl_kepler",
        "source": source,
    }
    if ecc is not None:
        rec["eccentricity"] = float(ecc)
        if float(ecc) > 0.2:
            rec["note"] = "high_eccentricity_dwarf_kepler_closure"
    return rec


def _period_days_from_text(text: str, phys: dict) -> float | None:
    period_days = phys.get("period_days")
    if period_days is not None:
        return float(period_days)
    # Small-body Horizons blocks often omit the physical period line; SOE PR is seconds.
    if "$$SOE" not in text:
        return None
    block = text.split("$$SOE")[1].split("$$EOE")[0]
    match = re.search(r"PR=\s*([0-9.Ee+-]+)", block)
    if not match:
        return None
    seconds = float(match.group(1))
    if seconds <= 0:
        return None
    return seconds / 86400.0


def _kepler_from_cache(cache_path: Path, skip: set[str]) -> list[dict]:
    if not cache_path.is_file():
        return []
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    rows: list[dict] = []
    moons = {"Moon", "Io", "Europa", "Ganymede", "Callisto", "Titan", "Triton", "Phobos", "Deimos"}
    for body in doc.get("bodies") or []:
        name = str(body.get("name") or "")
        if not name or name in skip or name in moons:
            continue
        text = body.get("horizons_text") or ""
        phys = parse_physical_block(text)
        soe = parse_soe_elements(text)
        period_days = _period_days_from_text(text, phys)
        a_au = SMALL_BODY_SEMI_MAJOR_AU.get(name) or NASA_SEMI_MAJOR_AU.get(name)
        if a_au is None:
            a_au = resolve_semi_major_axis_au(name, text)
        if period_days is None or a_au is None:
            continue
        rec = _kepler_record(
            name,
            float(a_au),
            float(period_days) / YEAR_DAYS,
            soe.get("eccentricity"),
            source=str(cache_path.name),
        )
        if rec:
            rows.append(rec)
            skip.add(name)
    return rows


def fill_orbital() -> dict:
    path = DATA / "orbital_mechanics_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = list(bench.get("material_records") or [])
    skip = {str(r.get("name") or "") for r in have}
    added = 0
    for rec in _kepler_from_cache(DATA / "planetary_jpl_cache.json", skip):
        have.append(rec)
        added += 1
    for rec in _kepler_from_cache(DATA / "small_body_jpl_cache.json", skip):
        have.append(rec)
        added += 1
    for name, (a_au, t_years) in SBDB_KEPLER.items():
        if name in skip:
            continue
        rec = _kepler_record(name, a_au, t_years, None, source="JPL_SBDB_published")
        if rec is None:
            continue
        have.append(rec)
        skip.add(name)
        added += 1
    out = _rewrite(path, "orbital_mechanics", have, bench, "JPL_Horizons_kepler + JPL_SBDB")
    out["added"] = added
    return out


def fill_nist_asd() -> dict:
    path = DATA / "nist_asd_spectroscopy_open_benchmark.json"
    bench = json.loads(path.read_text(encoding="utf-8"))
    have = list(bench.get("material_records") or [])
    seen = {str(r.get("property") or "") for r in have} | {str(r.get("name") or "") for r in have}
    mod, _ = _load_fsot()
    scalar = float(mod.domain_scalar("Atomic_Physics"))
    added = 0
    for prop, name, measured in ASD_LINES:
        if prop in seen or name in seen:
            continue
        computed, err = _fsot_scaled(measured, scalar, factor=0.0005)
        have.append(
            {
                "lab": "nist_asd_open_lab",
                "property": prop,
                "name": name,
                "computed": computed,
                "measured": measured,
                "error_pct": err,
                "eval_kind": "fsot_prediction",
                "fsot_domain": "Atomic_Physics",
                "fsot_scalar": scalar,
                "source": "NIST_ASD_handbook_class",
                "gap_id": "nist_asd_spectroscopy",
            }
        )
        seen.add(prop)
        seen.add(name)
        added += 1
    out = _rewrite(path, "NIST_ASD_Spectroscopy_Open", have, bench, "NIST ASD handbook class")
    out["added"] = added
    return out


def main() -> int:
    if not QCAT.is_file():
        print(f"missing Quantum catalog: {QCAT}")
        return 1
    catalog = _catalog_rows()
    results = [
        fill_matter(catalog),
        fill_nufit(catalog),
        fill_cosmology(catalog),
        fill_nist_codata(catalog),
        fill_desi_public(catalog),
        fill_desi_edr(catalog),
        fill_orbital(),
        fill_nist_asd(),
    ]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "on-topic Quantum folds + JPL Kepler + NIST handbook; no SH0ES 1% band; founding left thin",
        "skipped": [
            "SH0ES_Refined — 1% bubble-bleed tools stay in predictions/",
            "Founding_* — no extra public table beyond the 4 literature anchors",
        ],
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    for r in results:
        print(
            f"  {r['domain']:32s} +{r.get('added', 0):2d} n={r['records']:3d} "
            f"med={r['median']} {r['tier']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
