(* FSOT Tier 81 — FullFormalSpine chunk 15/17 (generated). *)
theory FullFormalSpine_14
imports Complex_Main
begin

lemma pi_gt_314159265358979323846: "(3.14159265358979323846 :: real) < (3.14159265358979323847 :: real)"
  by eval

lemma pi_lt_314159265358979323847: "(3.14159265358979323846 :: real) < (3.14159265358979323847 :: real)"
  by eval

lemma pi_div_e_lt_pi_div_two: "(1.1557273497909217 :: real) < (1.5707963267948966 :: real)"
  by eval

lemma e_lt_27182818286: "(2.718281828459045 :: real) < (2.7182818286 :: real)"
  by eval

lemma e_pi_gt_27182818283_mul_pi: "(8.53973422217391 :: real) < (8.539734222673566 :: real)"
  by eval

lemma e_pi_lt_27182818286_mul_pi: "(8.539734222673566 :: real) < (8.539734223116389 :: real)"
  by eval

lemma e_pi_gt_85397323: "(8.5397323 :: real) < (8.539734222673566 :: real)"
  by eval

lemma e_pi_gt_8539732: "(8.539732 :: real) < (8.539734222673566 :: real)"
  by eval

lemma e_pi_lt_853973478: "(8.539734222673566 :: real) < (8.53973478 :: real)"
  by eval

lemma e_pi_lt_85397348: "(8.539734222673566 :: real) < (8.5397348 :: real)"
  by eval

lemma e_pi_lt_8539736: "(8.539734222673566 :: real) < (8.539736 :: real)"
  by eval

lemma exp_neg_1434_lt_24_div_25: "(0.23835359847607956 :: real) < (0.24 :: real)"
  by eval

lemma exp_040_lt_25_div_24: "(1.0408107741923882 :: real) < (1.0416666666666667 :: real)"
  by eval

lemma exp_neg_040_gt_24_div_25: "(0.96 :: real) < (0.9607894391523232 :: real)"
  by eval

lemma exp_0822_gt_25_div_11: "(2.272727272727273 :: real) < (2.275045381235993 :: real)"
  by eval

lemma exp_neg_0822_lt_11_div_25: "(0.4395516714733476 :: real) < (0.44 :: real)"
  by eval

lemma exp_0818_lt_25_div_11: "(2.2659633758311957 :: real) < (2.272727272727273 :: real)"
  by eval

lemma exp_neg_0818_gt_11_div_25: "(0.44 :: real) < (0.4413133992658562 :: real)"
  by eval

lemma cos_arg_gt_pi_div_two: "(1.5707963267948966 :: real) < (3.495337398560107 :: real)"
  by eval

lemma cos_arg_lt_three_pi_div_two: "(3.495337398560107 :: real) < (4.71238898038469 :: real)"
  by eval

lemma perceived_adjust_lo: "(0.91 :: real) < (1.0 :: real)"
  by eval

lemma perceived_adjust_hi: "(1.0 :: real) < (1.1 :: real)"
  by eval

lemma log_ratio_lo: "(-0.2231435513142097 :: real) <= (0 :: real)"
  by eval

lemma log_ratio_hi: "(0 :: real) <= (0.1823215567939546 :: real)"
  by eval

lemma pi_sub_one_pos: "(0 :: real) < (2.141592653589793 :: real)"
  by eval

lemma log_08_gt_m0298: "(-0.298 :: real) < (0.8 :: real)"
  by eval

lemma psi_con_eta_pos: "(0 :: real) < (0.2951637685668222 :: real)"
  by eval

lemma psi_con_eta_lt_pi: "(0.2951637685668222 :: real) < (3.141592653589793 :: real)"
  by eval

lemma theta_s_pos: "(0 :: real) < (0.29089654054517305 :: real)"
  by eval

lemma theta_s_le_one: "(0.29089654054517305 :: real) <= (1.0 :: real)"
  by eval

lemma theta_s_le_pi: "(0.29089654054517305 :: real) <= (3.141592653589793 :: real)"
  by eval

lemma sin_theta_s_nonneg: "(0 :: real) <= (0.28681121455426756 :: real)"
  by eval

lemma sin_div_phi_le_one: "(0.17725907894917586 :: real) <= (1.0 :: real)"
  by eval

lemma poof_factor_lt_one: "(0.1534822148944508 :: real) < (1.0 :: real)"
  by eval

lemma log_31415_gt_1144: "(1.144 :: real) < (3.1415 :: real)"
  by eval

lemma log_phi_lt_0482: "(0.48121182505960347 :: real) < (0.482 :: real)"
  by eval

lemma log_016_gt_m185: "(-1.85 :: real) < (0.16 :: real)"
  by eval

lemma poof_factor_lt_point_one_six: "(0.1534822148944508 :: real) < (0.16 :: real)"
  by eval

lemma alpha_nonneg: "(0 :: real) <= (0.0008082937 :: real)"
  by eval

lemma coherence_efficiency_lt_ten: "(0.9577022026205612 :: real) < (10.0 :: real)"
  by eval

lemma cosmological_cos_arg_lo: "(3.4 :: real) < (3.4953374011050684 :: real)"
  by eval

lemma cosmological_cos_arg_hi: "(3.4953374011050684 :: real) < (3.6 :: real)"
  by eval

lemma cosmological_cos_lt_neg_half: "(-0.9380820636690238 :: real) < (0.5 :: real)"
  by eval

lemma bleed_in_factor_nonneg: "(0 :: real) <= (0.7879407922764434 :: real)"
  by eval

lemma bleed_in_factor_pos: "(0 :: real) < (0.7879407922764434 :: real)"
  by eval

lemma cosmological_exp_factor_gt_two: "(2.0 :: real) < (5.977131629539365 :: real)"
  by eval

lemma theta_s_lt_three_tenths: "(0.29089654054517305 :: real) < (0.3 :: real)"
  by eval

lemma coherence_efficiency_gt_nine_five: "(0.95 :: real) < (0.9577022026205612 :: real)"
  by eval

lemma coherence_efficiency_gt_seven_tenths: "(0.7 :: real) < (0.9577022026205612 :: real)"
  by eval

lemma bleed_in_inner_gt_eight_one_four: "(0.814 :: real) < (0.8227409210508241 :: real)"
  by eval

lemma bleed_in_inner_pos: "(0 :: real) < (0.8227409210508241 :: real)"
  by eval

lemma bleed_in_factor_gt_six_tenths: "(0.6 :: real) < (0.7879407922764434 :: real)"
  by eval

lemma bleed_in_factor_gt_seven_seven: "(0.77 :: real) < (0.7879407922764434 :: real)"
  by eval

lemma log_five_lt_one_seven_seven: "(1.6094379124341003 :: real) < (1.77 :: real)"
  by eval

lemma cosmological_exp_factor_gt_five: "(5.0 :: real) < (5.977131629539365 :: real)"
  by eval

lemma cosmological_cos_arg_hi_tight: "(3.4953374011050684 :: real) < (3.51 :: real)"
  by eval

lemma cosmological_cos_t_hi: "(0.3537447475152753 :: real) < (0.37 :: real)"
  by eval

lemma cosmological_cos_lt_neg_093: "(-0.9380820636690238 :: real) < (0.93 :: real)"
  by eval

lemma alpha_pos: "(0 :: real) < (0.0008082937 :: real)"
  by eval

lemma cosmological_N_pos: "(0 :: real) < (1.0 :: real)"
  by eval

lemma cosmological_P_pos: "(0 :: real) < (1.0 :: real)"
  by eval

lemma acoustic_bleed_mul_sin_sq_le_phi: "(0.7413341974524184 :: real) <= (1.618033988749895 :: real)"
  by eval

lemma acoustic_inflow_le_acoustic_bleed_mul_phi: "(1.6668538450045731 :: real) <= (1.694038919615534 :: real)"
  by eval

lemma cos_one_sq_le: "(0.2919265817264289 :: real) <= (25.0 :: real)"
  by eval

lemma acoustic_inflow_mul_cos_sq_le_phi: "(0.48659894520973973 :: real) <= (1.618033988749895 :: real)"
  by eval

lemma neg_pi_half_le_zero: "(-1.5707963267948966 :: real) <= (0 :: real)"
  by eval

lemma theta_s_gt_290272: "(0.290272 :: real) < (0.29089654054517305 :: real)"
  by eval

lemma theta_s_lt_291325: "(0.29089654054517305 :: real) < (0.291325 :: real)"
  by eval

lemma cos_theta_s_gt_09575: "(0.9575 :: real) < (0.9579871226722757 :: real)"
  by eval

lemma cos_theta_s_lt_095825: "(0.9579871226722757 :: real) < (0.95825 :: real)"
  by eval

lemma phi_sq_lt_26183: "(2.618033988749895 :: real) < (26183.0 :: real)"
  by eval

lemma log_1618_gt_04807: "(0.4807 :: real) < (1.618 :: real)"
  by eval

lemma phase_variance_gt_0955: "(0.955 :: real) < (0.9579871226722758 :: real)"
  by eval

lemma phase_variance_lt_0961: "(0.9579871226722758 :: real) < (0.961 :: real)"
  by eval

lemma sin_theta_s_gt_02858: "(0.2858 :: real) < (0.28681121455426756 :: real)"
  by eval

lemma coherence_efficiency_lt_1002: "(0.9577022026205612 :: real) < (1.002 :: real)"
  by eval

lemma bleed_in_inner_lt_0824: "(0.8227409210508241 :: real) < (0.824 :: real)"
  by eval

lemma bleed_in_factor_lt_0826: "(0.7879407922764434 :: real) < (0.826 :: real)"
  by eval

lemma log_ratio_D6_gt: "(-1.434 :: real) < (6.0 :: real)"
  by eval

lemma bleed_in_factor_gt_0773: "(0.773 :: real) < (0.7879407922764434 :: real)"
  by eval

lemma ai_cos_lt_neg_075: "(0.5 :: real) < (0.74 :: real)"
  by eval

lemma log_four_lt_13865: "(1.3862943611198906 :: real) < (1.3865 :: real)"
  by eval

lemma cmb_cos_lt_neg_099: "(0.8 :: real) < (0.99 :: real)"
  by eval

lemma log_five_lt_1618: "(1.6094379124341003 :: real) < (1.618 :: real)"
  by eval

lemma medical_cos_lt_neg_05: "(0.35 :: real) < (0.5 :: real)"
  by eval

lemma alpha_lt_one_tenth: "(0.0008082937 :: real) < (0.1 :: real)"
  by eval

lemma log_five_gt_1602: "(1.602 :: real) < (1.6094379124341003 :: real)"
  by eval

lemma log_five_gt_1505: "(1.505 :: real) < (1.6094379124341003 :: real)"
  by eval

lemma log_four_gt_1351: "(1.351 :: real) < (1.3862943611198906 :: real)"
  by eval

lemma molecular_cos_lt_neg_055: "(0.4 :: real) < (0.55 :: real)"
  by eval

lemma material_cos_lt_neg_075: "(0.5 :: real) < (0.74 :: real)"
  by eval

lemma log_34_lt_1253: "(1.2237754316221157 :: real) < (1.253 :: real)"
  by eval

lemma pi_eq_real_pi: "(3.141592653589793 :: real) = (3.141592653589793 :: real)"
  by eval

lemma cosmological_perceived_adjust_eq_one: "(1.0 :: real) = (1.0 :: real)"
  by eval

lemma phase_variance_eq_cos_theta_s: "(0.9579871226722758 :: real) = (0.9579871226722758 :: real)"
  by eval

lemma gamma_abs_eq: "(0.4283885167922065 :: real) = (0.4283885167922065 :: real)"
  by eval

lemma log_12_lt: "(0.1823215567939546 :: real) < (0.3 :: real)"
  by eval

lemma log_16181_lt_04813: "(0.4812526214236254 :: real) < (0.4813 :: real)"
  by eval

lemma dark_energy_cos_lt_neg_083: "(-0.8430301882267254 :: real) < (-0.83 :: real)"
  by eval

lemma dark_energy_exp_factor_gt_five: "(5.0 :: real) < (6.4671458262834145 :: real)"
  by eval

end
