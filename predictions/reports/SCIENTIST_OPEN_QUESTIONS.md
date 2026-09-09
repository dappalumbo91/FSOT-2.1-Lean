# Scientist open questions → FSOT folds

*Generated 2026-09-08T00:37:18.739034+00:00 · pin D1D38A*

This is a **discovery ledger**, not a trophy wall. Each row is a question
working scientists actually argue about. Status is one of:

| Status | Meaning |
|--------|---------|
| `solved_residual` | Already gated on a named public table |
| `preregistered` | Frozen PRED with a kill; waiting on a catalog/paper |
| `next_layer` | Green catalog exists; no hand PRED / dated window yet |
| `honest_refusal` | The model does **not** claim this (S2S NWP beat, prices, diagnoses) |
| `sibling_owned` | Genetics/Quantum live freeze, not this hub's product |
| `open_residual` | Domain is green but the interconnect is still thin |

Counts: {'preregistered': 23, 'solved_residual': 4, 'honest_refusal': 3, 'sibling_owned': 1}

| ID | Field | Question | Community | FSOT | Status | PREDs |
|----|-------|----------|-----------|------|--------|-------|
| `Q-EQ-01` | seismology | Can we predict the time and place of the next large earthquake? | No deterministic short-term prediction; probabilistic hazard (Gutenberg–Richter, ETAS, CSE). | Not a clock-time hypocenter. Dated *windows* on live pressure cells (PRED-064): location + 7-day POOF window, scored after valid_to. | **preregistered** | PRED-056, PRED-064 |
| `Q-EQ-02` | seismology | Why is the global b-value ≈ 1? | Empirical Gutenberg–Richter; regional 0.6–1.4; physical origin debated. | b = φ − 1/φ = 1. Acoustic counting in the crustal fluid. PRED-056 literature band 0.90–1.10. | **preregistered** | PRED-056 |
| `Q-EQ-03` | seismology | Are slow slip and fast earthquakes two different physics? | Moment-duration scaling linear vs cubic still contested; no unifying constitutive law. | One T3 valve: POOF = fast, SUCTION = slow. Viscosity continuum. PRED-057. | **preregistered** | PRED-057 |
| `Q-EQ-04` | seismology | Lab acoustics vs Earth PREM — same wave? | Often siloed (ultrasonics vs global Earth models). | Already residual-gated: mafic/lid vp/vs from ν=D_atomic/25. PRED-061. | **solved_residual** | PRED-061 |
| `Q-VOLC-01` | volcanology | Can we predict eruption onset dates? | Unrest monitoring (InSAR, SO2, seismicity); no reliable date forecast. | Not a clock-time. Volcanic USGS cells get 14-day POOF windows (PRED-064) plus GVP residual hold PRED-058. | **preregistered** | PRED-058, PRED-064 |
| `Q-SOL-01` | solar_space_weather | What will the solar-cycle amplitude be (one SSN)? | Cycle 25 panel said ~115 (Jul 2025); cycle ran stronger. Amplitude remains hard. | Not one number — quiet vs storm sectors of one valve (same grammar as H0). PRED-062. Do not relock Cycle 25 SSN after the peak. | **preregistered** | PRED-062, PRED-059, PRED-007 |
| `Q-SOL-02` | solar_space_weather | Can Kp/Dst be classified from first principles rather than decoupled heuristics? | Empirical Kp/Dst thresholds; coupling to F10.7 / IMF is statistical. | Already green classifiers + PRED-007 ionospheric β. Hold PRED-059 on SWPC refresh. | **solved_residual** | PRED-007, PRED-059 |
| `Q-WX-01` | weather_climate | Is ENSO a separate oscillator from the rest of the fluid? | Coupled ocean-atmosphere modes; S2S skill is the operational frontier. | κ(Oceanography, Atmospheric_Physics, Fluid_Dynamics). Residual holds PRED-060/063/054. Not an ECMWF-beating week-3 forecast. | **preregistered** | PRED-060, PRED-063, PRED-054 |
| `Q-WX-02` | weather_climate | Can FSOT beat numerical weather prediction at S2S? | S2S is an active WMO/NOAA program; skill drops after ~2 weeks. | Not claimed. Class residuals on NDBC/NCEI only. Individual storm tracks are T1 look, not a new H0. | **honest_refusal** | — |
| `Q-H0-01` | cosmology | Why do Planck and SH0ES disagree on H0? | Hubble tension; new physics vs systematics. | Solved as sectors of one fluid, not two cosmologies. Bridge 70.75 ≠ JWST Perfect Host 73.49 (local ladder). Fair bridge compare is CCHP TRGB / dual-anchor. See docs/OBJECT_SCORING.md. | **solved_residual** | PRED-001, PRED-024, PRED-051 |
| `Q-S8-01` | cosmology | S8 tension (Planck vs weak lensing)? | Open. Euclid DR1 is the next independent drop. | PRED-002 / PRED-042 lock 0.805. DES Y6 alone 0.789 is a tension row; joint DES+CMB+low-z 0.806 is the fair compare (arXiv:2601.14559). Euclid DR1 Nov 2026 still awaiting. CLOE is synthetic. | **preregistered** | PRED-002, PRED-042 |
| `Q-LI-01` | cosmology_nuclear | Cosmological lithium problem? | BBN vs halo-star Li gap ~factor 3. | PRED-005 factor 2.85. Nuclear orifice already dual-routed (PRED nuclear levels). | **preregistered** | PRED-005 |
| `Q-G2-01` | particle | Muon g-2 excess? | Experiment vs lattice SM still moving. | PRED-004/050 same-sign lock. Do not retune after lattice papers. | **preregistered** | PRED-004, PRED-050 |
| `Q-HIGGS-01` | particle | Is m_H an input or a prediction? | SM input; measured ~125.25 GeV. | PRED-049 hold vs next PDG combination at 0.5%. | **preregistered** | PRED-049 |
| `Q-GEN-01` | biology | Can sequence-only models beat measured-map folds? | AlphaFold-class interpolators; wet-lab structures still the product. | Genetics freeze 2026-08-17 quoted in the hub: product 0.13 Å vs AF 0.47 Å vs cryo-EM FSC ~1.2 Å vs bulk ~13 Å — do not cross-cite. Engine stays Genetics. CASP/CAMEO blind is OPEN (docs/CASP_CAMEO_BLIND_PROTOCOL.md). Zebrafish 0.358% stays inside 0.5%. | **sibling_owned** | PRED-055 |
| `Q-ECON-01` | economics | Is a market a different medium from a neural net? | Econophysics vs institutional economics. | As-above-so-below. Same World Bank YoY on Economics and Neuroscience folds; |S_E/S_N| vs 5/4. Siloed 0.129% panel is not retuned. | **solved_residual** | — |
| `Q-TIDE-01` | oceanography | Are coastal water levels only astronomical harmonics, or a fluid pressure cell? | NOAA CO-OPS harmonics are the operational standard; storm surge is added statistically. | PRED-065 residual hold 0.030%. Dated 48 h surge windows (residual vs harmonic, threshold = POOF m) under PRED-064. Not a beat of the harmonic table at every minute. | **preregistered** | PRED-065, PRED-064 |
| `Q-HYDRO-01` | hydrology | Can floods be windowed like earthquakes (pressure loads, then POOF)? | USGS NWIS stage + NWS flood watches; hydrologic models are catchment-specific. | PRED-078 two-sector valve (load bar = 1+POOF). Dated 7-day NWIS gage windows under PRED-064. Not street-level inundation. | **preregistered** | PRED-078, PRED-064 |
| `Q-GEO-01` | geomagnetism | Can geomagnetic storms be issued as dated windows, not only Kp thresholds? | SWPC Kp/Dst watches; coupling to F10.7 / IMF is statistical. | Classifiers already solved (Q-SOL-02). New dated issues emit Kp≥5 72 h windows when the valve is loading (PRED-064). First issue 2026-08-25 locked quiet Kp<5 and stays frozen. | **preregistered** | PRED-059, PRED-062, PRED-064 |
| `Q-GW-01` | gravitational_waves | Are chirp-mass and event-rate classes one compact-object fluid? | GWTC catalogs; rates still model-dependent; siren H0 is sparse. | PRED-067 chirp-mass class. PRED-077 siren H0 70.024 mid-sector — do not retune ρ onto SH0ES. | **preregistered** | PRED-048, PRED-067, PRED-077 |
| `Q-FRB-01` | fast_radio_bursts | Does FRB DM excess track the same bubble density as H0 sectors? | IGM-only DM vs host/bubble excess still debated; CHIME catalog growing. | FRBs are BH→WH orifice outgassing (PRED-084): repeaters = saloon-door post-POOF, one-shots = paper-rip. Energy = width×fluence vs e·POOF (37/37). Activity season T=5π+1/φ days vs FRB20180916B 16.35 d. 200·(1+sky_density) is REMEDIED_WRONG_APPLY (~66%, retired). PRED-052 keeps the 200 class. PRED-076 is angular grammar only. | **preregistered** | PRED-052, PRED-076, PRED-084 |
| `Q-EXO-01` | exoplanets | Is radius–period–insolation architecture one planetary fold? | Formation channels (core accretion vs disk instability) still a zoo. | PRED-066 architecture class hold. CAT-EXO 0.023%. Not one ε per planet. | **preregistered** | PRED-066 |
| `Q-GBIF-01` | ecology | Is species-occurrence structure a second biosphere law? | SDMs and occupancy models; no single counting law. | PRED-068 occurrence-class hold (240 rec / 0.006%). Acoustic-ecology counting on D=15. Not a county arrival date. | **preregistered** | PRED-068 |
| `Q-EPI-01` | epidemiology | Are epidemic waves a different physics from other counting processes? | Compartmental models (SIR/SEIR); wave timing remains hard. | PRED-069 class hold (24 rec / 0.015%). Same POOF/SUCTION counting as GR b-value. Not a city outbreak date. | **preregistered** | PRED-069 |
| `Q-ICE-01` | cryosphere | Is ice-mass loss a seasonal valve on the same ocean/air fluid? | GRACE/GRACE-FO mass; ice-sheet models vs observation still offset. | PRED-080 GravIS |delta| APPLY residual (scalar median 0.023%). Decline classifier stays 100% match. Not a calving date. | **preregistered** | PRED-080 |
| `Q-AG-01` | agriculture | Is growing-season / yield class the same viscosity as ecology and hydrology? | Agroecology field surveys and USDA yield models; season class is statistical, not a first-principles valve. | PRED-081 season-class residual (276 rec / 0.018%) on D=16. Not county bushels next Tuesday. | **preregistered** | PRED-081 |
| `Q-GAIA-01` | astrometry | Is Gaia parallax / proper-motion structure a second astrometry law, or the same ladder-adjacent fold? | Gaia DR3/DR4 reprocesses; distance-ladder papers often treat astrometry as a separate reduction. | PRED-082 parallax class (deep 0.022%; CAT-GAIA-DR3 3459 / 0.022%). Not a new H0 from one star. | **preregistered** | PRED-082 |
| `Q-PALEO-01` | paleoclimate | Is millennial climate a different physics from the station-climate fluid (PRED-054)? | GCM paleo surrogates vs ice-core reconstructions; millennial vs instrumental often siloed. | PRED-083 millennial class on D=17 Atmospheric_Physics (20 rec / 0.006%). Distinct from PRED-054 NCEI. Not a named-year drought date. | **preregistered** | PRED-083 |
| `Q-CKM-01` | particle | Are CKM/PMNS angles predicted or fitted SM inputs? | CKM from global fits; PMNS from oscillation experiments; SM does not predict the mixings. | PRED-070–075 promote V_ud, V_tb, δ_CKM, sin²θ12, sin²θ13, α_s(M_Z) from the Higgs/flavor layer. Kill = next PDG combination outside 0.5%. | **preregistered** | PRED-070, PRED-071, PRED-072, PRED-073, PRED-074, PRED-075 |
| `Q-FIN-01` | finance | Can the model pick next-day prices or a crash date? | EMH vs factor models; crash timing is not a solved forecast. | Not claimed. World Bank YoY class residuals only. A ticker as a 0.5% central is a kill. | **honest_refusal** | — |
| `Q-MED-01` | clinical_medicine | Can the model predict an individual's diagnosis or onset date? | Risk scores and trials; person-level onset remains clinical, not a ToE central. | Not claimed. Immunology/cardiology class residuals and the 20.00 W observer lock only. | **honest_refusal** | — |

Related: [`EARTH_SYSTEM_PREDICTIONS.md`](EARTH_SYSTEM_PREDICTIONS.md) ·
[`PREDICTION_EXPANSION_MAP.md`](PREDICTION_EXPANSION_MAP.md) ·
[`PREDICTION_TIERS.md`](PREDICTION_TIERS.md) · [`../EXPLAINED.md`](../EXPLAINED.md)

Refresh: `python scripts/build_earth_system_prediction_layer.py`
