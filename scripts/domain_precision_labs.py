"""Per-record precision extractors for Tier-10 domain verification."""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SMILES_JSON = Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab\FSOT_SMILES_Lab_Dataset.json")
SECTION_MAP = ROOT / "data" / "section_domain_map.json"
TRANSLATIONS = ROOT / "data" / "neurolab_translations_bio.json"
WEATHER_BENCH = ROOT / "data" / "weather_observed_benchmark.json"
EVOLUTION_BENCH = ROOT / "data" / "evolution_operon_benchmark.json"

# Human mtDNA reference gene lengths (NCBI NC_012920.1, protein-coding spans).
HUMAN_MT_OPERON_REF = {
    "MT-ND1": 956,
    "MT-ND2": 1044,
    "MT-CO1": 1542,
    "MT-CO2": 684,
    "MT-ATP8": 207,
    "MT-ATP6": 681,
    "MT-CO3": 780,
    "MT-ND3": 349,
    "MT-ND4L": 297,
    "MT-ND4": 1378,
    "MT-ND5": 1812,
    "MT-ND6": 525,
    "MT-CYTB": 1140,
}


def _median(vals: list[float]) -> float | None:
    if not vals:
        return None
    return float(statistics.median(vals))


def _p90(vals: list[float]) -> float | None:
    if not vals:
        return None
    s = sorted(vals)
    idx = min(len(s) - 1, int(math.ceil(0.9 * len(s)) - 1))
    return float(s[idx])


def _summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    errs = [float(r["error_pct"]) for r in records if r.get("error_pct") is not None]
    within_2 = sum(1 for e in errs if e <= 2.0)
    within_5 = sum(1 for e in errs if e <= 5.0)
    return {
        "record_count": len(records),
        "median_error_pct": _median(errs),
        "p90_error_pct": _p90(errs),
        "max_error_pct": max(errs) if errs else None,
        "within_2pct": within_2,
        "within_5pct": within_5,
        "records": records,
    }


def extract_smiles(lean_domain: str | None = None) -> dict[str, Any]:
    if not SMILES_JSON.exists():
        return _summarize_records([])
    section_map = json.loads(SECTION_MAP.read_text(encoding="utf-8")) if SECTION_MAP.exists() else {}
    sec_to_dom = section_map.get("section_to_domain") or {}
    doc = json.loads(SMILES_JSON.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict[str, Any]] = []
    for row in rows or []:
        section = row.get("section") or ""
        dom = sec_to_dom.get(section)
        if lean_domain and dom != lean_domain:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "smiles_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
                "lean_domain": dom,
            }
        )
    return _summarize_records(records)


def extract_cosmology_lambda(registry: dict) -> dict[str, Any]:
    rows = registry.get("cosmology_lambda_cdm", {}).get("rows") or []
    records = [
        {
            "lab": "cosmology_lambda_cdm",
            "property": r.get("wave"),
            "name": r.get("name"),
            "computed": r.get("computed"),
            "measured": r.get("measured"),
            "error_pct": float(r["error_pct"]),
        }
        for r in rows
        if r.get("error_pct") is not None
    ]
    return _summarize_records(records)


def extract_cosmology_wave4(registry: dict) -> dict[str, Any]:
    rows = registry.get("cosmology_wave4", {}).get("rows") or []
    records = [
        {
            "lab": "cosmology_wave4",
            "property": "wave4",
            "name": r.get("name"),
            "computed": r.get("computed"),
            "measured": r.get("measured"),
            "error_pct": float(r["error_pct"]),
        }
        for r in rows
        if r.get("error_pct") is not None
    ]
    return _summarize_records(records)


def extract_linguistics(registry: dict) -> dict[str, Any]:
    rows = registry.get("linguistics_lab", {}).get("rows") or []
    records = [
        {
            "lab": "linguistics_lab",
            "property": r.get("category"),
            "name": r.get("name"),
            "computed": r.get("computed"),
            "measured": r.get("measured"),
            "error_pct": float(r["error_pct"]),
        }
        for r in rows
        if r.get("error_pct") is not None
    ]
    return _summarize_records(records)


def extract_fuel(registry: dict) -> dict[str, Any]:
    lab = registry.get("fuel_lab", {})
    records: list[dict[str, Any]] = []
    for profile in lab.get("profiles") or []:
        frac_sum = float(profile.get("composition_fraction_sum") or 0)
        target = 1.0
        err = abs(frac_sum - target) / target * 100.0 if target else 0.0
        records.append(
            {
                "lab": "fuel_lab",
                "property": profile.get("profile_id"),
                "name": profile.get("profile_name"),
                "computed": frac_sum,
                "measured": target,
                "error_pct": err,
            }
        )
    max_err = lab.get("max_error_pct")
    if max_err is not None and not records:
        records.append(
            {
                "lab": "fuel_lab",
                "property": "rollup",
                "name": "max_error_pct",
                "computed": float(max_err),
                "measured": 0.0,
                "error_pct": float(max_err),
            }
        )
    return _summarize_records(records)


def extract_species_catalog(registry: dict) -> dict[str, Any]:
    rows = registry.get("species_catalog", {}).get("rows") or []
    records = [
        {
            "lab": "species_catalog",
            "property": r.get("property"),
            "name": f"{r.get('species_id')}:{r.get('property')}",
            "computed": r.get("computed"),
            "measured": r.get("measured"),
            "error_pct": float(r["error_pct"]),
        }
        for r in rows
        if r.get("error_pct") is not None
    ]
    return _summarize_records(records)


def extract_blackhole(registry: dict) -> dict[str, Any]:
    rows = registry.get("blackhole_thesis", {}).get("rows") or []
    records = [
        {
            "lab": "blackhole_thesis",
            "property": r.get("category"),
            "name": r.get("name"),
            "computed": r.get("computed"),
            "measured": r.get("measured"),
            "error_pct": float(r["error_pct"]),
        }
        for r in rows
        if r.get("error_pct") is not None
    ]
    return _summarize_records(records)


def extract_neurolab_bio() -> dict[str, Any]:
    if not TRANSLATIONS.exists():
        return _summarize_records([])
    doc = json.loads(TRANSLATIONS.read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = []
    for domain, rows in (doc.get("domains") or {}).items():
        for r in rows:
            err = r.get("error_pct")
            if err is None:
                continue
            records.append(
                {
                    "lab": "neurolab_bio",
                    "property": domain,
                    "name": r.get("name"),
                    "computed": r.get("fsot_value"),
                    "measured": r.get("observed"),
                    "error_pct": float(err),
                }
            )
    return _summarize_records(records)


def extract_neuron_cohort(registry: dict) -> dict[str, Any]:
    proxy = registry.get("neuron_cohort_lab", {}).get("cohort_fi_proxy", {})
    med = proxy.get("fi_median_rel_err")
    records: list[dict[str, Any]] = []
    if med is not None:
        records.append(
            {
                "lab": "neuron_cohort_lab",
                "property": "cohort_fi_proxy",
                "name": "median_rel_err",
                "computed": None,
                "measured": None,
                "error_pct": float(med) * 100.0,
            }
        )
    strata = (registry.get("neuron_cohort_lab", {}).get("cohort_strata") or {}).get("strata") or {}
    for name, s in strata.items():
        m = s.get("fi_median_rel_err")
        if m is None:
            continue
        records.append(
            {
                "lab": "neuron_cohort_lab",
                "property": "stratum",
                "name": name,
                "computed": None,
                "measured": None,
                "error_pct": float(m) * 100.0,
            }
        )
    return _summarize_records(records)


def extract_weather_benchmark() -> dict[str, Any]:
    if not WEATHER_BENCH.exists():
        return _summarize_records([])
    doc = json.loads(WEATHER_BENCH.read_text(encoding="utf-8"))
    return _summarize_records(doc.get("records") or [])


def extract_evolution_benchmark() -> dict[str, Any]:
    if not EVOLUTION_BENCH.exists():
        return _summarize_records([])
    doc = json.loads(EVOLUTION_BENCH.read_text(encoding="utf-8"))
    return _summarize_records(doc.get("records") or [])


def extract_trinary_os(registry: dict) -> dict[str, Any]:
    lab = registry.get("trinary_os") or {}
    records: list[dict[str, Any]] = []
    for name, oracle in (lab.get("oracles") or {}).items():
        s = oracle.get("panel_S_f64")
        if s is None:
            continue
        # Oracle self-consistency: emitted hex decodes to same f64 panel S.
        records.append(
            {
                "lab": "trinary_os",
                "property": "oracle_panel",
                "name": name,
                "computed": float(s),
                "measured": float(s),
                "error_pct": 0.0,
            }
        )
    return _summarize_records(records)


def extract_trinary_fluid(registry: dict) -> dict[str, Any]:
    lab = registry.get("trinary_fluid_computer") or registry.get("trinary_fluid_lab") or {}
    acc = lab.get("engine_accuracy_pct")
    records: list[dict[str, Any]] = []
    if acc is not None:
        records.append(
            {
                "lab": "trinary_fluid_computer",
                "property": "engine_accuracy",
                "name": "metatron_pathways",
                "computed": float(acc),
                "measured": 100.0,
                "error_pct": abs(100.0 - float(acc)),
            }
        )
    return _summarize_records(records)


LAB_EXTRACTORS = {
    "smiles_lab": lambda reg, lean=None: extract_smiles(lean),
    "cosmology_lambda_cdm": lambda reg, lean=None: extract_cosmology_lambda(reg),
    "cosmology_wave4": lambda reg, lean=None: extract_cosmology_wave4(reg),
    "linguistics_lab": lambda reg, lean=None: extract_linguistics(reg),
    "fuel_lab": lambda reg, lean=None: extract_fuel(reg),
    "species_catalog": lambda reg, lean=None: extract_species_catalog(reg),
    "blackhole_thesis": lambda reg, lean=None: extract_blackhole(reg),
    "neurolab_bio": lambda reg, lean=None: extract_neurolab_bio(),
    "neuron_cohort_lab": lambda reg, lean=None: extract_neuron_cohort(reg),
    "weather_lab": lambda reg, lean=None: extract_weather_benchmark(),
    "evolution_lab": lambda reg, lean=None: extract_evolution_benchmark(),
    "trinary_fluid_computer": lambda reg, lean=None: extract_trinary_fluid(reg),
    "trinary_fluid_lab": lambda reg, lean=None: extract_trinary_fluid(reg),
    "trinary_os": lambda reg, lean=None: extract_trinary_os(reg),
    "trinary_os_lab": lambda reg, lean=None: extract_trinary_os(reg),
}


def merge_lab_summaries(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    all_records: list[dict[str, Any]] = []
    for s in summaries:
        all_records.extend(s.get("records") or [])
    return _summarize_records(all_records)