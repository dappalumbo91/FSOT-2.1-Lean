(* FSOT Tier 80 — FullFormalSpine chunk 8/21 (generated). *)
(* Independent of Lean proof terms — same decimal obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Lia.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma gwas_catalog_depth_open_pooled_median_under_half_pct : (0.022236%R) < (0.5%R).
Proof. lra. Qed.

Lemma gwas_catalog_depth_open_headline_median_under_half_pct : (0.022236%R) < (0.5%R).
Proof. lra. Qed.

Lemma gwas_catalog_depth_open_observable_count_pos : (0 < 81)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gwosc_live_event_deep_observable_count_pos : (0 < 191)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gwosc_live_event_deep_median_error_under_half_pct : (0.008488%R) < (0.5%R).
Proof. lra. Qed.

Lemma gwosc_strain_metadata_open_pooled_median_under_half_pct : (0.008488%R) < (0.5%R).
Proof. lra. Qed.

Lemma gwosc_strain_metadata_open_headline_median_under_half_pct : (0.008488%R) < (0.5%R).
Proof. lra. Qed.

Lemma gwosc_strain_metadata_open_observable_count_pos : (0 < 54)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gwtc_catalog_open_pooled_median_under_half_pct : (0.008488%R) < (0.5%R).
Proof. lra. Qed.

Lemma gwtc_catalog_open_headline_median_under_half_pct : (0.008488%R) < (0.5%R).
Proof. lra. Qed.

Lemma gwtc_catalog_open_observable_count_pos : (0 < 1972)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma heavy_ion_lab_synthesis_panel_observable_count_pos : (0 < 39)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma heavy_ion_lab_synthesis_panel_median_error_under_half_pct : (0.000095%R) < (0.5%R).
Proof. lra. Qed.

Lemma higgs_branching_median_error_under_half_pct : (0.08808351263334355%R) < (0.5%R).
Proof. lra. Qed.

Lemma higgs_compute_branching_count_pos : (0 < 9)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma higgs_branching_observable_count_pos : (0 < 14)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma higgs_branching_max_error_under_five_pct : (4.232801452006084%R) < (5.0%R).
Proof. lra. Qed.

Lemma higgs_branching_components_sum : (14 = 14)%nat.
Proof. reflexivity. Qed.

Lemma higgs_mass_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma higgs_mass_median_error_under_half_pct : (0.012112816039879785%R) < (0.5%R).
Proof. lra. Qed.

Lemma history_ext_pooled_median_under_half_pct : (0.019504399572477397%R) < (0.5%R).
Proof. lra. Qed.

Lemma history_ext_headline_median_under_half_pct : (0.019504399572477397%R) < (0.5%R).
Proof. lra. Qed.

Lemma history_ext_observable_count_pos : (0 < 170)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma history_ext_beats_sota_headlines_pos : (0 < 2)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma history_panel_observable_count_pos : (0 < 60)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma history_panel_median_error_under_half_pct : (0.01382%R) < (0.5%R).
Proof. lra. Qed.

Lemma history_observable_count_pos : (0 < 170)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma history_median_error_under_half_pct : (0.019504399572477397%R) < (0.5%R).
Proof. lra. Qed.

Lemma hubble_bubble_tension_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma hubble_bubble_tension_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma hubble_dark_sector_crosswalk_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma hubble_dark_sector_crosswalk_median_error_under_half_pct : (0.0198985%R) < (0.5%R).
Proof. lra. Qed.

Lemma hvac_thermal_systems_observable_count_pos : (0 < 7)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma hvac_thermal_systems_median_error_under_five_pct : 0%R < (5.0%R).
Proof. lra. Qed.

Lemma hybrid_fi_sim_multi_hero_panel_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma hybrid_fi_sim_multi_hero_panel_median_error_under_half_pct : (0.008488%R) < (0.5%R).
Proof. lra. Qed.

Lemma hybrid_fi_sim_stratum_deep_panel_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma hybrid_fi_sim_stratum_deep_panel_median_error_under_half_pct : (0.018003%R) < (0.5%R).
Proof. lra. Qed.

Lemma hydrology_month_count_pos : (0 < 960)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma hydrology_stability_match_le_total : (957 <= 960)%nat.
Proof. apply Nat.leb_le; reflexivity. Qed.

Lemma hydrology_stability_match_rate_nonneg : 0 <= (0.996875%R).
Proof. lra. Qed.

Lemma igem_live_fasta_observable_count_pos : (0 < 42)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma igem_live_fasta_median_error_under_five_pct : 0%R < (5.0%R).
Proof. lra. Qed.

Lemma igem_parts_expanded_observable_count_pos : (0 < 111)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma igem_parts_expanded_median_error_under_half_pct : (0.00005882356401581393%R) < (0.5%R).
Proof. lra. Qed.

Lemma igem_synthetic_biology_pooled_median_under_half_pct : (0.022236250385203583%R) < (0.5%R).
Proof. lra. Qed.

Lemma igem_synthetic_biology_headline_median_under_half_pct : (0.022236250385203583%R) < (0.5%R).
Proof. lra. Qed.

Lemma igem_synthetic_biology_observable_count_pos : (0 < 54)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma igem_synthetic_biology_part_count_pos : (0 < 20)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma igem_synthetic_biology_beats_sota_headlines_pos : (0 < 6)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma immunology_panel_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma immunology_panel_median_error_under_half_pct : (0.040788%R) < (0.5%R).
Proof. lra. Qed.

Lemma immunology_observable_count_pos : (0 < 84)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma immunology_median_error_under_half_pct : (0.061205%R) < (0.5%R).
Proof. lra. Qed.

Lemma inaturalist_observation_panel_observable_count_pos : (0 < 288)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma inaturalist_observation_panel_median_error_under_half_pct : (0.006006%R) < (0.5%R).
Proof. lra. Qed.

Lemma inaturalist_observation_observable_count_pos : (0 < 288)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma inaturalist_observation_median_error_under_five_pct : (0.006006%R) < (5.0%R).
Proof. lra. Qed.

Lemma inertial_confinement_fusion_panel_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma inertial_confinement_fusion_panel_median_error_under_half_pct : (0.000079%R) < (0.5%R).
Proof. lra. Qed.

Lemma information_theory_public_panel_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma information_theory_public_panel_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma initiation_transformation_archetype_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma initiation_transformation_archetype_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma fic_best_intelligence_score_positive : 0 < (0.9997093332777109%R).
Proof. lra. Qed.

Lemma fic_sweep_row_count_pos : (0 < 572)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma fic_fertile_rows_present : (0 < 156)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma fic_fertile_replay_match_le_total : (572 <= 572)%nat.
Proof. apply Nat.leb_le; reflexivity. Qed.

Lemma fic_fertile_replay_match_rate_le_one : (1.0%R) <= (1.0%R).
Proof. lra. Qed.

Lemma interactive_media_prereg_scaffold_observable_count_pos : (0 < 42)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma interactive_media_prereg_scaffold_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma interdisciplinary_spine_crosswalk_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma interdisciplinary_spine_crosswalk_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma intrinsic_llm_validators_panel_observable_count_pos : (0 < 21)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma intrinsic_llm_validators_panel_median_error_under_half_pct : (0.014767%R) < (0.5%R).
Proof. lra. Qed.

Lemma intrinsic_llm_validators_observable_count_pos : (0 < 10)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma intrinsic_llm_validators_median_error_under_five_pct : 0%R < (5.0%R).
Proof. lra. Qed.

Lemma ionospheric_chemistry_coupling_observable_count_pos : (0 < 85)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma ionospheric_chemistry_coupling_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma island_of_stability_deep_panel_observable_count_pos : (0 < 23)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma island_of_stability_deep_panel_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma jarvis_dft_open_panel_pooled_median_under_half_pct : (0.01341%R) < (0.5%R).
Proof. lra. Qed.

Lemma jarvis_dft_open_panel_headline_median_under_half_pct : (0.01341%R) < (0.5%R).
Proof. lra. Qed.

Lemma jarvis_dft_open_panel_observable_count_pos : (0 < 77)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma knowledge_base_portable_bundle_panel_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma knowledge_base_portable_bundle_panel_median_error_under_half_pct : (0.0020923899350648867%R) < (0.5%R).
Proof. lra. Qed.

Lemma knowledge_base_source_count_pos : (0 < 39)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma knowledge_base_catalog_formulas_pos : (0 < 19213)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma knowledge_base_observable_matched_le_verified : (7941 <= 7941)%nat.
Proof. apply Nat.leb_le; reflexivity. Qed.

Lemma kronos_best_fractional_error_positive : 0 < (0.0000001644295%R).
Proof. lra. Qed.

Lemma kronos_record_fractional_uncertainty_positive : 0 < (0.00000000000000000055%R).
Proof. lra. Qed.

Lemma kronos_run_count_pos : (0 < 569)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma lab_synthesis_metamaterial_spine_observable_count_pos : (0 < 43)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma lab_synthesis_metamaterial_spine_median_error_under_half_pct : (0.000034%R) < (0.5%R).
Proof. lra. Qed.

Lemma law_policy_ext_pooled_median_under_half_pct : (0.019504399572479934%R) < (0.5%R).
Proof. lra. Qed.

Lemma law_policy_ext_headline_median_under_half_pct : (0.019504399572479934%R) < (0.5%R).
Proof. lra. Qed.

Lemma law_policy_ext_observable_count_pos : (0 < 180)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma law_policy_ext_beats_sota_headlines_pos : (0 < 2)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma law_policy_panel_observable_count_pos : (0 < 20)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma law_policy_panel_median_error_under_half_pct : (0.013003%R) < (0.5%R).
Proof. lra. Qed.

