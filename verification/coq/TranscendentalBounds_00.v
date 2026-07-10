(* FSOT Tier 83 — transcendental bounds chunk 1/3 (generated). *)
From Stdlib Require Import Reals.
Require Import TranscendentalBoundsBase.
Require Import TranscendentalBoundsCert.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.

Lemma exp_neg_one_gt_367 : (0.367%R) < exp (-1).
Proof.
exact certified_exp_neg_one_gt_367.
Qed.

Lemma exp_neg_one_lt_368 : exp (-1) < (0.368%R).
Proof.
exact certified_exp_neg_one_lt_368.
Qed.

Lemma exp_neg_0298_lt_08 : exp (-0.298) < (0.8%R).
Proof.
exact certified_exp_neg_0298_lt_08.
Qed.

Lemma exp_03_gt_12 : (1.2%R) < exp (0.3%R).
Proof.
pose proof (exp_ineq1 (0.3%R) nonzero_03) as H.
lra.
Qed.

Lemma exp_0572_lt_1772 : exp (0.572%R) < (1.772%R).
Proof.
exact certified_exp_0572_lt_1772.
Qed.

Lemma exp_1144_lt_31415 : exp (1.144%R) < (3.1415%R).
Proof.
exact certified_exp_1144_lt_31415.
Qed.

Lemma exp_11445_lt_3141592 : exp (1.1445%R) < (3.141592%R).
Proof.
exact certified_exp_11445_lt_3141592.
Qed.

Lemma exp_0245_gt_1275 : (1.275%R) < exp (0.245%R).
Proof.
exact certified_exp_0245_gt_1275.
Qed.

Lemma exp_049_gt_16181 : (1.6181%R) < exp (0.49%R).
Proof.
exact certified_exp_049_gt_16181.
Qed.

Lemma exp_04813_gt_16181 : (1.6181%R) < exp (0.4813%R).
Proof.
exact certified_exp_04813_gt_16181.
Qed.

Lemma exp_185_gt_626 : (6.26%R) < exp (1.85%R).
Proof.
exact certified_exp_185_gt_626.
Qed.

Lemma exp_neg_185_lt_016 : exp (-1.85) < (0.16%R).
Proof.
exact certified_exp_neg_185_lt_016.
Qed.

Lemma exp_077_gt_184 : (1.84%R) < exp (0.77%R).
Proof.
exact certified_exp_077_gt_184.
Qed.

Lemma exp_177_gt_five : (5%R) < exp (1.77%R).
Proof.
exact certified_exp_177_gt_five.
Qed.

Lemma e_minus_one_gt_one : (1%R) < exp 1 - 1.
Proof.
exact certified_e_minus_one_gt_one.
Qed.

Lemma exp_five_gt_100 : (100%R) < exp (5%R).
Proof.
exact certified_exp_five_gt_100.
Qed.

Lemma exp_three_gt_twenty : (20%R) < exp (3%R).
Proof.
exact certified_exp_three_gt_twenty.
Qed.

Lemma exp_six_gt_400 : (400%R) < exp (6%R).
Proof.
exact certified_exp_six_gt_400.
Qed.

Lemma exp_28_gt_410 : (410%R) < exp (28%R).
Proof.
exact certified_exp_28_gt_410.
Qed.

Lemma pi_div_e_lt_pi_div_two : PI / exp 1 < PI / 2.
Proof.
exact certified_pi_div_e_lt_pi_div_two.
Qed.

Lemma e_gt_27182818283 : (2.7182818283%R) < exp 1.
Proof.
exact certified_exp_one_lo.
Qed.

Lemma e_lt_27182818286 : exp 1 < (2.7182818286%R).
Proof.
exact certified_exp_one_hi.
Qed.

Lemma pi_gt_314159265358979323846 : (3.14159265358979323846%R) < PI.
Proof.
exact certified_pi_lo.
Qed.

Lemma pi_lt_314159265358979323847 : PI < (3.14159265358979323847%R).
Proof.
exact certified_pi_hi.
Qed.

Lemma e_pi_gt_27182818283_mul_pi : (2.7182818283%R) * (3.14159265358979323846%R) < exp 1 * PI.
Proof.
exact certified_e_pi_gt_27182818283_mul_pi.
Qed.
