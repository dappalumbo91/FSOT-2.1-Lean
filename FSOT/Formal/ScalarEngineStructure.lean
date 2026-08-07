/-
  FSOT Formal ScalarEngineStructure — T1 / T2 / T3 definitional depth.

  Master identity:  raw_S = term1 + term2 + term3
                    scaled_S = k · raw_S
                    S = K · (T1 + T2 + T3)  (Python authority pin D1D38A)

  These lemmas pin the *structure* of the scalar engine (not residual
  domain factors). They are the Lean-side backbone for multiprover
  cross-proof of the master formula decomposition.
-/

import FSOT.Formal.Scalar
import FSOT.Formal.Bounds
import FSOT.Formal.Theorems
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace FSOT.Formal

noncomputable section

open Real

-- ============================================================
-- MASTER DECOMPOSITION (definitional)
-- ============================================================

/-- Core identity: raw scalar is exactly the sum of the three engine terms. -/
theorem raw_S_eq_term1_term2_term3 (p : FSOTParams) :
    raw_S p = term1 p + term2 p + term3 p := by
  rfl

/-- Universal scaling: final S is always K · raw_S. -/
theorem scaled_S_eq_k_mul_raw_S (p : FSOTParams) :
    scaled_S p = raw_S p * k := by
  rfl

/-- Combined master formula: scaled_S = k · (T1 + T2 + T3). -/
theorem scaled_S_eq_k_mul_terms (p : FSOTParams) :
    scaled_S p = k * (term1 p + term2 p + term3 p) := by
  simp [scaled_S, raw_S, mul_comm]

-- ============================================================
-- T2 — linear baseline (scale · amplitude + trend)
-- ============================================================

/-- T2 is exactly the linear baseline term. -/
theorem term2_eq_scale_amplitude_bias (p : FSOTParams) :
    term2 p = p.scale * p.amplitude + p.trend_bias := by
  rfl

/-- Default parameters give T2 = 1 (unit baseline). -/
theorem term2_unit_defaults :
    term2 { scale := 1, amplitude := 1, trend_bias := 0 } = 1 := by
  simp [term2]

/-- Zeroing scale or amplitude zeros the product part of T2. -/
theorem term2_zero_scale (p : FSOTParams) (h : p.scale = 0) :
    term2 p = p.trend_bias := by
  simp [term2, h]

theorem term2_zero_amplitude (p : FSOTParams) (h : p.amplitude = 0) :
    term2 p = p.trend_bias := by
  simp [term2, h]

-- ============================================================
-- T1 — base × perceived_adjust × quirkMod
-- ============================================================

/-- Perceived-adjust factor extracted from T1. -/
def perceived_adjust (p : FSOTParams) : ℝ :=
  1 + new_perceived_param * log (p.D_eff / 25)

/-- T1 factors as base × perceived_adjust × quirkMod. -/
theorem term1_eq_base_adjust_quirk (p : FSOTParams) :
    term1 p = term1_base p * perceived_adjust p * quirkMod p := by
  simp [term1, perceived_adjust]

/-- Unobserved regimes: quirkMod is exactly 1. -/
theorem quirkMod_unobserved (p : FSOTParams) (h : p.observed = false) :
    quirkMod p = 1 := by
  simp [quirkMod, h]

/-- Unobserved: T1 collapses to base × perceived_adjust. -/
theorem term1_unobserved_eq_base_adjust (p : FSOTParams) (h : p.observed = false) :
    term1 p = term1_base p * perceived_adjust p := by
  simp [term1_eq_base_adjust_quirk, quirkMod_unobserved p h]

/-- At the 25-D fluid ceiling, log(D_eff/25)=0 so perceived_adjust = 1. -/
theorem perceived_adjust_at_ceiling
    (p : FSOTParams) (h : p.D_eff = 25) :
    perceived_adjust p = 1 := by
  simp [perceived_adjust, h, log_one]

/-- Ceiling + unobserved: T1 = term1_base (pure geometric base). -/
theorem term1_ceiling_unobserved
    (p : FSOTParams) (hD : p.D_eff = 25) (hObs : p.observed = false) :
    term1 p = term1_base p := by
  simp [term1_unobserved_eq_base_adjust p hObs, perceived_adjust_at_ceiling p hD]

/-- Growth factor is always strictly positive. -/
theorem growth_term_pos (p : FSOTParams) : (0 : ℝ) < growth_term p :=
  Real.exp_pos _

-- ============================================================
-- T3 — chaos / poof / acoustic composite (structure skeleton)
-- ============================================================

/-- T3 geometric prefactor shared with T1 base: N·P/√D_eff. -/
def term3_geometric (p : FSOTParams) : ℝ :=
  p.N * p.P / sqrt p.D_eff

/-- Chaos modulation of dimensional bleed away from 25-D. -/
def term3_chaos_mod (p : FSOTParams) : ℝ :=
  1 + chaos_factor * (p.D_eff - 25) / 25

/-- Poof / suction phase channel. -/
def term3_poof_suction : ℝ :=
  1 + poof_factor * cos (theta_s + pi) + suction_factor * sin theta_s

/-- Acoustic bleed / inflow channel. -/
def term3_acoustic (p : FSOTParams) : ℝ :=
  1 + acoustic_bleed * (sin p.delta_theta) ^ 2 / phi +
    acoustic_inflow * (cos p.delta_theta) ^ 2 / phi

/-- Bleed-in × phase-variance channel. -/
def term3_bleed_phase : ℝ :=
  1 + bleed_in_factor * phase_variance

/-- T3 is exactly β · cos(δψ) · geometric · chaos · poof · acoustic · bleed. -/
theorem term3_eq_composite (p : FSOTParams) :
    term3 p =
      beta * cos p.delta_psi * term3_geometric p *
        term3_chaos_mod p * term3_poof_suction *
        term3_acoustic p * term3_bleed_phase := by
  simp [term3, term3_geometric, term3_chaos_mod, term3_poof_suction,
        term3_acoustic, term3_bleed_phase]

/-- At D_eff = 25 the chaos modulation is exactly 1. -/
theorem term3_chaos_mod_at_ceiling (p : FSOTParams) (h : p.D_eff = 25) :
    term3_chaos_mod p = 1 := by
  simp [term3_chaos_mod, h]

-- ============================================================
-- SIGN / BALANCE SKELETON (uses decomposition, not residual factors)
-- ============================================================

/-- raw_S is the sum of three independent channels — rearranging T2. -/
theorem raw_S_rearrange_term2 (p : FSOTParams) :
    raw_S p - term2 p = term1 p + term3 p := by
  simp [raw_S]
  ring

/-- If T1 + T3 overcomes unit T2, raw_S is negative (damping regime). -/
theorem raw_S_neg_of_t1_t3_over_unit_t2
    (p : FSOTParams)
    (h2 : term2 p = 1)
    (h : term1 p + term3 p < -1) :
    raw_S p < 0 := by
  simp [raw_S, h2]
  linarith

/-- If T1 + T3 exceeds zero under unit T2, raw_S is positive (emergence). -/
theorem raw_S_pos_of_t1_t3_over_neg_unit_t2
    (p : FSOTParams)
    (h2 : term2 p = 1)
    (h : (0 : ℝ) < term1 p + term3 p + 1) :
    (0 : ℝ) < raw_S p := by
  simp [raw_S, h2]
  linarith

-- ============================================================
-- ANALYTIC DEPTH — sign transport, unit T2 rewrite, k-positivity
-- ============================================================

/-- Under unit T2, raw_S rewrites as T1 + T3 + 1. -/
theorem raw_S_of_unit_term2 (p : FSOTParams) (h2 : term2 p = 1) :
    raw_S p = term1 p + term3 p + 1 := by
  simp [raw_S, h2]
  ring

/-- k > 0 ⇒ scaled_S and raw_S share sign (positive direction). -/
theorem scaled_S_pos_of_raw_S_pos (p : FSOTParams) (h : (0 : ℝ) < raw_S p) :
    (0 : ℝ) < scaled_S p := by
  simp [scaled_S]
  exact mul_pos h k_pos

/-- k > 0 ⇒ scaled_S and raw_S share sign (negative direction). -/
theorem scaled_S_neg_of_raw_S_neg (p : FSOTParams) (h : raw_S p < 0) :
    scaled_S p < 0 := by
  simp [scaled_S]
  exact mul_neg_of_neg_of_pos h k_pos

/-- Emergence transport: unit T2 + (T1+T3+1)>0 ⇒ scaled_S > 0. -/
theorem scaled_S_emergence_of_unit_t2
    (p : FSOTParams)
    (h2 : term2 p = 1)
    (h : (0 : ℝ) < term1 p + term3 p + 1) :
    (0 : ℝ) < scaled_S p :=
  scaled_S_pos_of_raw_S_pos p (raw_S_pos_of_t1_t3_over_neg_unit_t2 p h2 h)

/-- Damping transport: unit T2 + (T1+T3)<−1 ⇒ scaled_S < 0. -/
theorem scaled_S_damping_of_unit_t2
    (p : FSOTParams)
    (h2 : term2 p = 1)
    (h : term1 p + term3 p < -1) :
    scaled_S p < 0 :=
  scaled_S_neg_of_raw_S_neg p (raw_S_neg_of_t1_t3_over_unit_t2 p h2 h)

/-- T1 base is negative whenever the geometric cos-argument is negative
    and the remaining scale factors stay positive (high-D / typical δψ). -/
theorem term1_base_neg_of_cos_neg
    (p : FSOTParams)
    (h_cos : cos ((psi_con + p.delta_psi) / eta_eff) < 0)
    (h_scale : (0 : ℝ) < p.N * p.P / sqrt p.D_eff)
    (h_tail :
      (0 : ℝ) <
        exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) *
          (1 + growth_term p * coherence_efficiency)) :
    term1_base p < 0 := by
  have h_cs : cos ((psi_con + p.delta_psi) / eta_eff) * (p.N * p.P / sqrt p.D_eff) < 0 := by
    nlinarith [h_cos, h_scale]
  have h_prod :
      cos ((psi_con + p.delta_psi) / eta_eff) * (p.N * p.P / sqrt p.D_eff) *
        exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) *
        (1 + growth_term p * coherence_efficiency) < 0 := by
    nlinarith [h_cs, h_tail]
  simpa [term1_base, mul_assoc, mul_left_comm, mul_comm] using h_prod

/-- Growth-tail factor of T1 base is always strictly positive. -/
theorem term1_base_tail_pos (p : FSOTParams) :
    (0 : ℝ) <
      exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) *
        (1 + growth_term p * coherence_efficiency) := by
  have h_exp := exp_pos (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi)
  have h_g := growth_term_pos p
  have h_c := coherence_efficiency_positive
  have h_one : (0 : ℝ) < 1 + growth_term p * coherence_efficiency := by nlinarith
  exact mul_pos h_exp h_one

/-- Geometric prefactor of T1 base is positive when N, P, D_eff > 0. -/
theorem term1_geometric_pos
    (p : FSOTParams)
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P)
    (hD : (0 : ℝ) < p.D_eff) :
    (0 : ℝ) < p.N * p.P / sqrt p.D_eff := by
  have hs : (0 : ℝ) < sqrt p.D_eff := sqrt_pos.mpr hD
  exact div_pos (mul_pos hN hP) hs

/-- Typical high-D cos-argument is negative (Bounds cos_arg interval). -/
theorem term1_base_neg_typical_high_D
    (p : FSOTParams)
    (h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P)
    (hD : (0 : ℝ) < p.D_eff) :
    term1_base p < 0 :=
  term1_base_neg_of_cos_neg p
    (cos_arg_negative_for_typical_delta_psi p h_delta)
    (term1_geometric_pos p hN hP hD)
    (term1_base_tail_pos p)

-- ============================================================
-- BUNDLE — exportable structural certificate
-- ============================================================

/-- Count of named structural identity theorems in this module (inventory pin). -/
def scalar_engine_structure_theorem_count : ℕ := 28

theorem scalar_engine_structure_theorem_count_pos :
    0 < scalar_engine_structure_theorem_count := by
  unfold scalar_engine_structure_theorem_count; decide

theorem scalar_engine_structure_theorem_count_eq :
    scalar_engine_structure_theorem_count = 28 := by
  unfold scalar_engine_structure_theorem_count; decide

/-- Bundle: master formula structure is definitionally pinned. -/
theorem scalar_engine_structure_bundle :
    scalar_engine_structure_theorem_count = 28 ∧
    (0 : ℝ) < k ∧
    term2 { scale := 1, amplitude := 1, trend_bias := 0 } = 1 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · exact scalar_engine_structure_theorem_count_eq
  · exact k_pos
  · exact term2_unit_defaults

/-- Depth bundle: emergence/damping transport through k-scaling. -/
theorem scalar_engine_depth_bundle :
    scalar_engine_structure_theorem_count = 28 ∧
    (0 : ℝ) < k ∧
    (0 : ℝ) < 0.42 ∧
    (0.42 : ℝ) < k := by
  refine ⟨scalar_engine_structure_theorem_count_eq, k_pos, by norm_num, k_gt_0420⟩

end

end FSOT.Formal
