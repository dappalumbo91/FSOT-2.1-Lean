From Stdlib Require Import Reals.
From Stdlib Require Import Rtrigo1.
From Stdlib Require Import Rtrigo_def.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.
Lemma PI_gt_314 : (314%R / 100%R) < PI.
Proof.
  unfold PI.
  lra.
Qed.
