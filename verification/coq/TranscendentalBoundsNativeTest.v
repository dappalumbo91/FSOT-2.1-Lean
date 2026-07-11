From Stdlib Require Import Reals.
From Stdlib Require Import Rpower.
From Stdlib Require Import Rtrigo1.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.

Lemma certified_exp_one_lo : (2.7182818283%R) < exp 1.
Proof.
  pose proof (exp_ineq1 (1%R)) as H.
  lra.
Qed.