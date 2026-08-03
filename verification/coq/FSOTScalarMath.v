(*
  FSOT Coq/Rocq mathematical core — engine math, not only catalog structure.

  Mirrors Lean FSOT.Formal.Scalar and Isabelle FSOTScalarMath:
    raw_S = term1 + term2 + term3
    scaled_S = k * raw_S
  Seeds: PI, exp 1, phi = (1+√5)/2, gamma_euler, catalan_G.
*)
From Stdlib Require Import Reals.
From Stdlib Require Import Rpower.
From Stdlib Require Import Rtrigo_def.
From Stdlib Require Import Rtrigo1.
From Stdlib Require Import Ratan.
From Stdlib Require Import Psatz.
From Stdlib Require Import Lra.
Local Open Scope R_scope.

(* ---- Seeds ---- *)
Definition phi : R := (1 + sqrt 5) / 2.
Definition e_fsot : R := exp 1.
Definition gamma_euler : R := 5772156649015329 / 10000000000000000.
Definition catalan_G : R := 915965594177219 / 1000000000000000.

(* ---- Layer-1 derived ---- *)
Definition psi_con : R := 1 - exp (-1).
Definition eta_eff : R := 1 / (PI - 1).
Definition alpha_fsot : R := ln PI / (e_fsot * phi ^ 13).
Definition gamma_c : R := - ln 2 / phi.
Definition poof_factor : R :=
  exp (- (ln PI / e_fsot) / (eta_eff * ln phi)).
Definition beta_fsot : R := 1 / exp (Rpower PI PI + (e_fsot - 1)).

(* ---- Parameters ---- *)
Record fsot_params : Type := mkParams {
  N : R;
  P : R;
  D_eff : R;
  recent_hits : R;
  delta_psi : R;
  delta_theta : R;
  rho : R;
  scale : R;
  amplitude : R;
  trend_bias : R;
  observed : bool
}.

Definition default_params : fsot_params :=
  mkParams 1 1 25 0 1 1 1 1 1 0 false.

Definition growth_term (p : fsot_params) : R :=
  exp (alpha_fsot * (1 - recent_hits p / N p) * gamma_euler / phi).

Definition quirk_mod (p : fsot_params) : R :=
  if observed p then
    (* simplified: consciousness_factor * phase_variance folded as free cos/exp site *)
    exp 0 * cos (delta_psi p)
  else 1.

Definition term2 (p : fsot_params) : R :=
  scale p * amplitude p + trend_bias p.

(* Abstract term1/term3 shells for structural engine identities.
   Full closed forms match Python/Lean; Coq proves the algebraic engine laws. *)
Parameter term1 : fsot_params -> R.
Parameter term3 : fsot_params -> R.
Parameter k_fsot : R.

Definition raw_S (p : fsot_params) : R := term1 p + term2 p + term3 p.
Definition scaled_S (p : fsot_params) : R := raw_S p * k_fsot.

(* ---- Core mathematical identities ---- *)

Lemma raw_S_decomposition : forall p,
  raw_S p = term1 p + term2 p + term3 p.
Proof. intros; unfold raw_S; reflexivity. Qed.

Lemma scaled_S_factorization : forall p,
  scaled_S p = k_fsot * (term1 p + term2 p + term3 p).
Proof. intros; unfold scaled_S, raw_S; ring. Qed.

Lemma engine_three_term_form : forall p,
  scaled_S p = k_fsot * term1 p + k_fsot * term2 p + k_fsot * term3 p.
Proof. intros; unfold scaled_S, raw_S; ring. Qed.

Lemma quirk_mod_unobserved : forall p,
  observed p = false -> quirk_mod p = 1.
Proof. intros p H; unfold quirk_mod; rewrite H; reflexivity. Qed.

Lemma growth_term_pos : forall p, 0 < growth_term p.
Proof. intros; unfold growth_term; apply exp_pos. Qed.

Lemma e_fsot_pos : 0 < e_fsot.
Proof. unfold e_fsot; apply exp_pos. Qed.

Lemma poof_factor_pos : 0 < poof_factor.
Proof. unfold poof_factor; apply exp_pos. Qed.

Lemma gamma_euler_pos : 0 < gamma_euler.
Proof. unfold gamma_euler; lra. Qed.

Lemma catalan_G_pos : 0 < catalan_G.
Proof. unfold catalan_G; lra. Qed.

Lemma phi_gt_one : 1 < phi.
Proof.
  unfold phi.
  (* (1+√5)/2 > 1  ⇔  √5 > 1. Use 1 = sqrt 1 and monotonicity of sqrt. *)
  assert (Hsq : 1 < 5) by lra.
  assert (H1 : sqrt 1 < sqrt 5).
  { apply sqrt_lt_1; lra. }
  rewrite sqrt_1 in H1.
  lra.
Qed.

Lemma phi_pos : 0 < phi.
Proof. pose proof phi_gt_one; lra. Qed.

Lemma psi_con_eq : psi_con = 1 - exp (-1).
Proof. reflexivity. Qed.

Lemma term2_default_is_one : term2 default_params = 1.
Proof. unfold term2, default_params; simpl; lra. Qed.

Lemma default_D_eff : D_eff default_params = 25.
Proof. reflexivity. Qed.

Lemma default_unobserved : observed default_params = false.
Proof. reflexivity. Qed.

Lemma default_quirk_mod_one : quirk_mod default_params = 1.
Proof. apply quirk_mod_unobserved; apply default_unobserved. Qed.

(* ---- Native pi/e bands (shared with TranscendentalBoundsNative) ---- *)

Lemma pi_gt_one : 1 < PI.
Proof.
  (* Stdlib Ratan: 3/2 < PI/2 ⇒ 3 < PI ⇒ 1 < PI *)
  pose proof PI2_3_2 as H.
  lra.
Qed.

Lemma eta_eff_pos : 0 < eta_eff.
Proof.
  unfold eta_eff.
  assert (H : 0 < PI - 1) by (pose proof pi_gt_one; lra).
  rewrite Rdiv_1_l.
  apply Rinv_0_lt_compat; exact H.
Qed.

Lemma exp_one_lo_band : 2 < exp 1.
Proof. apply exp_ineq1; lra. Qed.

(* ---- Honesty ----
   Proved: algebraic raw_S/scaled_S engine, growth_term > 0, phi > 1,
   quirk_mod = 1 when unobserved, default route facts, eta_eff > 0.
   Empirical 402-domain medians live in Python/Lean export spines, not here.
*)
