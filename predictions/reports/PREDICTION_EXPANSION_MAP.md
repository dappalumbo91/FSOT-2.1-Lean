# Prediction expansion map

*Generated 2026-09-09T22:33:43.878711+00:00 · pin D1D38A*

Green residual catalogs are **not** automatically predictions. A prediction
is a named lock with a public catalog, a place or class, a calendar window
or survey drop, and a kill. This is the directory of **remaining** slots
given the domains this hub already covers.

**Refresh:** `python scripts/build_prediction_expansion_map.py`

## Already locked (do not re-litigate)

| Surface | Status |
|---------|--------|
| Hand PREDs | **77** (A 29 / C 26 / D 22) |
| Catalog layer | **35** (MPCORB, Gaia, DESI, GWTC, PubChem, exo, climate) |
| Higgs + flavor | **33** (all inside literature-tight band) |
| Dated fluid issue | **2026-08-25 frozen**; **2026-09-09** issued (do not rewrite) |
| Closed-window scores | hold **65** · kill **45** · awaiting **4**; score 09-09 after valid_to |
| Nearest cosmology drop | Euclid DR1-Foundation **2026-11-12** (PRED-042/043) |
| Family-tree remaining gap | Genetics / zebrafish **sibling-owned** |

Issue/score loop stays `python scripts/issue_earth_fluid_forecasts.py` then
`python scripts/score_earth_fluid_forecasts.py`. Never rewrite
`predictions/dated_forecasts/2026-08-25_issue.json`.

## How to expand (same grammar as H0 and PRED-064)

1. **Dated window** — pressure cell + calendar window + score after `valid_to`.
2. **Survey / class hold** — named observable vs a public catalog refresh.
3. **Bridge** — same bubble/valve across two messengers (FRB×density, siren×H0 sector).
4. **Calendar watch** — already frozen; score when the drop lands.
5. **Wait / refuse** — Genetics sibling; S2S vs ECMWF; clock-time hypocenter; prices; diagnoses; Tier D headlines.

Slots **25** · actionable **16** · styles `{'dated_window': 5, 'survey_class': 9, 'bridge': 3, 'calendar_watch': 2, 'wait_sibling': 1, 'honest_refusal': 5}`.

## Wave 1 — more dated fluid windows (highest checkable ROI)

Same kernel \(R_\oplus\cdot\mathrm{POOF}/25 \approx 39.1\,\mathrm{km}\), same
horizons (EQ 7 d / WX 48 h / solar 72 h / volcanic 14 d). This is the
playbook already frozen in [`WEATHER_MONITORING_APPROACH.md`](../../docs/WEATHER_MONITORING_APPROACH.md).

| ID | Domain | Next prediction | Catalog | Ready? | Not |
|----|--------|-----------------|---------|:------:|-----|
| `EXP-TIDE-01` | NOAA_Coastal_Tides | Score 48 h surge windows after valid_to. Do not rewrite issued files. | NOAA CO-OPS harmonic + observed (already in noaa_coastal_tides_benchmark.json) | ready_live_catalog | Beating NOAA's own harmonic tide tables at every minute. Those are T1 look. |
| `EXP-GEO-01` | Geomagnetism | Score each solar window vs SWPC after 72 h. Do not rewrite 2026-08-25. | NOAA SWPC Kp / Dst (already ingested for the 2026-08-25 solar cell) | ready_live_catalog | Flare time-of-arrival for a named active region. Cycle 25 SSN pick. |
| `EXP-WX-BASIN-01` | Meteorology / Oceanography / Fluid_Dynamics | Score 48 h NDBC realtime2 after valid_to. Do not rewrite 2026-08-25. | NDBC realtime (895 rows on 2026-08-25 issue; PRED-060/063 residual) | ready_live_catalog | ECMWF week-3 S2S beat. Individual hurricane track. |
| `EXP-VOLC-CELLS-01` | Volcanology_Panel | Score 14 d USGS volcanic/explosion windows. Do not rewrite 2026-08-25. | Smithsonian GVP + USGS volcano feeds (PRED-058 residual 0.0235%) | ready_live_catalog | Clock-time of the next VEI≥4 eruption. |
| `EXP-HYDRO-01` | Hydrology | Score hydro windows after valid_to. Do not rewrite issued files. | USGS NWIS daily values (hydrology_benchmark.json, 957 records) | ready_live_catalog | Street-level inundation maps. A 0.5% central on one gauge's next-hour stage. |

## Wave 2 — catalog-class PREDs (green panels with no hand PRED)

| ID | Domain | Records / % | Next prediction | Kill | Not |
|----|--------|-------------|-----------------|------|-----|
| `EXP-EXO-01` | Exoplanet_System_Architecture | 882 architecture / 1976 archive / 0.0 / 0.023 | Hold ≤0.5% on NASA archive refresh. Not one ε per planet. | Architecture pooled > 0.5% on NASA archive refresh, or a per-planet fitted ε. | The discovery date of the next transiting Earth analog. |
| `EXP-GW-01` | Compact_Object_Binary_Events | 1972 GWTC / 40 compact-object / 0.0085 / 0.010 | Hold ≤0.5% on GWTC O4/O5. Sirens stay mid-sector. | GWTC pooled > 0.5%; siren H0 forced onto the SH0ES class bin. | The GPS time of the next binary-black-hole merger. |
| `EXP-GBIF-01` | GBIF_Species_Occurrence | 240 / 0.006 | Hold ≤0.5% on GBIF dump refresh. Not a county arrival date. | GBIF pooled > 0.5% on named dump refresh. | The date a named species arrives in a new county. |
| `EXP-EPI-01` | Epidemiology_Panel | 24 / 0.015 | Hold ≤0.5% on World Bank / WHO refresh. Not a city outbreak date. | Panel pooled > 0.5% on refresh. | The start date of the next named outbreak in a named city. |
| `EXP-ICE-01` | Cryosphere / Grace_Cryosphere | 2399 classifier / 0.0 (not a scalar residual) | Hold ≤0.5% on GravIS refresh. Dual-fold D=16 vs Planetary_Science D=21 stays an honest APPLY residual. | Fitted mass-loss coefficient; stuffing classifier 0% as if it were a mass residual. | The calendar day the next ice shelf calves. |
| `EXP-AG-01` | Agriculture_Agroecology | gap-fill panel / 0.018 | Hold ≤0.5% on GBIF / World Bank agriculture refresh. Not county bushels. | Panel pooled > 0.5%; post-hoc yield retune. | County bushels next Tuesday. |
| `EXP-GAIA-01` | Gaia_Astrometry_Panel_Deep | 3459 CAT + 62 deep / 0.022 | Hold ≤0.5% on Gaia DR4 / DR3 reprocess. Not a new H0 from one star. | Pooled > 0.5% on DR4; one free ε per Gaia source. | A new H0 from one star. |
| `EXP-PALEO-01` | Paleoclimate_Panel | 20 + 40 extension / 0.006 / 0.015 | Hold ≤0.5% on ice-core / paleo class refresh. Not a named-year drought date. | Panel pooled > 0.5% on refresh; per-epoch GCM retune. | A named-year drought date. |

## Wave 3 — multi-messenger and flavor bridges

Distinctive ToE signature: one valve across messengers. Deepen or promote;
do not invent a second H0.

| ID | Domain | Next prediction | Kill |
|----|--------|-----------------|------|
| `EXP-FRB-01` | Cosmology / Particle_Astrophysics | Hold the shared kernel on CHIME refresh. Do not 0.5%-gate the 10-row seed. | CHIME high-DM class outside 0.5% of frozen central on catalog refresh. |
| `EXP-SIREN-01` | Astronomy / Cosmology | Score each public siren vs 70.024. Do not retune ρ onto 73.04. | Forcing the siren onto 73.04, or retuning ρ. |
| `EXP-CKM-01` | Particle_Physics / TOE_CKM_PMNS_Flavor | Kill = next PDG combination outside 0.5%. No per-channel ε. | Next PDG combination outside 0.5% of freeze; per-channel ε. |
| `EXP-MPCORB-CLASS-01` | MPCORB_Minor_Planet_Catalog | Named dynamical-class residual holds (NEA vs MBA). Impact windows stay T1 unless a real POOF cell exists. | Catalog pooled > 0.5%; one free ε per designation. |

## Wave 4 — calendar watches (already registered)

Do not invent new cosmology centrals. Score Euclid / Rubin / LVK against the SHA.

| ID | Domain | Drop | Lock |
|----|--------|------|------|
| `EXP-EUCLID-01` | Cosmology | Euclid DR1-Foundation 12 Nov 2026; full WL mid-2027 | PRED-002, PRED-042, PRED-043, PRED-044, PRED-046, PRED-047 registered. |
| `EXP-RUBIN-01` | Cosmology / Astronomy | Rubin LSST Early DP2 (target ~2026-10-01) | PRED-044 pathfinder lock. |

## Wave 5 — wait (sibling)

- `EXP-GEN-WAIT` — Biology / Zebrafish_Developmental_Mechanics: Migrate when the Genetics freeze is handed over. Do not densify here.

## Wave 6 — do not expand as headline

| ID | Temptation | Why not |
|----|------------|---------|
| `EXP-REFUSE-S2S` | Can FSOT beat ECMWF at S2S week 3–4? | Anything that sounds like replacing ECMWF. |
| `EXP-REFUSE-CLOCK` | Clock-time + single hypocenter as a 0.5% central? | Replacing a USGS/NWS watch. |
| `EXP-REFUSE-FIN` | Next-day prices / a crash date? | Beating the market. |
| `EXP-REFUSE-DX` | Individual diagnosis or onset dates? | Clinical decision support. |
| `EXP-REFUSE-TIERD` | Cold fusion, superheavy Z islands, transporter, warp portal as public ToE scoreboard? | Unpublished tech numerics (registry is names-only). |

## Recommended next build (when you say go)

1. **Shipped:** Waves 1–3 through PRED-083; D11 orifice-scale triangulation;
   uniqueness attractor Lean; CHIME Cat-2 dump (3390) as catalog class,
   orifice classifier stays frozen 37/37; catalog-class refresh 12/12;
   FSOT-Materials sibling (fuels first freeze).
2. **Next:** Score 2026-09-09 after valid_to (weather ~11 Sep, EQ/hydro 16 Sep).
   Next dated issue carries fold + potentials. Do not rewrite issued JSON.
3. Genetics stays sibling-owned. Euclid stays a watch.
   Architecture_Building_Science densify held (already 0.079%, no new table).

Kill for this map: treating it as a request for more free parameters, or
leading public claims with Wave 6.

Related: [`SCIENTIST_OPEN_QUESTIONS.md`](SCIENTIST_OPEN_QUESTIONS.md) ·
[`NEXT_LAYERS.md`](../NEXT_LAYERS.md) ·
[`DATED_FLUID_FORECASTS.md`](DATED_FLUID_FORECASTS.md) ·
[`../../docs/DOMAIN_FAMILY_TREE.md`](../../docs/DOMAIN_FAMILY_TREE.md)
