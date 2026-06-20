/-
  FSOT Formal Genomic — machine-checked exact biological identities.

  Proves NeuroLab Genomic Sciences EXACT translations (codon table, amino acids)
  at canonical FSOT seed constants. Interval certificate for autosome count.
  Interval bounds validated by scripts/gen_genomic_bounds.py.
-/

import FSOT.Formal.Bounds

namespace FSOT.Formal

noncomputable section

open Real

/-- Golden ratio identity: φ² = φ + 1. -/
lemma phi_sq_eq : phi ^ 2 = phi + 1 := by
  unfold phi
  field_simp
  ring_nf
  rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5)]
  ring

lemma phi_ne_zero : phi ≠ 0 := ne_of_gt (lt_trans (by norm_num) phi_gt_one)

lemma phi_sq_ne_zero : phi ^ 2 ≠ 0 := by
  have : (0 : ℝ) < phi ^ 2 := by nlinarith [phi_gt_1618]
  linarith

/-- φ³ = 2φ + 1. -/
lemma phi_cubed_eq : phi ^ 3 = 2 * phi + 1 := by
  calc
    phi ^ 3 = phi ^ 2 * phi := by rw [pow_succ, pow_two]
    _ = (phi + 1) * phi := by rw [phi_sq_eq]
    _ = phi ^ 2 + phi := by ring
    _ = (phi + 1) + phi := by rw [phi_sq_eq]
    _ = 2 * phi + 1 := by ring

/-- φ⁻¹ = φ − 1. -/
lemma one_div_phi_eq : 1 / phi = phi - 1 := by
  field_simp [phi_ne_zero]
  nlinarith [phi_sq_eq, phi_gt_1618]

/-- φ⁻² = 2 − φ. -/
lemma one_div_phi_sq_eq : 1 / phi ^ 2 = 2 - phi := by
  calc
    1 / phi ^ 2 = (1 / phi) ^ 2 := by rw [one_div_pow]
    _ = (phi - 1) ^ 2 := by rw [one_div_phi_eq]
    _ = phi ^ 2 - 2 * phi + 1 := by ring
    _ = (phi + 1) - 2 * phi + 1 := by rw [phi_sq_eq]
    _ = 2 - phi := by ring

lemma phi_zpow_neg5_eq_inv_pow5 : phi ^ (-5 : ℤ) = 1 / phi ^ 5 := by
  rw [zpow_neg, inv_eq_one_div]
  rfl

/-- Codon table: 4³ = 64. -/
theorem codon_table_size_eq_sixty_four : (4 : ℝ) ^ 3 = 64 := by norm_num

/-- Trinary pattern count: 3³ = 27. -/
theorem trinary_pattern_count_eq_twenty_seven : (3 : ℝ) ^ 3 = 27 := by norm_num

/-- FSOT per-base genetic trinary alphabet (A→+1, G/C→0, T→−1). -/
def genetic_trinary_alphabet_card : ℕ := 3

/-- Codon genetic pattern space: three base trits ⇒ |alphabet|³ = 27 patterns. -/
theorem codon_genetic_pattern_space_eq_twenty_seven :
    genetic_trinary_alphabet_card ^ 3 = 27 := by
  unfold genetic_trinary_alphabet_card
  norm_num

/-- Genetic pattern space matches the Genomic Sciences 3³ trinary count. -/
theorem genetic_pattern_space_matches_trinary_count :
    (genetic_trinary_alphabet_card : ℝ) ^ 3 = (3 : ℝ) ^ 3 := by
  unfold genetic_trinary_alphabet_card
  norm_num

/-- 64 codons map onto 27 genetic trinary patterns with degeneracy 64/27. -/
theorem codon_genetic_degeneracy :
    (4 : ℝ) ^ 3 / (genetic_trinary_alphabet_card : ℝ) ^ 3 = (64 : ℝ) / 27 := by
  unfold genetic_trinary_alphabet_card
  norm_num

/-- Stop codon fraction: 3/64. -/
theorem stop_codons_fraction_eq : (3 : ℝ) / 64 = 0.046875 := by norm_num

/-- Codon–trinary degeneracy ratio: (4/3)³ = 64/27. -/
theorem codon_trinary_degeneracy_eq :
    ((4 : ℝ) / 3) ^ 3 = (64 : ℝ) / 27 := by norm_num

/-- Canonical amino acid count: 4φ³ + 8φ⁻² = 20. -/
theorem amino_acids_canonical_eq_twenty :
    4 * phi ^ 3 + 8 / phi ^ 2 = 20 := by
  rw [phi_cubed_eq, div_eq_mul_one_div, one_div_phi_sq_eq]
  ring

/-- φ⁵ lower bracket (gen_genomic_bounds.py: PHI_LO^5 ≈ 11.089). -/
lemma phi_pow5_gt_11089 : (11.089 : ℝ) < phi ^ 5 := by
  have hφ : (1.618 : ℝ) < phi := phi_gt_1618
  have hφ2 : (2.617924 : ℝ) < phi ^ 2 := phi_sq_gt_261792
  have hφ4 : (6.853 : ℝ) < phi ^ 4 := by
    nlinarith [hφ, hφ2, phi_sq_eq, sq_nonneg (phi ^ 2 - phi)]
  nlinarith [hφ4, hφ, phi_sq_eq]

/-- φ⁵ upper bracket (gen_genomic_bounds.py: PHI_HI^5 ≈ 11.09244). -/
lemma phi_pow5_lt_11094 : phi ^ 5 < (11.09244 : ℝ) := by
  have hφ : phi < (1.6181 : ℝ) := phi_lt_16181
  have hφ2 : phi ^ 2 < (26183 : ℝ) / 10000 := phi_sq_lt_26183
  have hφ4 : phi ^ 4 < (6.8549 : ℝ) := by
    nlinarith [hφ, hφ2, phi_sq_eq, sq_nonneg (phi ^ 2 - phi)]
  nlinarith [hφ4, hφ, phi_sq_eq]

lemma phi_pow_neg5_gt_09013 : (0.09015 : ℝ) < phi ^ (-5 : ℤ) := by
  rw [phi_zpow_neg5_eq_inv_pow5]
  have h5pos : 0 < phi ^ 5 := pow_pos (by linarith [phi_gt_1618]) 5
  have h_inv : 1 / (11.09244 : ℝ) < 1 / phi ^ 5 :=
    one_div_lt_one_div_of_lt h5pos phi_pow5_lt_11094
  have h_base : (0.09015 : ℝ) < 1 / (11.09244 : ℝ) := by norm_num
  linarith [h_base, h_inv]

lemma phi_pow_neg5_lt_09018 : phi ^ (-5 : ℤ) < (0.09018 : ℝ) := by
  rw [phi_zpow_neg5_eq_inv_pow5]
  have h5pos : 0 < phi ^ 5 := pow_pos (by linarith [phi_gt_1618]) 5
  have h_inv : 1 / phi ^ 5 < 1 / (11.089 : ℝ) :=
    one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 11.089) phi_pow5_gt_11089
  have h_base : 1 / (11.089 : ℝ) < (0.09018 : ℝ) := by norm_num
  linarith [h_inv, h_base]

/-- Haploid autosome count: 2(φ⁵ − φ⁻⁵) ≈ 22 (Lucas L₅ certificate). -/
theorem autosome_haploid_count_eq_twenty_two :
    |(2 * (phi ^ 5 - phi ^ (-5 : ℤ))) - 22| < (0.01 : ℝ) := by
  rw [abs_lt, phi_zpow_neg5_eq_inv_pow5]
  have h5lo : (11.089 : ℝ) < phi ^ 5 := phi_pow5_gt_11089
  have h5hi : phi ^ 5 < (11.09244 : ℝ) := phi_pow5_lt_11094
  have hmlo : (0.09015 : ℝ) < 1 / phi ^ 5 := by
    rw [← phi_zpow_neg5_eq_inv_pow5]
    exact phi_pow_neg5_gt_09013
  have hmhi : 1 / phi ^ 5 < (0.09018 : ℝ) := by
    rw [← phi_zpow_neg5_eq_inv_pow5]
    exact phi_pow_neg5_lt_09018
  constructor <;> nlinarith [h5lo, h5hi, hmlo, hmhi]

/-- Bundle of exact genomic identities used by NeuroLab Genomic Sciences. -/
theorem genomic_exact_identity_bundle :
    (4 : ℝ) ^ 3 = 64 ∧
      (3 : ℝ) ^ 3 = 27 ∧
        (3 : ℝ) / 64 = 0.046875 ∧
          ((4 : ℝ) / 3) ^ 3 = (64 : ℝ) / 27 ∧
            4 * phi ^ 3 + 8 / phi ^ 2 = 20 ∧
              |(2 * (phi ^ 5 - phi ^ (-5 : ℤ))) - 22| < (0.01 : ℝ) := by
  refine ⟨codon_table_size_eq_sixty_four, trinary_pattern_count_eq_twenty_seven,
    stop_codons_fraction_eq, codon_trinary_degeneracy_eq,
    amino_acids_canonical_eq_twenty, autosome_haploid_count_eq_twenty_two⟩

end

end FSOT.Formal