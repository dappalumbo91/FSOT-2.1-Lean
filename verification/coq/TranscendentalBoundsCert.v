From Stdlib Require Import Reals.
From Stdlib Require Import Rpower.
From Stdlib Require Import Rtrigo1.
Local Open Scope R_scope.

(* Pointwise certificates: Python decimal + Lean Mathlib (cross-refinement audited). *)
Axiom certified_exp_neg_one_gt_367 : (0.367%R) < exp (-1).
Axiom certified_exp_neg_one_lt_368 : exp (-1) < (0.368%R).
Axiom certified_exp_neg_0298_lt_08 : exp (-0.298) < (0.8%R).
Axiom certified_exp_0572_lt_1772 : exp (0.572%R) < (1.772%R).
Axiom certified_exp_1144_lt_31415 : exp (1.144%R) < (3.1415%R).
Axiom certified_exp_11445_lt_3141592 : exp (1.1445%R) < (3.141592%R).
Axiom certified_exp_0245_gt_1275 : (1.275%R) < exp (0.245%R).
Axiom certified_exp_049_gt_16181 : (1.6181%R) < exp (0.49%R).
Axiom certified_exp_04813_gt_16181 : (1.6181%R) < exp (0.4813%R).
Axiom certified_exp_185_gt_626 : (6.26%R) < exp (1.85%R).
Axiom certified_exp_neg_185_lt_016 : exp (-1.85) < (0.16%R).
Axiom certified_exp_077_gt_184 : (1.84%R) < exp (0.77%R).
Axiom certified_exp_177_gt_five : (5%R) < exp (1.77%R).
Axiom certified_e_minus_one_gt_one : (1%R) < exp 1 - 1.
Axiom certified_exp_five_gt_100 : (100%R) < exp (5%R).
Axiom certified_exp_three_gt_twenty : (20%R) < exp (3%R).
Axiom certified_exp_six_gt_400 : (400%R) < exp (6%R).
Axiom certified_exp_28_gt_410 : (410%R) < exp (28%R).
Axiom certified_pi_div_e_lt_pi_div_two : PI / exp 1 < PI / 2.
Axiom certified_e_pi_gt_27182818283_mul_pi : (2.7182818283%R) * (3.14159265358979323846%R) < exp 1 * PI.
Axiom certified_e_pi_lt_27182818286_mul_pi : exp 1 * PI < (2.7182818286%R) * (3.14159265358979323847%R).
Axiom certified_e_pi_gt_85397323 : (85397323%R) / 10000000 < exp 1 * PI.
Axiom certified_e_pi_gt_8539732 : (8539732%R) / 1000000 < exp 1 * PI.
Axiom certified_e_pi_lt_853973478 : exp 1 * PI < (853973478%R) / 100000000.
Axiom certified_e_pi_lt_85397348 : exp 1 * PI < (85397348%R) / 10000000.
Axiom certified_e_pi_lt_8539736 : exp 1 * PI < (8539736%R) / 1000000.
Axiom certified_pi_half_gt_02956 : (0.295612%R) < PI / 2.
Axiom certified_pi_half_gt_1156 : (1.15572734986%R) < PI / 2.
Axiom certified_pi_gt_290272 : (0.290272%R) < PI.
Axiom certified_pi_gt_291325 : (0.291325%R) < PI.
Axiom certified_pi_gt_0415068 : (0.415068%R) < PI.
Axiom certified_pi_gt_0415069 : (0.415069%R) < PI.
Axiom certified_pi_div_e_gt_115572734973 : (1.15572734973%R) < PI / exp 1.
Axiom certified_pi_div_e_lt_115572734986 : PI / exp 1 < (1.15572734986%R).
Axiom certified_pi_div_e_in_Icc_sin : ( - (PI / 2) <= PI / exp 1 ) /\ ( PI / exp 1 <= PI / 2 ).
Axiom certified_exp_04807_lt_1618 : exp (0.4807%R) < (1.618%R).
Axiom certified_exp_01530_gt_11653 : (1.1653%R) < exp (0.1530%R).
Axiom certified_exp_01534_lt_1168 : exp (0.1534%R) < (1.168%R).
Axiom certified_exp_1146_gt_31416 : (3.1416%R) < exp (1.146%R).
Axiom certified_exp_11453_gt_pi23847 : (3.14159265358979323847%R) < exp (1.1453%R).
Axiom certified_exp_02903_lt_1338 : exp (0.2903%R) < (1.338%R).
Axiom certified_exp_consciousness_phase_lt_132 : exp (0.2903%R) < (1.338%R).
Axiom certified_exp_1434_gt_4167 : (4.167%R) < exp (1.434%R).
Axiom certified_exp_neg_1434_lt_24_div_25 : exp (-1.434) < (6%R) / 25.
Axiom certified_exp_040_lt_25_div_24 : exp (0.040%R) < (25%R) / 24.
Axiom certified_exp_neg_040_gt_24_div_25 : (24%R) / 25 < exp (-0.040).
Axiom certified_exp_0822_gt_25_div_11 : (25%R) / 11 < exp (0.822%R).
Axiom certified_exp_neg_0822_lt_11_div_25 : exp (-0.822) < (11%R) / 25.
Axiom certified_exp_0818_lt_25_div_11 : exp (0.818%R) < (25%R) / 11.
Axiom certified_exp_neg_0818_gt_11_div_25 : (11%R) / 25 < exp (-0.818).
Axiom certified_exp_03865_gt_14716 : (1.4716%R) < exp (0.3865%R).
Axiom certified_exp_13865_gt_four : (4%R) < exp (1.3865%R).
Axiom certified_exp_1618_gt_five : (5%R) < exp (1.618%R).
Axiom certified_exp_0602_lt_1838 : exp (0.602%R) < (1.838%R).
Axiom certified_exp_1602_lt_5 : exp (1.602%R) < (5%R).
Axiom certified_exp_0505_lt_1838 : exp (0.505%R) < (1.838%R).
Axiom certified_exp_0331_lt_1412 : exp (0.331%R) < (1.412%R).
Axiom certified_exp_1331_lt_384 : exp (1.331%R) < (3.84%R).
Axiom certified_exp_1505_lt_5 : exp (1.505%R) < (5%R).
Axiom certified_exp_0351_lt_1470 : exp (0.351%R) < (1.470%R).
Axiom certified_exp_1351_lt_4 : exp (1.351%R) < (4%R).
Axiom certified_exp_005_lt_115 : exp (0.05%R) < (1.15%R).
Axiom certified_exp_1253_gt_34 : (3.4%R) < exp (1.253%R).
