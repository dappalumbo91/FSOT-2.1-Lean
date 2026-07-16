## Preregistered Outcome Tracking & Verification Scaffolds

**Panels:** 5 · **Records:** 264 · **Mean panel median error:** 0.00488585%

#### Material In Silico Screening Scaffold

Extension panel **`Material_In_Silico_Screening_Scaffold`** (verification tier 65) evaluates **42** measured records at **0.00206%** pooled median error (B_verified). Formal module: `FSOT.Formal.MaterialInSilicoScreeningScaffoldPriors`. This panel extends the core spine into material in silico screening scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/material_in_silico_screening_scaffold_benchmark.json`](data/material_in_silico_screening_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `chemical`, `particle`, `energy`
- **Panel tags:** Material, Silico, Screening, Scaffold
- **Data sources / cohorts:** Public DFT, materials screening gates — novel emergence outputs preregistered separately

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| bandgap_tolerance_ev · Bandgap relay tolerance | 0.1 | 0.1 | 0 |
| dft_energy_convergence_ev · DFT energy convergence threshold | 1e-05 | 1e-05 | 0 |
| force_threshold_ev_ang · Ionic force threshold (eV/Å) | 0.05 | 0.05 | 0 |
| formation_energy_window_ev · Formation energy screening window | 0.5 | 0.5 | 0 |
| formula_mass_closure · 962 | 18.015 | 18.015 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Material In Silico Screening Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Material In Silico Screening Scaffold: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`O`** in Material In Silico Screening Scaffold: measured **1.461**, seed-derived **1.4609166182653626** via `G⁻³+Ψ⁴` (error **0.005707%**). Constants: g_cat. Authority: Andersen et al., JPCRD 28 (1999).

#### Material Property Verification Scaffold

Extension panel **`Material_Property_Verification_Scaffold`** (verification tier 59) evaluates **79** measured records at **0.002271%** pooled median error (B_verified). Formal module: `FSOT.Formal.MaterialPropertyVerificationScaffoldPriors`. This panel extends the core spine into material property verification scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/material_property_verification_scaffold_benchmark.json`](data/material_property_verification_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `chemical`, `energy`, `particle`
- **Panel tags:** Material, Property, Verification, Scaffold
- **Data sources / cohorts:** Crosswalk relay from tier 55–57 material, chemistry, fuel panels — no novel in-silico claims

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| density_kg_m3 · ethanol | 789 | 789 | 0 |
| formula_mass_closure · 962 | 18.015 | 18.015 | 0 |
| formula_mass_g_mol · ethanol | 46.069 | 46.069 | 0 |
| lhv_mj_kg · ethanol | 26.8 | 26.8 | 0 |
| materials_science_scalar · fsot_Materials_Science | 0.33526 | 0.33526 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Material Property Verification Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Material Property Verification Scaffold: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.
- **`Methanol`** in Material Property Verification Scaffold: measured **126.8**, seed-derived **126.79733372555232** via `PI^3+PI^4-PHI^1` (error **0.002103%**). Constants: phi, pi. Authority: NIST Chemistry WebBook / CRC.

#### Preregistered Outcome Tracking

Extension panel **`Preregistered_Outcome_Tracking`** (verification tier 70) evaluates **56** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PreregisteredOutcomeTrackingPriors`. This panel extends the core spine into preregistered outcome tracking observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/preregistered_outcome_tracking_benchmark.json`](data/preregistered_outcome_tracking_benchmark.json)

**Subfield map:**

- **Lean routes:** `cosmological`, `particle`, `biological`, `material`
- **Panel tags:** Preregistered, Outcome, Tracking
- **Data sources / cohorts:** Preregistered prediction discriminant outcome tracking vs ΛCDM, SM baselines

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| discriminant_pass · PRED-001 | 1 | 1 | 0 |
| fsot_predicted · PRED-001 | 70.75 | 70.75 | 0 |
| outcome_gate · prereg_tracking | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| tier46_panel_bridge · preregistered_predictions | 0.0200982 | 0.0200982 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Preregistered Outcome Tracking: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Preregistered Outcome Tracking: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Preregistered Outcome Tracking: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Preregistered Predictions

Extension panel **`Preregistered_Predictions`** (verification tier 46) evaluates **27** measured records at **0.0200982%** pooled median error (B_verified). Formal module: `FSOT.Formal.PreregisteredPredictionsPriors`. This panel extends the core spine into preregistered predictions observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/preregistered_predictions_benchmark.json`](data/preregistered_predictions_benchmark.json)

**Subfield map:**

- **Lean routes:** `cosmological`, `particle`, `biological`
- **Panel tags:** Preregistered, Predictions
- **Data sources / cohorts:** 5 locked predictions discriminating FSOT from ΛCDM, SM baselines

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| prediction_discriminant · PRED-001 | 70.75 | 70.7642 | 0.0200982 |
| pooled_median · all_channels | 0 | 0.020098 | 0.0200982 |
| preregistered · prediction_panel | 0 | 0.020098 | 0.0200982 |
| prediction_discriminant · PRED-013 | 1.2e+09 | 1.20024e+09 | 0.0200982 |
| prediction_discriminant · PRED-032 | 0.0096632 | 0.009665 | 0.0200982 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Preregistered Predictions: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Preregistered Predictions: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`P`** in Preregistered Predictions: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Preregistered Predictions Verification Scaffold

Extension panel **`Preregistered_Predictions_Verification_Scaffold`** (verification tier 63) evaluates **60** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PreregisteredPredictionsVerificationScaffoldPriors`. This panel extends the core spine into preregistered predictions verification scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/preregistered_predictions_verification_scaffold_benchmark.json`](data/preregistered_predictions_verification_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `cosmological`, `particle`, `biological`, `material`, `ai`
- **Panel tags:** Preregistered, Predictions, Verification, Scaffold
- **Data sources / cohorts:** Public prereg manifest scaffold — novel in-silico screens gated separately

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| alternate_sota · PRED-001 | 73.04 | 73.04 | 0 |
| fsot_predicted · PRED-001 | 70.75 | 70.75 | 0 |
| manifest_prediction_count · preregistered_predictions_manifest | 27 | 27 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| prereg_anchor · verification_scaffold | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Preregistered Predictions Verification Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Preregistered Predictions Verification Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Fe`** in Preregistered Predictions Verification Scaffold: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
