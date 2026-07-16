## Climate, Geoscience Depth & Applied Physics Panels

**Panels:** 15 · **Records:** 19,132 · **Mean panel median error:** 0.0130589%

#### Cartography GIS Panel

Extension panel **`Cartography_GIS_Panel`** (verification tier 82) evaluates **48** measured records at **0.018856%** pooled median error (B_verified). Formal module: `FSOT.Formal.CartographyGisPriors`. This panel extends the core spine into cartography gis panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/cartography_gis_panel_benchmark.json`](data/cartography_gis_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `economic`, `energy`
- **Panel tags:** Cartography, Gis, Panel
- **Data sources / cohorts:** Cartography, GIS — Natural Earth admin boundaries

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| bbox_width_deg · Argentina | 19.7871 | 19.7897 | 0.013003 |
| label_x · Argentina | -64.1733 | -64.1817 | 0.013003 |
| pooled_median · all_channels | 0 | 0.018856 | 0.018856 |
| fsot_prediction · cartography | 0 | 0.024709 | 0.024709 |
| label_y · Argentina | -33.5012 | -33.5094 | 0.024709 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Cartography GIS Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Cartography GIS Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Cartography GIS Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Chaos Mediated Phase Transitions

Extension panel **`Chaos_Mediated_Phase_Transitions`** (verification tier 47) evaluates **21** measured records at **0.031479%** pooled median error (B_verified). Formal module: `FSOT.Formal.ChaosMediatedPhaseTransitionsPriors`. This panel extends the core spine into chaos mediated phase transitions observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/chaos_mediated_phase_transitions_benchmark.json`](data/chaos_mediated_phase_transitions_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `energy`, `fusion`, `plasma`
- **Panel tags:** Chaos, Mediated, Phase, Transitions
- **Data sources / cohorts:** term3.chaos_factor high-D_eff physics — plasma, particle, higgs phase transitions

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| mhd_beta_phase · fusion_ignition_edge | 0 | 0 | 0 |
| higgs_branching_transition · median_error_pct | 0.5 | 0.500118 | 0.0236092 |
| phase_transition · chaos_panel | 0 | 0.031479 | 0.031479 |
| pooled_median · all_channels | 0 | 0.031479 | 0.031479 |
| mhd_beta_phase · reverse_field_pinch | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Chaos Mediated Phase Transitions: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Chaos Mediated Phase Transitions: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Chaos Mediated Phase Transitions: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Climate Science

Extension panel **`Climate_Science`** (verification tier 12) evaluates **17320** measured records at **0%** pooled median error (A_strong). Formal module: `FSOT.Formal.ClimateSciencePriors`. This panel extends the core spine into climate science observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/climate_observed_benchmark.json`](data/climate_observed_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `galactic`
- **Panel tags:** Climate, Science
- **Data sources / cohorts:** Post-glacial recovery frame — ice-core paleo anchors, NCEI cohort (not crisis narrative classifier)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| post_glacial_recovery_classifier · USC00053005:1975-01 | 1 | 1 | 0 |
| co2_ppm · vostok_co2_preindustrial | 280 | 280.013 | 0.00450476 |
| ch4_ppb · methane_lgm_ppb | 350 | 350.016 | 0.00450476 |
| sea_level_m · sea_level_eemian | 6 | 6.00072 | 0.0120127 |
| temp_anomaly_c · eemian_temp_anomaly | 1.5 | 1.50018 | 0.0120127 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Bi2Te3`** in Climate Science: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
- **`F`** in Climate Science: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Climate Science: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Complexity Folding Emergence Panel

Extension panel **`Complexity_Folding_Emergence_Panel`** (verification tier 91) evaluates **29** measured records at **0.0265879%** pooled median error (B_verified). Formal module: `FSOT.Formal.ComplexityFoldingEmergencePanelPriors`. This panel extends the core spine into complexity folding emergence panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/complexity_folding_emergence_panel_benchmark.json`](data/complexity_folding_emergence_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `mathematical`, `cosmological`, `particle`
- **Panel tags:** Complexity, Folding, Emergence, Panel
- **Data sources / cohorts:** Complexity folding in on itself — compactification ladder, reality folding relay

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| panel_pooled_median · adjacent_rung_coupling | 0.0200982 | 0.0200982 | 0 |
| compactification_rung_count · fold_ladder_depth | 10 | 10.0009 | 0.009504 |
| fractal_branch_panel_count · complexity_fold_tree | 318 | 318.03 | 0.009504 |
| fold_depth_span · string_cosmo_span | 2.7194 | 2.71992 | 0.0190083 |
| toe_unity_green · unification_spine | 1 | 1.00019 | 0.0190083 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Bi2Te3`** in Complexity Folding Emergence Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
- **`F`** in Complexity Folding Emergence Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Complexity Folding Emergence Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Environmental Engineering

Extension panel **`Environmental_Engineering`** (verification tier 35) evaluates **1120** measured records at **0%** pooled median error (A_strong). Formal module: `FSOT.Formal.EnvironmentalEngineeringExtensionPriors`. This panel extends the core spine into environmental engineering observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/environmental_engineering_extension_benchmark.json`](data/environmental_engineering_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `biological`, `galactic`
- **Panel tags:** Environmental, Engineering
- **Data sources / cohorts:** Climate, USGS hydrology, World Bank environmental indicators

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| environmental_panel · environmental_engineering | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| GDP_per_capita · IT_2022 | 35653.9 | 35657.1 | 0.00900951 |
| population_total · CN_2022 | 1.41218e+09 | 1.4123e+09 | 0.00900951 |
| GDP_current_USD · IN_2019 | 2.83561e+12 | 2.83586e+12 | 0.00900951 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Environmental Engineering: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Environmental Engineering: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Ca`** in Environmental Engineering: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### HVAC Thermal Systems

Extension panel **`HVAC_Thermal_Systems`** (verification tier 39) evaluates **23** measured records at **0.0178361%** pooled median error (B_verified). Formal module: `FSOT.Formal.HvacThermalSystemsPriors`. This panel extends the core spine into hvac thermal systems observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/hvac_thermal_systems_benchmark.json`](data/hvac_thermal_systems_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `material`
- **Panel tags:** Hvac, Thermal, Systems
- **Data sources / cohorts:** Heat pumps, SEER, COP, Carnot-limit HVAC thermal cohort (12 systems)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| scalar_ratio_unity · Astronomy__Cosmology_Extended__astronomical | 1 | 1 | 0 |
| shallow_earthquake_classifier · us6000pgkb | 1 | 1 | 0 |
| molecular_weight · 2244 | 180.16 | 180.159 | 0.000555 |
| depth_relay · HVAC_Thermal_Systems_depth | 0 | 0.013377 | 0.013377 |
| geologic_age_ma · Ammonoidea indet. | 312.8 | 312.842 | 0.013377 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`CO₂`** in HVAC Thermal Systems: measured **180.0**, seed-derived **180.0** via `π (rad→°)` (error **0%**). Constants: pi. Authority: NIST CCCBDB.
- **`XeF₂`** in HVAC Thermal Systems: measured **180.0**, seed-derived **180.0** via `π (rad→°)` (error **0%**). Constants: pi. Authority: NIST CCCBDB.
- **`BeCl₂`** in HVAC Thermal Systems: measured **180.0**, seed-derived **180.0** via `π (rad→°)` (error **0%**). Constants: pi. Authority: NIST CCCBDB.

#### Heavy Ion Lab Synthesis Panel

Extension panel **`Heavy_Ion_Lab_Synthesis_Panel`** (verification tier 73) evaluates **39** measured records at **9.5e-05%** pooled median error (B_verified). Formal module: `FSOT.Formal.HeavyIonLabSynthesisPanelPriors`. This panel extends the core spine into heavy ion lab synthesis panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/heavy_ion_lab_synthesis_panel_benchmark.json`](data/heavy_ion_lab_synthesis_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `material`
- **Panel tags:** Heavy, Ion, Lab, Synthesis, Panel
- **Data sources / cohorts:** Published heavy-ion fusion-evaporation reactions, proposed Z119+ beam targets — GSI, JINR, RIKEN, LBNL anchors

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| facility_energy_classifier · Cn_1996 | 1 | 1 | 0 |
| particle_physics_scalar · fsot_Particle_Physics | 0.950413 | 0.950413 | 0 |
| proposed_viability_classifier · Z119_Ti_Bk | 1 | 1 | 0 |
| cross_section_pb · Cn_1996 | 0.5 | 0.5 | 9.5e-05 |
| fusion_energetics_relay · dd_fusion | 4.03 | 4.03 | 9.5e-05 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Bi2Te3`** in Heavy Ion Lab Synthesis Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
- **`F`** in Heavy Ion Lab Synthesis Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Heavy Ion Lab Synthesis Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Mechanistic Coupling

Extension panel **`Mechanistic_Coupling`** (verification tier 45) evaluates **116** measured records at **0%** pooled median error (A_strong). Formal module: `FSOT.Formal.MechanisticCouplingPriors`. This panel extends the core spine into mechanistic coupling observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/mechanistic_coupling_benchmark.json`](data/mechanistic_coupling_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `energy`, `consciousness`
- **Panel tags:** Mechanistic, Coupling
- **Data sources / cohorts:** Causal mechanism manifest — why domains connect, mapped to formula branches

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| affinity_edge_error · Astronomy__Astrophysical_Structure_Crosswalk__astronomical | 1 | 1 | 0 |
| mechanism_channels · mechanistic_panel | 0 | 0 | 0 |
| mechanism_node_pair_validated · AI_Galactic_Orbital_Bridge__Cosmology_Extended | 1 | 1 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| mechanism_channel_weight · MEC-003 | 2 | 2.00015 | 0.00738366 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Mechanistic Coupling: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Mechanistic Coupling: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Mechanistic Coupling: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Optics Interferometry Depth Panel

Extension panel **`Optics_Interferometry_Depth_Panel`** (verification tier 87) evaluates **127** measured records at **0.026954%** pooled median error (A_strong). Formal module: `FSOT.Formal.OpticsInterferometryDepthPanelPriors`. This panel extends the core spine into optics interferometry depth panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/optics_interferometry_depth_panel_benchmark.json`](data/optics_interferometry_depth_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `astronomical`, `particle`, `galactic`
- **Panel tags:** Optics, Interferometry, Depth, Panel
- **Data sources / cohorts:** Optics interferometry depth — LIGO, JWST reference, MAST em wavelengths

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| hst_fraction · HD 189733 | 0 | 0 | 0 |
| fsot_prediction · optics_interferometry | 0 | 0.026954 | 0.026954 |
| instrument_diversity · 55 Cancri system | 11 | 11.003 | 0.026954 |
| median_em_min_nm · 55 Cancri system | 4.6e+11 | 4.60124e+11 | 0.026954 |
| pooled_median · all_channels | 0 | 0.026954 | 0.026954 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Optics Interferometry Depth Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Optics Interferometry Depth Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Fe`** in Optics Interferometry Depth Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).

#### Semiconductor Physics Public Panel

Extension panel **`Semiconductor_Physics_Public_Panel`** (verification tier 64) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.SemiconductorPhysicsPublicPanelPriors`. This panel extends the core spine into semiconductor physics public panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/semiconductor_physics_public_panel_benchmark.json`](data/semiconductor_physics_public_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `material`, `particle`
- **Panel tags:** Semiconductor, Physics, Public, Panel
- **Data sources / cohorts:** Bandgap, mobility, dielectric public semiconductor ratios

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_relay · Semiconductor_Physics_Public_Panel_depth | 0 | 0 | 0 |
| domain_scalar · fsot_Condensed_Matter | 0.338406 | 0.338406 | 0 |
| observable · debye_t_si_ge | 4.619 | 4.619 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| scalar_ratio_unity · Astronomy__Cosmology_Extended__astronomical | 1 | 1 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Semiconductor Physics Public Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Semiconductor Physics Public Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Semiconductor Physics Public Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Soil Science Panel

Extension panel **`Soil_Science_Panel`** (verification tier 82) evaluates **96** measured records at **0.006006%** pooled median error (B_verified). Formal module: `FSOT.Formal.SoilSciencePriors`. This panel extends the core spine into soil science panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/soil_science_panel_benchmark.json`](data/soil_science_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `material`
- **Panel tags:** Soil, Science, Panel
- **Data sources / cohorts:** Soil science — ISRIC SoilGrids bulk density, CEC, pH

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| fsot_prediction · soil_science | 0 | 0.006006 | 0.006006 |
| latitude · kansas_0-5cm | 37 | 37.0022 | 0.006006 |
| longitude · kansas_0-5cm | -95 | -95.0057 | 0.006006 |
| pooled_median · all_channels | 0 | 0.006006 | 0.006006 |
| value · kansas_0-5cm | 1.36 | 1.36008 | 0.006006 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Soil Science Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Soil Science Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Soil Science Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Sports Biomechanics

Extension panel **`Sports_Biomechanics`** (verification tier 34) evaluates **35** measured records at **0.0444725%** pooled median error (B_verified). Formal module: `FSOT.Formal.SportsBiomechanicsGapFillPriors`. This panel extends the core spine into sports biomechanics observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/sports_biomechanics_gap_fill_benchmark.json`](data/sports_biomechanics_gap_fill_benchmark.json)

**Subfield map:**

- **Lean routes:** `biological`, `medical`, `energy`
- **Panel tags:** Sports, Biomechanics
- **Data sources / cohorts:** World Athletics records, aerodynamic motion bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| dataset_artifact · Airfoil Gas-Medium Similarity Readout | 1 | 1 | 0 |
| full_dataset_rmse · Airfoil Gas-Medium Similarity Readout | 5.06102 | 5.06102 | 0 |
| held_out_test_rmse · Airfoil Gas-Medium Similarity Readout | 5.10255 | 5.10255 | 0 |
| report_artifact · Airfoil Gas-Medium Similarity Readout | 1 | 1 | 0 |
| row_count · Airfoil Gas-Medium Similarity Readout | 1503 | 1503 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Bi2Te3`** in Sports Biomechanics: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
- **`F`** in Sports Biomechanics: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Sports Biomechanics: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Statistical Mechanics Public Panel

Extension panel **`Statistical_Mechanics_Public_Panel`** (verification tier 64) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.StatisticalMechanicsPublicPanelPriors`. This panel extends the core spine into statistical mechanics public panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/statistical_mechanics_public_panel_benchmark.json`](data/statistical_mechanics_public_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `particle`, `thermodynamics`
- **Panel tags:** Statistical, Mechanics, Public, Panel
- **Data sources / cohorts:** Apéry ζ(3), partition ratios, equipartition public anchors

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_relay · Statistical_Mechanics_Public_Panel_depth | 0 | 0 | 0 |
| domain_scalar · fsot_Thermodynamics | 0.786975 | 0.786975 | 0 |
| observable · apery_zeta3 | 1.20206 | 1.20206 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| scalar_ratio_unity · Astronomy__Cosmology_Extended__astronomical | 1 | 1 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Statistical Mechanics Public Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Statistical Mechanics Public Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Statistical Mechanics Public Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Volcanology Panel

Extension panel **`Volcanology_Panel`** (verification tier 82) evaluates **90** measured records at **0.023502%** pooled median error (B_verified). Formal module: `FSOT.Formal.VolcanologyPriors`. This panel extends the core spine into volcanology panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/volcanology_panel_benchmark.json`](data/volcanology_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `energy`
- **Panel tags:** Volcanology, Panel
- **Data sources / cohorts:** Volcanology — GVP, USGS geohazard cross-ref Geophysics, Seismology

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| latitude · 139 km S of ‘Ohonua, Tonga | -22.6035 | -22.6049 | 0.006006 |
| longitude · 139 km S of ‘Ohonua, Tonga | -174.917 | -174.928 | 0.006006 |
| elevation_m · 139 km S of ‘Ohonua, Tonga | 1000 | 1000.22 | 0.022295 |
| pooled_median · all_channels | 0 | 0.023502 | 0.023502 |
| depth_km · 139 km S of ‘Ohonua, Tonga | 10 | 10.0025 | 0.024709 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Volcanology Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Volcanology Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Volcanology Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Z120 Z126 Beam Synthesis Panel

Extension panel **`Z120_Z126_Beam_Synthesis_Panel`** (verification tier 74) evaluates **20** measured records at **9.5e-05%** pooled median error (B_verified). Formal module: `FSOT.Formal.Z120Z126BeamSynthesisPanelPriors`. This panel extends the core spine into z120 z126 beam synthesis panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/z120_z126_beam_synthesis_panel_benchmark.json`](data/z120_z126_beam_synthesis_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `material`
- **Panel tags:** Z120, Z126, Beam, Synthesis, Panel
- **Data sources / cohorts:** Proposed Cr, Fe, Ni, Zn beams targeting Z=120-126 island — cross-section, facility viability

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| heavy_ion_lab_bridge · heavy_ion_lab_synthesis_panel | 9.5e-05 | 9.5e-05 | 0 |
| island_beam_ceiling_Z · proposed_Z126 | 126 | 126 | 0 |
| island_beam_viability_classifier · Z120_Cr_Cm | 0 | 0 | 0 |
| cross_section_pb · Z120_Cr_Cm | 0.012 | 0.012 | 9.5e-05 |
| pooled_median · all_channels | 0 | 9.5e-05 | 9.5e-05 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Z120 Z126 Beam Synthesis Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Z120 Z126 Beam Synthesis Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Z120 Z126 Beam Synthesis Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
