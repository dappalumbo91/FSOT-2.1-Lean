(* FSOT Tier 83 — transcendental bounds chunk 3/3 (generated). *)
From Stdlib Require Import Reals.
Require Import TranscendentalBoundsBase.
Require Import TranscendentalBoundsCert.
From Stdlib Require Import Psatz.
Local Open Scope R_scope.

Lemma exp_neg_040_gt_24_div_25 : (24%R) / 25 < exp (-0.040).
Proof.
exact certified_exp_neg_040_gt_24_div_25.
Qed.

Lemma exp_0822_gt_25_div_11 : (25%R) / 11 < exp (0.822%R).
Proof.
exact certified_exp_0822_gt_25_div_11.
Qed.

Lemma exp_neg_0822_lt_11_div_25 : exp (-0.822) < (11%R) / 25.
Proof.
exact certified_exp_neg_0822_lt_11_div_25.
Qed.

Lemma exp_0818_lt_25_div_11 : exp (0.818%R) < (25%R) / 11.
Proof.
exact certified_exp_0818_lt_25_div_11.
Qed.

Lemma exp_neg_0818_gt_11_div_25 : (11%R) / 25 < exp (-0.818).
Proof.
exact certified_exp_neg_0818_gt_11_div_25.
Qed.

Lemma exp_03865_gt_14716 : (1.4716%R) < exp (0.3865%R).
Proof.
exact certified_exp_03865_gt_14716.
Qed.

Lemma exp_13865_gt_four : (4%R) < exp (1.3865%R).
Proof.
exact certified_exp_13865_gt_four.
Qed.

Lemma exp_1618_gt_five : (5%R) < exp (1.618%R).
Proof.
exact certified_exp_1618_gt_five.
Qed.

Lemma exp_0602_lt_1838 : exp (0.602%R) < (1.838%R).
Proof.
exact certified_exp_0602_lt_1838.
Qed.

Lemma exp_1602_lt_5 : exp (1.602%R) < (5%R).
Proof.
exact certified_exp_1602_lt_5.
Qed.

Lemma exp_0505_lt_1838 : exp (0.505%R) < (1.838%R).
Proof.
exact certified_exp_0505_lt_1838.
Qed.

Lemma exp_0331_lt_1412 : exp (0.331%R) < (1.412%R).
Proof.
exact certified_exp_0331_lt_1412.
Qed.

Lemma exp_1331_lt_384 : exp (1.331%R) < (3.84%R).
Proof.
exact certified_exp_1331_lt_384.
Qed.

Lemma exp_1505_lt_5 : exp (1.505%R) < (5%R).
Proof.
exact certified_exp_1505_lt_5.
Qed.

Lemma exp_0351_lt_1470 : exp (0.351%R) < (1.470%R).
Proof.
exact certified_exp_0351_lt_1470.
Qed.

Lemma exp_1351_lt_4 : exp (1.351%R) < (4%R).
Proof.
exact certified_exp_1351_lt_4.
Qed.

Lemma exp_005_lt_115 : exp (0.05%R) < (1.15%R).
Proof.
exact certified_exp_005_lt_115.
Qed.

Lemma exp_1253_gt_34 : (3.4%R) < exp (1.253%R).
Proof.
exact certified_exp_1253_gt_34.
Qed.
