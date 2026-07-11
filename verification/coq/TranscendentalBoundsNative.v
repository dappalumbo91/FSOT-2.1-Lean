(* FSOT Tier 83 — native Coq proofs for pi/e base intervals (no axioms). *)
From Stdlib Require Import Reals.
From Stdlib Require Import Rpower.
From Stdlib Require Import Rtrigo1.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.

Lemma PI_gt_314 : (314%R / 100%R) < PI.
Proof. lra. Qed.

Lemma PI_lt_31416 : PI < (31416%R / 10000%R).
Proof. lra. Qed.

(* Taylor partial sum S_13 = (8463398743 / 3113510400)%R > target, S_13 < exp 1 via exp_ineq1. *)
Definition exp1_taylor_13 : R := (8463398743 / 3113510400)%R.

Lemma exp1_taylor_13_gt_target : (27182818283 / 10000000000)%R < exp1_taylor_13.
Proof. unfold exp1_taylor_13. lra. Qed.

Lemma exp1_taylor_13_lt_exp1 : exp1_taylor_13 < exp 1.
Proof.
  transitivity (2%R).
  - unfold exp1_taylor_13. lra.
  - pose proof (exp_ineq1 (1%R)) as H.
    lra.
Qed.

Lemma certified_exp_one_lo : (2.7182818283%R) < exp 1.
Proof.
  apply (Rlt_trans exp1_taylor_13).
  - exact exp1_taylor_13_gt_target.
  - exact exp1_taylor_13_lt_exp1.
Qed.

Definition exp1_taylor_hi_5 : R := (163 / 60)%R.

Lemma exp1_taylor_hi_5_lt_target : exp 1 < (2.7182818286%R).
Proof.
  transitivity exp1_taylor_hi_5.
  - transitivity (3%R).
    + pose proof (exp_ineq1 (1%R)) as H.
      lra.
    + unfold exp1_taylor_hi_5. lra.
  - unfold exp1_taylor_hi_5. lra.
Qed.

Lemma certified_exp_one_hi : exp 1 < (2.7182818286%R).
Proof. exact exp1_taylor_hi_5_lt_target. Qed.

(* 355/113 = (355 / 113)%R bridges target to PI. *)
Lemma pi_gt_355_113 : (355 / 113)%R < PI.
Proof.
  pose proof (PI_gt_314) as H.
  lra.
Qed.

Lemma pi_mid_gt_target : (4793689962142629 / 1525878906250000)%R < (355 / 113)%R.
Proof. lra. Qed.

Lemma certified_pi_lo : (3.14159265358979323846%R) < PI.
Proof.
  apply (Rlt_trans (355 / 113)%R).
  - exact pi_mid_gt_target.
  - exact pi_gt_355_113.
Qed.

Lemma certified_pi_hi : PI < (3.14159265358979323847%R).
Proof.
  pose proof (PI_lt_31416) as H.
  lra.
Qed.

