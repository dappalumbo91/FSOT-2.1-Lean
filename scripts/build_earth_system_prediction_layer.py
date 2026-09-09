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
        {
            "id": "PRED-065",
            "name": "noaa_coastal_tides_residual_hold",
            "domain": "NOAA_Coastal_Tides",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 5.0,
            "sota_label": "per-station harmonic-only climatology",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "noaa_coastal_tides_benchmark exceeds 0.5% on CO-OPS refresh",
            "future_survey": "NOAA CO-OPS station dumps",
            "what_it_is": "Station residual hold. Dated surge windows use POOF metres under PRED-064.",
            "what_it_is_not": "A beat of NOAA harmonic tables at every minute.",
            "panel": "data/noaa_coastal_tides_benchmark.json",
            "live_pooled_pct": 0.030173,
        },
        {
            "id": "PRED-066",
            "name": "exoplanet_architecture_class_hold",
            "domain": "Exoplanet_System_Architecture",
            "tier_hint": "A",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 12.0,
            "sota_label": "per-planet free-parameter formation channels",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "Exoplanet_System_Architecture pooled median exceeds 0.5% on NASA archive refresh",
            "future_survey": "NASA Exoplanet Archive TAP refreshes",
            "what_it_is": "Radius–period–insolation as one D=21 fold. Not one ε per planet.",
            "what_it_is_not": "The discovery date of the next transiting Earth analog.",
            "panel": "data/exoplanet_system_architecture_benchmark.json",
        },
        {
            "id": "PRED-067",
            "name": "gwtc_chirp_mass_class_hold",
            "domain": "Compact_Object_Binary_Events",
            "tier_hint": "A",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 10.0,
            "sota_label": "GW surrogate templates",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "compact_object_binary_events chirp-mass class exceeds 0.5% on GWTC refresh",
            "future_survey": "GWOSC / GWTC O4 remainder and O5",
            "what_it_is": "Chirp-mass class (live 0.010%). Sirens stay mid-sector (~70).",
            "what_it_is_not": "The GPS time of the next compact-binary merger.",
            "panel": "data/compact_object_binary_events_benchmark.json",
            "live_pooled_pct": 0.010049,
        },
        {
            "id": "PRED-068",
            "name": "gbif_occurrence_class_hold",
            "domain": "GBIF_Species_Occurrence",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 8.0,
            "sota_label": "species-distribution model occupancy zoo",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "gbif_species_occurrence_benchmark exceeds 0.5% on dump refresh",
            "future_survey": "GBIF occurrence dump refreshes",
            "what_it_is": "Occurrence-field counting (240 rec / 0.006%). Acoustic-ecology, D=15.",
            "what_it_is_not": "The date a named species arrives in a new county.",
            "panel": "data/gbif_species_occurrence_benchmark.json",
            "live_pooled_pct": 0.006006,
        },
        {
            "id": "PRED-069",
            "name": "epidemiology_class_hold",
            "domain": "Epidemiology_Panel",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 8.0,
            "sota_label": "unstructured public-health null",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "epidemiology_panel_benchmark exceeds 0.5% on World Bank / WHO refresh",
            "future_survey": "World Bank / WHO named health-indicator refreshes",
            "what_it_is": "Class counts on the same valve as GR b-value (24 rec / 0.015%).",
            "what_it_is_not": "The start date of the next named outbreak in a named city.",
            "panel": "data/epidemiology_panel_benchmark.json",
            "live_pooled_pct": 0.015311,
        },
        {
            "id": "PRED-078",
            "name": "hydrology_flood_quiet_two_sectors",
            "domain": "Hydrology",
            "tier_hint": "C",
            "fsot_predicted": 1.0,
            "unit": "two_sector_classifier",
            "sota_baseline": 0.0,
            "sota_label": "one catchment-specific flood law per gage",
            "discriminant": "quiet_and_storm_remain_distinct_sectors",
            "kill_if": "high-flow and quiet NWIS classes collapse to one residual sector, or issued hydro windows never scored",
            "future_survey": "USGS NWIS IV/DV after each hydrology window",
            "what_it_is": "High-flow vs quiet = two sectors of one valve (load bar = 1+POOF). Dated 7-day gage windows.",
            "what_it_is_not": "Street-level inundation maps. A 0.5% central on one gage's next-hour stage.",
            "panel": "data/hydrology_usgs_manifest.yaml",
        },
        {
            "id": "PRED-080",
            "name": "grace_greenland_mass_delta_hold",
            "domain": "Grace_Cryosphere",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 10.0,
            "sota_label": "ice-sheet model vs GRACE offset",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "grace_cryosphere |delta| scalar median exceeds 0.5% on GravIS refresh",
            "future_survey": "GFZ GravIS Greenland mass time series",
            "what_it_is": "Month-to-month |delta| APPLY residual (live 0.023%). Decline classifier is separate.",
            "what_it_is_not": "The calendar day the next ice shelf calves.",
            "panel": "data/grace_cryosphere_benchmark.json",
            "live_pooled_pct": 0.023015,
        },
        {
            "id": "PRED-081",
            "name": "agriculture_season_class_hold",
            "domain": "Agriculture_Agroecology",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 10.0,
            "sota_label": "agroecology field-survey / USDA post-harvest retune",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "agriculture_agroecology_gap_fill pooled median exceeds 0.5% on GBIF / World Bank refresh",
            "future_survey": "GBIF crop-proxy + World Bank agriculture indicator refreshes",
            "what_it_is": "Season-class residual (276 rec / 0.018%). Same viscosity as ecology and hydrology.",
            "what_it_is_not": "County bushels next Tuesday. A USDA yield-number pick after harvest.",
            "panel": "data/agriculture_agroecology_gap_fill_benchmark.json",
            "live_pooled_pct": 0.018019,
        },
        {
            "id": "PRED-082",
            "name": "gaia_parallax_class_hold",
            "domain": "Gaia_Astrometry_Panel_Deep",
            "tier_hint": "A",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 5.0,
            "sota_label": "one free epsilon per Gaia source",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "Gaia astrometry / CAT-GAIA-DR3 pooled median exceeds 0.5% on DR4 / DR3 reprocess",
            "future_survey": "Gaia DR4 / DR3 reprocess public samples",
            "what_it_is": "Parallax / proper-motion class (deep 62 / 0.022%; CAT 3459 / 0.022%). Ladder-adjacent.",
            "what_it_is_not": "A new H0 from one star.",
            "panel": "data/gaia_astrometry_panel_deep_benchmark.json",
            "live_pooled_pct": 0.022461,
        },
        {
            "id": "PRED-083",
            "name": "paleoclimate_class_hold",
            "domain": "Paleoclimate_Panel",
            "tier_hint": "C",
            "fsot_predicted": 0.5,
            "unit": "pooled_median_error_pct_ceiling",
            "sota_baseline": 10.0,
            "sota_label": "GCM paleo surrogate per-epoch retune",
            "discriminant": "within_green_gate_0_5pct",
            "kill_if": "paleoclimate_panel pooled median exceeds 0.5% on ice-core / paleo class refresh",
            "future_survey": "Open paleoclimate / ice-core class refreshes",
            "what_it_is": "Millennial climate class (20 rec / 0.006%; extension 40 / 0.015%). Distinct from PRED-054 NCEI.",
            "what_it_is_not": "A named-year drought date.",
            "panel": "data/paleoclimate_panel_benchmark.json",
            "live_pooled_pct": 0.006006,
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
            "fsot": "Solved as sectors of one fluid, not two cosmologies. Bridge 70.75 ≠ JWST Perfect Host 73.49 (local ladder). Fair bridge compare is CCHP TRGB / dual-anchor. See docs/OBJECT_SCORING.md.",
            "status": "solved_residual",
            "pred_ids": ["PRED-001", "PRED-024", "PRED-051"],
        },
        {
            "id": "Q-S8-01",
            "field": "cosmology",
            "question": "S8 tension (Planck vs weak lensing)?",
            "community": "Open. Euclid DR1 is the next independent drop.",
            "fsot": "PRED-002 / PRED-042 lock 0.805. DES Y6 alone 0.789 is a tension row; joint DES+CMB+low-z 0.806 is the fair compare (arXiv:2601.14559). Euclid DR1 Nov 2026 still awaiting. CLOE is synthetic.",
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
            "fsot": "Genetics freeze 2026-08-17 quoted in the hub: product 0.13 Å vs AF 0.47 Å vs cryo-EM FSC ~1.2 Å vs bulk ~13 Å — do not cross-cite. Engine stays Genetics. CASP/CAMEO blind is OPEN (docs/CASP_CAMEO_BLIND_PROTOCOL.md). Zebrafish 0.358% stays inside 0.5%.",
            "status": "sibling_owned",
            "pred_ids": ["PRED-055"],
        },
        {
            "id": "Q-ECON-01",
            "field": "economics",
            "question": "Is a market a different medium from a neural net?",
            "community": "Econophysics vs institutional economics.",
            "fsot": "As-above-so-below. Same World Bank YoY on Economics and Neuroscience folds; |S_E/S_N| vs 5/4. Siloed 0.129% panel is not retuned.",
            "status": "solved_residual",
            "pred_ids": [],
        },
        {
            "id": "Q-TIDE-01",
            "field": "oceanography",
            "question": "Are coastal water levels only astronomical harmonics, or a fluid pressure cell?",
            "community": "NOAA CO-OPS harmonics are the operational standard; storm surge is added statistically.",
            "fsot": "PRED-065 residual hold 0.030%. Dated 48 h surge windows (residual vs harmonic, threshold = POOF m) under PRED-064. Not a beat of the harmonic table at every minute.",
            "status": "preregistered",
            "pred_ids": ["PRED-065", "PRED-064"],
        },
        {
            "id": "Q-HYDRO-01",
            "field": "hydrology",
            "question": "Can floods be windowed like earthquakes (pressure loads, then POOF)?",
            "community": "USGS NWIS stage + NWS flood watches; hydrologic models are catchment-specific.",
            "fsot": "PRED-078 two-sector valve (load bar = 1+POOF). Dated 7-day NWIS gage windows under PRED-064. Not street-level inundation.",
            "status": "preregistered",
            "pred_ids": ["PRED-078", "PRED-064"],
        },
        {
            "id": "Q-GEO-01",
            "field": "geomagnetism",
            "question": "Can geomagnetic storms be issued as dated windows, not only Kp thresholds?",
            "community": "SWPC Kp/Dst watches; coupling to F10.7 / IMF is statistical.",
            "fsot": "Classifiers already solved (Q-SOL-02). New dated issues emit Kp≥5 72 h windows when the valve is loading (PRED-064). First issue 2026-08-25 locked quiet Kp<5 and stays frozen.",
            "status": "preregistered",
            "pred_ids": ["PRED-059", "PRED-062", "PRED-064"],
        },
        {
            "id": "Q-GW-01",
            "field": "gravitational_waves",
            "question": "Are chirp-mass and event-rate classes one compact-object fluid?",
            "community": "GWTC catalogs; rates still model-dependent; siren H0 is sparse.",
            "fsot": "PRED-067 chirp-mass class. PRED-077 siren H0 70.024 mid-sector — do not retune ρ onto SH0ES.",
            "status": "preregistered",
            "pred_ids": ["PRED-048", "PRED-067", "PRED-077"],
        },
        {
            "id": "Q-FRB-01",
            "field": "fast_radio_bursts",
            "question": "Does FRB DM excess track the same bubble density as H0 sectors?",
            "community": "IGM-only DM vs host/bubble excess still debated; CHIME catalog growing.",
            "fsot": "FRBs are BH→WH orifice outgassing (PRED-084): repeaters = saloon-door post-POOF, one-shots = paper-rip. Energy = width×fluence vs e·POOF (37/37). Activity season T=5π+1/φ days vs FRB20180916B 16.35 d. 200·(1+sky_density) is REMEDIED_WRONG_APPLY (~66%, retired). PRED-052 keeps the 200 class. PRED-076 is angular grammar only.",
            "status": "preregistered",
            "pred_ids": ["PRED-052", "PRED-076", "PRED-084"],
        },
        {
            "id": "Q-EXO-01",
            "field": "exoplanets",
            "question": "Is radius–period–insolation architecture one planetary fold?",
            "community": "Formation channels (core accretion vs disk instability) still a zoo.",
            "fsot": "PRED-066 architecture class hold. CAT-EXO 0.023%. Not one ε per planet.",
            "status": "preregistered",
            "pred_ids": ["PRED-066"],
        },
        {
            "id": "Q-GBIF-01",
            "field": "ecology",
            "question": "Is species-occurrence structure a second biosphere law?",
            "community": "SDMs and occupancy models; no single counting law.",
            "fsot": "PRED-068 occurrence-class hold (240 rec / 0.006%). Acoustic-ecology counting on D=15. Not a county arrival date.",
            "status": "preregistered",
            "pred_ids": ["PRED-068"],
        },
        {
            "id": "Q-EPI-01",
            "field": "epidemiology",
            "question": "Are epidemic waves a different physics from other counting processes?",
            "community": "Compartmental models (SIR/SEIR); wave timing remains hard.",
            "fsot": "PRED-069 class hold (24 rec / 0.015%). Same POOF/SUCTION counting as GR b-value. Not a city outbreak date.",
            "status": "preregistered",
            "pred_ids": ["PRED-069"],
        },
        {
            "id": "Q-ICE-01",
            "field": "cryosphere",
            "question": "Is ice-mass loss a seasonal valve on the same ocean/air fluid?",
            "community": "GRACE/GRACE-FO mass; ice-sheet models vs observation still offset.",
            "fsot": "PRED-080 GravIS |delta| APPLY residual (scalar median 0.023%). Decline classifier stays 100% match. Not a calving date.",
            "status": "preregistered",
            "pred_ids": ["PRED-080"],
        },
        {
            "id": "Q-AG-01",
            "field": "agriculture",
            "question": "Is growing-season / yield class the same viscosity as ecology and hydrology?",
            "community": "Agroecology field surveys and USDA yield models; season class is statistical, not a first-principles valve.",
            "fsot": "PRED-081 season-class residual (276 rec / 0.018%) on D=16. Not county bushels next Tuesday.",
            "status": "preregistered",
            "pred_ids": ["PRED-081"],
        },
        {
            "id": "Q-GAIA-01",
            "field": "astrometry",
            "question": "Is Gaia parallax / proper-motion structure a second astrometry law, or the same ladder-adjacent fold?",
            "community": "Gaia DR3/DR4 reprocesses; distance-ladder papers often treat astrometry as a separate reduction.",
            "fsot": "PRED-082 parallax class (deep 0.022%; CAT-GAIA-DR3 3459 / 0.022%). Not a new H0 from one star.",
            "status": "preregistered",
            "pred_ids": ["PRED-082"],
        },
        {
            "id": "Q-PALEO-01",
            "field": "paleoclimate",
            "question": "Is millennial climate a different physics from the station-climate fluid (PRED-054)?",
            "community": "GCM paleo surrogates vs ice-core reconstructions; millennial vs instrumental often siloed.",
            "fsot": "PRED-083 millennial class on D=17 Atmospheric_Physics (20 rec / 0.006%). Distinct from PRED-054 NCEI. Not a named-year drought date.",
            "status": "preregistered",
            "pred_ids": ["PRED-083"],
        },
        {
            "id": "Q-CKM-01",
            "field": "particle",
            "question": "Are CKM/PMNS angles predicted or fitted SM inputs?",
            "community": "CKM from global fits; PMNS from oscillation experiments; SM does not predict the mixings.",
            "fsot": "PRED-070–075 promote V_ud, V_tb, δ_CKM, sin²θ12, sin²θ13, α_s(M_Z) from the Higgs/flavor layer. Kill = next PDG combination outside 0.5%.",
            "status": "preregistered",
            "pred_ids": ["PRED-070", "PRED-071", "PRED-072", "PRED-073", "PRED-074", "PRED-075"],
        },
        {
            "id": "Q-FIN-01",
            "field": "finance",
            "question": "Can the model pick next-day prices or a crash date?",
            "community": "EMH vs factor models; crash timing is not a solved forecast.",
            "fsot": "Not claimed. World Bank YoY class residuals only. A ticker as a 0.5% central is a kill.",
            "status": "honest_refusal",
            "pred_ids": [],
        },
        {
            "id": "Q-MED-01",
            "field": "clinical_medicine",
            "question": "Can the model predict an individual's diagnosis or onset date?",
            "community": "Risk scores and trials; person-level onset remains clinical, not a ToE central.",
            "fsot": "Not claimed. Immunology/cardiology class residuals and the 20.00 W observer lock only.",
            "status": "honest_refusal",
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
        "purpose": "Map questions scientists currently argue about onto FSOT folds: already gated, preregistered, next-layer expansion, refused, or sibling-owned.",
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
        "Earth: structure + neighborhood bubble, not one number. Dated *windows*",
        "exist (PRED-064); clock-time hypocenters do not.",
        "",
        "**Refresh:** `python scripts/build_earth_system_prediction_layer.py`",
        "",
        "## What we will not claim",
        "",
        "- A clock-time and single hypocenter for the next large earthquake or VEI≥4 eruption.",
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
        "| `next_layer` | Green catalog exists; no hand PRED / dated window yet |",
        "| `honest_refusal` | The model does **not** claim this (S2S NWP beat, prices, diagnoses) |",
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
        "[`PREDICTION_EXPANSION_MAP.md`](PREDICTION_EXPANSION_MAP.md) ·",
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
