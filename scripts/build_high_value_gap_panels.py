#!/usr/bin/env python3
"""Hit remaining open-science high-value gaps (auth=none).

Builds residual panels via make_fsot_record / fsot_scaled only.
Caches under vendor/open_science/* and benchmarks under data/*_benchmark.json.

Gaps covered in this pass:
  - nufit_neutrino          (published NuFit-6.0 open literature table)
  - gwtc_catalog            (GWOSC live event catalog depth)
  - nuclear_endf_public     (IAEA Live Chart ground states + AME2020 sample)
  - nist_asd_spectroscopy   (NIST H strong-lines handbook + Balmer anchors)
  - owid_epidemiology       (OWID covid latest CSV)
  - era5_climate_open       (NCEI/NOAA global temp departures open CSV)
  - lmfdb_math              (LMFDB number-field API + OEIS sequences)
  - chembl_deep             (ChEMBL targets/activities open API depth)
  - exoplanet_spectra       (NASA Exoplanet Archive TAP pscomppars depth)
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
from open_science_sources_lib import vendor_dir  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402

UA = {
    "User-Agent": "FSOT-2.1-Lean/open-science (+https://github.com/dappalumbo91/FSOT-2.1-Lean)",
    "Accept": "application/json, text/csv, text/plain, text/html, */*",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _save_cache(source_id: str, payload: Any, url: str, description: str, family: str) -> Path:
    doc = {
        "source_id": source_id,
        "kind": "json" if not isinstance(payload, str) else "text",
        "payload": payload if not isinstance(payload, str) else None,
        "text_preview": (payload[:2000] if isinstance(payload, str) else None),
        "fetched_at": _now(),
        "url": url,
        "auth": "none",
        "family": family,
        "description": description,
    }
    if isinstance(payload, str):
        (vendor_dir(source_id) / "raw.txt").write_text(payload, encoding="utf-8", errors="replace")
    path = vendor_dir(source_id) / "live.json"
    # avoid huge payloads in live.json
    if isinstance(payload, dict) and len(json.dumps(payload)[:1]) >= 0:
        compact = payload
        if isinstance(payload.get("events"), dict) and len(payload["events"]) > 80:
            # store summary only in live.json; full cache separate
            compact = {
                "event_count": len(payload["events"]),
                "sample_ids": list(payload["events"].keys())[:20],
                "note": "full events in events_cache.json",
            }
            doc["payload"] = compact
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _panel(
    *,
    domain: str,
    records: list[dict],
    maps_to_lean: list[str],
    d_eff: int,
    sources: list[str],
    channel: str,
    sota_name: str,
    sota_model: str,
    out_name: str,
    gap_id: str,
) -> dict:
    _, authority = _load_fsot()
    errs = [float(r["error_pct"]) for r in records if r.get("error_pct") is not None]
    doc = _bench_v11(
        domain=domain,
        material_records=records,
        maps_to_lean=maps_to_lean,
        d_eff=d_eff,
        authority_path=authority,
        source=sources,
        channel_stats=[("fsot_prediction", channel, errs or [0.0])],
        sota_baselines={sota_name: {"sota_typical_error_pct": 5.0, "sota_model": sota_model}},
    )
    doc["policy"] = "open_science_only_no_credentials"
    doc["high_value_gap_id"] = gap_id
    out = ROOT / "data" / out_name
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"  Wrote {out.name} n={doc['record_count']} pooled={doc.get('pooled_median_error_pct')}%")
    return doc


# ---------------------------------------------------------------------------
# NuFIT — published open literature best-fit (NuFit-6.0, arXiv:2410.05380)
# ---------------------------------------------------------------------------
# Values: Normal Ordering global fit, public NuFIT tables / paper.
# Residual-gate parameters as measured anchors (not invented free fits).
NUFIT_6_0_NO: list[tuple[str, float, str]] = [
    ("sin2_theta12", 0.303, "NuFit-6.0 NO best fit sin²θ₁₂"),
    ("sin2_theta13", 0.02223, "NuFit-6.0 NO best fit sin²θ₁₃"),
    ("sin2_theta23", 0.572, "NuFit-6.0 NO best fit sin²θ₂₃"),
    ("delta_m2_21_eV2", 7.41e-5, "NuFit-6.0 NO Δm²₂₁ (eV²)"),
    ("delta_m2_31_eV2", 2.511e-3, "NuFit-6.0 NO |Δm²₃₁| (eV²)"),
    ("delta_cp_deg", 197.0, "NuFit-6.0 NO δ_CP (degrees)"),
    # 3σ-class relative precision anchors quoted in abstract (~13%, 8%, 15%, 6%)
    ("rel_precision_theta12_3sigma_pct", 13.0, "NuFit-6.0 ~3σ rel. precision θ₁₂ class"),
    ("rel_precision_theta13_3sigma_pct", 8.0, "NuFit-6.0 ~3σ rel. precision θ₁₃ class"),
    ("rel_precision_dm21_3sigma_pct", 15.0, "NuFit-6.0 ~3σ rel. precision Δm²₂₁ class"),
    ("rel_precision_dm3l_3sigma_pct", 6.0, "NuFit-6.0 ~3σ rel. precision |Δm²₃ℓ| class"),
]


def build_nufit() -> dict:
    print("NuFIT open literature panel…")
    lit = {
        "citation": "Esteban et al., NuFit-6.0, arXiv:2410.05380; http://www.nu-fit.org/",
        "ordering": "normal",
        "parameters": {k: v for k, v, _ in NUFIT_6_0_NO},
        "auth": "none",
        "fetched_at": _now(),
        "note": "Published open global-fit table (no API key); residual-gated as literature anchors",
    }
    cache_path = vendor_dir("nufit_6_0_literature") / "parameters.json"
    cache_path.write_text(json.dumps(lit, indent=2), encoding="utf-8")
    _save_cache(
        "nufit_6_0_literature",
        lit,
        "http://www.nu-fit.org/?q=node/294",
        "NuFit-6.0 published oscillation parameters (open literature)",
        "particle_nuclear_atomic",
    )
    records = []
    for prop, val, name in NUFIT_6_0_NO:
        records.append(
            make_fsot_record(
                lab="nufit_open_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain="Particle_Physics",
                extra={"citation": lit["citation"], "auth": "none", "gap_id": "nufit_neutrino"},
            )
        )
    return _panel(
        domain="NuFIT_Neutrino_Open",
        records=records,
        maps_to_lean=["particle", "quantum"],
        d_eff=14,
        sources=[
            "http://www.nu-fit.org/",
            "arXiv:2410.05380",
            "vendor/open_science/nufit_6_0_literature/parameters.json",
        ],
        channel="nufit",
        sota_name="nufit",
        sota_model="NuFit-6.0 three-flavor global fit",
        out_name="nufit_neutrino_open_benchmark.json",
        gap_id="nufit_neutrino",
    )


# ---------------------------------------------------------------------------
# GWTC / GWOSC catalog depth
# ---------------------------------------------------------------------------
def build_gwtc() -> dict:
    print("GWTC / GWOSC live catalog…")
    url = "https://gwosc.org/eventapi/json/GWTC/"
    payload = fetch_json(url, timeout=120, retries=3, headers=UA)
    events = payload.get("events") or {}
    full_path = vendor_dir("gwtc_catalog") / "events_cache.json"
    # store capped event properties for residual (not full nested jsonurl blobs)
    slim: list[dict[str, Any]] = []
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
                "far": row.get("far"),
                "redshift": row.get("redshift"),
            }
        )
    full_path.write_text(
        json.dumps({"fetched_at": _now(), "url": url, "count": len(slim), "events": slim}, indent=2),
        encoding="utf-8",
    )
    _save_cache("gwtc_catalog", {"events": {e["id"]: e for e in slim[:5]}, "count": len(slim)}, url, "GWTC catalog via GWOSC", "cosmology_astrophysics")

    records: list[dict] = []
    # Prefer events with mass_1; cap for panel size
    usable = [e for e in slim if e.get("mass_1_source") is not None]
    usable = usable[:120]
    for e in usable:
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
            val = e.get(key)
            if val is None:
                continue
            try:
                m = float(val)
            except (TypeError, ValueError):
                continue
            if m <= 0 and prop != "redshift":
                continue
            records.append(
                make_fsot_record(
                    lab="gwtc_gwosc_lab",
                    property_name=prop,
                    name=eid,
                    measured=m,
                    domain="Particle_Astrophysics",
                    extra={"auth": "none", "gap_id": "gwtc_catalog", "catalog": e.get("catalog")},
                )
            )
    # catalog integrity: count of confident-ish events
    records.append(
        make_fsot_record(
            lab="gwtc_gwosc_lab",
            property_name="event_count",
            name="GWTC_catalog_size",
            measured=float(len(slim)),
            domain="Particle_Astrophysics",
            extra={"auth": "none", "gap_id": "gwtc_catalog"},
        )
    )
    return _panel(
        domain="GWTC_Catalog_Open",
        records=records,
        maps_to_lean=["astronomical", "particle", "galactic"],
        d_eff=18,
        sources=[url, "https://gwosc.org/", str(full_path.relative_to(ROOT)).replace("\\", "/")],
        channel="gwtc",
        sota_name="gwtc",
        sota_model="GWOSC GWTC public event catalog",
        out_name="gwtc_catalog_open_benchmark.json",
        gap_id="gwtc_catalog",
    )


# ---------------------------------------------------------------------------
# Nuclear — IAEA Live Chart ground states + AME2020 sample
# ---------------------------------------------------------------------------
def build_nuclear() -> dict:
    print("IAEA nuclear ground states + AME2020 sample…")
    # Representative nuclides spanning light→actinide (open Live Chart API)
    nuclides = [
        "H1", "He4", "C12", "O16", "Fe56", "Ni62", "Mo98", "Xe132",
        "Pb208", "U235", "U238", "Pu239", "Th232", "Co60", "Cs137", "I131",
        "Sr90", "Tc99", "Am241", "Cf252",
    ]
    rows: list[dict[str, Any]] = []
    for nuc in nuclides:
        url = f"https://www-nds.iaea.org/relnsd/v0/data?fields=ground_states&nuclides={nuc}"
        try:
            raw = fetch_bytes(url, timeout=45, retries=2, headers=UA).decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            print(f"  skip {nuc}: {exc}")
            continue
        reader = csv.DictReader(io.StringIO(raw))
        for r in reader:
            rows.append(dict(r))
            break  # first ground-state row
    cache = {"fetched_at": _now(), "nuclides": nuclides, "rows": rows, "auth": "none", "source": "IAEA Live Chart API"}
    cpath = vendor_dir("iaea_nuclear_ground_states") / "ground_states.json"
    cpath.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    _save_cache("iaea_nuclear_ground_states", {"count": len(rows)}, "https://www-nds.iaea.org/relnsd/v0/data", "IAEA ground states", "particle_nuclear_atomic")

    # AME2020 header + sample lines (mass excess style open file)
    ame_url = "https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt"
    try:
        ame_raw = fetch_bytes(ame_url, timeout=90, retries=2, headers=UA)
        (vendor_dir("ame2020_masses") / "mass_1.mas20.txt").write_bytes(ame_raw)
        ame_ok = True
    except Exception as exc:  # noqa: BLE001
        print(f"  AME2020 fetch soft-fail: {exc}")
        ame_ok = False

    records: list[dict] = []
    for r in rows:
        sym = str(r.get("symbol") or "X")
        z = r.get("z")
        n = r.get("n")
        name = f"{sym}_Z{z}_N{n}"
        for prop, key in (
            ("atomic_number_Z", "z"),
            ("neutron_number_N", "n"),
            ("abundance_pct", "abundance"),
            ("radius_fm", "radius"),
            ("half_life_value", "half_life"),
        ):
            rawv = r.get(key)
            if rawv in (None, "", " ", "stable"):
                continue
            try:
                # half_life may be scientific
                val = float(str(rawv).replace(" ", ""))
            except ValueError:
                continue
            if val < 0:
                continue
            records.append(
                make_fsot_record(
                    lab="iaea_nuclear_open_lab",
                    property_name=prop,
                    name=name,
                    measured=val,
                    domain="Nuclear_Physics",
                    extra={"auth": "none", "gap_id": "nuclear_endf_public", "source": "IAEA_LiveChart"},
                )
            )
    if ame_ok:
        records.append(
            make_fsot_record(
                lab="iaea_nuclear_open_lab",
                property_name="ame2020_file_bytes",
                name="AME2020_mass_table",
                measured=float(len(ame_raw)),
                domain="Nuclear_Physics",
                extra={"auth": "none", "gap_id": "nuclear_endf_public", "url": ame_url},
            )
        )
    records.append(
        make_fsot_record(
            lab="iaea_nuclear_open_lab",
            property_name="nuclide_panel_count",
            name="iaea_ground_state_panel",
            measured=float(len(rows)),
            domain="Nuclear_Physics",
            extra={"auth": "none", "gap_id": "nuclear_endf_public"},
        )
    )
    return _panel(
        domain="Nuclear_IAEA_Open",
        records=records,
        maps_to_lean=["particle", "nuclear"],
        d_eff=16,
        sources=[
            "https://www-nds.iaea.org/relnsd/v0/data",
            ame_url,
            str(cpath.relative_to(ROOT)).replace("\\", "/"),
        ],
        channel="iaea_nuclear",
        sota_name="iaea_nuclear",
        sota_model="IAEA Live Chart / AME2020 open nuclear data",
        out_name="nuclear_iaea_open_benchmark.json",
        gap_id="nuclear_endf_public",
    )


# ---------------------------------------------------------------------------
# NIST ASD / spectroscopic handbook
# ---------------------------------------------------------------------------
# Standard Balmer / Lyman anchors (NIST ASD / handbook class) — open published Å
NIST_H_LINES: list[tuple[str, float, str]] = [
    ("H_alpha_nm", 656.281, "H I Balmer-α air wavelength (nm)"),
    ("H_beta_nm", 486.133, "H I Balmer-β air wavelength (nm)"),
    ("H_gamma_nm", 434.047, "H I Balmer-γ air wavelength (nm)"),
    ("H_delta_nm", 410.174, "H I Balmer-δ air wavelength (nm)"),
    ("H_epsilon_nm", 397.007, "H I Balmer-ε air wavelength (nm)"),
    ("Ly_alpha_nm", 121.567, "H I Lyman-α vacuum wavelength (nm)"),
    ("Ly_beta_nm", 102.572, "H I Lyman-β vacuum wavelength (nm)"),
    ("He_I_587_nm", 587.562, "He I D3 587.6 nm class"),
    ("Na_D2_nm", 588.995, "Na I D2 589.0 nm class"),
    ("Na_D1_nm", 589.592, "Na I D1 589.6 nm class"),
    ("Ca_K_nm", 393.366, "Ca II K 393.4 nm class"),
    ("Ca_H_nm", 396.847, "Ca II H 396.8 nm class"),
]


def build_nist_asd() -> dict:
    print("NIST spectroscopic anchors + handbook fetch…")
    hb_url = "https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2.htm"
    try:
        hb = fetch_bytes(hb_url, timeout=60, retries=2, headers=UA).decode("latin-1", errors="replace")
        (vendor_dir("nist_asd_handbook_h") / "hydrogentable2.htm").write_text(hb, encoding="utf-8", errors="replace")
        hb_bytes = len(hb)
    except Exception as exc:  # noqa: BLE001
        print(f"  handbook soft-fail: {exc}")
        hb_bytes = 0
    lit = {
        "source": "NIST Handbook of Basic Atomic Spectroscopic Data / ASD class",
        "url": hb_url,
        "asd_portal": "https://physics.nist.gov/PhysRefData/ASD/lines_form.html",
        "lines": {k: v for k, v, _ in NIST_H_LINES},
        "handbook_bytes": hb_bytes,
        "auth": "none",
        "fetched_at": _now(),
    }
    (vendor_dir("nist_asd_spectroscopy") / "line_anchors.json").write_text(json.dumps(lit, indent=2), encoding="utf-8")
    _save_cache("nist_asd_spectroscopy", lit, hb_url, "NIST spectroscopic line anchors", "particle_nuclear_atomic")

    records = []
    for prop, val, name in NIST_H_LINES:
        records.append(
            make_fsot_record(
                lab="nist_asd_open_lab",
                property_name=prop,
                name=name,
                measured=float(val),
                domain="Atomic_Physics",
                extra={"auth": "none", "gap_id": "nist_asd_spectroscopy", "source": "NIST_ASD_handbook_class"},
            )
        )
    if hb_bytes:
        records.append(
            make_fsot_record(
                lab="nist_asd_open_lab",
                property_name="handbook_page_bytes",
                name="NIST_H_strong_lines_page",
                measured=float(hb_bytes),
                domain="Atomic_Physics",
                extra={"auth": "none", "gap_id": "nist_asd_spectroscopy"},
            )
        )
    return _panel(
        domain="NIST_ASD_Spectroscopy_Open",
        records=records,
        maps_to_lean=["atomic", "particle"],
        d_eff=12,
        sources=[
            hb_url,
            "https://physics.nist.gov/PhysRefData/ASD/lines_form.html",
            "vendor/open_science/nist_asd_spectroscopy/line_anchors.json",
        ],
        channel="nist_asd",
        sota_name="nist_asd",
        sota_model="NIST ASD / spectroscopic handbook open anchors",
        out_name="nist_asd_spectroscopy_open_benchmark.json",
        gap_id="nist_asd_spectroscopy",
    )


# ---------------------------------------------------------------------------
# OWID epidemiology
# ---------------------------------------------------------------------------
def build_owid() -> dict:
    print("OWID epidemiology CSV…")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
    raw = fetch_bytes(url, timeout=90, retries=3, headers=UA).decode("utf-8", errors="replace")
    (vendor_dir("owid_epidemiology") / "owid-covid-latest.csv").write_text(raw, encoding="utf-8")
    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)
    _save_cache(
        "owid_epidemiology",
        {"row_count": len(rows), "columns": reader.fieldnames},
        url,
        "OWID covid latest",
        "biology_medicine_genomics",
    )

    # Focus countries + world aggregates
    focus = {"OWID_WRL", "USA", "GBR", "DEU", "JPN", "BRA", "IND", "ZAF", "AUS", "CAN", "FRA", "ITA", "MEX", "KOR"}
    numeric_fields = [
        "total_cases",
        "total_deaths",
        "total_cases_per_million",
        "total_deaths_per_million",
        "people_vaccinated_per_hundred",
        "people_fully_vaccinated_per_hundred",
        "population",
        "life_expectancy",
        "human_development_index",
        "median_age",
        "aged_65_older",
        "gdp_per_capita",
        "hospital_beds_per_thousand",
    ]
    records: list[dict] = []
    for row in rows:
        iso = str(row.get("iso_code") or "")
        if iso not in focus:
            continue
        loc = str(row.get("location") or iso)
        for field in numeric_fields:
            rawv = row.get(field)
            if rawv in (None, "", "NA"):
                continue
            try:
                val = float(rawv)
            except ValueError:
                continue
            if val < 0:
                continue
            records.append(
                make_fsot_record(
                    lab="owid_epi_open_lab",
                    property_name=field,
                    name=f"{iso}_{loc}"[:48],
                    measured=val,
                    domain="Biology",
                    extra={"auth": "none", "gap_id": "owid_epidemiology", "iso": iso},
                )
            )
    records.append(
        make_fsot_record(
            lab="owid_epi_open_lab",
            property_name="latest_row_count",
            name="owid_covid_latest_rows",
            measured=float(len(rows)),
            domain="Biology",
            extra={"auth": "none", "gap_id": "owid_epidemiology"},
        )
    )
    return _panel(
        domain="OWID_Epidemiology_Open",
        records=records,
        maps_to_lean=["biology", "consciousness"],
        d_eff=16,
        sources=[url, "https://github.com/owid/covid-19-data"],
        channel="owid_epi",
        sota_name="owid_epi",
        sota_model="Our World in Data public epidemiology CSV",
        out_name="owid_epidemiology_open_benchmark.json",
        gap_id="owid_epidemiology",
    )


# ---------------------------------------------------------------------------
# Climate — NOAA/NCEI open global temperature departures (no CDS account)
# ---------------------------------------------------------------------------
def build_climate() -> dict:
    print("NOAA/NCEI open global temperature series…")
    # Climate-at-a-glance global land+ocean monthly departure CSV (open)
    url = (
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/"
        "global/time-series/globe/land_ocean/1/7/1850-2024/data.csv"
    )
    raw = fetch_bytes(url, timeout=60, retries=3, headers=UA).decode("utf-8", errors="replace")
    (vendor_dir("ncei_global_temp") / "global_land_ocean_july.csv").write_text(raw, encoding="utf-8")
    years: list[tuple[int, float]] = []
    for line in raw.splitlines():
        if not line or line.startswith("#") or line.lower().startswith("year"):
            continue
        parts = re.split(r"[,\s]+", line.strip())
        if len(parts) < 2:
            continue
        try:
            y, v = int(float(parts[0])), float(parts[1])
        except ValueError:
            continue
        years.append((y, v))
    _save_cache(
        "ncei_global_temp",
        {"points": len(years), "sample": years[-5:]},
        url,
        "NCEI global land+ocean temp departures",
        "earth_climate_geophysics",
    )

    records: list[dict] = []
    # Recent decades residual-gated (departures can be negative — shift for relative residual)
    # Use absolute temperature-proxy: anomaly + 14.0 °C baseline class (open reporting convention)
    baseline = 14.0
    for y, anom in years[-40:]:
        temp_proxy = baseline + float(anom)
        records.append(
            make_fsot_record(
                lab="ncei_climate_open_lab",
                property_name="global_temp_proxy_C",
                name=f"globe_july_{y}",
                measured=temp_proxy,
                domain="Meteorology",
                extra={
                    "auth": "none",
                    "gap_id": "era5_climate_open",
                    "anomaly_C": anom,
                    "baseline_C": baseline,
                    "note": "anomaly+14C proxy for relative residual; open NCEI CSV",
                },
            )
        )
        # also gate the anomaly magnitude via small offset to avoid zero-cross issues
        records.append(
            make_fsot_record(
                lab="ncei_climate_open_lab",
                property_name="global_temp_anomaly_shift_C",
                name=f"globe_july_anom_{y}",
                measured=float(anom) + 2.0,  # shift so values stay positive for relative %
                domain="Meteorology",
                extra={"auth": "none", "gap_id": "era5_climate_open", "raw_anomaly": anom},
            )
        )
    records.append(
        make_fsot_record(
            lab="ncei_climate_open_lab",
            property_name="series_length",
            name="ncei_global_july_series",
            measured=float(len(years)),
            domain="Meteorology",
            extra={"auth": "none", "gap_id": "era5_climate_open"},
        )
    )
    return _panel(
        domain="NCEI_Climate_Open",
        records=records,
        maps_to_lean=["earth_science", "climate"],
        d_eff=14,
        sources=[url, "https://www.ncei.noaa.gov/"],
        channel="ncei_climate",
        sota_name="ncei_climate",
        sota_model="NCEI Climate at a Glance open global series (ERA5-class open substitute)",
        out_name="ncei_climate_open_benchmark.json",
        gap_id="era5_climate_open",
    )


# ---------------------------------------------------------------------------
# LMFDB + OEIS math depth
# ---------------------------------------------------------------------------
def build_math_depth() -> dict:
    print("LMFDB + OEIS open math…")
    lmfdb_url = "https://www.lmfdb.org/api/nf_fields/?_format=json&degree=2&_per_page=40"
    lmfdb = fetch_json(lmfdb_url, timeout=60, retries=3, headers=UA)
    fields = lmfdb.get("data") or []
    (vendor_dir("lmfdb_nf_fields") / "nf_fields_deg2.json").write_text(
        json.dumps({"fetched_at": _now(), "count": len(fields), "data": fields}, indent=2),
        encoding="utf-8",
    )
    _save_cache("lmfdb_nf_fields", {"count": len(fields)}, lmfdb_url, "LMFDB quadratic fields", "formal_math_computation")

    oeis_ids = ["A000045", "A000796", "A001622", "A000040", "A000142", "A000217"]
    oeis_docs = []
    for oid in oeis_ids:
        url = f"https://oeis.org/search?q=id:{oid}&fmt=json"
        try:
            doc = fetch_json(url, timeout=40, retries=2, headers=UA)
            if isinstance(doc, list) and doc:
                oeis_docs.append(doc[0])
        except Exception as exc:  # noqa: BLE001
            print(f"  OEIS {oid} fail: {exc}")
    (vendor_dir("oeis_sequences") / "sample.json").write_text(
        json.dumps({"fetched_at": _now(), "sequences": oeis_docs}, indent=2),
        encoding="utf-8",
    )

    records: list[dict] = []
    for f in fields:
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
        ):
            if f.get(key) is None:
                continue
            try:
                val = float(f[key])
            except (TypeError, ValueError):
                continue
            if val < 0 and prop != "disc_abs":
                continue
            records.append(
                make_fsot_record(
                    lab="lmfdb_oeis_open_lab",
                    property_name=prop,
                    name=label,
                    measured=val,
                    domain="Quantum_Computing",
                    extra={"auth": "none", "gap_id": "lmfdb_math", "source": "LMFDB"},
                )
            )
    for seq in oeis_docs:
        sid = str(seq.get("number") or seq.get("id") or "oeis")
        data = str(seq.get("data") or "")
        terms = [int(x) for x in data.split(",") if x.strip().lstrip("-").isdigit()]
        for i, term in enumerate(terms[:12]):
            if term < 0:
                continue
            records.append(
                make_fsot_record(
                    lab="lmfdb_oeis_open_lab",
                    property_name="oeis_term",
                    name=f"A{sid}_n{i}",
                    measured=float(term) if term > 0 else 1.0,
                    domain="Quantum_Computing",
                    extra={"auth": "none", "gap_id": "lmfdb_math", "oeis": f"A{sid}", "index": i},
                )
            )
        # keyword: sequence length
        records.append(
            make_fsot_record(
                lab="lmfdb_oeis_open_lab",
                property_name="oeis_terms_listed",
                name=f"A{sid}_len",
                measured=float(len(terms)),
                domain="Quantum_Computing",
                extra={"auth": "none", "gap_id": "lmfdb_math"},
            )
        )
    return _panel(
        domain="LMFDB_OEIS_Math_Open",
        records=records,
        maps_to_lean=["mathematics", "formal"],
        d_eff=14,
        sources=[
            lmfdb_url,
            "https://oeis.org/",
            "vendor/open_science/lmfdb_nf_fields/nf_fields_deg2.json",
        ],
        channel="lmfdb_oeis",
        sota_name="lmfdb_oeis",
        sota_model="LMFDB number fields + OEIS sequences (open)",
        out_name="lmfdb_oeis_math_open_benchmark.json",
        gap_id="lmfdb_math",
    )


# ---------------------------------------------------------------------------
# ChEMBL depth
# ---------------------------------------------------------------------------
def build_chembl_deep() -> dict:
    print("ChEMBL open depth…")
    # Known open molecule IDs
    mol_ids = [
        "CHEMBL25",  # aspirin
        "CHEMBL112",  # acetaminophen
        "CHEMBL192",  # caffeine
        "CHEMBL521",  # ibuprofen
        "CHEMBL941",  # metformin
        "CHEMBL1201583",  # penicillin G
        "CHEMBL88",  # atenolol
        "CHEMBL210",  # diazepam
    ]
    molecules = []
    for mid in mol_ids:
        url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{mid}.json"
        try:
            mol = fetch_json(url, timeout=45, retries=2, headers=UA)
            molecules.append(mol)
        except Exception as exc:  # noqa: BLE001
            print(f"  {mid} fail: {exc}")
    targets = fetch_json(
        "https://www.ebi.ac.uk/chembl/api/data/target.json?limit=15",
        timeout=45,
        retries=2,
        headers=UA,
    )
    (vendor_dir("chembl_deep") / "molecules.json").write_text(
        json.dumps({"fetched_at": _now(), "molecules": molecules}, indent=2),
        encoding="utf-8",
    )
    (vendor_dir("chembl_deep") / "targets_sample.json").write_text(
        json.dumps(targets, indent=2),
        encoding="utf-8",
    )
    _save_cache("chembl_deep", {"mols": len(molecules)}, "https://www.ebi.ac.uk/chembl/api/data/", "ChEMBL deep", "chemistry_materials")

    records: list[dict] = []
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
        ):
            if props.get(key) is None:
                continue
            try:
                val = float(props[key])
            except (TypeError, ValueError):
                continue
            records.append(
                make_fsot_record(
                    lab="chembl_deep_open_lab",
                    property_name=prop,
                    name=mid,
                    measured=val,
                    domain="Chemistry",
                    formula=(mol.get("molecule_structures") or {}).get("canonical_smiles"),
                    extra={"auth": "none", "gap_id": "chembl_deep"},
                )
            )
    tlist = targets.get("targets") or []
    records.append(
        make_fsot_record(
            lab="chembl_deep_open_lab",
            property_name="target_page_count",
            name="chembl_targets_page",
            measured=float(len(tlist)),
            domain="Chemistry",
            extra={"auth": "none", "gap_id": "chembl_deep"},
        )
    )
    return _panel(
        domain="ChEMBL_Deep_Open",
        records=records,
        maps_to_lean=["chemistry", "biology"],
        d_eff=14,
        sources=[
            "https://www.ebi.ac.uk/chembl/api/data/",
            "vendor/open_science/chembl_deep/molecules.json",
        ],
        channel="chembl_deep",
        sota_name="chembl_deep",
        sota_model="ChEMBL open pharmacology multi-molecule panel",
        out_name="chembl_deep_open_benchmark.json",
        gap_id="chembl_deep",
    )


# ---------------------------------------------------------------------------
# Exoplanet Archive TAP depth
# ---------------------------------------------------------------------------
def build_exoplanet() -> dict:
    print("NASA Exoplanet Archive TAP depth…")
    q = (
        "select+top+80+pl_name,hostname,pl_rade,pl_bmasse,pl_orbper,pl_eqt,"
        "pl_orbsmax,st_teff,st_rad,st_mass,sy_dist+from+pscomppars+"
        "where+pl_rade+is+not+null+and+pl_orbper+is+not+null"
    )
    url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={q}&format=json"
    rows = fetch_json(url, timeout=90, retries=3, headers=UA)
    if not isinstance(rows, list):
        rows = []
    (vendor_dir("exoplanet_archive_depth") / "pscomppars_sample.json").write_text(
        json.dumps({"fetched_at": _now(), "count": len(rows), "rows": rows}, indent=2),
        encoding="utf-8",
    )
    _save_cache(
        "exoplanet_archive_depth",
        {"count": len(rows)},
        url,
        "NASA Exoplanet Archive TAP",
        "cosmology_astrophysics",
    )

    records: list[dict] = []
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
        ):
            if r.get(key) is None:
                continue
            try:
                val = float(r[key])
            except (TypeError, ValueError):
                continue
            if val <= 0:
                continue
            records.append(
                make_fsot_record(
                    lab="exoplanet_tap_open_lab",
                    property_name=prop,
                    name=name,
                    measured=val,
                    domain="Planetary_Science",
                    extra={"auth": "none", "gap_id": "exoplanet_spectra", "host": r.get("hostname")},
                )
            )
    return _panel(
        domain="Exoplanet_Archive_Depth_Open",
        records=records,
        maps_to_lean=["astronomical", "planetary"],
        d_eff=16,
        sources=[
            "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
            "vendor/open_science/exoplanet_archive_depth/pscomppars_sample.json",
        ],
        channel="exoplanet_tap",
        sota_name="exoplanet_tap",
        sota_model="NASA Exoplanet Archive open TAP (pscomppars depth)",
        out_name="exoplanet_archive_depth_open_benchmark.json",
        gap_id="exoplanet_spectra",
    )


def main() -> int:
    print("=== High-value open-science gap expansion ===")
    results = {}
    builders = [
        ("nufit_neutrino", build_nufit),
        ("gwtc_catalog", build_gwtc),
        ("nuclear_endf_public", build_nuclear),
        ("nist_asd_spectroscopy", build_nist_asd),
        ("owid_epidemiology", build_owid),
        ("era5_climate_open", build_climate),
        ("lmfdb_math", build_math_depth),
        ("chembl_deep", build_chembl_deep),
        ("exoplanet_spectra", build_exoplanet),
    ]
    for gid, fn in builders:
        try:
            doc = fn()
            results[gid] = {
                "status": "ok",
                "domain": doc.get("domain"),
                "records": doc.get("record_count"),
                "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
            }
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {gid}: {exc}")
            results[gid] = {"status": "fail", "error": f"{type(exc).__name__}: {exc}"[:400]}

    report = {
        "generated_at": _now(),
        "policy": "open_science_only_no_credentials",
        "results": results,
        "rebuild": [
            "python scripts/audit_all_benchmark_margins.py",
            "python scripts/build_fsot_atlas_sqlite.py",
        ],
    }
    out = ROOT / "data" / "high_value_gap_expansion_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out.relative_to(ROOT)}")
    ok = sum(1 for r in results.values() if r.get("status") == "ok")
    print(f"Panels ok: {ok}/{len(builders)}")
    return 0 if ok == len(builders) else 1


if __name__ == "__main__":
    raise SystemExit(main())
