(* FSOT Tier 83 — transcendental bounds chunk 4/4 (generated). *)
From Stdlib Require Import Reals.
Require Import TranscendentalBoundsBase.
Require Import TranscendentalBoundsCert.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.

Lemma exp_1253_gt_34 : (3.4%R) < exp (1.253%R).
Proof.
exact certified_exp_1253_gt_34.
Qed.
