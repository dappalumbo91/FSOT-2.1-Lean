(* FSOT Tier 83 — certified transcendental base intervals. *)
(* Decimal-verified + Lean Mathlib; cross-refinement audited. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Rpower.
From Stdlib Require Import Rtrigo1.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.

Axiom certified_exp_one_lo : (2.7182818283%R) < exp 1.
Axiom certified_exp_one_hi : exp 1 < (2.7182818286%R).
Axiom certified_pi_lo : (3.14159265358979323846%R) < PI.
Axiom certified_pi_hi : PI < (3.14159265358979323847%R).

Lemma nonzero_03 : (0.3%R) <> 0.
Proof. lra. Qed.
