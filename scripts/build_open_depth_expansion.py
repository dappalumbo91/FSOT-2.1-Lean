#!/usr/bin/env python3
"""Increase depth on open-science residual panels (auth=none).

Larger samples than the first high-value gap pass. Same residual law:
make_fsot_record / fsot_scaled only. Rebuilds deepened benchmarks and a depth report.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from live_api_fetch_lib import fetch_bytes, fetch_json  # noqa: E402
from open_science_sources_lib import vendor_dir  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402

UA = {
    "User-Agent": "FSOT-2.1-Lean/open-science (+https://github.com/dappalumbo91/FSOT-2.1-Lean)",
    "Accept": "application/json, text/csv, text/plain, */*",
}
_JARVIS_MISSING = -99999


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _valid(v: Any) -> float | None:
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if x <= -90000:
        return None
    return x


def _panel(domain: str, records: list[dict], maps: list[str], d_eff: int, sources: list[str], channel: str, model: str, out: str, gap_id: str) -> dict:
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
    doc["depth_pass"] = "open_depth_expansion"
    doc["high_value_gap_id"] = gap_id
    path = ROOT / "data" / out
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"  {out}: n={doc['record_count']} pooled={doc.get('pooled_median_error_pct')}%")
    return doc


def deepen_jarvis() -> dict:
    print("Depth JARVIS…")
    url = "https://jarvis.nist.gov/optimade/jarvisdft/v1/structures?filter=nelements<=4&page_limit=120"
    payload = fetch_json(url, timeout=120, retries=3, headers=UA)
    materials = []
    for item in payload.get("data") or []:
        a = item.get("attributes") or {}
        row = {
            "id": str(item.get("id") or ""),
            "formula": a.get("_jarvis_formula") or a.get("chemical_formula_reduced") or "",
        }
        for prop, key in (
            ("band_gap_eV", "_jarvis_optb88vdw_bandgap"),
            ("mbj_bandgap_eV", "_jarvis_mbj_bandgap"),
            ("formation_energy_eV_per_atom", "_jarvis_formation_energy_peratom"),
            ("total_energy_eV", "_jarvis_optb88vdw_total_energy"),
            ("exfoliation_energy", "_jarvis_exfoliation_energy"),
            ("bulk_modulus_GPa", "_jarvis_bulk_modulus_kv"),
            ("shear_modulus_GPa", "_jarvis_shear_modulus_gv"),
        ):
            val = _valid(a.get(key))
            if val is not None:
                row[prop] = val
        if len(row) > 2:
            materials.append(row)
    (vendor_dir("jarvis_optimade_dft") / "materials_cache_depth.json").write_text(
        json.dumps({"fetched_at": _now(), "count": len(materials), "materials": materials, "url": url}, indent=2),
        encoding="utf-8",
    )
    records = []
    for m in materials:
        for prop in ("band_gap_eV", "mbj_bandgap_eV", "formation_energy_eV_per_atom", "total_energy_eV", "exfoliation_energy", "bulk_modulus_GPa", "shear_modulus_GPa"):
            if prop not in m:
                continue
            records.append(
                make_fsot_record(
                    lab="jarvis_dft_open_lab",
                    property_name=prop,
                    name=str(m["id"]),
                    measured=float(m[prop]),
                    domain="Materials_Science",
                    formula=m.get("formula") or None,
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    return _panel("JARVIS_DFT_Open_Panel", records, ["material", "particle", "energy"], 16, [url], "jarvis_dft", "JARVIS-DFT OPTIMADE depth", "jarvis_dft_open_panel_benchmark.json", "jarvis_dft_open")


def deepen_cod() -> dict:
    print("Depth COD…")
    # COD rate-limits large page_limit (403); polite UA + moderate limit.
    url = "https://www.crystallography.net/cod/optimade/v1/structures?page_limit=80"
    ua = {
        **UA,
        "User-Agent": "FSOT-2.1-Lean/open-science (mailto:dappalumbo91@users.noreply.github.com)",
    }
    payload = fetch_json(url, timeout=120, retries=3, headers=ua)
    structures = []
    for item in payload.get("data") or []:
        a = item.get("attributes") or {}
        row = {
            "id": str(item.get("id") or a.get("_cod_file") or ""),
            "formula": a.get("chemical_formula_reduced") or a.get("_cod_calcformula") or "",
        }
        for prop, key in (
            ("cell_a_A", "_cod_a"),
            ("cell_b_A", "_cod_b"),
            ("cell_c_A", "_cod_c"),
            ("cell_alpha_deg", "_cod_alpha"),
            ("cell_beta_deg", "_cod_beta"),
            ("cell_gamma_deg", "_cod_gamma"),
            ("Z", "_cod_Z"),
            ("R_factor", "_cod_Rall"),
            ("nelements", "nelements"),
        ):
            val = _valid(a.get(key))
            if val is not None:
                row[prop] = val
        structures.append(row)
    (vendor_dir("cod_optimade_structures") / "structures_cache_depth.json").write_text(
        json.dumps({"fetched_at": _now(), "count": len(structures), "structures": structures}, indent=2),
        encoding="utf-8",
    )
    records = []
    for st in structures:
        for prop in ("cell_a_A", "cell_b_A", "cell_c_A", "cell_alpha_deg", "cell_beta_deg", "cell_gamma_deg", "Z", "R_factor", "nelements"):
            if prop not in st:
                continue
            records.append(
                make_fsot_record(
                    lab="cod_optimade_lab",
                    property_name=prop,
                    name=str(st["id"]),
                    measured=float(st[prop]),
                    domain="Materials_Science",
                    formula=st.get("formula") or None,
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    return _panel("COD_OPTIMADE_Structures", records, ["material", "chemistry"], 14, [url], "cod_structures", "COD OPTIMADE depth", "cod_optimade_structures_benchmark.json", "condensed_matter_open_cod")


def deepen_gwtc() -> dict:
    print("Depth GWTC…")
    url = "https://gwosc.org/eventapi/json/GWTC/"
    payload = fetch_json(url, timeout=120, retries=3, headers=UA)
    events = payload.get("events") or {}
    slim = []
    for name, row in events.items():
        if not isinstance(row, dict):
            continue
        slim.append(
            {
                "id": name,
                "commonName": row.get("commonName"),
                "catalog": row.get("catalog.shortName") or row.get("catalog"),
                "mass_1_source": row.get("mass_1_source"),
                "mass_2_source": row.get("mass_2_source"),
                "chirp_mass_source": row.get("chirp_mass_source") or row.get("chirp_mass"),
                "final_mass_source": row.get("final_mass_source") or row.get("final_mass"),
                "luminosity_distance": row.get("luminosity_distance"),
                "network_snr": row.get("network_matched_filter_snr") or row.get("network_snr"),
                "redshift": row.get("redshift"),
                "far": row.get("far"),
            }
        )
    (vendor_dir("gwtc_catalog") / "events_cache_depth.json").write_text(
        json.dumps({"fetched_at": _now(), "count": len(slim), "events": slim}, indent=2),
        encoding="utf-8",
    )
    records = []
    for e in slim:
        if e.get("mass_1_source") is None:
            continue
        eid = str(e.get("commonName") or e.get("id"))
        for prop, key in (
            ("mass_1_msun", "mass_1_source"),
            ("mass_2_msun", "mass_2_source"),
            ("chirp_mass_msun", "chirp_mass_source"),
            ("final_mass_msun", "final_mass_source"),
            ("luminosity_distance_Mpc", "luminosity_distance"),
            ("network_snr", "network_snr"),
            ("redshift", "redshift"),
        ):
            val = _valid(e.get(key))
            if val is None or (val <= 0 and prop != "redshift"):
                continue
            records.append(
                make_fsot_record(
                    lab="gwtc_gwosc_lab",
                    property_name=prop,
                    name=eid,
                    measured=val,
                    domain="Particle_Astrophysics",
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    records.append(
        make_fsot_record(
            lab="gwtc_gwosc_lab",
            property_name="event_count",
            name="GWTC_catalog_size",
            measured=float(len(slim)),
            domain="Particle_Astrophysics",
            extra={"auth": "none", "depth_pass": True},
        )
    )
    return _panel("GWTC_Catalog_Open", records, ["astronomical", "particle"], 18, [url], "gwtc", "GWOSC full GWTC depth", "gwtc_catalog_open_benchmark.json", "gwtc_catalog")


def deepen_lmfdb_oeis() -> dict:
    print("Depth LMFDB+OEIS…")
    records = []
    for degree, limit in ((2, 80), (3, 60), (4, 40)):
        url = f"https://www.lmfdb.org/api/nf_fields/?_format=json&degree={degree}&_per_page={limit}"
        data = (fetch_json(url, timeout=90, retries=2, headers=UA).get("data") or [])
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
                val = _valid(f.get(key))
                if val is None or val < 0:
                    continue
                records.append(
                    make_fsot_record(
                        lab="lmfdb_oeis_open_lab",
                        property_name=prop,
                        name=f"deg{degree}_{label}",
                        measured=val,
                        domain="Quantum_Computing",
                        extra={"auth": "none", "depth_pass": True, "source": "LMFDB"},
                    )
                )
    oeis_ids = [
        "A000045", "A000796", "A001622", "A000040", "A000142", "A000217",
        "A000108", "A000041", "A000984", "A001006", "A000290", "A000578",
    ]
    oeis_docs = []
    for oid in oeis_ids:
        try:
            doc = fetch_json(f"https://oeis.org/search?q=id:{oid}&fmt=json", timeout=40, retries=2, headers=UA)
            if isinstance(doc, list) and doc:
                oeis_docs.append(doc[0])
        except Exception as exc:  # noqa: BLE001
            print(f"  OEIS {oid}: {exc}")
    for seq in oeis_docs:
        sid = str(seq.get("number") or seq.get("id") or "oeis")
        terms = [int(x) for x in str(seq.get("data") or "").split(",") if x.strip().lstrip("-").isdigit()]
        for i, term in enumerate(terms[:20]):
            if term <= 0:
                continue
            records.append(
                make_fsot_record(
                    lab="lmfdb_oeis_open_lab",
                    property_name="oeis_term",
                    name=f"A{sid}_n{i}",
                    measured=float(term),
                    domain="Quantum_Computing",
                    extra={"auth": "none", "depth_pass": True},
                )
            )
        records.append(
            make_fsot_record(
                lab="lmfdb_oeis_open_lab",
                property_name="oeis_terms_listed",
                name=f"A{sid}_len",
                measured=float(len(terms)),
                domain="Quantum_Computing",
                extra={"auth": "none", "depth_pass": True},
            )
        )
    (vendor_dir("lmfdb_nf_fields") / "depth_cache.json").write_text(
        json.dumps({"fetched_at": _now(), "records": len(records), "oeis": len(oeis_docs)}, indent=2),
        encoding="utf-8",
    )
    return _panel("LMFDB_OEIS_Math_Open", records, ["mathematics", "formal"], 14, ["https://www.lmfdb.org/", "https://oeis.org/"], "lmfdb_oeis", "LMFDB+OEIS depth", "lmfdb_oeis_math_open_benchmark.json", "lmfdb_math")


def deepen_chembl() -> dict:
    print("Depth ChEMBL…")
    mol_ids = [
        "CHEMBL25", "CHEMBL112", "CHEMBL192", "CHEMBL521", "CHEMBL941",
        "CHEMBL1201583", "CHEMBL88", "CHEMBL6", "CHEMBL50", "CHEMBL98",
        "CHEMBL101", "CHEMBL1200766", "CHEMBL1431", "CHEMBL1542", "CHEMBL1642",
        "CHEMBL178", "CHEMBL2103836", "CHEMBL27820", "CHEMBL4297185", "CHEMBL535",
    ]
    molecules = []
    for mid in mol_ids:
        try:
            molecules.append(fetch_json(f"https://www.ebi.ac.uk/chembl/api/data/molecule/{mid}.json", timeout=45, retries=2, headers=UA))
        except Exception as exc:  # noqa: BLE001
            print(f"  {mid}: {exc}")
    records = []
    for mol in molecules:
        mid = str(mol.get("molecule_chembl_id") or "mol")
        props = mol.get("molecule_properties") or {}
        for prop, key in (
            ("full_mwt", "full_mwt"),
            ("alogp", "alogp"),
            ("psa", "psa"),
            ("hba", "hba"),
            ("hbd", "hbd"),
            ("rtb", "rtb"),
            ("num_ro5_violations", "num_ro5_violations"),
            ("aromatic_rings", "aromatic_rings"),
            ("heavy_atoms", "heavy_atoms"),
            ("mw_freebase", "mw_freebase"),
            ("qed_weighted", "qed_weighted"),
        ):
            val = _valid(props.get(key))
            if val is None:
                continue
            records.append(
                make_fsot_record(
                    lab="chembl_deep_open_lab",
                    property_name=prop,
                    name=mid,
                    measured=val,
                    domain="Chemistry",
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    records.append(
        make_fsot_record(
            lab="chembl_deep_open_lab",
            property_name="molecule_panel_count",
            name="chembl_depth_mols",
            measured=float(len(molecules)),
            domain="Chemistry",
            extra={"auth": "none", "depth_pass": True},
        )
    )
    (vendor_dir("chembl_deep") / "molecules_depth.json").write_text(
        json.dumps({"fetched_at": _now(), "count": len(molecules), "ids": [m.get("molecule_chembl_id") for m in molecules]}, indent=2),
        encoding="utf-8",
    )
    return _panel("ChEMBL_Deep_Open", records, ["chemistry", "biology"], 14, ["https://www.ebi.ac.uk/chembl/api/data/"], "chembl_deep", "ChEMBL multi-molecule depth", "chembl_deep_open_benchmark.json", "chembl_deep")


def deepen_exoplanet() -> dict:
    print("Depth exoplanet TAP…")
    q = (
        "select+top+200+pl_name,hostname,pl_rade,pl_bmasse,pl_orbper,pl_eqt,"
        "pl_orbsmax,st_teff,st_rad,st_mass,sy_dist,pl_dens,pl_orbeccen+"
        "from+pscomppars+where+pl_rade+is+not+null+and+pl_orbper+is+not+null"
    )
    url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={q}&format=json"
    rows = fetch_json(url, timeout=120, retries=3, headers=UA)
    if not isinstance(rows, list):
        rows = []
    records = []
    for r in rows:
        name = str(r.get("pl_name") or "planet")[:40]
        for prop, key in (
            ("pl_rade", "pl_rade"),
            ("pl_bmasse", "pl_bmasse"),
            ("pl_orbper", "pl_orbper"),
            ("pl_eqt", "pl_eqt"),
            ("pl_orbsmax", "pl_orbsmax"),
            ("st_teff", "st_teff"),
            ("st_rad", "st_rad"),
            ("st_mass", "st_mass"),
            ("sy_dist", "sy_dist"),
            ("pl_dens", "pl_dens"),
        ):
            val = _valid(r.get(key))
            if val is None or val <= 0:
                continue
            records.append(
                make_fsot_record(
                    lab="exoplanet_tap_open_lab",
                    property_name=prop,
                    name=name,
                    measured=val,
                    domain="Planetary_Science",
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    return _panel("Exoplanet_Archive_Depth_Open", records, ["astronomical", "planetary"], 16, [url], "exoplanet_tap", "NASA Exoplanet TAP depth", "exoplanet_archive_depth_open_benchmark.json", "exoplanet_spectra")


def deepen_nuclear() -> dict:
    print("Depth nuclear IAEA…")
    nuclides = [
        "H1", "H2", "He3", "He4", "Li6", "Li7", "Be9", "B10", "B11", "C12", "C13", "C14",
        "N14", "N15", "O16", "O18", "F19", "Ne20", "Na23", "Mg24", "Al27", "Si28", "P31",
        "S32", "Cl35", "Ar40", "K39", "Ca40", "Ti48", "Cr52", "Mn55", "Fe56", "Fe57",
        "Co59", "Co60", "Ni58", "Ni62", "Cu63", "Zn64", "Ge74", "Se80", "Kr84", "Sr88",
        "Sr90", "Y89", "Zr90", "Mo98", "Tc99", "Ru102", "Pd106", "Ag107", "Cd114",
        "Sn120", "I127", "I131", "Xe132", "Cs133", "Cs137", "Ba138", "La139", "Ce140",
        "Nd146", "Sm152", "Eu153", "Gd158", "Dy164", "Er166", "Yb174", "Hf180", "W184",
        "Os192", "Pt195", "Au197", "Hg202", "Pb206", "Pb207", "Pb208", "Bi209", "Po210",
        "Rn222", "Ra226", "Th232", "U235", "U238", "Np237", "Pu239", "Pu240", "Am241",
        "Cm244", "Cf252",
    ]
    rows = []
    for nuc in nuclides:
        url = f"https://www-nds.iaea.org/relnsd/v0/data?fields=ground_states&nuclides={nuc}"
        try:
            raw = fetch_bytes(url, timeout=30, retries=1, headers=UA).decode("utf-8", errors="replace")
            reader = csv.DictReader(io.StringIO(raw))
            for r in reader:
                rows.append(dict(r))
                break
        except Exception:
            continue
    records = []
    for r in rows:
        sym = str(r.get("symbol") or "X")
        name = f"{sym}_Z{r.get('z')}_N{r.get('n')}"
        for prop, key in (
            ("atomic_number_Z", "z"),
            ("neutron_number_N", "n"),
            ("abundance_pct", "abundance"),
            ("radius_fm", "radius"),
            ("half_life_value", "half_life"),
        ):
            val = _valid(str(r.get(key) or "").replace(" ", "") if r.get(key) not in (None, "", "stable") else None)
            if val is None or val < 0:
                continue
            records.append(
                make_fsot_record(
                    lab="iaea_nuclear_open_lab",
                    property_name=prop,
                    name=name,
                    measured=val,
                    domain="Nuclear_Physics",
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    records.append(
        make_fsot_record(
            lab="iaea_nuclear_open_lab",
            property_name="nuclide_panel_count",
            name="iaea_depth_panel",
            measured=float(len(rows)),
            domain="Nuclear_Physics",
            extra={"auth": "none", "depth_pass": True},
        )
    )
    (vendor_dir("iaea_nuclear_ground_states") / "ground_states_depth.json").write_text(
        json.dumps({"fetched_at": _now(), "count": len(rows)}, indent=2),
        encoding="utf-8",
    )
    return _panel("Nuclear_IAEA_Open", records, ["particle", "nuclear"], 16, ["https://www-nds.iaea.org/relnsd/v0/data"], "iaea_nuclear", "IAEA Live Chart depth", "nuclear_iaea_open_benchmark.json", "nuclear_endf_public")


def deepen_owid() -> dict:
    print("Depth OWID…")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
    raw = fetch_bytes(url, timeout=90, retries=3, headers=UA).decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)
    # All countries with population > 5e6 plus OWID aggregates
    focus = set()
    for row in rows:
        iso = str(row.get("iso_code") or "")
        try:
            pop = float(row.get("population") or 0)
        except ValueError:
            pop = 0
        if iso.startswith("OWID_") or pop >= 5_000_000:
            focus.add(iso)
    fields = [
        "total_cases", "total_deaths", "total_cases_per_million", "total_deaths_per_million",
        "people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred", "population",
        "life_expectancy", "human_development_index", "median_age", "aged_65_older",
        "gdp_per_capita", "hospital_beds_per_thousand", "cardiovasc_death_rate",
        "diabetes_prevalence", "extreme_poverty",
    ]
    records = []
    for row in rows:
        iso = str(row.get("iso_code") or "")
        if iso not in focus:
            continue
        loc = str(row.get("location") or iso)
        for field in fields:
            val = _valid(row.get(field))
            if val is None or val < 0:
                continue
            records.append(
                make_fsot_record(
                    lab="owid_epi_open_lab",
                    property_name=field,
                    name=f"{iso}_{loc}"[:48],
                    measured=val,
                    domain="Biology",
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    records.append(
        make_fsot_record(
            lab="owid_epi_open_lab",
            property_name="latest_row_count",
            name="owid_covid_latest_rows",
            measured=float(len(rows)),
            domain="Biology",
            extra={"auth": "none", "depth_pass": True},
        )
    )
    return _panel("OWID_Epidemiology_Open", records, ["biology"], 16, [url], "owid_epi", "OWID epi depth", "owid_epidemiology_open_benchmark.json", "owid_epidemiology")


def deepen_world_bank() -> dict:
    print("Depth World Bank macro…")
    countries = (
        "USA", "DEU", "JPN", "GBR", "FRA", "CAN", "AUS", "BRA", "IND", "CHN",
        "MEX", "KOR", "ITA", "ESP", "NLD", "SWE", "CHE", "IDN", "TUR", "ZAF",
        "ARG", "SAU", "POL", "BEL", "NOR",
    )
    indicators = {
        "GDP_current_USD": "NY.GDP.MKTP.CD",
        "unemployment_pct": "SL.UEM.TOTL.ZS",
        "cpi_index": "FP.CPI.TOTL",
        "population_total": "SP.POP.TOTL",
        "gdp_per_capita": "NY.GDP.PCAP.CD",
    }
    series = []
    for prop, code in indicators.items():
        for country in countries:
            url = f"https://api.worldbank.org/v2/country/{country}/indicator/{code}?format=json&per_page=12"
            try:
                payload = fetch_json(url, timeout=40, retries=1, headers=UA)
            except Exception:
                continue
            rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
            for r in rows or []:
                if not isinstance(r, dict) or r.get("value") is None:
                    continue
                series.append(
                    {
                        "property": prop,
                        "country": country,
                        "year": str(r.get("date")),
                        "value": float(r["value"]),
                    }
                )
    by_key: dict[tuple[str, str], list] = {}
    for row in series:
        by_key.setdefault((row["property"], row["country"]), []).append(row)
    records = []
    for (prop, country), rows in sorted(by_key.items()):
        for row in sorted(rows, key=lambda r: r["year"], reverse=True)[:5]:
            records.append(
                make_fsot_record(
                    lab="world_bank_macro_open_lab",
                    property_name=prop,
                    name=f"{country}_{row['year']}",
                    measured=float(row["value"]),
                    domain="Economics",
                    extra={"auth": "none", "depth_pass": True},
                )
            )
    return _panel("World_Bank_Macro_Open", records, ["consciousness", "economic"], 18, ["https://api.worldbank.org/v2/"], "world_bank_macro", "World Bank macro depth", "world_bank_macro_open_benchmark.json", "world_bank_macro_open")


def main() -> int:
    print("=== Open depth expansion ===")
    results = {}
    for name, fn in [
        ("jarvis", deepen_jarvis),
        ("cod", deepen_cod),
        ("gwtc", deepen_gwtc),
        ("lmfdb_oeis", deepen_lmfdb_oeis),
        ("chembl", deepen_chembl),
        ("exoplanet", deepen_exoplanet),
        ("nuclear", deepen_nuclear),
        ("owid", deepen_owid),
        ("world_bank", deepen_world_bank),
    ]:
        try:
            doc = fn()
            results[name] = {
                "status": "ok",
                "domain": doc.get("domain"),
                "records": doc.get("record_count"),
                "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
            }
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {name}: {exc}")
            results[name] = {"status": "fail", "error": f"{type(exc).__name__}: {exc}"[:400]}
    report = {
        "generated_at": _now(),
        "policy": "open_science_only_no_credentials",
        "pass": "depth_expansion",
        "results": results,
    }
    out = ROOT / "data" / "open_depth_expansion_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")
    ok = sum(1 for r in results.values() if r.get("status") == "ok")
    print(f"Depth panels ok: {ok}/{len(results)}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
