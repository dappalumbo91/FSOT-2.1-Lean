# Scientific error metrics map (FSOT residuals → field language)

Generated: `2026-08-03T15:02:59.965687+00:00`

## Internal FSOT gate (unchanged)

- Pooled median relative error **≤ 0.5%**
- Classifier accuracy **≥ 99.5%** where applicable
- Margin health: **green 405/405**, fail **0**, worst scalar max **0.4989%** (`Phi_Morphogenetic_Scaling`)
- Nothing fell out: **True**

## Conversion anchors

| FSOT % residual | Fractional | ppm | Notes |
|-----------------|------------|-----|-------|
| 0.5 | 0.005 | 5000 | Green gate ceiling |
| 0.1 | 0.001 | 1000 | Strong continuous agreement |
| 0.01 | 0.0001 | 100 | Prefer ppm language |
| 0.001 | 1e-5 | 10 | Metrology-class relative error |

## Family rollup (median of domain pooled medians)

| Family | Domains | Green | Median % | Fractional | Field metric language |
|--------|--------:|------:|---------:|-----------:|----------------------|
| general_scientific | 179 | 179 | 0.0111155 | 0.000111155 | relative_percent_error |
| biology_medicine_genomics | 53 | 53 | 0.018019024892929635 | 0.00018019024892929633 | relative_percent_error |
| cosmology_astrophysics | 33 | 33 | 0.018002668701796783 | 0.00018002668701796784 | relative_percent_error |
| chemistry_materials | 32 | 32 | 0.0015412248894395779 | 1.541224889439578e-05 | relative_percent_error |
| formal_math_computation | 28 | 28 | 1.3580558531290437e-14 | 1.3580558531290438e-16 | relative_percent_error |
| engineering_propulsion_energy | 27 | 27 | 9.5e-05 | 9.5e-07 | relative_percent_error |
| earth_climate_geophysics | 20 | 20 | 0.0 | 0.0 | relative_percent_error |
| particle_nuclear_atomic | 18 | 18 | 0.013854616665746437 | 0.00013854616665746438 | relative_percent_error |
| social_econ_linguistics | 15 | 15 | 0.02261 | 0.00022610000000000002 | relative_percent_error |

## Field norms (how to publish)

### cosmology_astrophysics

- Primary: `relative_percent_error`
- Also: `fractional_residual`, `tension_sigma_proxy`
- Norm: Cosmology/astro results are usually quoted as percent-level or σ tension vs ΛCDM anchors (Planck H0, SH0ES). Fractional residual |c-m|/|m| is standard.

### particle_nuclear_atomic

- Primary: `relative_percent_error`
- Also: `ppm_when_sub_1e-4`, `absolute_residual`
- Norm: Particle/atomic constants often use relative uncertainty or ppm/ppb (CODATA/NIST). Percent is fine above ~0.01%; switch to ppm below.

### chemistry_materials

- Primary: `relative_percent_error`
- Also: `MAE_if_same_units`, `RMSE_if_available`
- Norm: Chemistry/materials properties commonly use % error vs handbook/CRC/NIST, or MAE/RMSE in physical units (e.g. kcal/mol, Å) when units are uniform.

### earth_climate_geophysics

- Primary: `relative_percent_error`
- Also: `bias`, `RMSE_proxy_from_pool`
- Norm: Geophysics/climate often report RMSE, bias, and anomaly correlation; relative % remains a cross-domain compression for multi-observable pools.

### biology_medicine_genomics

- Primary: `relative_percent_error`
- Also: `classifier_accuracy`, `AUC_proxy_if_classifier`
- Norm: Life sciences mix continuous biomarkers (% error / MAE) with classifiers (accuracy, F1, AUC). FSOT green gate already tracks classifier ≥99.5% where applicable.

### engineering_propulsion_energy

- Primary: `relative_percent_error`
- Also: `design_tolerance_band`
- Norm: Engineering specs use tolerance bands and % error vs measured performance (thrust, efficiency, impedance).

### social_econ_linguistics

- Primary: `relative_percent_error`
- Also: `MAPE`, `sMAPE`
- Norm: Economics/forecasting conventionally use MAPE/sMAPE; FSOT pooled median % is the MAPE-family cousin (median absolute percentage error style).

### formal_math_computation

- Primary: `relative_percent_error`
- Also: `exact_match_rate`, `bit_parity`
- Norm: Formal/computation layers emphasize exactness and parity; numeric residuals still use relative error when comparing derived scalars.

## Note

This map **does not retune** FSOT. It renames/annotates the same residuals so 
domain scientists see MAPE/fractional/ppm/σ-proxy language next to the green gate.

Machine-readable: `data\scientific_error_metrics_map.json`
Margin audit: `data\margin_health_audit.json`
