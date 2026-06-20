/-
  FSOT Formal ProteinPriors — auto-generated amino-acid trinary certificates.

  Source: Genetics/fsot_protein + data/lab_registry.json → protein_formulas
  Generator: scripts/gen_protein_priors_lean.py

  Each canonical amino acid maps to [Charge, Polarity, Volume] ∈ {-1,0,+1}³,
  a subset of the 27-pattern genomic codon space (FSOT.Formal.Genomic).
-/

import FSOT.Formal.Genomic

namespace FSOT.Formal

noncomputable section

open Real

def canonical_amino_acid_count : ℕ := 20
def distinct_aa_trinary_patterns : ℕ := 10

theorem canonical_amino_acid_count_eq_twenty :
    canonical_amino_acid_count = 20 := by
  unfold canonical_amino_acid_count; norm_num

theorem protein_trinary_pattern_space_eq_twenty_seven :
    genetic_trinary_alphabet_card ^ 3 = 27 :=
  codon_genetic_pattern_space_eq_twenty_seven

theorem protein_amino_acid_genomic_identity :
    4 * phi ^ 3 + 8 / phi ^ 2 = 20 :=
  amino_acids_canonical_eq_twenty

/-- `Alanine` (A) trinary phase [Charge, Polarity, Volume]. -/
def alanine_charge : ℤ := 0
def alanine_polarity : ℤ := -1
def alanine_volume : ℤ := -1
theorem alanine_trinary_phase :
    (alanine_charge, alanine_polarity, alanine_volume) = (0, -1, -1) := by
  unfold alanine_charge alanine_polarity alanine_volume; norm_num

/-- `Cysteine` (C) trinary phase [Charge, Polarity, Volume]. -/
def cysteine_charge : ℤ := 0
def cysteine_polarity : ℤ := 0
def cysteine_volume : ℤ := -1
theorem cysteine_trinary_phase :
    (cysteine_charge, cysteine_polarity, cysteine_volume) = (0, 0, -1) := by
  unfold cysteine_charge cysteine_polarity cysteine_volume; norm_num

/-- `Aspartic Acid` (D) trinary phase [Charge, Polarity, Volume]. -/
def aspartic_acid_charge : ℤ := -1
def aspartic_acid_polarity : ℤ := 1
def aspartic_acid_volume : ℤ := 0
theorem aspartic_acid_trinary_phase :
    (aspartic_acid_charge, aspartic_acid_polarity, aspartic_acid_volume) = (-1, 1, 0) := by
  unfold aspartic_acid_charge aspartic_acid_polarity aspartic_acid_volume; norm_num

/-- `Glutamic Acid` (E) trinary phase [Charge, Polarity, Volume]. -/
def glutamic_acid_charge : ℤ := -1
def glutamic_acid_polarity : ℤ := 1
def glutamic_acid_volume : ℤ := 1
theorem glutamic_acid_trinary_phase :
    (glutamic_acid_charge, glutamic_acid_polarity, glutamic_acid_volume) = (-1, 1, 1) := by
  unfold glutamic_acid_charge glutamic_acid_polarity glutamic_acid_volume; norm_num

/-- `Phenylalanine` (F) trinary phase [Charge, Polarity, Volume]. -/
def phenylalanine_charge : ℤ := 0
def phenylalanine_polarity : ℤ := -1
def phenylalanine_volume : ℤ := 1
theorem phenylalanine_trinary_phase :
    (phenylalanine_charge, phenylalanine_polarity, phenylalanine_volume) = (0, -1, 1) := by
  unfold phenylalanine_charge phenylalanine_polarity phenylalanine_volume; norm_num

/-- `Glycine` (G) trinary phase [Charge, Polarity, Volume]. -/
def glycine_charge : ℤ := 0
def glycine_polarity : ℤ := -1
def glycine_volume : ℤ := -1
theorem glycine_trinary_phase :
    (glycine_charge, glycine_polarity, glycine_volume) = (0, -1, -1) := by
  unfold glycine_charge glycine_polarity glycine_volume; norm_num

/-- `Histidine` (H) trinary phase [Charge, Polarity, Volume]. -/
def histidine_charge : ℤ := 1
def histidine_polarity : ℤ := 1
def histidine_volume : ℤ := 1
theorem histidine_trinary_phase :
    (histidine_charge, histidine_polarity, histidine_volume) = (1, 1, 1) := by
  unfold histidine_charge histidine_polarity histidine_volume; norm_num

/-- `Isoleucine` (I) trinary phase [Charge, Polarity, Volume]. -/
def isoleucine_charge : ℤ := 0
def isoleucine_polarity : ℤ := -1
def isoleucine_volume : ℤ := 1
theorem isoleucine_trinary_phase :
    (isoleucine_charge, isoleucine_polarity, isoleucine_volume) = (0, -1, 1) := by
  unfold isoleucine_charge isoleucine_polarity isoleucine_volume; norm_num

/-- `Lysine` (K) trinary phase [Charge, Polarity, Volume]. -/
def lysine_charge : ℤ := 1
def lysine_polarity : ℤ := 1
def lysine_volume : ℤ := 1
theorem lysine_trinary_phase :
    (lysine_charge, lysine_polarity, lysine_volume) = (1, 1, 1) := by
  unfold lysine_charge lysine_polarity lysine_volume; norm_num

/-- `Leucine` (L) trinary phase [Charge, Polarity, Volume]. -/
def leucine_charge : ℤ := 0
def leucine_polarity : ℤ := -1
def leucine_volume : ℤ := 1
theorem leucine_trinary_phase :
    (leucine_charge, leucine_polarity, leucine_volume) = (0, -1, 1) := by
  unfold leucine_charge leucine_polarity leucine_volume; norm_num

/-- `Methionine` (M) trinary phase [Charge, Polarity, Volume]. -/
def methionine_charge : ℤ := 0
def methionine_polarity : ℤ := -1
def methionine_volume : ℤ := 1
theorem methionine_trinary_phase :
    (methionine_charge, methionine_polarity, methionine_volume) = (0, -1, 1) := by
  unfold methionine_charge methionine_polarity methionine_volume; norm_num

/-- `Asparagine` (N) trinary phase [Charge, Polarity, Volume]. -/
def asparagine_charge : ℤ := 0
def asparagine_polarity : ℤ := 1
def asparagine_volume : ℤ := 0
theorem asparagine_trinary_phase :
    (asparagine_charge, asparagine_polarity, asparagine_volume) = (0, 1, 0) := by
  unfold asparagine_charge asparagine_polarity asparagine_volume; norm_num

/-- `Proline` (P) trinary phase [Charge, Polarity, Volume]. -/
def proline_charge : ℤ := 0
def proline_polarity : ℤ := -1
def proline_volume : ℤ := 0
theorem proline_trinary_phase :
    (proline_charge, proline_polarity, proline_volume) = (0, -1, 0) := by
  unfold proline_charge proline_polarity proline_volume; norm_num

/-- `Glutamine` (Q) trinary phase [Charge, Polarity, Volume]. -/
def glutamine_charge : ℤ := 0
def glutamine_polarity : ℤ := 1
def glutamine_volume : ℤ := 1
theorem glutamine_trinary_phase :
    (glutamine_charge, glutamine_polarity, glutamine_volume) = (0, 1, 1) := by
  unfold glutamine_charge glutamine_polarity glutamine_volume; norm_num

/-- `Arginine` (R) trinary phase [Charge, Polarity, Volume]. -/
def arginine_charge : ℤ := 1
def arginine_polarity : ℤ := 1
def arginine_volume : ℤ := 1
theorem arginine_trinary_phase :
    (arginine_charge, arginine_polarity, arginine_volume) = (1, 1, 1) := by
  unfold arginine_charge arginine_polarity arginine_volume; norm_num

/-- `Serine` (S) trinary phase [Charge, Polarity, Volume]. -/
def serine_charge : ℤ := 0
def serine_polarity : ℤ := 1
def serine_volume : ℤ := -1
theorem serine_trinary_phase :
    (serine_charge, serine_polarity, serine_volume) = (0, 1, -1) := by
  unfold serine_charge serine_polarity serine_volume; norm_num

/-- `Threonine` (T) trinary phase [Charge, Polarity, Volume]. -/
def threonine_charge : ℤ := 0
def threonine_polarity : ℤ := 1
def threonine_volume : ℤ := 0
theorem threonine_trinary_phase :
    (threonine_charge, threonine_polarity, threonine_volume) = (0, 1, 0) := by
  unfold threonine_charge threonine_polarity threonine_volume; norm_num

/-- `Valine` (V) trinary phase [Charge, Polarity, Volume]. -/
def valine_charge : ℤ := 0
def valine_polarity : ℤ := -1
def valine_volume : ℤ := 0
theorem valine_trinary_phase :
    (valine_charge, valine_polarity, valine_volume) = (0, -1, 0) := by
  unfold valine_charge valine_polarity valine_volume; norm_num

/-- `Tryptophan` (W) trinary phase [Charge, Polarity, Volume]. -/
def tryptophan_charge : ℤ := 0
def tryptophan_polarity : ℤ := -1
def tryptophan_volume : ℤ := 1
theorem tryptophan_trinary_phase :
    (tryptophan_charge, tryptophan_polarity, tryptophan_volume) = (0, -1, 1) := by
  unfold tryptophan_charge tryptophan_polarity tryptophan_volume; norm_num

/-- `Tyrosine` (Y) trinary phase [Charge, Polarity, Volume]. -/
def tyrosine_charge : ℤ := 0
def tyrosine_polarity : ℤ := 1
def tyrosine_volume : ℤ := 1
theorem tyrosine_trinary_phase :
    (tyrosine_charge, tyrosine_polarity, tyrosine_volume) = (0, 1, 1) := by
  unfold tyrosine_charge tyrosine_polarity tyrosine_volume; norm_num

/-- Bundle: 20 amino acids, trinary phases ⊆ 27-pattern genomic space. -/
theorem protein_amino_acid_trinary_bundle :
    canonical_amino_acid_count = 20 ∧
    distinct_aa_trinary_patterns = 10 ∧
    distinct_aa_trinary_patterns ≤ genetic_trinary_alphabet_card ^ 3 ∧
    genetic_trinary_alphabet_card ^ 3 = 27 ∧
    4 * phi ^ 3 + 8 / phi ^ 2 = 20 ∧
    (alanine_charge, alanine_polarity, alanine_volume) = (0, -1, -1) ∧
    (cysteine_charge, cysteine_polarity, cysteine_volume) = (0, 0, -1) ∧
    (aspartic_acid_charge, aspartic_acid_polarity, aspartic_acid_volume) = (-1, 1, 0) ∧
    (glutamic_acid_charge, glutamic_acid_polarity, glutamic_acid_volume) = (-1, 1, 1) ∧
    (phenylalanine_charge, phenylalanine_polarity, phenylalanine_volume) = (0, -1, 1) ∧
    (glycine_charge, glycine_polarity, glycine_volume) = (0, -1, -1) ∧
    (histidine_charge, histidine_polarity, histidine_volume) = (1, 1, 1) ∧
    (isoleucine_charge, isoleucine_polarity, isoleucine_volume) = (0, -1, 1) ∧
    (lysine_charge, lysine_polarity, lysine_volume) = (1, 1, 1) ∧
    (leucine_charge, leucine_polarity, leucine_volume) = (0, -1, 1) ∧
    (methionine_charge, methionine_polarity, methionine_volume) = (0, -1, 1) ∧
    (asparagine_charge, asparagine_polarity, asparagine_volume) = (0, 1, 0) ∧
    (proline_charge, proline_polarity, proline_volume) = (0, -1, 0) ∧
    (glutamine_charge, glutamine_polarity, glutamine_volume) = (0, 1, 1) ∧
    (arginine_charge, arginine_polarity, arginine_volume) = (1, 1, 1) ∧
    (serine_charge, serine_polarity, serine_volume) = (0, 1, -1) ∧
    (threonine_charge, threonine_polarity, threonine_volume) = (0, 1, 0) ∧
    (valine_charge, valine_polarity, valine_volume) = (0, -1, 0) ∧
    (tryptophan_charge, tryptophan_polarity, tryptophan_volume) = (0, -1, 1) ∧
    (tyrosine_charge, tyrosine_polarity, tyrosine_volume) = (0, 1, 1) := by
  refine ⟨by unfold canonical_amino_acid_count; norm_num, by unfold distinct_aa_trinary_patterns; norm_num, by unfold distinct_aa_trinary_patterns genetic_trinary_alphabet_card; norm_num, protein_trinary_pattern_space_eq_twenty_seven, protein_amino_acid_genomic_identity,
    alanine_trinary_phase,
    cysteine_trinary_phase,
    aspartic_acid_trinary_phase,
    glutamic_acid_trinary_phase,
    phenylalanine_trinary_phase,
    glycine_trinary_phase,
    histidine_trinary_phase,
    isoleucine_trinary_phase,
    lysine_trinary_phase,
    leucine_trinary_phase,
    methionine_trinary_phase,
    asparagine_trinary_phase,
    proline_trinary_phase,
    glutamine_trinary_phase,
    arginine_trinary_phase,
    serine_trinary_phase,
    threonine_trinary_phase,
    valine_trinary_phase,
    tryptophan_trinary_phase,
    tyrosine_trinary_phase⟩

end

end FSOT.Formal
