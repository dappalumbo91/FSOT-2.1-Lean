#!/usr/bin/env python3
"""Open substitutes for credential-gated Materials Project + FRED paths.

Policy: auth=none only.
  - Materials Project key → JARVIS-DFT OPTIMADE + COD OPTIMADE
  - FRED API key → World Bank Open Data (GDP, unemployment, CPI)

Writes vendor caches under vendor/open_science/ and residual benchmarks:
  - data/jarvis_dft_open_panel_benchmark.json
  - data/cod_optimade_structures_benchmark.json
  - data/world_bank_macro_open_benchmark.json

Residual law: make_fsot_record / fsot_scaled only (no free-fit parameters).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from live_api_fetch_lib import fetch_json  # noqa: E402
from open_science_sources_lib import vendor_dir  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402

UA = {
    "User-Agent": "FSOT-2.1-Lean/open-science (+https://github.com/dappalumbo91/FSOT-2.1-Lean)",
    "Accept": "application/json",
}

# Sentinel used by JARVIS for missing properties
_JARVIS_MISSING = -99999

JARVIS_URL = (
    "https://jarvis.nist.gov/optimade/jarvisdft/v1/structures"
    "?filter=nelements<=3&page_limit=40"
)
COD_URL = (
    "https://www.crystallography.net/cod/optimade/v1/structures?page_limit=40"
)

# World Bank: several countries × macro indicators (FRED-class surface)
WB_COUNTRIES = ("USA", "DEU", "JPN", "GBR", "FRA", "CAN", "AUS", "BRA", "IND", "CHN")
WB_INDICATORS = {
    "GDP_current_USD": "NY.GDP.MKTP.CD",
    "unemployment_pct": "SL.UEM.TOTL.ZS",
    "cpi_index": "FP.CPI.TOTL",
    "population_total": "SP.POP.TOTL",
}


def _save_live(source_id: str, url: str, payload: Any, description: str) -> Path:
    doc = {
        "source_id": source_id,
        "kind": "json",
        "payload": payload,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "auth": "none",
        "family": "chemistry_materials"
        if "jarvis" in source_id or "cod" in source_id
        else "social_econ_linguistics",
        "description": description,
    }
    path = vendor_dir(source_id) / "live.json"
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _valid_num(v: Any) -> float | None:
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if x == _JARVIS_MISSING or abs(x) > 1e12 and x == int(x) and x < 0:
        return None
    # JARVIS uses -99999; also reject absurd sentinels
    if x <= -90000:
        return None
    return x


def ingest_jarvis() -> dict[str, Any]:
    payload = fetch_json(JARVIS_URL, timeout=90, retries=3, headers=UA)
    path = _save_live(
        "jarvis_optimade_dft",
        JARVIS_URL,
        payload,
        "JARVIS-DFT OPTIMADE structures (Materials Project open substitute)",
    )
    materials: list[dict[str, Any]] = []
    for item in payload.get("data") or []:
        attrs = item.get("attributes") or {}
        jid = str(item.get("id") or attrs.get("_jarvis_jid") or "")
        formula = (
            attrs.get("_jarvis_formula")
            or attrs.get("chemical_formula_reduced")
            or attrs.get("chemical_formula_descriptive")
            or ""
        )
        row: dict[str, Any] = {
            "id": jid,
            "formula": formula,
            "nelements": attrs.get("nelements"),
            "elements": attrs.get("elements"),
        }
        prop_map = {
            "band_gap_eV": attrs.get("_jarvis_optb88vdw_bandgap"),
            "mbj_bandgap_eV": attrs.get("_jarvis_mbj_bandgap"),
            "formation_energy_eV_per_atom": attrs.get("_jarvis_formation_energy_peratom"),
            "total_energy_eV": attrs.get("_jarvis_optb88vdw_total_energy"),
            "exfoliation_energy": attrs.get("_jarvis_exfoliation_energy"),
            "bulk_modulus_GPa": attrs.get("_jarvis_bulk_modulus_kv"),
        }
        for k, raw in prop_map.items():
            val = _valid_num(raw)
            if val is not None:
                row[k] = val
        if any(k in row for k in ("band_gap_eV", "formation_energy_eV_per_atom", "total_energy_eV")):
            materials.append(row)
    cache = {
        "source": "JARVIS-DFT OPTIMADE (NIST)",
        "url": JARVIS_URL,
        "auth": "none",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "materials": materials,
        "count": len(materials),
        "live_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "replaces": "materials_project_api_key",
    }
    out = ROOT / "vendor" / "open_science" / "jarvis_optimade_dft" / "materials_cache.json"
    out.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    print(f"JARVIS: {len(materials)} materials → {out.relative_to(ROOT)}")
    return cache


def ingest_cod() -> dict[str, Any]:
    payload = fetch_json(COD_URL, timeout=90, retries=3, headers=UA)
    path = _save_live(
        "cod_optimade_structures",
        COD_URL,
        payload,
        "COD OPTIMADE crystal structures (open materials structures)",
    )
    structures: list[dict[str, Any]] = []
    for item in payload.get("data") or []:
        attrs = item.get("attributes") or {}
        sid = str(item.get("id") or attrs.get("_cod_file") or "")
        formula = (
            attrs.get("chemical_formula_reduced")
            or attrs.get("_cod_calcformula")
            or attrs.get("chemical_formula_descriptive")
            or ""
        )
        row: dict[str, Any] = {
            "id": sid,
            "formula": formula,
            "nelements": attrs.get("nelements"),
            "elements": attrs.get("elements"),
        }
        for key, attr in (
            ("cell_a_A", "_cod_a"),
            ("cell_b_A", "_cod_b"),
            ("cell_c_A", "_cod_c"),
            ("cell_alpha_deg", "_cod_alpha"),
            ("cell_beta_deg", "_cod_beta"),
            ("cell_gamma_deg", "_cod_gamma"),
            ("Z", "_cod_Z"),
            ("R_factor", "_cod_Rall"),
        ):
            val = _valid_num(attrs.get(attr))
            if val is not None:
                row[key] = val
        # nelements as integer structural complexity proxy
        ne = attrs.get("nelements")
        if ne is not None:
            try:
                row["nelements"] = int(ne)
            except (TypeError, ValueError):
                pass
        if formula or row.get("cell_a_A") is not None:
            structures.append(row)
    cache = {
        "source": "Crystallography Open Database OPTIMADE",
        "url": COD_URL,
        "auth": "none",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "structures": structures,
        "count": len(structures),
        "live_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "replaces": "materials_project_structures_key_path",
    }
    out = ROOT / "vendor" / "open_science" / "cod_optimade_structures" / "structures_cache.json"
    out.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    print(f"COD: {len(structures)} structures → {out.relative_to(ROOT)}")
    return cache


def ingest_world_bank_macro() -> dict[str, Any]:
    series: list[dict[str, Any]] = []
    for prop, code in WB_INDICATORS.items():
        for country in WB_COUNTRIES:
            url = (
                f"https://api.worldbank.org/v2/country/{country}/indicator/{code}"
                f"?format=json&per_page=15"
            )
            try:
                payload = fetch_json(url, timeout=60, retries=2, headers=UA)
            except Exception as exc:  # noqa: BLE001
                print(f"  WB fail {country}/{code}: {exc}")
                continue
            meta = payload[0] if isinstance(payload, list) and payload else {}
            rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
            for r in rows or []:
                if not isinstance(r, dict) or r.get("value") is None:
                    continue
                series.append(
                    {
                        "property": prop,
                        "indicator_code": code,
                        "country": country,
                        "country_name": (r.get("country") or {}).get("value") or country,
                        "year": str(r.get("date")),
                        "value": float(r["value"]),
                    }
                )
            # cache one representative live for USA streams
            if country == "USA":
                _save_live(
                    f"worldbank_{prop.lower()}",
                    url,
                    payload,
                    f"World Bank {prop} {country}",
                )
            _ = meta
    cache = {
        "source": "World Bank Open Data API v2",
        "auth": "none",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "series": series,
        "count": len(series),
        "countries": list(WB_COUNTRIES),
        "indicators": WB_INDICATORS,
        "replaces": "fred_api_key",
    }
    out = ROOT / "vendor" / "open_science" / "worldbank_macro" / "macro_cache.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    print(f"World Bank macro: {len(series)} observations → {out.relative_to(ROOT)}")
    return cache


def build_jarvis_panel(cache: dict[str, Any]) -> dict:
    mod, authority = _load_fsot()
    _ = mod
    records: list[dict] = []
    errs: list[float] = []
    for mat in cache.get("materials") or []:
        mid = str(mat.get("id") or "unknown")
        formula = mat.get("formula")
        for prop in (
            "band_gap_eV",
            "mbj_bandgap_eV",
            "formation_energy_eV_per_atom",
            "total_energy_eV",
            "exfoliation_energy",
            "bulk_modulus_GPa",
        ):
            if prop not in mat:
                continue
            val = float(mat[prop])
            # Skip exact-zero band gaps as metallic (still valid measured=0 edge)
            # fsot_scaled handles measured=0 via err_pct
            rec = make_fsot_record(
                lab="jarvis_dft_open_lab",
                property_name=prop,
                name=mid,
                measured=val,
                domain="Materials_Science",
                formula=formula if isinstance(formula, str) else None,
                extra={
                    "ingest_source": "jarvis_optimade_dft",
                    "auth": "none",
                    "replaces": "materials_project_api_key",
                },
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))
    doc = _bench_v11(
        domain="JARVIS_DFT_Open_Panel",
        material_records=records,
        maps_to_lean=["material", "particle", "energy"],
        d_eff=16,
        authority_path=authority,
        source=[
            JARVIS_URL,
            "vendor/open_science/jarvis_optimade_dft/materials_cache.json",
        ],
        channel_stats=[("fsot_prediction", "jarvis_dft", errs or [0.0])],
        sota_baselines={
            "jarvis_dft": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "JARVIS-DFT / OPTIMADE open materials class",
            }
        },
    )
    doc["policy"] = "open_science_only_no_credentials"
    doc["replaces"] = "materials_project_live_api_key"
    out = ROOT / "data" / "jarvis_dft_open_panel_benchmark.json"
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(
        f"Wrote {out.name} n={doc['record_count']} "
        f"pooled={doc.get('pooled_median_error_pct')}%"
    )
    return doc


def build_cod_panel(cache: dict[str, Any]) -> dict:
    mod, authority = _load_fsot()
    _ = mod
    records: list[dict] = []
    errs: list[float] = []
    for st in cache.get("structures") or []:
        sid = str(st.get("id") or "unknown")
        formula = st.get("formula")
        for prop in (
            "cell_a_A",
            "cell_b_A",
            "cell_c_A",
            "cell_alpha_deg",
            "cell_beta_deg",
            "cell_gamma_deg",
            "Z",
            "R_factor",
            "nelements",
        ):
            if prop not in st or st[prop] is None:
                continue
            val = float(st[prop])
            if val == 0.0 and prop == "R_factor":
                continue
            rec = make_fsot_record(
                lab="cod_optimade_lab",
                property_name=prop,
                name=sid,
                measured=val,
                domain="Materials_Science",
                formula=formula if isinstance(formula, str) else None,
                extra={
                    "ingest_source": "cod_optimade_structures",
                    "auth": "none",
                    "replaces": "materials_project_structures",
                },
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))
    doc = _bench_v11(
        domain="COD_OPTIMADE_Structures",
        material_records=records,
        maps_to_lean=["material", "chemistry"],
        d_eff=14,
        authority_path=authority,
        source=[
            COD_URL,
            "vendor/open_science/cod_optimade_structures/structures_cache.json",
        ],
        channel_stats=[("fsot_prediction", "cod_structures", errs or [0.0])],
        sota_baselines={
            "cod_structures": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "COD experimental crystal structures",
            }
        },
    )
    doc["policy"] = "open_science_only_no_credentials"
    doc["replaces"] = "materials_project_structures_key_path"
    out = ROOT / "data" / "cod_optimade_structures_benchmark.json"
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(
        f"Wrote {out.name} n={doc['record_count']} "
        f"pooled={doc.get('pooled_median_error_pct')}%"
    )
    return doc


def build_world_bank_macro_panel(cache: dict[str, Any]) -> dict:
    mod, authority = _load_fsot()
    _ = mod
    records: list[dict] = []
    errs: list[float] = []
    # Prefer recent non-null years; cap per property×country to keep panel focused
    by_key: dict[tuple[str, str], list[dict]] = {}
    for row in cache.get("series") or []:
        key = (str(row["property"]), str(row["country"]))
        by_key.setdefault(key, []).append(row)
    for (prop, country), rows in sorted(by_key.items()):
        rows_sorted = sorted(rows, key=lambda r: str(r.get("year") or ""), reverse=True)
        for row in rows_sorted[:6]:
            val = float(row["value"])
            name = f"{country}_{row['year']}"
            rec = make_fsot_record(
                lab="world_bank_macro_open_lab",
                property_name=prop,
                name=name,
                measured=val,
                domain="Economics",
                extra={
                    "ingest_source": "world_bank_open_data",
                    "auth": "none",
                    "indicator_code": row.get("indicator_code"),
                    "replaces": "fred_api_key",
                },
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))
    doc = _bench_v11(
        domain="World_Bank_Macro_Open",
        material_records=records,
        maps_to_lean=["consciousness", "economic"],
        d_eff=18,
        authority_path=authority,
        source=[
            "https://api.worldbank.org/v2/",
            "vendor/open_science/worldbank_macro/macro_cache.json",
        ],
        channel_stats=[("fsot_prediction", "world_bank_macro", errs or [0.0])],
        sota_baselines={
            "world_bank_macro": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "World Bank Open Data macro indicators (FRED-class open substitute)",
            }
        },
    )
    doc["policy"] = "open_science_only_no_credentials"
    doc["replaces"] = "fred_api_key"
    out = ROOT / "data" / "world_bank_macro_open_benchmark.json"
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(
        f"Wrote {out.name} n={doc['record_count']} "
        f"pooled={doc.get('pooled_median_error_pct')}%"
    )
    return doc


def main() -> int:
    print("=== Open credential replacements (auth=none) ===")
    jarvis = ingest_jarvis()
    cod = ingest_cod()
    wb = ingest_world_bank_macro()
    jdoc = build_jarvis_panel(jarvis)
    cdoc = build_cod_panel(cod)
    wdoc = build_world_bank_macro_panel(wb)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "open_science_only_no_credentials",
        "replacements": {
            "materials_project_api_key": {
                "open_sources": ["jarvis_optimade_dft", "cod_optimade_structures"],
                "benchmarks": [
                    "data/jarvis_dft_open_panel_benchmark.json",
                    "data/cod_optimade_structures_benchmark.json",
                ],
                "jarvis_records": jdoc.get("record_count"),
                "jarvis_pooled_pct": jdoc.get("pooled_median_error_pct"),
                "cod_records": cdoc.get("record_count"),
                "cod_pooled_pct": cdoc.get("pooled_median_error_pct"),
            },
            "fred_api_key": {
                "open_sources": ["worldbank_gdp", "worldbank_unemployment", "worldbank_cpi"],
                "benchmarks": ["data/world_bank_macro_open_benchmark.json"],
                "records": wdoc.get("record_count"),
                "pooled_pct": wdoc.get("pooled_median_error_pct"),
            },
        },
    }
    sp = ROOT / "data" / "open_credential_replacements_report.json"
    sp.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {sp.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
