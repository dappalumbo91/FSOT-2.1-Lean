(* FSOT Tier 83 — transcendental bounds chunk 3/3 (generated). *)
theory TranscendentalBounds_02
imports TranscendentalBoundsCert
begin

lemma exp_neg_040_gt_24_div_25: "(24 :: real) / 25 < exp (-0.040)"
  by (rule certified_exp_neg_040_gt_24_div_25)

lemma exp_0822_gt_25_div_11: "(25 :: real) / 11 < exp (0.822 :: real)"
  by (rule certified_exp_0822_gt_25_div_11)

lemma exp_neg_0822_lt_11_div_25: "exp (-0.822) < (11 :: real) / 25"
  by (rule certified_exp_neg_0822_lt_11_div_25)

lemma exp_0818_lt_25_div_11: "exp (0.818 :: real) < (25 :: real) / 11"
  by (rule certified_exp_0818_lt_25_div_11)

lemma exp_neg_0818_gt_11_div_25: "(11 :: real) / 25 < exp (-0.818)"
  by (rule certified_exp_neg_0818_gt_11_div_25)

lemma exp_03865_gt_14716: "(1.4716 :: real) < exp (0.3865 :: real)"
  by (rule certified_exp_03865_gt_14716)

lemma exp_13865_gt_four: "(4 :: real) < exp (1.3865 :: real)"
  by (rule certified_exp_13865_gt_four)

lemma exp_1618_gt_five: "(5 :: real) < exp (1.618 :: real)"
  by (rule certified_exp_1618_gt_five)

lemma exp_0602_lt_1838: "exp (0.602 :: real) < (1.838 :: real)"
  by (rule certified_exp_0602_lt_1838)

lemma exp_1602_lt_5: "exp (1.602 :: real) < (5 :: real)"
  by (rule certified_exp_1602_lt_5)

lemma exp_0505_lt_1838: "exp (0.505 :: real) < (1.838 :: real)"
  by (rule certified_exp_0505_lt_1838)

lemma exp_0331_lt_1412: "exp (0.331 :: real) < (1.412 :: real)"
  by (rule certified_exp_0331_lt_1412)

lemma exp_1331_lt_384: "exp (1.331 :: real) < (3.84 :: real)"
  by (rule certified_exp_1331_lt_384)

lemma exp_1505_lt_5: "exp (1.505 :: real) < (5 :: real)"
  by (rule certified_exp_1505_lt_5)

lemma exp_0351_lt_1470: "exp (0.351 :: real) < (1.470 :: real)"
  by (rule certified_exp_0351_lt_1470)

lemma exp_1351_lt_4: "exp (1.351 :: real) < (4 :: real)"
  by (rule certified_exp_1351_lt_4)

lemma exp_005_lt_115: "exp (0.05 :: real) < (1.15 :: real)"
  by (rule certified_exp_005_lt_115)

lemma exp_1253_gt_34: "(3.4 :: real) < exp (1.253 :: real)"
  by (rule certified_exp_1253_gt_34)

end
