(* FSOT Tier 83 — transcendental bounds chunk 1/3 (generated). *)
theory TranscendentalBounds_00
imports TranscendentalBoundsCert
begin

lemma exp_neg_one_gt_367: "(0.367 :: real) < exp (-1)"
  by (rule certified_exp_neg_one_gt_367)

lemma exp_neg_one_lt_368: "exp (-1) < (0.368 :: real)"
  by (rule certified_exp_neg_one_lt_368)

lemma exp_neg_0298_lt_08: "exp (-0.298) < (0.8 :: real)"
  by (rule certified_exp_neg_0298_lt_08)

lemma exp_03_gt_12: "(1.2 :: real) < exp (0.3 :: real)"
  by (rule certified_exp_03_gt_12)

lemma exp_0572_lt_1772: "exp (0.572 :: real) < (1.772 :: real)"
  by (rule certified_exp_0572_lt_1772)

lemma exp_1144_lt_31415: "exp (1.144 :: real) < (3.1415 :: real)"
  by (rule certified_exp_1144_lt_31415)

lemma exp_11445_lt_3141592: "exp (1.1445 :: real) < (3.141592 :: real)"
  by (rule certified_exp_11445_lt_3141592)

lemma exp_0245_gt_1275: "(1.275 :: real) < exp (0.245 :: real)"
  by (rule certified_exp_0245_gt_1275)

lemma exp_049_gt_16181: "(1.6181 :: real) < exp (0.49 :: real)"
  by (rule certified_exp_049_gt_16181)

lemma exp_04813_gt_16181: "(1.6181 :: real) < exp (0.4813 :: real)"
  by (rule certified_exp_04813_gt_16181)

lemma exp_185_gt_626: "(6.26 :: real) < exp (1.85 :: real)"
  by (rule certified_exp_185_gt_626)

lemma exp_neg_185_lt_016: "exp (-1.85) < (0.16 :: real)"
  by (rule certified_exp_neg_185_lt_016)

lemma exp_077_gt_184: "(1.84 :: real) < exp (0.77 :: real)"
  by (rule certified_exp_077_gt_184)

lemma exp_177_gt_five: "(5 :: real) < exp (1.77 :: real)"
  by (rule certified_exp_177_gt_five)

lemma e_minus_one_gt_one: "(1 :: real) < (exp (1 :: real)) - 1"
  by (rule certified_e_minus_one_gt_one)

lemma exp_five_gt_100: "(100 :: real) < exp (5 :: real)"
  by (rule certified_exp_five_gt_100)

lemma exp_three_gt_twenty: "(20 :: real) < exp (3 :: real)"
  by (rule certified_exp_three_gt_twenty)

lemma exp_six_gt_400: "(400 :: real) < exp (6 :: real)"
  by (rule certified_exp_six_gt_400)

lemma exp_28_gt_410: "(410 :: real) < exp (28 :: real)"
  by (rule certified_exp_28_gt_410)

lemma pi_div_e_lt_pi_div_two: "pi / (exp (1 :: real)) < pi / 2"
  by (rule certified_pi_div_e_lt_pi_div_two)

lemma e_gt_27182818283: "(2.7182818283 :: real) < (exp (1 :: real))"
  by (rule certified_exp_one_lo)

lemma e_lt_27182818286: "(exp (1 :: real)) < (2.7182818286 :: real)"
  by (rule certified_exp_one_hi)

lemma pi_gt_314159265358979323846: "(3.14159265358979323846 :: real) < pi"
  by (rule certified_pi_lo)

lemma pi_lt_314159265358979323847: "pi < (3.14159265358979323847 :: real)"
  by (rule certified_pi_hi)

lemma e_pi_gt_27182818283_mul_pi: "(2.7182818283 :: real) * (3.14159265358979323846 :: real) < (exp (1 :: real)) * pi"
  by (rule certified_e_pi_gt_27182818283_mul_pi)

end
