(* FSOT Tier 83 — transcendental bounds chunk 2/3 (generated). *)
theory TranscendentalBounds_01
imports TranscendentalBoundsCert
begin

lemma e_pi_lt_27182818286_mul_pi: "(exp (1 :: real)) * pi < (2.7182818286 :: real) * (3.14159265358979323847 :: real)"
  by (rule certified_e_pi_lt_27182818286_mul_pi)

lemma e_pi_gt_85397323: "(85397323 :: real) / 10000000 < (exp (1 :: real)) * pi"
  by (rule certified_e_pi_gt_85397323)

lemma e_pi_gt_8539732: "(8539732 :: real) / 1000000 < (exp (1 :: real)) * pi"
  by (rule certified_e_pi_gt_8539732)

lemma e_pi_lt_853973478: "(exp (1 :: real)) * pi < (853973478 :: real) / 100000000"
  by (rule certified_e_pi_lt_853973478)

lemma e_pi_lt_85397348: "(exp (1 :: real)) * pi < (85397348 :: real) / 10000000"
  by (rule certified_e_pi_lt_85397348)

lemma e_pi_lt_8539736: "(exp (1 :: real)) * pi < (8539736 :: real) / 1000000"
  by (rule certified_e_pi_lt_8539736)

lemma pi_half_gt_02956: "(0.295612 :: real) < pi / 2"
  by (rule certified_pi_half_gt_02956)

lemma pi_half_gt_1156: "(1.15572734986 :: real) < pi / 2"
  by (rule certified_pi_half_gt_1156)

lemma pi_gt_290272: "(0.290272 :: real) < pi"
  by (rule certified_pi_gt_290272)

lemma pi_gt_291325: "(0.291325 :: real) < pi"
  by (rule certified_pi_gt_291325)

lemma pi_gt_0415068: "(0.415068 :: real) < pi"
  by (rule certified_pi_gt_0415068)

lemma pi_gt_0415069: "(0.415069 :: real) < pi"
  by (rule certified_pi_gt_0415069)

lemma pi_div_e_gt_115572734973: "(1.15572734973 :: real) < pi / (exp (1 :: real))"
  by (rule certified_pi_div_e_gt_115572734973)

lemma pi_div_e_lt_115572734986: "pi / (exp (1 :: real)) < (1.15572734986 :: real)"
  by (rule certified_pi_div_e_lt_115572734986)

lemma pi_div_e_in_Icc_sin: "- (pi / 2) \<le> pi / (exp (1 :: real)) \<and> pi / (exp (1 :: real)) \<le> pi / 2"
  by (rule certified_pi_div_e_in_Icc_sin)

lemma exp_04807_lt_1618: "exp (0.4807 :: real) < (1.618 :: real)"
  by (rule certified_exp_04807_lt_1618)

lemma exp_01530_gt_11653: "(1.1653 :: real) < exp (0.1530 :: real)"
  by (rule certified_exp_01530_gt_11653)

lemma exp_01534_lt_1168: "exp (0.1534 :: real) < (1.168 :: real)"
  by (rule certified_exp_01534_lt_1168)

lemma exp_1146_gt_31416: "(3.1416 :: real) < exp (1.146 :: real)"
  by (rule certified_exp_1146_gt_31416)

lemma exp_11453_gt_pi23847: "(3.14159265358979323847 :: real) < exp (1.1453 :: real)"
  by (rule certified_exp_11453_gt_pi23847)

lemma exp_02903_lt_1338: "exp (0.2903 :: real) < (1.338 :: real)"
  by (rule certified_exp_02903_lt_1338)

lemma exp_consciousness_phase_lt_132: "exp (0.2903 :: real) < (1.338 :: real)"
  by (rule certified_exp_consciousness_phase_lt_132)

lemma exp_1434_gt_4167: "(4.167 :: real) < exp (1.434 :: real)"
  by (rule certified_exp_1434_gt_4167)

lemma exp_neg_1434_lt_24_div_25: "exp (-1.434) < (6 :: real) / 25"
  by (rule certified_exp_neg_1434_lt_24_div_25)

lemma exp_040_lt_25_div_24: "exp (0.040 :: real) < (25 :: real) / 24"
  by (rule certified_exp_040_lt_25_div_24)

end
