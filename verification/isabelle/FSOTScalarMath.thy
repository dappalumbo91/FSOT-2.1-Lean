(*
  FSOT Isabelle mathematical core — NOT literal-only obligation replay.

  Mirrors Lean `FSOT.Formal.Scalar` and Python `vendor/fsot_compute.py` seed arithmetic.
  Goal: Isabelle checks the *scalar engine math* (definitions + identities + sign/pos
  lemmas), not only domain-bundle bookkeeping.

  Seeds: π, e = exp 1, φ = (1+√5)/2, γ (Euler–Mascheroni), G (Catalan).
  Engine: raw_S = term1 + term2 + term3 ; scaled_S = k * raw_S.
*)
theory FSOTScalarMath
  imports Complex_Main "HOL-Decision_Procs.Approximation"
begin

section ‹Foundational seeds›

definition phi :: real where
  "phi = (1 + sqrt 5) / 2"

definition e_fsot :: real where
  "e_fsot = exp 1"

definition gamma_euler :: real where
  "gamma_euler = 0.57721566490153286060651209008240243"

definition catalan_G :: real where
  "catalan_G = 0.91596559417721901505460351493238411"

section ‹Layer-1 derived constants (seed arithmetic)›

definition alpha_fsot :: real where
  "alpha_fsot = ln pi / (e_fsot * phi ^ 13)"

definition psi_con :: real where
  "psi_con = 1 - exp (-1)"

definition eta_eff :: real where
  "eta_eff = 1 / (pi - 1)"

definition beta_fsot :: real where
  "beta_fsot = 1 / exp (pi powr pi + (e_fsot - 1))"

definition gamma_c :: real where
  "gamma_c = - ln 2 / phi"

definition omega_fsot :: real where
  "omega_fsot = sin (pi / e_fsot) * sqrt 2"

definition theta_s :: real where
  "theta_s = sin (psi_con * eta_eff)"

definition poof_factor :: real where
  "poof_factor = exp (- (ln pi / e_fsot) / (eta_eff * ln phi))"

section ‹Layer-2 composite constants›

definition acoustic_bleed :: real where
  "acoustic_bleed = sin (pi / e_fsot) * phi / sqrt 2"

definition phase_variance :: real where
  "phase_variance = - cos (theta_s + pi)"

definition coherence_efficiency :: real where
  "coherence_efficiency =
     (1 - poof_factor * sin theta_s) * (1 + 0.01 * catalan_G / (pi * phi))"

definition bleed_in_factor :: real where
  "bleed_in_factor = coherence_efficiency * (1 - sin theta_s / phi)"

definition acoustic_inflow :: real where
  "acoustic_inflow = acoustic_bleed * (1 + cos theta_s / phi)"

definition suction_factor :: real where
  "suction_factor = poof_factor * (- cos (theta_s - pi))"

definition chaos_factor :: real where
  "chaos_factor = gamma_c / omega_fsot"

definition new_perceived_param :: real where
  "new_perceived_param = (gamma_euler / e_fsot) * sqrt 2"

definition consciousness_factor :: real where
  "consciousness_factor = coherence_efficiency * new_perceived_param"

definition k_fsot :: real where
  "k_fsot = phi * (gamma_euler / e_fsot) * sqrt 2 / ln pi * (99 / 100)"

section ‹Domain / evaluation parameters›

record fsot_params =
  N :: real
  P :: real
  D_eff :: real
  recent_hits :: real
  delta_psi :: real
  delta_theta :: real
  rho :: real
  scale :: real
  amplitude :: real
  trend_bias :: real
  observed :: bool

definition default_params :: fsot_params where
  "default_params =
    ⦇ N = 1, P = 1, D_eff = 25, recent_hits = 0, delta_psi = 1, delta_theta = 1,
      rho = 1, scale = 1, amplitude = 1, trend_bias = 0, observed = False ⦈"

definition get_domain_params :: "string ⇒ fsot_params" where
  "get_domain_params d =
    (if d = ''quantum'' then default_params ⦇ D_eff := 6, delta_psi := 1, observed := True ⦈
     else if d = ''particle'' then default_params ⦇ D_eff := 7, delta_psi := 0.85, observed := True ⦈
     else if d = ''proton'' then default_params ⦇ D_eff := 8, delta_psi := 0.7, observed := True ⦈
     else if d = ''biological'' then default_params ⦇ D_eff := 12, delta_psi := 0.08, observed := False ⦈
     else if d = ''medical'' then default_params ⦇ D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := True ⦈
     else if d = ''neural'' then default_params ⦇ D_eff := 14, recent_hits := 1, delta_psi := 0.70, observed := True ⦈
     else if d = ''astronomical'' then default_params ⦇ D_eff := 20, recent_hits := 1, delta_psi := 1, observed := True ⦈
     else if d = ''cosmological'' then default_params ⦇ D_eff := 25, delta_psi := 1, observed := False ⦈
     else if d = ''cmb'' then default_params ⦇ D_eff := 24, delta_psi := 0.8, observed := False ⦈
     else if d = ''blackhole'' then default_params ⦇ D_eff := 23, recent_hits := 2, delta_psi := 1.25, observed := True ⦈
     else if d = ''consciousness'' then default_params ⦇ D_eff := 16, recent_hits := 1, delta_psi := 1.15, observed := True ⦈
     else default_params)"

section ‹Scalar engine — the heartbeat›

definition growth_term :: "fsot_params ⇒ real" where
  "growth_term p =
     exp (alpha_fsot * (1 - recent_hits p / N p) * gamma_euler / phi)"

definition quirk_mod :: "fsot_params ⇒ real" where
  "quirk_mod p =
     (if observed p then
        exp (consciousness_factor * phase_variance) * cos (delta_psi p + phase_variance)
      else 1)"

definition term1_base :: "fsot_params ⇒ real" where
  "term1_base p =
     (N p * P p / sqrt (D_eff p)) *
     cos ((psi_con + delta_psi p) / eta_eff) *
     exp (- alpha_fsot * recent_hits p / N p + rho p + bleed_in_factor * delta_psi p) *
     (1 + growth_term p * coherence_efficiency)"

definition perceived_adjust :: "fsot_params ⇒ real" where
  "perceived_adjust p = 1 + new_perceived_param * ln (D_eff p / 25)"

definition term1 :: "fsot_params ⇒ real" where
  "term1 p = term1_base p * perceived_adjust p * quirk_mod p"

definition term2 :: "fsot_params ⇒ real" where
  "term2 p = scale p * amplitude p + trend_bias p"

definition term3 :: "fsot_params ⇒ real" where
  "term3 p =
     beta_fsot * cos (delta_psi p) * (N p * P p / sqrt (D_eff p)) *
     (1 + chaos_factor * (D_eff p - 25) / 25) *
     (1 + poof_factor * cos (theta_s + pi) + suction_factor * sin theta_s) *
     (1 + acoustic_bleed * (sin (delta_theta p))\<^sup>2 / phi +
          acoustic_inflow * (cos (delta_theta p))\<^sup>2 / phi) *
     (1 + bleed_in_factor * phase_variance)"

definition raw_S :: "fsot_params ⇒ real" where
  "raw_S p = term1 p + term2 p + term3 p"

definition scaled_S :: "fsot_params ⇒ real" where
  "scaled_S p = raw_S p * k_fsot"

section ‹Core mathematical identities (proved)›

lemma raw_S_decomposition:
  "raw_S p = term1 p + term2 p + term3 p"
  by (simp add: raw_S_def)

lemma scaled_S_factorization:
  "scaled_S p = k_fsot * (term1 p + term2 p + term3 p)"
  by (simp add: scaled_S_def raw_S_def)

lemma term1_factorization:
  "term1 p = term1_base p * perceived_adjust p * quirk_mod p"
  by (simp add: term1_def)

lemma raw_S_with_perceived:
  "raw_S p = term1_base p * perceived_adjust p * quirk_mod p + term2 p + term3 p"
  by (simp add: raw_S_def term1_def)

lemma quirk_mod_unobserved:
  "¬ observed p ⟹ quirk_mod p = 1"
  by (simp add: quirk_mod_def)

lemma growth_term_pos:
  "0 < growth_term p"
  by (simp add: growth_term_def)

lemma e_fsot_pos: "0 < e_fsot"
  by (simp add: e_fsot_def)

lemma e_fsot_eq_exp1: "e_fsot = exp 1"
  by (simp add: e_fsot_def)

lemma psi_con_eq: "psi_con = 1 - exp (-1)"
  by (simp add: psi_con_def)

lemma poof_factor_pos: "0 < poof_factor"
  by (simp add: poof_factor_def)

lemma beta_fsot_pos: "0 < beta_fsot"
  by (simp add: beta_fsot_def)

lemma gamma_euler_pos: "0 < gamma_euler"
  unfolding gamma_euler_def by simp

lemma catalan_G_pos: "0 < catalan_G"
  unfolding catalan_G_def by simp

lemma phi_gt_one: "1 < phi"
proof -
  have "sqrt 4 < sqrt 5"
    by (rule real_sqrt_less_mono) simp
  hence "2 < sqrt 5" by simp
  thus ?thesis unfolding phi_def by simp
qed

lemma phi_pos: "0 < phi"
  using phi_gt_one by linarith

lemma pi_gt_one: "1 < pi"
  by (approximation 20)

lemma eta_eff_pos: "0 < eta_eff"
  using pi_gt_one by (simp add: eta_eff_def)

lemma term2_default_is_one:
  "term2 default_params = 1"
  by (simp add: term2_def default_params_def)

lemma cosmological_route_D_eff:
  "D_eff (get_domain_params ''cosmological'') = 25"
  by (simp add: get_domain_params_def default_params_def)

lemma cosmological_route_unobserved:
  "¬ observed (get_domain_params ''cosmological'')"
  by (simp add: get_domain_params_def default_params_def)

lemma quantum_route_observed:
  "observed (get_domain_params ''quantum'')"
  by (simp add: get_domain_params_def default_params_def)

lemma quantum_route_D_eff:
  "D_eff (get_domain_params ''quantum'') = 6"
  by (simp add: get_domain_params_def default_params_def)

lemma cosmological_quirk_mod_one:
  "quirk_mod (get_domain_params ''cosmological'') = 1"
  using cosmological_route_unobserved by (simp add: quirk_mod_def)

lemma cmb_route_unobserved:
  "¬ observed (get_domain_params ''cmb'')"
  by (simp add: get_domain_params_def default_params_def)

lemma cmb_quirk_mod_one:
  "quirk_mod (get_domain_params ''cmb'') = 1"
  using cmb_route_unobserved by (simp add: quirk_mod_def)

section ‹Native π / e intervals (Approximation — no floating black-box)›

lemma exp_one_lo: "2.7182818283 < exp (1::real)"
  by (approximation 50)

lemma exp_one_hi: "exp (1::real) < 2.7182818286"
  by (approximation 50)

lemma pi_lo: "3.14159265358979323846 < pi"
  by (approximation 80)

lemma pi_hi: "pi < 3.14159265358979323847"
  by (approximation 80)

lemma psi_con_gt_632: "0.632 < psi_con"
proof -
  have "exp (-1::real) < 0.368"
  proof -
    have "exp 1 > 1 / 0.368"
    proof -
      have "1 / 0.368 < 2.7182818283" by simp
      thus ?thesis using exp_one_lo by linarith
    qed
    hence "1 / exp 1 < 0.368"
      using exp_gt_zero[of 1] by (simp add: divide_less_eq mult.commute)
    thus ?thesis by (simp add: exp_minus)
  qed
  thus ?thesis unfolding psi_con_def by linarith
qed

lemma psi_con_lt_633: "psi_con < 0.633"
proof -
  have "0.367 < exp (-1::real)"
  proof -
    have "exp 1 < 1 / 0.367"
    proof -
      have "2.7182818286 < 1 / 0.367" by simp
      thus ?thesis using exp_one_hi by linarith
    qed
    hence "0.367 < 1 / exp 1"
      using exp_gt_zero[of 1] by (simp add: divide_less_eq mult.commute)
    thus ?thesis by (simp add: exp_minus)
  qed
  thus ?thesis unfolding psi_con_def by linarith
qed

lemma psi_con_bounds: "0.632 < psi_con ∧ psi_con < 0.633"
  using psi_con_gt_632 psi_con_lt_633 by blast

section ‹Deeper engine identities (math, not catalog stats)›

lemma perceived_adjust_at_manifold_root:
  "D_eff p = 25 ⟹ perceived_adjust p = 1"
  by (simp add: perceived_adjust_def)

lemma term1_at_manifold_root_unobserved:
  assumes "D_eff p = 25" "¬ observed p"
  shows "term1 p = term1_base p"
proof -
  have "perceived_adjust p = 1" using assms(1) by (rule perceived_adjust_at_manifold_root)
  have "quirk_mod p = 1" using assms(2) by (rule quirk_mod_unobserved)
  thus ?thesis by (simp add: term1_def ‹perceived_adjust p = 1›)
qed

lemma ln_phi_pos: "0 < ln phi"
  using phi_gt_one by (simp add: ln_gt_zero)

lemma gamma_c_neg: "gamma_c < 0"
proof -
  have "0 < ln 2" by simp
  have "0 < phi" by (rule phi_pos)
  thus ?thesis unfolding gamma_c_def by (simp add: divide_neg_pos)
qed

lemma alpha_fsot_pos: "0 < alpha_fsot"
proof -
  have "1 < pi" by (rule pi_gt_one)
  hence "0 < ln pi" by (simp add: ln_gt_zero)
  have "0 < e_fsot" by (rule e_fsot_pos)
  have "0 < phi" by (rule phi_pos)
  hence "0 < phi ^ 13" by simp
  hence "0 < e_fsot * phi ^ 13" using ‹0 < e_fsot› by simp
  thus ?thesis unfolding alpha_fsot_def using ‹0 < ln pi› by (simp add: divide_pos_pos)
qed

lemma new_perceived_param_pos: "0 < new_perceived_param"
proof -
  have "0 < gamma_euler" by (rule gamma_euler_pos)
  have "0 < e_fsot" by (rule e_fsot_pos)
  have "0 < sqrt 2" by simp
  thus ?thesis unfolding new_perceived_param_def by (simp add: divide_pos_pos)
qed

lemma engine_three_term_form:
  "scaled_S p = k_fsot * term1 p + k_fsot * term2 p + k_fsot * term3 p"
  by (simp add: scaled_S_def raw_S_def algebra_simps)

lemma default_params_N_pos: "0 < N default_params"
  by (simp add: default_params_def)

lemma default_params_D_eff: "D_eff default_params = 25"
  by (simp add: default_params_def)

text ‹
  Alignment note (Python authority pin D1D38A / Lean Formal):
  • S = k · (T1 + T2 + T3) matches vendor/fsot_compute.py compute_scalar
  • T1 includes growth, cos((ψ_con+δψ)/η_eff), perceived_adjust, quirk_mod
  • T2 = scale·amplitude + trend_bias
  • T3 = valve · acoustic · phase (chaos / poof / acoustic bleed)
  These definitions are the mathematical object under cross-prover verification.
›

section ‹Honesty markers›

text ‹
  PROVED HERE (machine-checked math structure):
  • raw_S / scaled_S algebraic decomposition from seed-derived terms
  • growth_term > 0, poof_factor > 0, beta_fsot > 0, phi > 1, eta_eff > 0
  • quirk_mod = 1 when unobserved (cosmology / CMB routes)
  • domain routing for cosmological / quantum / CMB folds
  • native π and e interval bounds via Approximation
  • psi_con quantitative band (0.632, 0.633)

  NOT claimed here (belongs to empirical / Lean oracle layers):
  • per-domain median error ≤ 0.5% against measured catalogs
  • 402-domain pooled statistics
  • f64 boot-scalar bit equality without oracle triangulation

  FullFormalSpine continues to cross-check exported numeric obligations.
  This theory supplies the mathematical engine that StructuralProofSpine lacked.
›

end
