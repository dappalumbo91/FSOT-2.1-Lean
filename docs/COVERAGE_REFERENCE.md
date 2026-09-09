# Coverage reference — what the program actually solves

*Generated 2026-09-09T23:06:48Z · pin D1D38A*

**Refresh:** `python scripts/build_coverage_reference.py`

This is the **coverage ledger**, not a second theory.
Green-file count **477/477** is what Label A scores.
The 35 cores are the folds. Extensions are subdomains of a fold.
Do not mix this with atlas-row (~403) or scalar-record (181,477) counts —
see [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md).

The flagship checklist paper cites this page. It does **not** reprint 477 files.

## Snapshot

| Ledger | Live |
|--------|-----:|
| Green residual files | **477/477** |
| Fail | **0** |
| Unique domain names in the audit | 475 |
| Core folds | 35 |
| Extension subdomains | 375 |
| Atlas named rows | 403 |

## Core folds (the 35 interfaces)

| Core | D_eff | observed | Band | Child extensions |
|------|------:|:--------:|------|-----------------:|
| **Particle_Physics** | 5 | yes | D=5–8 micro / bond / observer-on | 0 |
| **Quantum_Mechanics** | 6 | yes | D=5–8 micro / bond / observer-on | 0 |
| **Atomic_Physics** | 7 | yes | D=5–8 micro / bond / observer-on | 2 |
| **High_Energy_Physics** | 7 | yes | D=5–8 micro / bond / observer-on | 0 |
| **Chemistry** | 8 | yes | D=5–8 micro / bond / observer-on | 4 |
| **Physical_Chemistry** | 8 | yes | D=5–8 micro / bond / observer-on | 0 |
| **Electromagnetism** | 9 | yes | D=9–11 look / compute / sound | 3 |
| **Molecular_Chemistry** | 9 | yes | D=9–11 look / compute / sound | 0 |
| **Acoustics** | 10 | yes | D=9–11 look / compute / sound | 4 |
| **Materials_Science** | 10 | yes | D=9–11 look / compute / sound | 0 |
| **Optics** | 10 | yes | D=9–11 look / compute / sound | 0 |
| **Quantum_Computing** | 11 | dark | D=9–11 look / compute / sound | 5 |
| **Quantum_Optics** | 11 | yes | D=9–11 look / compute / sound | 0 |
| **Biology** | 12 | dark | D=12–16 life / fluid / weather | 21 |
| **Biochemistry** | 13 | yes | D=12–16 life / fluid / weather | 14 |
| **Condensed_Matter** | 14 | yes | D=12–16 life / fluid / weather | 47 |
| **Neuroscience** | 14 | yes | D=12–16 life / fluid / weather | 0 |
| **Ecology** | 15 | dark | D=12–16 life / fluid / weather | 36 |
| **Fluid_Dynamics** | 15 | dark | D=12–16 life / fluid / weather | 0 |
| **Nuclear_Physics** | 15 | yes | D=12–16 life / fluid / weather | 0 |
| **Thermodynamics** | 15 | yes | D=12–16 life / fluid / weather | 0 |
| **Meteorology** | 16 | dark | D=12–16 life / fluid / weather | 44 |
| **Psychology** | 16 | yes | D=12–16 life / fluid / weather | 0 |
| **Atmospheric_Physics** | 17 | dark | D=17–21 bulk / catalogs | 59 |
| **Oceanography** | 17 | dark | D=17–21 bulk / catalogs | 0 |
| **Seismology** | 18 | dark | D=17–21 bulk / catalogs | 40 |
| **Sociology** | 18 | yes | D=17–21 bulk / catalogs | 0 |
| **Geophysics** | 19 | dark | D=17–21 bulk / catalogs | 22 |
| **Astronomy** | 20 | yes | D=17–21 bulk / catalogs | 27 |
| **Economics** | 20 | yes | D=17–21 bulk / catalogs | 0 |
| **Planetary_Science** | 21 | yes | D=17–21 bulk / catalogs | 11 |
| **Quantum_Gravity** | 22 | dark | D=22–25 deep / ceiling | 13 |
| **Astrophysics** | 24 | yes | D=22–25 deep / ceiling | 6 |
| **Particle_Astrophysics** | 24 | dark | D=22–25 deep / ceiling | 0 |
| **Cosmology** | 25 | dark | D=22–25 deep / ceiling | 17 |

## Bands

- **D=5–8 — micro / bond / observer-on** (6 cores). Particle, QM, chemistry — form at the small orifice
- **D=9–11 — look / compute / sound** (7 cores). EM, optics, acoustics; QC stays dark on purpose
- **D=12–16 — life / fluid / weather** (10 cores). Biology through meteorology — viscosity and C_factor
- **D=17–21 — bulk / catalogs** (8 cores). Atmosphere, ocean, rock, planets, astronomy
- **D=22–25 — deep / ceiling** (4 cores). QG, particle-astro, astrophysics, cosmology at D=25

## Green files (reviewable list)

Each row is one residual panel. Pooled median ≤ 0.5% is the official gate.

| File | Domain | Records | Pooled % |
|------|--------|--------:|---------:|
| `acoustic_resonance_materials_benchmark.json` | Acoustic_Resonance_Materials | 29 | 0.008381 |
| `actuarial_science_panel_benchmark.json` | Actuarial_Science_Panel | 60 | 0.022610 |
| `adjacent_rung_coupling_benchmark.json` | Adjacent_Rung_Coupling | 36 | 0.029433 |
| `adversarial_fractal_break_benchmark.json` | Adversarial_Fractal_Break_Tests | 13 | 0.000000 |
| `agriculture_agroecology_gap_fill_benchmark.json` | Agriculture_Agroecology | 276 | 0.018019 |
| `ai_galactic_orbital_bridge_benchmark.json` | AI_Galactic_Orbital_Bridge | 48 | 0.005169 |
| `alphafold_batch_meta_open_benchmark.json` | AlphaFold_Batch_Meta_Open | 182 | 0.015311 |
| `alternate_base_mathematics_explorer_panel_benchmark.json` | Alternate_Base_Mathematics_Explorer_Panel | 56 | 0.009504 |
| `alternate_base_mathematics_spine_benchmark.json` | Alternate_Base_Mathematics_Spine | 21 | 0.000000 |
| `anthropology_extension_benchmark.json` | Anthropology | 160 | -0.000787 |
| `architecture_building_science_gap_fill_benchmark.json` | Architecture_Building_Science | 43 | 0.078697 |
| `arxiv_brain_knowledge_panel_benchmark.json` | Arxiv_Brain_Knowledge_Panel | 20 | 0.018003 |
| `arxiv_gravitational_waves_panel_benchmark.json` | Arxiv_Gravitational_Waves_Panel | 60 | 0.017480 |
| `arxiv_primitives_panel_benchmark.json` | Arxiv_Primitives_Panel | 22 | 0.031506 |
| `arxiv_primitives_v14_benchmark.json` | Arxiv_Primitives_V14 | 21 | 0.000055 |
| `astrophysical_structure_crosswalk_benchmark.json` | Astrophysical_Structure_Crosswalk | 24 | 0.000000 |
| `atmospheric_physics_gap_fill_benchmark.json` | Atmospheric_Physics | 47 | 0.000000 |
| `atomic_physics_gap_fill_benchmark.json` | Atomic_Physics | 80 | 0.000950 |
| `between_scale_interconnect_benchmark.json` | Between_Scale_Interconnects | 7719 | 0.027455 |
| `bibliography_corpus_panel_benchmark.json` | Bibliography_Corpus_Panel | 20 | 0.013294 |
| `bibliography_lean_corpus_benchmark.json` | Bibliography_Lean_Corpus | 23 | 0.000562 |
| `binary_decoder_panel_benchmark.json` | Binary_Decoder_Panel | 20 | 0.000022 |
| `binary_decoder_rendlesham_benchmark.json` | Binary_Decoder_Rendlesham | 21 | 0.000055 |
| `biological_cuda_physarum_benchmark.json` | biological_cuda_physarum_benchmark | 34 | 0.000000 |
| `biology_developmental_structural_depth_panel_benchmark.json` | Biology_Developmental_Structural_Depth_Panel | 24 | 0.015311 |
| `biophysics_public_panel_benchmark.json` | Biophysics_Public_Panel | 24 | 0.000000 |
| `blackhole_whitehole_cycle_live_panel_benchmark.json` | BlackHole_WhiteHole_Cycle_Live_Panel | 24 | 0.026472 |
| `botany_extension_benchmark.json` | Botany | 426 | 0.022236 |
| `boundary_partition_tightening_benchmark.json` | Boundary_Partition_Tightening | 24 | 0.000000 |
| `breakthrough_discoveries_2024_2026_benchmark.json` | Breakthrough_Discoveries_2024_2026 | 21 | 0.000000 |
| `breakthrough_fusion_spine_benchmark.json` | Breakthrough_Fusion_Spine | 146 | 0.000000 |
| `canonical_oracle_panel_benchmark.json` | Canonical_Oracle_Panel | 24 | 0.000562 |
| `cardiology_extension_benchmark.json` | Cardiology | 45 | 0.030622 |
| `cardiology_panel_benchmark.json` | Cardiology_Panel | 20 | 0.015311 |
| `cartography_gis_panel_benchmark.json` | Cartography_GIS_Panel | 48 | 0.018856 |
| `cepheid_pl_interconnect_benchmark.json` | Cepheid_PL_Interconnect | 12 | 0.134988 |
| `cern_open_data_lhc_benchmark.json` | CERN_Open_Data_LHC | 83 | 0.013294 |
| `certified_agent_formal_panel_benchmark.json` | Certified_Agent_Formal_Panel | 21 | 0.014767 |
| `certified_agent_qwen_benchmark.json` | Certified_Agent_Qwen | 21 | 0.000055 |
| `chaos_mediated_phase_transitions_benchmark.json` | Chaos_Mediated_Phase_Transitions | 21 | 0.031479 |
| `chembl_deep_open_benchmark.json` | ChEMBL_Deep_Open | 188 | 0.040788 |
| `chemical_engineering_extension_benchmark.json` | Chemical_Engineering | 186 | 0.001022 |
| `chemical_structure_stability_panel_benchmark.json` | Chemical_Structure_Stability_Panel | 32 | 0.002060 |
| `circuit_component_emergence_panel_benchmark.json` | Circuit_Component_Emergence_Panel | 57 | 0.020755 |
| `civil_engineering_extension_benchmark.json` | Civil_Engineering | 37 | 0.033526 |
| `civil_engineering_panel_benchmark.json` | Civil_Engineering_Panel | 20 | 0.013410 |
| `climate_observed_benchmark.json` | climate_observed_benchmark | 17325 | 0.012013 |
| `clinical_medicine_extension_benchmark.json` | Clinical_Medicine | 260 | 0.002458 |
| `clinicaltrials_medical_panel_benchmark.json` | ClinicalTrials_Medical_Panel | 394 | 0.000000 |
| `cod_optimade_structures_benchmark.json` | COD_OPTIMADE_Structures | 682 | 0.013410 |
| `codata_full_table_open_benchmark.json` | CODATA_Full_Table_Open | 38 | 0.073582 |
| `code_genome_structure_cybersecurity_benchmark.json` | Code_Genome_Structure | 176 | 0.000000 |
| `coding_structure_verifier_panel_benchmark.json` | Coding_Structure_Verifier_Panel | 43 | 0.000000 |
| `cold_fusion_candidate_prereg_scaffold_benchmark.json` | Cold_Fusion_Candidate_Prereg_Scaffold | 24 | 0.000000 |
| `cold_fusion_lab_synthesis_crosswalk_benchmark.json` | Cold_Fusion_Lab_Synthesis_Crosswalk | 49 | 0.000079 |
| `compact_object_binary_events_benchmark.json` | Compact_Object_Binary_Events | 40 | 0.010049 |
| `compactification_ladder_benchmark.json` | Compactification_Ladder | 60 | 0.015074 |
| `complexity_folding_emergence_panel_benchmark.json` | Complexity_Folding_Emergence_Panel | 29 | 0.026588 |
| `computational_reasoning_benchmark.json` | computational_reasoning_benchmark.json | 577 | 0.000000 |
| `condensed_matter_superconductivity_depth_panel_benchmark.json` | Condensed_Matter_Superconductivity_Depth_Panel | 24 | 0.033841 |
| `consciousness_econ_benchmark.json` | Consciousness_Econ | 32 | 0.020728 |
| `consciousness_expansion_spine_benchmark.json` | Consciousness_Expansion_Spine | 24 | 0.000000 |
| `consciousness_galactic_orbital_bridge_benchmark.json` | Consciousness_Galactic_Orbital_Bridge | 48 | 0.036757 |
| `consciousness_genetics_coupling_panel_benchmark.json` | Consciousness_Genetics_Coupling_Panel | 24 | 0.031506 |
| `consciousness_genetics_species_panel_benchmark.json` | Consciousness_Genetics_Species_Panel | 27 | 0.022236 |
| `consciousness_lean_route_credibility_benchmark.json` | Consciousness_Lean_Route_Credibility | 101 | 0.018003 |
| `consciousness_soul_bridge_benchmark.json` | Consciousness_Soul_Bridge | 24 | 0.000000 |
| `consciousness_species_multi_panel_benchmark.json` | Consciousness_Species_Multi_Panel | 269 | 0.020119 |
| `cosmology_anomalies_benchmark.json` | cosmology_anomalies | 28 | 0.015148 |
| `cosmology_anomaly_deep_panel_benchmark.json` | Cosmology_Anomaly_Deep_Panel | 24 | 0.000000 |
| `cosmology_bubble_bleed_benchmark.json` | cosmology_bubble_bleed_benchmark | 110 | 0.000000 |
| `cosmology_extended_benchmark.json` | Cosmology_Extended | 23 | 0.000562 |
| `crc_handbook_properties_benchmark.json` | CRC_Handbook_Properties | 391 | 0.026922 |
| `creative_arts_math_spine_benchmark.json` | Creative_Arts_Math_Spine | 56 | 0.000000 |
| `cross_proof_verification_benchmark.json` | Cross_Proof_Verification_Spine | 0 | 0.000000 |
| `crossref_scholarly_panel_benchmark.json` | Crossref_Scholarly_Panel | 200 | 0.013820 |
| `cryosphere_benchmark.json` | cryosphere_benchmark.json | 2399 | 0.000000 |
| `cryptography_technology_cybersecurity_benchmark.json` | Cryptography_Technology | 44 | 0.000000 |
| `culinary_arts_benchmark.json` | culinary_arts_benchmark.json | 52 | 0.047615 |
| `culinary_fermentation_maillard_panel_benchmark.json` | Culinary_Fermentation_Maillard_Panel | 151 | 0.040788 |
| `cve_codon_hole_falsification_benchmark.json` | CVE_Codon_Hole_Falsification | 29 | 0.009187 |
| `dark_energy_cpl_benchmark.json` | Dark_Energy_CPL | 20 | 0.001816 |
| `dark_sector_open_problems_benchmark.json` | Dark_Sector_Open_Problems | 24 | 0.000562 |
| `desi_edr_fits_residual_benchmark.json` | DESI_EDR_FITS_Residual | 97144 | 0.022461 |
| `desi_edr_table_slice_open_benchmark.json` | DESI_EDR_Table_Slice_Open | 22 | 0.010049 |
| `desi_public_depth_open_benchmark.json` | DESI_Public_Depth_Open | 20 | 0.010049 |
| `desi_wa_constraint_benchmark.json` | DESI_wa_Constraint | 27 | 0.000000 |
| `desktop_application_wiring_spine_benchmark.json` | Desktop_Application_Wiring_Spine | 81 | 0.000000 |
| `desktop_observer_loop_panel_benchmark.json` | Desktop_Observer_Loop_Panel | 24 | 0.001025 |
| `distant_island_emergence_simulation_benchmark.json` | Distant_Island_Emergence_Simulation | 26 | 0.000000 |
| `distant_island_z128_z132_deep_panel_benchmark.json` | Distant_Island_Z128_Z132_Deep_Panel | 24 | 0.000000 |
| `domain_coupling_simulation_benchmark.json` | Domain_Coupling_Simulation | 18617 | 0.000000 |
| `domain_coupling_simulation_refresh_panel_benchmark.json` | Domain_Coupling_Simulation_Refresh_Panel | 22 | 0.000000 |
| `domain_orbital_predictions_benchmark.json` | Domain_Orbital_Predictions | 12 | 0.000000 |
| `dzhanibekov_intermediate_axis_fsot_panel_benchmark.json` | Dzhanibekov_Intermediate_Axis_FSOT_Panel | 32 | 0.000000 |
| `early_lean_mc_panel_benchmark.json` | Early_Lean_MC_Panel | 21 | 0.000022 |
| `ecology_benchmark.json` | Ecology | 24 | 0.000000 |
| `ecology_gap_fill_benchmark.json` | Ecology | 627 | 0.017789 |
| `econometrics_gap_fill_benchmark.json` | Econometrics | 172 | 0.129201 |
| `economics_gap_fill_benchmark.json` | Economics | 157 | 0.129201 |
| `econophysics_benchmark.json` | Econophysics | 24 | 0.000000 |
| `electrical_power_systems_benchmark.json` | Electrical_Power_Systems | 23 | 0.000562 |
| `element_synthesis_condition_scaffold_benchmark.json` | Element_Synthesis_Condition_Scaffold | 45 | 0.000787 |
| `emergent_domains_benchmark.json` | emergent_domains_benchmark.json | 29 | None |
| `endf_iaea_nuclear_open_benchmark.json` | ENDF_IAEA_Nuclear_Open | 517 | 0.046065 |
| `energy_ai_orbital_bridge_benchmark.json` | Energy_AI_Orbital_Bridge | 48 | 0.027544 |
| `energy_lean_route_credibility_benchmark.json` | Energy_Lean_Route_Credibility | 40 | 0.039349 |
| `energy_neural_orbital_bridge_benchmark.json` | Energy_Neural_Orbital_Bridge | 48 | 0.018003 |
| `engineering_hardware_code_spine_benchmark.json` | Engineering_Hardware_Code_Spine | 93 | 0.000000 |
| `entomology_extension_benchmark.json` | Entomology | 430 | 0.020013 |
| `entomology_panel_benchmark.json` | Entomology_Panel | 90 | 0.006006 |
| `environmental_engineering_extension_benchmark.json` | Environmental_Engineering | 1117 | 0.009010 |
| `epidemiology_extension_benchmark.json` | Epidemiology | 20 | 0.030622 |
| `epidemiology_panel_benchmark.json` | Epidemiology_Panel | 24 | 0.015311 |
| `esp32_platform_engineering_panel_benchmark.json` | ESP32_Platform_Engineering_Panel | 34 | 0.020755 |
| `ethology_panel_benchmark.json` | Ethology_Panel | 100 | 0.006607 |
| `evolution_operon_benchmark.json` | Evolution_Operon | 20 | 0.000000 |
| `existence_simulation_gap_fill_panel_benchmark.json` | Existence_Simulation_Gap_Fill_Panel | 20 | 0.000039 |
| `existence_simulation_refinement_panel_benchmark.json` | Existence_Simulation_Refinement_Panel | 26 | 0.014120 |
| `exogeology_extension_benchmark.json` | Exogeology | 316 | 0.000000 |
| `exogeology_panel_benchmark.json` | Exogeology_Panel | 100 | 0.026472 |
| `exoplanet_archive_depth_open_benchmark.json` | Exoplanet_Archive_Depth_Open | 1976 | 0.023015 |
| `exoplanet_system_architecture_benchmark.json` | Exoplanet_System_Architecture | 882 | 0.000000 |
| `experimental_base_mathematics_panel_benchmark.json` | Experimental_Base_Mathematics_Panel | 36 | 0.009504 |
| `external_oss_code_genome_benchmark.json` | External_OSS_Code_Genome | 161 | 0.000000 |
| `federal_science_registry_panel_benchmark.json` | Federal_Science_Registry_Panel | 24 | 0.013294 |
| `finance_markets_extension_benchmark.json` | Finance_Markets | 150 | 0.025840 |
| `finance_markets_panel_benchmark.json` | Finance_Markets_Panel | 36 | 0.025840 |
| `fluid_dynamics_gap_fill_benchmark.json` | Fluid_Dynamics | 55 | 0.000000 |
| `fluid_phase_current_spine_benchmark.json` | Fluid_Phase_Current_Spine | 24 | 0.000039 |
| `fluid_spacetime_observable_spine_benchmark.json` | Fluid_Spacetime_Observable_Spine | 29 | 0.011116 |
| `fluid_spacetime_prereg_validation_panel_benchmark.json` | Fluid_Spacetime_Prereg_Validation_Panel | 20 | 0.000000 |
| `fold_depth_metrics_benchmark.json` | Fold_Depth_Metrics | 51 | 0.025754 |
| `food_microbiology_gap_fill_benchmark.json` | Food_Microbiology | 30 | 0.044473 |
| `formula_branching_fractal_benchmark.json` | Formula_Branching_Fractal | 380 | 0.038017 |
| `formula_corpus_closure_benchmark.json` | Formula_Corpus_Closure | 203 | 0.009504 |
| `formula_corpus_cnc_benchmark.json` | Formula_Corpus_CNC | 23 | 0.000562 |
| `formula_precision_spine_benchmark.json` | Formula_Precision_Spine | 26 | 0.000000 |
| `foundational_ontology_spine_benchmark.json` | Foundational_Ontology_Spine | 60 | 0.009504 |
| `founding_atmospheric_ozone_panel_benchmark.json` | Founding_Atmospheric_Ozone_Panel | 20 | 0.023822 |
| `founding_cosmic_dust_panel_benchmark.json` | Founding_Cosmic_Dust_Panel | 20 | 0.044121 |
| `founding_cosmic_ray_panel_benchmark.json` | Founding_Cosmic_Ray_Panel | 20 | 0.021221 |
| `founding_galactic_halo_rotation_panel_benchmark.json` | Founding_Galactic_Halo_Rotation_Panel | 20 | 0.025123 |
| `founding_pulsar_glitch_panel_benchmark.json` | Founding_Pulsar_Glitch_Panel | 20 | 0.044923 |
| `founding_quantum_vacuum_panel_benchmark.json` | Founding_Quantum_Vacuum_Panel | 20 | 0.047775 |
| `founding_white_dwarf_cooling_panel_benchmark.json` | Founding_White_Dwarf_Cooling_Panel | 20 | 0.044923 |
| `fpc_fluidlink_timing_deep_panel_benchmark.json` | FPC_Fluidlink_Timing_Deep_Panel | 24 | 0.000011 |
| `fpc_temporal_coupling_benchmark.json` | FPC_Temporal_Coupling | 24 | 0.000638 |
| `fractal_constant_recursion_benchmark.json` | Fractal_Constant_Recursion | 21 | 0.000000 |
| `frb_orifice_outgassing_benchmark.json` | FRB_Orifice_Outgassing | 3396 | 0.000000 |
| `fsot_aggregate_organized_panel_benchmark.json` | FSOT_Aggregate_Organized_Panel | 24 | 0.000000 |
| `fsot_aggregate_unified_db_benchmark.json` | FSOT_Aggregate_Unified_DB | 23 | 0.000562 |
| `fsot_c_pack_parity_panel_benchmark.json` | FSOT_C_Pack_Parity_Panel | 24 | 0.000000 |
| `fsot_cache_hierarchy_panel_benchmark.json` | FSOT_Cache_Hierarchy_Panel | 61 | 0.000000 |
| `fsot_gpu_cuda_competitive_panel_benchmark.json` | FSOT_GPU_CUDA_Competitive_Panel | 27 | 0.000000 |
| `fsot_gpu_engineering_spine_benchmark.json` | FSOT_GPU_Engineering_Spine | 40 | 0.000000 |
| `fsot_gpu_parity_verify_panel_benchmark.json` | FSOT_GPU_Parity_Verify_Panel | 48 | 0.000000 |
| `fsot_hardware_depth_spine_benchmark.json` | FSOT_Hardware_Depth_Spine | 170 | 0.000000 |
| `fsot_interconnect_coherence_panel_benchmark.json` | FSOT_Interconnect_Coherence_Panel | 62 | 0.000000 |
| `fsot_physics_all_solved_benchmark.json` | FSOT_Physics_All_Solved | 287 | 0.009504 |
| `fsot_processor_function_panel_benchmark.json` | FSOT_Processor_Function_Panel | 24 | 0.000000 |
| `fsot_ram_function_panel_benchmark.json` | FSOT_RAM_Function_Panel | 32 | 0.000000 |
| `fuel_candidate_prereg_scaffold_benchmark.json` | Fuel_Candidate_Prereg_Scaffold | 33 | 0.000000 |
| `fuel_lab_live_panel_benchmark.json` | Fuel_Lab_Live_Panel | 366 | 0.039349 |
| `fuel_thermochemistry_public_anchors_benchmark.json` | Fuel_Thermochemistry_Public_Anchors | 24 | 0.000000 |
| `fusion_decay_chain_prereg_scaffold_benchmark.json` | Fusion_Decay_Chain_Prereg_Scaffold | 24 | 0.000000 |
| `fusion_lab_certificate_spine_benchmark.json` | Fusion_Lab_Certificate_Spine | 50 | 0.000000 |
| `fusion_lean_route_credibility_benchmark.json` | Fusion_Lean_Route_Credibility | 81 | 0.009504 |
| `fusion_physics_public_panel_benchmark.json` | Fusion_Physics_Public_Panel | 24 | 0.000095 |
| `gaia_astrometry_panel_deep_benchmark.json` | Gaia_Astrometry_Panel_Deep | 62 | 0.022461 |
| `gaia_dr3_source_sample_open_benchmark.json` | Gaia_DR3_Source_Sample_Open | 3459 | 0.022461 |
| `gaia_dr3_tap_deep_benchmark.json` | Gaia_DR3_TAP_Deep | 1826 | 0.022461 |
| `galactic_structure_sample_benchmark.json` | Galactic_Structure_Sample | 101 | 0.000000 |
| `gbif_species_occurrence_benchmark.json` | GBIF_Species_Occurrence | 240 | 0.006006 |
| `gbif_taxon_depth_open_benchmark.json` | GBIF_Taxon_Depth_Open | 203 | 0.006006 |
| `genomic_sciences_benchmark.json` | Genomic_Sciences | 24 | 0.000000 |
| `geochemistry_benchmark.json` | geochemistry_benchmark.json | 153 | 0.006625 |
| `geology_stratigraphy_extension_benchmark.json` | Geology_Stratigraphy | 1957 | 0.000000 |
| `geomagnetism_benchmark.json` | geomagnetism_benchmark.json | 524 | 0.000000 |
| `government_open_data_spine_benchmark.json` | Government_Open_Data_Spine | 28 | 0.000000 |
| `grace_cryosphere_benchmark.json` | grace_cryosphere_benchmark.json | 505 | 0.023015 |
| `gwas_catalog_depth_open_benchmark.json` | GWAS_Catalog_Depth_Open | 81 | 0.022236 |
| `gwosc_live_event_deep_benchmark.json` | GWOSC_Live_Event_Deep | 185 | 0.008488 |
| `gwosc_strain_metadata_open_benchmark.json` | GWOSC_Strain_Metadata_Open | 54 | 0.008488 |
| `gwtc_catalog_open_benchmark.json` | GWTC_Catalog_Open | 1972 | 0.008488 |
| `h0_planck_benchmark.json` | H0_Planck_CMB_Sector | 20 | 0.000000 |
| `heavy_ion_lab_synthesis_panel_benchmark.json` | Heavy_Ion_Lab_Synthesis_Panel | 39 | 0.000095 |
| `higgs_branching_benchmark.json` | Higgs_Branching | 27 | 0.000000 |
| `higgs_mass_benchmark.json` | higgs_mass | 23 | 0.039905 |
| `history_extension_benchmark.json` | History | 170 | 0.019504 |
| `history_panel_benchmark.json` | History_Panel | 60 | 0.013820 |
| `hubble_bubble_tension_benchmark.json` | Hubble_Bubble_Tension | 21 | 0.000000 |
| `hubble_dark_sector_crosswalk_benchmark.json` | Hubble_Dark_Sector_Crosswalk | 32 | 0.004253 |
| `hvac_thermal_systems_benchmark.json` | HVAC_Thermal_Systems | 23 | 0.000562 |
| `hybrid_fi_sim_multi_hero_panel_benchmark.json` | Hybrid_FI_Sim_Multi_Hero_Panel | 32 | 0.000000 |
| `hybrid_fi_sim_stratum_deep_panel_benchmark.json` | Hybrid_FI_Sim_Stratum_Deep_Panel | 24 | 0.015311 |
| `hydrology_benchmark.json` | hydrology_benchmark | 957 | 0.000000 |
| `igem_live_fasta_benchmark.json` | igem_live_fasta_benchmark.json | 42 | 0.000000 |
| `igem_parts_expanded_benchmark.json` | IGEM_Parts_Expanded | 111 | 0.000059 |
| `igem_synthetic_biology_benchmark.json` | igem_synthetic_biology_benchmark.json | 54 | 0.022236 |
| `immunology_benchmark.json` | immunology_benchmark.json | 84 | 0.060854 |
| `immunology_panel_benchmark.json` | Immunology_Panel | 24 | 0.040788 |
| `inaturalist_observation_panel_benchmark.json` | iNaturalist_Observation_Panel | 288 | 0.006006 |
| `inertial_confinement_fusion_panel_benchmark.json` | Inertial_Confinement_Fusion_Panel | 24 | 0.000000 |
| `information_theory_public_panel_benchmark.json` | Information_Theory_Public_Panel | 21 | 0.000000 |
| `initiation_transformation_archetype_benchmark.json` | Initiation_Transformation_Archetype | 23 | 0.000000 |
| `intelligence_compression_benchmark.json` | Intelligence_Compression | 87 | 0.018003 |
| `interactive_media_prereg_scaffold_benchmark.json` | Interactive_Media_Prereg_Scaffold | 42 | 0.000000 |
| `interdisciplinary_spine_crosswalk_benchmark.json` | Interdisciplinary_Spine_Crosswalk | 24 | 0.000000 |
| `intrinsic_llm_validators_benchmark.json` | Intrinsic_LLM_Validators | 21 | 0.000055 |
| `ionospheric_chemistry_coupling_benchmark.json` | Ionospheric_Chemistry_Coupling | 85 | 0.023609 |
| `island_of_stability_deep_panel_benchmark.json` | Island_Of_Stability_Deep_Panel | 23 | 0.000001 |
| `jarvis_dft_open_panel_benchmark.json` | JARVIS_DFT_Open_Panel | 77 | 0.013410 |
| `knowledge_base_portable_bundle_panel_benchmark.json` | Knowledge_Base_Portable_Bundle_Panel | 23 | 0.000000 |
| `lab_synthesis_metamaterial_spine_benchmark.json` | Lab_Synthesis_Metamaterial_Spine | 43 | 0.000095 |
| `law_policy_extension_benchmark.json` | Law_Policy | 180 | 0.019504 |
| `law_policy_panel_benchmark.json` | Law_Policy_Panel | 20 | 0.013003 |
| `limnology_panel_benchmark.json` | Limnology_Panel | 2010 | 0.030173 |
| `linguistics_formal_benchmark.json` | Linguistics_Formal | 23 | 0.000562 |
| `live_ingest_spine_benchmark.json` | Live_Ingest_Spine | 28 | 0.000000 |
| `living_fsot_hardware_benchmark.json` | Living_FSOT_Hardware | 4 | 0.000000 |
| `living_fsot_hardware_panel_benchmark.json` | Living_FSOT_Hardware_Panel | 152 | 0.014767 |
| `lmfdb_elliptic_curves_open_benchmark.json` | LMFDB_Elliptic_Curves_Open | 1016 | 0.014767 |
| `lmfdb_oeis_math_open_benchmark.json` | LMFDB_OEIS_Math_Open | 3918 | 0.014767 |
| `longevity_anage_catalog_panel_benchmark.json` | Longevity_AnAge_Catalog_Panel | 966 | 0.022236 |
| `longevity_consciousness_coupling_panel_benchmark.json` | Longevity_Consciousness_Coupling_Panel | 890 | 0.022424 |
| `longevity_extreme_species_panel_benchmark.json` | Longevity_Extreme_Species_Panel | 164 | 0.017789 |
| `longevity_genetic_mechanics_panel_benchmark.json` | Longevity_Genetic_Mechanics_Panel | 35 | 0.022236 |
| `longevity_megadeep_ncbi_panel_benchmark.json` | Longevity_MegaDeep_NCBI_Panel | 1746 | 0.017789 |
| `longevity_telomere_repair_panel_benchmark.json` | Longevity_Telomere_Repair_Panel | 60 | 0.022236 |
| `machine_and_molecule_live_panel_benchmark.json` | Machine_And_Molecule_Live_Panel | 120 | 0.013410 |
| `magnetic_confinement_fusion_panel_benchmark.json` | Magnetic_Confinement_Fusion_Panel | 22 | 0.000000 |
| `magnetosphere_benchmark.json` | magnetosphere_benchmark.json | 167 | 0.000000 |
| `magnetosphere_extended_benchmark.json` | Magnetosphere_Extended | 24 | 0.000039 |
| `maillard_chemistry_gap_fill_benchmark.json` | Maillard_Chemistry | 30 | 0.094437 |
| `malware_threat_intelligence_cybersecurity_benchmark.json` | Malware_Threat_Intelligence | 85 | 0.045933 |
| `marine_biology_extension_benchmark.json` | Marine_Biology | 540 | 0.022236 |
| `marine_biology_panel_benchmark.json` | Marine_Biology_Panel | 90 | 0.006006 |
| `material_in_silico_screening_scaffold_benchmark.json` | Material_In_Silico_Screening_Scaffold | 42 | 0.000000 |
| `material_property_verification_scaffold_benchmark.json` | Material_Property_Verification_Scaffold | 79 | 0.002060 |
| `materials_creep_fracture_depth_panel_benchmark.json` | Materials_Creep_Fracture_Depth_Panel | 47 | 0.013410 |
| `materials_engineering_benchmark.json` | materials_engineering_benchmark.json | 87 | 0.027170 |
| `materials_genome_crosswalk_benchmark.json` | Materials_Genome_Crosswalk | 38 | 0.000000 |
| `materials_project_live_panel_benchmark.json` | Materials_Project_Live_Panel | 141 | 0.011734 |
| `materials_species_bridge_benchmark.json` | materials_species_bridge_benchmark.json | 34 | 0.000000 |
| `materials_species_bridge_live_panel_benchmark.json` | Materials_Species_Bridge_Live_Panel | 150 | 0.013410 |
| `math_generator_airfoil_rmse_benchmark.json` | Math_Generator_Airfoil_RMSE | 23 | 0.000562 |
| `math_generator_benchmark_formula_eval_benchmark.json` | Math_Generator_Benchmark_Formula_Eval | 23 | 0.000562 |
| `math_generator_rules_benchmark.json` | math_generator_rules_benchmark.json | 1552 | None |
| `math_generator_rules_eval_benchmark.json` | math_generator_rules_eval_benchmark.json | 1552 | 0.000000 |
| `mathematics_computational_benchmark.json` | mathematics_computational_benchmark.json | 20 | 0.000000 |
| `matter_antimatter_benchmark.json` | Matter_Antimatter | 27 | 0.000000 |
| `mechanical_engineering_extension_benchmark.json` | Mechanical_Engineering | 50 | 0.000000 |
| `mechanical_engineering_panel_benchmark.json` | Mechanical_Engineering_Panel | 20 | 0.039349 |
| `mechanistic_coupling_benchmark.json` | Mechanistic_Coupling | 39 | 0.007384 |
| `medical_galactic_orbital_bridge_benchmark.json` | Medical_Galactic_Orbital_Bridge | 48 | 0.010718 |
| `metamaterial_fluid_design_prereg_scaffold_benchmark.json` | Metamaterial_Fluid_Design_Prereg_Scaffold | 25 | 0.000034 |
| `meteorology_gap_fill_benchmark.json` | Meteorology | 47 | 0.000000 |
| `microtubule_quantum_consciousness_panel_benchmark.json` | Microtubule_Quantum_Consciousness_Panel | 21 | 0.009442 |
| `mpcorb_fsot_benchmark.json` | MPCORB_Minor_Planet_Catalog | 1554101 | 0.023015 |
| `multi_hero_benchmark.json` | multi_hero_benchmark.json | 32 | 0.000000 |
| `music_harmonics_public_panel_benchmark.json` | Music_Harmonics_Public_Panel | 24 | 0.000000 |
| `mycology_extension_benchmark.json` | Mycology | 420 | 0.022236 |
| `mycology_panel_benchmark.json` | Mycology_Panel | 90 | 0.006006 |
| `nasa_donki_solar_panel_benchmark.json` | NASA_DONKI_Solar_Panel | 2148 | 0.020755 |
| `nasa_exoplanet_archive_benchmark.json` | NASA_Exoplanet_Archive | 158 | 0.023015 |
| `nasa_neo_feed_panel_benchmark.json` | NASA_NEO_Feed_Panel | 56 | 0.021097 |
| `natural_formation_element_simulation_benchmark.json` | Natural_Formation_Element_Simulation | 32 | 0.000000 |
| `ncbi_gene_public_panel_benchmark.json` | NCBI_Gene_Public_Panel | 48 | 0.025572 |
| `ncei_climate_open_benchmark.json` | NCEI_Climate_Open | 607 | 0.029100 |
| `ncei_multivar_climate_open_benchmark.json` | NCEI_Climate_Open | 607 | 0.029100 |
| `network_internet_protocols_cybersecurity_benchmark.json` | Network_Internet_Protocols | 22 | 0.010337 |
| `network_science_public_panel_benchmark.json` | Network_Science_Public_Panel | 21 | 0.000000 |
| `neural_galactic_orbital_bridge_benchmark.json` | Neural_Galactic_Orbital_Bridge | 49 | 0.018003 |
| `neuroeconomics_extension_benchmark.json` | Neuroeconomics | 65 | 0.105021 |
| `neuroeconomics_panel_benchmark.json` | Neuroeconomics_Panel | 20 | 0.031506 |
| `neuroimmunology_benchmark.json` | neuroimmunology_benchmark.json | 92 | 0.050420 |
| `neurolab_gaps_math_spine_benchmark.json` | Neurolab_Gaps_Math_Spine | 35 | 0.000000 |
| `neurolab_residual_math_spine_benchmark.json` | Neurolab_Residual_Math_Spine | 28 | 0.000000 |
| `neuron_zig_mind_panel_benchmark.json` | Neuron_Zig_Mind_Panel | 25 | 0.000000 |
| `neuron_zig_os_path_panel_benchmark.json` | Neuron_Zig_OS_Path_Panel | 41 | 0.000000 |
| `neuroscience_connectomics_depth_panel_benchmark.json` | Neuroscience_Connectomics_Depth_Panel | 27 | 0.020119 |
| `neuroscience_fi_precision_benchmark.json` | Neuroscience | 20 | 0.000000 |
| `neutrino_physics_panel_benchmark.json` | Neutrino_Physics_Panel | 20 | 0.009504 |
| `nist_asd_multi_species_open_benchmark.json` | NIST_ASD_Multi_Species_Open | 26 | 0.036791 |
| `nist_asd_spectroscopy_open_benchmark.json` | NIST_ASD_Spectroscopy_Open | 24 | 0.036791 |
| `nist_codata_constants_benchmark.json` | NIST_CODATA_Constants | 20 | 0.000180 |
| `nist_dlmf_special_functions_benchmark.json` | NIST_DLMF_Special_Functions | 21 | 0.000000 |
| `noaa_coastal_tides_benchmark.json` | NOAA_Coastal_Tides | 20 | 0.030173 |
| `noaa_ndbc_buoy_panel_benchmark.json` | NOAA_NDBC_Buoy_Panel | 596 | 0.028287 |
| `noaa_tides_multi_station_open_benchmark.json` | NOAA_Tides_Multi_Station_Open | 209 | 0.030173 |
| `nothing_perfection_friction_origin_panel_benchmark.json` | Nothing_Perfection_Friction_Origin_Panel | 24 | 0.000000 |
| `nuclear_iaea_open_benchmark.json` | Nuclear_IAEA_Open | 360 | 0.046065 |
| `nuclear_lean_route_credibility_benchmark.json` | Nuclear_Lean_Route_Credibility | 24 | 0.000638 |
| `nufit_neutrino_open_benchmark.json` | NuFIT_Neutrino_Open | 20 | 0.009504 |
| `observer_channel_derivation_benchmark.json` | Observer_Channel_Derivation | 372 | 0.052510 |
| `observer_effect_cross_species_panel_benchmark.json` | Observer_Effect_Cross_Species_Panel | 289 | 0.000000 |
| `observer_lean_route_credibility_benchmark.json` | Observer_Lean_Route_Credibility | 53 | 0.018003 |
| `oceanography_gap_fill_benchmark.json` | Oceanography | 65 | 0.030173 |
| `oeis_family_sweep_open_benchmark.json` | OEIS_Family_Sweep_Open | 394 | 0.014767 |
| `omni_theory_genesis_benchmark.json` | omni_theory_genesis_benchmark | 26 | 0.000000 |
| `omni_theory_humanities_panel_benchmark.json` | Omni_Theory_Humanities_Panel | 37 | 0.022254 |
| `oncology_benchmark.json` | oncology_benchmark.json | 67 | 0.050420 |
| `open_meteo_live_panel_benchmark.json` | Open_Meteo_Live_Panel | 432 | 0.026204 |
| `open_science_live_concordance_benchmark.json` | Open_Science_Live_Concordance | 24 | 0.000000 |
| `open_science_seed_constants_benchmark.json` | Open_Science_Seed_Constants | 21 | 0.000000 |
| `openalex_citation_depth_open_benchmark.json` | OpenAlex_Citation_Depth_Open | 150 | 0.008863 |
| `openalex_citation_graph_benchmark.json` | OpenAlex_Citation_Graph | 80 | 0.031506 |
| `openneuro_depth_open_benchmark.json` | OpenNeuro_Depth_Open | 47 | 0.018003 |
| `openneuro_full_panel_benchmark.json` | OpenNeuro_Full_Panel | 20 | 0.015431 |
| `oph_fsot_challenge_panel_benchmark.json` | OPH_FSOT_Challenge_Panel | 31 | 0.000000 |
| `optics_interferometry_depth_panel_benchmark.json` | Optics_Interferometry_Depth_Panel | 82 | 0.026954 |
| `orbital_mechanics_benchmark.json` | orbital_mechanics | 21 | 0.000000 |
| `osti_doe_science_panel_benchmark.json` | OSTI_DOE_Science_Panel | 100 | 0.013820 |
| `overflow_carry_emergence_panel_benchmark.json` | Overflow_Carry_Emergence_Panel | 29 | 0.009504 |
| `owid_epidemiology_open_benchmark.json` | OWID_Epidemiology_Open | 1778 | 0.022236 |
| `paleoclimate_extension_benchmark.json` | Paleoclimate | 40 | 0.015016 |
| `paleoclimate_panel_benchmark.json` | Paleoclimate_Panel | 20 | 0.006006 |
| `paleontology_extension_benchmark.json` | Paleontology | 630 | 0.017836 |
| `paleontology_panel_benchmark.json` | Paleontology_Panel | 120 | 0.016730 |
| `particle_neural_orbital_bridge_benchmark.json` | Particle_Neural_Orbital_Bridge | 48 | 0.033264 |
| `particle_physics_benchmark.json` | particle_physics_benchmark.json | 98 | 0.014415 |
| `particle_physics_gap_fill_benchmark.json` | Particle_Physics | 98 | 0.002322 |
| `pdg_live_depth_open_benchmark.json` | PDG_Live_Depth_Open | 33 | 0.009504 |
| `pdg_particle_properties_benchmark.json` | PDG_Particle_Properties | 27 | 0.008160 |
| `perceived_lean_route_credibility_benchmark.json` | Perceived_Lean_Route_Credibility | 58 | 0.018003 |
| `periodic_extension_decay_topology_scaffold_benchmark.json` | Periodic_Extension_Decay_Topology_Scaffold | 24 | 0.000000 |
| `periodic_table_completion_spine_benchmark.json` | Periodic_Table_Completion_Spine | 36 | 0.000040 |
| `periodic_table_extension_closure_spine_benchmark.json` | Periodic_Table_Extension_Closure_Spine | 39 | 0.000000 |
| `periodic_table_public_panel_benchmark.json` | Periodic_Table_Public_Panel | 52 | 0.000095 |
| `petrology_geochemistry_panel_benchmark.json` | Petrology_Geochemistry_Panel | 80 | 0.030428 |
| `pharmacokinetics_gap_fill_benchmark.json` | Pharmacokinetics | 56 | 0.002412 |
| `pharmacology_benchmark.json` | pharmacology_benchmark.json | 120 | 0.001167 |
| `phi_morphogenetic_scaling_benchmark.json` | Phi_Morphogenetic_Scaling | 289 | 0.017608 |
| `physarum_biological_cuda_panel_benchmark.json` | Physarum_Biological_CUDA_Panel | 24 | 0.000309 |
| `planetary_atmospheres_benchmark.json` | planetary_atmospheres_benchmark.json | 21 | 0.000000 |
| `planetary_structure_benchmark.json` | planetary_structure_benchmark.json | 20 | 0.000000 |
| `plasma_physics_benchmark.json` | plasma_physics_benchmark.json | 20 | 0.000000 |
| `portable_clone_verify_benchmark.json` | Portable_Clone_Verify | 419 | 0.000000 |
| `prediction_rederivation_benchmark.json` | Prediction_Rederivation | 23 | 0.000562 |
| `preregistered_outcome_tracking_benchmark.json` | Preregistered_Outcome_Tracking | 72 | 0.000000 |
| `preregistered_predictions_benchmark.json` | Preregistered_Predictions | 35 | 0.020098 |
| `preregistered_predictions_verification_scaffold_benchmark.json` | Preregistered_Predictions_Verification_Scaffold | 60 | 0.000000 |
| `programming_language_laws_benchmark.json` | Programming_Language_Laws | 105 | 0.000000 |
| `proof_carrying_code_genome_benchmark.json` | Proof_Carrying_Code_Genome | 25 | 0.005169 |
| `proof_ledger_closure_spine_benchmark.json` | Proof_Ledger_Closure_Spine | 17 | 0.000000 |
| `proton_lean_route_credibility_benchmark.json` | Proton_Lean_Route_Credibility | 58 | 0.009504 |
| `psychology_gap_fill_benchmark.json` | Psychology | 160 | 0.031506 |
| `psychology_psychometrics_depth_panel_benchmark.json` | Psychology_Psychometrics_Depth_Panel | 24 | 0.009282 |
| `pubchem_compound_properties_benchmark.json` | PubChem_Compound_Properties | 500 | 0.002633 |
| `pubchem_depth_open_benchmark.json` | PubChem_Depth_Open | 149 | 0.040788 |
| `pubchem_live_deep_benchmark.json` | PubChem_Live_Deep | 5043 | 0.032631 |
| `pubchem_stability_panel_benchmark.json` | PubChem_Stability_Panel | 59 | 0.002424 |
| `public_verifiable_spine_benchmark.json` | Public_Verifiable_Spine | 20 | 0.000000 |
| `published_fuel_property_panel_benchmark.json` | Published_Fuel_Property_Panel | 31 | 0.000000 |
| `pure_mathematics_extension_benchmark.json` | Pure_Mathematics | 1578 | 0.000000 |
| `pure_mathematics_panel_benchmark.json` | Pure_Mathematics_Panel | 44 | 0.025840 |
| `qce_elm_fusion_edge_panel_benchmark.json` | QCE_ELM_Fusion_Edge_Panel | 45 | 0.000000 |
| `quantum_computing_gap_fill_benchmark.json` | Quantum_Computing | 177 | 0.000295 |
| `quantum_computing_math_depth_panel_benchmark.json` | Quantum_Computing_Math_Depth_Panel | 77 | 0.014767 |
| `quantum_information_benchmark.json` | Quantum_Information | 21 | 0.000000 |
| `quantum_materials_benchmark.json` | quantum_materials_benchmark.json | 168 | 0.023805 |
| `quantum_mechanics_entanglement_depth_panel_benchmark.json` | Quantum_Mechanics_Entanglement_Depth_Panel | 21 | 0.014767 |
| `quantum_mechanics_gap_fill_benchmark.json` | Quantum_Mechanics | 50 | 0.000095 |
| `quantum_optics_gap_fill_benchmark.json` | Quantum_Optics | 50 | 0.000095 |
| `quantum_trinary_syntax_benchmark.json` | Quantum_Trinary_Syntax | 27 | 0.005907 |
| `radio_astronomy_panel_benchmark.json` | Radio_Astronomy_Panel | 30 | 0.022461 |
| `rcsb_pdb_structures_benchmark.json` | RCSB_PDB_Structures | 45 | 0.026519 |
| `rcsb_structure_batch_open_benchmark.json` | RCSB_Structure_Batch_Open | 91 | 0.022236 |
| `rd_interval_tightening_panel_benchmark.json` | RD_Interval_Tightening_Panel | 24 | 0.000000 |
| `reality_folding_spine_benchmark.json` | Reality_Folding_Spine | 24 | 0.000638 |
| `recent_breakthroughs_expansion_panel_benchmark.json` | Recent_Breakthroughs_Expansion_Panel | 63 | 0.000000 |
| `robotics_control_systems_extension_benchmark.json` | Robotics_Control_Systems | 44 | 0.000000 |
| `robotics_control_systems_panel_benchmark.json` | Robotics_Control_Systems_Panel | 24 | 0.013410 |
| `rust_lean_bridge_benchmark.json` | rust_lean_bridge_benchmark.json | 9 | 0.000000 |
| `rust_lean_bridge_panel_benchmark.json` | Rust_Lean_Bridge_Panel | 21 | 0.000000 |
| `scalar_solver_35_panel_benchmark.json` | Scalar_Solver_35_Panel | 21 | 0.007394 |
| `schematic_netlist_intrinsic_panel_benchmark.json` | Schematic_Netlist_Intrinsic_Panel | 27 | 0.020755 |
| `scientific_expansion_depth_spine_benchmark.json` | Scientific_Expansion_Depth_Spine | 72 | 0.033841 |
| `scientific_expansion_depth_wave2_spine_benchmark.json` | Scientific_Expansion_Depth_Wave2_Spine | 40 | 0.000000 |
| `scientific_expansion_spine_benchmark.json` | Scientific_Expansion_Spine | 40 | 0.000000 |
| `scientific_expansion_wave2_spine_benchmark.json` | Scientific_Expansion_Wave2_Spine | 40 | 0.000000 |
| `scientific_expansion_wave3_spine_benchmark.json` | Scientific_Expansion_Wave3_Spine | 40 | 0.000000 |
| `secure_software_engineering_cybersecurity_benchmark.json` | Secure_Software_Engineering | 59 | 0.000000 |
| `seismology_benchmark.json` | seismology_benchmark.json | 500 | 0.000000 |
| `seismology_deep_benchmark.json` | seismology_deep_benchmark.json | 1000 | 0.000000 |
| `semiconductor_physics_public_panel_benchmark.json` | Semiconductor_Physics_Public_Panel | 24 | 0.000000 |
| `sh0es_full_sample_benchmark.json` | SH0ES_Full_Sample | 11 | 0.140950 |
| `sh0es_ladder_chain_benchmark.json` | SH0ES_Ladder_Chain | 5 | 0.328405 |
| `sh0es_refined_benchmark.json` | SH0ES_Refined | 7 | 0.000000 |
| `simbad_identity_depth_open_benchmark.json` | SIMBAD_Identity_Depth_Open | 1365 | 0.022461 |
| `simbad_stellar_identity_deep_benchmark.json` | SIMBAD_Stellar_Identity_Deep | 520 | 0.022461 |
| `small_body_orbits_benchmark.json` | Small_Body_Orbits | 23 | 0.000562 |
| `sociology_gap_fill_benchmark.json` | Sociology | 200 | 0.019504 |
| `soil_science_panel_benchmark.json` | Soil_Science_Panel | 96 | 0.006006 |
| `solar_system_structure_deep_benchmark.json` | Solar_System_Structure_Deep | 48 | 0.000000 |
| `space_propulsion_systems_benchmark.json` | Space_Propulsion_Systems | 21 | 0.000000 |
| `space_weather_benchmark.json` | space_weather_benchmark.json | 271813 | 0.000000 |
| `space_weather_summary_benchmark.json` | space_weather_summary_benchmark.json | 271813 | 0.000000 |
| `speleology_extension_benchmark.json` | Speleology | 65 | 0.044590 |
| `speleology_panel_benchmark.json` | Speleology_Panel | 24 | 0.000638 |
| `sports_biomechanics_gap_fill_benchmark.json` | Sports_Biomechanics | 35 | 0.044473 |
| `star_trek_transporter_live_panel_benchmark.json` | Star_Trek_Transporter_Live_Panel | 1575 | 0.012464 |
| `statistical_mechanics_public_panel_benchmark.json` | Statistical_Mechanics_Public_Panel | 24 | 0.000000 |
| `stellar_multiplicity_catalog_benchmark.json` | Stellar_Multiplicity_Catalog | 68 | 0.000000 |
| `stellar_multiplicity_live_deep_benchmark.json` | Stellar_Multiplicity_Live_Deep | 69 | 0.000000 |
| `stsci_mast_telescope_panel_benchmark.json` | STScI_MAST_Telescope_Panel | 377 | 0.026954 |
| `stumped_observables_panel_benchmark.json` | Stumped_Observables_Panel | 22 | 0.007871 |
| `stumped_observables_spine_benchmark.json` | Stumped_Observables_Spine | 24 | 0.000039 |
| `superheavy_element_stability_panel_benchmark.json` | Superheavy_Element_Stability_Panel | 50 | 0.000001 |
| `superheavy_island_completion_spine_benchmark.json` | Superheavy_Island_Completion_Spine | 41 | 0.000000 |
| `superheavy_island_emergence_simulation_benchmark.json` | Superheavy_Island_Emergence_Simulation | 32 | 0.000000 |
| `supply_chain_logistics_extension_benchmark.json` | Supply_Chain_Logistics | 40 | 0.025160 |
| `supply_chain_logistics_panel_benchmark.json` | Supply_Chain_Logistics_Panel | 40 | 0.025840 |
| `symbolic_archetype_panel_benchmark.json` | Symbolic_Archetype_Panel | 22 | 0.000000 |
| `synthetic_biology_benchmark.json` | synthetic_biology_benchmark | 20 | 0.000000 |
| `tectonics_benchmark.json` | tectonics_benchmark.json | 500 | 0.000000 |
| `term3_acoustic_bleed_depth_benchmark.json` | Term3_Acoustic_Bleed_Depth | 23 | 0.008381 |
| `the_well_outcomes_verification_panel_benchmark.json` | The_Well_Outcomes_Verification_Panel | 246 | 0.031159 |
| `the_well_spot_check_panel_benchmark.json` | The_Well_Spot_Check_Panel | 24 | 0.015860 |
| `the_well_verification_spine_benchmark.json` | The_Well_Verification_Spine | 24 | 0.000000 |
| `theory_completeness_spine_benchmark.json` | Theory_Completeness_Spine | 6 | 0.000000 |
| `thesis_simulation_benchmark.json` | thesis_simulation_benchmark.json | 156 | None |
| `tier_93_dual_wave_spine_benchmark.json` | Tier_93_Dual_Wave_Spine | 24 | 0.000000 |
| `tier_94_longevity_spine_benchmark.json` | Tier_94_Longevity_Spine | 34 | 0.000000 |
| `tier_95_zebrafish_spine_benchmark.json` | Tier_95_Zebrafish_Spine | 24 | 0.000000 |
| `tier_96_circuit_spine_benchmark.json` | Tier_96_Circuit_Spine | 37 | 0.020755 |
| `time_domain_crosswalk_benchmark.json` | Time_Domain_Crosswalk | 371 | 0.027551 |
| `time_emergence_deep_panel_benchmark.json` | Time_Emergence_Deep_Panel | 24 | 0.000000 |
| `time_emergence_simulation_benchmark.json` | Time_Emergence_Simulation | 28 | 0.000000 |
| `toe_ckm_pmns_benchmark.json` | TOE_CKM_PMNS_Flavor | 40 | 0.052353 |
| `toe_claim_certificate_bundle_benchmark.json` | ToE_Claim_Certificate_Bundle | 7 | 0.000000 |
| `toe_dynamics_benchmark.json` | TOE_Dynamics | 18 | 0.000000 |
| `toe_gap_closure_spine_benchmark.json` | ToE_Gap_Closure_Spine | 7 | 0.000000 |
| `toe_gr_sm_deep_benchmark.json` | TOE_GR_SM_Deep | 99 | 0.004720 |
| `toe_limit_recovery_benchmark.json` | TOE_Limit_Recovery | 43 | 0.004710 |
| `toe_unification_spine_benchmark.json` | ToE_Unification_Spine | 8 | 0.000000 |
| `tokenization_live_panel_benchmark.json` | Tokenization_Live_Panel | 51 | 0.031506 |
| `tokenization_smoke_benchmark.json` | Tokenization_Smoke | 21 | 0.000055 |
| `toxicology_panel_benchmark.json` | Toxicology_Panel | 21 | 0.033401 |
| `trinary_hardware_live_panel_benchmark.json` | Trinary_Hardware_Live_Panel | 28 | 0.014767 |
| `trinary_hardware_motif_benchmark.json` | Trinary_Hardware_Motif | 21 | 0.000055 |
| `trinary_os_isa_rebuild_benchmark.json` | trinary_os_isa_rebuild_benchmark.json | 38 | 0.000000 |
| `trinary_os_portable_benchmark.json` | Trinary_OS_Portable | 21 | 0.000055 |
| `trinary_os_round_trip_benchmark.json` | trinary_os_round_trip_benchmark.json | 22 | 0.000000 |
| `trinary_os_tier_e_benchmark.json` | Trinary_OS_Tier_E | 68 | 0.000000 |
| `uap_war_gov_release_panel_benchmark.json` | UAP_War_Gov_Release_Panel | 542 | 0.008488 |
| `undiscovered_element_candidate_prereg_scaffold_benchmark.json` | Undiscovered_Element_Candidate_Prereg_Scaffold | 25 | 0.000000 |
| `unified_db_candidate_crosswalk_benchmark.json` | Unified_DB_Candidate_Crosswalk | 45 | 0.000000 |
| `unified_db_crosswalk_spine_benchmark.json` | Unified_DB_Crosswalk_Spine | 43 | 0.000000 |
| `uniprot_protein_annotations_benchmark.json` | UniProt_Protein_Annotations | 22 | 0.020997 |
| `uniprot_proteome_slice_open_benchmark.json` | UniProt_Proteome_Slice_Open | 68 | 0.022236 |
| `uniprot_structure_annotations_deep_benchmark.json` | UniProt_Structure_Annotations_Deep | 121 | 0.000000 |
| `usgs_seismic_history_open_benchmark.json` | USGS_Seismic_History_Open | 398 | 0.022295 |
| `validators_intrinsic_llm_panel_benchmark.json` | Intrinsic_LLM_Validators_Panel | 21 | 0.014767 |
| `virology_extension_benchmark.json` | Virology | 50 | 0.045933 |
| `virology_panel_benchmark.json` | Virology_Panel | 24 | 0.000638 |
| `vizier_wds_tap_live_deep_benchmark.json` | VizieR_WDS_TAP_Live_Deep | 91 | 0.026954 |
| `vl_agent_distill_panel_benchmark.json` | VL_Agent_Distill_Panel | 21 | 0.031506 |
| `vl_distill_atlas_benchmark.json` | VL_Distill_Atlas | 21 | 0.000055 |
| `volcanology_panel_benchmark.json` | Volcanology_Panel | 90 | 0.023502 |
| `warp_bh_wh_portal_benchmark.json` | Warp_BH_WH_Portal_Panel | 23 | 0.000000 |
| `wds_live_multiplicity_deep_benchmark.json` | WDS_Live_Multiplicity_Deep | 281 | 0.026954 |
| `weather_observed_benchmark.json` | weather_observed_benchmark.json | 47 | 0.000000 |
| `world_bank_development_benchmark.json` | World_Bank_Development | 395 | 0.025840 |
| `world_bank_macro_open_benchmark.json` | World_Bank_Macro_Open | 605 | 0.025840 |
| `xr_interactive_media_math_scaffold_benchmark.json` | XR_Interactive_Media_Math_Scaffold | 24 | 0.000000 |
| `z120_z126_beam_synthesis_panel_benchmark.json` | Z120_Z126_Beam_Synthesis_Panel | 20 | 0.000095 |
| `z164_distant_island_prereg_scaffold_benchmark.json` | Z164_Distant_Island_Prereg_Scaffold | 24 | 0.000000 |
| `zebrafish_cell_tracking_panel_benchmark.json` | Zebrafish_Cell_Tracking_Panel | 20 | 0.022236 |
| `zebrafish_developmental_mechanics_panel_benchmark.json` | Zebrafish_Developmental_Mechanics_Panel | 31 | 0.017789 |
| `zebrafish_longevity_genetics_coupling_panel_benchmark.json` | Zebrafish_Longevity_Genetics_Coupling_Panel | 24 | 0.013342 |
| `zebrafish_predictive_validation_panel_benchmark.json` | Zebrafish_Predictive_Validation_Panel | 20 | 0.357969 |
| `zenodo_records_depth_open_benchmark.json` | Zenodo_Records_Depth_Open | 32 | 0.031506 |
| `zero_boundary_not_entity_panel_benchmark.json` | Zero_Boundary_Not_Entity_Panel | 24 | 0.000055 |
| `zero_day_risk_evaluator_cybersecurity_benchmark.json` | Zero_Day_Risk_Evaluator | 25 | 0.010337 |
| `zoology_extension_benchmark.json` | Zoology | 1000 | 0.017789 |

Query live:

```powershell
python scripts/audit_all_benchmark_margins.py
python scripts/query_fsot_atlas.py --stats
python scripts/query_fsot_domain_navigator.py
```

Related: [`DOMAIN_FAMILY_TREE.md`](DOMAIN_FAMILY_TREE.md) · [`APPLY.md`](APPLY.md) ·
[`WHY_NOT_CLAIMED.md`](WHY_NOT_CLAIMED.md) · [`WORKED_EXAMPLES.md`](WORKED_EXAMPLES.md).
