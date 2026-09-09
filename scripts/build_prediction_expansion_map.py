#!/usr/bin/env python3
"""Prediction expansion map — where the next dated / survey PREDs can go.

Green residual catalogs are not automatically predictions. A prediction is a
named lock with a public catalog, a location or class, a calendar window or
survey drop, and a kill. This map is the directory of *remaining* expansion
slots given the domains we already cover.

Refresh: python scripts/build_prediction_expansion_map.py
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRED = ROOT / "predictions"
OUT_JSON = PRED / "prediction_expansion_map.json"
OUT_MD = PRED / "reports" / "PREDICTION_EXPANSION_MAP.md"

PIN = "D1D38A"


def _row(
    *,
    id: str,
    wave: int,
    style: str,
    domain: str,
    d_eff: int | None,
    question: str,
    catalog: str,
    already: str,
    next_pred: str,
    kill: str,
    not_claim: str,
    readiness: str,
    records: str,
    pooled_pct: str,
) -> dict:
    return {
        "id": id,
        "wave": wave,
        "style": style,
        "domain": domain,
        "D_eff": d_eff,
        "question": question,
        "catalog": catalog,
        "already": already,
        "next_pred": next_pred,
        "kill": kill,
        "not_claim": not_claim,
        "readiness": readiness,
        "records": records,
        "pooled_pct": pooled_pct,
    }


def slots() -> list[dict]:
    """Ranked expansion slots. Wave 1 = same PRED-064 grammar, checkable now."""
    return [
        # ── Wave 1: dated fluid windows (same kernel / valve as PRED-064) ──
        _row(
            id="EXP-TIDE-01",
            wave=1,
            style="dated_window",
            domain="NOAA_Coastal_Tides",
            d_eff=17,
            question="Do coastal water-level cells load and release on the same 39.1 km / φ⁴ grammar as weather?",
            catalog="NOAA CO-OPS harmonic + observed (already in noaa_coastal_tides_benchmark.json)",
            already="PRED-065 residual hold. Dated surge windows: score bar = POOF m; issue bar = POOF·(1+POOF). SF 8.5 mm miss would not re-issue.",
            next_pred="Score 48 h surge windows after valid_to. Do not rewrite issued files.",
            kill="Issued window rewritten, or scored hit rate abandoned; residual > 0.5% on CO-OPS refresh.",
            not_claim="Beating NOAA's own harmonic tide tables at every minute. Those are T1 look.",
            readiness="ready_live_catalog",
            records="20",
            pooled_pct="0.030",
        ),
        _row(
            id="EXP-GEO-01",
            wave=1,
            style="dated_window",
            domain="Geomagnetism",
            d_eff=13,
            question="Can Kp/Dst storms be issued as dated windows, not only a quiet-vs-storm classifier?",
            catalog="NOAA SWPC Kp / Dst (already ingested for the 2026-08-25 solar cell)",
            already="PRED-007/059/062 classifiers. 2026-08-25 locked quiet Kp<5. New issues emit Kp≥5 when loading.",
            next_pred="Score each solar window vs SWPC after 72 h. Do not rewrite 2026-08-25.",
            kill="Quiet and storm collapse to one residual sector, or issued Kp windows never scored.",
            not_claim="Flare time-of-arrival for a named active region. Cycle 25 SSN pick.",
            readiness="ready_live_catalog",
            records="524 + SWPC stream",
            pooled_pct="0.0 classifier / PRED-059 hold",
        ),
        _row(
            id="EXP-WX-BASIN-01",
            wave=1,
            style="dated_window",
            domain="Meteorology / Oceanography / Fluid_Dynamics",
            d_eff=16,
            question="Do NDBC storm cells exist outside the Arctic, on the same three-tank bleed?",
            catalog="NDBC realtime (895 rows on 2026-08-25 issue; PRED-060/063 residual)",
            already="2026-08-25 Arctic cells frozen. New issues pick one loaded cell per ocean basin.",
            next_pred="Score 48 h NDBC realtime2 after valid_to. Do not rewrite 2026-08-25.",
            kill="Storm and quiet NDBC classes become one residual; issued windows rewritten.",
            not_claim="ECMWF week-3 S2S beat. Individual hurricane track.",
            readiness="ready_live_catalog",
            records="150+ NDBC tanks; 895 live on last issue",
            pooled_pct="0.026–0.030 interconnect",
        ),
        _row(
            id="EXP-VOLC-CELLS-01",
            wave=1,
            style="dated_window",
            domain="Volcanology_Panel",
            d_eff=18,
            question="Are other GVP unrest cells the same 14-day POOF window as Volcano Islands?",
            catalog="Smithsonian GVP + USGS volcano feeds (PRED-058 residual 0.0235%)",
            already="PRED-058 residual. 2026-08-25 Volcano Islands frozen. New issues merge USGS volcanic-eruption events, up to 4 cells.",
            next_pred="Score 14 d USGS volcanic/explosion windows. Do not rewrite 2026-08-25.",
            kill="GVP residual > 0.5%; issued volcanic windows never scored.",
            not_claim="Clock-time of the next VEI≥4 eruption.",
            readiness="ready_live_catalog",
            records="GVP panel + USGS volcanic cells",
            pooled_pct="0.0235",
        ),
        _row(
            id="EXP-HYDRO-01",
            wave=1,
            style="dated_window",
            domain="Hydrology",
            d_eff=15,
            question="Do river-stage / flood cells load and POOF the same way as crustal EQ cells?",
            catalog="USGS NWIS daily values (hydrology_benchmark.json, 957 records)",
            already="PRED-078 two-sector valve. Dated 7-day NWIS gage windows (load bar = 1+POOF).",
            next_pred="Score hydro windows after valid_to. Do not rewrite issued files.",
            kill="Issued flood window rewritten; or stuffing a fitted β onto stage.",
            not_claim="Street-level inundation maps. A 0.5% central on one gauge's next-hour stage.",
            readiness="ready_live_catalog",
            records="957 (classifier panel today)",
            pooled_pct="0.0 (not a scalar residual)",
        ),
        # ── Wave 2: catalog-class PREDs (named survey/lab kills, already green) ──
        _row(
            id="EXP-EXO-01",
            wave=2,
            style="survey_class",
            domain="Exoplanet_System_Architecture",
            d_eff=21,
            question="Is radius–period–insolation architecture one D=21 planetary fold, not a zoo of formation laws?",
            catalog="NASA Exoplanet Archive (CAT-EXO residual + architecture panel 882 records)",
            already="PRED-066 architecture class hold. CAT-EXO 0.023%.",
            next_pred="Hold ≤0.5% on NASA archive refresh. Not one ε per planet.",
            kill="Architecture pooled > 0.5% on NASA archive refresh, or a per-planet fitted ε.",
            not_claim="The discovery date of the next transiting Earth analog.",
            readiness="ready_green_panel",
            records="882 architecture / 1976 archive",
            pooled_pct="0.0 / 0.023",
        ),
        _row(
            id="EXP-GW-01",
            wave=2,
            style="survey_class",
            domain="Compact_Object_Binary_Events",
            d_eff=24,
            question="Are chirp-mass / event-rate classes one compact-object fluid, not a new H0?",
            catalog="GWOSC / GWTC (CAT-GWTC 1972 rec / 0.0085%; compact-object panel 40 rec / 0.010%)",
            already="PRED-067 chirp-mass class + PRED-048 panel + siren tool row 70.024.",
            next_pred="Hold ≤0.5% on GWTC O4/O5. Sirens stay mid-sector.",
            kill="GWTC pooled > 0.5%; siren H0 forced onto the SH0ES class bin.",
            not_claim="The GPS time of the next binary-black-hole merger.",
            readiness="ready_green_panel",
            records="1972 GWTC / 40 compact-object",
            pooled_pct="0.0085 / 0.010",
        ),
        _row(
            id="EXP-GBIF-01",
            wave=2,
            style="survey_class",
            domain="GBIF_Species_Occurrence",
            d_eff=15,
            question="Is occurrence-field structure acoustic-ecology counting, not a second biosphere law?",
            catalog="GBIF occurrence dumps (240 records / 0.006%)",
            already="PRED-068 occurrence-class hold (240 rec / 0.006%).",
            next_pred="Hold ≤0.5% on GBIF dump refresh. Not a county arrival date.",
            kill="GBIF pooled > 0.5% on named dump refresh.",
            not_claim="The date a named species arrives in a new county.",
            readiness="ready_green_panel",
            records="240",
            pooled_pct="0.006",
        ),
        _row(
            id="EXP-EPI-01",
            wave=2,
            style="survey_class",
            domain="Epidemiology_Panel",
            d_eff=15,
            question="Are epidemic waves POOF/SUCTION class counts (same as GR b-value), not a new pathogen law?",
            catalog="World Bank / WHO neonatal and incidence series (24 records / 0.015%)",
            already="PRED-069 class hold (24 rec / 0.015%).",
            next_pred="Hold ≤0.5% on World Bank / WHO refresh. Not a city outbreak date.",
            kill="Panel pooled > 0.5% on refresh.",
            not_claim="The start date of the next named outbreak in a named city.",
            readiness="ready_green_panel",
            records="24",
            pooled_pct="0.015",
        ),
        _row(
            id="EXP-ICE-01",
            wave=2,
            style="survey_class",
            domain="Cryosphere / Grace_Cryosphere",
            d_eff=16,
            question="Is ice-mass loss a seasonal SUCTION/POOF valve on the same fluid as ocean/air tanks?",
            catalog="Cryosphere panel 2399 rec (classifier today) + GRACE cryosphere extension",
            already="PRED-080 GravIS |delta| APPLY residual (scalar median 0.023%). Decline classifier 100% match.",
            next_pred="Hold ≤0.5% on GravIS refresh. Dual-fold D=16 vs Planetary_Science D=21 stays an honest APPLY residual.",
            kill="Fitted mass-loss coefficient; stuffing classifier 0% as if it were a mass residual.",
            not_claim="The calendar day the next ice shelf calves.",
            readiness="needs_scalar_densify",
            records="2399 classifier",
            pooled_pct="0.0 (not a scalar residual)",
        ),
        _row(
            id="EXP-AG-01",
            wave=2,
            style="survey_class",
            domain="Agriculture_Agroecology",
            d_eff=16,
            question="Is growing-season / yield class the same viscosity as ecology and hydrology?",
            catalog="Agriculture agroecology gap-fill + GBIF",
            already="PRED-081 season-class hold (276 rec / 0.018%).",
            next_pred="Hold ≤0.5% on GBIF / World Bank agriculture refresh. Not county bushels.",
            kill="Panel pooled > 0.5%; post-hoc yield retune.",
            not_claim="County bushels next Tuesday.",
            readiness="ready_green_panel",
            records="gap-fill panel",
            pooled_pct="0.018",
        ),
        _row(
            id="EXP-GAIA-01",
            wave=2,
            style="survey_class",
            domain="Gaia_Astrometry_Panel_Deep",
            d_eff=20,
            question="Is Gaia parallax / proper-motion structure the same ladder-adjacent fold, not a second astrometry law?",
            catalog="Gaia DR3 public sample (CAT-GAIA-DR3 3459 / 0.022%) + deep panel 62 / 0.022%",
            already="PRED-082 parallax class hold. CAT-GAIA-DR3 residual already locked.",
            next_pred="Hold ≤0.5% on Gaia DR4 / DR3 reprocess. Not a new H0 from one star.",
            kill="Pooled > 0.5% on DR4; one free ε per Gaia source.",
            not_claim="A new H0 from one star.",
            readiness="ready_green_panel",
            records="3459 CAT + 62 deep",
            pooled_pct="0.022",
        ),
        _row(
            id="EXP-PALEO-01",
            wave=2,
            style="survey_class",
            domain="Paleoclimate_Panel",
            d_eff=17,
            question="Is millennial climate a different physics from the NCEI station-climate fluid?",
            catalog="Paleoclimate panel 20 rec / 0.006% + extension 40 rec / 0.015%",
            already="PRED-083 millennial class hold. Distinct from PRED-054 NCEI.",
            next_pred="Hold ≤0.5% on ice-core / paleo class refresh. Not a named-year drought date.",
            kill="Panel pooled > 0.5% on refresh; per-epoch GCM retune.",
            not_claim="A named-year drought date.",
            readiness="ready_green_panel",
            records="20 + 40 extension",
            pooled_pct="0.006 / 0.015",
        ),
        # ── Wave 3: multi-messenger / flavor bridges (distinctive ToE signature) ──
        _row(
            id="EXP-FRB-01",
            wave=3,
            style="bridge",
            domain="Cosmology / Particle_Astrophysics",
            d_eff=25,
            question="Does FRB DM excess track the same bubble-density grammar as H0 sectors?",
            catalog="CHIME/FRB catalog (PRED-052 200 pc cm⁻³ excess class; WATCH-CHIME-FRB)",
            already="PRED-076 same-kernel as H0. PRED-052 200 class. 10-row 200*(1+dens) residual ~70% not stuffed.",
            next_pred="Hold the shared kernel on CHIME refresh. Do not 0.5%-gate the 10-row seed.",
            kill="CHIME high-DM class outside 0.5% of frozen central on catalog refresh.",
            not_claim="The UTC of the next FRB.",
            readiness="deepen_existing_pred",
            records="CHIME catalog continuous",
            pooled_pct="PRED-052 freeze",
        ),
        _row(
            id="EXP-SIREN-01",
            wave=3,
            style="bridge",
            domain="Astronomy / Cosmology",
            d_eff=25,
            question="Do GW standard sirens land mid-sector (~70), not on the SH0ES class bin?",
            catalog="LVK / GWOSC sirens; PRED-H0-gw_standard_siren = 70.024",
            already="PRED-077 = 70.024 mid-sector (same as PRED-H0-gw_standard_siren).",
            next_pred="Score each public siren vs 70.024. Do not retune ρ onto 73.04.",
            kill="Forcing the siren onto 73.04, or retuning ρ.",
            not_claim="A new H0 from one event.",
            readiness="deepen_existing_pred",
            records="sparse sirens",
            pooled_pct="tool row 70.024",
        ),
        _row(
            id="EXP-CKM-01",
            wave=3,
            style="bridge",
            domain="Particle_Physics / TOE_CKM_PMNS_Flavor",
            d_eff=5,
            question="Are CKM/PMNS angles predicted (unitarity from the seed) or fitted SM inputs?",
            catalog="PDG CKM/PMNS + Higgs branching layer (17 Higgs + 16 flavor companions, all inside tight band)",
            already="PRED-070–075 hand locks (V_ud, V_tb, δ, sin²θ12, sin²θ13, α_s). Flavor layer still the tight band.",
            next_pred="Kill = next PDG combination outside 0.5%. No per-channel ε.",
            kill="Next PDG combination outside 0.5% of freeze; per-channel ε.",
            not_claim="A new generation of quarks. Superheavy Z-island headlines (Tier D).",
            readiness="promote_existing_layer",
            records="33 Higgs/flavor PREDs",
            pooled_pct="all beat literature-tight",
        ),
        _row(
            id="EXP-MPCORB-CLASS-01",
            wave=3,
            style="survey_class",
            domain="MPCORB_Minor_Planet_Catalog",
            d_eff=21,
            question="Do NEA / MBA / KBO classes share one orbital fluid, not one ε per asteroid?",
            catalog="MPC / IAU MPCORB (~1.55M records / 0.023%)",
            already="PRED-CAT-MPCORB-RESIDUAL + Kepler scalar locks. No NEA-class dated impact PRED.",
            next_pred="Named dynamical-class residual holds (NEA vs MBA). Impact windows stay T1 unless a real POOF cell exists.",
            kill="Catalog pooled > 0.5%; one free ε per designation.",
            not_claim="The impact date of a named NEA as a 0.5% central.",
            readiness="deepen_existing_pred",
            records="1,554,101",
            pooled_pct="0.023",
        ),
        # ── Wave 4: calendar-bound cosmology (already registered — watch, don't invent) ──
        _row(
            id="EXP-EUCLID-01",
            wave=4,
            style="calendar_watch",
            domain="Cosmology",
            d_eff=25,
            question="Does Euclid DR1 S8 land on the 0.805 bridge (PRED-002/042)?",
            catalog="Euclid DR1-Foundation 12 Nov 2026; full WL mid-2027",
            already="PRED-002, PRED-042, PRED-043, PRED-044, PRED-046, PRED-047 registered.",
            next_pred="Score in results/ when the products land. Do not retune the SHA.",
            kill="S8 outside the Planck–DES-class band; wa sign flip vs −1.018.",
            not_claim="A new cosmology because one catalog bin is noisy.",
            readiness="wait_for_drop",
            records="Tier A already frozen",
            pooled_pct="locks 0.805 / wa −1.018",
        ),
        _row(
            id="EXP-RUBIN-01",
            wave=4,
            style="calendar_watch",
            domain="Cosmology / Astronomy",
            d_eff=25,
            question="Does Rubin early DP2 pathfinder S8 stay on the same bridge?",
            catalog="Rubin LSST Early DP2 (target ~2026-10-01)",
            already="PRED-044 pathfinder lock.",
            next_pred="Score pathfinder; do not invent a second S8.",
            kill="Pathfinder S8 outside 0.5% of 0.805 when a consensus number exists.",
            not_claim="Full LSST year-10 cosmology from DP2 images.",
            readiness="wait_for_drop",
            records="PRED-044",
            pooled_pct="0.805",
        ),
        # ── Wait / sibling ──
        _row(
            id="EXP-GEN-WAIT",
            wave=5,
            style="wait_sibling",
            domain="Biology / Zebrafish_Developmental_Mechanics",
            d_eff=12,
            question="Can sequence-only models beat measured-map folds?",
            catalog="FSOT-Genetics sibling freeze 2026-08-17 (0.13 Å vs AF 0.47 Å)",
            already="PRED-055 residual hold. Hub D_eff metadata fixed to 12. Residual 0.358% left honest.",
            next_pred="Migrate when the Genetics freeze is handed over. Do not densify here.",
            kill="LSQ a new f to hide 0.358%; claiming sequence-only AF-beating from this hub.",
            not_claim="A hub product until the sibling freeze lands.",
            readiness="sibling_owned",
            records="20 zebrafish",
            pooled_pct="0.358",
        ),
        # ── Honest refusals (do not expand as headline PREDs) ──
        _row(
            id="EXP-REFUSE-S2S",
            wave=6,
            style="honest_refusal",
            domain="Meteorology",
            d_eff=16,
            question="Can FSOT beat ECMWF at S2S week 3–4?",
            catalog="WMO S2S / NWP ensembles",
            already="Q-WX-02 honest refusal. NDBC/NCEI class residuals only.",
            next_pred="None. Weather sibling may ingest NWP later; still not a beat-claim.",
            kill="Marketing an S2S beat.",
            not_claim="Anything that sounds like replacing ECMWF.",
            readiness="do_not_expand",
            records="—",
            pooled_pct="—",
        ),
        _row(
            id="EXP-REFUSE-CLOCK",
            wave=6,
            style="honest_refusal",
            domain="Seismology",
            d_eff=18,
            question="Clock-time + single hypocenter as a 0.5% central?",
            catalog="USGS ComCat",
            already="PRED-064 windowed cells. First issue 8 EQ windows through 2026-09-01.",
            next_pred="Keep windows. Always-on sibling shortens dt. Never a 0.5% clock-time.",
            kill="Rewriting issued JSON; scoring a clock-time as if it were the central.",
            not_claim="Replacing a USGS/NWS watch.",
            readiness="do_not_expand",
            records="299 ComCat on last issue",
            pooled_pct="PRED-056 b=1 band",
        ),
        _row(
            id="EXP-REFUSE-FIN",
            wave=6,
            style="honest_refusal",
            domain="Economics / Finance_Markets",
            d_eff=20,
            question="Next-day prices / a crash date?",
            catalog="World Bank YoY already dual-routed (econ 0.026% interconnect; siloed 0.129% not retuned)",
            already="Q-ECON-01 solved as as-above-so-below. No price PRED.",
            next_pred="None. Class residuals only.",
            kill="A ticker forecast as a 0.5% central.",
            not_claim="Beating the market.",
            readiness="do_not_expand",
            records="157 Economics / 172 Econometrics",
            pooled_pct="0.129 siloed / 0.026 interconnect",
        ),
        _row(
            id="EXP-REFUSE-DX",
            wave=6,
            style="honest_refusal",
            domain="Clinical_Medicine / Cardiology / Oncology",
            d_eff=14,
            question="Individual diagnosis or onset dates?",
            catalog="ClinicalTrials / cardiology / immunology panels (green residuals)",
            already="Class residuals. Consciousness 20.003601 vs 20.0 W (0.018%) is the observer lock.",
            next_pred="None at the person. Species / panel class only.",
            kill="A named-patient date as a PRED.",
            not_claim="Clinical decision support.",
            readiness="do_not_expand",
            records="clinical / immunology panels",
            pooled_pct="green class only",
        ),
        _row(
            id="EXP-REFUSE-TIERD",
            wave=6,
            style="honest_refusal",
            domain="Tier D scaffolds",
            d_eff=None,
            question="Cold fusion, superheavy Z islands, transporter, warp portal as public ToE scoreboard?",
            catalog="PRED-009…023, 032–033, 036, 038–041 registered as scaffold",
            already="22 Tier D hand PREDs. Keep labeled.",
            next_pred="Do not expand as headline until A–C are saturated.",
            kill="Leading X with Tier D as if equal to Euclid / PRED-064.",
            not_claim="Unpublished tech numerics (registry is names-only).",
            readiness="do_not_expand",
            records="22 hand PREDs",
            pooled_pct="scaffold",
        ),
    ]


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    items = slots()
    counts = Counter(str(x["style"]) for x in items)
    wave_counts = Counter(int(x["wave"]) for x in items)
    ready = [x for x in items if str(x["readiness"]) in {
        "ready_live_catalog", "ready_green_panel", "promote_existing_layer", "deepen_existing_pred",
    }]

    doc = {
        "generated_at": ts,
        "pin": PIN,
        "purpose": (
            "Directory of remaining prediction expansions given domains already "
            "green in this hub. Not 400 new theories. Same 25-D fluid; new "
            "interfaces that already have public catalogs and kill criteria."
        ),
        "policy": [
            "dated_window_not_clock_time",
            "do_not_rewrite_issued_forecasts",
            "no_s2s_claim_vs_ecmwf",
            "no_posthoc_cycle25_ssn",
            "no_unpublished_tech_numerics",
            "genetics_wait_for_sibling_freeze",
            "tier_d_stay_labeled",
            "do_not_stuff_shoes_1pct_into_0_5pct",
        ],
        "already_locked_summary": {
            "hand_preds": 76,
            "tier_A_hand": 28,
            "tier_C_hand": 26,
            "tier_D_hand": 22,
            "catalog_layer_preds": 35,
            "higgs_flavor_preds": 33,
            "dated_issue": "2026-08-25 frozen; 2026-09-01 uses loading M≥4.5 / quiet-hold; tide issue bar POOF·(1+POOF) on next issues",
            "next_score_windows": {
                "weather": "2026-09-03",
                "solar": "2026-09-04",
                "earthquake": "2026-09-08",
                "volcanic": "2026-09-08",
            },
            "nearest_cosmology_drop": "Euclid DR1-Foundation 2026-11-12",
            "playbook_retro": "results/dated_forecast_scores/RULE_RETRO.md",
        },
        "style_counts": dict(counts),
        "wave_counts": {str(k): v for k, v in sorted(wave_counts.items())},
        "n_slots": len(items),
        "n_actionable": len(ready),
        "slots": items,
    }
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    lines = [
        "# Prediction expansion map",
        "",
        f"*Generated {ts} · pin {PIN}*",
        "",
        "Green residual catalogs are **not** automatically predictions. A prediction",
        "is a named lock with a public catalog, a place or class, a calendar window",
        "or survey drop, and a kill. This is the directory of **remaining** slots",
        "given the domains this hub already covers.",
        "",
        "**Refresh:** `python scripts/build_prediction_expansion_map.py`",
        "",
        "## Already locked (do not re-litigate)",
        "",
        "| Surface | Status |",
        "|---------|--------|",
        "| Hand PREDs | **76** (A 28 / C 26 / D 22) |",
        "| Catalog layer | **35** (MPCORB, Gaia, DESI, GWTC, PubChem, exo, climate) |",
        "| Higgs + flavor | **33** (all inside literature-tight band) |",
        "| Dated fluid issue | **2026-08-25 frozen**; newer issues add basins / Kp≥5 / extra GVP / CO-OPS tides |",
        "| Closed-window scores | WX/tides/solar scored 2026-08-31 · EQ/hydro **2026-09-01** · volcanic **2026-09-08** |",
        "| Nearest cosmology drop | Euclid DR1-Foundation **2026-11-12** (PRED-042/043) |",
        "| Family-tree remaining gap | Genetics / zebrafish **sibling-owned** |",
        "",
        "Issue/score loop stays `python scripts/issue_earth_fluid_forecasts.py` then",
        "`python scripts/score_earth_fluid_forecasts.py`. Never rewrite",
        "`predictions/dated_forecasts/2026-08-25_issue.json`.",
        "",
        "## How to expand (same grammar as H0 and PRED-064)",
        "",
        "1. **Dated window** — pressure cell + calendar window + score after `valid_to`.",
        "2. **Survey / class hold** — named observable vs a public catalog refresh.",
        "3. **Bridge** — same bubble/valve across two messengers (FRB×density, siren×H0 sector).",
        "4. **Calendar watch** — already frozen; score when the drop lands.",
        "5. **Wait / refuse** — Genetics sibling; S2S vs ECMWF; clock-time hypocenter; prices; diagnoses; Tier D headlines.",
        "",
        f"Slots **{len(items)}** · actionable **{len(ready)}** · styles `{dict(counts)}`.",
        "",
        "## Wave 1 — more dated fluid windows (highest checkable ROI)",
        "",
        "Same kernel \(R_\\oplus\\cdot\\mathrm{POOF}/25 \\approx 39.1\\,\\mathrm{km}\), same",
        "horizons (EQ 7 d / WX 48 h / solar 72 h / volcanic 14 d). This is the",
        "playbook already frozen in [`WEATHER_MONITORING_APPROACH.md`](../../docs/WEATHER_MONITORING_APPROACH.md).",
        "",
        "| ID | Domain | Next prediction | Catalog | Ready? | Not |",
        "|----|--------|-----------------|---------|:------:|-----|",
    ]
    for x in items:
        if int(x["wave"]) != 1:
            continue
        lines.append(
            f"| `{x['id']}` | {x['domain']} | {x['next_pred']} | {x['catalog']} | "
            f"{x['readiness']} | {x['not_claim']} |"
        )

    lines += [
        "",
        "## Wave 2 — catalog-class PREDs (green panels with no hand PRED)",
        "",
        "| ID | Domain | Records / % | Next prediction | Kill | Not |",
        "|----|--------|-------------|-----------------|------|-----|",
    ]
    for x in items:
        if int(x["wave"]) != 2:
            continue
        lines.append(
            f"| `{x['id']}` | {x['domain']} | {x['records']} / {x['pooled_pct']} | "
            f"{x['next_pred']} | {x['kill']} | {x['not_claim']} |"
        )

    lines += [
        "",
        "## Wave 3 — multi-messenger and flavor bridges",
        "",
        "Distinctive ToE signature: one valve across messengers. Deepen or promote;",
        "do not invent a second H0.",
        "",
        "| ID | Domain | Next prediction | Kill |",
        "|----|--------|-----------------|------|",
    ]
    for x in items:
        if int(x["wave"]) != 3:
            continue
        lines.append(
            f"| `{x['id']}` | {x['domain']} | {x['next_pred']} | {x['kill']} |"
        )

    lines += [
        "",
        "## Wave 4 — calendar watches (already registered)",
        "",
        "Do not invent new cosmology centrals. Score Euclid / Rubin / LVK against the SHA.",
        "",
        "| ID | Domain | Drop | Lock |",
        "|----|--------|------|------|",
    ]
    for x in items:
        if int(x["wave"]) != 4:
            continue
        lines.append(
            f"| `{x['id']}` | {x['domain']} | {x['catalog']} | {x['already']} |"
        )

    lines += [
        "",
        "## Wave 5 — wait (sibling)",
        "",
    ]
    for x in items:
        if int(x["wave"]) != 5:
            continue
        lines.append(
            f"- `{x['id']}` — {x['domain']}: {x['next_pred']}"
        )

    lines += [
        "",
        "## Wave 6 — do not expand as headline",
        "",
        "| ID | Temptation | Why not |",
        "|----|------------|---------|",
    ]
    for x in items:
        if int(x["wave"]) != 6:
            continue
        lines.append(
            f"| `{x['id']}` | {x['question']} | {x['not_claim']} |"
        )

    lines += [
        "",
        "## Recommended next build (when you say go)",
        "",
        "1. **Shipped:** Waves 1–3 through PRED-083; D11 orifice-scale triangulation;",
        "   uniqueness attractor Lean; CHIME Cat-2 dump (3390) as catalog class,",
        "   orifice classifier stays frozen 37/37; catalog-class refresh 12/12;",
        "   FSOT-Materials sibling (fuels first freeze).",
        "2. **Next:** Score 2026-09-09 after valid_to (weather ~11 Sep, EQ/hydro 16 Sep).",
        "   Next dated issue carries fold + potentials. Do not rewrite issued JSON.",
        "3. Genetics stays sibling-owned. Euclid stays a watch.",
        "   Architecture_Building_Science densify held (already 0.079%, no new table).",
        "",
        "Kill for this map: treating it as a request for more free parameters, or",
        "leading public claims with Wave 6.",
        "",
        "Related: [`SCIENTIST_OPEN_QUESTIONS.md`](SCIENTIST_OPEN_QUESTIONS.md) ·",
        "[`NEXT_LAYERS.md`](../NEXT_LAYERS.md) ·",
        "[`DATED_FLUID_FORECASTS.md`](DATED_FLUID_FORECASTS.md) ·",
        "[`../../docs/DOMAIN_FAMILY_TREE.md`](../../docs/DOMAIN_FAMILY_TREE.md)",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"  slots={len(items)} actionable={len(ready)} styles={dict(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
