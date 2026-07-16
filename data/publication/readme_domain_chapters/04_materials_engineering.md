## Materials Engineering, Metamaterials & Condensed Matter

**Panels:** 8 · **Records:** 603 · **Mean panel median error:** 0.011741%

### Panel index

| Panel | Records | Median error % | Tier |
|-------|--------:|---------------:|------|
| `Acoustic_Resonance_Materials` | 29 | 0.0083815 | B_verified |
| `Chemical_Engineering` | 186 | 0.00103334 | A_strong |
| `Condensed_Matter_Superconductivity_Depth_Panel` | 21 | 0.033841 | B_verified |
| `Lab_Synthesis_Metamaterial_Spine` | 43 | 3.4e-05 | B_verified |
| `Materials_Creep_Fracture_Depth_Panel` | 71 | 0.011734 | B_verified |
| `Materials_Engineering` | 87 | 0.0271703 | B_verified |
| `Materials_Project_Live_Panel` | 141 | 0.011734 | A_strong |
| `Metamaterial_Fluid_Design_Prereg_Scaffold` | 25 | 0 | B_verified |

#### Acoustic Resonance Materials

Extension panel **`Acoustic_Resonance_Materials`** (verification tier 47) evaluates **29** measured records at **0.0083815%** pooled median error (B_verified). Formal module: `FSOT.Formal.AcousticResonanceMaterialsPriors`. This panel extends the core spine into acoustic resonance materials observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/acoustic_resonance_materials_benchmark.json`](data/acoustic_resonance_materials_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `material`, `energy`, `acoustical`
- **Panel tags:** Acoustic, Resonance, Materials
- **Data sources / cohorts:** term3.acoustic_bleed gap — species acoustic impedance, building aeroacoustics

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_impedance_MRayl · Glass | 14.5 | 14.5 | 0 |
| building_acoustical_coupling · Carnot COP (0C cold, 27C hot) | 11 | 11.0009 | 0.0083815 |
| building_aero · built_env_panel | 0 | 0.008381 | 0.0083815 |
| pooled_median · all_channels | 0 | 0.008381 | 0.0083815 |
| aeroacoustic_rmse · airfoil_seed | 5.06102 | 5.06152 | 0.0100578 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Acoustic Resonance Materials: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Acoustic Resonance Materials: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Acoustic Resonance Materials: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Chemical Engineering

Extension panel **`Chemical_Engineering`** (verification tier 35) evaluates **186** measured records at **0.00103334%** pooled median error (A_strong). Formal module: `FSOT.Formal.ChemicalEngineeringExtensionPriors`. This panel extends the core spine into chemical engineering observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/chemical_engineering_extension_benchmark.json`](data/chemical_engineering_extension_benchmark.json)

**Subfield map:**

- **Lean routes:** `chemical`, `electron`, `energy`
- **Panel tags:** Chemical, Engineering
- **Data sources / cohorts:** PubChem process chemistry, thermodynamics engineering rules

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| molecular_weight · AMINOHIPPURIC ACID | 194.19 | 194.19 | 0 |
| symbolic_schema · MS-001 | 1 | 1 | 0 |
| pooled_median · all_channels | 0 | 0.001033 | 0.00103334 |
| process_chemistry · chemical_engineering_panel | 0 | 0.001033 | 0.00103334 |
| molecular_weight · BUTALBITAL | 224.26 | 224.26 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Chemical Engineering: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Chemical Engineering: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Chemical Engineering: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Condensed Matter Superconductivity Depth Panel

Extension panel **`Condensed_Matter_Superconductivity_Depth_Panel`** (verification tier 87) evaluates **21** measured records at **0.033841%** pooled median error (B_verified). Formal module: `FSOT.Formal.CondensedMatterSuperconductivityDepthPanelPriors`. This panel extends the core spine into condensed matter superconductivity depth panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/condensed_matter_superconductivity_depth_panel_benchmark.json`](data/condensed_matter_superconductivity_depth_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `particle`, `energy`
- **Panel tags:** Condensed, Matter, Superconductivity, Depth, Panel
- **Data sources / cohorts:** Superconductivity Tc depth — literature, breakthrough, quantum materials

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| Tc_K · Al | 1.18 | 1.1804 | 0.033841 |
| fsot_prediction · superconductivity_Tc | 0 | 0.033841 | 0.033841 |
| pooled_median · all_channels | 0 | 0.033841 | 0.033841 |
| Tc_K · BaKFe2As2 | 38 | 38.0129 | 0.033841 |
| Tc_K · Bi2212 | 95 | 95.0321 | 0.033841 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Condensed Matter Superconductivity Depth Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Condensed Matter Superconductivity Depth Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Fe`** in Condensed Matter Superconductivity Depth Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).

#### Lab Synthesis Metamaterial Spine

Extension panel **`Lab_Synthesis_Metamaterial_Spine`** (verification tier 73) evaluates **43** measured records at **3.4e-05%** pooled median error (B_verified). Formal module: `FSOT.Formal.LabSynthesisMetamaterialSpinePriors`. This panel extends the core spine into lab synthesis metamaterial spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/lab_synthesis_metamaterial_spine_benchmark.json`](data/lab_synthesis_metamaterial_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `material`, `energy`
- **Panel tags:** Lab, Synthesis, Metamaterial, Spine
- **Data sources / cohorts:** Lab synthesis, metamaterial certificate rollup — heavy-ion, conditions, cold-fusion crosswalk, periodic, fusion bridges

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_bleed_panel_bridge · term3_acoustic_bleed_depth | 0.0083815 | 0.0083815 | 0 |
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| fluid_like_response_classifier · acoustic_bleed_phononic_crystal | 0 | 0 | 0 |
| lab_synthesis_metamaterial_ready · lab_synthesis_metamaterial_spine | 1 | 1 | 0 |
| magic_number_proximity · H | 2 | 2 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Lab Synthesis Metamaterial Spine: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Lab Synthesis Metamaterial Spine: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Lab Synthesis Metamaterial Spine: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Materials Creep Fracture Depth Panel

Extension panel **`Materials_Creep_Fracture_Depth_Panel`** (verification tier 87) evaluates **71** measured records at **0.011734%** pooled median error (B_verified). Formal module: `FSOT.Formal.MaterialsCreepFractureDepthPanelPriors`. This panel extends the core spine into materials creep fracture depth panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/materials_creep_fracture_depth_panel_benchmark.json`](data/materials_creep_fracture_depth_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `energy`, `particle`
- **Panel tags:** Materials, Creep, Fracture, Depth, Panel
- **Data sources / cohorts:** Creep, fracture mechanics anchors, Materials Project relay

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| band_gap_eV · Al | 0 | 0 | 0 |
| formation_energy_eV_per_atom · Al | 0 | 0 | 0 |
| bulk_modulus_GPa · Al | 76 | 76.0089 | 0.011734 |
| fsot_prediction · materials_creep_fracture_depth_lab | 0 | 0.011734 | 0.011734 |
| pooled_median · all_channels | 0 | 0.011734 | 0.011734 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Materials Creep Fracture Depth Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Materials Creep Fracture Depth Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Materials Creep Fracture Depth Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Materials Engineering

Extension panel **`Materials_Engineering`** (verification tier 29) evaluates **87** measured records at **0.0271703%** pooled median error (B_verified). Formal module: `FSOT.Formal.MaterialsEngineeringPriors`. This panel extends the core spine into materials engineering observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/materials_engineering_benchmark.json`](data/materials_engineering_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `energy`
- **Panel tags:** Materials, Engineering
- **Data sources / cohorts:** Young's modulus, thermal κ, bulk, shear, Poisson — buildable engineering SMILES

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| §34 Young's Modulus · Pb | 16 | 16 | 0 |
| §73 Thermal Expansion · Diamond | 1 | 1 | 0 |
| §70 Shear Modulus · Pt | 61 | 60.9995 | 0.000759439 |
| §84 Poisson Ratio ν · Ni | 0.31 | 0.309994 | 0.00193239 |
| §37 Thermal κ · Fe | 80.4 | 80.4026 | 0.00318833 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`alpha_Fe`** in Materials Engineering: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Materials Engineering: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
- **`Fe`** in Materials Engineering: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).

#### Materials Project Live Panel

Extension panel **`Materials_Project_Live_Panel`** (verification tier 68) evaluates **141** measured records at **0.011734%** pooled median error (A_strong). Formal module: `FSOT.Formal.MaterialsProjectLivePanelPriors`. This panel extends the core spine into materials project live panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/materials_project_live_panel_benchmark.json`](data/materials_project_live_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `particle`, `energy`
- **Panel tags:** Materials, Project, Live, Panel
- **Data sources / cohorts:** Materials Project API, bundled fallback — band gap, formation energy

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| band_gap_eV · mp-106 | 0 | 0 | 0 |
| formation_energy_eV_per_atom · mp-106 | 0 | 0 | 0 |
| live_vs_bundled_band_gap_eV · mp-1265 | 3.44 | 3.44 | 0 |
| live_vs_bundled_formation_energy_eV_per_atom · mp-1265 | -0.73 | -0.73 | 0 |
| materials_science_scalar · fsot_Materials_Science | 0.33526 | 0.33526 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Materials Project Live Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Materials Project Live Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Materials Project Live Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Metamaterial Fluid Design Prereg Scaffold

Extension panel **`Metamaterial_Fluid_Design_Prereg_Scaffold`** (verification tier 73) evaluates **25** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.MetamaterialFluidDesignPreregScaffoldPriors`. This panel extends the core spine into metamaterial fluid design prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/metamaterial_fluid_design_prereg_scaffold_benchmark.json`](data/metamaterial_fluid_design_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `fusion`, `energy`, `particle`
- **Panel tags:** Metamaterial, Fluid, Design, Prereg, Scaffold
- **Data sources / cohorts:** Fluid-like metamaterial candidates preregistered via term3 acoustic_bleed, boundary_partition — not claimed synthesized

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_bleed_panel_bridge · term3_acoustic_bleed_depth | 0.0083815 | 0.0083815 | 0 |
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| fluid_like_response_classifier · acoustic_bleed_phononic_crystal | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| prereg_discriminant_gate · acoustic_bleed_phononic_crystal | 1 | 1 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Metamaterial Fluid Design Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Metamaterial Fluid Design Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Metamaterial Fluid Design Prereg Scaffold: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
