#!/usr/bin/env python3
"""Audit FSOT green-gate margins and map them to domain-standard scientific metrics.

Does not re-fit the engine. Reads:
  - data/benchmark_margin_audit.json
  - data/publication/domain_atlas.csv

Writes:
  - data/scientific_error_metrics_map.json
  - data/scientific_error_metrics_map.md
  - data/margin_health_audit.json
"""

from __future__ import annotations

import csv
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BM_PATH = ROOT / "data" / "benchmark_margin_audit.json"
ATLAS_PATH = ROOT / "data" / "publication" / "domain_atlas.csv"
OUT_JSON = ROOT / "data" / "scientific_error_metrics_map.json"
OUT_MD = ROOT / "data" / "scientific_error_metrics_map.md"
OUT_MARGIN = ROOT / "data" / "margin_health_audit.json"

# FSOT internal gate (percent relative error on scalar/observable pools)
FSOT_GREEN_POOLED_MEDIAN_PCT = 0.5
FSOT_CLASSIFIER_MIN_PCT = 99.5

# Domain-family → conventional scientific reporting metrics.
# These are *reporting anchors* for the same residual numbers, not new free parameters.
FAMILY_SPECS: list[dict] = [
    {
        "family": "cosmology_astrophysics",
        "match": [
            "cosmolog", "astrophys", "hubble", "cmb", "dark_energy", "gravitational",
            "blackhole", "stellar", "galactic", "exoplanet", "space_weather", "magnetosphere",
            "plasma", "orbital", "astrometry", "gaia", "nebula", "frb",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["fractional_residual", "tension_sigma_proxy"],
        "field_norm": (
            "Cosmology/astro results are usually quoted as percent-level or σ tension "
            "vs ΛCDM anchors (Planck H0, SH0ES). Fractional residual |c-m|/|m| is standard."
        ),
        "good_practice_band": "sub-percent to few-percent on derived scalars; σ for tensions",
    },
    {
        "family": "particle_nuclear_atomic",
        "match": [
            "particle", "higgs", "nuclear", "atomic", "quantum", "proton", "electron",
            "standard_model", "cern", "pdg",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["ppm_when_sub_1e-4", "absolute_residual"],
        "field_norm": (
            "Particle/atomic constants often use relative uncertainty or ppm/ppb "
            "(CODATA/NIST). Percent is fine above ~0.01%; switch to ppm below."
        ),
        "good_practice_band": "ppm–% depending on observable class",
    },
    {
        "family": "chemistry_materials",
        "match": [
            "chem", "molecular", "smiles", "pubchem", "material", "metamaterial",
            "bond", "fuel", "thermochem", "periodic", "superheavy", "crystal",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["MAE_if_same_units", "RMSE_if_available"],
        "field_norm": (
            "Chemistry/materials properties commonly use % error vs handbook/CRC/NIST, "
            "or MAE/RMSE in physical units (e.g. kcal/mol, Å) when units are uniform."
        ),
        "good_practice_band": "sub-percent to low-% on extensive property tables",
    },
    {
        "family": "earth_climate_geophysics",
        "match": [
            "climate", "meteorolog", "hydrolog", "seism", "geolog", "ocean",
            "cryosphere", "weather", "atmospheric", "tectonic", "geomagnet",
            "soil", "limnolog",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["bias", "RMSE_proxy_from_pool"],
        "field_norm": (
            "Geophysics/climate often report RMSE, bias, and anomaly correlation; "
            "relative % remains a cross-domain compression for multi-observable pools."
        ),
        "good_practice_band": "RMSE/bias in native units preferred; % for multi-metric pools",
    },
    {
        "family": "biology_medicine_genomics",
        "match": [
            "bio", "genom", "immun", "cardio", "medic", "clinic", "protein",
            "species", "ecology", "longevity", "zebra", "ncbi", "oncolog",
            "virolog", "neuro", "cell",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["classifier_accuracy", "AUC_proxy_if_classifier"],
        "field_norm": (
            "Life sciences mix continuous biomarkers (% error / MAE) with classifiers "
            "(accuracy, F1, AUC). FSOT green gate already tracks classifier ≥99.5% where applicable."
        ),
        "good_practice_band": "continuous: % or MAE; discrete: accuracy/F1",
    },
    {
        "family": "engineering_propulsion_energy",
        "match": [
            "engineer", "propulsion", "fuel", "fusion", "electrical", "power",
            "hvac", "circuit", "hardware", "desktop", "transporter", "airfoil",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["design_tolerance_band"],
        "field_norm": (
            "Engineering specs use tolerance bands and % error vs measured performance "
            "(thrust, efficiency, impedance)."
        ),
        "good_practice_band": "typically ≤1–5% depending on subsystem",
    },
    {
        "family": "social_econ_linguistics",
        "match": [
            "econ", "soci", "lingu", "anthrop", "finance", "actuar", "world_bank",
            "supply", "music", "creative",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["MAPE", "sMAPE"],
        "field_norm": (
            "Economics/forecasting conventionally use MAPE/sMAPE; FSOT pooled median % "
            "is the MAPE-family cousin (median absolute percentage error style)."
        ),
        "good_practice_band": "MAPE-style; domain-dependent",
    },
    {
        "family": "formal_math_computation",
        "match": [
            "math", "formula", "proof", "formal", "trinary", "comput", "token",
            "llm", "oracle", "certified",
        ],
        "primary_metric": "relative_percent_error",
        "also_report": ["exact_match_rate", "bit_parity"],
        "field_norm": (
            "Formal/computation layers emphasize exactness and parity; numeric residuals "
            "still use relative error when comparing derived scalars."
        ),
        "good_practice_band": "near-exact for discrete; sub-% for continuous scalars",
    },
]


def _family_for(domain: str) -> dict:
    d = (domain or "").lower()
    for spec in FAMILY_SPECS:
        if any(tok in d for tok in spec["match"]):
            return spec
    return {
        "family": "general_scientific",
        "primary_metric": "relative_percent_error",
        "also_report": ["fractional_residual"],
        "field_norm": "Default: median absolute percentage residual vs measured anchors.",
        "good_practice_band": "FSOT green: pooled median ≤ 0.5%",
        "match": [],
    }


def pct_to_fractional(pct: float | None) -> float | None:
    if pct is None:
        return None
    return float(pct) / 100.0


def pct_to_ppm(pct: float | None) -> float | None:
    if pct is None:
        return None
    return float(pct) * 10_000.0  # 1% = 10000 ppm


def pct_to_db_like(pct: float | None) -> float | None:
    """Optional SNR-style transform: -20 log10(frac) for tiny residuals (informational)."""
    if pct is None or pct <= 0:
        return None
    frac = pct / 100.0
    if frac <= 0:
        return None
    return -20.0 * math.log10(frac)


def main() -> int:
    bm = json.loads(BM_PATH.read_text(encoding="utf-8"))
    atlas_rows = list(csv.DictReader(ATLAS_PATH.open(encoding="utf-8")))
    atlas_by = {r["domain"]: r for r in atlas_rows}

    domains = bm.get("all_domains") or []
    by_family: dict[str, list[dict]] = defaultdict(list)
    mapped: list[dict] = []

    green = 0
    fail = 0
    near_miss = []

    for d in domains:
        name = d.get("domain") or d.get("file") or "?"
        pooled = d.get("official_pooled_median_error_pct")
        if pooled is None:
            pooled = d.get("pooled_median_error_pct")
        try:
            pooled_f = float(pooled) if pooled is not None else None
        except (TypeError, ValueError):
            pooled_f = None
        max_scalar = d.get("max_scalar_error_pct")
        try:
            max_scalar_f = float(max_scalar) if max_scalar is not None else None
        except (TypeError, ValueError):
            max_scalar_f = None

        gpass = bool(d.get("green_gate_pass"))
        if gpass:
            green += 1
        else:
            fail += 1

        if pooled_f is not None and pooled_f > 0.4:
            near_miss.append((name, pooled_f, max_scalar_f))

        fam = _family_for(name)
        atl = atlas_by.get(name, {})
        rec = {
            "domain": name,
            "family": fam["family"],
            "records": d.get("records") or atl.get("record_count"),
            "fsot_pooled_median_error_pct": pooled_f,
            "fsot_max_scalar_error_pct": max_scalar_f,
            "green_gate_pass": gpass,
            "coverage_tier": atl.get("coverage_tier"),
            "scientific_metrics": {
                "relative_percent_error_median": pooled_f,
                "fractional_residual_median": pct_to_fractional(pooled_f),
                "ppm_median": pct_to_ppm(pooled_f) if pooled_f is not None and pooled_f < 0.01 else None,
                "mape_family_note": "FSOT pooled median % is MAPE-family (median absolute % residual)",
                "snr_like_db": pct_to_db_like(pooled_f),
                "primary_metric": fam["primary_metric"],
                "also_report": fam["also_report"],
                "field_norm": fam["field_norm"],
            },
            "fsot_gate": {
                "pooled_median_le_pct": FSOT_GREEN_POOLED_MEDIAN_PCT,
                "classifier_min_pct": FSOT_CLASSIFIER_MIN_PCT,
            },
        }
        mapped.append(rec)
        by_family[fam["family"]].append(rec)

    family_summary = []
    for fam_name, rows in sorted(by_family.items(), key=lambda kv: -len(kv[1])):
        pools = [r["fsot_pooled_median_error_pct"] for r in rows if r["fsot_pooled_median_error_pct"] is not None]
        family_summary.append(
            {
                "family": fam_name,
                "domain_count": len(rows),
                "green_count": sum(1 for r in rows if r["green_gate_pass"]),
                "pooled_median_of_domains_pct": statistics.median(pools) if pools else None,
                "pooled_mean_of_domains_pct": statistics.mean(pools) if pools else None,
                "pooled_max_of_domains_pct": max(pools) if pools else None,
                "fractional_median": pct_to_fractional(statistics.median(pools)) if pools else None,
                "primary_metric": rows[0]["scientific_metrics"]["primary_metric"] if rows else None,
                "field_norm": rows[0]["scientific_metrics"]["field_norm"] if rows else None,
            }
        )

    margin_doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(BM_PATH.relative_to(ROOT)),
        "green_gate_pass_count": bm.get("green_gate_pass_count"),
        "green_gate_fail_count": bm.get("green_gate_fail_count"),
        "benchmark_file_count": bm.get("benchmark_file_count"),
        "worst_scalar_max_error_pct": bm.get("worst_scalar_max_error_pct"),
        "worst_scalar_domain": bm.get("worst_scalar_domain"),
        "thresholds": {k: bm[k] for k in bm if str(k).startswith("threshold")},
        "recomputed_green": green,
        "recomputed_fail": fail,
        "near_miss_pooled_gt_0_4pct": [
            {"domain": n, "pooled_median_pct": p, "max_scalar_pct": m}
            for n, p, m in sorted(near_miss, key=lambda t: -t[1])[:40]
        ],
        "atlas_domain_count": len(atlas_rows),
        "benchmark_domain_count": len(domains),
        "nothing_fell_out": fail == 0 and int(bm.get("green_gate_fail_count") or 0) == 0,
    }
    OUT_MARGIN.write_text(json.dumps(margin_doc, indent=2), encoding="utf-8")

    metrics_doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Anchor FSOT's internal ≤0.5% pooled median residual gate to conventional "
            "scientific error reporting per domain family. Same residuals; clearer units."
        ),
        "fsot_internal_gate": {
            "pooled_median_error_pct_max": FSOT_GREEN_POOLED_MEDIAN_PCT,
            "classifier_accuracy_min_pct": FSOT_CLASSIFIER_MIN_PCT,
            "definition": "ε_i = 100 * |c_i - m_i| / max(|m_i|, ε_floor); domain metric = median(ε)",
        },
        "conversion": {
            "fractional_residual": "pct / 100",
            "ppm": "pct * 10000 (only highlighted when pct < 0.01)",
            "mape_family": "pooled median % is the cross-domain MAPE-style statistic",
            "snr_like_db": "-20 * log10(pct/100) informational transform",
        },
        "family_summary": family_summary,
        "domains": mapped,
    }
    OUT_JSON.write_text(json.dumps(metrics_doc, indent=2), encoding="utf-8")

    lines = [
        "# Scientific error metrics map (FSOT residuals → field language)",
        "",
        f"Generated: `{metrics_doc['generated_at']}`",
        "",
        "## Internal FSOT gate (unchanged)",
        "",
        f"- Pooled median relative error **≤ {FSOT_GREEN_POOLED_MEDIAN_PCT}%**",
        f"- Classifier accuracy **≥ {FSOT_CLASSIFIER_MIN_PCT}%** where applicable",
        f"- Margin health: **green {margin_doc['green_gate_pass_count']}/{margin_doc['benchmark_file_count']}**, "
        f"fail **{margin_doc['green_gate_fail_count']}**, "
        f"worst scalar max **{margin_doc['worst_scalar_max_error_pct']}%** "
        f"(`{margin_doc['worst_scalar_domain']}`)",
        f"- Nothing fell out: **{margin_doc['nothing_fell_out']}**",
        "",
        "## Conversion anchors",
        "",
        "| FSOT % residual | Fractional | ppm | Notes |",
        "|-----------------|------------|-----|-------|",
        "| 0.5 | 0.005 | 5000 | Green gate ceiling |",
        "| 0.1 | 0.001 | 1000 | Strong continuous agreement |",
        "| 0.01 | 0.0001 | 100 | Prefer ppm language |",
        "| 0.001 | 1e-5 | 10 | Metrology-class relative error |",
        "",
        "## Family rollup (median of domain pooled medians)",
        "",
        "| Family | Domains | Green | Median % | Fractional | Field metric language |",
        "|--------|--------:|------:|---------:|-----------:|----------------------|",
    ]
    for fs in family_summary:
        lines.append(
            f"| {fs['family']} | {fs['domain_count']} | {fs['green_count']} | "
            f"{fs['pooled_median_of_domains_pct'] if fs['pooled_median_of_domains_pct'] is not None else 'n/a'} | "
            f"{fs['fractional_median'] if fs['fractional_median'] is not None else 'n/a'} | "
            f"{fs['primary_metric']} |"
        )
    lines += [
        "",
        "## Field norms (how to publish)",
        "",
    ]
    for spec in FAMILY_SPECS:
        lines += [
            f"### {spec['family']}",
            "",
            f"- Primary: `{spec['primary_metric']}`",
            f"- Also: {', '.join(f'`{x}`' for x in spec['also_report'])}",
            f"- Norm: {spec['field_norm']}",
            "",
        ]
    lines += [
        "## Note",
        "",
        "This map **does not retune** FSOT. It renames/annotates the same residuals so ",
        "domain scientists see MAPE/fractional/ppm/σ-proxy language next to the green gate.",
        "",
        f"Machine-readable: `{OUT_JSON.relative_to(ROOT)}`",
        f"Margin audit: `{OUT_MARGIN.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_MARGIN}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"green={margin_doc['green_gate_pass_count']}/{margin_doc['benchmark_file_count']} "
        f"fail={margin_doc['green_gate_fail_count']} nothing_fell_out={margin_doc['nothing_fell_out']}"
    )
    print(f"families={len(family_summary)} near_miss>0.4%={len(near_miss)}")
    return 0 if margin_doc["nothing_fell_out"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
