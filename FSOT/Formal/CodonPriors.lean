/-
  FSOT Formal CodonPriors — auto-generated 64-codon dual-axis trinary certificates.

  Source: Genetics/64_codon_trinary_map.txt + codon_core + data/lab_registry.json
  Generator: scripts/gen_codon_priors_lean.py

  primary   (spin):     A,G = +1 ; C,T = -1   — matches genomic_trinary.SPIN_MAP
  secondary (genetic):  A = +1 ; T = -1 ; G,C = 0 — matches genomic_trinary.GENETIC_MAP
-/

import FSOT.Formal.Genomic

namespace FSOT.Formal

noncomputable section

open Real

def codon_table_count : ℕ := 64
def distinct_primary_codon_patterns : ℕ := 8
def distinct_secondary_codon_patterns : ℕ := 27
def stop_codon_count_cert : ℕ := 3

theorem codon_table_count_eq_sixty_four :
    codon_table_count = 64 := by
  unfold codon_table_count; norm_num

theorem codon_primary_pattern_space_eq_eight :
    (2 : ℝ) ^ 3 = 8 := by norm_num

theorem codon_secondary_pattern_space_eq_twenty_seven :
    genetic_trinary_alphabet_card ^ 3 = 27 :=
  codon_genetic_pattern_space_eq_twenty_seven

theorem codon_genomic_table_link :
    (4 : ℝ) ^ 3 = 64 := by
  exact_mod_cast codon_table_size_eq_sixty_four

theorem stop_codon_fraction_cert :
    (3 : ℝ) / 64 = 0.046875 := by
  exact stop_codons_fraction_eq

/-- `AAA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_aaa_primary_0 : ℤ := 1
def codon_aaa_primary_1 : ℤ := 1
def codon_aaa_primary_2 : ℤ := 1
theorem codon_aaa_primary_phase :
    (codon_aaa_primary_0, codon_aaa_primary_1, codon_aaa_primary_2) = (1, 1, 1) := by
  unfold codon_aaa_primary_0 codon_aaa_primary_1 codon_aaa_primary_2; norm_num
/-- `AAA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_aaa_secondary_0 : ℤ := 1
def codon_aaa_secondary_1 : ℤ := 1
def codon_aaa_secondary_2 : ℤ := 1
theorem codon_aaa_secondary_phase :
    (codon_aaa_secondary_0, codon_aaa_secondary_1, codon_aaa_secondary_2) = (1, 1, 1) := by
  unfold codon_aaa_secondary_0 codon_aaa_secondary_1 codon_aaa_secondary_2; norm_num

/-- `AAC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_aac_primary_0 : ℤ := 1
def codon_aac_primary_1 : ℤ := 1
def codon_aac_primary_2 : ℤ := -1
theorem codon_aac_primary_phase :
    (codon_aac_primary_0, codon_aac_primary_1, codon_aac_primary_2) = (1, 1, -1) := by
  unfold codon_aac_primary_0 codon_aac_primary_1 codon_aac_primary_2; norm_num
/-- `AAC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_aac_secondary_0 : ℤ := 1
def codon_aac_secondary_1 : ℤ := 1
def codon_aac_secondary_2 : ℤ := 0
theorem codon_aac_secondary_phase :
    (codon_aac_secondary_0, codon_aac_secondary_1, codon_aac_secondary_2) = (1, 1, 0) := by
  unfold codon_aac_secondary_0 codon_aac_secondary_1 codon_aac_secondary_2; norm_num

/-- `AAG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_aag_primary_0 : ℤ := 1
def codon_aag_primary_1 : ℤ := 1
def codon_aag_primary_2 : ℤ := 1
theorem codon_aag_primary_phase :
    (codon_aag_primary_0, codon_aag_primary_1, codon_aag_primary_2) = (1, 1, 1) := by
  unfold codon_aag_primary_0 codon_aag_primary_1 codon_aag_primary_2; norm_num
/-- `AAG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_aag_secondary_0 : ℤ := 1
def codon_aag_secondary_1 : ℤ := 1
def codon_aag_secondary_2 : ℤ := 0
theorem codon_aag_secondary_phase :
    (codon_aag_secondary_0, codon_aag_secondary_1, codon_aag_secondary_2) = (1, 1, 0) := by
  unfold codon_aag_secondary_0 codon_aag_secondary_1 codon_aag_secondary_2; norm_num

/-- `AAT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_aat_primary_0 : ℤ := 1
def codon_aat_primary_1 : ℤ := 1
def codon_aat_primary_2 : ℤ := -1
theorem codon_aat_primary_phase :
    (codon_aat_primary_0, codon_aat_primary_1, codon_aat_primary_2) = (1, 1, -1) := by
  unfold codon_aat_primary_0 codon_aat_primary_1 codon_aat_primary_2; norm_num
/-- `AAT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_aat_secondary_0 : ℤ := 1
def codon_aat_secondary_1 : ℤ := 1
def codon_aat_secondary_2 : ℤ := -1
theorem codon_aat_secondary_phase :
    (codon_aat_secondary_0, codon_aat_secondary_1, codon_aat_secondary_2) = (1, 1, -1) := by
  unfold codon_aat_secondary_0 codon_aat_secondary_1 codon_aat_secondary_2; norm_num

/-- `ACA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_aca_primary_0 : ℤ := 1
def codon_aca_primary_1 : ℤ := -1
def codon_aca_primary_2 : ℤ := 1
theorem codon_aca_primary_phase :
    (codon_aca_primary_0, codon_aca_primary_1, codon_aca_primary_2) = (1, -1, 1) := by
  unfold codon_aca_primary_0 codon_aca_primary_1 codon_aca_primary_2; norm_num
/-- `ACA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_aca_secondary_0 : ℤ := 1
def codon_aca_secondary_1 : ℤ := 0
def codon_aca_secondary_2 : ℤ := 1
theorem codon_aca_secondary_phase :
    (codon_aca_secondary_0, codon_aca_secondary_1, codon_aca_secondary_2) = (1, 0, 1) := by
  unfold codon_aca_secondary_0 codon_aca_secondary_1 codon_aca_secondary_2; norm_num

/-- `ACC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_acc_primary_0 : ℤ := 1
def codon_acc_primary_1 : ℤ := -1
def codon_acc_primary_2 : ℤ := -1
theorem codon_acc_primary_phase :
    (codon_acc_primary_0, codon_acc_primary_1, codon_acc_primary_2) = (1, -1, -1) := by
  unfold codon_acc_primary_0 codon_acc_primary_1 codon_acc_primary_2; norm_num
/-- `ACC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_acc_secondary_0 : ℤ := 1
def codon_acc_secondary_1 : ℤ := 0
def codon_acc_secondary_2 : ℤ := 0
theorem codon_acc_secondary_phase :
    (codon_acc_secondary_0, codon_acc_secondary_1, codon_acc_secondary_2) = (1, 0, 0) := by
  unfold codon_acc_secondary_0 codon_acc_secondary_1 codon_acc_secondary_2; norm_num

/-- `ACG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_acg_primary_0 : ℤ := 1
def codon_acg_primary_1 : ℤ := -1
def codon_acg_primary_2 : ℤ := 1
theorem codon_acg_primary_phase :
    (codon_acg_primary_0, codon_acg_primary_1, codon_acg_primary_2) = (1, -1, 1) := by
  unfold codon_acg_primary_0 codon_acg_primary_1 codon_acg_primary_2; norm_num
/-- `ACG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_acg_secondary_0 : ℤ := 1
def codon_acg_secondary_1 : ℤ := 0
def codon_acg_secondary_2 : ℤ := 0
theorem codon_acg_secondary_phase :
    (codon_acg_secondary_0, codon_acg_secondary_1, codon_acg_secondary_2) = (1, 0, 0) := by
  unfold codon_acg_secondary_0 codon_acg_secondary_1 codon_acg_secondary_2; norm_num

/-- `ACT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_act_primary_0 : ℤ := 1
def codon_act_primary_1 : ℤ := -1
def codon_act_primary_2 : ℤ := -1
theorem codon_act_primary_phase :
    (codon_act_primary_0, codon_act_primary_1, codon_act_primary_2) = (1, -1, -1) := by
  unfold codon_act_primary_0 codon_act_primary_1 codon_act_primary_2; norm_num
/-- `ACT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_act_secondary_0 : ℤ := 1
def codon_act_secondary_1 : ℤ := 0
def codon_act_secondary_2 : ℤ := -1
theorem codon_act_secondary_phase :
    (codon_act_secondary_0, codon_act_secondary_1, codon_act_secondary_2) = (1, 0, -1) := by
  unfold codon_act_secondary_0 codon_act_secondary_1 codon_act_secondary_2; norm_num

/-- `AGA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_aga_primary_0 : ℤ := 1
def codon_aga_primary_1 : ℤ := 1
def codon_aga_primary_2 : ℤ := 1
theorem codon_aga_primary_phase :
    (codon_aga_primary_0, codon_aga_primary_1, codon_aga_primary_2) = (1, 1, 1) := by
  unfold codon_aga_primary_0 codon_aga_primary_1 codon_aga_primary_2; norm_num
/-- `AGA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_aga_secondary_0 : ℤ := 1
def codon_aga_secondary_1 : ℤ := 0
def codon_aga_secondary_2 : ℤ := 1
theorem codon_aga_secondary_phase :
    (codon_aga_secondary_0, codon_aga_secondary_1, codon_aga_secondary_2) = (1, 0, 1) := by
  unfold codon_aga_secondary_0 codon_aga_secondary_1 codon_aga_secondary_2; norm_num

/-- `AGC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_agc_primary_0 : ℤ := 1
def codon_agc_primary_1 : ℤ := 1
def codon_agc_primary_2 : ℤ := -1
theorem codon_agc_primary_phase :
    (codon_agc_primary_0, codon_agc_primary_1, codon_agc_primary_2) = (1, 1, -1) := by
  unfold codon_agc_primary_0 codon_agc_primary_1 codon_agc_primary_2; norm_num
/-- `AGC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_agc_secondary_0 : ℤ := 1
def codon_agc_secondary_1 : ℤ := 0
def codon_agc_secondary_2 : ℤ := 0
theorem codon_agc_secondary_phase :
    (codon_agc_secondary_0, codon_agc_secondary_1, codon_agc_secondary_2) = (1, 0, 0) := by
  unfold codon_agc_secondary_0 codon_agc_secondary_1 codon_agc_secondary_2; norm_num

/-- `AGG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_agg_primary_0 : ℤ := 1
def codon_agg_primary_1 : ℤ := 1
def codon_agg_primary_2 : ℤ := 1
theorem codon_agg_primary_phase :
    (codon_agg_primary_0, codon_agg_primary_1, codon_agg_primary_2) = (1, 1, 1) := by
  unfold codon_agg_primary_0 codon_agg_primary_1 codon_agg_primary_2; norm_num
/-- `AGG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_agg_secondary_0 : ℤ := 1
def codon_agg_secondary_1 : ℤ := 0
def codon_agg_secondary_2 : ℤ := 0
theorem codon_agg_secondary_phase :
    (codon_agg_secondary_0, codon_agg_secondary_1, codon_agg_secondary_2) = (1, 0, 0) := by
  unfold codon_agg_secondary_0 codon_agg_secondary_1 codon_agg_secondary_2; norm_num

/-- `AGT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_agt_primary_0 : ℤ := 1
def codon_agt_primary_1 : ℤ := 1
def codon_agt_primary_2 : ℤ := -1
theorem codon_agt_primary_phase :
    (codon_agt_primary_0, codon_agt_primary_1, codon_agt_primary_2) = (1, 1, -1) := by
  unfold codon_agt_primary_0 codon_agt_primary_1 codon_agt_primary_2; norm_num
/-- `AGT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_agt_secondary_0 : ℤ := 1
def codon_agt_secondary_1 : ℤ := 0
def codon_agt_secondary_2 : ℤ := -1
theorem codon_agt_secondary_phase :
    (codon_agt_secondary_0, codon_agt_secondary_1, codon_agt_secondary_2) = (1, 0, -1) := by
  unfold codon_agt_secondary_0 codon_agt_secondary_1 codon_agt_secondary_2; norm_num

/-- `ATA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ata_primary_0 : ℤ := 1
def codon_ata_primary_1 : ℤ := -1
def codon_ata_primary_2 : ℤ := 1
theorem codon_ata_primary_phase :
    (codon_ata_primary_0, codon_ata_primary_1, codon_ata_primary_2) = (1, -1, 1) := by
  unfold codon_ata_primary_0 codon_ata_primary_1 codon_ata_primary_2; norm_num
/-- `ATA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ata_secondary_0 : ℤ := 1
def codon_ata_secondary_1 : ℤ := -1
def codon_ata_secondary_2 : ℤ := 1
theorem codon_ata_secondary_phase :
    (codon_ata_secondary_0, codon_ata_secondary_1, codon_ata_secondary_2) = (1, -1, 1) := by
  unfold codon_ata_secondary_0 codon_ata_secondary_1 codon_ata_secondary_2; norm_num

/-- `ATC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_atc_primary_0 : ℤ := 1
def codon_atc_primary_1 : ℤ := -1
def codon_atc_primary_2 : ℤ := -1
theorem codon_atc_primary_phase :
    (codon_atc_primary_0, codon_atc_primary_1, codon_atc_primary_2) = (1, -1, -1) := by
  unfold codon_atc_primary_0 codon_atc_primary_1 codon_atc_primary_2; norm_num
/-- `ATC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_atc_secondary_0 : ℤ := 1
def codon_atc_secondary_1 : ℤ := -1
def codon_atc_secondary_2 : ℤ := 0
theorem codon_atc_secondary_phase :
    (codon_atc_secondary_0, codon_atc_secondary_1, codon_atc_secondary_2) = (1, -1, 0) := by
  unfold codon_atc_secondary_0 codon_atc_secondary_1 codon_atc_secondary_2; norm_num

/-- `ATG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_atg_primary_0 : ℤ := 1
def codon_atg_primary_1 : ℤ := -1
def codon_atg_primary_2 : ℤ := 1
theorem codon_atg_primary_phase :
    (codon_atg_primary_0, codon_atg_primary_1, codon_atg_primary_2) = (1, -1, 1) := by
  unfold codon_atg_primary_0 codon_atg_primary_1 codon_atg_primary_2; norm_num
/-- `ATG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_atg_secondary_0 : ℤ := 1
def codon_atg_secondary_1 : ℤ := -1
def codon_atg_secondary_2 : ℤ := 0
theorem codon_atg_secondary_phase :
    (codon_atg_secondary_0, codon_atg_secondary_1, codon_atg_secondary_2) = (1, -1, 0) := by
  unfold codon_atg_secondary_0 codon_atg_secondary_1 codon_atg_secondary_2; norm_num

/-- `ATT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_att_primary_0 : ℤ := 1
def codon_att_primary_1 : ℤ := -1
def codon_att_primary_2 : ℤ := -1
theorem codon_att_primary_phase :
    (codon_att_primary_0, codon_att_primary_1, codon_att_primary_2) = (1, -1, -1) := by
  unfold codon_att_primary_0 codon_att_primary_1 codon_att_primary_2; norm_num
/-- `ATT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_att_secondary_0 : ℤ := 1
def codon_att_secondary_1 : ℤ := -1
def codon_att_secondary_2 : ℤ := -1
theorem codon_att_secondary_phase :
    (codon_att_secondary_0, codon_att_secondary_1, codon_att_secondary_2) = (1, -1, -1) := by
  unfold codon_att_secondary_0 codon_att_secondary_1 codon_att_secondary_2; norm_num

/-- `CAA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_caa_primary_0 : ℤ := -1
def codon_caa_primary_1 : ℤ := 1
def codon_caa_primary_2 : ℤ := 1
theorem codon_caa_primary_phase :
    (codon_caa_primary_0, codon_caa_primary_1, codon_caa_primary_2) = (-1, 1, 1) := by
  unfold codon_caa_primary_0 codon_caa_primary_1 codon_caa_primary_2; norm_num
/-- `CAA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_caa_secondary_0 : ℤ := 0
def codon_caa_secondary_1 : ℤ := 1
def codon_caa_secondary_2 : ℤ := 1
theorem codon_caa_secondary_phase :
    (codon_caa_secondary_0, codon_caa_secondary_1, codon_caa_secondary_2) = (0, 1, 1) := by
  unfold codon_caa_secondary_0 codon_caa_secondary_1 codon_caa_secondary_2; norm_num

/-- `CAC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cac_primary_0 : ℤ := -1
def codon_cac_primary_1 : ℤ := 1
def codon_cac_primary_2 : ℤ := -1
theorem codon_cac_primary_phase :
    (codon_cac_primary_0, codon_cac_primary_1, codon_cac_primary_2) = (-1, 1, -1) := by
  unfold codon_cac_primary_0 codon_cac_primary_1 codon_cac_primary_2; norm_num
/-- `CAC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cac_secondary_0 : ℤ := 0
def codon_cac_secondary_1 : ℤ := 1
def codon_cac_secondary_2 : ℤ := 0
theorem codon_cac_secondary_phase :
    (codon_cac_secondary_0, codon_cac_secondary_1, codon_cac_secondary_2) = (0, 1, 0) := by
  unfold codon_cac_secondary_0 codon_cac_secondary_1 codon_cac_secondary_2; norm_num

/-- `CAG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cag_primary_0 : ℤ := -1
def codon_cag_primary_1 : ℤ := 1
def codon_cag_primary_2 : ℤ := 1
theorem codon_cag_primary_phase :
    (codon_cag_primary_0, codon_cag_primary_1, codon_cag_primary_2) = (-1, 1, 1) := by
  unfold codon_cag_primary_0 codon_cag_primary_1 codon_cag_primary_2; norm_num
/-- `CAG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cag_secondary_0 : ℤ := 0
def codon_cag_secondary_1 : ℤ := 1
def codon_cag_secondary_2 : ℤ := 0
theorem codon_cag_secondary_phase :
    (codon_cag_secondary_0, codon_cag_secondary_1, codon_cag_secondary_2) = (0, 1, 0) := by
  unfold codon_cag_secondary_0 codon_cag_secondary_1 codon_cag_secondary_2; norm_num

/-- `CAT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cat_primary_0 : ℤ := -1
def codon_cat_primary_1 : ℤ := 1
def codon_cat_primary_2 : ℤ := -1
theorem codon_cat_primary_phase :
    (codon_cat_primary_0, codon_cat_primary_1, codon_cat_primary_2) = (-1, 1, -1) := by
  unfold codon_cat_primary_0 codon_cat_primary_1 codon_cat_primary_2; norm_num
/-- `CAT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cat_secondary_0 : ℤ := 0
def codon_cat_secondary_1 : ℤ := 1
def codon_cat_secondary_2 : ℤ := -1
theorem codon_cat_secondary_phase :
    (codon_cat_secondary_0, codon_cat_secondary_1, codon_cat_secondary_2) = (0, 1, -1) := by
  unfold codon_cat_secondary_0 codon_cat_secondary_1 codon_cat_secondary_2; norm_num

/-- `CCA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cca_primary_0 : ℤ := -1
def codon_cca_primary_1 : ℤ := -1
def codon_cca_primary_2 : ℤ := 1
theorem codon_cca_primary_phase :
    (codon_cca_primary_0, codon_cca_primary_1, codon_cca_primary_2) = (-1, -1, 1) := by
  unfold codon_cca_primary_0 codon_cca_primary_1 codon_cca_primary_2; norm_num
/-- `CCA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cca_secondary_0 : ℤ := 0
def codon_cca_secondary_1 : ℤ := 0
def codon_cca_secondary_2 : ℤ := 1
theorem codon_cca_secondary_phase :
    (codon_cca_secondary_0, codon_cca_secondary_1, codon_cca_secondary_2) = (0, 0, 1) := by
  unfold codon_cca_secondary_0 codon_cca_secondary_1 codon_cca_secondary_2; norm_num

/-- `CCC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ccc_primary_0 : ℤ := -1
def codon_ccc_primary_1 : ℤ := -1
def codon_ccc_primary_2 : ℤ := -1
theorem codon_ccc_primary_phase :
    (codon_ccc_primary_0, codon_ccc_primary_1, codon_ccc_primary_2) = (-1, -1, -1) := by
  unfold codon_ccc_primary_0 codon_ccc_primary_1 codon_ccc_primary_2; norm_num
/-- `CCC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ccc_secondary_0 : ℤ := 0
def codon_ccc_secondary_1 : ℤ := 0
def codon_ccc_secondary_2 : ℤ := 0
theorem codon_ccc_secondary_phase :
    (codon_ccc_secondary_0, codon_ccc_secondary_1, codon_ccc_secondary_2) = (0, 0, 0) := by
  unfold codon_ccc_secondary_0 codon_ccc_secondary_1 codon_ccc_secondary_2; norm_num

/-- `CCG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ccg_primary_0 : ℤ := -1
def codon_ccg_primary_1 : ℤ := -1
def codon_ccg_primary_2 : ℤ := 1
theorem codon_ccg_primary_phase :
    (codon_ccg_primary_0, codon_ccg_primary_1, codon_ccg_primary_2) = (-1, -1, 1) := by
  unfold codon_ccg_primary_0 codon_ccg_primary_1 codon_ccg_primary_2; norm_num
/-- `CCG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ccg_secondary_0 : ℤ := 0
def codon_ccg_secondary_1 : ℤ := 0
def codon_ccg_secondary_2 : ℤ := 0
theorem codon_ccg_secondary_phase :
    (codon_ccg_secondary_0, codon_ccg_secondary_1, codon_ccg_secondary_2) = (0, 0, 0) := by
  unfold codon_ccg_secondary_0 codon_ccg_secondary_1 codon_ccg_secondary_2; norm_num

/-- `CCT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cct_primary_0 : ℤ := -1
def codon_cct_primary_1 : ℤ := -1
def codon_cct_primary_2 : ℤ := -1
theorem codon_cct_primary_phase :
    (codon_cct_primary_0, codon_cct_primary_1, codon_cct_primary_2) = (-1, -1, -1) := by
  unfold codon_cct_primary_0 codon_cct_primary_1 codon_cct_primary_2; norm_num
/-- `CCT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cct_secondary_0 : ℤ := 0
def codon_cct_secondary_1 : ℤ := 0
def codon_cct_secondary_2 : ℤ := -1
theorem codon_cct_secondary_phase :
    (codon_cct_secondary_0, codon_cct_secondary_1, codon_cct_secondary_2) = (0, 0, -1) := by
  unfold codon_cct_secondary_0 codon_cct_secondary_1 codon_cct_secondary_2; norm_num

/-- `CGA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cga_primary_0 : ℤ := -1
def codon_cga_primary_1 : ℤ := 1
def codon_cga_primary_2 : ℤ := 1
theorem codon_cga_primary_phase :
    (codon_cga_primary_0, codon_cga_primary_1, codon_cga_primary_2) = (-1, 1, 1) := by
  unfold codon_cga_primary_0 codon_cga_primary_1 codon_cga_primary_2; norm_num
/-- `CGA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cga_secondary_0 : ℤ := 0
def codon_cga_secondary_1 : ℤ := 0
def codon_cga_secondary_2 : ℤ := 1
theorem codon_cga_secondary_phase :
    (codon_cga_secondary_0, codon_cga_secondary_1, codon_cga_secondary_2) = (0, 0, 1) := by
  unfold codon_cga_secondary_0 codon_cga_secondary_1 codon_cga_secondary_2; norm_num

/-- `CGC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cgc_primary_0 : ℤ := -1
def codon_cgc_primary_1 : ℤ := 1
def codon_cgc_primary_2 : ℤ := -1
theorem codon_cgc_primary_phase :
    (codon_cgc_primary_0, codon_cgc_primary_1, codon_cgc_primary_2) = (-1, 1, -1) := by
  unfold codon_cgc_primary_0 codon_cgc_primary_1 codon_cgc_primary_2; norm_num
/-- `CGC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cgc_secondary_0 : ℤ := 0
def codon_cgc_secondary_1 : ℤ := 0
def codon_cgc_secondary_2 : ℤ := 0
theorem codon_cgc_secondary_phase :
    (codon_cgc_secondary_0, codon_cgc_secondary_1, codon_cgc_secondary_2) = (0, 0, 0) := by
  unfold codon_cgc_secondary_0 codon_cgc_secondary_1 codon_cgc_secondary_2; norm_num

/-- `CGG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cgg_primary_0 : ℤ := -1
def codon_cgg_primary_1 : ℤ := 1
def codon_cgg_primary_2 : ℤ := 1
theorem codon_cgg_primary_phase :
    (codon_cgg_primary_0, codon_cgg_primary_1, codon_cgg_primary_2) = (-1, 1, 1) := by
  unfold codon_cgg_primary_0 codon_cgg_primary_1 codon_cgg_primary_2; norm_num
/-- `CGG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cgg_secondary_0 : ℤ := 0
def codon_cgg_secondary_1 : ℤ := 0
def codon_cgg_secondary_2 : ℤ := 0
theorem codon_cgg_secondary_phase :
    (codon_cgg_secondary_0, codon_cgg_secondary_1, codon_cgg_secondary_2) = (0, 0, 0) := by
  unfold codon_cgg_secondary_0 codon_cgg_secondary_1 codon_cgg_secondary_2; norm_num

/-- `CGT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cgt_primary_0 : ℤ := -1
def codon_cgt_primary_1 : ℤ := 1
def codon_cgt_primary_2 : ℤ := -1
theorem codon_cgt_primary_phase :
    (codon_cgt_primary_0, codon_cgt_primary_1, codon_cgt_primary_2) = (-1, 1, -1) := by
  unfold codon_cgt_primary_0 codon_cgt_primary_1 codon_cgt_primary_2; norm_num
/-- `CGT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cgt_secondary_0 : ℤ := 0
def codon_cgt_secondary_1 : ℤ := 0
def codon_cgt_secondary_2 : ℤ := -1
theorem codon_cgt_secondary_phase :
    (codon_cgt_secondary_0, codon_cgt_secondary_1, codon_cgt_secondary_2) = (0, 0, -1) := by
  unfold codon_cgt_secondary_0 codon_cgt_secondary_1 codon_cgt_secondary_2; norm_num

/-- `CTA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_cta_primary_0 : ℤ := -1
def codon_cta_primary_1 : ℤ := -1
def codon_cta_primary_2 : ℤ := 1
theorem codon_cta_primary_phase :
    (codon_cta_primary_0, codon_cta_primary_1, codon_cta_primary_2) = (-1, -1, 1) := by
  unfold codon_cta_primary_0 codon_cta_primary_1 codon_cta_primary_2; norm_num
/-- `CTA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_cta_secondary_0 : ℤ := 0
def codon_cta_secondary_1 : ℤ := -1
def codon_cta_secondary_2 : ℤ := 1
theorem codon_cta_secondary_phase :
    (codon_cta_secondary_0, codon_cta_secondary_1, codon_cta_secondary_2) = (0, -1, 1) := by
  unfold codon_cta_secondary_0 codon_cta_secondary_1 codon_cta_secondary_2; norm_num

/-- `CTC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ctc_primary_0 : ℤ := -1
def codon_ctc_primary_1 : ℤ := -1
def codon_ctc_primary_2 : ℤ := -1
theorem codon_ctc_primary_phase :
    (codon_ctc_primary_0, codon_ctc_primary_1, codon_ctc_primary_2) = (-1, -1, -1) := by
  unfold codon_ctc_primary_0 codon_ctc_primary_1 codon_ctc_primary_2; norm_num
/-- `CTC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ctc_secondary_0 : ℤ := 0
def codon_ctc_secondary_1 : ℤ := -1
def codon_ctc_secondary_2 : ℤ := 0
theorem codon_ctc_secondary_phase :
    (codon_ctc_secondary_0, codon_ctc_secondary_1, codon_ctc_secondary_2) = (0, -1, 0) := by
  unfold codon_ctc_secondary_0 codon_ctc_secondary_1 codon_ctc_secondary_2; norm_num

/-- `CTG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ctg_primary_0 : ℤ := -1
def codon_ctg_primary_1 : ℤ := -1
def codon_ctg_primary_2 : ℤ := 1
theorem codon_ctg_primary_phase :
    (codon_ctg_primary_0, codon_ctg_primary_1, codon_ctg_primary_2) = (-1, -1, 1) := by
  unfold codon_ctg_primary_0 codon_ctg_primary_1 codon_ctg_primary_2; norm_num
/-- `CTG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ctg_secondary_0 : ℤ := 0
def codon_ctg_secondary_1 : ℤ := -1
def codon_ctg_secondary_2 : ℤ := 0
theorem codon_ctg_secondary_phase :
    (codon_ctg_secondary_0, codon_ctg_secondary_1, codon_ctg_secondary_2) = (0, -1, 0) := by
  unfold codon_ctg_secondary_0 codon_ctg_secondary_1 codon_ctg_secondary_2; norm_num

/-- `CTT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ctt_primary_0 : ℤ := -1
def codon_ctt_primary_1 : ℤ := -1
def codon_ctt_primary_2 : ℤ := -1
theorem codon_ctt_primary_phase :
    (codon_ctt_primary_0, codon_ctt_primary_1, codon_ctt_primary_2) = (-1, -1, -1) := by
  unfold codon_ctt_primary_0 codon_ctt_primary_1 codon_ctt_primary_2; norm_num
/-- `CTT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ctt_secondary_0 : ℤ := 0
def codon_ctt_secondary_1 : ℤ := -1
def codon_ctt_secondary_2 : ℤ := -1
theorem codon_ctt_secondary_phase :
    (codon_ctt_secondary_0, codon_ctt_secondary_1, codon_ctt_secondary_2) = (0, -1, -1) := by
  unfold codon_ctt_secondary_0 codon_ctt_secondary_1 codon_ctt_secondary_2; norm_num

/-- `GAA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gaa_primary_0 : ℤ := 1
def codon_gaa_primary_1 : ℤ := 1
def codon_gaa_primary_2 : ℤ := 1
theorem codon_gaa_primary_phase :
    (codon_gaa_primary_0, codon_gaa_primary_1, codon_gaa_primary_2) = (1, 1, 1) := by
  unfold codon_gaa_primary_0 codon_gaa_primary_1 codon_gaa_primary_2; norm_num
/-- `GAA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gaa_secondary_0 : ℤ := 0
def codon_gaa_secondary_1 : ℤ := 1
def codon_gaa_secondary_2 : ℤ := 1
theorem codon_gaa_secondary_phase :
    (codon_gaa_secondary_0, codon_gaa_secondary_1, codon_gaa_secondary_2) = (0, 1, 1) := by
  unfold codon_gaa_secondary_0 codon_gaa_secondary_1 codon_gaa_secondary_2; norm_num

/-- `GAC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gac_primary_0 : ℤ := 1
def codon_gac_primary_1 : ℤ := 1
def codon_gac_primary_2 : ℤ := -1
theorem codon_gac_primary_phase :
    (codon_gac_primary_0, codon_gac_primary_1, codon_gac_primary_2) = (1, 1, -1) := by
  unfold codon_gac_primary_0 codon_gac_primary_1 codon_gac_primary_2; norm_num
/-- `GAC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gac_secondary_0 : ℤ := 0
def codon_gac_secondary_1 : ℤ := 1
def codon_gac_secondary_2 : ℤ := 0
theorem codon_gac_secondary_phase :
    (codon_gac_secondary_0, codon_gac_secondary_1, codon_gac_secondary_2) = (0, 1, 0) := by
  unfold codon_gac_secondary_0 codon_gac_secondary_1 codon_gac_secondary_2; norm_num

/-- `GAG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gag_primary_0 : ℤ := 1
def codon_gag_primary_1 : ℤ := 1
def codon_gag_primary_2 : ℤ := 1
theorem codon_gag_primary_phase :
    (codon_gag_primary_0, codon_gag_primary_1, codon_gag_primary_2) = (1, 1, 1) := by
  unfold codon_gag_primary_0 codon_gag_primary_1 codon_gag_primary_2; norm_num
/-- `GAG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gag_secondary_0 : ℤ := 0
def codon_gag_secondary_1 : ℤ := 1
def codon_gag_secondary_2 : ℤ := 0
theorem codon_gag_secondary_phase :
    (codon_gag_secondary_0, codon_gag_secondary_1, codon_gag_secondary_2) = (0, 1, 0) := by
  unfold codon_gag_secondary_0 codon_gag_secondary_1 codon_gag_secondary_2; norm_num

/-- `GAT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gat_primary_0 : ℤ := 1
def codon_gat_primary_1 : ℤ := 1
def codon_gat_primary_2 : ℤ := -1
theorem codon_gat_primary_phase :
    (codon_gat_primary_0, codon_gat_primary_1, codon_gat_primary_2) = (1, 1, -1) := by
  unfold codon_gat_primary_0 codon_gat_primary_1 codon_gat_primary_2; norm_num
/-- `GAT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gat_secondary_0 : ℤ := 0
def codon_gat_secondary_1 : ℤ := 1
def codon_gat_secondary_2 : ℤ := -1
theorem codon_gat_secondary_phase :
    (codon_gat_secondary_0, codon_gat_secondary_1, codon_gat_secondary_2) = (0, 1, -1) := by
  unfold codon_gat_secondary_0 codon_gat_secondary_1 codon_gat_secondary_2; norm_num

/-- `GCA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gca_primary_0 : ℤ := 1
def codon_gca_primary_1 : ℤ := -1
def codon_gca_primary_2 : ℤ := 1
theorem codon_gca_primary_phase :
    (codon_gca_primary_0, codon_gca_primary_1, codon_gca_primary_2) = (1, -1, 1) := by
  unfold codon_gca_primary_0 codon_gca_primary_1 codon_gca_primary_2; norm_num
/-- `GCA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gca_secondary_0 : ℤ := 0
def codon_gca_secondary_1 : ℤ := 0
def codon_gca_secondary_2 : ℤ := 1
theorem codon_gca_secondary_phase :
    (codon_gca_secondary_0, codon_gca_secondary_1, codon_gca_secondary_2) = (0, 0, 1) := by
  unfold codon_gca_secondary_0 codon_gca_secondary_1 codon_gca_secondary_2; norm_num

/-- `GCC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gcc_primary_0 : ℤ := 1
def codon_gcc_primary_1 : ℤ := -1
def codon_gcc_primary_2 : ℤ := -1
theorem codon_gcc_primary_phase :
    (codon_gcc_primary_0, codon_gcc_primary_1, codon_gcc_primary_2) = (1, -1, -1) := by
  unfold codon_gcc_primary_0 codon_gcc_primary_1 codon_gcc_primary_2; norm_num
/-- `GCC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gcc_secondary_0 : ℤ := 0
def codon_gcc_secondary_1 : ℤ := 0
def codon_gcc_secondary_2 : ℤ := 0
theorem codon_gcc_secondary_phase :
    (codon_gcc_secondary_0, codon_gcc_secondary_1, codon_gcc_secondary_2) = (0, 0, 0) := by
  unfold codon_gcc_secondary_0 codon_gcc_secondary_1 codon_gcc_secondary_2; norm_num

/-- `GCG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gcg_primary_0 : ℤ := 1
def codon_gcg_primary_1 : ℤ := -1
def codon_gcg_primary_2 : ℤ := 1
theorem codon_gcg_primary_phase :
    (codon_gcg_primary_0, codon_gcg_primary_1, codon_gcg_primary_2) = (1, -1, 1) := by
  unfold codon_gcg_primary_0 codon_gcg_primary_1 codon_gcg_primary_2; norm_num
/-- `GCG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gcg_secondary_0 : ℤ := 0
def codon_gcg_secondary_1 : ℤ := 0
def codon_gcg_secondary_2 : ℤ := 0
theorem codon_gcg_secondary_phase :
    (codon_gcg_secondary_0, codon_gcg_secondary_1, codon_gcg_secondary_2) = (0, 0, 0) := by
  unfold codon_gcg_secondary_0 codon_gcg_secondary_1 codon_gcg_secondary_2; norm_num

/-- `GCT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gct_primary_0 : ℤ := 1
def codon_gct_primary_1 : ℤ := -1
def codon_gct_primary_2 : ℤ := -1
theorem codon_gct_primary_phase :
    (codon_gct_primary_0, codon_gct_primary_1, codon_gct_primary_2) = (1, -1, -1) := by
  unfold codon_gct_primary_0 codon_gct_primary_1 codon_gct_primary_2; norm_num
/-- `GCT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gct_secondary_0 : ℤ := 0
def codon_gct_secondary_1 : ℤ := 0
def codon_gct_secondary_2 : ℤ := -1
theorem codon_gct_secondary_phase :
    (codon_gct_secondary_0, codon_gct_secondary_1, codon_gct_secondary_2) = (0, 0, -1) := by
  unfold codon_gct_secondary_0 codon_gct_secondary_1 codon_gct_secondary_2; norm_num

/-- `GGA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gga_primary_0 : ℤ := 1
def codon_gga_primary_1 : ℤ := 1
def codon_gga_primary_2 : ℤ := 1
theorem codon_gga_primary_phase :
    (codon_gga_primary_0, codon_gga_primary_1, codon_gga_primary_2) = (1, 1, 1) := by
  unfold codon_gga_primary_0 codon_gga_primary_1 codon_gga_primary_2; norm_num
/-- `GGA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gga_secondary_0 : ℤ := 0
def codon_gga_secondary_1 : ℤ := 0
def codon_gga_secondary_2 : ℤ := 1
theorem codon_gga_secondary_phase :
    (codon_gga_secondary_0, codon_gga_secondary_1, codon_gga_secondary_2) = (0, 0, 1) := by
  unfold codon_gga_secondary_0 codon_gga_secondary_1 codon_gga_secondary_2; norm_num

/-- `GGC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ggc_primary_0 : ℤ := 1
def codon_ggc_primary_1 : ℤ := 1
def codon_ggc_primary_2 : ℤ := -1
theorem codon_ggc_primary_phase :
    (codon_ggc_primary_0, codon_ggc_primary_1, codon_ggc_primary_2) = (1, 1, -1) := by
  unfold codon_ggc_primary_0 codon_ggc_primary_1 codon_ggc_primary_2; norm_num
/-- `GGC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ggc_secondary_0 : ℤ := 0
def codon_ggc_secondary_1 : ℤ := 0
def codon_ggc_secondary_2 : ℤ := 0
theorem codon_ggc_secondary_phase :
    (codon_ggc_secondary_0, codon_ggc_secondary_1, codon_ggc_secondary_2) = (0, 0, 0) := by
  unfold codon_ggc_secondary_0 codon_ggc_secondary_1 codon_ggc_secondary_2; norm_num

/-- `GGG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ggg_primary_0 : ℤ := 1
def codon_ggg_primary_1 : ℤ := 1
def codon_ggg_primary_2 : ℤ := 1
theorem codon_ggg_primary_phase :
    (codon_ggg_primary_0, codon_ggg_primary_1, codon_ggg_primary_2) = (1, 1, 1) := by
  unfold codon_ggg_primary_0 codon_ggg_primary_1 codon_ggg_primary_2; norm_num
/-- `GGG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ggg_secondary_0 : ℤ := 0
def codon_ggg_secondary_1 : ℤ := 0
def codon_ggg_secondary_2 : ℤ := 0
theorem codon_ggg_secondary_phase :
    (codon_ggg_secondary_0, codon_ggg_secondary_1, codon_ggg_secondary_2) = (0, 0, 0) := by
  unfold codon_ggg_secondary_0 codon_ggg_secondary_1 codon_ggg_secondary_2; norm_num

/-- `GGT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ggt_primary_0 : ℤ := 1
def codon_ggt_primary_1 : ℤ := 1
def codon_ggt_primary_2 : ℤ := -1
theorem codon_ggt_primary_phase :
    (codon_ggt_primary_0, codon_ggt_primary_1, codon_ggt_primary_2) = (1, 1, -1) := by
  unfold codon_ggt_primary_0 codon_ggt_primary_1 codon_ggt_primary_2; norm_num
/-- `GGT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ggt_secondary_0 : ℤ := 0
def codon_ggt_secondary_1 : ℤ := 0
def codon_ggt_secondary_2 : ℤ := -1
theorem codon_ggt_secondary_phase :
    (codon_ggt_secondary_0, codon_ggt_secondary_1, codon_ggt_secondary_2) = (0, 0, -1) := by
  unfold codon_ggt_secondary_0 codon_ggt_secondary_1 codon_ggt_secondary_2; norm_num

/-- `GTA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gta_primary_0 : ℤ := 1
def codon_gta_primary_1 : ℤ := -1
def codon_gta_primary_2 : ℤ := 1
theorem codon_gta_primary_phase :
    (codon_gta_primary_0, codon_gta_primary_1, codon_gta_primary_2) = (1, -1, 1) := by
  unfold codon_gta_primary_0 codon_gta_primary_1 codon_gta_primary_2; norm_num
/-- `GTA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gta_secondary_0 : ℤ := 0
def codon_gta_secondary_1 : ℤ := -1
def codon_gta_secondary_2 : ℤ := 1
theorem codon_gta_secondary_phase :
    (codon_gta_secondary_0, codon_gta_secondary_1, codon_gta_secondary_2) = (0, -1, 1) := by
  unfold codon_gta_secondary_0 codon_gta_secondary_1 codon_gta_secondary_2; norm_num

/-- `GTC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gtc_primary_0 : ℤ := 1
def codon_gtc_primary_1 : ℤ := -1
def codon_gtc_primary_2 : ℤ := -1
theorem codon_gtc_primary_phase :
    (codon_gtc_primary_0, codon_gtc_primary_1, codon_gtc_primary_2) = (1, -1, -1) := by
  unfold codon_gtc_primary_0 codon_gtc_primary_1 codon_gtc_primary_2; norm_num
/-- `GTC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gtc_secondary_0 : ℤ := 0
def codon_gtc_secondary_1 : ℤ := -1
def codon_gtc_secondary_2 : ℤ := 0
theorem codon_gtc_secondary_phase :
    (codon_gtc_secondary_0, codon_gtc_secondary_1, codon_gtc_secondary_2) = (0, -1, 0) := by
  unfold codon_gtc_secondary_0 codon_gtc_secondary_1 codon_gtc_secondary_2; norm_num

/-- `GTG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gtg_primary_0 : ℤ := 1
def codon_gtg_primary_1 : ℤ := -1
def codon_gtg_primary_2 : ℤ := 1
theorem codon_gtg_primary_phase :
    (codon_gtg_primary_0, codon_gtg_primary_1, codon_gtg_primary_2) = (1, -1, 1) := by
  unfold codon_gtg_primary_0 codon_gtg_primary_1 codon_gtg_primary_2; norm_num
/-- `GTG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gtg_secondary_0 : ℤ := 0
def codon_gtg_secondary_1 : ℤ := -1
def codon_gtg_secondary_2 : ℤ := 0
theorem codon_gtg_secondary_phase :
    (codon_gtg_secondary_0, codon_gtg_secondary_1, codon_gtg_secondary_2) = (0, -1, 0) := by
  unfold codon_gtg_secondary_0 codon_gtg_secondary_1 codon_gtg_secondary_2; norm_num

/-- `GTT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_gtt_primary_0 : ℤ := 1
def codon_gtt_primary_1 : ℤ := -1
def codon_gtt_primary_2 : ℤ := -1
theorem codon_gtt_primary_phase :
    (codon_gtt_primary_0, codon_gtt_primary_1, codon_gtt_primary_2) = (1, -1, -1) := by
  unfold codon_gtt_primary_0 codon_gtt_primary_1 codon_gtt_primary_2; norm_num
/-- `GTT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_gtt_secondary_0 : ℤ := 0
def codon_gtt_secondary_1 : ℤ := -1
def codon_gtt_secondary_2 : ℤ := -1
theorem codon_gtt_secondary_phase :
    (codon_gtt_secondary_0, codon_gtt_secondary_1, codon_gtt_secondary_2) = (0, -1, -1) := by
  unfold codon_gtt_secondary_0 codon_gtt_secondary_1 codon_gtt_secondary_2; norm_num

/-- `TAA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_taa_primary_0 : ℤ := -1
def codon_taa_primary_1 : ℤ := 1
def codon_taa_primary_2 : ℤ := 1
theorem codon_taa_primary_phase :
    (codon_taa_primary_0, codon_taa_primary_1, codon_taa_primary_2) = (-1, 1, 1) := by
  unfold codon_taa_primary_0 codon_taa_primary_1 codon_taa_primary_2; norm_num
/-- `TAA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_taa_secondary_0 : ℤ := -1
def codon_taa_secondary_1 : ℤ := 1
def codon_taa_secondary_2 : ℤ := 1
theorem codon_taa_secondary_phase :
    (codon_taa_secondary_0, codon_taa_secondary_1, codon_taa_secondary_2) = (-1, 1, 1) := by
  unfold codon_taa_secondary_0 codon_taa_secondary_1 codon_taa_secondary_2; norm_num

/-- `TAC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tac_primary_0 : ℤ := -1
def codon_tac_primary_1 : ℤ := 1
def codon_tac_primary_2 : ℤ := -1
theorem codon_tac_primary_phase :
    (codon_tac_primary_0, codon_tac_primary_1, codon_tac_primary_2) = (-1, 1, -1) := by
  unfold codon_tac_primary_0 codon_tac_primary_1 codon_tac_primary_2; norm_num
/-- `TAC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tac_secondary_0 : ℤ := -1
def codon_tac_secondary_1 : ℤ := 1
def codon_tac_secondary_2 : ℤ := 0
theorem codon_tac_secondary_phase :
    (codon_tac_secondary_0, codon_tac_secondary_1, codon_tac_secondary_2) = (-1, 1, 0) := by
  unfold codon_tac_secondary_0 codon_tac_secondary_1 codon_tac_secondary_2; norm_num

/-- `TAG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tag_primary_0 : ℤ := -1
def codon_tag_primary_1 : ℤ := 1
def codon_tag_primary_2 : ℤ := 1
theorem codon_tag_primary_phase :
    (codon_tag_primary_0, codon_tag_primary_1, codon_tag_primary_2) = (-1, 1, 1) := by
  unfold codon_tag_primary_0 codon_tag_primary_1 codon_tag_primary_2; norm_num
/-- `TAG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tag_secondary_0 : ℤ := -1
def codon_tag_secondary_1 : ℤ := 1
def codon_tag_secondary_2 : ℤ := 0
theorem codon_tag_secondary_phase :
    (codon_tag_secondary_0, codon_tag_secondary_1, codon_tag_secondary_2) = (-1, 1, 0) := by
  unfold codon_tag_secondary_0 codon_tag_secondary_1 codon_tag_secondary_2; norm_num

/-- `TAT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tat_primary_0 : ℤ := -1
def codon_tat_primary_1 : ℤ := 1
def codon_tat_primary_2 : ℤ := -1
theorem codon_tat_primary_phase :
    (codon_tat_primary_0, codon_tat_primary_1, codon_tat_primary_2) = (-1, 1, -1) := by
  unfold codon_tat_primary_0 codon_tat_primary_1 codon_tat_primary_2; norm_num
/-- `TAT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tat_secondary_0 : ℤ := -1
def codon_tat_secondary_1 : ℤ := 1
def codon_tat_secondary_2 : ℤ := -1
theorem codon_tat_secondary_phase :
    (codon_tat_secondary_0, codon_tat_secondary_1, codon_tat_secondary_2) = (-1, 1, -1) := by
  unfold codon_tat_secondary_0 codon_tat_secondary_1 codon_tat_secondary_2; norm_num

/-- `TCA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tca_primary_0 : ℤ := -1
def codon_tca_primary_1 : ℤ := -1
def codon_tca_primary_2 : ℤ := 1
theorem codon_tca_primary_phase :
    (codon_tca_primary_0, codon_tca_primary_1, codon_tca_primary_2) = (-1, -1, 1) := by
  unfold codon_tca_primary_0 codon_tca_primary_1 codon_tca_primary_2; norm_num
/-- `TCA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tca_secondary_0 : ℤ := -1
def codon_tca_secondary_1 : ℤ := 0
def codon_tca_secondary_2 : ℤ := 1
theorem codon_tca_secondary_phase :
    (codon_tca_secondary_0, codon_tca_secondary_1, codon_tca_secondary_2) = (-1, 0, 1) := by
  unfold codon_tca_secondary_0 codon_tca_secondary_1 codon_tca_secondary_2; norm_num

/-- `TCC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tcc_primary_0 : ℤ := -1
def codon_tcc_primary_1 : ℤ := -1
def codon_tcc_primary_2 : ℤ := -1
theorem codon_tcc_primary_phase :
    (codon_tcc_primary_0, codon_tcc_primary_1, codon_tcc_primary_2) = (-1, -1, -1) := by
  unfold codon_tcc_primary_0 codon_tcc_primary_1 codon_tcc_primary_2; norm_num
/-- `TCC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tcc_secondary_0 : ℤ := -1
def codon_tcc_secondary_1 : ℤ := 0
def codon_tcc_secondary_2 : ℤ := 0
theorem codon_tcc_secondary_phase :
    (codon_tcc_secondary_0, codon_tcc_secondary_1, codon_tcc_secondary_2) = (-1, 0, 0) := by
  unfold codon_tcc_secondary_0 codon_tcc_secondary_1 codon_tcc_secondary_2; norm_num

/-- `TCG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tcg_primary_0 : ℤ := -1
def codon_tcg_primary_1 : ℤ := -1
def codon_tcg_primary_2 : ℤ := 1
theorem codon_tcg_primary_phase :
    (codon_tcg_primary_0, codon_tcg_primary_1, codon_tcg_primary_2) = (-1, -1, 1) := by
  unfold codon_tcg_primary_0 codon_tcg_primary_1 codon_tcg_primary_2; norm_num
/-- `TCG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tcg_secondary_0 : ℤ := -1
def codon_tcg_secondary_1 : ℤ := 0
def codon_tcg_secondary_2 : ℤ := 0
theorem codon_tcg_secondary_phase :
    (codon_tcg_secondary_0, codon_tcg_secondary_1, codon_tcg_secondary_2) = (-1, 0, 0) := by
  unfold codon_tcg_secondary_0 codon_tcg_secondary_1 codon_tcg_secondary_2; norm_num

/-- `TCT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tct_primary_0 : ℤ := -1
def codon_tct_primary_1 : ℤ := -1
def codon_tct_primary_2 : ℤ := -1
theorem codon_tct_primary_phase :
    (codon_tct_primary_0, codon_tct_primary_1, codon_tct_primary_2) = (-1, -1, -1) := by
  unfold codon_tct_primary_0 codon_tct_primary_1 codon_tct_primary_2; norm_num
/-- `TCT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tct_secondary_0 : ℤ := -1
def codon_tct_secondary_1 : ℤ := 0
def codon_tct_secondary_2 : ℤ := -1
theorem codon_tct_secondary_phase :
    (codon_tct_secondary_0, codon_tct_secondary_1, codon_tct_secondary_2) = (-1, 0, -1) := by
  unfold codon_tct_secondary_0 codon_tct_secondary_1 codon_tct_secondary_2; norm_num

/-- `TGA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tga_primary_0 : ℤ := -1
def codon_tga_primary_1 : ℤ := 1
def codon_tga_primary_2 : ℤ := 1
theorem codon_tga_primary_phase :
    (codon_tga_primary_0, codon_tga_primary_1, codon_tga_primary_2) = (-1, 1, 1) := by
  unfold codon_tga_primary_0 codon_tga_primary_1 codon_tga_primary_2; norm_num
/-- `TGA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tga_secondary_0 : ℤ := -1
def codon_tga_secondary_1 : ℤ := 0
def codon_tga_secondary_2 : ℤ := 1
theorem codon_tga_secondary_phase :
    (codon_tga_secondary_0, codon_tga_secondary_1, codon_tga_secondary_2) = (-1, 0, 1) := by
  unfold codon_tga_secondary_0 codon_tga_secondary_1 codon_tga_secondary_2; norm_num

/-- `TGC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tgc_primary_0 : ℤ := -1
def codon_tgc_primary_1 : ℤ := 1
def codon_tgc_primary_2 : ℤ := -1
theorem codon_tgc_primary_phase :
    (codon_tgc_primary_0, codon_tgc_primary_1, codon_tgc_primary_2) = (-1, 1, -1) := by
  unfold codon_tgc_primary_0 codon_tgc_primary_1 codon_tgc_primary_2; norm_num
/-- `TGC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tgc_secondary_0 : ℤ := -1
def codon_tgc_secondary_1 : ℤ := 0
def codon_tgc_secondary_2 : ℤ := 0
theorem codon_tgc_secondary_phase :
    (codon_tgc_secondary_0, codon_tgc_secondary_1, codon_tgc_secondary_2) = (-1, 0, 0) := by
  unfold codon_tgc_secondary_0 codon_tgc_secondary_1 codon_tgc_secondary_2; norm_num

/-- `TGG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tgg_primary_0 : ℤ := -1
def codon_tgg_primary_1 : ℤ := 1
def codon_tgg_primary_2 : ℤ := 1
theorem codon_tgg_primary_phase :
    (codon_tgg_primary_0, codon_tgg_primary_1, codon_tgg_primary_2) = (-1, 1, 1) := by
  unfold codon_tgg_primary_0 codon_tgg_primary_1 codon_tgg_primary_2; norm_num
/-- `TGG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tgg_secondary_0 : ℤ := -1
def codon_tgg_secondary_1 : ℤ := 0
def codon_tgg_secondary_2 : ℤ := 0
theorem codon_tgg_secondary_phase :
    (codon_tgg_secondary_0, codon_tgg_secondary_1, codon_tgg_secondary_2) = (-1, 0, 0) := by
  unfold codon_tgg_secondary_0 codon_tgg_secondary_1 codon_tgg_secondary_2; norm_num

/-- `TGT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tgt_primary_0 : ℤ := -1
def codon_tgt_primary_1 : ℤ := 1
def codon_tgt_primary_2 : ℤ := -1
theorem codon_tgt_primary_phase :
    (codon_tgt_primary_0, codon_tgt_primary_1, codon_tgt_primary_2) = (-1, 1, -1) := by
  unfold codon_tgt_primary_0 codon_tgt_primary_1 codon_tgt_primary_2; norm_num
/-- `TGT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tgt_secondary_0 : ℤ := -1
def codon_tgt_secondary_1 : ℤ := 0
def codon_tgt_secondary_2 : ℤ := -1
theorem codon_tgt_secondary_phase :
    (codon_tgt_secondary_0, codon_tgt_secondary_1, codon_tgt_secondary_2) = (-1, 0, -1) := by
  unfold codon_tgt_secondary_0 codon_tgt_secondary_1 codon_tgt_secondary_2; norm_num

/-- `TTA` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_tta_primary_0 : ℤ := -1
def codon_tta_primary_1 : ℤ := -1
def codon_tta_primary_2 : ℤ := 1
theorem codon_tta_primary_phase :
    (codon_tta_primary_0, codon_tta_primary_1, codon_tta_primary_2) = (-1, -1, 1) := by
  unfold codon_tta_primary_0 codon_tta_primary_1 codon_tta_primary_2; norm_num
/-- `TTA` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_tta_secondary_0 : ℤ := -1
def codon_tta_secondary_1 : ℤ := -1
def codon_tta_secondary_2 : ℤ := 1
theorem codon_tta_secondary_phase :
    (codon_tta_secondary_0, codon_tta_secondary_1, codon_tta_secondary_2) = (-1, -1, 1) := by
  unfold codon_tta_secondary_0 codon_tta_secondary_1 codon_tta_secondary_2; norm_num

/-- `TTC` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ttc_primary_0 : ℤ := -1
def codon_ttc_primary_1 : ℤ := -1
def codon_ttc_primary_2 : ℤ := -1
theorem codon_ttc_primary_phase :
    (codon_ttc_primary_0, codon_ttc_primary_1, codon_ttc_primary_2) = (-1, -1, -1) := by
  unfold codon_ttc_primary_0 codon_ttc_primary_1 codon_ttc_primary_2; norm_num
/-- `TTC` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ttc_secondary_0 : ℤ := -1
def codon_ttc_secondary_1 : ℤ := -1
def codon_ttc_secondary_2 : ℤ := 0
theorem codon_ttc_secondary_phase :
    (codon_ttc_secondary_0, codon_ttc_secondary_1, codon_ttc_secondary_2) = (-1, -1, 0) := by
  unfold codon_ttc_secondary_0 codon_ttc_secondary_1 codon_ttc_secondary_2; norm_num

/-- `TTG` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ttg_primary_0 : ℤ := -1
def codon_ttg_primary_1 : ℤ := -1
def codon_ttg_primary_2 : ℤ := 1
theorem codon_ttg_primary_phase :
    (codon_ttg_primary_0, codon_ttg_primary_1, codon_ttg_primary_2) = (-1, -1, 1) := by
  unfold codon_ttg_primary_0 codon_ttg_primary_1 codon_ttg_primary_2; norm_num
/-- `TTG` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ttg_secondary_0 : ℤ := -1
def codon_ttg_secondary_1 : ℤ := -1
def codon_ttg_secondary_2 : ℤ := 0
theorem codon_ttg_secondary_phase :
    (codon_ttg_secondary_0, codon_ttg_secondary_1, codon_ttg_secondary_2) = (-1, -1, 0) := by
  unfold codon_ttg_secondary_0 codon_ttg_secondary_1 codon_ttg_secondary_2; norm_num

/-- `TTT` primary spin axis [A,G=+1; C,T=-1]. -/
def codon_ttt_primary_0 : ℤ := -1
def codon_ttt_primary_1 : ℤ := -1
def codon_ttt_primary_2 : ℤ := -1
theorem codon_ttt_primary_phase :
    (codon_ttt_primary_0, codon_ttt_primary_1, codon_ttt_primary_2) = (-1, -1, -1) := by
  unfold codon_ttt_primary_0 codon_ttt_primary_1 codon_ttt_primary_2; norm_num
/-- `TTT` secondary genetic axis [A=+1; T=-1; G,C=0]. -/
def codon_ttt_secondary_0 : ℤ := -1
def codon_ttt_secondary_1 : ℤ := -1
def codon_ttt_secondary_2 : ℤ := -1
theorem codon_ttt_secondary_phase :
    (codon_ttt_secondary_0, codon_ttt_secondary_1, codon_ttt_secondary_2) = (-1, -1, -1) := by
  unfold codon_ttt_secondary_0 codon_ttt_secondary_1 codon_ttt_secondary_2; norm_num

/-- Bundle: 64 codons, dual-axis trinary map linked to Genomic exact identities. -/
theorem codon_trinary_map_bundle :
    codon_table_count = 64 ∧
    distinct_primary_codon_patterns = 8 ∧
    distinct_secondary_codon_patterns = 27 ∧
    stop_codon_count_cert = 3 ∧
    distinct_primary_codon_patterns ≤ 2 ^ 3 ∧
    distinct_secondary_codon_patterns ≤ genetic_trinary_alphabet_card ^ 3 ∧
    genetic_trinary_alphabet_card ^ 3 = 27 ∧
    (4 : ℝ) ^ 3 = 64 ∧
    (3 : ℝ) / 64 = 0.046875 ∧
    (codon_aaa_primary_0, codon_aaa_primary_1, codon_aaa_primary_2) = (1, 1, 1) ∧
    (codon_ttt_primary_0, codon_ttt_primary_1, codon_ttt_primary_2) = (-1, -1, -1) ∧
    (codon_gca_primary_0, codon_gca_primary_1, codon_gca_primary_2) = (1, -1, 1) ∧
    (codon_cgt_primary_0, codon_cgt_primary_1, codon_cgt_primary_2) = (-1, 1, -1) ∧
    (codon_atg_primary_0, codon_atg_primary_1, codon_atg_primary_2) = (1, -1, 1) ∧
    (codon_taa_primary_0, codon_taa_primary_1, codon_taa_primary_2) = (-1, 1, 1) ∧
    (codon_aaa_secondary_0, codon_aaa_secondary_1, codon_aaa_secondary_2) = (1, 1, 1) ∧
    (codon_ttt_secondary_0, codon_ttt_secondary_1, codon_ttt_secondary_2) = (-1, -1, -1) ∧
    (codon_gca_secondary_0, codon_gca_secondary_1, codon_gca_secondary_2) = (0, 0, 1) ∧
    (codon_cgt_secondary_0, codon_cgt_secondary_1, codon_cgt_secondary_2) = (0, 0, -1) ∧
    (codon_atg_secondary_0, codon_atg_secondary_1, codon_atg_secondary_2) = (1, -1, 0) ∧
    (codon_taa_secondary_0, codon_taa_secondary_1, codon_taa_secondary_2) = (-1, 1, 1) := by
  refine ⟨by unfold codon_table_count; norm_num, by unfold distinct_primary_codon_patterns; norm_num, by unfold distinct_secondary_codon_patterns; norm_num, by unfold stop_codon_count_cert; norm_num, by unfold distinct_primary_codon_patterns; norm_num,
    by unfold distinct_secondary_codon_patterns genetic_trinary_alphabet_card; norm_num, codon_secondary_pattern_space_eq_twenty_seven, codon_genomic_table_link, stop_codon_fraction_cert,
    codon_aaa_primary_phase,
    codon_ttt_primary_phase,
    codon_gca_primary_phase,
    codon_cgt_primary_phase,
    codon_atg_primary_phase,
    codon_taa_primary_phase,
    codon_aaa_secondary_phase,
    codon_ttt_secondary_phase,
    codon_gca_secondary_phase,
    codon_cgt_secondary_phase,
    codon_atg_secondary_phase,
    codon_taa_secondary_phase⟩

end

end FSOT.Formal
