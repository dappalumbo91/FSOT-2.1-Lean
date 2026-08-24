# Scientist open questions → FSOT folds

*Generated 2026-08-24T23:45:42.584771+00:00 · pin D1D38A*

This is a **discovery ledger**, not a trophy wall. Each row is a question
working scientists actually argue about. Status is one of:

| Status | Meaning |
|--------|---------|
| `solved_residual` | Already gated on a named public table |
| `preregistered` | Frozen PRED with a kill; waiting on a catalog/paper |
| `honest_refusal` | The model does **not** claim this (dates, S2S NWP beat) |
| `sibling_owned` | Genetics/Quantum live freeze, not this hub's product |
| `open_residual` | Domain is green but the interconnect is still thin |

Counts: {'honest_refusal': 3, 'preregistered': 8, 'solved_residual': 3, 'sibling_owned': 1, 'open_residual': 1}

| ID | Field | Question | Community | FSOT | Status | PREDs |
|----|-------|----------|-----------|------|--------|-------|
| `Q-EQ-01` | seismology | Can we predict the time and place of the next large earthquake? | No deterministic short-term prediction; probabilistic hazard (Gutenberg–Richter, ETAS, CSE). | We also refuse dates. Class statistics only (PRED-056). Individual M≥7 is not a 0.5% object. | **honest_refusal** | PRED-056 |
| `Q-EQ-02` | seismology | Why is the global b-value ≈ 1? | Empirical Gutenberg–Richter; regional 0.6–1.4; physical origin debated. | b = φ − 1/φ = 1. Acoustic counting in the crustal fluid. PRED-056 literature band 0.90–1.10. | **preregistered** | PRED-056 |
| `Q-EQ-03` | seismology | Are slow slip and fast earthquakes two different physics? | Moment-duration scaling linear vs cubic still contested; no unifying constitutive law. | One T3 valve: POOF = fast, SUCTION = slow. Viscosity continuum. PRED-057. | **preregistered** | PRED-057 |
| `Q-EQ-04` | seismology | Lab acoustics vs Earth PREM — same wave? | Often siloed (ultrasonics vs global Earth models). | Already residual-gated: mafic/lid vp/vs from ν=D_atomic/25. PRED-061. | **solved_residual** | PRED-061 |
| `Q-VOLC-01` | volcanology | Can we predict eruption onset dates? | Unrest monitoring (InSAR, SO2, seismicity); no reliable date forecast. | Refuse dates. GVP catalog residual hold PRED-058. Eruption = POOF orifice (C10). | **honest_refusal** | PRED-058 |
| `Q-SOL-01` | solar_space_weather | What will the solar-cycle amplitude be (one SSN)? | Cycle 25 panel said ~115 (Jul 2025); cycle ran stronger. Amplitude remains hard. | Not one number — quiet vs storm sectors of one valve (same grammar as H0). PRED-062. Do not relock Cycle 25 SSN after the peak. | **preregistered** | PRED-062, PRED-059, PRED-007 |
| `Q-SOL-02` | solar_space_weather | Can Kp/Dst be classified from first principles rather than decoupled heuristics? | Empirical Kp/Dst thresholds; coupling to F10.7 / IMF is statistical. | Already green classifiers + PRED-007 ionospheric β. Hold PRED-059 on SWPC refresh. | **solved_residual** | PRED-007, PRED-059 |
| `Q-WX-01` | weather_climate | Is ENSO a separate oscillator from the rest of the fluid? | Coupled ocean-atmosphere modes; S2S skill is the operational frontier. | κ(Oceanography, Atmospheric_Physics, Fluid_Dynamics). Residual holds PRED-060/063/054. Not an ECMWF-beating week-3 forecast. | **preregistered** | PRED-060, PRED-063, PRED-054 |
| `Q-WX-02` | weather_climate | Can FSOT beat numerical weather prediction at S2S? | S2S is an active WMO/NOAA program; skill drops after ~2 weeks. | Not claimed. Class residuals on NDBC/NCEI only. Individual storm tracks are T1 look, not a new H0. | **honest_refusal** | — |
| `Q-H0-01` | cosmology | Why do Planck and SH0ES disagree on H0? | Hubble tension; new physics vs systematics. | Solved as sectors of one fluid, not two cosmologies. Class vs chain vs local cz/d. PRED-001 family. | **solved_residual** | PRED-001, PRED-024, PRED-051 |
| `Q-S8-01` | cosmology | S8 tension (Planck vs weak lensing)? | Open. Euclid DR1 is the next independent drop. | PRED-002 / PRED-042 lock 0.805 between Planck and DES. Watch Euclid Nov 2026. | **preregistered** | PRED-002, PRED-042 |
| `Q-LI-01` | cosmology_nuclear | Cosmological lithium problem? | BBN vs halo-star Li gap ~factor 3. | PRED-005 factor 2.85. Nuclear orifice already dual-routed (PRED nuclear levels). | **preregistered** | PRED-005 |
| `Q-G2-01` | particle | Muon g-2 excess? | Experiment vs lattice SM still moving. | PRED-004/050 same-sign lock. Do not retune after lattice papers. | **preregistered** | PRED-004, PRED-050 |
| `Q-HIGGS-01` | particle | Is m_H an input or a prediction? | SM input; measured ~125.25 GeV. | PRED-049 hold vs next PDG combination at 0.5%. | **preregistered** | PRED-049 |
| `Q-GEN-01` | biology | Can sequence-only models beat measured-map folds? | AlphaFold-class interpolators; wet-lab structures still the product. | Genetics sibling freeze 0.13 Å vs AF 0.47 Å. Hub waits for that freeze to migrate. Zebrafish 0.358% stays inside 0.5%. | **sibling_owned** | PRED-055 |
| `Q-ECON-01` | economics | Is a market a different medium from a neural net? | Econophysics vs institutional economics. | As-above-so-below. Economics pooled 0.129% still the largest social residual — next interconnect, not a fitted β. | **open_residual** | — |

Related: [`EARTH_SYSTEM_PREDICTIONS.md`](EARTH_SYSTEM_PREDICTIONS.md) ·
[`PREDICTION_TIERS.md`](PREDICTION_TIERS.md) · [`../EXPLAINED.md`](../EXPLAINED.md)

Refresh: `python scripts/build_earth_system_prediction_layer.py`
