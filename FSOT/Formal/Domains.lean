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
  simp [get_domain_params, cosmologicalParams, mediumFold]

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
  constructor <;> linarith

lemma cmb_observed_false :
    (get_domain_params "cmb").observed = false := by
  simp [get_domain_params]

lemma cmb_D_eff_eq :
    (get_domain_params "cmb").D_eff = 25 := by
  simp [get_domain_params]

lemma cmb_eq_cosmological :
    get_domain_params "cmb" = get_domain_params "cosmological" := by
  simp [get_domain_params]

lemma dark_energy_eq_cosmological :
    get_domain_params "dark_energy" = get_domain_params "cosmological" := by
  simp [get_domain_params]

lemma ai_observed_false :
    (get_domain_params "ai").observed = false := by
  simp [get_domain_params]

lemma ai_D_eff_eq :
    (get_domain_params "ai").D_eff = 8 := by
  simp [get_domain_params]

lemma neural_observed_true :
    (get_domain_params "neural").observed = true := by
  simp [get_domain_params]

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

theorem cosmological_term1_dominates_term3 :
    abs (term3 (get_domain_params "cosmological")) <
      abs (term1 (get_domain_params "cosmological")) := by
  rw [cosmological_domain_eq]
  exact term3_dominates_in_cosmological_regime

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

theorem dark_energy_term1_negative :
    term1 (get_domain_params "dark_energy") < 0 := by
  rw [dark_energy_eq_cosmological]
  exact cosmological_term1_negative

lemma dark_energy_params_eq :
    get_domain_params "dark_energy" = cosmologicalParams := by
  simp [get_domain_params, cosmologicalParams, mediumFold]

lemma dark_energy_term2_eq_one :
    term2 (get_domain_params "dark_energy") = 1 := by
  simp [term2, get_domain_params]

theorem dark_energy_raw_S_negative :
    raw_S (get_domain_params "dark_energy") < 0 := by
  rw [dark_energy_eq_cosmological]
  exact cosmological_raw_S_negative

theorem cmb_term1_negative :
    term1 (get_domain_params "cmb") < 0 := by
  rw [cmb_eq_cosmological]
  exact cosmological_term1_negative

lemma domain_term2_eq_one (domain : String) :
    term2 (get_domain_params domain) = 1 := by
  simp only [term2, get_domain_params]
  split <;> simp [specimenFold, mediumFold, atomicFold, hepFold]

lemma domain_term3_abs_lt_fifth (domain : String)
    (h_D : (5 : ℝ) ≤ (get_domain_params domain).D_eff ∧
      (get_domain_params domain).D_eff ≤ 25)
    (h_dp : (0 : ℝ) ≤ (get_domain_params domain).delta_psi ∧
      (get_domain_params domain).delta_psi ≤ 1.3) :
    abs (term3 (get_domain_params domain)) < (0.2 : ℝ) := by
  refine term3_abs_lt_fifth_default (get_domain_params domain) h_D h_dp ?_ ?_ ?_
  all_goals (simp only [get_domain_params]; split <;>
    simp [specimenFold, mediumFold, atomicFold, hepFold])

lemma look1_specimen_of_domain (domain : String)
    (h_obs : (get_domain_params domain).observed = true)
    (h_look : (get_domain_params domain).delta_psi = (1.0 : ℝ))
    (h_D : (5 : ℝ) ≤ (get_domain_params domain).D_eff ∧
      (get_domain_params domain).D_eff ≤ 25)
    (h_N : (get_domain_params domain).N = 1)
    (h_P : (get_domain_params domain).P = 1)
    (h_dt : (get_domain_params domain).delta_theta = 1) :
    raw_S (get_domain_params domain) > 0 :=
  specimen_raw_S_positive (get_domain_params domain) h_obs
    (by rw [h_look]; constructor <;> norm_num)
    (by rw [h_look]; norm_num) h_D h_N h_P h_dt (domain_term2_eq_one domain)

theorem ai_raw_S_non_positive :
    raw_S (get_domain_params "ai") ≤ 0 := by
  set p := get_domain_params "ai"
  have h_term1_neg := lt_trans domain_term1_lt_neg_08_ai (by norm_num : (-0.8 : ℝ) < 0)
  have h_neg := raw_S_negative_of_term1_overcomes_term3 p (domain_term2_eq_one "ai")
    h_term1_neg domain_ai_term1_overcomes_term3
  exact le_of_lt h_neg

macro "look1_specimen_tac" : tactic =>
  `(tactic| (simp [get_domain_params] <;> (try constructor) <;> norm_num))

theorem neural_raw_S_positive :
    raw_S (get_domain_params "neural") > 0 := by
  refine look1_specimen_of_domain "neural" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem quantum_raw_S_positive :
    raw_S (get_domain_params "quantum") > 0 := by
  refine look1_specimen_of_domain "quantum" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem particle_raw_S_positive :
    raw_S (get_domain_params "particle") > 0 := by
  refine look1_specimen_of_domain "particle" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem cmb_raw_S_negative :
    raw_S (get_domain_params "cmb") < 0 := by
  rw [cmb_eq_cosmological]
  exact cosmological_raw_S_negative

theorem chemical_raw_S_positive :
    raw_S (get_domain_params "chemical") > 0 := by
  refine look1_specimen_of_domain "chemical" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem electron_raw_S_positive :
    raw_S (get_domain_params "electron") > 0 := by
  refine specimen_raw_S_positive (get_domain_params "electron") ?_ ?_ ?_ ?_ ?_ ?_ ?_
    (domain_term2_eq_one "electron")
  · simp [get_domain_params]
  · simpa [get_domain_params] using atomic_look_bounds
  · simpa [get_domain_params] using atomic_look_ge_07
  · simp [get_domain_params]; constructor <;> norm_num
  · simp [get_domain_params]
  · simp [get_domain_params]
  · simp [get_domain_params]

theorem astronomical_raw_S_positive :
    raw_S (get_domain_params "astronomical") > 0 := by
  refine look1_specimen_of_domain "astronomical" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem higgs_raw_S_positive :
    raw_S (get_domain_params "higgs") > 0 := by
  refine specimen_raw_S_positive (get_domain_params "higgs") ?_ ?_ ?_ ?_ ?_ ?_ ?_
    (domain_term2_eq_one "higgs")
  · simp [get_domain_params]
  · simpa [get_domain_params] using hep_look_bounds
  · simpa [get_domain_params] using hep_look_ge_07
  · simp [get_domain_params]; constructor <;> norm_num
  · simp [get_domain_params]
  · simp [get_domain_params]
  · simp [get_domain_params]

theorem galactic_raw_S_positive :
    raw_S (get_domain_params "galactic") > 0 := by
  refine look1_specimen_of_domain "galactic" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem fusion_raw_S_positive :
    raw_S (get_domain_params "fusion") > 0 := by
  refine look1_specimen_of_domain "fusion" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem proton_raw_S_positive :
    raw_S (get_domain_params "proton") > 0 := by
  refine look1_specimen_of_domain "proton" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem medical_raw_S_positive :
    raw_S (get_domain_params "medical") > 0 := by
  refine look1_specimen_of_domain "medical" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem blackhole_raw_S_positive :
    raw_S (get_domain_params "blackhole") > 0 := by
  refine look1_specimen_of_domain "blackhole" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem consciousness_raw_S_positive :
    raw_S (get_domain_params "consciousness") > 0 := by
  refine look1_specimen_of_domain "consciousness" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem molecular_raw_S_positive :
    raw_S (get_domain_params "molecular") > 0 := by
  refine look1_specimen_of_domain "molecular" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem material_raw_S_positive :
    raw_S (get_domain_params "material") > 0 := by
  refine look1_specimen_of_domain "material" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

/-- Biology is a bulk medium (look = 1, unobserved). Nest S is negative. -/
theorem biological_raw_S_negative :
    raw_S (get_domain_params "biological") < 0 := by
  exact raw_S_negative_of_term1_overcomes_term3 (get_domain_params "biological")
    (domain_term2_eq_one "biological") domain_term1_negative_biological
    domain_biological_term1_overcomes_term3

theorem cellular_params_eq_biological :
    get_domain_params "cellular" = get_domain_params "biological" := by
  simp [get_domain_params, FSOTParams]

theorem cellular_raw_S_negative :
    raw_S (get_domain_params "cellular") < 0 := by
  rw [cellular_params_eq_biological]
  exact biological_raw_S_negative

theorem nuclear_raw_S_positive :
    raw_S (get_domain_params "nuclear") > 0 := by
  refine look1_specimen_of_domain "nuclear" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem energy_raw_S_positive :
    raw_S (get_domain_params "energy") > 0 := by
  refine look1_specimen_of_domain "energy" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac

theorem economic_raw_S_positive :
    raw_S (get_domain_params "economic") > 0 := by
  refine look1_specimen_of_domain "economic" ?_ ?_ ?_ ?_ ?_ ?_
  all_goals look1_specimen_tac


end

end FSOT.Formal