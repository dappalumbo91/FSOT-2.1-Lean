## Fusion Physics, Fuels & Thermochemistry

**Panels:** 11 · **Records:** 644 · **Mean panel median error:** 0.003593%

### Panel index

| Panel | Records | Median error % | Tier |
|-------|--------:|---------------:|------|
| `Cold_Fusion_Candidate_Prereg_Scaffold` | 24 | 0 | B_verified |
| `Cold_Fusion_Lab_Synthesis_Crosswalk` | 22 | 0 | B_verified |
| `Fuel_Candidate_Prereg_Scaffold` | 33 | 0 | B_verified |
| `Fuel_Lab_Live_Panel` | 366 | 0.039349 | A_strong |
| `Fuel_Thermochemistry_Public_Anchors` | 24 | 0 | B_verified |
| `Fusion_Decay_Chain_Prereg_Scaffold` | 24 | 0 | B_verified |
| `Fusion_Lab_Certificate_Spine` | 50 | 0 | B_verified |
| `Fusion_Physics_Public_Panel` | 24 | 9.5e-05 | B_verified |
| `Inertial_Confinement_Fusion_Panel` | 24 | 7.9e-05 | B_verified |
| `Magnetic_Confinement_Fusion_Panel` | 22 | 0 | B_verified |
| `Published_Fuel_Property_Panel` | 31 | 0 | B_verified |

#### Cold Fusion Candidate Prereg Scaffold

Extension panel **`Cold_Fusion_Candidate_Prereg_Scaffold`** (verification tier 71) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.ColdFusionCandidatePreregScaffoldPriors`. This panel extends the core spine into cold fusion candidate prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/cold_fusion_candidate_prereg_scaffold_benchmark.json`](data/cold_fusion_candidate_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `energy`, `particle`, `material`
- **Panel tags:** Cold, Fusion, Candidate, Prereg, Scaffold
- **Data sources / cohorts:** Low-temperature fusion candidate screening via term3 acoustic bleed, boundary partition — preregistered, not claimed discovered

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_bleed_panel_bridge · term3_acoustic_bleed_depth | 0.0083815 | 0.0083815 | 0 |
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| depth_relay · Cold_Fusion_Candidate_Prereg_Scaffold_depth | 0 | 0 | 0 |
| panel_pooled_median · fusion_physics_public | 9.5e-05 | 9.5e-05 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Cold Fusion Candidate Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Cold Fusion Candidate Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Cold Fusion Candidate Prereg Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Cold Fusion Lab Synthesis Crosswalk

Extension panel **`Cold_Fusion_Lab_Synthesis_Crosswalk`** (verification tier 73) evaluates **22** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.ColdFusionLabSynthesisCrosswalkPriors`. This panel extends the core spine into cold fusion lab synthesis crosswalk observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/cold_fusion_lab_synthesis_crosswalk_benchmark.json`](data/cold_fusion_lab_synthesis_crosswalk_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `material`, `energy`
- **Panel tags:** Cold, Fusion, Lab, Synthesis, Crosswalk
- **Data sources / cohorts:** Tier 71↔72↔73 bridge — Ti-D absorption → Z119 Ti beam, Pd-D lattice → metamaterial heat exchanger, muon-catalyzed → fusion decay chain

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_bleed_panel_bridge · term3_acoustic_bleed_depth | 0.0083815 | 0.0083815 | 0 |
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| candidate_predicted_half_life_s · Z120_N184_unbinilium | 2.5e+06 | 2.5e+06 | 0 |
| cold_fusion_crosswalk · lab_synthesis_bridge | 0 | 0 | 0 |
| cold_fusion_synthesis_crosswalk_gate · muon_catalyzed_dd | 1 | 1 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Cold Fusion Lab Synthesis Crosswalk: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Cold Fusion Lab Synthesis Crosswalk: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Cold Fusion Lab Synthesis Crosswalk: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Fuel Candidate Prereg Scaffold

Extension panel **`Fuel_Candidate_Prereg_Scaffold`** (verification tier 65) evaluates **33** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.FuelCandidatePreregScaffoldPriors`. This panel extends the core spine into fuel candidate prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/fuel_candidate_prereg_scaffold_benchmark.json`](data/fuel_candidate_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `chemical`, `material`
- **Panel tags:** Fuel, Candidate, Prereg, Scaffold
- **Data sources / cohorts:** NIST, CRC fuel screening methodology — novel fuel discovery preregistered separately

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| density_kg_m3 · ethanol | 789 | 789 | 0 |
| density_tolerance_pct · Fuel density tolerance | 3 | 3 | 0 |
| flash_point_margin_c · Flash point safety margin (°C) | 10 | 10 | 0 |
| formula_mass_g_mol · hydrogen | 2.016 | 2.016 | 0 |
| hf_kj_mol · ethanol | -234.8 | -234.8 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Fuel Candidate Prereg Scaffold: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Fuel Candidate Prereg Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Fuel Candidate Prereg Scaffold: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Fuel Lab Live Panel

Extension panel **`Fuel_Lab_Live_Panel`** (verification tier 88) evaluates **366** measured records at **0.039349%** pooled median error (A_strong). Formal module: `FSOT.Formal.FuelLabLivePanelPriors`. This panel extends the core spine into fuel lab live panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/fuel_lab_live_panel_benchmark.json`](data/fuel_lab_live_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `chemical`, `material`
- **Panel tags:** Fuel, Lab, Live, Panel
- **Data sources / cohorts:** Desktop Fuel Lab engine simulator grounded fuel profiles

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| renewable_rank · compare_fsot_algae_oil_biodiesel | 0.822939 | 0.822988 | 0.006006 |
| material_compatibility_index · compare_fsot_algae_oil_biodiesel | 0.929 | 0.929125 | 0.01341 |
| conversion_efficiency · compare_fsot_algae_oil_biodiesel | 0.84 | 0.840281 | 0.033401 |
| bsfc_g_kwh · compare_fsot_algae_oil_biodiesel | 258.596 | 258.698 | 0.039349 |
| clean_index · fsot_algae_oil_biodiesel | 0.89 | 0.89035 | 0.039349 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Fuel Lab Live Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Fuel Lab Live Panel: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Si`** in Fuel Lab Live Panel: measured **1.385**, seed-derived **1.3850362977165687** via `Ω⁻²+B_IN` (error **0.002621%**). Constants: seed constants. Authority: Andersen et al., JPCRD 28 (1999).

#### Fuel Thermochemistry Public Anchors

Extension panel **`Fuel_Thermochemistry_Public_Anchors`** (verification tier 59) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.FuelThermochemistryPublicAnchorsPriors`. This panel extends the core spine into fuel thermochemistry public anchors observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/fuel_thermochemistry_public_anchors_benchmark.json`](data/fuel_thermochemistry_public_anchors_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `chemical`, `material`
- **Panel tags:** Fuel, Thermochemistry, Public, Anchors
- **Data sources / cohorts:** NIST ΔHf, published fuel catalog bridge — novel fuel discovery preregistered separately

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| density_kg_m3 · hydrogen | 0.0899 | 0.0899 | 0 |
| depth_relay · Fuel_Thermochemistry_Public_Anchors_depth | 0 | 0 | 0 |
| hf_kj_mol · ammonia | -45.9 | -45.9 | 0 |
| lhv_mj_kg · ammonia | 18.6 | 18.6 | 0 |
| panel_pooled_median · materials_engineering | 0.02717 | 0.02717 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Fuel Thermochemistry Public Anchors: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Fuel Thermochemistry Public Anchors: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Fuel Thermochemistry Public Anchors: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Fusion Decay Chain Prereg Scaffold

Extension panel **`Fusion_Decay_Chain_Prereg_Scaffold`** (verification tier 74) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.FusionDecayChainPreregScaffoldPriors`. This panel extends the core spine into fusion decay chain prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/fusion_decay_chain_prereg_scaffold_benchmark.json`](data/fusion_decay_chain_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `energy`
- **Panel tags:** Fusion, Decay, Chain, Prereg, Scaffold
- **Data sources / cohorts:** Pd-D, muon-catalyzed, ICF → Z=119-126 decay chain prereg — not claimed observed

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| cold_fusion_bridge · cold_fusion_candidate_prereg_scaffold | 0 | 0 | 0 |
| decay_chain_viability_classifier · icf_nif_to_Z124_cascade | 1 | 1 | 0 |
| depth_relay · Fusion_Decay_Chain_Prereg_Scaffold_depth | 0 | 0 | 0 |
| lab_synthesis_crosswalk_bridge · cold_fusion_lab_synthesis_crosswalk | 0 | 0 | 0 |
| panel_pooled_median · heavy_ion_lab_synthesis | 9.5e-05 | 9.5e-05 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Fusion Decay Chain Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Fusion Decay Chain Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Fusion Decay Chain Prereg Scaffold: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Fusion Lab Certificate Spine

Extension panel **`Fusion_Lab_Certificate_Spine`** (verification tier 71) evaluates **50** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.FusionLabCertificateSpinePriors`. This panel extends the core spine into fusion lab certificate spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/fusion_lab_certificate_spine_benchmark.json`](data/fusion_lab_certificate_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `energy`, `plasma`, `particle`, `material`
- **Panel tags:** Fusion, Lab, Certificate, Spine
- **Data sources / cohorts:** Fusion lab certificate rollup — public panels, plasma, fuel thermochemistry, energy bridges

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_bleed_panel_bridge · term3_acoustic_bleed_depth | 0.0083815 | 0.0083815 | 0 |
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| fusion_certificate · fusion_lab_spine | 0 | 0 | 0 |
| fusion_lab_certificate_ready · fusion_lab_certificate_spine | 1 | 1 | 0 |
| hf_kj_mol · ethanol | -234.8 | -234.8 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Fusion Lab Certificate Spine: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Fusion Lab Certificate Spine: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Fusion Lab Certificate Spine: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Fusion Physics Public Panel

Extension panel **`Fusion_Physics_Public_Panel`** (verification tier 71) evaluates **24** measured records at **9.5e-05%** pooled median error (B_verified). Formal module: `FSOT.Formal.FusionPhysicsPublicPanelPriors`. This panel extends the core spine into fusion physics public panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/fusion_physics_public_panel_benchmark.json`](data/fusion_physics_public_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `energy`, `particle`, `plasma`
- **Panel tags:** Fusion, Physics, Public, Panel
- **Data sources / cohorts:** IAEA, NIF, ITER published reaction energetics, Lawson thresholds, power-balance temps

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| lawson_triple_product · dt_breakeven | 3e+20 | 3e+20 | 0 |
| particle_physics_scalar · fsot_Particle_Physics | 0.950413 | 0.950413 | 0 |
| scalar_ratio_unity · Astronomy__Cosmology_Extended__astronomical | 1 | 1 | 0 |
| coulomb_peak_kev · dd_fusion | 50 | 50 | 9.5e-05 |
| cross_section_peak_barn · dd_fusion | 0.1 | 0.1 | 9.5e-05 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Bi2Te3`** in Fusion Physics Public Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
- **`F`** in Fusion Physics Public Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Fusion Physics Public Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Inertial Confinement Fusion Panel

Extension panel **`Inertial_Confinement_Fusion_Panel`** (verification tier 71) evaluates **24** measured records at **7.9e-05%** pooled median error (B_verified). Formal module: `FSOT.Formal.InertialConfinementFusionPanelPriors`. This panel extends the core spine into inertial confinement fusion panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/inertial_confinement_fusion_panel_benchmark.json`](data/inertial_confinement_fusion_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `energy`, `plasma`, `particle`
- **Panel tags:** Inertial, Confinement, Fusion, Panel
- **Data sources / cohorts:** NIF, Omega ICF ignition, yield, Q relays from published milestones

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| ignition_classifier · NIF_2021 | 0 | 0 | 0 |
| mhd_beta_stability · ICF_hohlraum | 1 | 1 | 0 |
| panel_pooled_median · fusion_physics_public | 9.5e-05 | 9.5e-05 | 0 |
| scalar_ratio_unity · Astronomy__Cosmology_Extended__astronomical | 1 | 1 | 0 |
| thermodynamics_scalar · fsot_Thermodynamics | 0.786975 | 0.786975 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Inertial Confinement Fusion Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Inertial Confinement Fusion Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Inertial Confinement Fusion Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Magnetic Confinement Fusion Panel

Extension panel **`Magnetic_Confinement_Fusion_Panel`** (verification tier 71) evaluates **22** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.MagneticConfinementFusionPanelPriors`. This panel extends the core spine into magnetic confinement fusion panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/magnetic_confinement_fusion_panel_benchmark.json`](data/magnetic_confinement_fusion_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `energy`, `plasma`, `particle`
- **Panel tags:** Magnetic, Confinement, Fusion, Panel
- **Data sources / cohorts:** Tokamak, stellarator MHD relay, JET, ITER, EAST facility triple-product anchors

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| ignition_classifier · EAST_2023 | 0 | 0 | 0 |
| magnetic_confinement · tokamak_stellarator | 0 | 0 | 0 |
| mhd_beta_stability · FRC_laboratory | 1 | 1 | 0 |
| plasma_scalar_bridge · fsot_plasma_thermodynamics | 0.786975 | 0.786975 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Magnetic Confinement Fusion Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Magnetic Confinement Fusion Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Magnetic Confinement Fusion Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Published Fuel Property Panel

Extension panel **`Published_Fuel_Property_Panel`** (verification tier 57) evaluates **31** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PublishedFuelPropertyPanelPriors`. This panel extends the core spine into published fuel property panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/published_fuel_property_panel_benchmark.json`](data/published_fuel_property_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `chemical`, `material`
- **Panel tags:** Published, Fuel, Property, Panel
- **Data sources / cohorts:** NIST, CRC published LHV, density — novel fuel discovery preregistered separately

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| density_kg_m3 · ammonia | 682 | 682 | 0 |
| energy_scalar · fsot_Thermodynamics | 0.786975 | 0.786975 | 0 |
| formula_mass_g_mol · ammonia | 17.031 | 17.031 | 0 |
| fuel_panel · published_fuel | 0 | 0 | 0 |
| lhv_mj_kg · ammonia | 18.6 | 18.6 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Published Fuel Property Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Published Fuel Property Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Published Fuel Property Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
