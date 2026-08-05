(* FSOT Tier 83 — native Coq proofs for pi/e base intervals (no axioms). *)
(* Proved via Interval (Rocq Platform) interval arithmetic — not Axiom, not fake lra. *)
From Stdlib Require Import Reals.
From Interval Require Import Tactic.
Local Open Scope R_scope.

(** exp 1 lower bound (seed e interval). *)
Lemma certified_exp_one_lo : 2.7182818283 < exp 1.
Proof. interval with (i_prec 50). Qed.

(** exp 1 upper bound. *)
Lemma certified_exp_one_hi : exp 1 < 2.7182818286.
Proof. interval with (i_prec 50). Qed.

(** Tight pi lower digit string (matches Bounds.lean / Mathlib pi_gt_d20 chain). *)
Lemma certified_pi_lo : 3.14159265358979323846 < PI.
Proof. interval with (i_prec 80). Qed.

(** Tight pi upper digit string. *)
Lemma certified_pi_hi : PI < 3.14159265358979323847.
Proof. interval with (i_prec 80). Qed.

(** Coarser classical bridges (optional consumers / densify docs). *)
Lemma PI_gt_3 : 3 < PI.
Proof. interval. Qed.

Lemma PI_lt_22_7 : PI < 22 / 7.
Proof. interval. Qed.

Lemma exp1_gt_2 : 2 < exp 1.
Proof. interval. Qed.

Lemma exp1_lt_3 : exp 1 < 3.
Proof. interval. Qed.
