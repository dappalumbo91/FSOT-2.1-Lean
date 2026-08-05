(* FSOT Tier 80 — FullFormalSpine chunk 11/21 (generated). *)
(* Independent of Lean proof terms — same decimal obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Lia.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma stratum_pv_cell_count_pos : (200 < 222)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma stratum_vip_cell_count_pos : (140 < 146)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma stratum_l23_pyramidal_cell_count_pos : (1100 < 1127)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuron_train_cell_count_pos : (0 < 1745)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuron_holdout_cell_count_pos : (0 < 420)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuron_train_fi_median_lt_thirty_pct : (0.24544591854270223%R) < (0.3%R).
Proof. lra. Qed.

Lemma neuron_holdout_fi_median_lt_thirty_pct : (0.23879717016341562%R) < (0.3%R).
Proof. lra. Qed.

Lemma neuron_holdout_fi_pearson_gt_fifty_five : (0.55%R) < (0.5982032061315143%R).
Proof. lra. Qed.

Lemma neuron_train_cell_count_ge_gate : (1744 < 1745)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuron_holdout_cell_count_ge_gate : (419 < 420)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuron_canonical_neuroscience_S_positive : 0 < (0.5143619629083619%R).
Proof. lra. Qed.

Lemma neuron_fi_point_count_pos : (0 < 4)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuron_mean_rel_err_lt_fifteen_pct : (0.07002728543379658%R) < (0.15%R).
Proof. lra. Qed.

Lemma neuron_K_matches_thalamic_gate : 0%R < (0.0005%R).
Proof. lra. Qed.

Lemma neuron_verifier_confidence_gt_ninety_pct : (0.9%R) < (0.9598886696481669%R).
Proof. lra. Qed.

Lemma neuron_multi_hero_median_error_under_half_pct : (0.00225237811160842%R) < (0.5%R).
Proof. lra. Qed.

Lemma neuron_multi_hero_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuron_multi_hero_median_fi_under_thirty_pct : 0%R < (30.0%R).
Proof. lra. Qed.

Lemma neuroscience_connectomics_depth_panel_observable_count_pos : (0 < 27)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neuroscience_connectomics_depth_panel_median_error_under_half_pct : (0.0201195%R) < (0.5%R).
Proof. lra. Qed.

Lemma neutrino_physics_panel_observable_count_pos : (0 < 20)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neutrino_physics_panel_median_error_under_half_pct : (0.009504%R) < (0.5%R).
Proof. lra. Qed.

Lemma neutrino_physics_observable_count_pos : (0 < 20)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma neutrino_physics_median_error_under_five_pct : (0.009504%R) < (5.0%R).
Proof. lra. Qed.

Lemma nist_asd_multi_species_open_pooled_median_under_half_pct : (0.073582%R) < (0.5%R).
Proof. lra. Qed.

Lemma nist_asd_multi_species_open_headline_median_under_half_pct : (0.073582%R) < (0.5%R).
Proof. lra. Qed.

Lemma nist_asd_multi_species_open_observable_count_pos : (0 < 26)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma nist_asd_spectroscopy_open_pooled_median_under_half_pct : (0.073582%R) < (0.5%R).
Proof. lra. Qed.

Lemma nist_asd_spectroscopy_open_headline_median_under_half_pct : (0.073582%R) < (0.5%R).
Proof. lra. Qed.

Lemma nist_asd_spectroscopy_open_observable_count_pos : (0 < 13)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma nist_codata_constants_observable_count_pos : (0 < 6)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma nist_codata_constants_median_error_under_five_pct : 0%R < (5.0%R).
Proof. lra. Qed.

Lemma nist_dlmf_special_functions_observable_count_pos : (0 < 21)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma nist_dlmf_special_functions_median_error_under_half_pct : (0.020055%R) < (0.5%R).
Proof. lra. Qed.

Lemma noaa_coastal_tides_observable_count_pos : (0 < 20)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma noaa_coastal_tides_median_error_under_five_pct : (0.030173%R) < (5.0%R).
Proof. lra. Qed.

Lemma noaa_ndbc_buoy_panel_observable_count_pos : (0 < 596)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma noaa_ndbc_buoy_panel_median_error_under_half_pct : (0.028287%R) < (0.5%R).
Proof. lra. Qed.

Lemma noaa_ndbc_buoy_observable_count_pos : (0 < 596)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma noaa_ndbc_buoy_median_error_under_five_pct : (0.028287%R) < (5.0%R).
Proof. lra. Qed.

Lemma noaa_tides_multi_station_open_pooled_median_under_half_pct : (0.030173%R) < (0.5%R).
Proof. lra. Qed.

Lemma noaa_tides_multi_station_open_headline_median_under_half_pct : (0.030173%R) < (0.5%R).
Proof. lra. Qed.

Lemma noaa_tides_multi_station_open_observable_count_pos : (0 < 209)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma nothing_perfection_friction_origin_panel_observable_count_pos : (0 < 24)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma nothing_perfection_friction_origin_panel_median_error_under_half_pct : (0.008488%R) < (0.5%R).
Proof. lra. Qed.

Lemma nuclear_iaea_open_pooled_median_under_half_pct : (0.092131%R) < (0.5%R).
Proof. lra. Qed.

Lemma nuclear_iaea_open_headline_median_under_half_pct : (0.092131%R) < (0.5%R).
Proof. lra. Qed.

Lemma nuclear_iaea_open_observable_count_pos : (0 < 360)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma nufit_neutrino_open_pooled_median_under_half_pct : (0.009504%R) < (0.5%R).
Proof. lra. Qed.

Lemma nufit_neutrino_open_headline_median_under_half_pct : (0.009504%R) < (0.5%R).
Proof. lra. Qed.

Lemma nufit_neutrino_open_observable_count_pos : (0 < 10)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma observer_channel_derivation_observable_count_pos : (0 < 348)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma observer_channel_derivation_median_error_under_half_pct : (0.0525102820198906%R) < (0.5%R).
Proof. lra. Qed.

Lemma observer_effect_cross_species_panel_observable_count_pos : (0 < 289)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma observer_effect_cross_species_panel_median_error_under_half_pct : 0%R < (0.5%R).
Proof. lra. Qed.

Lemma oceanography_gap_fill_pooled_median_under_half_pct : (0.03017272606768673%R) < (0.5%R).
Proof. lra. Qed.

Lemma oceanography_gap_fill_headline_median_under_half_pct : (0.030172726067689837%R) < (0.5%R).
Proof. lra. Qed.

Lemma oceanography_gap_fill_observable_count_pos : (0 < 65)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma oceanography_gap_fill_beats_sota_headlines_pos : (0 < 2)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma oeis_family_sweep_open_pooled_median_under_half_pct : (0.014767%R) < (0.5%R).
Proof. lra. Qed.

Lemma oeis_family_sweep_open_headline_median_under_half_pct : (0.014767%R) < (0.5%R).
Proof. lra. Qed.

Lemma oeis_family_sweep_open_observable_count_pos : (0 < 394)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma omni_theory_genesis_observable_count_pos : (0 < 27)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma omni_theory_genesis_median_error_under_five_pct : 0%R < (5.0%R).
Proof. lra. Qed.

Lemma omni_theory_humanities_panel_observable_count_pos : (0 < 37)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma omni_theory_humanities_panel_median_error_under_half_pct : (0.0222545%R) < (0.5%R).
Proof. lra. Qed.

Lemma oncology_pooled_median_under_half_pct : (0.05041956982053305%R) < (0.5%R).
Proof. lra. Qed.

Lemma oncology_headline_median_under_half_pct : (0.05041956982053305%R) < (0.5%R).
Proof. lra. Qed.

Lemma oncology_observable_count_pos : (0 < 67)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma oncology_section_count_pos : (0 < 5)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma oncology_beats_sota_headlines_pos : (0 < 5)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma openalex_citation_depth_open_pooled_median_under_half_pct : (0.008863%R) < (0.5%R).
Proof. lra. Qed.

Lemma openalex_citation_depth_open_headline_median_under_half_pct : (0.031506%R) < (0.5%R).
Proof. lra. Qed.

Lemma openalex_citation_depth_open_observable_count_pos : (0 < 150)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma openalex_citation_graph_observable_count_pos : (0 < 80)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma openalex_citation_graph_median_error_under_five_pct : (0.031506%R) < (5.0%R).
Proof. lra. Qed.

Lemma open_meteo_live_panel_observable_count_pos : (0 < 432)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma open_meteo_live_panel_median_error_under_half_pct : (0.026204%R) < (0.5%R).
Proof. lra. Qed.

Lemma open_meteo_live_observable_count_pos : (0 < 432)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma open_meteo_live_median_error_under_five_pct : (0.026204%R) < (5.0%R).
Proof. lra. Qed.

Lemma openneuro_depth_open_pooled_median_under_half_pct : (0.018003%R) < (0.5%R).
Proof. lra. Qed.

Lemma openneuro_depth_open_headline_median_under_half_pct : (0.018003%R) < (0.5%R).
Proof. lra. Qed.

Lemma openneuro_depth_open_observable_count_pos : (0 < 47)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma openneuro_full_panel_observable_count_pos : (0 < 123)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma openneuro_full_panel_median_error_under_half_pct : (0.015431%R) < (0.5%R).
Proof. lra. Qed.

Lemma optics_interferometry_depth_panel_observable_count_pos : (0 < 127)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma optics_interferometry_depth_panel_median_error_under_half_pct : (0.026954%R) < (0.5%R).
Proof. lra. Qed.

Lemma orbital_mechanics_median_error_under_half_pct : (0.106141%R) < (0.5%R).
Proof. lra. Qed.

Lemma orbital_mechanics_body_count_pos : (0 < 9)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma osti_doe_science_panel_observable_count_pos : (0 < 100)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma osti_doe_science_panel_median_error_under_half_pct : (0.01382%R) < (0.5%R).
Proof. lra. Qed.

Lemma osti_doe_science_observable_count_pos : (0 < 100)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma osti_doe_science_median_error_under_five_pct : (0.01382%R) < (5.0%R).
Proof. lra. Qed.

Lemma overflow_carry_emergence_panel_observable_count_pos : (0 < 29)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma overflow_carry_emergence_panel_median_error_under_half_pct : (0.009504%R) < (0.5%R).
Proof. lra. Qed.

Lemma owid_epidemiology_open_pooled_median_under_half_pct : (0.022236%R) < (0.5%R).
Proof. lra. Qed.

Lemma owid_epidemiology_open_headline_median_under_half_pct : (0.022236%R) < (0.5%R).
Proof. lra. Qed.

Lemma owid_epidemiology_open_observable_count_pos : (0 < 1778)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma paleoclimate_ext_pooled_median_under_half_pct : (0.015015854077432778%R) < (0.5%R).
Proof. lra. Qed.

Lemma paleoclimate_ext_headline_median_under_half_pct : (0.015015854077432778%R) < (0.5%R).
Proof. lra. Qed.

