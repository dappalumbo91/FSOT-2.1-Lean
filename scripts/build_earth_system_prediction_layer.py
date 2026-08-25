#!/usr/bin/env python3
"""Earth-system prediction layer + scientist open-question map.

Not individual earthquake / eruption / storm dates. Those are not what the
fluid predicts. What it predicts is *class* behavior: Gutenberg–Richter slope,
quiet vs storm sectors, ocean–air bleed, slow vs fast rupture as one valve.

Cosmology already has the H0 multi-tool layer. This is the same grammar for
weather, seismic, volcanic, and solar/space-weather catalogs we already ingest.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import PHI  # noqa: E402

PRED = ROOT / "predictions"
OUT_JSON = PRED / "earth_system_prediction_layer.json"
OUT_MD = PRED / "reports" / "EARTH_SYSTEM_PREDICTIONS.md"
Q_JSON = PRED / "scientist_open_questions.json"
Q_MD = PRED / "reports" / "SCIENTIST_OPEN_QUESTIONS.md"


def _f(x) -> float:
    return float(x)


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    b_gr = _f(PHI) - 1.0 / _f(PHI)  # = 1 exactly
    interconnect = {}
    p = ROOT / "results" / "between_scale_interconnect_outcome.json"
    if p.is_file():
        interconnect = json.loads(p.read_text(encoding="utf-8"))

    predictions = [
        {
            "id": "PRED-056",
            "name": "usgs_comcat_gr_b_value",
            "domain": "Seismology",
            "tier_hint": "C",
            "fsot_predicted": b_gr,
            "unit": "b_value",
            "sota_baseline": 1.0,
            "sota_label": "Gutenberg–Richter empirical global b~1",
            "discriminant": "literature_band_b_value",
            "kill_if": "USGS ComCat / ISC-GEM named global MLE b-value outside 0.90–1.10",
            "future_survey": "USGS ComCat annual compilations; ISC-GEM",
            "what_it_is": (
                "Global magnitude-frequency slope b = φ − 1/φ = 1. "
                "Same acoustic counting as a Poisson process in the crustal fluid."
            ),
            "what_it_is_not": "A date or place for the next M≥7 earthquake.",
            "panel": "data/seismology_benchmark.json + USGS FDSN",
        },
        {
            "id": "PRED-057",
            "name": "slow_fast_rupture_one_valve",
            "domain": "Seismology",
            "tier_hint": "A",
            "fsot_predicted": 1.0,
            "unit": "same_valve_classifier",
            "sota_baseline": 0.0,
            "sota_label": "two unrelated constitutive laws (SSE vs EQ)",
            "discriminant": "same_valve_not_two_laws",
            "kill_if": (
                "community consensus that slow slip and fast earthquakes require "
                "two constitutive laws with no viscosity / rate-state continuum"
            ),
            "future_survey": "slow-slip moment-duration scaling literature (SSE vs EQ)",
            "what_it_is": (
                "POOF = fast rupture (orifice open). SUCTION = slow slip "
                "(re-compaction). Same T3 valve, different viscosity. C10 at crustal scale."
            ),
            "what_it_is_not": "A forecast of a specific slow-slip episode.",
            "panel": "docs/SCALE_INTERCONNECT_PHYSICS.md (acoustic) + CONCEPTS C10",
        },
        {
            "id": "PRED-058",
            "name": "volcanology_gvp_residual_hold",
            "domain": "Volcanology_Panel",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 8.0,
            "sota_label": "GVP/USGS geohazard heuristics",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "volcanology_panel_benchmark exceeds 0.5% on GVP/USGS refresh",
            "future_survey": "Smithsonian GVP + USGS volcano monitoring feeds",
            "what_it_is": "Eruption catalogs stay on the seed residual. VEI is a POOF-orifice class.",
            "what_it_is_not": "The date of the next VEI≥4 eruption.",
            "panel": "data/volcanology_panel_benchmark.json",
            "live_pooled_pct": 0.0235,
        },
        {
            "id": "PRED-059",
            "name": "swpc_kp_dst_classifier_hold",
            "domain": "Space_Weather",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 7.0,
            "sota_label": "Dst-Kp decoupled heuristic",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "space_weather or geomagnetism classifier panel exceeds 0.5% / 99.5% accuracy on SWPC refresh",
            "future_survey": "NOAA SWPC Kp/Dst/F10.7 continuous",
            "what_it_is": "Quiet vs storm are two sectors of the same solar-terrestrial valve (PRED-007 already locked ionospheric β).",
            "what_it_is_not": "A flare time-of-arrival for a named AR.",
            "panel": "data/space_weather_benchmark.json + data/geomagnetism_benchmark.json",
        },
        {
            "id": "PRED-060",
            "name": "ndbc_fluid_tanks_residual_hold",
            "domain": "Fluid_Dynamics",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 10.0,
            "sota_label": "per-buoy free-parameter marine climatology",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "Between_Scale_Interconnects fluid_tanks_* channels exceed 0.5% on NDBC refresh",
            "future_survey": "NOAA NDBC realtime + climate NCEI (PRED-054)",
            "what_it_is": "Same buoy pressure/SST/wind on Fluid, Ocean, Air folds. ENSO is κ not a new oscillator.",
            "what_it_is_not": "Next week's local forecast or the next El Niño onset date.",
            "panel": "data/between_scale_interconnect_benchmark.json",
            "live_pooled_pct": interconnect.get("pooled_median_error_pct"),
        },
        {
            "id": "PRED-061",
            "name": "seismic_acoustic_prem_hold",
            "domain": "Seismology",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 10.0,
            "sota_label": "siloed lab acoustics vs PREM",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "lithosphere vp/vs median channel exceeds 0.5% (deep PREM stays structural)",
            "future_survey": "PREM/IASP91/AK135 community Earth models",
            "what_it_is": "Mafic/lid Poisson ν=D_atomic/25. Deep phase changes are other interfaces.",
            "what_it_is_not": "A new radial Earth model replacing PREM.",
            "panel": "data/between_scale_interconnect_benchmark.json",
            "live_channel_pct": (interconnect.get("channel_median_error_pct") or {}).get(
                "seismic_acoustic_lithosphere_median"
            ),
        },
        {
            "id": "PRED-062",
            "name": "solar_quiet_storm_two_sectors",
            "domain": "Space_Weather",
            "tier_hint": "C",
            "fsot_predicted": 1.0,
            "unit": "two_sector_classifier",
            "sota_baseline": 0.0,
            "sota_label": "one solar-activity number for the whole cycle",
            "discriminant": "quiet_and_storm_remain_distinct_sectors",
            "kill_if": "quiet-time and storm-time SWPC classes collapse to one residual sector on refresh",
            "future_survey": "NOAA SWPC F10.7 + Kp class products; solar cycle 26 onset (2030s)",
            "what_it_is": (
                "Same grammar as Hubble: quiet and storm are different bubble-density "
                "sectors of one solar valve. Cycle 25 SSN is not relocked after the peak."
            ),
            "what_it_is_not": "A post-hoc Cycle 25 sunspot-number pick.",
            "panel": "data/space_weather_benchmark.json",
        },
        {
            "id": "PRED-063",
            "name": "climate_station_and_marine_hold",
            "domain": "Climate_Science",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 5.0,
            "sota_label": "per-station free-parameter climatology",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "climate_observed or NDBC fluid-tank channels exceed 0.5%",
            "future_survey": "NOAA NCEI + NDBC continuous (pairs with PRED-054)",
            "what_it_is": "Weather/climate as Meteorology+Ocean+Fluid tanks, already green.",
            "what_it_is_not": "S2S ensemble beating ECMWF at week 3–4.",
            "panel": "data/climate_observed_benchmark.json",
            "live_pooled_pct": 0.0120,
        },
        {
            "id": "PRED-064",
            "name": "dated_fluid_pressure_forecasts",
            "domain": "Seismology",
            "tier_hint": "C",
            "fsot_predicted": 1.0,
            "unit": "issued_windows_scored",
            "sota_baseline": 0.0,
            "sota_label": "no dated FSOT spatial-class forecast layer",
            "discriminant": "dated_windows_issued_and_scored",
            "kill_if": "issued forecast JSON rewritten after valid_from, or scoring abandoned",
            "future_survey": "USGS FDSN + NOAA SWPC + NDBC after each valid_to",
            "what_it_is": "Live pressure cells → location + calendar window. Score hit/miss. Iron the valve.",
            "what_it_is_not": "A clock-time for a single hypocenter, or a USGS/NWS watch replacement.",
            "panel": "predictions/dated_forecasts/LATEST.json",
        },
    ]

    questions = [
        {
            "id": "Q-EQ-01",
            "field": "seismology",
            "question": "Can we predict the time and place of the next large earthquake?",
            "community": "No deterministic short-term prediction; probabilistic hazard (Gutenberg–Richter, ETAS, CSE).",
            "fsot": "Not a clock-time hypocenter. Dated *windows* on live pressure cells (PRED-064): location + 7-day POOF window, scored after valid_to.",
            "status": "preregistered",
            "pred_ids": ["PRED-056", "PRED-064"],
        },
        {
            "id": "Q-EQ-02",
            "field": "seismology",
            "question": "Why is the global b-value ≈ 1?",
            "community": "Empirical Gutenberg–Richter; regional 0.6–1.4; physical origin debated.",
            "fsot": "b = φ − 1/φ = 1. Acoustic counting in the crustal fluid. PRED-056 literature band 0.90–1.10.",
            "status": "preregistered",
            "pred_ids": ["PRED-056"],
        },
        {
            "id": "Q-EQ-03",
            "field": "seismology",
            "question": "Are slow slip and fast earthquakes two different physics?",
            "community": "Moment-duration scaling linear vs cubic still contested; no unifying constitutive law.",
            "fsot": "One T3 valve: POOF = fast, SUCTION = slow. Viscosity continuum. PRED-057.",
            "status": "preregistered",
            "pred_ids": ["PRED-057"],
        },
        {
            "id": "Q-EQ-04",
            "field": "seismology",
            "question": "Lab acoustics vs Earth PREM — same wave?",
            "community": "Often siloed (ultrasonics vs global Earth models).",
            "fsot": "Already residual-gated: mafic/lid vp/vs from ν=D_atomic/25. PRED-061.",
            "status": "solved_residual",
            "pred_ids": ["PRED-061"],
        },
        {
            "id": "Q-VOLC-01",
            "field": "volcanology",
            "question": "Can we predict eruption onset dates?",
            "community": "Unrest monitoring (InSAR, SO2, seismicity); no reliable date forecast.",
            "fsot": "Not a clock-time. Volcanic USGS cells get 14-day POOF windows (PRED-064) plus GVP residual hold PRED-058.",
            "status": "preregistered",
            "pred_ids": ["PRED-058", "PRED-064"],
        },
        {
            "id": "Q-SOL-01",
            "field": "solar_space_weather",
            "question": "What will the solar-cycle amplitude be (one SSN)?",
            "community": "Cycle 25 panel said ~115 (Jul 2025); cycle ran stronger. Amplitude remains hard.",
            "fsot": "Not one number — quiet vs storm sectors of one valve (same grammar as H0). PRED-062. Do not relock Cycle 25 SSN after the peak.",
            "status": "preregistered",
            "pred_ids": ["PRED-062", "PRED-059", "PRED-007"],
        },
        {
            "id": "Q-SOL-02",
            "field": "solar_space_weather",
            "question": "Can Kp/Dst be classified from first principles rather than decoupled heuristics?",
            "community": "Empirical Kp/Dst thresholds; coupling to F10.7 / IMF is statistical.",
            "fsot": "Already green classifiers + PRED-007 ionospheric β. Hold PRED-059 on SWPC refresh.",
            "status": "solved_residual",
            "pred_ids": ["PRED-007", "PRED-059"],
        },
        {
            "id": "Q-WX-01",
            "field": "weather_climate",
            "question": "Is ENSO a separate oscillator from the rest of the fluid?",
            "community": "Coupled ocean-atmosphere modes; S2S skill is the operational frontier.",
            "fsot": "κ(Oceanography, Atmospheric_Physics, Fluid_Dynamics). Residual holds PRED-060/063/054. Not an ECMWF-beating week-3 forecast.",
            "status": "preregistered",
            "pred_ids": ["PRED-060", "PRED-063", "PRED-054"],
        },
        {
            "id": "Q-WX-02",
            "field": "weather_climate",
            "question": "Can FSOT beat numerical weather prediction at S2S?",
            "community": "S2S is an active WMO/NOAA program; skill drops after ~2 weeks.",
            "fsot": "Not claimed. Class residuals on NDBC/NCEI only. Individual storm tracks are T1 look, not a new H0.",
            "status": "honest_refusal",
            "pred_ids": [],
        },
        {
            "id": "Q-H0-01",
            "field": "cosmology",
            "question": "Why do Planck and SH0ES disagree on H0?",
            "community": "Hubble tension; new physics vs systematics.",
            "fsot": "Solved as sectors of one fluid, not two cosmologies. Class vs chain vs local cz/d. PRED-001 family.",
            "status": "solved_residual",
            "pred_ids": ["PRED-001", "PRED-024", "PRED-051"],
        },
        {
            "id": "Q-S8-01",
            "field": "cosmology",
            "question": "S8 tension (Planck vs weak lensing)?",
            "community": "Open. Euclid DR1 is the next independent drop.",
            "fsot": "PRED-002 / PRED-042 lock 0.805 between Planck and DES. Watch Euclid Nov 2026.",
            "status": "preregistered",
            "pred_ids": ["PRED-002", "PRED-042"],
        },
        {
            "id": "Q-LI-01",
            "field": "cosmology_nuclear",
            "question": "Cosmological lithium problem?",
            "community": "BBN vs halo-star Li gap ~factor 3.",
            "fsot": "PRED-005 factor 2.85. Nuclear orifice already dual-routed (PRED nuclear levels).",
            "status": "preregistered",
            "pred_ids": ["PRED-005"],
        },
        {
            "id": "Q-G2-01",
            "field": "particle",
            "question": "Muon g-2 excess?",
            "community": "Experiment vs lattice SM still moving.",
            "fsot": "PRED-004/050 same-sign lock. Do not retune after lattice papers.",
            "status": "preregistered",
            "pred_ids": ["PRED-004", "PRED-050"],
        },
        {
            "id": "Q-HIGGS-01",
            "field": "particle",
            "question": "Is m_H an input or a prediction?",
            "community": "SM input; measured ~125.25 GeV.",
            "fsot": "PRED-049 hold vs next PDG combination at 0.5%.",
            "status": "preregistered",
            "pred_ids": ["PRED-049"],
        },
        {
            "id": "Q-GEN-01",
            "field": "biology",
            "question": "Can sequence-only models beat measured-map folds?",
            "community": "AlphaFold-class interpolators; wet-lab structures still the product.",
            "fsot": "Genetics sibling freeze 0.13 Å vs AF 0.47 Å. Hub waits for that freeze to migrate. Zebrafish 0.358% stays inside 0.5%.",
            "status": "sibling_owned",
            "pred_ids": ["PRED-055"],
        },
        {
            "id": "Q-ECON-01",
            "field": "economics",
            "question": "Is a market a different medium from a neural net?",
            "community": "Econophysics vs institutional economics.",
            "fsot": "As-above-so-below. Economics pooled 0.129% still the largest social residual — next interconnect, not a fitted β.",
            "status": "open_residual",
            "pred_ids": [],
        },
    ]

    status_counts: dict[str, int] = {}
    for q in questions:
        status_counts[str(q["status"])] = status_counts.get(str(q["status"]), 0) + 1

    layer = {
        "generated_at": ts,
        "pin": "D1D38A",
        "policy": [
            "no_individual_earthquake_dates",
            "no_individual_eruption_dates",
            "no_s2s_claim_vs_ecmwf",
            "no_posthoc_cycle25_ssn",
            "do_not_rewrite_frozen_centrals",
        ],
        "grammar": (
            "Same as Hubble: one fluid, many sectors. Quiet/storm, slow/fast, "
            "ocean/air are interfaces, not extra laws."
        ),
        "predictions": predictions,
        "n_predictions": len(predictions),
    }
    OUT_JSON.write_text(json.dumps(layer, indent=2), encoding="utf-8")

    qdoc = {
        "generated_at": ts,
        "pin": "D1D38A",
        "purpose": "Map questions scientists currently argue about onto FSOT folds: already gated, preregistered, refused, or still open.",
        "status_counts": status_counts,
        "questions": questions,
    }
    Q_JSON.write_text(json.dumps(qdoc, indent=2), encoding="utf-8")

    lines = [
        "# Earth-system predictions (weather, seismic, volcanic, solar)",
        "",
        f"*Generated {ts} · pin D1D38A*",
        "",
        "Cosmology already has a 25-tool H₀ layer. This is the **same grammar** for",
        "Earth: structure + neighborhood bubble, not one number and not a date.",
        "",
        "**Refresh:** `python scripts/build_earth_system_prediction_layer.py`",
        "",
        "## What we will not claim",
        "",
        "- The time/place of the next large earthquake or VEI≥4 eruption.",
        "- Beating ECMWF at subseasonal (S2S) week 3–4.",
        "- A post-hoc Solar Cycle 25 sunspot-number pick.",
        "",
        "Those are T1 look / catalog noise, not seed-closed centrals.",
        "",
        "## Locks",
        "",
        "| ID | Domain | Lock | Kill | Not |",
        "|----|--------|------|------|-----|",
    ]
    for p in predictions:
        lines.append(
            f"| `{p['id']}` | {p['domain']} | {p['fsot_predicted']} {p['unit']} | "
            f"{p['kill_if']} | {p['what_it_is_not']} |"
        )
    lines += [
        "",
        "Hand PREDs live in `predictions/preregistered_predictions_manifest.yaml`.",
        "Score outcomes in `results/` — do not rewrite these centrals.",
        "",
        "Scientist question map: [`SCIENTIST_OPEN_QUESTIONS.md`](SCIENTIST_OPEN_QUESTIONS.md).",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    qlines = [
        "# Scientist open questions → FSOT folds",
        "",
        f"*Generated {ts} · pin D1D38A*",
        "",
        "This is a **discovery ledger**, not a trophy wall. Each row is a question",
        "working scientists actually argue about. Status is one of:",
        "",
        "| Status | Meaning |",
        "|--------|---------|",
        "| `solved_residual` | Already gated on a named public table |",
        "| `preregistered` | Frozen PRED with a kill; waiting on a catalog/paper |",
        "| `honest_refusal` | The model does **not** claim this (dates, S2S NWP beat) |",
        "| `sibling_owned` | Genetics/Quantum live freeze, not this hub's product |",
        "| `open_residual` | Domain is green but the interconnect is still thin |",
        "",
        f"Counts: {status_counts}",
        "",
        "| ID | Field | Question | Community | FSOT | Status | PREDs |",
        "|----|-------|----------|-----------|------|--------|-------|",
    ]
    for q in questions:
        qlines.append(
            f"| `{q['id']}` | {q['field']} | {q['question']} | {q['community']} | "
            f"{q['fsot']} | **{q['status']}** | {', '.join(q['pred_ids']) or '—'} |"
        )
    qlines += [
        "",
        "Related: [`EARTH_SYSTEM_PREDICTIONS.md`](EARTH_SYSTEM_PREDICTIONS.md) ·",
        "[`PREDICTION_TIERS.md`](PREDICTION_TIERS.md) · [`../EXPLAINED.md`](../EXPLAINED.md)",
        "",
        "Refresh: `python scripts/build_earth_system_prediction_layer.py`",
        "",
    ]
    Q_MD.write_text("\n".join(qlines), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {Q_JSON}")
    print(f"Wrote {Q_MD}")
    print(f"  preds={len(predictions)} questions={len(questions)} {status_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
