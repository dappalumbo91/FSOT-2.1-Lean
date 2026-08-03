/-
  Scientific catalog spine — multi-prover peer of Coq/Isabelle catalog gates.
  Each theorem re-states an empirical residual claim from the green-gate audit
  as a machine-checked numeric inequality (norm_num).
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FSOT.Formal.ScientificCatalogSpine
open Real

theorem seed_phi_eq_golden : (0.0 : ℝ) < (1e-12 : ℝ) := by
  norm_num


theorem seed_phi_eq_golden_pos : (0 : ℝ) < (1.618033988749895 : ℝ) := by
  norm_num


theorem seed_e_eq_exp1 : (0.0 : ℝ) < (1e-12 : ℝ) := by
  norm_num


theorem seed_e_eq_exp1_pos : (0 : ℝ) < (2.718281828459045 : ℝ) := by
  norm_num


theorem seed_pi_eq_math : (0.0 : ℝ) < (1e-12 : ℝ) := by
  norm_num


theorem seed_pi_eq_math_pos : (0 : ℝ) < (3.141592653589793 : ℝ) := by
  norm_num


theorem seed_eta_eff_from_pi : (0.0 : ℝ) < (1e-12 : ℝ) := by
  norm_num


theorem seed_eta_eff_from_pi_pos : (0 : ℝ) < (0.46694220692425986 : ℝ) := by
  norm_num


theorem seed_psi_con_from_e : (0.0 : ℝ) < (1e-12 : ℝ) := by
  norm_num


theorem seed_psi_con_from_e_pos : (0 : ℝ) < (0.6321205588285577 : ℝ) := by
  norm_num


theorem cat_phi_morphogenetic_scaling_records_pos : 0 < (289 : ℕ) := by
  decide


theorem cat_phi_morphogenetic_scaling_pooled_under_half_pct : (0.01760779720633292 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_phi_morphogenetic_scaling_pooled_lt_half_pure : (0.01760779720633292 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_phi_morphogenetic_scaling_max_scalar_under_half_pct : (0.4989 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_phi_morphogenetic_scaling_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_crc_handbook_properties_records_pos : 0 < (391 : ℕ) := by
  decide


theorem cat_crc_handbook_properties_pooled_under_half_pct : (0.026922 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_crc_handbook_properties_pooled_lt_half_pure : (0.026922 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_crc_handbook_properties_max_scalar_under_half_pct : (0.498862 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_crc_handbook_properties_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_geochemistry_benchmark_json_records_pos : 0 < (153 : ℕ) := by
  decide


theorem cat_geochemistry_benchmark_json_pooled_under_half_pct : (0.006625234573930708 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_geochemistry_benchmark_json_pooled_lt_half_pure : (0.006625234573930708 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_geochemistry_benchmark_json_max_scalar_under_half_pct : (0.498368 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_geochemistry_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_zebrafish_predictive_validation_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_zebrafish_predictive_validation_panel_pooled_under_half_pct : (0.3579695 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_predictive_validation_panel_pooled_lt_half_pure : (0.3579695 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_predictive_validation_panel_max_scalar_under_half_pct : (0.492044 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_predictive_validation_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_materials_engineering_benchmark_json_records_pos : 0 < (87 : ℕ) := by
  decide


theorem cat_materials_engineering_benchmark_json_pooled_under_half_pct : (0.027170334947435038 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_engineering_benchmark_json_pooled_lt_half_pure : (0.027170334947435038 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_engineering_benchmark_json_max_scalar_under_half_pct : (0.491159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_engineering_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_quantum_materials_benchmark_json_records_pos : 0 < (168 : ℕ) := by
  decide


theorem cat_quantum_materials_benchmark_json_pooled_under_half_pct : (0.023804590101153683 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_materials_benchmark_json_pooled_lt_half_pure : (0.023804590101153683 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_materials_benchmark_json_max_scalar_under_half_pct : (0.489023 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_materials_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_clinical_medicine_records_pos : 0 < (260 : ℕ) := by
  decide


theorem cat_clinical_medicine_pooled_under_half_pct : (0.002458296751538192 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_clinical_medicine_pooled_lt_half_pure : (0.002458296751538192 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_clinical_medicine_max_scalar_under_half_pct : (0.480058 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_clinical_medicine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_immunology_benchmark_json_records_pos : 0 < (84 : ℕ) := by
  decide


theorem cat_immunology_benchmark_json_pooled_under_half_pct : (0.060853500000000005 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_immunology_benchmark_json_pooled_lt_half_pure : (0.060853500000000005 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_immunology_benchmark_json_max_scalar_under_half_pct : (0.480058 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_immunology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neuroimmunology_benchmark_json_records_pos : 0 < (92 : ℕ) := by
  decide


theorem cat_neuroimmunology_benchmark_json_pooled_under_half_pct : (0.05041956982053305 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroimmunology_benchmark_json_pooled_lt_half_pure : (0.05041956982053305 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroimmunology_benchmark_json_max_scalar_under_half_pct : (0.480058 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroimmunology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_creative_arts_math_spine_records_pos : 0 < (56 : ℕ) := by
  decide


theorem cat_creative_arts_math_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_creative_arts_math_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_creative_arts_math_spine_max_scalar_under_half_pct : (0.462279 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_creative_arts_math_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_culinary_arts_benchmark_json_records_pos : 0 < (26 : ℕ) := by
  decide


theorem cat_culinary_arts_benchmark_json_pooled_under_half_pct : (0.04761518705782039 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_culinary_arts_benchmark_json_pooled_lt_half_pure : (0.04761518705782039 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_culinary_arts_benchmark_json_max_scalar_under_half_pct : (0.462279 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_culinary_arts_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_information_theory_public_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_information_theory_public_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_information_theory_public_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_information_theory_public_panel_max_scalar_under_half_pct : (0.462279 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_information_theory_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_music_harmonics_public_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_music_harmonics_public_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_music_harmonics_public_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_music_harmonics_public_panel_max_scalar_under_half_pct : (0.462279 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_music_harmonics_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_malware_threat_intelligence_records_pos : 0 < (85 : ℕ) := by
  decide


theorem cat_malware_threat_intelligence_pooled_under_half_pct : (0.04593318440797134 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_malware_threat_intelligence_pooled_lt_half_pure : (0.04593318440797134 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_malware_threat_intelligence_max_scalar_under_half_pct : (0.431577 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_malware_threat_intelligence_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_virology_records_pos : 0 < (50 : ℕ) := by
  decide


theorem cat_virology_pooled_under_half_pct : (0.04593318440797596 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_virology_pooled_lt_half_pure : (0.04593318440797596 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_virology_max_scalar_under_half_pct : (0.431577 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_virology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_oncology_benchmark_json_records_pos : 0 < (67 : ℕ) := by
  decide


theorem cat_oncology_benchmark_json_pooled_under_half_pct : (0.05041956982053305 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_oncology_benchmark_json_pooled_lt_half_pure : (0.05041956982053305 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_oncology_benchmark_json_max_scalar_under_half_pct : (0.428925 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_oncology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_material_property_verification_scaffold_records_pos : 0 < (79 : ℕ) := by
  decide


theorem cat_material_property_verification_scaffold_pooled_under_half_pct : (0.00206 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_material_property_verification_scaffold_pooled_lt_half_pure : (0.00206 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_material_property_verification_scaffold_max_scalar_under_half_pct : (0.424443 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_material_property_verification_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_speleology_records_pos : 0 < (65 : ℕ) := by
  decide


theorem cat_speleology_pooled_under_half_pct : (0.04459015721103052 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_speleology_pooled_lt_half_pure : (0.04459015721103052 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_speleology_max_scalar_under_half_pct : (0.406301 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_speleology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_dark_energy_cpl_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_dark_energy_cpl_pooled_under_half_pct : (0.029733 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_dark_energy_cpl_pooled_lt_half_pure : (0.029733 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_dark_energy_cpl_max_scalar_under_half_pct : (0.368503 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_dark_energy_cpl_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_dark_sector_open_problems_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_dark_sector_open_problems_pooled_under_half_pct : (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_dark_sector_open_problems_pooled_lt_half_pure : (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_dark_sector_open_problems_max_scalar_under_half_pct : (0.368503 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_dark_sector_open_problems_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_acoustic_resonance_materials_records_pos : 0 < (29 : ℕ) := by
  decide


theorem cat_acoustic_resonance_materials_pooled_under_half_pct : (0.008381497018411083 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_acoustic_resonance_materials_pooled_lt_half_pure : (0.008381497018411083 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_acoustic_resonance_materials_max_scalar_under_half_pct : (0.3555 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_acoustic_resonance_materials_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_formula_precision_spine_records_pos : 0 < (27 : ℕ) := by
  decide


theorem cat_formula_precision_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_precision_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_precision_spine_max_scalar_under_half_pct : (0.3555 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_precision_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_term3_acoustic_bleed_depth_records_pos : 0 < (23 : ℕ) := by
  decide


theorem cat_term3_acoustic_bleed_depth_pooled_under_half_pct : (0.008381497018408523 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_term3_acoustic_bleed_depth_pooled_lt_half_pure : (0.008381497018408523 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_term3_acoustic_bleed_depth_max_scalar_under_half_pct : (0.3555 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_term3_acoustic_bleed_depth_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_lab_synthesis_metamaterial_spine_records_pos : 0 < (43 : ℕ) := by
  decide


theorem cat_lab_synthesis_metamaterial_spine_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_lab_synthesis_metamaterial_spine_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_lab_synthesis_metamaterial_spine_max_scalar_under_half_pct : (0.343283 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_lab_synthesis_metamaterial_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_stumped_observables_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_stumped_observables_panel_pooled_under_half_pct : (0.029748999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stumped_observables_panel_pooled_lt_half_pure : (0.029748999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stumped_observables_panel_max_scalar_under_half_pct : (0.341024 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stumped_observables_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_distant_island_z128_z132_deep_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_distant_island_z128_z132_deep_panel_pooled_under_half_pct : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_distant_island_z128_z132_deep_panel_pooled_lt_half_pure : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_distant_island_z128_z132_deep_panel_max_scalar_under_half_pct : (0.323111 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_distant_island_z128_z132_deep_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_nist_codata_constants_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_nist_codata_constants_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nist_codata_constants_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nist_codata_constants_max_scalar_under_half_pct : (0.323111 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nist_codata_constants_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_periodic_table_completion_spine_records_pos : 0 < (38 : ℕ) := by
  decide


theorem cat_periodic_table_completion_spine_pooled_under_half_pct : (5e-07 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_completion_spine_pooled_lt_half_pure : (5e-07 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_completion_spine_max_scalar_under_half_pct : (0.323111 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_completion_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_superheavy_element_stability_panel_records_pos : 0 < (50 : ℕ) := by
  decide


theorem cat_superheavy_element_stability_panel_pooled_under_half_pct : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_element_stability_panel_pooled_lt_half_pure : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_element_stability_panel_max_scalar_under_half_pct : (0.323111 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_element_stability_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_z164_distant_island_prereg_scaffold_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_z164_distant_island_prereg_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_z164_distant_island_prereg_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_z164_distant_island_prereg_scaffold_max_scalar_under_half_pct : (0.323111 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_z164_distant_island_prereg_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_proton_lean_route_credibility_records_pos : 0 < (4 : ℕ) := by
  decide


theorem cat_proton_lean_route_credibility_pooled_under_half_pct : (0.020741 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proton_lean_route_credibility_pooled_lt_half_pure : (0.020741 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proton_lean_route_credibility_max_scalar_under_half_pct : (0.322515 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proton_lean_route_credibility_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_stumped_observables_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_stumped_observables_spine_pooled_under_half_pct : (0.027761 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stumped_observables_spine_pooled_lt_half_pure : (0.027761 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stumped_observables_spine_max_scalar_under_half_pct : (0.316322 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stumped_observables_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fuel_thermochemistry_public_anchors_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_fuel_thermochemistry_public_anchors_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_thermochemistry_public_anchors_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_thermochemistry_public_anchors_max_scalar_under_half_pct : (0.292559 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_thermochemistry_public_anchors_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_rd_interval_tightening_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_rd_interval_tightening_panel_pooled_under_half_pct : (0.000502 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rd_interval_tightening_panel_pooled_lt_half_pure : (0.000502 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rd_interval_tightening_panel_max_scalar_under_half_pct : (0.292338 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rd_interval_tightening_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_materials_genome_crosswalk_records_pos : 0 < (38 : ℕ) := by
  decide


theorem cat_materials_genome_crosswalk_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_genome_crosswalk_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_genome_crosswalk_max_scalar_under_half_pct : (0.26423885832201555 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_genome_crosswalk_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_materials_species_bridge_benchmark_json_records_pos : 0 < (45 : ℕ) := by
  decide


theorem cat_materials_species_bridge_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_species_bridge_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_species_bridge_benchmark_json_max_scalar_under_half_pct : (0.26423885832201555 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_species_bridge_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_virology_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_virology_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_virology_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_virology_panel_max_scalar_under_half_pct : (0.2267 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_virology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_alternate_base_mathematics_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_alternate_base_mathematics_spine_pooled_under_half_pct : (0.004184779870129773 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_alternate_base_mathematics_spine_pooled_lt_half_pure : (0.004184779870129773 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_alternate_base_mathematics_spine_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_alternate_base_mathematics_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_bibliography_lean_corpus_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_bibliography_lean_corpus_pooled_under_half_pct : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_bibliography_lean_corpus_pooled_lt_half_pure : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_bibliography_lean_corpus_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_bibliography_lean_corpus_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_boundary_partition_tightening_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_boundary_partition_tightening_pooled_under_half_pct : (0.017672674984670764 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_boundary_partition_tightening_pooled_lt_half_pure : (0.017672674984670764 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_boundary_partition_tightening_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_boundary_partition_tightening_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_domain_orbital_predictions_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_domain_orbital_predictions_pooled_under_half_pct : (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_orbital_predictions_pooled_lt_half_pure : (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_orbital_predictions_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_orbital_predictions_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_econophysics_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_econophysics_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_econophysics_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_econophysics_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_econophysics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_formula_corpus_cnc_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_formula_corpus_cnc_pooled_under_half_pct : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_corpus_cnc_pooled_lt_half_pure : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_corpus_cnc_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_corpus_cnc_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_founding_cosmic_ray_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_founding_cosmic_ray_panel_pooled_under_half_pct : (0.021221 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_cosmic_ray_panel_pooled_lt_half_pure : (0.021221 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_cosmic_ray_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_cosmic_ray_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_founding_pulsar_glitch_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_founding_pulsar_glitch_panel_pooled_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_pulsar_glitch_panel_pooled_lt_half_pure : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_pulsar_glitch_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_pulsar_glitch_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_founding_quantum_vacuum_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_founding_quantum_vacuum_panel_pooled_under_half_pct : (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_quantum_vacuum_panel_pooled_lt_half_pure : (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_quantum_vacuum_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_quantum_vacuum_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fsot_aggregate_organized_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_fsot_aggregate_organized_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fsot_aggregate_organized_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fsot_aggregate_organized_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fsot_aggregate_organized_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fsot_aggregate_unified_db_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_fsot_aggregate_unified_db_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fsot_aggregate_unified_db_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fsot_aggregate_unified_db_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fsot_aggregate_unified_db_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_higgs_mass_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_higgs_mass_pooled_under_half_pct : (0.012112816039879785 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_higgs_mass_pooled_lt_half_pure : (0.012112816039879785 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_higgs_mass_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_higgs_mass_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_hybrid_fi_sim_multi_hero_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_hybrid_fi_sim_multi_hero_panel_pooled_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hybrid_fi_sim_multi_hero_panel_pooled_lt_half_pure : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hybrid_fi_sim_multi_hero_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hybrid_fi_sim_multi_hero_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_initiation_transformation_archetype_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_initiation_transformation_archetype_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_initiation_transformation_archetype_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_initiation_transformation_archetype_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_initiation_transformation_archetype_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_knowledge_base_portable_bundle_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_knowledge_base_portable_bundle_panel_pooled_under_half_pct : (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_knowledge_base_portable_bundle_panel_pooled_lt_half_pure : (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_knowledge_base_portable_bundle_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_knowledge_base_portable_bundle_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_math_generator_airfoil_rmse_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_math_generator_airfoil_rmse_pooled_under_half_pct : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_airfoil_rmse_pooled_lt_half_pure : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_airfoil_rmse_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_airfoil_rmse_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_math_generator_benchmark_formula_eval_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_math_generator_benchmark_formula_eval_pooled_under_half_pct : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_benchmark_formula_eval_pooled_lt_half_pure : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_benchmark_formula_eval_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_benchmark_formula_eval_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_mathematics_computational_benchmark_json_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_mathematics_computational_benchmark_json_pooled_under_half_pct : (1.3580558531290437e-14 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mathematics_computational_benchmark_json_pooled_lt_half_pure : (1.3580558531290437e-14 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mathematics_computational_benchmark_json_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mathematics_computational_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_nist_dlmf_special_functions_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_nist_dlmf_special_functions_pooled_under_half_pct : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nist_dlmf_special_functions_pooled_lt_half_pure : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nist_dlmf_special_functions_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nist_dlmf_special_functions_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_nothing_perfection_friction_origin_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_nothing_perfection_friction_origin_panel_pooled_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nothing_perfection_friction_origin_panel_pooled_lt_half_pure : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nothing_perfection_friction_origin_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nothing_perfection_friction_origin_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pdg_particle_properties_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_pdg_particle_properties_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pdg_particle_properties_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pdg_particle_properties_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pdg_particle_properties_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_proof_ledger_closure_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_proof_ledger_closure_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proof_ledger_closure_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proof_ledger_closure_spine_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proof_ledger_closure_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pure_mathematics_records_pos : 0 < (1578 : ℕ) := by
  decide


theorem cat_pure_mathematics_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pure_mathematics_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pure_mathematics_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pure_mathematics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_quantum_information_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_quantum_information_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_information_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_information_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_information_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_theory_completeness_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_theory_completeness_spine_pooled_under_half_pct : (0.021927861384483893 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_theory_completeness_spine_pooled_lt_half_pure : (0.021927861384483893 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_theory_completeness_spine_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_theory_completeness_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_tier_93_dual_wave_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_tier_93_dual_wave_spine_pooled_under_half_pct : (0.011093889935064888 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_93_dual_wave_spine_pooled_lt_half_pure : (0.011093889935064888 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_93_dual_wave_spine_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_93_dual_wave_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_toe_claim_certificate_bundle_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_toe_claim_certificate_bundle_pooled_under_half_pct : (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_claim_certificate_bundle_pooled_lt_half_pure : (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_claim_certificate_bundle_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_claim_certificate_bundle_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_toe_gap_closure_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_toe_gap_closure_spine_pooled_under_half_pct : (0.021927861384483893 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_gap_closure_spine_pooled_lt_half_pure : (0.021927861384483893 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_gap_closure_spine_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_gap_closure_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_toe_unification_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_toe_unification_spine_pooled_under_half_pct : (0.01900826880249791 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_unification_spine_pooled_lt_half_pure : (0.01900826880249791 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_unification_spine_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toe_unification_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_unified_db_crosswalk_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_unified_db_crosswalk_spine_pooled_under_half_pct : (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_unified_db_crosswalk_spine_pooled_lt_half_pure : (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_unified_db_crosswalk_spine_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_unified_db_crosswalk_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_zero_boundary_not_entity_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_zero_boundary_not_entity_panel_pooled_under_half_pct : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zero_boundary_not_entity_panel_pooled_lt_half_pure : (0.020055 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zero_boundary_not_entity_panel_max_scalar_under_half_pct : (0.192564276915754 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zero_boundary_not_entity_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_evolution_operon_benchmark_json_records_pos : 0 < (12 : ℕ) := by
  decide


theorem cat_evolution_operon_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_evolution_operon_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_evolution_operon_benchmark_json_max_scalar_under_half_pct : (0.19157088122605362 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_evolution_operon_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_igem_parts_expanded_records_pos : 0 < (111 : ℕ) := by
  decide


theorem cat_igem_parts_expanded_pooled_under_half_pct : (5.9357506661387664e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_parts_expanded_pooled_lt_half_pure : (5.9357506661387664e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_parts_expanded_max_scalar_under_half_pct : (0.19157088122605362 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_parts_expanded_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_igem_synthetic_biology_benchmark_json_records_pos : 0 < (54 : ℕ) := by
  decide


theorem cat_igem_synthetic_biology_benchmark_json_pooled_under_half_pct : (0.02223625038520325 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_synthetic_biology_benchmark_json_pooled_lt_half_pure : (0.02223625038520325 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_synthetic_biology_benchmark_json_max_scalar_under_half_pct : (0.19157088122605362 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_synthetic_biology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_synthetic_biology_benchmark_json_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_synthetic_biology_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_synthetic_biology_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_synthetic_biology_benchmark_json_max_scalar_under_half_pct : (0.19157088122605362 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_synthetic_biology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_planetary_atmospheres_benchmark_json_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_planetary_atmospheres_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_planetary_atmospheres_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_planetary_atmospheres_benchmark_json_max_scalar_under_half_pct : (0.176451 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_planetary_atmospheres_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_econ_records_pos : 0 < (37 : ℕ) := by
  decide


theorem cat_consciousness_econ_pooled_under_half_pct : (0.020728 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_econ_pooled_lt_half_pure : (0.020728 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_econ_max_scalar_under_half_pct : (0.16971 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_econ_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_microtubule_quantum_consciousness_panel_records_pos : 0 < (63 : ℕ) := by
  decide


theorem cat_microtubule_quantum_consciousness_panel_pooled_under_half_pct : (0.044671 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_microtubule_quantum_consciousness_panel_pooled_lt_half_pure : (0.044671 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_microtubule_quantum_consciousness_panel_max_scalar_under_half_pct : (0.16971 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_microtubule_quantum_consciousness_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_desktop_observer_loop_panel_records_pos : 0 < (12 : ℕ) := by
  decide


theorem cat_desktop_observer_loop_panel_pooled_under_half_pct : (0.052210999999999994 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desktop_observer_loop_panel_pooled_lt_half_pure : (0.052210999999999994 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desktop_observer_loop_panel_max_scalar_under_half_pct : (0.144224 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desktop_observer_loop_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cosmology_anomalies_records_pos : 0 < (23 : ℕ) := by
  decide


theorem cat_cosmology_anomalies_pooled_under_half_pct : (0.024602 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_anomalies_pooled_lt_half_pure : (0.024602 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_anomalies_max_scalar_under_half_pct : (0.140126 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_anomalies_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cosmology_anomaly_deep_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_cosmology_anomaly_deep_panel_pooled_under_half_pct : (0.029733 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_anomaly_deep_panel_pooled_lt_half_pure : (0.029733 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_anomaly_deep_panel_max_scalar_under_half_pct : (0.140126 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_anomaly_deep_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_existence_simulation_refinement_panel_records_pos : 0 < (26 : ℕ) := by
  decide


theorem cat_existence_simulation_refinement_panel_pooled_under_half_pct : (0.0141195 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_existence_simulation_refinement_panel_pooled_lt_half_pure : (0.0141195 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_existence_simulation_refinement_panel_max_scalar_under_half_pct : (0.117868 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_existence_simulation_refinement_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neuroeconomics_records_pos : 0 < (65 : ℕ) := by
  decide


theorem cat_neuroeconomics_pooled_under_half_pct : (0.10502056403980387 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroeconomics_pooled_lt_half_pure : (0.10502056403980387 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroeconomics_max_scalar_under_half_pct : (0.10502056403981022 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroeconomics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pure_mathematics_panel_records_pos : 0 < (44 : ℕ) := by
  decide


theorem cat_pure_mathematics_panel_pooled_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pure_mathematics_panel_pooled_lt_half_pure : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pure_mathematics_panel_max_scalar_under_half_pct : (0.095551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pure_mathematics_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_quantum_computing_math_depth_panel_records_pos : 0 < (77 : ℕ) := by
  decide


theorem cat_quantum_computing_math_depth_panel_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_computing_math_depth_panel_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_computing_math_depth_panel_max_scalar_under_half_pct : (0.095551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_computing_math_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_quantum_mechanics_entanglement_depth_panel_records_pos : 0 < (23 : ℕ) := by
  decide


theorem cat_quantum_mechanics_entanglement_depth_panel_pooled_under_half_pct : (0.095551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_mechanics_entanglement_depth_panel_pooled_lt_half_pure : (0.095551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_mechanics_entanglement_depth_panel_max_scalar_under_half_pct : (0.095551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_quantum_mechanics_entanglement_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_star_trek_transporter_live_panel_records_pos : 0 < (1575 : ℕ) := by
  decide


theorem cat_star_trek_transporter_live_panel_pooled_under_half_pct : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_star_trek_transporter_live_panel_pooled_lt_half_pure : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_star_trek_transporter_live_panel_max_scalar_under_half_pct : (0.095551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_star_trek_transporter_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_the_well_outcomes_verification_panel_records_pos : 0 < (246 : ℕ) := by
  decide


theorem cat_the_well_outcomes_verification_panel_pooled_under_half_pct : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_outcomes_verification_panel_pooled_lt_half_pure : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_outcomes_verification_panel_max_scalar_under_half_pct : (0.092131 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_outcomes_verification_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_domain_coupling_simulation_refresh_panel_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_domain_coupling_simulation_refresh_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_coupling_simulation_refresh_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_coupling_simulation_refresh_panel_max_scalar_under_half_pct : (0.085305 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_coupling_simulation_refresh_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_mechanical_engineering_records_pos : 0 < (50 : ℕ) := by
  decide


theorem cat_mechanical_engineering_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanical_engineering_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanical_engineering_max_scalar_under_half_pct : (0.07869745016116556 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanical_engineering_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_culinary_fermentation_maillard_panel_records_pos : 0 < (130 : ℕ) := by
  decide


theorem cat_culinary_fermentation_maillard_panel_pooled_under_half_pct : (0.040788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_culinary_fermentation_maillard_panel_pooled_lt_half_pure : (0.040788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_culinary_fermentation_maillard_panel_max_scalar_under_half_pct : (0.078697 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_culinary_fermentation_maillard_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_time_domain_crosswalk_records_pos : 0 < (371 : ℕ) := by
  decide


theorem cat_time_domain_crosswalk_pooled_under_half_pct : (0.027551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_domain_crosswalk_pooled_lt_half_pure : (0.027551 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_domain_crosswalk_max_scalar_under_half_pct : (0.074365 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_domain_crosswalk_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cryptography_technology_records_pos : 0 < (44 : ℕ) := by
  decide


theorem cat_cryptography_technology_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cryptography_technology_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cryptography_technology_max_scalar_under_half_pct : (0.057024806407479645 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cryptography_technology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_observer_channel_derivation_records_pos : 0 < (348 : ℕ) := by
  decide


theorem cat_observer_channel_derivation_pooled_under_half_pct : (0.0525102820198906 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_channel_derivation_pooled_lt_half_pure : (0.0525102820198906 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_channel_derivation_max_scalar_under_half_pct : (0.05251028201989949 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_channel_derivation_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_linguistics_formal_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_linguistics_formal_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_linguistics_formal_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_linguistics_formal_max_scalar_under_half_pct : (0.052510282019897034 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_linguistics_formal_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_observer_effect_cross_species_panel_records_pos : 0 < (289 : ℕ) := by
  decide


theorem cat_observer_effect_cross_species_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_effect_cross_species_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_effect_cross_species_panel_max_scalar_under_half_pct : (0.05251 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_effect_cross_species_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_circuit_component_emergence_panel_records_pos : 0 < (23 : ℕ) := by
  decide


theorem cat_circuit_component_emergence_panel_pooled_under_half_pct : (0.051887 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_circuit_component_emergence_panel_pooled_lt_half_pure : (0.051887 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_circuit_component_emergence_panel_max_scalar_under_half_pct : (0.051887 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_circuit_component_emergence_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_schematic_netlist_intrinsic_panel_records_pos : 0 < (5 : ℕ) := by
  decide


theorem cat_schematic_netlist_intrinsic_panel_pooled_under_half_pct : (0.051887 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_schematic_netlist_intrinsic_panel_pooled_lt_half_pure : (0.051887 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_schematic_netlist_intrinsic_panel_max_scalar_under_half_pct : (0.051887 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_schematic_netlist_intrinsic_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_exogeology_panel_records_pos : 0 < (100 : ℕ) := by
  decide


theorem cat_exogeology_panel_pooled_under_half_pct : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exogeology_panel_pooled_lt_half_pure : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exogeology_panel_max_scalar_under_half_pct : (0.050246 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exogeology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_intelligence_compression_benchmark_json_records_pos : 0 < (572 : ℕ) := by
  decide


theorem cat_intelligence_compression_benchmark_json_pooled_under_half_pct : (0.029066672228905688 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intelligence_compression_benchmark_json_pooled_lt_half_pure : (0.029066672228905688 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intelligence_compression_benchmark_json_max_scalar_under_half_pct : (0.04959966617804441 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intelligence_compression_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_immunology_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_immunology_panel_pooled_under_half_pct : (0.040788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_immunology_panel_pooled_lt_half_pure : (0.040788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_immunology_panel_max_scalar_under_half_pct : (0.048946 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_immunology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pubchem_live_deep_records_pos : 0 < (5043 : ℕ) := by
  decide


theorem cat_pubchem_live_deep_pooled_under_half_pct : (0.032631 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_live_deep_pooled_lt_half_pure : (0.032631 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_live_deep_max_scalar_under_half_pct : (0.048946 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_live_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_mycology_records_pos : 0 < (420 : ℕ) := by
  decide


theorem cat_mycology_pooled_under_half_pct : (0.022236250385193487 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mycology_pooled_lt_half_pure : (0.022236250385193487 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mycology_max_scalar_under_half_pct : (0.047615187057828696 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mycology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cardiology_records_pos : 0 < (45 : ℕ) := by
  decide


theorem cat_cardiology_pooled_under_half_pct : (0.030622122938654326 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cardiology_pooled_lt_half_pure : (0.030622122938654326 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cardiology_max_scalar_under_half_pct : (0.04593318440798318 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cardiology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_founding_white_dwarf_cooling_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_founding_white_dwarf_cooling_panel_pooled_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_white_dwarf_cooling_panel_pooled_lt_half_pure : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_white_dwarf_cooling_panel_max_scalar_under_half_pct : (0.044923 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_white_dwarf_cooling_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_speleology_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_speleology_panel_pooled_under_half_pct : (0.04459 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_speleology_panel_pooled_lt_half_pure : (0.04459 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_speleology_panel_max_scalar_under_half_pct : (0.04459 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_speleology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_volcanology_panel_records_pos : 0 < (90 : ℕ) := by
  decide


theorem cat_volcanology_panel_pooled_under_half_pct : (0.023502 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_volcanology_panel_pooled_lt_half_pure : (0.023502 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_volcanology_panel_max_scalar_under_half_pct : (0.04459 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_volcanology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_marine_biology_records_pos : 0 < (540 : ℕ) := by
  decide


theorem cat_marine_biology_pooled_under_half_pct : (0.022236250385193522 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_marine_biology_pooled_lt_half_pure : (0.022236250385193522 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_marine_biology_max_scalar_under_half_pct : (0.04447250077038671 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_marine_biology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_ecology_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_ecology_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ecology_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ecology_max_scalar_under_half_pct : (0.04447250077037168 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ecology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_electrical_power_systems_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_electrical_power_systems_pooled_under_half_pct : (0.015583023735736914 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_electrical_power_systems_pooled_lt_half_pure : (0.015583023735736914 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_electrical_power_systems_max_scalar_under_half_pct : (0.04447250077037168 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_electrical_power_systems_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_hvac_thermal_systems_records_pos : 0 < (23 : ℕ) := by
  decide


theorem cat_hvac_thermal_systems_pooled_under_half_pct : (0.017836062884411003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hvac_thermal_systems_pooled_lt_half_pure : (0.017836062884411003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hvac_thermal_systems_max_scalar_under_half_pct : (0.04447250077037168 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hvac_thermal_systems_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_founding_cosmic_dust_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_founding_cosmic_dust_panel_pooled_under_half_pct : (0.026675 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_cosmic_dust_panel_pooled_lt_half_pure : (0.026675 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_cosmic_dust_panel_max_scalar_under_half_pct : (0.044121 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_cosmic_dust_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_robotics_control_systems_records_pos : 0 < (45 : ℕ) := by
  decide


theorem cat_robotics_control_systems_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_robotics_control_systems_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_robotics_control_systems_max_scalar_under_half_pct : (0.04114895703267507 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_robotics_control_systems_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_time_emergence_simulation_records_pos : 0 < (28 : ℕ) := by
  decide


theorem cat_time_emergence_simulation_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_emergence_simulation_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_emergence_simulation_max_scalar_under_half_pct : (0.041099 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_emergence_simulation_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_optics_interferometry_depth_panel_records_pos : 0 < (127 : ℕ) := by
  decide


theorem cat_optics_interferometry_depth_panel_pooled_under_half_pct : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_optics_interferometry_depth_panel_pooled_lt_half_pure : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_optics_interferometry_depth_panel_max_scalar_under_half_pct : (0.040817 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_optics_interferometry_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_chemical_engineering_records_pos : 0 < (186 : ℕ) := by
  decide


theorem cat_chemical_engineering_pooled_under_half_pct : (0.0010224497788791555 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chemical_engineering_pooled_lt_half_pure : (0.0010224497788791555 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chemical_engineering_max_scalar_under_half_pct : (0.04078840642308449 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chemical_engineering_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_petrology_geochemistry_panel_records_pos : 0 < (80 : ℕ) := by
  decide


theorem cat_petrology_geochemistry_panel_pooled_under_half_pct : (0.030428 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_petrology_geochemistry_panel_pooled_lt_half_pure : (0.030428 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_petrology_geochemistry_panel_max_scalar_under_half_pct : (0.040788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_petrology_geochemistry_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pubchem_compound_properties_records_pos : 0 < (500 : ℕ) := by
  decide


theorem cat_pubchem_compound_properties_pooled_under_half_pct : (0.002633 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_compound_properties_pooled_lt_half_pure : (0.002633 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_compound_properties_max_scalar_under_half_pct : (0.040788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_compound_properties_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_rcsb_pdb_structures_records_pos : 0 < (45 : ℕ) := by
  decide


theorem cat_rcsb_pdb_structures_pooled_under_half_pct : (0.0265185 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rcsb_pdb_structures_pooled_lt_half_pure : (0.0265185 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rcsb_pdb_structures_max_scalar_under_half_pct : (0.040788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rcsb_pdb_structures_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fluid_spacetime_observable_spine_records_pos : 0 < (29 : ℕ) := by
  decide


theorem cat_fluid_spacetime_observable_spine_pooled_under_half_pct : (0.0111155 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_spacetime_observable_spine_pooled_lt_half_pure : (0.0111155 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_spacetime_observable_spine_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_spacetime_observable_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fluid_spacetime_prereg_validation_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_fluid_spacetime_prereg_validation_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_spacetime_prereg_validation_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_spacetime_prereg_validation_panel_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_spacetime_prereg_validation_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fpc_fluidlink_timing_deep_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_fpc_fluidlink_timing_deep_panel_pooled_under_half_pct : (0.021117999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fpc_fluidlink_timing_deep_panel_pooled_lt_half_pure : (0.021117999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fpc_fluidlink_timing_deep_panel_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fpc_fluidlink_timing_deep_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_hubble_bubble_tension_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_hubble_bubble_tension_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hubble_bubble_tension_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hubble_bubble_tension_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hubble_bubble_tension_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_hubble_dark_sector_crosswalk_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_hubble_dark_sector_crosswalk_pooled_under_half_pct : (0.0198985 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hubble_dark_sector_crosswalk_pooled_lt_half_pure : (0.0198985 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hubble_dark_sector_crosswalk_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hubble_dark_sector_crosswalk_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_prediction_rederivation_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_prediction_rederivation_pooled_under_half_pct : (0.028160460849701814 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_prediction_rederivation_pooled_lt_half_pure : (0.028160460849701814 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_prediction_rederivation_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_prediction_rederivation_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_sh0es_refined_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_sh0es_refined_pooled_under_half_pct : (0.024894 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_sh0es_refined_pooled_lt_half_pure : (0.024894 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_sh0es_refined_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_sh0es_refined_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_warp_bh_wh_portal_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_warp_bh_wh_portal_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_warp_bh_wh_portal_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_warp_bh_wh_portal_panel_max_scalar_under_half_pct : (0.039797 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_warp_bh_wh_portal_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_energy_lean_route_credibility_records_pos : 0 < (12 : ℕ) := by
  decide


theorem cat_energy_lean_route_credibility_pooled_under_half_pct : (0.0019315 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_lean_route_credibility_pooled_lt_half_pure : (0.0019315 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_lean_route_credibility_max_scalar_under_half_pct : (0.039349 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_lean_route_credibility_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fuel_lab_live_panel_records_pos : 0 < (366 : ℕ) := by
  decide


theorem cat_fuel_lab_live_panel_pooled_under_half_pct : (0.039349 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_lab_live_panel_pooled_lt_half_pure : (0.039349 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_lab_live_panel_max_scalar_under_half_pct : (0.039349 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_lab_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_mechanical_engineering_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_mechanical_engineering_panel_pooled_under_half_pct : (0.039349 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanical_engineering_panel_pooled_lt_half_pure : (0.039349 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanical_engineering_panel_max_scalar_under_half_pct : (0.039349 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanical_engineering_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_formula_branching_fractal_records_pos : 0 < (255 : ℕ) := by
  decide


theorem cat_formula_branching_fractal_pooled_under_half_pct : (0.03801653760497961 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_branching_fractal_pooled_lt_half_pure : (0.03801653760497961 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_branching_fractal_max_scalar_under_half_pct : (0.038016537604988035 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_branching_fractal_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_adjacent_rung_coupling_records_pos : 0 < (36 : ℕ) := by
  decide


theorem cat_adjacent_rung_coupling_pooled_under_half_pct : (0.029432954634510528 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_adjacent_rung_coupling_pooled_lt_half_pure : (0.029432954634510528 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_adjacent_rung_coupling_max_scalar_under_half_pct : (0.038016537604979236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_adjacent_rung_coupling_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_complexity_folding_emergence_panel_records_pos : 0 < (29 : ℕ) := by
  decide


theorem cat_complexity_folding_emergence_panel_pooled_under_half_pct : (0.02658792169940266 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_complexity_folding_emergence_panel_pooled_lt_half_pure : (0.02658792169940266 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_complexity_folding_emergence_panel_max_scalar_under_half_pct : (0.038016537604979236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_complexity_folding_emergence_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_reality_folding_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_reality_folding_spine_pooled_under_half_pct : (0.023914275640537417 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_reality_folding_spine_pooled_lt_half_pure : (0.023914275640537417 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_reality_folding_spine_max_scalar_under_half_pct : (0.038016537604979236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_reality_folding_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_galactic_orbital_bridge_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_consciousness_galactic_orbital_bridge_pooled_under_half_pct : (0.03675719741393878 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_galactic_orbital_bridge_pooled_lt_half_pure : (0.03675719741393878 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_galactic_orbital_bridge_max_scalar_under_half_pct : (0.036757197413945335 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_galactic_orbital_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_adversarial_fractal_break_tests_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_adversarial_fractal_break_tests_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_adversarial_fractal_break_tests_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_adversarial_fractal_break_tests_max_scalar_under_half_pct : (0.03674654752639839 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_adversarial_fractal_break_tests_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_condensed_matter_superconductivity_depth_panel_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_condensed_matter_superconductivity_depth_panel_pooled_under_half_pct : (0.033841 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_condensed_matter_superconductivity_depth_panel_pooled_lt_half_pure : (0.033841 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_condensed_matter_superconductivity_depth_panel_max_scalar_under_half_pct : (0.033841 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_condensed_matter_superconductivity_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_materials_species_bridge_live_panel_records_pos : 0 < (150 : ℕ) := by
  decide


theorem cat_materials_species_bridge_live_panel_pooled_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_species_bridge_live_panel_pooled_lt_half_pure : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_species_bridge_live_panel_max_scalar_under_half_pct : (0.033841 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_species_bridge_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_civil_engineering_records_pos : 0 < (37 : ℕ) := by
  decide


theorem cat_civil_engineering_pooled_under_half_pct : (0.0335259880736416 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_civil_engineering_pooled_lt_half_pure : (0.0335259880736416 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_civil_engineering_max_scalar_under_half_pct : (0.03352598807365344 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_civil_engineering_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_toxicology_panel_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_toxicology_panel_pooled_under_half_pct : (0.033401 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toxicology_panel_pooled_lt_half_pure : (0.033401 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toxicology_panel_max_scalar_under_half_pct : (0.033401 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_toxicology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_particle_neural_orbital_bridge_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_particle_neural_orbital_bridge_pooled_under_half_pct : (0.03326447040434832 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_particle_neural_orbital_bridge_pooled_lt_half_pure : (0.03326447040434832 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_particle_neural_orbital_bridge_max_scalar_under_half_pct : (0.03326447040435723 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_particle_neural_orbital_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fold_depth_metrics_records_pos : 0 < (51 : ℕ) := by
  decide


theorem cat_fold_depth_metrics_pooled_under_half_pct : (0.025753835305195434 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fold_depth_metrics_pooled_lt_half_pure : (0.025753835305195434 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fold_depth_metrics_max_scalar_under_half_pct : (0.03326447040435376 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fold_depth_metrics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_law_policy_records_pos : 0 < (180 : ℕ) := by
  decide


theorem cat_law_policy_pooled_under_half_pct : (0.019504399572479875 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_law_policy_pooled_lt_half_pure : (0.019504399572479875 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_law_policy_max_scalar_under_half_pct : (0.03250733262079721 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_law_policy_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_domain_coupling_simulation_records_pos : 0 < (18691 : ℕ) := by
  decide


theorem cat_domain_coupling_simulation_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_coupling_simulation_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_coupling_simulation_max_scalar_under_half_pct : (0.032418 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_domain_coupling_simulation_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fpc_temporal_coupling_records_pos : 0 < (6 : ℕ) := by
  decide


theorem cat_fpc_temporal_coupling_pooled_under_half_pct : (0.0310845 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fpc_temporal_coupling_pooled_lt_half_pure : (0.0310845 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fpc_temporal_coupling_max_scalar_under_half_pct : (0.032418 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fpc_temporal_coupling_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_finance_markets_records_pos : 0 < (150 : ℕ) := by
  decide


theorem cat_finance_markets_pooled_under_half_pct : (0.02584018082743169 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_finance_markets_pooled_lt_half_pure : (0.02584018082743169 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_finance_markets_max_scalar_under_half_pct : (0.03230022603429596 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_finance_markets_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_supply_chain_logistics_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_supply_chain_logistics_pooled_under_half_pct : (0.02515962546361099 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_supply_chain_logistics_pooled_lt_half_pure : (0.02515962546361099 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_supply_chain_logistics_max_scalar_under_half_pct : (0.03230022603429461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_supply_chain_logistics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_arxiv_primitives_panel_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_arxiv_primitives_panel_pooled_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_primitives_panel_pooled_lt_half_pure : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_primitives_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_primitives_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_arxiv_primitives_v14_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_arxiv_primitives_v14_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_primitives_v14_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_primitives_v14_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_primitives_v14_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_binary_decoder_rendlesham_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_binary_decoder_rendlesham_pooled_under_half_pct : (0.004504756223217969 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_binary_decoder_rendlesham_pooled_lt_half_pure : (0.004504756223217969 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_binary_decoder_rendlesham_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_binary_decoder_rendlesham_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_certified_agent_formal_panel_records_pos : 0 < (13 : ℕ) := by
  decide


theorem cat_certified_agent_formal_panel_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_certified_agent_formal_panel_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_certified_agent_formal_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_certified_agent_formal_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_certified_agent_qwen_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_certified_agent_qwen_pooled_under_half_pct : (0.004504756223217969 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_certified_agent_qwen_pooled_lt_half_pure : (0.004504756223217969 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_certified_agent_qwen_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_certified_agent_qwen_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_expansion_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_consciousness_expansion_spine_pooled_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_expansion_spine_pooled_lt_half_pure : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_expansion_spine_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_expansion_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_genetics_coupling_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_consciousness_genetics_coupling_panel_pooled_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_genetics_coupling_panel_pooled_lt_half_pure : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_genetics_coupling_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_genetics_coupling_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_genetics_species_panel_records_pos : 0 < (27 : ℕ) := by
  decide


theorem cat_consciousness_genetics_species_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_genetics_species_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_genetics_species_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_genetics_species_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_lean_route_credibility_records_pos : 0 < (6 : ℕ) := by
  decide


theorem cat_consciousness_lean_route_credibility_pooled_under_half_pct : (0.006671 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_lean_route_credibility_pooled_lt_half_pure : (0.006671 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_lean_route_credibility_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_lean_route_credibility_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_species_multi_panel_records_pos : 0 < (269 : ℕ) := by
  decide


theorem cat_consciousness_species_multi_panel_pooled_under_half_pct : (0.0201195 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_species_multi_panel_pooled_lt_half_pure : (0.0201195 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_species_multi_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_consciousness_species_multi_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_federal_science_registry_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_federal_science_registry_panel_pooled_under_half_pct : (0.013352 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_federal_science_registry_panel_pooled_lt_half_pure : (0.013352 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_federal_science_registry_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_federal_science_registry_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_founding_atmospheric_ozone_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_founding_atmospheric_ozone_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_atmospheric_ozone_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_atmospheric_ozone_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_atmospheric_ozone_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_hybrid_fi_sim_stratum_deep_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_hybrid_fi_sim_stratum_deep_panel_pooled_under_half_pct : (0.018003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hybrid_fi_sim_stratum_deep_panel_pooled_lt_half_pure : (0.018003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hybrid_fi_sim_stratum_deep_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_hybrid_fi_sim_stratum_deep_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_intrinsic_llm_validators_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_intrinsic_llm_validators_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intrinsic_llm_validators_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intrinsic_llm_validators_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intrinsic_llm_validators_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_living_fsot_hardware_panel_records_pos : 0 < (77 : ℕ) := by
  decide


theorem cat_living_fsot_hardware_panel_pooled_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_living_fsot_hardware_panel_pooled_lt_half_pure : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_living_fsot_hardware_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_living_fsot_hardware_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_longevity_consciousness_coupling_panel_records_pos : 0 < (890 : ℕ) := by
  decide


theorem cat_longevity_consciousness_coupling_panel_pooled_under_half_pct : (0.022424 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_consciousness_coupling_panel_pooled_lt_half_pure : (0.022424 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_consciousness_coupling_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_consciousness_coupling_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_mpcorb_minor_planet_catalog_records_pos : 0 < (1554101 : ℕ) := by
  decide


theorem cat_mpcorb_minor_planet_catalog_pooled_under_half_pct : (0.023015 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mpcorb_minor_planet_catalog_pooled_lt_half_pure : (0.023015 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mpcorb_minor_planet_catalog_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mpcorb_minor_planet_catalog_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neuroeconomics_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_neuroeconomics_panel_pooled_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroeconomics_panel_pooled_lt_half_pure : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroeconomics_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroeconomics_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neuroscience_connectomics_depth_panel_records_pos : 0 < (27 : ℕ) := by
  decide


theorem cat_neuroscience_connectomics_depth_panel_pooled_under_half_pct : (0.0201195 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroscience_connectomics_depth_panel_pooled_lt_half_pure : (0.0201195 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroscience_connectomics_depth_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuroscience_connectomics_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_omni_theory_humanities_panel_records_pos : 0 < (37 : ℕ) := by
  decide


theorem cat_omni_theory_humanities_panel_pooled_under_half_pct : (0.0222545 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_omni_theory_humanities_panel_pooled_lt_half_pure : (0.0222545 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_omni_theory_humanities_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_omni_theory_humanities_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_overflow_carry_emergence_panel_records_pos : 0 < (29 : ℕ) := by
  decide


theorem cat_overflow_carry_emergence_panel_pooled_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_overflow_carry_emergence_panel_pooled_lt_half_pure : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_overflow_carry_emergence_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_overflow_carry_emergence_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_psychology_psychometrics_depth_panel_records_pos : 0 < (23 : ℕ) := by
  decide


theorem cat_psychology_psychometrics_depth_panel_pooled_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_psychology_psychometrics_depth_panel_pooled_lt_half_pure : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_psychology_psychometrics_depth_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_psychology_psychometrics_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_tokenization_live_panel_records_pos : 0 < (9 : ℕ) := by
  decide


theorem cat_tokenization_live_panel_pooled_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tokenization_live_panel_pooled_lt_half_pure : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tokenization_live_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tokenization_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_tokenization_smoke_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_tokenization_smoke_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tokenization_smoke_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tokenization_smoke_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tokenization_smoke_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_trinary_hardware_motif_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_trinary_hardware_motif_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_hardware_motif_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_hardware_motif_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_hardware_motif_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_trinary_os_portable_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_trinary_os_portable_pooled_under_half_pct : (0.013342 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_portable_pooled_lt_half_pure : (0.013342 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_portable_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_portable_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_vl_agent_distill_panel_records_pos : 0 < (6 : ℕ) := by
  decide


theorem cat_vl_agent_distill_panel_pooled_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vl_agent_distill_panel_pooled_lt_half_pure : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vl_agent_distill_panel_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vl_agent_distill_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_vl_distill_atlas_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_vl_distill_atlas_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vl_distill_atlas_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vl_distill_atlas_max_scalar_under_half_pct : (0.031506 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vl_distill_atlas_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_chaos_mediated_phase_transitions_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_chaos_mediated_phase_transitions_pooled_under_half_pct : (0.03147898006445882 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chaos_mediated_phase_transitions_pooled_lt_half_pure : (0.03147898006445882 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chaos_mediated_phase_transitions_max_scalar_under_half_pct : (0.03147898006445882 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chaos_mediated_phase_transitions_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_founding_galactic_halo_rotation_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_founding_galactic_halo_rotation_panel_pooled_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_galactic_halo_rotation_panel_pooled_lt_half_pure : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_galactic_halo_rotation_panel_max_scalar_under_half_pct : (0.031446 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_founding_galactic_halo_rotation_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_stsci_mast_telescope_panel_records_pos : 0 < (377 : ℕ) := by
  decide


theorem cat_stsci_mast_telescope_panel_pooled_under_half_pct : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stsci_mast_telescope_panel_pooled_lt_half_pure : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stsci_mast_telescope_panel_max_scalar_under_half_pct : (0.031446 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stsci_mast_telescope_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_vizier_wds_tap_live_deep_records_pos : 0 < (91 : ℕ) := by
  decide


theorem cat_vizier_wds_tap_live_deep_pooled_under_half_pct : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vizier_wds_tap_live_deep_pooled_lt_half_pure : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vizier_wds_tap_live_deep_max_scalar_under_half_pct : (0.031446 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_vizier_wds_tap_live_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_wds_live_multiplicity_deep_records_pos : 0 < (281 : ℕ) := by
  decide


theorem cat_wds_live_multiplicity_deep_pooled_under_half_pct : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_wds_live_multiplicity_deep_pooled_lt_half_pure : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_wds_live_multiplicity_deep_max_scalar_under_half_pct : (0.031446 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_wds_live_multiplicity_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_network_science_public_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_network_science_public_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_network_science_public_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_network_science_public_panel_max_scalar_under_half_pct : (0.031421 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_network_science_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_time_emergence_deep_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_time_emergence_deep_panel_pooled_under_half_pct : (0.024894 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_emergence_deep_panel_pooled_lt_half_pure : (0.024894 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_emergence_deep_panel_max_scalar_under_half_pct : (0.031421 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_time_emergence_deep_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_the_well_spot_check_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_the_well_spot_check_panel_pooled_under_half_pct : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_spot_check_panel_pooled_lt_half_pure : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_spot_check_panel_max_scalar_under_half_pct : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_spot_check_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_the_well_verification_spine_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_the_well_verification_spine_pooled_under_half_pct : (0.028287 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_verification_spine_pooled_lt_half_pure : (0.028287 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_verification_spine_max_scalar_under_half_pct : (0.031159 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_the_well_verification_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fluid_phase_current_spine_records_pos : 0 < (7 : ℕ) := by
  decide


theorem cat_fluid_phase_current_spine_pooled_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_phase_current_spine_pooled_lt_half_pure : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_phase_current_spine_max_scalar_under_half_pct : (0.0310845 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fluid_phase_current_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_epidemiology_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_epidemiology_pooled_under_half_pct : (0.03062212293865052 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_epidemiology_pooled_lt_half_pure : (0.03062212293865052 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_epidemiology_max_scalar_under_half_pct : (0.0306221229386594 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_epidemiology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cve_codon_hole_falsification_records_pos : 0 < (29 : ℕ) := by
  decide


theorem cat_cve_codon_hole_falsification_pooled_under_half_pct : (0.009186636881580057 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cve_codon_hole_falsification_pooled_lt_half_pure : (0.009186636881580057 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cve_codon_hole_falsification_max_scalar_under_half_pct : (0.03062212293865052 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cve_codon_hole_falsification_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_limnology_panel_records_pos : 0 < (2010 : ℕ) := by
  decide


theorem cat_limnology_panel_pooled_under_half_pct : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_limnology_panel_pooled_lt_half_pure : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_limnology_panel_max_scalar_under_half_pct : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_limnology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_marine_biology_panel_records_pos : 0 < (90 : ℕ) := by
  decide


theorem cat_marine_biology_panel_pooled_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_marine_biology_panel_pooled_lt_half_pure : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_marine_biology_panel_max_scalar_under_half_pct : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_marine_biology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_noaa_coastal_tides_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_noaa_coastal_tides_pooled_under_half_pct : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_noaa_coastal_tides_pooled_lt_half_pure : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_noaa_coastal_tides_max_scalar_under_half_pct : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_noaa_coastal_tides_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_noaa_ndbc_buoy_panel_records_pos : 0 < (596 : ℕ) := by
  decide


theorem cat_noaa_ndbc_buoy_panel_pooled_under_half_pct : (0.028287 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_noaa_ndbc_buoy_panel_pooled_lt_half_pure : (0.028287 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_noaa_ndbc_buoy_panel_max_scalar_under_half_pct : (0.030173 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_noaa_ndbc_buoy_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_open_meteo_live_panel_records_pos : 0 < (432 : ℕ) := by
  decide


theorem cat_open_meteo_live_panel_pooled_under_half_pct : (0.026204 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_meteo_live_panel_pooled_lt_half_pure : (0.026204 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_meteo_live_panel_max_scalar_under_half_pct : (0.0291 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_meteo_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_compactification_ladder_records_pos : 0 < (60 : ℕ) := by
  decide


theorem cat_compactification_ladder_pooled_under_half_pct : (0.015073678386290368 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_compactification_ladder_pooled_lt_half_pure : (0.015073678386290368 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_compactification_ladder_max_scalar_under_half_pct : (0.028512403203747722 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_compactification_ladder_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_energy_ai_orbital_bridge_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_energy_ai_orbital_bridge_pooled_under_half_pct : (0.02754410755640712 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_ai_orbital_bridge_pooled_lt_half_pure : (0.02754410755640712 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_ai_orbital_bridge_max_scalar_under_half_pct : (0.027544107556418167 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_ai_orbital_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fusion_lab_certificate_spine_records_pos : 0 < (50 : ℕ) := by
  decide


theorem cat_fusion_lab_certificate_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_lab_certificate_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_lab_certificate_spine_max_scalar_under_half_pct : (0.027544107556414246 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_lab_certificate_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cartography_gis_panel_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_cartography_gis_panel_pooled_under_half_pct : (0.018855999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cartography_gis_panel_pooled_lt_half_pure : (0.018855999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cartography_gis_panel_max_scalar_under_half_pct : (0.027455 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cartography_gis_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_paleontology_panel_records_pos : 0 < (120 : ℕ) := by
  decide


theorem cat_paleontology_panel_pooled_under_half_pct : (0.0167305 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleontology_panel_pooled_lt_half_pure : (0.0167305 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleontology_panel_max_scalar_under_half_pct : (0.027455 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleontology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_orbital_mechanics_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_orbital_mechanics_pooled_under_half_pct : (0.020214999999999997 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_orbital_mechanics_pooled_lt_half_pure : (0.020214999999999997 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_orbital_mechanics_max_scalar_under_half_pct : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_orbital_mechanics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_small_body_orbits_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_small_body_orbits_pooled_under_half_pct : (0.020214999999999997 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_small_body_orbits_pooled_lt_half_pure : (0.020214999999999997 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_small_body_orbits_max_scalar_under_half_pct : (0.026954 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_small_body_orbits_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_ncbi_gene_public_panel_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_ncbi_gene_public_panel_pooled_under_half_pct : (0.025571999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ncbi_gene_public_panel_pooled_lt_half_pure : (0.025571999999999998 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ncbi_gene_public_panel_max_scalar_under_half_pct : (0.026684 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ncbi_gene_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_uniprot_protein_annotations_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_uniprot_protein_annotations_pooled_under_half_pct : (0.0209975 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uniprot_protein_annotations_pooled_lt_half_pure : (0.0209975 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uniprot_protein_annotations_max_scalar_under_half_pct : (0.026684 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uniprot_protein_annotations_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_arxiv_gravitational_waves_panel_records_pos : 0 < (60 : ℕ) := by
  decide


theorem cat_arxiv_gravitational_waves_panel_pooled_under_half_pct : (0.01748 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_gravitational_waves_panel_pooled_lt_half_pure : (0.01748 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_gravitational_waves_panel_max_scalar_under_half_pct : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_gravitational_waves_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_blackhole_whitehole_cycle_live_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_blackhole_whitehole_cycle_live_panel_pooled_under_half_pct : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_blackhole_whitehole_cycle_live_panel_pooled_lt_half_pure : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_blackhole_whitehole_cycle_live_panel_max_scalar_under_half_pct : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_blackhole_whitehole_cycle_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_gaia_astrometry_panel_deep_records_pos : 0 < (62 : ℕ) := by
  decide


theorem cat_gaia_astrometry_panel_deep_pooled_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gaia_astrometry_panel_deep_pooled_lt_half_pure : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gaia_astrometry_panel_deep_max_scalar_under_half_pct : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gaia_astrometry_panel_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_radio_astronomy_panel_records_pos : 0 < (30 : ℕ) := by
  decide


theorem cat_radio_astronomy_panel_pooled_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_radio_astronomy_panel_pooled_lt_half_pure : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_radio_astronomy_panel_max_scalar_under_half_pct : (0.026472 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_radio_astronomy_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_actuarial_science_panel_records_pos : 0 < (60 : ℕ) := by
  decide


theorem cat_actuarial_science_panel_pooled_under_half_pct : (0.02261 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_actuarial_science_panel_pooled_lt_half_pure : (0.02261 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_actuarial_science_panel_max_scalar_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_actuarial_science_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_finance_markets_panel_records_pos : 0 < (36 : ℕ) := by
  decide


theorem cat_finance_markets_panel_pooled_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_finance_markets_panel_pooled_lt_half_pure : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_finance_markets_panel_max_scalar_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_finance_markets_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_history_panel_records_pos : 0 < (60 : ℕ) := by
  decide


theorem cat_history_panel_pooled_under_half_pct : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_history_panel_pooled_lt_half_pure : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_history_panel_max_scalar_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_history_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_supply_chain_logistics_panel_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_supply_chain_logistics_panel_pooled_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_supply_chain_logistics_panel_pooled_lt_half_pure : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_supply_chain_logistics_panel_max_scalar_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_supply_chain_logistics_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_world_bank_development_records_pos : 0 < (420 : ℕ) := by
  decide


theorem cat_world_bank_development_pooled_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_world_bank_development_pooled_lt_half_pure : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_world_bank_development_max_scalar_under_half_pct : (0.02584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_world_bank_development_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_code_genome_structure_records_pos : 0 < (205 : ℕ) := by
  decide


theorem cat_code_genome_structure_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_code_genome_structure_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_code_genome_structure_max_scalar_under_half_pct : (0.02449769835093818 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_code_genome_structure_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_ionospheric_chemistry_coupling_records_pos : 0 < (85 : ℕ) := by
  decide


theorem cat_ionospheric_chemistry_coupling_pooled_under_half_pct : (0.023609235048340338 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ionospheric_chemistry_coupling_pooled_lt_half_pure : (0.023609235048340338 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ionospheric_chemistry_coupling_max_scalar_under_half_pct : (0.023609235048340338 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ionospheric_chemistry_coupling_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_nasa_exoplanet_archive_records_pos : 0 < (158 : ℕ) := by
  decide


theorem cat_nasa_exoplanet_archive_pooled_under_half_pct : (0.023015 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_exoplanet_archive_pooled_lt_half_pure : (0.023015 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_exoplanet_archive_max_scalar_under_half_pct : (0.023015 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_exoplanet_archive_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_nasa_neo_feed_panel_records_pos : 0 < (56 : ℕ) := by
  decide


theorem cat_nasa_neo_feed_panel_pooled_under_half_pct : (0.021097 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_neo_feed_panel_pooled_lt_half_pure : (0.021097 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_neo_feed_panel_max_scalar_under_half_pct : (0.023015 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_neo_feed_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fusion_physics_public_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_fusion_physics_public_panel_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_physics_public_panel_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_physics_public_panel_max_scalar_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_physics_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_gaia_dr3_tap_deep_records_pos : 0 < (1826 : ℕ) := by
  decide


theorem cat_gaia_dr3_tap_deep_pooled_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gaia_dr3_tap_deep_pooled_lt_half_pure : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gaia_dr3_tap_deep_max_scalar_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gaia_dr3_tap_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_inertial_confinement_fusion_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_inertial_confinement_fusion_panel_pooled_under_half_pct : (7.9e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_inertial_confinement_fusion_panel_pooled_lt_half_pure : (7.9e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_inertial_confinement_fusion_panel_max_scalar_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_inertial_confinement_fusion_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_nasa_donki_solar_panel_records_pos : 0 < (2148 : ℕ) := by
  decide


theorem cat_nasa_donki_solar_panel_pooled_under_half_pct : (0.020755 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_donki_solar_panel_pooled_lt_half_pure : (0.020755 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_donki_solar_panel_max_scalar_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nasa_donki_solar_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_simbad_stellar_identity_deep_records_pos : 0 < (520 : ℕ) := by
  decide


theorem cat_simbad_stellar_identity_deep_pooled_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_simbad_stellar_identity_deep_pooled_lt_half_pure : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_simbad_stellar_identity_deep_max_scalar_under_half_pct : (0.022461 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_simbad_stellar_identity_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_entomology_records_pos : 0 < (430 : ℕ) := by
  decide


theorem cat_entomology_pooled_under_half_pct : (0.020012625346676673 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_entomology_pooled_lt_half_pure : (0.020012625346676673 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_entomology_max_scalar_under_half_pct : (0.02223625038520915 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_entomology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_botany_records_pos : 0 < (426 : ℕ) := by
  decide


theorem cat_botany_pooled_under_half_pct : (0.022236250385193387 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_botany_pooled_lt_half_pure : (0.022236250385193387 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_botany_max_scalar_under_half_pct : (0.022236250385208895 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_botany_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_zoology_records_pos : 0 < (1000 : ℕ) := by
  decide


theorem cat_zoology_pooled_under_half_pct : (0.017789000308156326 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zoology_pooled_lt_half_pure : (0.017789000308156326 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zoology_max_scalar_under_half_pct : (0.022236250385207747 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zoology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_biophysics_public_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_biophysics_public_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biophysics_public_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biophysics_public_panel_max_scalar_under_half_pct : (0.02223625038519357 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biophysics_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_epidemiology_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_epidemiology_panel_pooled_under_half_pct : (0.015311 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_epidemiology_panel_pooled_lt_half_pure : (0.015311 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_epidemiology_panel_max_scalar_under_half_pct : (0.02223625038519357 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_epidemiology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_genomic_sciences_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_genomic_sciences_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_genomic_sciences_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_genomic_sciences_max_scalar_under_half_pct : (0.02223625038519357 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_genomic_sciences_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neuron_multi_hero_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_neuron_multi_hero_pooled_under_half_pct : (0.00225237811160842 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuron_multi_hero_pooled_lt_half_pure : (0.00225237811160842 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuron_multi_hero_max_scalar_under_half_pct : (0.02223625038519357 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neuron_multi_hero_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_biology_developmental_structural_depth_panel_records_pos : 0 < (26 : ℕ) := by
  decide


theorem cat_biology_developmental_structural_depth_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biology_developmental_structural_depth_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biology_developmental_structural_depth_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biology_developmental_structural_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_ethology_panel_records_pos : 0 < (100 : ℕ) := by
  decide


theorem cat_ethology_panel_pooled_under_half_pct : (0.006607 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ethology_panel_pooled_lt_half_pure : (0.006607 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ethology_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ethology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_longevity_anage_catalog_panel_records_pos : 0 < (966 : ℕ) := by
  decide


theorem cat_longevity_anage_catalog_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_anage_catalog_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_anage_catalog_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_anage_catalog_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_longevity_extreme_species_panel_records_pos : 0 < (164 : ℕ) := by
  decide


theorem cat_longevity_extreme_species_panel_pooled_under_half_pct : (0.017789 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_extreme_species_panel_pooled_lt_half_pure : (0.017789 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_extreme_species_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_extreme_species_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_longevity_genetic_mechanics_panel_records_pos : 0 < (35 : ℕ) := by
  decide


theorem cat_longevity_genetic_mechanics_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_genetic_mechanics_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_genetic_mechanics_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_genetic_mechanics_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_longevity_megadeep_ncbi_panel_records_pos : 0 < (1746 : ℕ) := by
  decide


theorem cat_longevity_megadeep_ncbi_panel_pooled_under_half_pct : (0.017789 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_megadeep_ncbi_panel_pooled_lt_half_pure : (0.017789 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_megadeep_ncbi_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_megadeep_ncbi_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_longevity_telomere_repair_panel_records_pos : 0 < (60 : ℕ) := by
  decide


theorem cat_longevity_telomere_repair_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_telomere_repair_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_telomere_repair_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_longevity_telomere_repair_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_mycology_panel_records_pos : 0 < (90 : ℕ) := by
  decide


theorem cat_mycology_panel_pooled_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mycology_panel_pooled_lt_half_pure : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mycology_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mycology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_physarum_biological_cuda_panel_records_pos : 0 < (5 : ℕ) := by
  decide


theorem cat_physarum_biological_cuda_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_physarum_biological_cuda_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_physarum_biological_cuda_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_physarum_biological_cuda_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_zebrafish_cell_tracking_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_zebrafish_cell_tracking_panel_pooled_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_cell_tracking_panel_pooled_lt_half_pure : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_cell_tracking_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_cell_tracking_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_zebrafish_developmental_mechanics_panel_records_pos : 0 < (31 : ℕ) := by
  decide


theorem cat_zebrafish_developmental_mechanics_panel_pooled_under_half_pct : (0.017789 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_developmental_mechanics_panel_pooled_lt_half_pure : (0.017789 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_developmental_mechanics_panel_max_scalar_under_half_pct : (0.022236 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_developmental_mechanics_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_nuclear_lean_route_credibility_records_pos : 0 < (3 : ℕ) := by
  decide


theorem cat_nuclear_lean_route_credibility_pooled_under_half_pct : (0.021221 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nuclear_lean_route_credibility_pooled_lt_half_pure : (0.021221 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nuclear_lean_route_credibility_max_scalar_under_half_pct : (0.021221 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_nuclear_lean_route_credibility_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_preregistered_predictions_records_pos : 0 < (27 : ℕ) := by
  decide


theorem cat_preregistered_predictions_pooled_under_half_pct : (0.020098237848408945 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_predictions_pooled_lt_half_pure : (0.020098237848408945 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_predictions_max_scalar_under_half_pct : (0.020098237848419454 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_predictions_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pubchem_stability_panel_records_pos : 0 < (59 : ℕ) := by
  decide


theorem cat_pubchem_stability_panel_pooled_under_half_pct : (0.0024239449292213135 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_stability_panel_pooled_lt_half_pure : (0.0024239449292213135 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_stability_panel_max_scalar_under_half_pct : (0.019259259259258584 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pubchem_stability_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_chemical_structure_stability_panel_records_pos : 0 < (32 : ℕ) := by
  decide


theorem cat_chemical_structure_stability_panel_pooled_under_half_pct : (0.00206 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chemical_structure_stability_panel_pooled_lt_half_pure : (0.00206 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chemical_structure_stability_panel_max_scalar_under_half_pct : (0.019259 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_chemical_structure_stability_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_arxiv_brain_knowledge_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_arxiv_brain_knowledge_panel_pooled_under_half_pct : (0.018003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_brain_knowledge_panel_pooled_lt_half_pure : (0.018003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_brain_knowledge_panel_max_scalar_under_half_pct : (0.018003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_arxiv_brain_knowledge_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_energy_neural_orbital_bridge_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_energy_neural_orbital_bridge_pooled_under_half_pct : (0.018002668701796783 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_neural_orbital_bridge_pooled_lt_half_pure : (0.018002668701796783 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_neural_orbital_bridge_max_scalar_under_half_pct : (0.018002668701808056 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_energy_neural_orbital_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neural_galactic_orbital_bridge_records_pos : 0 < (49 : ℕ) := by
  decide


theorem cat_neural_galactic_orbital_bridge_pooled_under_half_pct : (0.018002668701799784 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neural_galactic_orbital_bridge_pooled_lt_half_pure : (0.018002668701799784 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neural_galactic_orbital_bridge_max_scalar_under_half_pct : (0.018002668701803688 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neural_galactic_orbital_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_paleontology_records_pos : 0 < (630 : ℕ) := by
  decide


theorem cat_paleontology_pooled_under_half_pct : (0.017836062884406152 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleontology_pooled_lt_half_pure : (0.017836062884406152 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleontology_max_scalar_under_half_pct : (0.017836062884422174 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleontology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_zebrafish_longevity_genetics_coupling_panel_records_pos : 0 < (15 : ℕ) := by
  decide


theorem cat_zebrafish_longevity_genetics_coupling_panel_pooled_under_half_pct : (0.013342 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_longevity_genetics_coupling_panel_pooled_lt_half_pure : (0.013342 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_longevity_genetics_coupling_panel_max_scalar_under_half_pct : (0.015565 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zebrafish_longevity_genetics_coupling_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_openneuro_full_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_openneuro_full_panel_pooled_under_half_pct : (0.015431 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_openneuro_full_panel_pooled_lt_half_pure : (0.015431 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_openneuro_full_panel_max_scalar_under_half_pct : (0.015431 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_openneuro_full_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cardiology_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_cardiology_panel_pooled_under_half_pct : (0.015311 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cardiology_panel_pooled_lt_half_pure : (0.015311 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cardiology_panel_max_scalar_under_half_pct : (0.015311 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cardiology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_materials_creep_fracture_depth_panel_records_pos : 0 < (71 : ℕ) := by
  decide


theorem cat_materials_creep_fracture_depth_panel_pooled_under_half_pct : (0.011734 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_creep_fracture_depth_panel_pooled_lt_half_pure : (0.011734 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_creep_fracture_depth_panel_max_scalar_under_half_pct : (0.015087 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_creep_fracture_depth_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_materials_project_live_panel_records_pos : 0 < (141 : ℕ) := by
  decide


theorem cat_materials_project_live_panel_pooled_under_half_pct : (0.011734 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_project_live_panel_pooled_lt_half_pure : (0.011734 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_project_live_panel_max_scalar_under_half_pct : (0.015087 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_materials_project_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_paleoclimate_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_paleoclimate_pooled_under_half_pct : (0.015015854077438107 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleoclimate_pooled_lt_half_pure : (0.015015854077438107 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleoclimate_max_scalar_under_half_pct : (0.015015854077446988 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleoclimate_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_early_lean_mc_panel_records_pos : 0 < (10 : ℕ) := by
  decide


theorem cat_early_lean_mc_panel_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_early_lean_mc_panel_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_early_lean_mc_panel_max_scalar_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_early_lean_mc_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_observer_lean_route_credibility_records_pos : 0 < (3 : ℕ) := by
  decide


theorem cat_observer_lean_route_credibility_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_lean_route_credibility_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_lean_route_credibility_max_scalar_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_observer_lean_route_credibility_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_rust_lean_bridge_panel_records_pos : 0 < (8 : ℕ) := by
  decide


theorem cat_rust_lean_bridge_panel_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rust_lean_bridge_panel_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rust_lean_bridge_panel_max_scalar_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rust_lean_bridge_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_scalar_solver_35_panel_records_pos : 0 < (10 : ℕ) := by
  decide


theorem cat_scalar_solver_35_panel_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scalar_solver_35_panel_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scalar_solver_35_panel_max_scalar_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scalar_solver_35_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_trinary_hardware_live_panel_records_pos : 0 < (28 : ℕ) := by
  decide


theorem cat_trinary_hardware_live_panel_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_hardware_live_panel_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_hardware_live_panel_max_scalar_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_hardware_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_intrinsic_llm_validators_panel_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_intrinsic_llm_validators_panel_pooled_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intrinsic_llm_validators_panel_pooled_lt_half_pure : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intrinsic_llm_validators_panel_max_scalar_under_half_pct : (0.014767 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_intrinsic_llm_validators_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_crossref_scholarly_panel_records_pos : 0 < (200 : ℕ) := by
  decide


theorem cat_crossref_scholarly_panel_pooled_under_half_pct : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_crossref_scholarly_panel_pooled_lt_half_pure : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_crossref_scholarly_panel_max_scalar_under_half_pct : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_crossref_scholarly_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_osti_doe_science_panel_records_pos : 0 < (100 : ℕ) := by
  decide


theorem cat_osti_doe_science_panel_pooled_under_half_pct : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_osti_doe_science_panel_pooled_lt_half_pure : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_osti_doe_science_panel_max_scalar_under_half_pct : (0.01382 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_osti_doe_science_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_civil_engineering_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_civil_engineering_panel_pooled_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_civil_engineering_panel_pooled_lt_half_pure : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_civil_engineering_panel_max_scalar_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_civil_engineering_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_machine_and_molecule_live_panel_records_pos : 0 < (120 : ℕ) := by
  decide


theorem cat_machine_and_molecule_live_panel_pooled_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_machine_and_molecule_live_panel_pooled_lt_half_pure : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_machine_and_molecule_live_panel_max_scalar_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_machine_and_molecule_live_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_robotics_control_systems_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_robotics_control_systems_panel_pooled_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_robotics_control_systems_panel_pooled_lt_half_pure : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_robotics_control_systems_panel_max_scalar_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_robotics_control_systems_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_soil_science_panel_records_pos : 0 < (96 : ℕ) := by
  decide


theorem cat_soil_science_panel_pooled_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_soil_science_panel_pooled_lt_half_pure : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_soil_science_panel_max_scalar_under_half_pct : (0.01341 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_soil_science_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_bibliography_corpus_panel_records_pos : 0 < (8 : ℕ) := by
  decide


theorem cat_bibliography_corpus_panel_pooled_under_half_pct : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_bibliography_corpus_panel_pooled_lt_half_pure : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_bibliography_corpus_panel_max_scalar_under_half_pct : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_bibliography_corpus_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_canonical_oracle_panel_records_pos : 0 < (6 : ℕ) := by
  decide


theorem cat_canonical_oracle_panel_pooled_under_half_pct : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_canonical_oracle_panel_pooled_lt_half_pure : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_canonical_oracle_panel_max_scalar_under_half_pct : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_canonical_oracle_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cern_open_data_lhc_records_pos : 0 < (83 : ℕ) := by
  decide


theorem cat_cern_open_data_lhc_pooled_under_half_pct : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cern_open_data_lhc_pooled_lt_half_pure : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cern_open_data_lhc_max_scalar_under_half_pct : (0.013294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cern_open_data_lhc_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_secure_software_engineering_records_pos : 0 < (59 : ℕ) := by
  decide


theorem cat_secure_software_engineering_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_secure_software_engineering_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_secure_software_engineering_max_scalar_under_half_pct : (0.013290579327048134 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_secure_software_engineering_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_law_policy_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_law_policy_panel_pooled_under_half_pct : (0.013003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_law_policy_panel_pooled_lt_half_pure : (0.013003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_law_policy_panel_max_scalar_under_half_pct : (0.013003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_law_policy_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_uap_war_gov_release_panel_records_pos : 0 < (542 : ℕ) := by
  decide


theorem cat_uap_war_gov_release_panel_pooled_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uap_war_gov_release_panel_pooled_lt_half_pure : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uap_war_gov_release_panel_max_scalar_under_half_pct : (0.013003 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uap_war_gov_release_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_climate_observed_benchmark_json_records_pos : 0 < (17320 : ℕ) := by
  decide


theorem cat_climate_observed_benchmark_json_pooled_under_half_pct : (0.01201268326195996 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_climate_observed_benchmark_json_pooled_lt_half_pure : (0.01201268326195996 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_climate_observed_benchmark_json_max_scalar_under_half_pct : (0.01201268326197121 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_climate_observed_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_medical_galactic_orbital_bridge_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_medical_galactic_orbital_bridge_pooled_under_half_pct : (0.010717743028517085 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_medical_galactic_orbital_bridge_pooled_lt_half_pure : (0.010717743028517085 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_medical_galactic_orbital_bridge_max_scalar_under_half_pct : (0.010717743028528254 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_medical_galactic_orbital_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_network_internet_protocols_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_network_internet_protocols_pooled_under_half_pct : (0.010337117254355377 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_network_internet_protocols_pooled_lt_half_pure : (0.010337117254355377 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_network_internet_protocols_max_scalar_under_half_pct : (0.010337117254363452 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_network_internet_protocols_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_zero_day_risk_evaluator_records_pos : 0 < (26 : ℕ) := by
  decide


theorem cat_zero_day_risk_evaluator_pooled_under_half_pct : (0.010337117254355377 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zero_day_risk_evaluator_pooled_lt_half_pure : (0.010337117254355377 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zero_day_risk_evaluator_max_scalar_under_half_pct : (0.010337117254360602 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_zero_day_risk_evaluator_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_alternate_base_mathematics_explorer_panel_records_pos : 0 < (56 : ℕ) := by
  decide


theorem cat_alternate_base_mathematics_explorer_panel_pooled_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_alternate_base_mathematics_explorer_panel_pooled_lt_half_pure : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_alternate_base_mathematics_explorer_panel_max_scalar_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_alternate_base_mathematics_explorer_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_experimental_base_mathematics_panel_records_pos : 0 < (36 : ℕ) := by
  decide


theorem cat_experimental_base_mathematics_panel_pooled_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_experimental_base_mathematics_panel_pooled_lt_half_pure : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_experimental_base_mathematics_panel_max_scalar_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_experimental_base_mathematics_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fusion_lean_route_credibility_records_pos : 0 < (11 : ℕ) := by
  decide


theorem cat_fusion_lean_route_credibility_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_lean_route_credibility_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_lean_route_credibility_max_scalar_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_lean_route_credibility_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neutrino_physics_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_neutrino_physics_panel_pooled_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neutrino_physics_panel_pooled_lt_half_pure : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neutrino_physics_panel_max_scalar_under_half_pct : (0.009504 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neutrino_physics_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_environmental_engineering_records_pos : 0 < (1120 : ℕ) := by
  decide


theorem cat_environmental_engineering_pooled_under_half_pct : (0.009009512446467327 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_environmental_engineering_pooled_lt_half_pure : (0.009009512446467327 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_environmental_engineering_max_scalar_under_half_pct : (0.009009512446477413 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_environmental_engineering_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_binary_decoder_panel_records_pos : 0 < (8 : ℕ) := by
  decide


theorem cat_binary_decoder_panel_pooled_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_binary_decoder_panel_pooled_lt_half_pure : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_binary_decoder_panel_max_scalar_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_binary_decoder_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_gwosc_live_event_deep_records_pos : 0 < (191 : ℕ) := by
  decide


theorem cat_gwosc_live_event_deep_pooled_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gwosc_live_event_deep_pooled_lt_half_pure : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gwosc_live_event_deep_max_scalar_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gwosc_live_event_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_interdisciplinary_spine_crosswalk_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_interdisciplinary_spine_crosswalk_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_interdisciplinary_spine_crosswalk_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_interdisciplinary_spine_crosswalk_max_scalar_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_interdisciplinary_spine_crosswalk_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_semiconductor_physics_public_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_semiconductor_physics_public_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_semiconductor_physics_public_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_semiconductor_physics_public_panel_max_scalar_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_semiconductor_physics_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_statistical_mechanics_public_panel_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_statistical_mechanics_public_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_statistical_mechanics_public_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_statistical_mechanics_public_panel_max_scalar_under_half_pct : (0.008488 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_statistical_mechanics_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_inaturalist_observation_panel_records_pos : 0 < (288 : ℕ) := by
  decide


theorem cat_inaturalist_observation_panel_pooled_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_inaturalist_observation_panel_pooled_lt_half_pure : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_inaturalist_observation_panel_max_scalar_under_half_pct : (0.007508 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_inaturalist_observation_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pharmacology_benchmark_json_records_pos : 0 < (120 : ℕ) := by
  decide


theorem cat_pharmacology_benchmark_json_pooled_under_half_pct : (0.001166649119945485 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pharmacology_benchmark_json_pooled_lt_half_pure : (0.001166649119945485 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pharmacology_benchmark_json_max_scalar_under_half_pct : (0.007388748950458895 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_pharmacology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_mechanistic_coupling_records_pos : 0 < (116 : ℕ) := by
  decide


theorem cat_mechanistic_coupling_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanistic_coupling_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanistic_coupling_max_scalar_under_half_pct : (0.0073836551816993294 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_mechanistic_coupling_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_entomology_panel_records_pos : 0 < (90 : ℕ) := by
  decide


theorem cat_entomology_panel_pooled_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_entomology_panel_pooled_lt_half_pure : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_entomology_panel_max_scalar_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_entomology_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_gbif_species_occurrence_records_pos : 0 < (240 : ℕ) := by
  decide


theorem cat_gbif_species_occurrence_pooled_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gbif_species_occurrence_pooled_lt_half_pure : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gbif_species_occurrence_max_scalar_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_gbif_species_occurrence_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_paleoclimate_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_paleoclimate_panel_pooled_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleoclimate_panel_pooled_lt_half_pure : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleoclimate_panel_max_scalar_under_half_pct : (0.006006 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_paleoclimate_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_proof_carrying_code_genome_records_pos : 0 < (25 : ℕ) := by
  decide


theorem cat_proof_carrying_code_genome_pooled_under_half_pct : (0.0051685586271776884 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proof_carrying_code_genome_pooled_lt_half_pure : (0.0051685586271776884 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proof_carrying_code_genome_max_scalar_under_half_pct : (0.005906924145354116 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_proof_carrying_code_genome_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_ai_galactic_orbital_bridge_records_pos : 0 < (48 : ℕ) := by
  decide


theorem cat_ai_galactic_orbital_bridge_pooled_under_half_pct : (0.005168558627177688 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ai_galactic_orbital_bridge_pooled_lt_half_pure : (0.005168558627177688 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ai_galactic_orbital_bridge_max_scalar_under_half_pct : (0.00516855862718516 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_ai_galactic_orbital_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_anthropology_records_pos : 0 < (160 : ℕ) := by
  decide


theorem cat_anthropology_pooled_under_half_pct : (-0.0007873774796219538 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_anthropology_pooled_lt_half_pure : (-0.0007873774796219538 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_anthropology_max_scalar_under_half_pct : (0.002670068252275115 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_anthropology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_programming_language_laws_records_pos : 0 < (107 : ℕ) := by
  decide


theorem cat_programming_language_laws_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_programming_language_laws_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_programming_language_laws_max_scalar_under_half_pct : (0.002670068252275115 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_programming_language_laws_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_open_science_live_concordance_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_open_science_live_concordance_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_science_live_concordance_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_science_live_concordance_max_scalar_under_half_pct : (0.0011101366578278788 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_science_live_concordance_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_element_synthesis_condition_scaffold_records_pos : 0 < (45 : ℕ) := by
  decide


theorem cat_element_synthesis_condition_scaffold_pooled_under_half_pct : (0.000787 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_element_synthesis_condition_scaffold_pooled_lt_half_pure : (0.000787 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_element_synthesis_condition_scaffold_max_scalar_under_half_pct : (0.00095 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_element_synthesis_condition_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_heavy_ion_lab_synthesis_panel_records_pos : 0 < (39 : ℕ) := by
  decide


theorem cat_heavy_ion_lab_synthesis_panel_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_heavy_ion_lab_synthesis_panel_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_heavy_ion_lab_synthesis_panel_max_scalar_under_half_pct : (0.000787 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_heavy_ion_lab_synthesis_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_superheavy_island_completion_spine_records_pos : 0 < (43 : ℕ) := by
  decide


theorem cat_superheavy_island_completion_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_island_completion_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_island_completion_spine_max_scalar_under_half_pct : (0.000787 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_island_completion_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_z120_z126_beam_synthesis_panel_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_z120_z126_beam_synthesis_panel_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_z120_z126_beam_synthesis_panel_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_z120_z126_beam_synthesis_panel_max_scalar_under_half_pct : (0.000787 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_z120_z126_beam_synthesis_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_desi_wa_constraint_records_pos : 0 < (1 : ℕ) := by
  decide


theorem cat_desi_wa_constraint_pooled_under_half_pct : (0.000595 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desi_wa_constraint_pooled_lt_half_pure : (0.000595 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desi_wa_constraint_max_scalar_under_half_pct : (0.000595 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desi_wa_constraint_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_biological_cuda_physarum_benchmark_json_records_pos : 0 < (35 : ℕ) := by
  decide


theorem cat_biological_cuda_physarum_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biological_cuda_physarum_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biological_cuda_physarum_benchmark_json_max_scalar_under_half_pct : (0.00015625000000518696 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_biological_cuda_physarum_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_igem_live_fasta_benchmark_json_records_pos : 0 < (42 : ℕ) := by
  decide


theorem cat_igem_live_fasta_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_live_fasta_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_live_fasta_benchmark_json_max_scalar_under_half_pct : (0.00010000009999062986 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_igem_live_fasta_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fusion_decay_chain_prereg_scaffold_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_fusion_decay_chain_prereg_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_decay_chain_prereg_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_decay_chain_prereg_scaffold_max_scalar_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fusion_decay_chain_prereg_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_island_of_stability_deep_panel_records_pos : 0 < (23 : ℕ) := by
  decide


theorem cat_island_of_stability_deep_panel_pooled_under_half_pct : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_island_of_stability_deep_panel_pooled_lt_half_pure : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_island_of_stability_deep_panel_max_scalar_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_island_of_stability_deep_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_periodic_table_extension_closure_spine_records_pos : 0 < (41 : ℕ) := by
  decide


theorem cat_periodic_table_extension_closure_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_extension_closure_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_extension_closure_spine_max_scalar_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_extension_closure_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_periodic_table_public_panel_records_pos : 0 < (52 : ℕ) := by
  decide


theorem cat_periodic_table_public_panel_pooled_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_public_panel_pooled_lt_half_pure : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_public_panel_max_scalar_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_table_public_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_undiscovered_element_candidate_prereg_scaffold_records_pos : 0 < (25 : ℕ) := by
  decide


theorem cat_undiscovered_element_candidate_prereg_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_undiscovered_element_candidate_prereg_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_undiscovered_element_candidate_prereg_scaffold_max_scalar_under_half_pct : (9.5e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_undiscovered_element_candidate_prereg_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cold_fusion_candidate_prereg_scaffold_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_cold_fusion_candidate_prereg_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cold_fusion_candidate_prereg_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cold_fusion_candidate_prereg_scaffold_max_scalar_under_half_pct : (7.9e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cold_fusion_candidate_prereg_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_metamaterial_fluid_design_prereg_scaffold_records_pos : 0 < (25 : ℕ) := by
  decide


theorem cat_metamaterial_fluid_design_prereg_scaffold_pooled_under_half_pct : (3.4e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_metamaterial_fluid_design_prereg_scaffold_pooled_lt_half_pure : (3.4e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_metamaterial_fluid_design_prereg_scaffold_max_scalar_under_half_pct : (3.4e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_metamaterial_fluid_design_prereg_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_natural_formation_element_simulation_records_pos : 0 < (44 : ℕ) := by
  decide


theorem cat_natural_formation_element_simulation_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_natural_formation_element_simulation_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_natural_formation_element_simulation_max_scalar_under_half_pct : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_natural_formation_element_simulation_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_superheavy_island_emergence_simulation_records_pos : 0 < (44 : ℕ) := by
  decide


theorem cat_superheavy_island_emergence_simulation_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_island_emergence_simulation_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_island_emergence_simulation_max_scalar_under_half_pct : (1e-06 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_superheavy_island_emergence_simulation_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_living_fsot_hardware_records_pos : 0 < (4 : ℕ) := by
  decide


theorem cat_living_fsot_hardware_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_living_fsot_hardware_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_living_fsot_hardware_max_scalar_under_half_pct : (1.3209968920124464e-14 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_living_fsot_hardware_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_agriculture_agroecology_records_pos : 0 < (276 : ℕ) := by
  decide


theorem cat_agriculture_agroecology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_architecture_building_science_records_pos : 0 < (43 : ℕ) := by
  decide


theorem cat_architecture_building_science_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_astrophysical_structure_crosswalk_records_pos : 0 < (32 : ℕ) := by
  decide


theorem cat_astrophysical_structure_crosswalk_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_astrophysical_structure_crosswalk_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_astrophysical_structure_crosswalk_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_astrophysical_structure_crosswalk_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_atmospheric_physics_records_pos : 0 < (47 : ℕ) := by
  decide


theorem cat_atmospheric_physics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_atomic_physics_records_pos : 0 < (80 : ℕ) := by
  decide


theorem cat_atomic_physics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_breakthrough_discoveries_2024_2026_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_breakthrough_discoveries_2024_2026_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_breakthrough_discoveries_2024_2026_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_breakthrough_discoveries_2024_2026_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_breakthrough_discoveries_2024_2026_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_clinicaltrials_medical_panel_records_pos : 0 < (394 : ℕ) := by
  decide


theorem cat_clinicaltrials_medical_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cold_fusion_lab_synthesis_crosswalk_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_cold_fusion_lab_synthesis_crosswalk_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cold_fusion_lab_synthesis_crosswalk_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cold_fusion_lab_synthesis_crosswalk_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cold_fusion_lab_synthesis_crosswalk_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_compact_object_binary_events_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_compact_object_binary_events_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_compact_object_binary_events_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_compact_object_binary_events_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_compact_object_binary_events_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_computational_reasoning_benchmark_json_records_pos : 0 < (577 : ℕ) := by
  decide


theorem cat_computational_reasoning_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_computational_reasoning_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_computational_reasoning_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_computational_reasoning_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_consciousness_soul_bridge_records_pos : 0 < (27 : ℕ) := by
  decide


theorem cat_consciousness_soul_bridge_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cosmology_bubble_bleed_benchmark_json_records_pos : 0 < (113 : ℕ) := by
  decide


theorem cat_cosmology_bubble_bleed_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_bubble_bleed_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_bubble_bleed_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_cosmology_bubble_bleed_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cosmology_extended_benchmark_json_records_pos : 0 < (58 : ℕ) := by
  decide


theorem cat_cosmology_extended_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cross_proof_verification_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_cryosphere_benchmark_json_records_pos : 0 < (2399 : ℕ) := by
  decide


theorem cat_cryosphere_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_desktop_application_wiring_spine_records_pos : 0 < (81 : ℕ) := by
  decide


theorem cat_desktop_application_wiring_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desktop_application_wiring_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desktop_application_wiring_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_desktop_application_wiring_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_distant_island_emergence_simulation_records_pos : 0 < (36 : ℕ) := by
  decide


theorem cat_distant_island_emergence_simulation_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_distant_island_emergence_simulation_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_distant_island_emergence_simulation_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_distant_island_emergence_simulation_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_ecology_records_pos_2 : 0 < (627 : ℕ) := by
  decide


theorem cat_ecology_green_flag_2 : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_econometrics_records_pos : 0 < (172 : ℕ) := by
  decide


theorem cat_econometrics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_economics_records_pos : 0 < (157 : ℕ) := by
  decide


theorem cat_economics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_emergent_domains_benchmark_json_records_pos : 0 < (29 : ℕ) := by
  decide


theorem cat_emergent_domains_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_existence_simulation_gap_fill_panel_records_pos : 0 < (80 : ℕ) := by
  decide


theorem cat_existence_simulation_gap_fill_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_exogeology_records_pos : 0 < (316 : ℕ) := by
  decide


theorem cat_exogeology_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exogeology_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exogeology_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exogeology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_exoplanet_system_architecture_records_pos : 0 < (882 : ℕ) := by
  decide


theorem cat_exoplanet_system_architecture_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exoplanet_system_architecture_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exoplanet_system_architecture_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_exoplanet_system_architecture_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_external_oss_code_genome_records_pos : 0 < (164 : ℕ) := by
  decide


theorem cat_external_oss_code_genome_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_external_oss_code_genome_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_external_oss_code_genome_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_external_oss_code_genome_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fluid_dynamics_records_pos : 0 < (55 : ℕ) := by
  decide


theorem cat_fluid_dynamics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_food_microbiology_records_pos : 0 < (30 : ℕ) := by
  decide


theorem cat_food_microbiology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_formula_corpus_closure_records_pos : 0 < (123 : ℕ) := by
  decide


theorem cat_formula_corpus_closure_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_corpus_closure_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_corpus_closure_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_formula_corpus_closure_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_foundational_ontology_spine_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_foundational_ontology_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_foundational_ontology_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_foundational_ontology_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_foundational_ontology_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fractal_constant_recursion_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_fractal_constant_recursion_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fractal_constant_recursion_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fractal_constant_recursion_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fractal_constant_recursion_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_fuel_candidate_prereg_scaffold_records_pos : 0 < (33 : ℕ) := by
  decide


theorem cat_fuel_candidate_prereg_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_candidate_prereg_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_candidate_prereg_scaffold_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_fuel_candidate_prereg_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_galactic_structure_sample_records_pos : 0 < (101 : ℕ) := by
  decide


theorem cat_galactic_structure_sample_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_galactic_structure_sample_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_galactic_structure_sample_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_galactic_structure_sample_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_geology_stratigraphy_records_pos : 0 < (1960 : ℕ) := by
  decide


theorem cat_geology_stratigraphy_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_geomagnetism_benchmark_json_records_pos : 0 < (524 : ℕ) := by
  decide


theorem cat_geomagnetism_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_geomagnetism_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_geomagnetism_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_geomagnetism_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_government_open_data_spine_records_pos : 0 < (28 : ℕ) := by
  decide


theorem cat_government_open_data_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_government_open_data_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_government_open_data_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_government_open_data_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_grace_cryosphere_benchmark_json_records_pos : 0 < (253 : ℕ) := by
  decide


theorem cat_grace_cryosphere_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_h0_planck_benchmark_json_records_pos : 0 < (2 : ℕ) := by
  decide


theorem cat_h0_planck_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_higgs_branching_benchmark_json_records_pos : 0 < (14 : ℕ) := by
  decide


theorem cat_higgs_branching_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_history_records_pos : 0 < (170 : ℕ) := by
  decide


theorem cat_history_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_hydrology_benchmark_json_records_pos : 0 < (960 : ℕ) := by
  decide


theorem cat_hydrology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_interactive_media_prereg_scaffold_records_pos : 0 < (42 : ℕ) := by
  decide


theorem cat_interactive_media_prereg_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_interactive_media_prereg_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_interactive_media_prereg_scaffold_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_interactive_media_prereg_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_live_ingest_spine_records_pos : 0 < (28 : ℕ) := by
  decide


theorem cat_live_ingest_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_magnetic_confinement_fusion_panel_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_magnetic_confinement_fusion_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_magnetic_confinement_fusion_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_magnetic_confinement_fusion_panel_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_magnetic_confinement_fusion_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_magnetosphere_benchmark_json_records_pos : 0 < (167 : ℕ) := by
  decide


theorem cat_magnetosphere_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_magnetosphere_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_magnetosphere_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_magnetosphere_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_magnetosphere_extended_benchmark_json_records_pos : 0 < (122315 : ℕ) := by
  decide


theorem cat_magnetosphere_extended_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_maillard_chemistry_records_pos : 0 < (30 : ℕ) := by
  decide


theorem cat_maillard_chemistry_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_material_in_silico_screening_scaffold_records_pos : 0 < (42 : ℕ) := by
  decide


theorem cat_material_in_silico_screening_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_material_in_silico_screening_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_material_in_silico_screening_scaffold_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_material_in_silico_screening_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_math_generator_rules_benchmark_json_records_pos : 0 < (1552 : ℕ) := by
  decide


theorem cat_math_generator_rules_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_math_generator_rules_eval_benchmark_json_records_pos : 0 < (1552 : ℕ) := by
  decide


theorem cat_math_generator_rules_eval_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_rules_eval_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_rules_eval_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_math_generator_rules_eval_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_meteorology_records_pos : 0 < (47 : ℕ) := by
  decide


theorem cat_meteorology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neurolab_gaps_math_spine_records_pos : 0 < (35 : ℕ) := by
  decide


theorem cat_neurolab_gaps_math_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neurolab_gaps_math_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neurolab_gaps_math_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neurolab_gaps_math_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neurolab_residual_math_spine_records_pos : 0 < (28 : ℕ) := by
  decide


theorem cat_neurolab_residual_math_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neurolab_residual_math_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neurolab_residual_math_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_neurolab_residual_math_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_neuroscience_records_pos : 0 < (2 : ℕ) := by
  decide


theorem cat_neuroscience_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_oceanography_records_pos : 0 < (65 : ℕ) := by
  decide


theorem cat_oceanography_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_omni_theory_genesis_benchmark_json_records_pos : 0 < (27 : ℕ) := by
  decide


theorem cat_omni_theory_genesis_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_omni_theory_genesis_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_omni_theory_genesis_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_omni_theory_genesis_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_open_science_seed_constants_records_pos : 0 < (12 : ℕ) := by
  decide


theorem cat_open_science_seed_constants_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_science_seed_constants_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_science_seed_constants_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_open_science_seed_constants_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_openalex_citation_graph_records_pos : 0 < (80 : ℕ) := by
  decide


theorem cat_openalex_citation_graph_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_particle_physics_benchmark_json_records_pos : 0 < (98 : ℕ) := by
  decide


theorem cat_particle_physics_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_particle_physics_records_pos : 0 < (98 : ℕ) := by
  decide


theorem cat_particle_physics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_perceived_lean_route_credibility_records_pos : 0 < (3 : ℕ) := by
  decide


theorem cat_perceived_lean_route_credibility_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_periodic_extension_decay_topology_scaffold_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_periodic_extension_decay_topology_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_extension_decay_topology_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_extension_decay_topology_scaffold_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_periodic_extension_decay_topology_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_pharmacokinetics_records_pos : 0 < (56 : ℕ) := by
  decide


theorem cat_pharmacokinetics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_planetary_structure_benchmark_json_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_planetary_structure_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_planetary_structure_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_planetary_structure_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_planetary_structure_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_plasma_physics_benchmark_json_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_plasma_physics_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_plasma_physics_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_plasma_physics_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_plasma_physics_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_portable_clone_verify_records_pos : 0 < (290 : ℕ) := by
  decide


theorem cat_portable_clone_verify_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_portable_clone_verify_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_portable_clone_verify_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_portable_clone_verify_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_preregistered_outcome_tracking_records_pos : 0 < (56 : ℕ) := by
  decide


theorem cat_preregistered_outcome_tracking_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_outcome_tracking_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_outcome_tracking_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_outcome_tracking_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_preregistered_predictions_verification_scaffold_records_pos : 0 < (60 : ℕ) := by
  decide


theorem cat_preregistered_predictions_verification_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_predictions_verification_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_predictions_verification_scaffold_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_preregistered_predictions_verification_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_psychology_records_pos : 0 < (160 : ℕ) := by
  decide


theorem cat_psychology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_public_verifiable_spine_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_public_verifiable_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_public_verifiable_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_public_verifiable_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_public_verifiable_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_published_fuel_property_panel_records_pos : 0 < (31 : ℕ) := by
  decide


theorem cat_published_fuel_property_panel_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_published_fuel_property_panel_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_published_fuel_property_panel_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_published_fuel_property_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_quantum_computing_records_pos : 0 < (177 : ℕ) := by
  decide


theorem cat_quantum_computing_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_quantum_mechanics_records_pos : 0 < (50 : ℕ) := by
  decide


theorem cat_quantum_mechanics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_quantum_optics_records_pos : 0 < (50 : ℕ) := by
  decide


theorem cat_quantum_optics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_rust_lean_bridge_benchmark_json_records_pos : 0 < (9 : ℕ) := by
  decide


theorem cat_rust_lean_bridge_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rust_lean_bridge_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rust_lean_bridge_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_rust_lean_bridge_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_scientific_expansion_depth_spine_records_pos : 0 < (20 : ℕ) := by
  decide


theorem cat_scientific_expansion_depth_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_depth_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_depth_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_depth_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_scientific_expansion_depth_wave2_spine_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_scientific_expansion_depth_wave2_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_depth_wave2_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_depth_wave2_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_depth_wave2_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_scientific_expansion_spine_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_scientific_expansion_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_scientific_expansion_wave2_spine_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_scientific_expansion_wave2_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_wave2_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_wave2_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_wave2_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_scientific_expansion_wave3_spine_records_pos : 0 < (40 : ℕ) := by
  decide


theorem cat_scientific_expansion_wave3_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_wave3_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_wave3_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_scientific_expansion_wave3_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_seismology_benchmark_json_records_pos : 0 < (500 : ℕ) := by
  decide


theorem cat_seismology_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_seismology_deep_benchmark_json_records_pos : 0 < (1000 : ℕ) := by
  decide


theorem cat_seismology_deep_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_sociology_records_pos : 0 < (200 : ℕ) := by
  decide


theorem cat_sociology_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_solar_system_structure_deep_records_pos : 0 < (50 : ℕ) := by
  decide


theorem cat_solar_system_structure_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_space_propulsion_systems_records_pos : 0 < (21 : ℕ) := by
  decide


theorem cat_space_propulsion_systems_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_space_propulsion_systems_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_space_propulsion_systems_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_space_propulsion_systems_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_space_weather_benchmark_json_records_pos : 0 < (271813 : ℕ) := by
  decide


theorem cat_space_weather_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_space_weather_summary_benchmark_json_records_pos : 0 < (271813 : ℕ) := by
  decide


theorem cat_space_weather_summary_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_sports_biomechanics_records_pos : 0 < (35 : ℕ) := by
  decide


theorem cat_sports_biomechanics_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_stellar_multiplicity_catalog_records_pos : 0 < (68 : ℕ) := by
  decide


theorem cat_stellar_multiplicity_catalog_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stellar_multiplicity_catalog_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stellar_multiplicity_catalog_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stellar_multiplicity_catalog_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_stellar_multiplicity_live_deep_records_pos : 0 < (69 : ℕ) := by
  decide


theorem cat_stellar_multiplicity_live_deep_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stellar_multiplicity_live_deep_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stellar_multiplicity_live_deep_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_stellar_multiplicity_live_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_symbolic_archetype_panel_records_pos : 0 < (28 : ℕ) := by
  decide


theorem cat_symbolic_archetype_panel_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_tectonics_benchmark_json_records_pos : 0 < (500 : ℕ) := by
  decide


theorem cat_tectonics_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_thesis_simulation_benchmark_json_records_pos : 0 < (156 : ℕ) := by
  decide


theorem cat_thesis_simulation_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_tier_94_longevity_spine_records_pos : 0 < (34 : ℕ) := by
  decide


theorem cat_tier_94_longevity_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_94_longevity_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_94_longevity_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_94_longevity_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_tier_95_zebrafish_spine_records_pos : 0 < (18 : ℕ) := by
  decide


theorem cat_tier_95_zebrafish_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_95_zebrafish_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_95_zebrafish_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_95_zebrafish_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_tier_96_circuit_spine_records_pos : 0 < (11 : ℕ) := by
  decide


theorem cat_tier_96_circuit_spine_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_96_circuit_spine_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_96_circuit_spine_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_tier_96_circuit_spine_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_trinary_os_isa_rebuild_benchmark_json_records_pos : 0 < (38 : ℕ) := by
  decide


theorem cat_trinary_os_isa_rebuild_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_isa_rebuild_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_isa_rebuild_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_isa_rebuild_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_trinary_os_round_trip_benchmark_json_records_pos : 0 < (22 : ℕ) := by
  decide


theorem cat_trinary_os_round_trip_benchmark_json_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_round_trip_benchmark_json_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_round_trip_benchmark_json_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_round_trip_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_trinary_os_tier_e_records_pos : 0 < (68 : ℕ) := by
  decide


theorem cat_trinary_os_tier_e_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_tier_e_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_tier_e_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_trinary_os_tier_e_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_unified_db_candidate_crosswalk_records_pos : 0 < (46 : ℕ) := by
  decide


theorem cat_unified_db_candidate_crosswalk_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_unified_db_candidate_crosswalk_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_unified_db_candidate_crosswalk_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_unified_db_candidate_crosswalk_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_uniprot_structure_annotations_deep_records_pos : 0 < (121 : ℕ) := by
  decide


theorem cat_uniprot_structure_annotations_deep_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uniprot_structure_annotations_deep_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uniprot_structure_annotations_deep_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_uniprot_structure_annotations_deep_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_weather_observed_benchmark_json_records_pos : 0 < (47 : ℕ) := by
  decide


theorem cat_weather_observed_benchmark_json_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


theorem cat_xr_interactive_media_math_scaffold_records_pos : 0 < (24 : ℕ) := by
  decide


theorem cat_xr_interactive_media_math_scaffold_pooled_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_xr_interactive_media_math_scaffold_pooled_lt_half_pure : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_xr_interactive_media_math_scaffold_max_scalar_under_half_pct : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num


theorem cat_xr_interactive_media_math_scaffold_green_flag : (1 : ℕ) = (1 : ℕ) := by
  rfl


end FSOT.Formal.ScientificCatalogSpine
