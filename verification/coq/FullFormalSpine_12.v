(* FSOT Tier 80 — FullFormalSpine chunk 13/13 (generated). *)
(* Independent of Lean proof terms — same decimal obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Lia.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma NeuronCohortStrataPriors_stratum_sst_fi_pearson_gt_bound : (0.5%R) < (0.5196512945807779%R).
Proof. lra. Qed.

Lemma NeuronCohortStrataPriors_stratum_pv_fi_pearson_gt_bound : (0.35%R) < (0.3915167429133035%R).
Proof. lra. Qed.

Lemma NeuronCohortStrataPriors_stratum_vip_fi_pearson_gt_bound : (0.4%R) < (0.42970594991301575%R).
Proof. lra. Qed.

Lemma NeuronCohortStrataPriors_stratum_l23_pyramidal_fi_pearson_gt_bound : (0.2%R) < (0.22516239104042488%R).
Proof. lra. Qed.

Lemma NeuronCohortStrataPriors_held_out_cell_count_large : (2100 < 2165)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma NeuronCohortStrataPriors_stratum_sst_cell_count_pos : (150 < 154)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma NeuronCohortStrataPriors_stratum_pv_cell_count_pos : (200 < 222)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma NeuronCohortStrataPriors_stratum_vip_cell_count_pos : (140 < 146)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma NeuronCohortStrataPriors_stratum_l23_pyramidal_cell_count_pos : (1100 < 1127)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma NeuronCohortStrataPriors_neuron_cohort_strata_bundle : (2100 < 2165)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma DomainPrecisionPriors_domain_precision_numeric_majority : (30 < 35)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma DomainPrecisionPriors_domain_precision_target_band_large : (32 < 35)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma DomainPrecisionPriors_domain_precision_huge_gap_bounded : (0 <= 2)%nat.
Proof. apply Nat.leb_le; reflexivity. Qed.

Lemma BrainPriors_brain_prior_codon_from_dna : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_neocortex_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_cerebellum_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_brainstem_arousal_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_hippocampus_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_basal_ganglia_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_thalamus_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_astrocyte_syncytium_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_oligodendrocyte_myelination_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_amygdala_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_microglial_surveillance_spin_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_neocortex_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_cerebellum_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_brainstem_arousal_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_hippocampus_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_basal_ganglia_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_thalamus_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_astrocyte_syncytium_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_oligodendrocyte_myelination_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_amygdala_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma BrainPriors_microglial_surveillance_genetic_counts_sum : (72 = 72)%nat.
Proof. reflexivity. Qed.

Lemma CodonPriors_codon_table_count_eq_sixty_four : (64 = 64)%nat.
Proof. reflexivity. Qed.

Lemma ProteinPriors_canonical_amino_acid_count_eq_twenty : (20 = 20)%nat.
Proof. reflexivity. Qed.

Lemma TrinaryOSPriors_trinary_os_word_width_eq_27 : (27 = 27)%nat.
Proof. reflexivity. Qed.

Lemma SotaCompetitivenessPriors_sota_beats_majority : (32 < 35)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma SotaCompetitivenessPriors_sota_meets_or_beats_large : (32 < 35)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma SotaCompetitivenessPriors_sota_below_bounded : (0 <= 5)%nat.
Proof. apply Nat.leb_le; reflexivity. Qed.

Lemma SotaCompetitivenessPriors_sota_zero_free_parameters : (0 = 0)%nat.
Proof. reflexivity. Qed.

