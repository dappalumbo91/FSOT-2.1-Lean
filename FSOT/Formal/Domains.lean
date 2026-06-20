/-
  FSOT Formal Domain Parameter Mappings (Real).

  35-domain ledger aligned with FSOTLean `Domains.lean` and the Dimensional Bleed Hierarchy.
  Sign theorems cite MC / combustion evidence where full numeric closure is still open;
  cosmological term-level sign and dominance lemmas are proved via `FSOT.Formal.Theorems`.
-/

import FSOT.Formal.Scalar
import FSOT.Formal.Bounds
import FSOT.Formal.Theorems

namespace FSOT.Formal

noncomputable section

open Real

/-- Domain scalar with optional parameter overrides. -/
noncomputable def compute_for_domain (domain : String) (overrides : FSOTParams := {}) : ℝ :=
  let base := get_domain_params domain
  let p := { base with
    N := overrides.N,
    P := overrides.P,
    D_eff := overrides.D_eff,
    recent_hits := overrides.recent_hits,
    delta_psi := overrides.delta_psi,
    observed := overrides.observed }
  scaled_S p

lemma cosmological_domain_eq :
    get_domain_params "cosmological" = cosmologicalParams := by
  simp [get_domain_params, cosmologicalParams]

lemma cosmological_observed_false :
    (get_domain_params "cosmological").observed = false := by
  simp [get_domain_params]

lemma cosmological_D_eff_eq :
    (get_domain_params "cosmological").D_eff = 25 := by
  simp [get_domain_params]

lemma dark_energy_observed_false :
    (get_domain_params "dark_energy").observed = false := by
  simp [get_domain_params]

lemma dark_energy_D_eff_eq :
    (get_domain_params "dark_energy").D_eff = 25 := by
  simp [get_domain_params]

lemma dark_energy_delta_bounds :
    (0.5 : ℝ) ≤ (get_domain_params "dark_energy").delta_psi ∧
      (get_domain_params "dark_energy").delta_psi ≤ 1.3 := by
  simp [get_domain_params]
  norm_num

lemma cmb_observed_false :
    (get_domain_params "cmb").observed = false := by
  simp [get_domain_params]

lemma cmb_D_eff_eq :
    (get_domain_params "cmb").D_eff = 24 := by
  simp [get_domain_params]

lemma ai_observed_false :
    (get_domain_params "ai").observed = false := by
  simp [get_domain_params]

lemma ai_D_eff_eq :
    (get_domain_params "ai").D_eff = 11 := by
  simp [get_domain_params]

lemma neural_observed_true :
    (get_domain_params "neural").observed = true := by
  simp [get_domain_params]

/-- Cosmological domain: term1 is strictly negative (high-D, no observer). -/
theorem cosmological_term1_negative :
    term1 (get_domain_params "cosmological") < 0 := by
  rw [cosmological_domain_eq]
  have h_adj := cosmological_perceived_adjust_eq_one
  have h_quirk : quirkMod cosmologicalParams = 1 := by simp [quirkMod, cosmologicalParams]
  have h_term1 : term1 cosmologicalParams = term1_base cosmologicalParams := by
    simp [term1, h_quirk, h_adj]
  rw [h_term1]
  exact term1_base_negative_for_high_D_eff cosmologicalParams
    cosmological_D_bounds (by rfl) cosmological_delta_bounds
    cosmological_N_pos cosmological_P_pos

/-- Cosmological domain: |term1| exceeds |term3| (term1 carries the dispersal sign). -/
theorem cosmological_term1_dominates_term3 :
    abs (term3 (get_domain_params "cosmological")) <
      abs (term1 (get_domain_params "cosmological")) := by
  rw [cosmological_domain_eq]
  exact term3_dominates_in_cosmological_regime

/-- Cosmological domain produces negative raw_S.
    MC oracle (`fsot_compute.py`, D=25, δψ=1, observed=false):
    raw_S ≈ −1.195693, scaled_S ≈ −0.502456 (T1≈−2.20, T2=1, T3≈0). -/
theorem cosmological_raw_S_negative :
    raw_S (get_domain_params "cosmological") < 0 := by
  rw [cosmological_domain_eq]
  have h_adj := cosmological_perceived_adjust_eq_one
  have h_quirk : quirkMod cosmologicalParams = 1 := by simp [quirkMod, cosmologicalParams]
  have h_term1_eq : term1 cosmologicalParams = term1_base cosmologicalParams := by
    simp [term1, h_quirk, h_adj]
  have h_term1_neg := cosmological_term1_negative
  have h_term3 := cosmological_term3_abs_lt_fifth
  have h_mag := cosmological_term1_base_abs_gt_one_two
  have h_base_neg := term1_base_negative_for_high_D_eff cosmologicalParams
    cosmological_D_bounds (by rfl) cosmological_delta_bounds
    cosmological_N_pos cosmological_P_pos
  have h_term1_mag : (1 : ℝ) + abs (term3 cosmologicalParams) < -term1 cosmologicalParams := by
    have h_neg : -term1 cosmologicalParams = abs (term1_base cosmologicalParams) := by
      rw [h_term1_eq, abs_of_neg h_base_neg]
    rw [h_neg]
    linarith [h_mag, h_term3]
  have h_term1_neg' : term1 cosmologicalParams < 0 := by
    simpa [cosmological_domain_eq] using h_term1_neg
  exact raw_S_negative_when_term1_overcomes_defaults cosmologicalParams
    cosmological_term2_eq_one h_term1_neg' h_term1_mag

/-- Dark-energy domain: term1 negative (same high-D dispersal regime as cosmological). -/
theorem dark_energy_term1_negative :
    term1 (get_domain_params "dark_energy") < 0 := by
  set p := get_domain_params "dark_energy"
  have h_obs := dark_energy_observed_false
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_adj : 1 + new_perceived_param * log (p.D_eff / 25) = 1 := by
    simp [p, get_domain_params, log_one]
  have h_term1 : term1 p = term1_base p := by simp [term1, h_quirk, h_adj]
  rw [h_term1]
  have h_D : (20 : ℝ) ≤ p.D_eff := by simp [p, get_domain_params]; norm_num
  exact term1_base_negative_for_high_D_eff p h_D h_obs dark_energy_delta_bounds
    (by simp [p, get_domain_params]) (by simp [p, get_domain_params])

lemma dark_energy_params_eq :
    get_domain_params "dark_energy" =
      { D_eff := 25, recent_hits := 0, delta_psi := 1.1, observed := false } := by
  simp [get_domain_params]

lemma dark_energy_term2_eq_one :
    term2 (get_domain_params "dark_energy") = 1 := by
  simp [term2, get_domain_params]

/-- Dark energy (D_eff=25, δψ=1.1, no observer) negative raw_S.
    MC oracle: raw_S ≈ −1.134979 (`fsot_compute.py`). -/
theorem dark_energy_raw_S_negative :
    raw_S (get_domain_params "dark_energy") < 0 := by
  set p := get_domain_params "dark_energy"
  have h_obs := dark_energy_observed_false
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_adj : 1 + new_perceived_param * log (p.D_eff / 25) = 1 := by
    simp [p, get_domain_params, log_one]
  have h_term1_eq : term1 p = term1_base p := by simp [term1, h_quirk, h_adj]
  have h_term1_neg := dark_energy_term1_negative
  have h_mag := dark_energy_term1_base_abs_gt_one_two p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    h_obs (by simp [p, get_domain_params]) (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    (by simp [p, get_domain_params])
  have h_base_neg := term1_base_negative_for_high_D_eff p (by simp [p, get_domain_params]; norm_num) h_obs
    dark_energy_delta_bounds (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_term3 := dark_energy_term3_abs_lt_fifth p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    (by simp [p, get_domain_params]) (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_term1_mag : (1 : ℝ) + abs (term3 p) < -term1 p := by
    have h_neg : -term1 p = abs (term1_base p) := by
      rw [h_term1_eq, abs_of_neg h_base_neg]
    rw [h_neg]
    linarith [h_mag, h_term3]
  exact raw_S_negative_when_term1_overcomes_defaults p dark_energy_term2_eq_one
    (lt_of_eq_of_lt h_term1_eq h_base_neg) h_term1_mag

/-- CMB domain: term1 negative (D=24, no observer). -/
theorem cmb_term1_negative :
    term1 (get_domain_params "cmb") < 0 := by
  set p := get_domain_params "cmb"
  have h_obs := cmb_observed_false
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_D_bounds : (20 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 30 := by
    simp [p, get_domain_params]; norm_num
  have h_adj_pos : (0 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25) :=
    lt_trans (by norm_num) (perceived_adjust_lo p h_D_bounds)
  have h_base := term1_base_negative_for_high_D_eff p h_D_bounds.1 h_obs cmb_delta_bounds
    (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_term1 : term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    simp [term1, h_quirk]
  rw [h_term1]
  nlinarith [h_base, h_adj_pos]

lemma domain_term2_eq_one (domain : String) :
    term2 (get_domain_params domain) = 1 := by
  simp only [term2, get_domain_params]
  split <;> simp

lemma domain_term3_abs_lt_fifth (domain : String)
    (h_D : (6 : ℝ) ≤ (get_domain_params domain).D_eff ∧
      (get_domain_params domain).D_eff ≤ 25)
    (h_dp : (0 : ℝ) ≤ (get_domain_params domain).delta_psi ∧
      (get_domain_params domain).delta_psi ≤ 1.3) :
    abs (term3 (get_domain_params domain)) < (0.2 : ℝ) := by
  refine term3_abs_lt_fifth_default (get_domain_params domain) h_D h_dp ?_ ?_ ?_
  all_goals (simp only [get_domain_params]; split <;> rfl)

/-- AI domain (D_eff=11, no observer) non-positive raw_S.
    Python oracle (`fsot_compute.py` ledger): raw_S ≈ −0.147673. -/
theorem ai_raw_S_non_positive :
    raw_S (get_domain_params "ai") ≤ 0 := by
  set p := get_domain_params "ai"
  have h_term1_neg := lt_trans domain_term1_lt_neg_08_ai (by norm_num : (-0.8 : ℝ) < 0)
  have h_neg := raw_S_negative_of_term1_overcomes_term3 p (domain_term2_eq_one "ai")
    h_term1_neg domain_ai_term1_overcomes_term3
  exact le_of_lt h_neg

/-- Neural domain (D_eff=14, observer) positive raw_S.
    Python oracle: raw_S ≈ +0.514362. -/
theorem neural_raw_S_positive :
    raw_S (get_domain_params "neural") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "neural") := by
    refine domain_term1_positive_of_params (get_domain_params "neural") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "neural")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "neural") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "neural")
    (domain_term2_eq_one "neural") (lt_trans (by norm_num) h_term1) h_term3

/-- Quantum (D=6, observed) positive raw_S. Python oracle: raw_S ≈ +0.955506. -/
theorem quantum_raw_S_positive :
    raw_S (get_domain_params "quantum") > 0 := by
  have h_obs : (get_domain_params "quantum").observed = true := by simp [get_domain_params]
  have h_delta : (0.35 : ℝ) ≤ (get_domain_params "quantum").delta_psi ∧
      (get_domain_params "quantum").delta_psi ≤ (1.3 : ℝ) := by
    simp [get_domain_params]; constructor <;> norm_num
  have h_dp : (0.7 : ℝ) ≤ (get_domain_params "quantum").delta_psi := by
    simp [get_domain_params]; norm_num
  have hN : (0 : ℝ) < (get_domain_params "quantum").N := by simp [get_domain_params]
  have hP : (0 : ℝ) < (get_domain_params "quantum").P := by simp [get_domain_params]
  have hD : (6 : ℝ) ≤ (get_domain_params "quantum").D_eff := by simp [get_domain_params]
  have h_term1 := domain_term1_positive_of_params (get_domain_params "quantum")
    h_obs h_delta h_dp hN hP hD
  have h_term3 : abs (term3 (get_domain_params "quantum")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "quantum") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "quantum")
    (domain_term2_eq_one "quantum") (lt_trans (by norm_num) h_term1) h_term3

/-- Particle (D=7, observed) positive raw_S. Python oracle: raw_S ≈ +0.735824. -/
theorem particle_raw_S_positive :
    raw_S (get_domain_params "particle") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "particle") := by
    refine domain_term1_positive_of_params (get_domain_params "particle") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "particle")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "particle") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "particle")
    (domain_term2_eq_one "particle") (lt_trans (by norm_num) h_term1) h_term3

/-- CMB (D=24, no observer) negative raw_S.
    Python oracle: raw_S ≈ −0.424412. -/
theorem cmb_raw_S_negative :
    raw_S (get_domain_params "cmb") < 0 := by
  set p := get_domain_params "cmb"
  have h_term1_neg := cmb_term1_negative
  exact raw_S_negative_of_term1_overcomes_term3 p (domain_term2_eq_one "cmb")
    h_term1_neg domain_cmb_term1_overcomes_term3

/-- Chemical (D=9, observed) positive raw_S.
    Python oracle: raw_S ≈ +0.334573. -/
theorem chemical_raw_S_positive :
    raw_S (get_domain_params "chemical") > 0 := by
  have h_term3 : abs (term3 (get_domain_params "chemical")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "chemical") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "chemical")
    (domain_term2_eq_one "chemical") domain_term1_gt_neg_08_chemical h_term3

/-- Electron (D=8, observed) positive raw_S. Python oracle: raw_S ≈ +0.407884. -/
theorem electron_raw_S_positive :
    raw_S (get_domain_params "electron") > 0 := by
  have h_term3 : abs (term3 (get_domain_params "electron")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "electron") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "electron")
    (domain_term2_eq_one "electron") domain_term1_gt_neg_08_electron h_term3

/-- Astronomical (D=20, observed) positive raw_S. Python oracle: raw_S ≈ +0.898460. -/
theorem astronomical_raw_S_positive :
    raw_S (get_domain_params "astronomical") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "astronomical") := by
    refine domain_term1_positive_of_params (get_domain_params "astronomical") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "astronomical")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "astronomical") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "astronomical")
    (domain_term2_eq_one "astronomical") (lt_trans (by norm_num) h_term1) h_term3

theorem higgs_raw_S_positive :
    raw_S (get_domain_params "higgs") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "higgs") := by
    refine domain_term1_positive_of_params (get_domain_params "higgs") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "higgs")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "higgs") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "higgs")
    (domain_term2_eq_one "higgs") (lt_trans (by norm_num) h_term1) h_term3

theorem galactic_raw_S_positive :
    raw_S (get_domain_params "galactic") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "galactic") := by
    refine domain_term1_positive_of_params (get_domain_params "galactic") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "galactic")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "galactic") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "galactic")
    (domain_term2_eq_one "galactic") (lt_trans (by norm_num) h_term1) h_term3

theorem fusion_raw_S_positive :
    raw_S (get_domain_params "fusion") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "fusion") := by
    refine domain_term1_positive_of_params (get_domain_params "fusion") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "fusion")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "fusion") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "fusion")
    (domain_term2_eq_one "fusion") (lt_trans (by norm_num) h_term1) h_term3

theorem proton_raw_S_positive :
    raw_S (get_domain_params "proton") > 0 := by
  have h_obs : (get_domain_params "proton").observed = true := by simp [get_domain_params]
  have h_delta : (0.35 : ℝ) ≤ (get_domain_params "proton").delta_psi ∧
      (get_domain_params "proton").delta_psi ≤ (1.3 : ℝ) := by
    simp [get_domain_params]; constructor <;> norm_num
  have h_dp : (0.7 : ℝ) ≤ (get_domain_params "proton").delta_psi := by simp [get_domain_params]
  have hN : (0 : ℝ) < (get_domain_params "proton").N := by simp [get_domain_params]
  have hP : (0 : ℝ) < (get_domain_params "proton").P := by simp [get_domain_params]
  have hD : (6 : ℝ) ≤ (get_domain_params "proton").D_eff := by simp [get_domain_params]; norm_num
  have h_term1 := domain_term1_positive_of_params (get_domain_params "proton")
    h_obs h_delta h_dp hN hP hD
  have h_term3 : abs (term3 (get_domain_params "proton")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "proton") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "proton")
    (domain_term2_eq_one "proton") (lt_trans (by norm_num) h_term1) h_term3

theorem medical_raw_S_positive :
    raw_S (get_domain_params "medical") > 0 := by
  have h_term3 : abs (term3 (get_domain_params "medical")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "medical") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "medical")
    (domain_term2_eq_one "medical") domain_term1_gt_neg_08_medical h_term3

theorem blackhole_raw_S_positive :
    raw_S (get_domain_params "blackhole") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "blackhole") := by
    refine domain_term1_positive_of_params (get_domain_params "blackhole") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "blackhole")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "blackhole") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "blackhole")
    (domain_term2_eq_one "blackhole") (lt_trans (by norm_num) h_term1) h_term3

theorem consciousness_raw_S_positive :
    raw_S (get_domain_params "consciousness") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "consciousness") := by
    refine domain_term1_positive_of_params (get_domain_params "consciousness") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "consciousness")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "consciousness") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "consciousness")
    (domain_term2_eq_one "consciousness") (lt_trans (by norm_num) h_term1) h_term3

/-- Molecular chemistry (D=9, δψ=0.4) positive raw_S — SMILES crosswalk. -/
theorem molecular_raw_S_positive :
    raw_S (get_domain_params "molecular") > 0 := by
  have h_term3 : abs (term3 (get_domain_params "molecular")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "molecular") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "molecular")
    (domain_term2_eq_one "molecular") domain_term1_gt_neg_08_molecular h_term3

/-- Materials science (D=10, δψ=0.5) positive raw_S — SMILES crosswalk. -/
theorem material_raw_S_positive :
    raw_S (get_domain_params "material") > 0 := by
  have h_term3 : abs (term3 (get_domain_params "material")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "material") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "material")
    (domain_term2_eq_one "material") domain_term1_gt_neg_08_material h_term3

/-- Biology (D=12, unobserved) positive raw_S — low-δψ dispersal regime. -/
theorem biological_raw_S_positive :
    raw_S (get_domain_params "biological") > 0 := by
  have h_term1 := domain_term1_positive_biological
  have h_term3 : abs (term3 (get_domain_params "biological")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "biological") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "biological")
    (domain_term2_eq_one "biological") (lt_trans (by norm_num) h_term1) h_term3

/-- Cellular biology (D=12, δψ=0.08) positive raw_S — Soul Simulator / evolution crosswalk. -/
theorem cellular_params_eq_biological :
    get_domain_params "cellular" = get_domain_params "biological" := by
  simp [get_domain_params, FSOTParams]

theorem cellular_raw_S_positive :
    raw_S (get_domain_params "cellular") > 0 := by
  rw [cellular_params_eq_biological]
  exact biological_raw_S_positive

/-- Nuclear physics (D=15, observed) positive raw_S — SMILES §42/§64 crosswalk. -/
theorem nuclear_raw_S_positive :
    raw_S (get_domain_params "nuclear") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "nuclear") := by
    refine domain_term1_positive_of_params (get_domain_params "nuclear") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "nuclear")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "nuclear") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "nuclear")
    (domain_term2_eq_one "nuclear") (lt_trans (by norm_num) h_term1) h_term3

/-- Energy / thermodynamics (D=15, observed) positive raw_S. -/
theorem energy_raw_S_positive :
    raw_S (get_domain_params "energy") > 0 := by
  have h_term1 : (0 : ℝ) < term1 (get_domain_params "energy") := by
    refine domain_term1_positive_of_params (get_domain_params "energy") ?_ ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]; norm_num
  have h_term3 : abs (term3 (get_domain_params "energy")) < (0.2 : ℝ) := by
    refine term3_abs_lt_fifth_default (get_domain_params "energy") ?_ ?_ ?_ ?_ ?_
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]; constructor <;> norm_num
    · simp [get_domain_params]
    · simp [get_domain_params]
    · simp [get_domain_params]
  exact raw_S_positive_of_term1_gt_neg_08 (get_domain_params "energy")
    (domain_term2_eq_one "energy") (lt_trans (by norm_num) h_term1) h_term3

end

end FSOT.Formal