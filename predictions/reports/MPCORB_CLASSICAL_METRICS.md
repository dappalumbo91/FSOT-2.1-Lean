# MPCORB classical metrics (field-standard)

*Generated 2026-08-06T14:12:24.143338+00:00 · objects **1,554,101***

Classical minor-planet work measures **astrometric O–C RMS in arcseconds**, orbit quality **U**, and element consistency — **not** a single pooled residual % across the whole catalog under one free-parameter-free operator.

This report adds those standard metrics **on top of** the existing FSOT residual %.

## Dual scoreboard

| Metric | Value | Unit / meaning |
|--------|------:|----------------|
| **Classical median RMS** | **0.76** | arcsec (MPC orbit-fit O–C RMS) |
| Classical p95 RMS | 0.98 | arcsec |
| Classical median \|Δn\|/n (Kepler) | 1.5875572596619725e-08 | fractional |
| Classical median Kepler error | 1.5875572596619725e-06 | % of n |
| **FSOT pooled median residual** | **0.023015** | % (seed engine; separate metric) |

Report both. Classical = field-standard arcsec / fractional integrity. FSOT = seed-engine catalog residual %. Different units, complementary claims.

## Classical RMS residual (arcsec)

Objects with RMS field: **1,554,079** / 1,554,101

| Stat | RMS (arcsec) |
|------|-------------:|
| min | 0.0 |
| p05 | 0.19 |
| p25 | 0.41 |
| median | 0.76 |
| p75 | 0.87 |
| p95 | 0.98 |
| p99 | 1.07 |
| mean | 0.6555534371161311 |
| max | 9.99 |

### Context bands (literature survey classes)

Approximate modern survey RMS classes for **well-observed** objects (not a claim that every MPCORB object matches them):

| Band | Arcsec | Count in catalog |
|------|--------|-----------------:|
| panstarrs_class_well_observed (0.12–0.25) | 0.12–0.25 | 87255 |
| modern_ccd_survey_typical (0.25–0.5) | 0.25–0.5 | 399201 |
| mixed_survey_class (0.5–0.8) | 0.5–0.8 | 345832 |
| older_photographic_class (1.0–3.0) | 1.0–3.0 | 61167 |
| sub-0.12 arcsec | <0.12 | 33980 |
| ≥1 arcsec | ≥1 | 61184 |

## U (uncertainty parameter) distribution

| U / flag | Count |
|----------|------:|
| 0 | 1110250 |
| 1 | 109553 |
| 2 | 73617 |
| 3 | 38848 |
| 4 | 31029 |
| 5 | 33603 |
| 6 | 34884 |
| 7 | 38229 |
| 8 | 40882 |
| 9 | 32777 |
| flag_D | 31 |
| flag_E | 1151 |
| missing | 9247 |

### Median RMS by U (where available)

| U | n | median RMS (arcsec) | p95 |
|---|--:|--------------------:|----:|
| 0 | 1110250 | 0.82 | 0.99 |
| 1 | 109553 | 0.4 | 0.8600000000000001 |
| 2 | 73617 | 0.39 | 0.8399999999999999 |
| 3 | 38848 | 0.34 | 0.92 |
| 4 | 31029 | 0.52 | 1.04 |
| 5 | 33603 | 0.63 | 1.07 |
| 6 | 34884 | 0.54 | 1.03 |
| 7 | 38229 | 0.46 | 0.99 |
| 8 | 40882 | 0.33 | 0.92 |
| 9 | 32777 | 0.18 | 0.77 |

## RMS by observation count tier

| Tier | n | median RMS | p95 |
|------|--:|-----------:|----:|
| obs_10_49 | 450139 | 0.41 | 0.97 |
| obs_200_999 | 398745 | 0.86 | 0.95 |
| obs_50_199 | 554177 | 0.71 | 1.01 |
| obs_ge_1000 | 122751 | 0.78 | 0.87 |
| obs_lt_10 | 28267 | 0.2 | 1.0 |

## Kepler element integrity (fractional Δn/n)

Two-body check: mean motion from semi-major axis vs catalog `n`. Best objects in the literature reach fractional element precision at 10⁻⁶–10⁻⁸; the full catalog has a long tail.

| Stat | \|Δn\|/n | as % |
|------|--------:|-----:|
| median | 1.5875572596619725e-08 | 1.5875572596619725e-06 |
| p95 | 4.110597706047307e-08 | 4.110597706047307e-06 |
| p99 | 4.9873025312305525e-08 | 4.987302531230553e-06 |
| mean | 2.4534994175588536e-08 | 2.453499417558854e-06 |

## By orbital regime

| Regime | n (rms) | med RMS (arcsec) | med Kepler % |
|--------|--------:|-----------------:|-------------:|
| distant | 7105 | 0.17 | 8.118495650911454e-05 |
| main_belt | 1438149 | 0.77 | 1.541930291044905e-06 |
| neo | 42079 | 0.61 | 2.2373116543722344e-06 |
| other | 40893 | 0.72 | 1.9986959224327274e-06 |
| outer_belt | 25853 | 0.75 | 2.555148007704372e-06 |

## FSOT companion (unchanged metric)

- FSOT pooled median residual %: **0.023015**
- FSOT structural median %: None
- Objects (FSOT bench): 1554101

FSOT residual % is a separate metric (seed engine / channel stack). Classical RMS arcsec is the field-standard residual unit.

## Metric definitions

- **rms_arcsec:** MPCORB orbit-fit r.m.s. residual in arcseconds — classical astrometric O–C RMS stored by the MPC for each object.
- **U:** MPC uncertainty parameter 0–9 (0 best). Special flags D/E/F when present.
- **frac_dn_over_n:** Two-body Kepler consistency: |n_Kepler(a) − n_catalog| / n_catalog. Fractional element-level integrity check (not a free fit).
- **kepler_error_pct:** 100 × frac_dn_over_n (percent form of the same integrity check).
- **fsot_pooled_pct:** Separate metric from build_mpcorb_fsot_benchmark.py — zero-parameter FSOT channel/domain residual. Not a substitute for rms_arcsec.
- **not_included:** Full epoch-by-epoch O–C re-reduction from raw observation files is not in MPCORB alone; that would require the observation archive.

Refresh: `python scripts/build_mpcorb_classical_metrics.py`

FSOT residual builder (separate): `python scripts/build_mpcorb_fsot_benchmark.py`
