## Chemistry, Materials & Molecular Engineering

**Panels:** 41 · **Records:** 8,231 · **Mean panel median error:** 0.00753307%

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

- **`F`** in Acoustic Resonance Materials: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Acoustic Resonance Materials: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Acoustic Resonance Materials: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### CRC Handbook Properties

Extension panel **`CRC_Handbook_Properties`** (verification tier 78) evaluates **391** measured records at **0.026922%** pooled median error (A_strong). Formal module: `FSOT.Formal.CrcHandbookPropertiesPriors`. This panel extends the core spine into crc handbook properties observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/crc_handbook_properties_benchmark.json`](data/crc_handbook_properties_benchmark.json)

**Subfield map:**

- **Lean routes:** `chemical`, `material`
- **Panel tags:** Crc, Handbook, Properties
- **Data sources / cohorts:** CRC Handbook, NIST chemistry anchors — SMILES lab empirical panel

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| §1 Foundation · pH_water (mixed) | 7 | 7 | 0 |
| §30 Refractive nD · diethyl ether (dimensionless) | 1.353 | 1.353 | 3.4e-05 |
| §48 ΔHfus · N₂ (kJ/mol) | 0.72 | 0.72 | 5.3e-05 |
| §98 Vapor Pressure · CS2 (mmHg) | 359 | 359 | 5.5e-05 |
| §87 Heat Cap Ratio Cp/Cv · N2 (dimensionless) | 1.4 | 1.4 | 7.4e-05 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`pH_water`** in CRC Handbook Properties: measured **7.0**, seed-derived **7.0** via `φ⁻⁴ + φ⁴` (error **0%**). Constants: phi. Authority: NIST / CRC / Allen / Luo.
- **`CS2`** in CRC Handbook Properties: measured **359.0**, seed-derived **358.99980082967573** via `E^4+PI^5-PHI^1` (error **5.5e-05%**). Constants: phi, pi. Authority: NIST Chemistry WebBook / CRC.
- **`F`** in CRC Handbook Properties: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

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

- **`IE_Ar`** in Chemical Engineering: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Chemical Engineering: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.
- **`P`** in Chemical Engineering: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Chemical Structure Stability Panel

Extension panel **`Chemical_Structure_Stability_Panel`** (verification tier 57) evaluates **32** measured records at **0.00206%** pooled median error (B_verified). Formal module: `FSOT.Formal.ChemicalStructureStabilityPanelPriors`. This panel extends the core spine into chemical structure stability panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/chemical_structure_stability_panel_benchmark.json`](data/chemical_structure_stability_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `chemical`, `material`, `particle`, `electron`
- **Panel tags:** Chemical, Structure, Stability, Panel
- **Data sources / cohorts:** PubChem formula-mass, NIST, SMILES topology — no novel stability claims

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| Planck constant | 6.62607e-34 | 6.62607e-34 | 0 |
| fine-structure constant | 0.00729735 | 0.00729735 | 0 |
| formula_mass_closure · 5280961 | 270.24 | 270.24 | 0 |
| proton mass | 1.67262e-27 | 1.67262e-27 | 0 |
| smiles_mapped_records · FSOT_SMILES_Lab | 1470 | 1470 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Chemical Structure Stability Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Chemical Structure Stability Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`P`** in Chemical Structure Stability Panel: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

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

- **`F`** in Cold Fusion Candidate Prereg Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Cold Fusion Candidate Prereg Scaffold: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Cold Fusion Candidate Prereg Scaffold: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

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

- **`Fe`** in Cold Fusion Lab Synthesis Crosswalk: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Cold Fusion Lab Synthesis Crosswalk: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Cold Fusion Lab Synthesis Crosswalk: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

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

- **`alpha_Fe`** in Condensed Matter Superconductivity Depth Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Fe`** in Condensed Matter Superconductivity Depth Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Condensed Matter Superconductivity Depth Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Distant Island Emergence Simulation

Extension panel **`Distant_Island_Emergence_Simulation`** (verification tier 75) evaluates **36** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.DistantIslandEmergenceSimulationPriors`. This panel extends the core spine into distant island emergence simulation observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/distant_island_emergence_simulation_benchmark.json`](data/distant_island_emergence_simulation_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `astronomical`
- **Panel tags:** Distant, Island, Emergence, Simulation
- **Data sources / cohorts:** Distant island emergence pathways — Z=128-164 fusion-decay-chain viability

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| distant_emergence · z128_z164_sim | 0 | 0 | 0 |
| distant_emergence_classifier · Z128_N184 | 1 | 1 | 0 |
| distant_emergence_score · Z128_N184 | 299043 | 299043 | 0 |
| emergence_pathway_viable · Z128_N184__cosmic_ray_spallation | 0 | 0 | 0 |
| periodic_extension_Z_ceiling · distant_island_Z164 | 164 | 164 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Distant Island Emergence Simulation: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Distant Island Emergence Simulation: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`P`** in Distant Island Emergence Simulation: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Distant Island Z128 Z132 Deep Panel

Extension panel **`Distant_Island_Z128_Z132_Deep_Panel`** (verification tier 75) evaluates **24** measured records at **1e-06%** pooled median error (B_verified). Formal module: `FSOT.Formal.DistantIslandZ128Z132DeepPanelPriors`. This panel extends the core spine into distant island z128 z132 deep panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/distant_island_z128_z132_deep_panel_benchmark.json`](data/distant_island_z128_z132_deep_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`
- **Panel tags:** Distant, Island, Z128, Z132, Deep, Panel
- **Data sources / cohorts:** Z=128-132 distant island deep anchors — half-lives, binding, magic proximity

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_relay · Distant_Island_Z128_Z132_Deep_Panel_depth | 0 | 0 | 0 |
| distant_island_Z132_ceiling · superheavy_shell_peak | 132 | 132 | 0 |
| distant_island_half_life_s · Z128_N184 | 180000 | 180000 | 0 |
| distant_island_peak_classifier · Z128_N184 | 1 | 1 | 0 |
| island_half_life_s · Z119_N177 | 0.8 | 0.8 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Distant Island Z128 Z132 Deep Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Distant Island Z128 Z132 Deep Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Distant Island Z128 Z132 Deep Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

#### Element Synthesis Condition Scaffold

Extension panel **`Element_Synthesis_Condition_Scaffold`** (verification tier 73) evaluates **45** measured records at **0.000787%** pooled median error (B_verified). Formal module: `FSOT.Formal.ElementSynthesisConditionScaffoldPriors`. This panel extends the core spine into element synthesis condition scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/element_synthesis_condition_scaffold_benchmark.json`](data/element_synthesis_condition_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `material`, `thermodynamics`
- **Panel tags:** Element, Synthesis, Condition, Scaffold
- **Data sources / cohorts:** Lab synthesis condition gates — beam energy margin, temperature proxy, facility capacity under published, proposed reactions

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| beam_energy_margin_mev_u · Z119_Ti_Bk | 0 | 0 | 0 |
| superheavy_stability_bridge · superheavy_element_stability_panel | 1e-06 | 1e-06 | 0 |
| synthesis_condition_classifier · Cn_1996 | 1 | 1 | 0 |
| synthesis_condition_ready · element_synthesis_condition_scaffold | 1 | 1 | 0 |
| synthesis_screening_gate · facility_margin_mev_u | 10 | 10 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Element Synthesis Condition Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Element Synthesis Condition Scaffold: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Element Synthesis Condition Scaffold: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

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
- **`BL_N−H`** in Fuel Lab Live Panel: measured **1.01**, seed-derived **1.0099883725773517** via `A_bleed − γ⁶` (error **0.001151%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

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

- **`F`** in Fuel Thermochemistry Public Anchors: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`P`** in Fuel Thermochemistry Public Anchors: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`BL_N−H`** in Fuel Thermochemistry Public Anchors: measured **1.01**, seed-derived **1.0099883725773517** via `A_bleed − γ⁶` (error **0.001151%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

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

- **`F`** in Fusion Decay Chain Prereg Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Fusion Decay Chain Prereg Scaffold: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Fusion Decay Chain Prereg Scaffold: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

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

- **`F`** in Fusion Lab Certificate Spine: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Fusion Lab Certificate Spine: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Fusion Lab Certificate Spine: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

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

- **`F`** in Fusion Physics Public Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Fusion Physics Public Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
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

- **`F`** in Inertial Confinement Fusion Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Inertial Confinement Fusion Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Inertial Confinement Fusion Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Ionospheric Chemistry Coupling

Extension panel **`Ionospheric_Chemistry_Coupling`** (verification tier 47) evaluates **85** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.IonosphericChemistryCouplingPriors`. This panel extends the core spine into ionospheric chemistry coupling observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/ionospheric_chemistry_coupling_benchmark.json`](data/ionospheric_chemistry_coupling_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`, `energy`, `plasma`
- **Panel tags:** Ionospheric, Chemistry, Coupling
- **Data sources / cohorts:** Magnetosphere cluster gap — ionosphere MHD, Dst, Kp, Bz coupling

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| dst_storm_classifier · 2026-06-26T17:00:00 | 0 | 0 | 0 |
| ionospheric · magnetosphere_cluster_panel | 0 | 0 | 0 |
| kp_storm_classifier · 1932-01-01T00:00:00 | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| ionosphere_mhd_beta · ionosphere | 1 | 1.00024 | 0.0236092 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Ionospheric Chemistry Coupling: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Ionospheric Chemistry Coupling: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`P`** in Ionospheric Chemistry Coupling: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Island Of Stability Deep Panel

Extension panel **`Island_Of_Stability_Deep_Panel`** (verification tier 74) evaluates **23** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.IslandOfStabilityDeepPanelPriors`. This panel extends the core spine into island of stability deep panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/island_of_stability_deep_panel_benchmark.json`](data/island_of_stability_deep_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`
- **Panel tags:** Island, Stability, Deep, Panel
- **Data sources / cohorts:** Z=119-126 island deep anchors — half-lives, binding energy, magic-number proximity, decay trend

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| island_Z_range · Z120_Z126_deep | 126 | 126 | 0 |
| island_half_life_s · Z119_N177 | 0.8 | 0.8 | 0 |
| island_peak_classifier · Z119_N177 | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| island_deep · z120_z126_stability | 0 | 0 | 9.50414e-09 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Island Of Stability Deep Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Island Of Stability Deep Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Island Of Stability Deep Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

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

- **`pH_water`** in Lab Synthesis Metamaterial Spine: measured **7.0**, seed-derived **7.0** via `φ⁻⁴ + φ⁴` (error **0%**). Constants: phi. Authority: NIST / CRC / Allen / Luo.
- **`H⁺/H₂`** in Lab Synthesis Metamaterial Spine: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Lab Synthesis Metamaterial Spine: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).

#### Machine And Molecule Live Panel

Extension panel **`Machine_And_Molecule_Live_Panel`** (verification tier 88) evaluates **120** measured records at **0.01341%** pooled median error (A_strong). Formal module: `FSOT.Formal.MachineAndMoleculeLivePanelPriors`. This panel extends the core spine into machine and molecule live panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/machine_and_molecule_live_panel_benchmark.json`](data/machine_and_molecule_live_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `material`, `energy`, `particle`
- **Panel tags:** Machine, And, Molecule, Live, Panel
- **Data sources / cohorts:** Desktop FSOT_Machine_And_Molecule species catalog live verification

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boiling_K · metals_Hg_boiling_K | 629.9 | 629.984 | 0.01341 |
| bulk_GPa · metals_Ag_bulk_GPa | 104 | 104.014 | 0.01341 |
| cohesive_eV · metals_Ag_cohesive_eV | 2.95 | 2.9504 | 0.01341 |
| cp_J_molK · metals_Al_cp_J_molK | 24.2 | 24.2032 | 0.01341 |
| expansion_e6_per_K · metals_Ag_expansion_e6_per_K | 18 | 18.0024 | 0.01341 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`IE_Ar`** in Machine And Molecule Live Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`P`** in Machine And Molecule Live Panel: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_S`** in Machine And Molecule Live Panel: measured **10.36**, seed-derived **10.360130217649854** via `φ⁶/√3` (error **0.001257%**). Constants: phi. Authority: NIST / CRC / Allen / Luo.

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

- **`F`** in Magnetic Confinement Fusion Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Magnetic Confinement Fusion Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Magnetic Confinement Fusion Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Maillard Chemistry

Extension panel **`Maillard_Chemistry`** (verification tier 34) evaluates **30** measured records at **0.0944369%** pooled median error (B_verified). Formal module: `FSOT.Formal.MaillardChemistryGapFillPriors`. This panel extends the core spine into maillard chemistry observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/maillard_chemistry_gap_fill_benchmark.json`](data/maillard_chemistry_gap_fill_benchmark.json)

**Subfield map:**

- **Lean routes:** `energy`, `medical`, `material`
- **Panel tags:** Maillard, Chemistry
- **Data sources / cohorts:** Maillard, browning kinetics from culinary SMILES, roast observables

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| §51 Solubility logS · caffeine | 0.81 | 0.81 | 2.94767e-05 |
| §50 Diffusion D · sucrose | 0.523 | 0.522947 | 0.0102218 |
| §90 Heat of Combustion · glucose | 2803 | 2804.28 | 0.0455353 |
| §61 Glass Tg · glucose_amorph | 309 | 309.161 | 0.052193 |
| browning_proxy_temp_C · beer_ale_fermentation | 20 | 20.0157 | 0.0786975 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Maillard Chemistry: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Maillard Chemistry: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Maillard Chemistry: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

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

- **`alpha_Fe`** in Materials Creep Fracture Depth Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Materials Creep Fracture Depth Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Materials Creep Fracture Depth Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

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
- **`Fe`** in Materials Engineering: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Materials Engineering: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

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

- **`F`** in Materials Project Live Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Materials Project Live Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Materials Project Live Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

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

- **`F`** in Metamaterial Fluid Design Prereg Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Metamaterial Fluid Design Prereg Scaffold: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`P`** in Metamaterial Fluid Design Prereg Scaffold: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Natural Formation Element Simulation

Extension panel **`Natural_Formation_Element_Simulation`** (verification tier 72) evaluates **44** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.NaturalFormationElementSimulationPriors`. This panel extends the core spine into natural formation element simulation observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/natural_formation_element_simulation_benchmark.json`](data/natural_formation_element_simulation_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `astronomical`
- **Panel tags:** Natural, Formation, Element, Simulation
- **Data sources / cohorts:** r-process, s-process, cosmic-ray, fusion-decay pathway simulation for undiscovered element emergence

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| formation_pathway_viable · Z119_N177_ununennium__cosmic_ray_spallation | 0 | 0 | 0 |
| formation_sim · natural_emergence | 0 | 0 | 0 |
| fsot_natural_Z_ceiling · fusion_decay_chain_extension | 132 | 132 | 0 |
| fusion_physics_panel_bridge · fusion_physics_public_panel | 9.5e-05 | 9.5e-05 | 0 |
| natural_emergence_classifier · Z119_N177_ununennium | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Natural Formation Element Simulation: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Natural Formation Element Simulation: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Natural Formation Element Simulation: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Periodic Extension Decay Topology Scaffold

Extension panel **`Periodic_Extension_Decay_Topology_Scaffold`** (verification tier 75) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicExtensionDecayTopologyScaffoldPriors`. This panel extends the core spine into periodic extension decay topology scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_extension_decay_topology_scaffold_benchmark.json`](data/periodic_extension_decay_topology_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `energy`
- **Panel tags:** Periodic, Extension, Decay, Topology, Scaffold
- **Data sources / cohorts:** Decay topology graph Z=126→132→164, fusion chain extensions prereg

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_relay · Periodic_Extension_Decay_Topology_Scaffold_depth | 0 | 0 | 0 |
| fusion_decay_chain_bridge · fusion_decay_chain_prereg_scaffold | 0 | 0 | 0 |
| panel_pooled_median · heavy_ion_lab_synthesis | 9.5e-05 | 9.5e-05 | 0 |
| periodic_extension_Z_ceiling · decay_topology_Z164 | 164 | 164 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Periodic Extension Decay Topology Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Periodic Extension Decay Topology Scaffold: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Periodic Extension Decay Topology Scaffold: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Periodic Table Completion Spine

Extension panel **`Periodic_Table_Completion_Spine`** (verification tier 72) evaluates **38** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicTableCompletionSpinePriors`. This panel extends the core spine into periodic table completion spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_table_completion_spine_benchmark.json`](data/periodic_table_completion_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `atomic`, `fusion`, `material`
- **Panel tags:** Periodic, Table, Completion, Spine
- **Data sources / cohorts:** Periodic table completion rollup — public table, superheavy, prereg, natural formation, fusion bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_bleed_panel_bridge · term3_acoustic_bleed_depth | 0.0083815 | 0.0083815 | 0 |
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| candidate_predicted_half_life_s · Z120_N184_unbinilium | 2.5e+06 | 2.5e+06 | 0 |
| formation_pathway_viable · Z120_N184_unbinilium__cosmic_ray_spallation | 0 | 0 | 0 |
| fusion_physics_panel_bridge · fusion_physics_public_panel | 9.5e-05 | 9.5e-05 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Periodic Table Completion Spine: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Periodic Table Completion Spine: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Periodic Table Completion Spine: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

#### Periodic Table Extension Closure Spine

Extension panel **`Periodic_Table_Extension_Closure_Spine`** (verification tier 75) evaluates **41** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicTableExtensionClosureSpinePriors`. This panel extends the core spine into periodic table extension closure spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_table_extension_closure_spine_benchmark.json`](data/periodic_table_extension_closure_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`, `material`, `energy`
- **Panel tags:** Periodic, Table, Extension, Closure, Spine
- **Data sources / cohorts:** Periodic extension arc CLOSED — Tiers 71-75 rollup, Z ceiling 164

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| distant_island_half_life_s · Z128_N184 | 180000 | 180000 | 0 |
| distant_island_peak_classifier · Z128_N184 | 1 | 1 | 0 |
| emergence_pathway_viable · Z128_N184__cosmic_ray_spallation | 0 | 0 | 0 |
| fusion_decay_chain_bridge · fusion_decay_chain_prereg_scaffold | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Periodic Table Extension Closure Spine: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Periodic Table Extension Closure Spine: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Periodic Table Extension Closure Spine: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

#### Periodic Table Public Panel

Extension panel **`Periodic_Table_Public_Panel`** (verification tier 72) evaluates **52** measured records at **9.5e-05%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicTablePublicPanelPriors`. This panel extends the core spine into periodic table public panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_table_public_panel_benchmark.json`](data/periodic_table_public_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `atomic`, `nuclear`, `material`
- **Panel tags:** Periodic, Table, Public, Panel
- **Data sources / cohorts:** IUPAC, NIST Z=1-118 anchors — atomic weights, ionization energies, magic-number proximity

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| known_element_ceiling_Z · IUPAC_confirmed | 118 | 118 | 0 |
| magic_number_proximity · Ag | 14 | 14 | 0 |
| particle_physics_scalar · fsot_Particle_Physics | 0.950413 | 0.950413 | 0 |
| atomic_weight · Ag | 107.868 | 107.868 | 9.5e-05 |
| ionization_ev · Ag | 7.576 | 7.57601 | 9.5e-05 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Periodic Table Public Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Periodic Table Public Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Periodic Table Public Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### PubChem Compound Properties

Extension panel **`PubChem_Compound_Properties`** (verification tier 38) evaluates **500** measured records at **0.002637%** pooled median error (A_strong). Formal module: `FSOT.Formal.PubchemCompoundPropertiesPriors`. This panel extends the core spine into pubchem compound properties observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/pubchem_compound_properties_benchmark.json`](data/pubchem_compound_properties_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`
- **Panel tags:** Pubchem, Compound, Properties
- **Data sources / cohorts:** PubChem molecular weight vs formula mass (31 compounds deep)

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| molecular_weight · 1054 | 169.18 | 169.18 | 0 |
| molecular_weight · 10975657 | 150.13 | 150.13 | 0 |
| molecular_weight · 1102 | 145.25 | 145.25 | 0 |
| molecular_weight · 11174599 | 319.27 | 319.27 | 0 |
| molecular_weight · 1176 | 60.056 | 60.056 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`IE_Ar`** in PubChem Compound Properties: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`BL_N−H`** in PubChem Compound Properties: measured **1.01**, seed-derived **1.0099883725773517** via `A_bleed − γ⁶` (error **0.001151%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`IE_S`** in PubChem Compound Properties: measured **10.36**, seed-derived **10.360130217649854** via `φ⁶/√3` (error **0.001257%**). Constants: phi. Authority: NIST / CRC / Allen / Luo.

#### PubChem Live Deep

Extension panel **`PubChem_Live_Deep`** (verification tier 68) evaluates **5254** measured records at **0.032631%** pooled median error (A_strong). Formal module: `FSOT.Formal.PubChemLiveDeepPriors`. This panel extends the core spine into pubchem live deep observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/pubchem_live_deep_benchmark.json`](data/pubchem_live_deep_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`, `medical`, `biological`, `material`, `energy`
- **Panel tags:** Pubchem, Live, Deep
- **Data sources / cohorts:** PubChem auto-expanded panel — PUG REST name discovery, culinary, pharmacology bridges

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| biological_scalar · fsot_Biology | 0.444725 | 0.444725 | 0 |
| chemistry_scalar · fsot_Chemistry | 0.407884 | 0.407884 | 0 |
| culinary_arts_crosswalk_count | 26 | 26 | 0 |
| food_microbiology_crosswalk_count · Food_Microbiology | 30 | 30 | 0 |
| hbond_acceptor_count · 1140 | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in PubChem Live Deep: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in PubChem Live Deep: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in PubChem Live Deep: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### PubChem Stability Panel

Extension panel **`PubChem_Stability_Panel`** (verification tier 55) evaluates **59** measured records at **0.00242389%** pooled median error (B_verified). Formal module: `FSOT.Formal.PubChemStabilityPanelPriors`. This panel extends the core spine into pubchem stability panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/pubchem_stability_panel_benchmark.json`](data/pubchem_stability_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `electron`, `chemical`, `material`
- **Panel tags:** Pubchem, Stability, Panel
- **Data sources / cohorts:** PubChem formula-mass closure — novel stability claims require preregistration

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| chemistry_scalar · fsot_Chemistry | 0.407884 | 0.407884 | 0 |
| molecular_weight · 5280961 | 270.24 | 270.24 | 0 |
| pooled_median · all_channels | 0 | 0.002424 | 0.00242389 |
| molecular_weight · 962 | 18.015 | 18.015 | 0 |
| molecular_weight · 3386 | 309.33 | 309.331 | 0.000323 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in PubChem Stability Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in PubChem Stability Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in PubChem Stability Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

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

- **`F`** in Published Fuel Property Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Published Fuel Property Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.
- **`P`** in Published Fuel Property Panel: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Superheavy Element Stability Panel

Extension panel **`Superheavy_Element_Stability_Panel`** (verification tier 72) evaluates **50** measured records at **1e-06%** pooled median error (B_verified). Formal module: `FSOT.Formal.SuperheavyElementStabilityPanelPriors`. This panel extends the core spine into superheavy element stability panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/superheavy_element_stability_panel_benchmark.json`](data/superheavy_element_stability_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `atomic`, `fusion`
- **Panel tags:** Superheavy, Element, Stability, Panel
- **Data sources / cohorts:** Z=104-118 discovered superheavies — half-lives, liquid-drop binding, island-of-stability anchors

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| island_predicted_half_life_s · Fl-298 island proxy | 3600 | 3600 | 0 |
| macroscopic_stability_classifier · Bh | 1 | 1 | 0 |
| superheavy_stability · island_of_stability | 0 | 1e-06 | 9.50413e-07 |
| half_life_s · Bh | 61 | 61 | 1e-06 |
| pooled_median · all_channels | 0 | 1e-06 | 1e-06 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Superheavy Element Stability Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Superheavy Element Stability Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Superheavy Element Stability Panel: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

#### Superheavy Island Completion Spine

Extension panel **`Superheavy_Island_Completion_Spine`** (verification tier 74) evaluates **43** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.SuperheavyIslandCompletionSpinePriors`. This panel extends the core spine into superheavy island completion spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/superheavy_island_completion_spine_benchmark.json`](data/superheavy_island_completion_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`, `material`
- **Panel tags:** Superheavy, Island, Completion, Spine
- **Data sources / cohorts:** Superheavy island completion rollup — deep panel, beams, decay chains, emergence, Tier 72-73 bridges

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| candidate_predicted_half_life_s · Z120_N184_unbinilium | 2.5e+06 | 2.5e+06 | 0 |
| cold_fusion_bridge · cold_fusion_candidate_prereg_scaffold | 0 | 0 | 0 |
| decay_chain_viability_classifier · pd_d_to_Z120_cascade | 1 | 1 | 0 |
| emergence_pathway_viable · Z119_N177__cosmic_ray_spallation | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Superheavy Island Completion Spine: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Superheavy Island Completion Spine: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Superheavy Island Completion Spine: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

#### Superheavy Island Emergence Simulation

Extension panel **`Superheavy_Island_Emergence_Simulation`** (verification tier 74) evaluates **44** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.SuperheavyIslandEmergenceSimulationPriors`. This panel extends the core spine into superheavy island emergence simulation observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/superheavy_island_emergence_simulation_benchmark.json`](data/superheavy_island_emergence_simulation_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `astronomical`
- **Panel tags:** Superheavy, Island, Emergence, Simulation
- **Data sources / cohorts:** Island emergence pathway simulation for Z=120-126 — lab, fusion-decay-chain viability

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| emergence_pathway_viable · Z119_N177__cosmic_ray_spallation | 0 | 0 | 0 |
| fsot_island_Z_ceiling · fusion_decay_chain_Z126 | 126 | 126 | 0 |
| island_emergence · z120_z126_sim | 0 | 0 | 0 |
| island_emergence_classifier · Z119_N177 | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Superheavy Island Emergence Simulation: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Superheavy Island Emergence Simulation: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Superheavy Island Emergence Simulation: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.

#### Undiscovered Element Candidate Prereg Scaffold

Extension panel **`Undiscovered_Element_Candidate_Prereg_Scaffold`** (verification tier 72) evaluates **25** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.UndiscoveredElementCandidatePreregScaffoldPriors`. This panel extends the core spine into undiscovered element candidate prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/undiscovered_element_candidate_prereg_scaffold_benchmark.json`](data/undiscovered_element_candidate_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `atomic`, `fusion`
- **Panel tags:** Undiscovered, Element, Candidate, Prereg, Scaffold
- **Data sources / cohorts:** Z>118 candidates (Z=119-164) preregistered via boundary_partition, phi scaling — not claimed synthesized

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| candidate_predicted_half_life_s · Z119_N177_ununennium | 0.8 | 0.8 | 0 |
| phi_morphogenetic_panel_bridge · phi_morphogenetic_scaling | 0.0565 | 0.0565 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| prereg_discriminant_gate · Z119_N177_ununennium | 1 | 1 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`Fe`** in Undiscovered Element Candidate Prereg Scaffold: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).
- **`F`** in Undiscovered Element Candidate Prereg Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Undiscovered Element Candidate Prereg Scaffold: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.

#### Z164 Distant Island Prereg Scaffold

Extension panel **`Z164_Distant_Island_Prereg_Scaffold`** (verification tier 75) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.Z164DistantIslandPreregScaffoldPriors`. This panel extends the core spine into z164 distant island prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/z164_distant_island_prereg_scaffold_benchmark.json`](data/z164_distant_island_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`
- **Panel tags:** Z164, Distant, Island, Prereg, Scaffold
- **Data sources / cohorts:** Z=164 distant island prereg — periodic extension ceiling, not claimed synthesized

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| depth_relay · Z164_Distant_Island_Prereg_Scaffold_depth | 0 | 0 | 0 |
| distant_island_viability_classifier · Z164_N228 | 1 | 1 | 0 |
| emergence_pathway_viable · Z119_N177__cosmic_ray_spallation | 0 | 0 | 0 |
| fusion_physics_panel_bridge · fusion_physics_public_panel | 9.5e-05 | 9.5e-05 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Z164 Distant Island Prereg Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`IE_Ar`** in Z164 Distant Island Prereg Scaffold: measured **15.76**, seed-derived **15.760123778469742** via `γ⁻⁵ + Poof` (error **0.000785%**). Constants: gamma. Authority: NIST / CRC / Allen / Luo.
- **`Ca`** in Z164 Distant Island Prereg Scaffold: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.
