(* FSOT Tier 83 — transcendental bounds chunk 2/3 (generated). *)
From Stdlib Require Import Reals.
Require Import TranscendentalBoundsBase.
Require Import TranscendentalBoundsCert.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.

Lemma e_pi_lt_27182818286_mul_pi : exp 1 * PI < (2.7182818286%R) * (3.14159265358979323847%R).
Proof.
exact certified_e_pi_lt_27182818286_mul_pi.
Qed.

Lemma e_pi_gt_85397323 : (85397323%R) / 10000000 < exp 1 * PI.
Proof.
exact certified_e_pi_gt_85397323.
Qed.

Lemma e_pi_gt_8539732 : (8539732%R) / 1000000 < exp 1 * PI.
Proof.
exact certified_e_pi_gt_8539732.
Qed.

Lemma e_pi_lt_853973478 : exp 1 * PI < (853973478%R) / 100000000.
Proof.
exact certified_e_pi_lt_853973478.
Qed.

Lemma e_pi_lt_85397348 : exp 1 * PI < (85397348%R) / 10000000.
Proof.
exact certified_e_pi_lt_85397348.
Qed.

Lemma e_pi_lt_8539736 : exp 1 * PI < (8539736%R) / 1000000.
Proof.
exact certified_e_pi_lt_8539736.
Qed.

Lemma pi_half_gt_02956 : (0.295612%R) < PI / 2.
Proof.
exact certified_pi_half_gt_02956.
Qed.

Lemma pi_half_gt_1156 : (1.15572734986%R) < PI / 2.
Proof.
exact certified_pi_half_gt_1156.
Qed.

Lemma pi_gt_290272 : (0.290272%R) < PI.
Proof.
exact certified_pi_gt_290272.
Qed.

Lemma pi_gt_291325 : (0.291325%R) < PI.
Proof.
exact certified_pi_gt_291325.
Qed.

Lemma pi_gt_0415068 : (0.415068%R) < PI.
Proof.
exact certified_pi_gt_0415068.
Qed.

Lemma pi_gt_0415069 : (0.415069%R) < PI.
Proof.
exact certified_pi_gt_0415069.
Qed.

Lemma pi_div_e_gt_115572734973 : (1.15572734973%R) < PI / exp 1.
Proof.
exact certified_pi_div_e_gt_115572734973.
Qed.

Lemma pi_div_e_lt_115572734986 : PI / exp 1 < (1.15572734986%R).
Proof.
exact certified_pi_div_e_lt_115572734986.
Qed.

Lemma pi_div_e_in_Icc_sin : ( - (PI / 2) <= PI / exp 1 ) /\ ( PI / exp 1 <= PI / 2 ).
Proof.
exact certified_pi_div_e_in_Icc_sin.
Qed.

Lemma exp_04807_lt_1618 : exp (0.4807%R) < (1.618%R).
Proof.
exact certified_exp_04807_lt_1618.
Qed.

Lemma exp_01530_gt_11653 : (1.1653%R) < exp (0.1530%R).
Proof.
exact certified_exp_01530_gt_11653.
Qed.

Lemma exp_01534_lt_1168 : exp (0.1534%R) < (1.168%R).
Proof.
exact certified_exp_01534_lt_1168.
Qed.

Lemma exp_1146_gt_31416 : (3.1416%R) < exp (1.146%R).
Proof.
exact certified_exp_1146_gt_31416.
Qed.

Lemma exp_11453_gt_pi23847 : (3.14159265358979323847%R) < exp (1.1453%R).
Proof.
exact certified_exp_11453_gt_pi23847.
Qed.

Lemma exp_02903_lt_1338 : exp (0.2903%R) < (1.338%R).
Proof.
exact certified_exp_02903_lt_1338.
Qed.

Lemma exp_consciousness_phase_lt_132 : exp (0.2903%R) < (1.338%R).
Proof.
exact certified_exp_consciousness_phase_lt_132.
Qed.

Lemma exp_1434_gt_4167 : (4.167%R) < exp (1.434%R).
Proof.
exact certified_exp_1434_gt_4167.
Qed.

Lemma exp_neg_1434_lt_24_div_25 : exp (-1.434) < (6%R) / 25.
Proof.
exact certified_exp_neg_1434_lt_24_div_25.
Qed.

Lemma exp_040_lt_25_div_24 : exp (0.040%R) < (25%R) / 24.
Proof.
exact certified_exp_040_lt_25_div_24.
Qed.
