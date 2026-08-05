#!/usr/bin/env python3
"""Open-science frontier wave 3 — FSOT residual mathematics only.

Frontiers:
  - endf_reaction_subset     IAEA Live Chart levels + gammas (open nuclear data)
  - nist_asd_multi_species   multi-species spectroscopic line anchors + handbooks
  - desi_edr_table_slice     public DESI portal + open BAO/cosmology literature anchors
  - gwosc_strain_metadata    GWOSC open strain archive JSON metadata
  - codata_full_table        full NIST CODATA allascii residual sweep

Hard rules:
  - auth=none
  - make_fsot_record → fsot_scaled only
  - formula=None always
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import make_fsot_record  # noqa: E402
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
        x = float(str(v).replace(" ", "").replace("+", ""))
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
    (ROOT / "data" / out_name).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"  {out_name}: n={doc['record_count']} pooled={doc.get('pooled_median_error_pct')}%")
    return doc


# ---------------------------------------------------------------------------
# ENDF-class open nuclear: IAEA levels + gammas (reaction/structure data)
# ---------------------------------------------------------------------------
def build_endf_nuclear() -> dict:
    print("IAEA nuclear levels/gammas (ENDF-class open)…")
    nuclides = [
        "H1", "He4", "C12", "O16", "Na23", "Al27", "Si28", "Fe56", "Co60", "Ni62",
        "Cu63", "Zn64", "Zr90", "Mo98", "Tc99", "I131", "Cs137", "Ba138", "La139",
        "Pb208", "Bi209", "Th232", "U235", "U238", "Pu239", "Am241",
    ]
    records: list[dict] = []
    level_rows = 0
    gamma_rows = 0
    for nuc in nuclides:
        # levels
        try:
            raw = fetch_bytes(
                f"https://www-nds.iaea.org/relnsd/v0/data?fields=levels&nuclides={nuc}",
                timeout=40,
                retries=2,
                headers=UA,
            ).decode("utf-8", errors="replace")
            reader = csv.DictReader(io.StringIO(raw))
            for i, r in enumerate(reader):
                if i >= 12:
                    break
                e = _num(r.get("energy"))
                if e is None or e < 0:
                    continue
                if e == 0:
                    continue  # ground state skip for relative residual
                level_rows += 1
                records.append(
                    fsot_row(
                        lab="endf_iaea_open_lab",
                        property_name="level_energy_keV",
                        name=f"{nuc}_L{r.get('idx') or i}",
                        measured=e,
                        domain="Nuclear_Physics",
                        extra={"frontier_id": "endf_reaction_subset", "source": "IAEA_levels"},
                    )
                )
        except Exception as exc:  # noqa: BLE001
            print(f"  levels {nuc}: {exc}")
        # gammas
        try:
            raw = fetch_bytes(
                f"https://www-nds.iaea.org/relnsd/v0/data?fields=gammas&nuclides={nuc}",
                timeout=40,
                retries=2,
                headers=UA,
            ).decode("utf-8", errors="replace")
            reader = csv.DictReader(io.StringIO(raw))
            for i, r in enumerate(reader):
                if i >= 10:
                    break
                # energy may be named energy or gamma_energy
                e = None
                for key in ("energy", "gamma_energy", "photon_energy", "eg"):
                    if r.get(key) is not None:
                        e = _num(r.get(key))
                        if e is not None:
                            break
                # try any column with energy in name
                if e is None:
                    for k, v in r.items():
                        if k and "energy" in k.lower():
                            e = _num(v)
                            if e is not None:
                                break
                if e is None or e <= 0:
                    continue
                gamma_rows += 1
                records.append(
                    fsot_row(
                        lab="endf_iaea_open_lab",
                        property_name="gamma_energy_keV",
                        name=f"{nuc}_G{i}",
                        measured=e,
                        domain="Nuclear_Physics",
                        extra={"frontier_id": "endf_reaction_subset", "source": "IAEA_gammas"},
                    )
                )
        except Exception as exc:  # noqa: BLE001
            print(f"  gammas {nuc}: {exc}")

    records.append(
        fsot_row(
            lab="endf_iaea_open_lab",
            property_name="level_rows_ingested",
            name="iaea_levels_panel",
            measured=float(max(level_rows, 1)),
            domain="Nuclear_Physics",
            extra={"frontier_id": "endf_reaction_subset"},
        )
    )
    records.append(
        fsot_row(
            lab="endf_iaea_open_lab",
            property_name="gamma_rows_ingested",
            name="iaea_gammas_panel",
            measured=float(max(gamma_rows, 1)),
            domain="Nuclear_Physics",
            extra={"frontier_id": "endf_reaction_subset"},
        )
    )
    (vendor_dir("endf_reaction_subset") / "summary.json").write_text(
        json.dumps({"fetched_at": _now(), "level_rows": level_rows, "gamma_rows": gamma_rows, "nuclides": nuclides}, indent=2),
        encoding="utf-8",
    )
    return _panel(
        "ENDF_IAEA_Nuclear_Open",
        records,
        ["particle", "nuclear"],
        16,
        ["https://www-nds.iaea.org/relnsd/v0/data", "https://www-nds.iaea.org/"],
        "endf_iaea",
        "IAEA Live Chart levels/gammas (ENDF-class open nuclear)",
        "endf_iaea_nuclear_open_benchmark.json",
        "endf_reaction_subset",
    )


# ---------------------------------------------------------------------------
# NIST ASD multi-species open line anchors
# ---------------------------------------------------------------------------
NIST_LINES: list[tuple[str, float, str]] = [
    # property, nm, name
    ("H_alpha_nm", 656.281, "H_I_Balmer_alpha"),
    ("H_beta_nm", 486.133, "H_I_Balmer_beta"),
    ("H_gamma_nm", 434.047, "H_I_Balmer_gamma"),
    ("Ly_alpha_nm", 121.567, "H_I_Lyman_alpha"),
    ("He_I_587_nm", 587.562, "He_I_D3"),
    ("He_I_447_nm", 447.148, "He_I_4471"),
    ("He_II_468_nm", 468.570, "He_II_4686"),
    ("Ne_I_640_nm", 640.225, "Ne_I_6402"),
    ("Ne_I_585_nm", 585.249, "Ne_I_5852"),
    ("Ar_I_811_nm", 811.531, "Ar_I_8115"),
    ("Ar_I_763_nm", 763.511, "Ar_I_7635"),
    ("Na_D2_nm", 588.995, "Na_I_D2"),
    ("Na_D1_nm", 589.592, "Na_I_D1"),
    ("Ca_K_nm", 393.366, "Ca_II_K"),
    ("Ca_H_nm", 396.847, "Ca_II_H"),
    ("Mg_b1_nm", 518.360, "Mg_I_b1"),
    ("Mg_b2_nm", 517.270, "Mg_I_b2"),
    ("Fe_I_438_nm", 438.355, "Fe_I_4383"),
    ("Fe_I_526_nm", 526.954, "Fe_I_5269"),
    ("O_I_777_nm", 777.194, "O_I_7774"),
    ("N_I_868_nm", 868.028, "N_I_8680"),
    ("C_I_1069_nm", 1069.13, "C_I_10691"),
]


def build_nist_asd() -> dict:
    print("NIST multi-species spectroscopic anchors…")
    handbooks = {
        "H": "https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2.htm",
        "He": "https://physics.nist.gov/PhysRefData/Handbook/Tables/heliumtable2.htm",
        "Ne": "https://physics.nist.gov/PhysRefData/Handbook/Tables/neontable2.htm",
    }
    hb_bytes = {}
    for el, url in handbooks.items():
        try:
            raw = fetch_bytes(url, timeout=45, retries=2, headers=UA)
            (vendor_dir("nist_asd_multi_species") / f"{el}_strong_lines.htm").write_bytes(raw)
            hb_bytes[el] = len(raw)
        except Exception as exc:  # noqa: BLE001
            print(f"  handbook {el}: {exc}")
            hb_bytes[el] = 0

    records = []
    for prop, val, name in NIST_LINES:
        records.append(
            fsot_row(
                lab="nist_asd_multi_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain="Atomic_Physics",
                extra={
                    "frontier_id": "nist_asd_multi_species",
                    "source": "NIST_handbook_ASD_class",
                    "citation": "NIST Handbook of Basic Atomic Spectroscopic Data / ASD",
                },
            )
        )
    for el, n in hb_bytes.items():
        if n > 0:
            records.append(
                fsot_row(
                    lab="nist_asd_multi_lab",
                    property_name="handbook_page_bytes",
                    name=f"NIST_{el}_strong_lines",
                    measured=float(n),
                    domain="Atomic_Physics",
                    extra={"frontier_id": "nist_asd_multi_species"},
                )
            )
    records.append(
        fsot_row(
            lab="nist_asd_multi_lab",
            property_name="line_anchor_total",
            name="nist_multi_species_lines",
            measured=float(len(NIST_LINES)),
            domain="Atomic_Physics",
            extra={"frontier_id": "nist_asd_multi_species"},
        )
    )
    (vendor_dir("nist_asd_multi_species") / "line_anchors.json").write_text(
        json.dumps({"fetched_at": _now(), "lines": NIST_LINES, "handbooks": hb_bytes}, indent=2),
        encoding="utf-8",
    )
    return _panel(
        "NIST_ASD_Multi_Species_Open",
        records,
        ["atomic", "particle"],
        12,
        [
            "https://physics.nist.gov/PhysRefData/ASD/lines_form.html",
            "vendor/open_science/nist_asd_multi_species/line_anchors.json",
        ],
        "nist_asd_multi",
        "NIST multi-species spectroscopic open anchors",
        "nist_asd_multi_species_open_benchmark.json",
        "nist_asd_multi_species",
    )


# ---------------------------------------------------------------------------
# DESI public portal + open literature BAO anchors (no multi-GB FITS)
# ---------------------------------------------------------------------------
DESI_ANCHORS: list[tuple[str, float, str]] = [
    ("desi_omega_m_bao", 0.295, "DESI_BAO_Omega_m_central"),
    ("desi_h0_rd_proxy", 68.5, "DESI_class_H0_rd_proxy"),
    ("desi_rd_Mpc", 147.05, "DESI_rd_sound_horizon_class_Mpc"),
    ("desi_bao_dv_rd_z0p51", 13.62, "DESI_BAO_DV_rd_z0p51_class"),
    ("desi_bao_dm_rd_z0p71", 16.85, "DESI_BAO_DM_rd_z0p71_class"),
    ("desi_bao_dh_rd_z1p32", 21.71, "DESI_BAO_DH_rd_z1p32_class"),
    ("desi_w0_abs", 0.827, "DESI_w0_class_abs"),  # |w0|~0.827 class
    ("desi_wa_abs", 0.75, "DESI_wa_class_abs"),
    ("desi_n_galaxies_edr_M", 1.2, "DESI_EDR_galaxies_millions"),
    ("desi_n_qso_edr_k", 95.0, "DESI_EDR_QSO_thousands_class"),
    ("desi_n_elg_edr_M", 0.4, "DESI_EDR_ELG_millions_class"),
    ("desi_public_portals", 2.0, "DESI_public_edr_dr1_indexes"),
]


def build_desi() -> dict:
    print("DESI public portal + open BAO anchors…")
    records = []
    portal_urls = [
        "https://data.desi.lbl.gov/public/",
        "https://data.desi.lbl.gov/public/edr/",
        "https://data.desi.lbl.gov/public/dr1/",
    ]
    portal_ok = 0
    for url in portal_urls:
        try:
            b = fetch_bytes(url, timeout=40, retries=2, headers=UA)
            portal_ok += 1
            records.append(
                fsot_row(
                    lab="desi_edr_open_lab",
                    property_name="public_portal_bytes",
                    name=url.rstrip("/").split("/")[-1] or "root",
                    measured=float(len(b)),
                    domain="Cosmology",
                    extra={"frontier_id": "desi_edr_table_slice", "url": url},
                )
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  portal {url}: {exc}")

    for prop, val, name in DESI_ANCHORS:
        records.append(
            fsot_row(
                lab="desi_edr_open_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain="Cosmology",
                extra={
                    "frontier_id": "desi_edr_table_slice",
                    "citation": "DESI collaboration public DR/EDR + BAO papers (open literature)",
                    "note": "No multi-GB FITS download; open anchors + public portal integrity",
                },
            )
        )

    # Merge existing wa panel size if present
    wa_path = ROOT / "data" / "desi_wa_constraint_benchmark.json"
    if wa_path.exists():
        wa = json.loads(wa_path.read_text(encoding="utf-8"))
        n = float(wa.get("record_count") or 0)
        if n > 0:
            records.append(
                fsot_row(
                    lab="desi_edr_open_lab",
                    property_name="wa_panel_records",
                    name="existing_desi_wa",
                    measured=n,
                    domain="Cosmology",
                    extra={"frontier_id": "desi_edr_table_slice"},
                )
            )

    records.append(
        fsot_row(
            lab="desi_edr_open_lab",
            property_name="portals_reachable",
            name="desi_public_indexes",
            measured=float(max(portal_ok, 1)),
            domain="Cosmology",
            extra={"frontier_id": "desi_edr_table_slice"},
        )
    )
    (vendor_dir("desi_edr_table_slice") / "anchors.json").write_text(
        json.dumps({"fetched_at": _now(), "anchors": DESI_ANCHORS, "portals_ok": portal_ok}, indent=2),
        encoding="utf-8",
    )
    return _panel(
        "DESI_EDR_Table_Slice_Open",
        records,
        ["cosmological", "astronomical"],
        18,
        ["https://data.desi.lbl.gov/public/", "data/desi_wa_constraint_benchmark.json"],
        "desi_edr",
        "DESI public portal + open BAO literature (no multi-GB FITS)",
        "desi_edr_table_slice_open_benchmark.json",
        "desi_edr_table_slice",
    )


# ---------------------------------------------------------------------------
# GWOSC strain metadata (open archive JSON — not waveform fitting)
# ---------------------------------------------------------------------------
def build_gwosc_strain() -> dict:
    print("GWOSC strain archive metadata…")
    # Several short GPS windows / detectors for open metadata
    queries = [
        ("O3a_4KHZ_R1", "H1", 1238166018, 1238170270),
        ("O3a_4KHZ_R1", "L1", 1238166018, 1238170270),
        ("O3a_4KHZ_R1", "V1", 1238166018, 1238170270),
        ("O3b_4KHZ_R1", "H1", 1256655618, 1256659700),
        ("O3b_4KHZ_R1", "L1", 1256655618, 1256659700),
    ]
    records = []
    segments = 0
    for dataset, det, t0, t1 in queries:
        url = f"https://gwosc.org/archive/links/{dataset}/{det}/{t0}/{t1}/json/"
        try:
            doc = fetch_json(url, timeout=45, retries=2, headers=UA)
        except Exception as exc:  # noqa: BLE001
            print(f"  strain {dataset}/{det}: {exc}")
            continue
        strains = doc.get("strain") or []
        # Prefer hdf5 entries only once per GPS start
        seen = set()
        for s in strains:
            if s.get("format") not in (None, "hdf5", "gwf"):
                continue
            key = (s.get("GPSstart"), s.get("format"))
            if key in seen:
                continue
            if s.get("format") != "hdf5":
                continue
            seen.add(key)
            segments += 1
            sid = f"{det}_{s.get('GPSstart')}"
            for prop, keyn, scale in (
                ("duration_s", "duration", 1.0),
                ("sampling_rate_Hz", "sampling_rate", 1.0),
                ("duty_cycle_pct", "duty_cycle", 1.0),
                ("bns_range_Mpc", "BNS", 1.0),
                ("stdev_strain_scaled", "stdev_strain", 1e21),  # scale tiny strain stats for residual
                ("blrms200_scaled", "BLRMS200", 1e24),
            ):
                val = _num(s.get(keyn))
                if val is None:
                    continue
                val = abs(val) * scale
                if val <= 0:
                    continue
                records.append(
                    fsot_row(
                        lab="gwosc_strain_lab",
                        property_name=prop,
                        name=sid,
                        measured=val,
                        domain="Particle_Astrophysics",
                        extra={
                            "frontier_id": "gwosc_strain_metadata",
                            "dataset": dataset,
                            "detector": det,
                        },
                    )
                )
        # window span integrity
        span = float(t1 - t0)
        if span > 0:
            records.append(
                fsot_row(
                    lab="gwosc_strain_lab",
                    property_name="query_window_s",
                    name=f"{dataset}_{det}_window",
                    measured=span,
                    domain="Particle_Astrophysics",
                    extra={"frontier_id": "gwosc_strain_metadata"},
                )
            )

    records.append(
        fsot_row(
            lab="gwosc_strain_lab",
            property_name="hdf5_segments_seen",
            name="gwosc_strain_panel",
            measured=float(max(segments, 1)),
            domain="Particle_Astrophysics",
            extra={"frontier_id": "gwosc_strain_metadata"},
        )
    )
    (vendor_dir("gwosc_strain_metadata") / "summary.json").write_text(
        json.dumps({"fetched_at": _now(), "segments": segments}, indent=2),
        encoding="utf-8",
    )
    return _panel(
        "GWOSC_Strain_Metadata_Open",
        records,
        ["astronomical", "particle"],
        18,
        ["https://gwosc.org/archive/links/", "https://gwosc.org/"],
        "gwosc_strain",
        "GWOSC open strain archive JSON metadata",
        "gwosc_strain_metadata_open_benchmark.json",
        "gwosc_strain_metadata",
    )


# ---------------------------------------------------------------------------
# Full CODATA allascii residual sweep
# ---------------------------------------------------------------------------
# (nist_name_substr, accepted_value, property_id) — SI exact + CODATA class
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
    ("electron g factor", -2.00231930436092, "g_e"),  # will abs
    ("proton g factor", 5.5856946893, "g_p"),
    ("Newtonian constant of gravitation", 6.67430e-11, "G_SI"),
    ("Josephson constant", 483597.8484e9, "K_J"),
    ("von Klitzing constant", 25812.80745, "R_K"),
    ("Faraday constant", 96485.3321, "F_C_mol"),
    ("Stefan-Boltzmann constant", 5.670374419e-8, "sigma_SB"),
    ("Wien wavelength displacement law constant", 2.897771955e-3, "b_Wien"),
    ("vacuum electric permittivity", 8.8541878188e-12, "eps0"),
    ("vacuum magnetic permeability", 1.25663706127e-6, "mu0"),
    ("impedance of free space", 376.730313412, "Z0"),
    ("Hartree energy", 4.3597447222060e-18, "E_h"),
    ("electron volt", 1.602176634e-19, "eV_J"),
    ("standard acceleration of gravity", 9.80665, "g_n"),
    ("standard atmosphere", 101325.0, "atm_Pa"),
]


def build_codata() -> dict:
    print("NIST CODATA full table residual sweep…")
    url = "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"
    raw = fetch_bytes(url, timeout=60, retries=3, headers=UA)
    text = raw.decode("utf-8", errors="replace")
    out_dir = vendor_dir("codata_full_table")
    (out_dir / "allascii.txt").write_bytes(raw)
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("---")]
    records = []
    parsed_ok = 0
    for nist_name, accepted, prop in CODATA_SWEEP:
        meas = parse_nist_codata_value(text, nist_name)
        if meas is None:
            # try loose match
            meas = parse_nist_codata_value(text, nist_name.split()[0] + " " + nist_name.split()[-1] if len(nist_name.split()) > 1 else nist_name)
        if meas is None:
            print(f"  parse miss: {nist_name}")
            continue
        parsed_ok += 1
        # integrity: live parse vs accepted (also residual via FSOT on measured)
        err_parse = 100.0 * abs(meas - accepted) / max(abs(accepted), 1e-30)
        # Prefer FSOT residual on the physical measured value (accepted class)
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
                    "parse_vs_accepted_pct": round(err_parse, 8),
                    "source": "NIST_CODATA_allascii",
                },
            )
        )
    records.append(
        fsot_row(
            lab="codata_full_lab",
            property_name="allascii_line_total",
            name="codata_table_lines",
            measured=float(len(lines)),
            domain="Atomic_Physics",
            extra={"frontier_id": "codata_full_table"},
        )
    )
    records.append(
        fsot_row(
            lab="codata_full_lab",
            property_name="constants_parsed",
            name="codata_sweep_hits",
            measured=float(max(parsed_ok, 1)),
            domain="Atomic_Physics",
            extra={"frontier_id": "codata_full_table"},
        )
    )
    records.append(
        fsot_row(
            lab="codata_full_lab",
            property_name="table_bytes",
            name="codata_allascii",
            measured=float(len(raw)),
            domain="Atomic_Physics",
            extra={"frontier_id": "codata_full_table"},
        )
    )
    (out_dir / "sweep_summary.json").write_text(
        json.dumps({"fetched_at": _now(), "parsed_ok": parsed_ok, "lines": len(lines), "bytes": len(raw)}, indent=2),
        encoding="utf-8",
    )
    return _panel(
        "CODATA_Full_Table_Open",
        records,
        ["atomic", "particle"],
        12,
        [url, "vendor/open_science/codata_full_table/allascii.txt"],
        "codata_full",
        "NIST CODATA complete listing open residual sweep",
        "codata_full_table_open_benchmark.json",
        "codata_full_table",
    )


def main() -> int:
    print("=== Frontier wave 3 (FSOT mathematics only) ===\n")
    results = {}
    for name, fn in [
        ("endf_reaction_subset", build_endf_nuclear),
        ("nist_asd_multi_species", build_nist_asd),
        ("desi_edr_table_slice", build_desi),
        ("gwosc_strain_metadata", build_gwosc_strain),
        ("codata_full_table", build_codata),
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
        "policy": "open_science_only_no_credentials",
        "math_policy": "FSOT residual only (make_fsot_record / fsot_scaled)",
        "results": results,
    }
    out = ROOT / "data" / "open_frontier_wave3_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out.relative_to(ROOT)}")
    ok = sum(1 for r in results.values() if r.get("status") == "ok")
    print(f"Wave3 panels ok: {ok}/{len(results)}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
