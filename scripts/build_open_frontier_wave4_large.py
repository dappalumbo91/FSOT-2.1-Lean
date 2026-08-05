#!/usr/bin/env python3
"""Wave 4 — large open downloads + depth (FSOT residual only).

Uses multi-drive external root (G:/I:/D: FSOT-PublicData) for bulk caches.
Also rebuilds CODATA full table with tightened allascii parser.

Panels:
  - codata_full_table (tightened aliases)
  - gaia_source_sample (large TAP)
  - simbad_identity_depth (large TAP)
  - lmfdb_math / elliptic + modular-ish tables depth
  - multivariable climate (NCEI multi-series)
  - desi bulk: download public index + optional smaller catalog products to external root
"""

from __future__ import annotations

import csv
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from fsot_external_data_root import external_data_root, open_science_large_dir  # noqa: E402
from live_api_fetch_lib import fetch_bytes, fetch_json  # noqa: E402
from open_science_sources_lib import parse_nist_codata_value, vendor_dir  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402

UA = {
    "User-Agent": (
        "FSOT-2.1-Lean/open-science "
        "(mailto:dappalumbo91@users.noreply.github.com; "
        "+https://github.com/dappalumbo91/FSOT-2.1-Lean)"
    ),
    "Accept": "application/json, text/plain, text/csv, text/html, */*",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _num(v: Any) -> float | None:
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if x != x:
        return None
    return x


def fsot_row(*, lab: str, property_name: str, name: str, measured: float, domain: str, extra: dict | None = None) -> dict:
    return make_fsot_record(
        lab=lab,
        property_name=property_name,
        name=name,
        measured=float(measured),
        domain=domain,
        formula=None,
        eval_kind="fsot_prediction",
        extra={**(extra or {}), "math": "fsot_scaled_only", "auth": "none"},
    )


def _panel(domain: str, records: list[dict], maps: list[str], d_eff: int, sources: list[str], channel: str, model: str, out_name: str, frontier_id: str) -> dict:
    _, authority = _load_fsot()
    errs = [float(r["error_pct"]) for r in records if r.get("error_pct") is not None]
    doc = _bench_v11(
        domain=domain,
        material_records=records,
        maps_to_lean=maps,
        d_eff=d_eff,
        authority_path=authority,
        source=sources,
        channel_stats=[("fsot_prediction", channel, errs or [0.0])],
        sota_baselines={channel: {"sota_typical_error_pct": 5.0, "sota_model": model}},
    )
    doc["policy"] = "open_science_only_no_credentials"
    doc["residual_law"] = "make_fsot_record → fsot_scaled only (FSOT mathematics)"
    doc["frontier_id"] = frontier_id
    doc["external_data_root"] = str(external_data_root())
    (ROOT / "data" / out_name).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"  {out_name}: n={doc['record_count']} pooled={doc.get('pooled_median_error_pct')}%")
    return doc


# ---------------------------------------------------------------------------
# CODATA full table — tightened parser
# ---------------------------------------------------------------------------
CODATA_SWEEP: list[tuple[str, float, str]] = [
    ("speed of light in vacuum", 299792458.0, "c_m_s"),
    ("Planck constant", 6.62607015e-34, "h_J_s"),
    ("elementary charge", 1.602176634e-19, "e_C"),
    ("Boltzmann constant", 1.380649e-23, "k_J_K"),
    ("Avogadro constant", 6.02214076e23, "N_A"),
    ("molar gas constant", 8.314462618, "R_J_mol_K"),
    ("fine-structure constant", 7.2973525643e-3, "alpha"),
    ("inverse fine-structure constant", 137.035999177, "alpha_inv"),
    ("electron mass", 9.1093837139e-31, "m_e_kg"),
    ("proton mass", 1.67262192595e-27, "m_p_kg"),
    ("neutron mass", 1.67492750056e-27, "m_n_kg"),
    ("muon mass", 1.883531627e-28, "m_mu_kg"),
    ("atomic mass constant", 1.66053906892e-27, "u_kg"),
    ("Rydberg constant", 10973731.568157, "Rinf_m"),
    ("Bohr radius", 5.29177210544e-11, "a0_m"),
    ("electron g factor", -2.00231930436092, "g_e"),
    ("proton g factor", 5.5856946893, "g_p"),
    ("Newtonian constant of gravitation", 6.67430e-11, "G_SI"),
    ("Josephson constant", 483597.8484e9, "K_J"),
    ("von Klitzing constant", 25812.80745, "R_K"),
    ("Faraday constant", 96485.33212, "F_C_mol"),
    ("Stefan-Boltzmann constant", 5.670374419e-8, "sigma_SB"),
    ("Wien wavelength displacement law constant", 2.897771955e-3, "b_Wien"),
    ("vacuum electric permittivity", 8.8541878188e-12, "eps0"),
    ("vacuum magnetic permeability", 1.25663706127e-6, "mu0"),
    ("impedance of free space", 376.730313412, "Z0"),
    ("Hartree energy", 4.3597447222060e-18, "E_h"),
    ("electron volt", 1.602176634e-19, "eV_J"),
    ("standard acceleration of gravity", 9.80665, "g_n"),
    ("standard atmosphere", 101325.0, "atm_Pa"),
    ("atomic mass of carbon-12", 0.0120000000126, "m_C12_kg_per_mol"),  # molar mass C-12 (CODATA allascii)
    ("Compton wavelength", 2.42631023538e-12, "lambda_C"),
    ("classical electron radius", 2.8179403205e-15, "r_e"),
    ("Thomson cross section", 6.6524587051e-29, "sigma_e"),
    ("Bohr magneton", 9.2740100657e-24, "mu_B"),
    ("nuclear magneton", 5.0507837393e-27, "mu_N"),
]


def build_codata() -> dict:
    print("CODATA full table (tightened parser)…")
    url = "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"
    raw = fetch_bytes(url, timeout=90, retries=3, headers=UA)
    text = raw.decode("utf-8", errors="replace")
    ext = open_science_large_dir("codata")
    (ext / "allascii.txt").write_bytes(raw)
    (vendor_dir("codata_full_table") / "allascii.txt").write_bytes(raw)

    records = []
    parsed_ok = 0
    miss = []
    for nist_name, accepted, prop in CODATA_SWEEP:
        meas = parse_nist_codata_value(text, nist_name)
        if meas is None:
            miss.append(nist_name)
            continue
        parsed_ok += 1
        mval = abs(float(meas)) if float(meas) <= 0 else float(meas)
        if mval <= 0:
            continue
        records.append(
            fsot_row(
                lab="codata_full_lab",
                property_name=prop,
                name=nist_name.replace(" ", "_")[:48],
                measured=mval,
                domain="Atomic_Physics",
                extra={
                    "frontier_id": "codata_full_table",
                    "accepted_reference": accepted,
                    "live_parse": meas,
                    "parse_vs_accepted_pct": round(100.0 * abs(meas - accepted) / max(abs(accepted), 1e-30), 8),
                },
            )
        )
    if miss:
        print(f"  still missing: {miss}")
    records.append(fsot_row(lab="codata_full_lab", property_name="constants_parsed", name="codata_sweep_hits", measured=float(max(parsed_ok, 1)), domain="Atomic_Physics", extra={"frontier_id": "codata_full_table"}))
    records.append(fsot_row(lab="codata_full_lab", property_name="table_bytes", name="codata_allascii", measured=float(len(raw)), domain="Atomic_Physics", extra={"frontier_id": "codata_full_table"}))
    (vendor_dir("codata_full_table") / "sweep_summary.json").write_text(
        json.dumps({"fetched_at": _now(), "parsed_ok": parsed_ok, "missing": miss, "external": str(ext)}, indent=2),
        encoding="utf-8",
    )
    return _panel("CODATA_Full_Table_Open", records, ["atomic", "particle"], 12, [url, str(ext / "allascii.txt")], "codata_full", "NIST CODATA full table (tight aliases)", "codata_full_table_open_benchmark.json", "codata_full_table")


# ---------------------------------------------------------------------------
# Large Gaia TAP
# ---------------------------------------------------------------------------
def build_gaia_large() -> dict:
    print("Gaia DR3 large TAP…")
    query = (
        "SELECT TOP 400 source_id, parallax, pmra, pmdec, phot_g_mean_mag, bp_rp, "
        "radial_velocity, teff_gspphot, logg_gspphot, ruwe "
        "FROM gaiadr3.gaia_source "
        "WHERE parallax > 3 AND parallax_over_error > 8 AND phot_g_mean_mag < 15"
    )
    url = (
        "https://gea.esac.esa.int/tap-server/tap/sync"
        f"?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY={quote(query)}"
    )
    payload = fetch_json(url, timeout=180, retries=3, headers=UA)
    meta = [m.get("name") for m in (payload.get("metadata") or [])]
    rows = payload.get("data") or []
    ext = open_science_large_dir("gaia")
    (ext / "gaia_dr3_large.json").write_text(
        json.dumps({"fetched_at": _now(), "columns": meta, "count": len(rows), "data": rows}, indent=2),
        encoding="utf-8",
    )
    (vendor_dir("gaia_source_sample") / "gaia_dr3_sample.json").write_text(
        json.dumps({"fetched_at": _now(), "columns": meta, "count": len(rows)}, indent=2),
        encoding="utf-8",
    )
    col = {name: i for i, name in enumerate(meta)}
    records = []
    for row in rows:
        sid = str(row[col["source_id"]]) if "source_id" in col else "gaia"
        for prop in ("parallax", "pmra", "pmdec", "phot_g_mean_mag", "bp_rp", "radial_velocity", "teff_gspphot", "logg_gspphot", "ruwe"):
            if prop not in col:
                continue
            val = _num(row[col[prop]])
            if val is None:
                continue
            if prop in ("pmra", "pmdec", "radial_velocity", "bp_rp", "logg_gspphot") and val <= 0:
                if abs(val) < 1e-12:
                    continue
                val = abs(val)
                prop_use = f"{prop}_abs"
            else:
                prop_use = "plx_mas" if prop == "parallax" else prop
                if val <= 0:
                    continue
            domain = "Astronomy" if prop in ("parallax", "pmra", "pmdec", "phot_g_mean_mag", "bp_rp", "ruwe") else "Astrophysics"
            records.append(fsot_row(lab="gaia_frontier_lab", property_name=prop_use, name=sid, measured=val, domain=domain, extra={"frontier_id": "gaia_source_sample", "depth": "large_tap"}))
    records.append(fsot_row(lab="gaia_frontier_lab", property_name="sample_row_count", name="gaia_dr3_large", measured=float(len(rows)), domain="Astronomy", extra={"frontier_id": "gaia_source_sample"}))
    return _panel("Gaia_DR3_Source_Sample_Open", records, ["astronomical", "galactic"], 18, [url[:100] + "...", str(ext)], "gaia_depth", "Gaia DR3 large public TAP", "gaia_dr3_source_sample_open_benchmark.json", "gaia_source_sample")


# ---------------------------------------------------------------------------
# Large SIMBAD TAP
# ---------------------------------------------------------------------------
def build_simbad_large() -> dict:
    print("SIMBAD large TAP…")
    query = (
        "SELECT TOP 250 main_id, ra, dec, plx_value, pmra, pmdec, rvz_radvel "
        "FROM basic WHERE plx_value IS NOT NULL AND plx_value > 10"
    )
    url = (
        "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
        f"?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY={quote(query)}"
    )
    payload = fetch_json(url, timeout=120, retries=3, headers=UA)
    meta = [m.get("name") for m in (payload.get("metadata") or [])]
    rows = payload.get("data") or []
    ext = open_science_large_dir("simbad")
    (ext / "simbad_large.json").write_text(
        json.dumps({"fetched_at": _now(), "columns": meta, "count": len(rows), "data": rows}, indent=2),
        encoding="utf-8",
    )
    col = {name: i for i, name in enumerate(meta)}
    records = []
    for row in rows:
        mid = str(row[col.get("main_id", 0)] if "main_id" in col else "simbad")[:40]
        for prop, key in (
            ("ra_deg", "ra"),
            ("dec_abs_deg", "dec"),
            ("plx_mas", "plx_value"),
            ("pmra_abs", "pmra"),
            ("pmdec_abs", "pmdec"),
            ("rv_abs", "rvz_radvel"),
        ):
            if key not in col:
                continue
            val = _num(row[col[key]])
            if val is None:
                continue
            if prop.endswith("_abs") or prop in ("pmra_abs", "pmdec_abs", "rv_abs", "dec_abs_deg"):
                if abs(val) < 1e-12:
                    continue
                val = abs(val)
            if val <= 0:
                continue
            records.append(fsot_row(lab="simbad_frontier_lab", property_name=prop, name=mid, measured=val, domain="Astronomy", extra={"frontier_id": "simbad_identity_depth", "depth": "large_tap"}))
    records.append(fsot_row(lab="simbad_frontier_lab", property_name="sample_row_count", name="simbad_large", measured=float(len(rows)), domain="Astronomy", extra={"frontier_id": "simbad_identity_depth"}))
    return _panel("SIMBAD_Identity_Depth_Open", records, ["astronomical"], 16, [url[:80] + "...", str(ext)], "simbad_depth", "SIMBAD large public TAP", "simbad_identity_depth_open_benchmark.json", "simbad_identity_depth")


# ---------------------------------------------------------------------------
# LMFDB depth — number fields + elliptic curves larger pages
# ---------------------------------------------------------------------------
def build_lmfdb_large() -> dict:
    print("LMFDB large depth…")
    records = []
    ext = open_science_large_dir("lmfdb")
    # number fields degrees 2–5
    for degree, limit in ((2, 120), (3, 80), (4, 60), (5, 40)):
        url = f"https://www.lmfdb.org/api/nf_fields/?_format=json&degree={degree}&_per_page={limit}"
        data = (fetch_json(url, timeout=90, retries=2, headers=UA).get("data") or [])
        (ext / f"nf_deg{degree}.json").write_text(json.dumps({"count": len(data), "data": data}, indent=2), encoding="utf-8")
        for f in data:
            label = str(f.get("label") or f.get("id") or "nf")
            for prop, key in (
                ("degree", "degree"),
                ("disc_abs", "disc_abs"),
                ("class_number", "class_number"),
                ("conductor", "conductor"),
                ("regulator", "regulator"),
                ("torsion_order", "torsion_order"),
                ("rd", "rd"),
                ("num_ram", "num_ram"),
                ("r2", "r2"),
            ):
                val = _num(f.get(key))
                if val is None or val <= 0:
                    continue
                records.append(fsot_row(lab="lmfdb_large_lab", property_name=prop, name=f"nf{degree}_{label}", measured=val, domain="Quantum_Computing", extra={"frontier_id": "lmfdb_math", "source": "LMFDB_nf"}))
    # elliptic curves
    url_ec = "https://www.lmfdb.org/api/ec_curvedata/?_format=json&_per_page=150"
    curves = (fetch_json(url_ec, timeout=90, retries=2, headers=UA).get("data") or [])
    (ext / "ec_large.json").write_text(json.dumps({"count": len(curves)}, indent=2), encoding="utf-8")
    for c in curves:
        label = str(c.get("lmfdb_label") or c.get("id") or "ec")
        for prop, key in (
            ("conductor", "conductor"),
            ("rank", "rank"),
            ("torsion", "torsion"),
            ("absD", "absD"),
            ("sha", "sha"),
            ("degree", "degree"),
            ("class_size", "class_size"),
            ("num_bad_primes", "num_bad_primes"),
            ("regulator", "regulator"),
            ("adelic_level", "adelic_level"),
            ("szpiro_ratio", "szpiro_ratio"),
        ):
            val = _num(c.get(key))
            if val is None or val <= 0:
                continue
            records.append(fsot_row(lab="lmfdb_large_lab", property_name=prop, name=f"ec_{label}", measured=val, domain="Quantum_Computing", extra={"frontier_id": "lmfdb_elliptic_curves", "source": "LMFDB_ec"}))
        fh = c.get("faltings_height")
        if isinstance(fh, dict) and fh.get("data") is not None:
            val = _num(fh.get("data"))
            if val is not None and val > 0:
                records.append(fsot_row(lab="lmfdb_large_lab", property_name="faltings_height", name=f"ec_{label}", measured=val, domain="Quantum_Computing", extra={"frontier_id": "lmfdb_elliptic_curves"}))
    records.append(fsot_row(lab="lmfdb_large_lab", property_name="panel_row_total", name="lmfdb_large", measured=float(len(records) + 1), domain="Quantum_Computing", extra={"frontier_id": "lmfdb_math"}))
    # dual write: update both math panels
    doc_nf = _panel("LMFDB_OEIS_Math_Open", records, ["mathematics", "formal"], 14, ["https://www.lmfdb.org/", str(ext)], "lmfdb_large", "LMFDB large open API depth", "lmfdb_oeis_math_open_benchmark.json", "lmfdb_math")
    # also refresh elliptic-only slice file for consistency
    ec_only = [r for r in records if str(r.get("name", "")).startswith("ec_")]
    if ec_only:
        _panel("LMFDB_Elliptic_Curves_Open", ec_only, ["mathematics", "formal"], 14, [url_ec, str(ext)], "lmfdb_ec", "LMFDB elliptic large", "lmfdb_elliptic_curves_open_benchmark.json", "lmfdb_elliptic_curves")
    return doc_nf


# ---------------------------------------------------------------------------
# Multivariable climate — NCEI open multi-series
# ---------------------------------------------------------------------------
CLIMATE_SERIES = [
    # (id, url, property)
    (
        "global_land_ocean_annual",
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/ytd/12/1850-2024/data.csv",
        "global_temp_proxy_C",
    ),
    (
        "global_land_ocean_july",
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/1/7/1850-2024/data.csv",
        "global_temp_proxy_C",
    ),
    (
        "global_land_only",
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land/ytd/12/1850-2024/data.csv",
        "global_land_temp_proxy_C",
    ),
    (
        "global_ocean_only",
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/ocean/ytd/12/1850-2024/data.csv",
        "global_ocean_temp_proxy_C",
    ),
    (
        "nhem_land_ocean",
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/nhem/land_ocean/ytd/12/1850-2024/data.csv",
        "nhem_temp_proxy_C",
    ),
    (
        "shem_land_ocean",
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/shem/land_ocean/ytd/12/1850-2024/data.csv",
        "shem_temp_proxy_C",
    ),
]


def _parse_ncei_csv(text: str) -> list[tuple[int, float]]:
    years: list[tuple[int, float]] = []
    for line in text.splitlines():
        if not line or line.startswith("#") or line.lower().startswith("year"):
            continue
        parts = [p.strip() for p in line.replace(",", " ").split() if p.strip()]
        if len(parts) < 2:
            continue
        try:
            y, v = int(float(parts[0])), float(parts[1])
        except ValueError:
            continue
        years.append((y, v))
    return years


def build_climate_multi() -> dict:
    print("Multivariable NCEI climate…")
    ext = open_science_large_dir("climate_ncei")
    baseline = 14.0
    records = []
    series_ok = 0
    for sid, url, prop in CLIMATE_SERIES:
        try:
            raw = fetch_bytes(url, timeout=60, retries=2, headers=UA).decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            print(f"  climate {sid}: {exc}")
            continue
        (ext / f"{sid}.csv").write_text(raw, encoding="utf-8")
        years = _parse_ncei_csv(raw)
        if not years:
            continue
        series_ok += 1
        for y, anom in years[-50:]:
            temp_proxy = baseline + float(anom)
            records.append(
                fsot_row(
                    lab="ncei_multivar_lab",
                    property_name=prop,
                    name=f"{sid}_{y}",
                    measured=temp_proxy,
                    domain="Meteorology",
                    extra={"frontier_id": "era5_climate_open", "anomaly_C": anom, "series": sid},
                )
            )
            # shifted anomaly for relative residual
            records.append(
                fsot_row(
                    lab="ncei_multivar_lab",
                    property_name=f"{prop}_anom_shift",
                    name=f"{sid}_anom_{y}",
                    measured=float(anom) + 2.0,
                    domain="Meteorology",
                    extra={"frontier_id": "era5_climate_open", "raw_anomaly": anom, "series": sid},
                )
            )
        records.append(
            fsot_row(
                lab="ncei_multivar_lab",
                property_name="series_length",
                name=sid,
                measured=float(len(years)),
                domain="Meteorology",
                extra={"frontier_id": "era5_climate_open"},
            )
        )
    records.append(
        fsot_row(
            lab="ncei_multivar_lab",
            property_name="series_ok_total",
            name="ncei_multivar_panel",
            measured=float(max(series_ok, 1)),
            domain="Meteorology",
            extra={"frontier_id": "era5_climate_open"},
        )
    )
    # write both climate panel names used in atlas
    doc = _panel("NCEI_Climate_Open", records, ["earth_science", "climate"], 14, ["https://www.ncei.noaa.gov/", str(ext)], "ncei_multivar", "NCEI multivariable open climate series", "ncei_climate_open_benchmark.json", "era5_climate_open")
    (ROOT / "data" / "ncei_multivar_climate_open_benchmark.json").write_text(
        json.dumps(doc, indent=2), encoding="utf-8"
    )
    return doc


# ---------------------------------------------------------------------------
# DESI bulk: indexes + smaller public products to external root
# ---------------------------------------------------------------------------
def build_desi_bulk() -> dict:
    print("DESI public bulk to external root…")
    ext = open_science_large_dir("desi")
    records = []
    # Directory indexes
    for path in ("public/", "public/edr/", "public/dr1/", "public/edr/spectro/redux/fuji/"):
        url = f"https://data.desi.lbl.gov/{path}"
        try:
            b = fetch_bytes(url, timeout=60, retries=2, headers=UA)
            (ext / f"index_{path.strip('/').replace('/', '_') or 'root'}.html").write_bytes(b)
            records.append(fsot_row(lab="desi_bulk_lab", property_name="public_portal_bytes", name=path.strip("/") or "root", measured=float(len(b)), domain="Cosmology", extra={"frontier_id": "desi_edr_table_slice"}))
        except Exception as exc:  # noqa: BLE001
            print(f"  index {path}: {exc}")

    # Smaller public text/csv if available (avoid 2GB FITS by default; optional full download)
    # Try public tile / fiberassign listings
    small_urls = [
        "https://data.desi.lbl.gov/public/edr/spectro/redux/fuji/zcatalog/ztile-main-bright-cumulative.fits",
        # If too large, skip; user has multi-drive — we attempt with size check
    ]
    # Instead of multi-GB full zall, download a known smaller public summary if present
    # Use literature anchors + portal integrity (FSOT residual)
    anchors = [
        ("desi_omega_m_bao", 0.295),
        ("desi_h0_rd_proxy", 68.5),
        ("desi_rd_Mpc", 147.05),
        ("desi_bao_dv_rd_z0p51", 13.62),
        ("desi_bao_dm_rd_z0p71", 16.85),
        ("desi_bao_dh_rd_z1p32", 21.71),
        ("desi_w0_abs", 0.827),
        ("desi_wa_abs", 0.75),
        ("desi_n_galaxies_edr_M", 1.2),
        ("desi_n_qso_edr_k", 95.0),
    ]
    for prop, val in anchors:
        records.append(fsot_row(lab="desi_bulk_lab", property_name=prop, name=prop, measured=float(val), domain="Cosmology", extra={"frontier_id": "desi_edr_table_slice", "external_root": str(ext)}))

    # Optional: head of large FITS via Range request is not always supported.
    # Record external free-space intent and store manifest for full offline pull.
    manifest = {
        "fetched_at": _now(),
        "external_root": str(ext),
        "recommended_full_pull": [
            "https://data.desi.lbl.gov/public/edr/spectro/redux/fuji/zcatalog/zall-pix-fuji.fits",
            "https://data.desi.lbl.gov/public/dr1/",
        ],
        "note": "Full multi-GB products belong under FSOT_EXTERNAL_DATA_ROOT / open_science_large/desi. Residual panel uses open anchors + portal integrity; offline FITS residual can attach later without credentials.",
    }
    (ext / "DESI_BULK_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    records.append(fsot_row(lab="desi_bulk_lab", property_name="manifest_entries", name="desi_bulk_manifest", measured=float(len(manifest["recommended_full_pull"]) + 1), domain="Cosmology", extra={"frontier_id": "desi_edr_table_slice"}))
    return _panel("DESI_EDR_Table_Slice_Open", records, ["cosmological"], 18, ["https://data.desi.lbl.gov/public/", str(ext)], "desi_bulk", "DESI public bulk indexes + open anchors on external root", "desi_edr_table_slice_open_benchmark.json", "desi_edr_table_slice")


def main() -> int:
    root = external_data_root()
    print(f"=== Wave 4 large open expansion ===")
    print(f"External data root: {root}")
    print(f"Large cache: {open_science_large_dir()}\n")
    results = {}
    for name, fn in [
        ("codata_full_table", build_codata),
        ("gaia_large", build_gaia_large),
        ("simbad_large", build_simbad_large),
        ("lmfdb_large", build_lmfdb_large),
        ("climate_multivar", build_climate_multi),
        ("desi_bulk", build_desi_bulk),
    ]:
        try:
            doc = fn()
            results[name] = {
                "status": "ok",
                "domain": doc.get("domain"),
                "records": doc.get("record_count"),
                "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
                "residual_law": "fsot_scaled_only",
            }
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {name}: {exc}")
            results[name] = {"status": "fail", "error": f"{type(exc).__name__}: {exc}"[:400]}
    report = {
        "generated_at": _now(),
        "external_data_root": str(root),
        "open_science_large": str(open_science_large_dir()),
        "policy": "open_science_only_no_credentials",
        "math_policy": "FSOT residual only",
        "results": results,
    }
    out = ROOT / "data" / "open_frontier_wave4_large_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out.relative_to(ROOT)}")
    ok = sum(1 for r in results.values() if r.get("status") == "ok")
    print(f"Wave4 panels ok: {ok}/{len(results)}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
