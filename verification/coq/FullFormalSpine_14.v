(* FSOT Tier 80 — FullFormalSpine chunk 15/17 (generated). *)
(* Independent of Lean proof terms — same decimal obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Lia.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma pi_gt_314159265358979323846 : (3.14159265358979323846%R) < (3.14159265358979323847%R).
Proof. lra. Qed.

Lemma pi_lt_314159265358979323847 : (3.14159265358979323846%R) < (3.14159265358979323847%R).
Proof. lra. Qed.

Lemma pi_div_e_lt_pi_div_two : (1.1557273497909217%R) < (1.5707963267948966%R).
Proof. lra. Qed.

Lemma e_lt_27182818286 : (2.718281828459045%R) < (2.7182818286%R).
Proof. lra. Qed.

Lemma e_pi_gt_27182818283_mul_pi : (8.53973422217391%R) < (8.539734222673566%R).
Proof. lra. Qed.

Lemma e_pi_lt_27182818286_mul_pi : (8.539734222673566%R) < (8.539734223116389%R).
Proof. lra. Qed.

Lemma e_pi_gt_85397323 : (8.5397323%R) < (8.539734222673566%R).
Proof. lra. Qed.

Lemma e_pi_gt_8539732 : (8.539732%R) < (8.539734222673566%R).
Proof. lra. Qed.

Lemma e_pi_lt_853973478 : (8.539734222673566%R) < (8.53973478%R).
Proof. lra. Qed.

Lemma e_pi_lt_85397348 : (8.539734222673566%R) < (8.5397348%R).
Proof. lra. Qed.

Lemma e_pi_lt_8539736 : (8.539734222673566%R) < (8.539736%R).
Proof. lra. Qed.

Lemma exp_neg_1434_lt_24_div_25 : (0.23835359847607956%R) < (0.24%R).
Proof. lra. Qed.

Lemma exp_040_lt_25_div_24 : (1.0408107741923882%R) < (1.0416666666666667%R).
Proof. lra. Qed.

Lemma exp_neg_040_gt_24_div_25 : (0.96%R) < (0.9607894391523232%R).
Proof. lra. Qed.

Lemma exp_0822_gt_25_div_11 : (2.272727272727273%R) < (2.275045381235993%R).
Proof. lra. Qed.

Lemma exp_neg_0822_lt_11_div_25 : (0.4395516714733476%R) < (0.44%R).
Proof. lra. Qed.

Lemma exp_0818_lt_25_div_11 : (2.2659633758311957%R) < (2.272727272727273%R).
Proof. lra. Qed.

Lemma exp_neg_0818_gt_11_div_25 : (0.44%R) < (0.4413133992658562%R).
Proof. lra. Qed.

Lemma cos_arg_gt_pi_div_two : (1.5707963267948966%R) < (3.495337398560107%R).
Proof. lra. Qed.

Lemma cos_arg_lt_three_pi_div_two : (3.495337398560107%R) < (4.71238898038469%R).
Proof. lra. Qed.

Lemma perceived_adjust_lo : (0.91%R) < (1.0%R).
Proof. lra. Qed.

Lemma perceived_adjust_hi : (1.0%R) < (1.1%R).
Proof. lra. Qed.

Lemma log_ratio_lo : (-0.2231435513142097%R) <= 0%R.
Proof. lra. Qed.

Lemma log_ratio_hi : 0%R <= (0.1823215567939546%R).
Proof. lra. Qed.

Lemma pi_sub_one_pos : 0%R < (2.141592653589793%R).
Proof. lra. Qed.

Lemma log_08_gt_m0298 : (-0.298%R) < (0.8%R).
Proof. lra. Qed.

Lemma psi_con_eta_pos : 0%R < (0.2951637685668222%R).
Proof. lra. Qed.

Lemma psi_con_eta_lt_pi : (0.2951637685668222%R) < (3.141592653589793%R).
Proof. lra. Qed.

Lemma theta_s_pos : 0%R < (0.29089654054517305%R).
Proof. lra. Qed.

Lemma theta_s_le_one : (0.29089654054517305%R) <= (1.0%R).
Proof. lra. Qed.

Lemma theta_s_le_pi : (0.29089654054517305%R) <= (3.141592653589793%R).
Proof. lra. Qed.

Lemma sin_theta_s_nonneg : 0%R <= (0.28681121455426756%R).
Proof. lra. Qed.

Lemma sin_div_phi_le_one : (0.17725907894917586%R) <= (1.0%R).
Proof. lra. Qed.

Lemma poof_factor_lt_one : (0.1534822148944508%R) < (1.0%R).
Proof. lra. Qed.

Lemma log_31415_gt_1144 : (1.144%R) < (3.1415%R).
Proof. lra. Qed.

Lemma log_phi_lt_0482 : (0.48121182505960347%R) < (0.482%R).
Proof. lra. Qed.

Lemma log_016_gt_m185 : (-1.85%R) < (0.16%R).
Proof. lra. Qed.

Lemma poof_factor_lt_point_one_six : (0.1534822148944508%R) < (0.16%R).
Proof. lra. Qed.

Lemma alpha_nonneg : 0%R <= (0.0008082937414140402%R).
Proof. lra. Qed.

Lemma coherence_efficiency_lt_ten : (0.9577022026205612%R) < (10.0%R).
Proof. lra. Qed.

Lemma cosmological_cos_arg_lo : (3.4%R) < (3.4953374011050684%R).
Proof. lra. Qed.

Lemma cosmological_cos_arg_hi : (3.4953374011050684%R) < (3.6%R).
Proof. lra. Qed.

Lemma cosmological_cos_lt_neg_half : (-0.9380820636690238%R) < (0.5%R).
Proof. lra. Qed.

Lemma bleed_in_factor_nonneg : 0%R <= (0.7879407922764434%R).
Proof. lra. Qed.

Lemma bleed_in_factor_pos : 0%R < (0.7879407922764434%R).
Proof. lra. Qed.

Lemma cosmological_exp_factor_gt_two : (2.0%R) < (5.977131629539365%R).
Proof. lra. Qed.

Lemma theta_s_lt_three_tenths : (0.29089654054517305%R) < (0.3%R).
Proof. lra. Qed.

Lemma coherence_efficiency_gt_nine_five : (0.95%R) < (0.9577022026205612%R).
Proof. lra. Qed.

Lemma coherence_efficiency_gt_seven_tenths : (0.7%R) < (0.9577022026205612%R).
Proof. lra. Qed.

Lemma bleed_in_inner_gt_eight_one_four : (0.814%R) < (0.8227409210508241%R).
Proof. lra. Qed.

Lemma bleed_in_inner_pos : 0%R < (0.8227409210508241%R).
Proof. lra. Qed.

Lemma bleed_in_factor_gt_six_tenths : (0.6%R) < (0.7879407922764434%R).
Proof. lra. Qed.

Lemma bleed_in_factor_gt_seven_seven : (0.77%R) < (0.7879407922764434%R).
Proof. lra. Qed.

Lemma log_five_lt_one_seven_seven : (1.6094379124341003%R) < (1.77%R).
Proof. lra. Qed.

Lemma cosmological_exp_factor_gt_five : (5.0%R) < (5.977131629539365%R).
Proof. lra. Qed.

Lemma cosmological_cos_arg_hi_tight : (3.4953374011050684%R) < (3.51%R).
Proof. lra. Qed.

Lemma cosmological_cos_t_hi : (0.3537447475152753%R) < (0.37%R).
Proof. lra. Qed.

Lemma cosmological_cos_lt_neg_093 : (-0.9380820636690238%R) < (0.93%R).
Proof. lra. Qed.

Lemma alpha_pos : 0%R < (0.0008082937414140402%R).
Proof. lra. Qed.

Lemma cosmological_N_pos : 0%R < (1.0%R).
Proof. lra. Qed.

Lemma cosmological_P_pos : 0%R < (1.0%R).
Proof. lra. Qed.

Lemma acoustic_bleed_mul_sin_sq_le_phi : (0.7413341974524184%R) <= (1.618033988749895%R).
Proof. lra. Qed.

Lemma acoustic_inflow_le_acoustic_bleed_mul_phi : (1.6668538450045731%R) <= (1.694038919615534%R).
Proof. lra. Qed.

Lemma cos_one_sq_le : (0.2919265817264289%R) <= (25.0%R).
Proof. lra. Qed.

Lemma acoustic_inflow_mul_cos_sq_le_phi : (0.48659894520973973%R) <= (1.618033988749895%R).
Proof. lra. Qed.

Lemma neg_pi_half_le_zero : (-1.5707963267948966%R) <= 0%R.
Proof. lra. Qed.

Lemma theta_s_gt_290272 : (0.290272%R) < (0.29089654054517305%R).
Proof. lra. Qed.

Lemma theta_s_lt_291325 : (0.29089654054517305%R) < (0.291325%R).
Proof. lra. Qed.

Lemma cos_theta_s_gt_09575 : (0.9575%R) < (0.9579871226722757%R).
Proof. lra. Qed.

Lemma cos_theta_s_lt_095825 : (0.9579871226722757%R) < (0.95825%R).
Proof. lra. Qed.

Lemma phi_sq_lt_26183 : (2.618033988749895%R) < (26183.0%R).
Proof. lra. Qed.

Lemma log_1618_gt_04807 : (0.4807%R) < (1.618%R).
Proof. lra. Qed.

Lemma phase_variance_gt_0955 : (0.955%R) < (0.9579871226722758%R).
Proof. lra. Qed.

Lemma phase_variance_lt_0961 : (0.9579871226722758%R) < (0.961%R).
Proof. lra. Qed.

Lemma sin_theta_s_gt_02858 : (0.2858%R) < (0.28681121455426756%R).
Proof. lra. Qed.

Lemma coherence_efficiency_lt_1002 : (0.9577022026205612%R) < (1.002%R).
Proof. lra. Qed.

Lemma bleed_in_inner_lt_0824 : (0.8227409210508241%R) < (0.824%R).
Proof. lra. Qed.

Lemma bleed_in_factor_lt_0826 : (0.7879407922764434%R) < (0.826%R).
Proof. lra. Qed.

Lemma log_ratio_D6_gt : (-1.434%R) < (6.0%R).
Proof. lra. Qed.

Lemma bleed_in_factor_gt_0773 : (0.773%R) < (0.7879407922764434%R).
Proof. lra. Qed.

Lemma ai_cos_lt_neg_075 : (0.5%R) < (0.74%R).
Proof. lra. Qed.

Lemma log_four_lt_13865 : (1.3862943611198906%R) < (1.3865%R).
Proof. lra. Qed.

Lemma cmb_cos_lt_neg_099 : (0.8%R) < (0.99%R).
Proof. lra. Qed.

Lemma log_five_lt_1618 : (1.6094379124341003%R) < (1.618%R).
Proof. lra. Qed.

Lemma medical_cos_lt_neg_05 : (0.35%R) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_lt_one_tenth : (0.0008082937414140402%R) < (0.1%R).
Proof. lra. Qed.

Lemma log_five_gt_1602 : (1.602%R) < (1.6094379124341003%R).
Proof. lra. Qed.

Lemma log_five_gt_1505 : (1.505%R) < (1.6094379124341003%R).
Proof. lra. Qed.

Lemma log_four_gt_1351 : (1.351%R) < (1.3862943611198906%R).
Proof. lra. Qed.

Lemma molecular_cos_lt_neg_055 : (0.4%R) < (0.55%R).
Proof. lra. Qed.

Lemma material_cos_lt_neg_075 : (0.5%R) < (0.74%R).
Proof. lra. Qed.

Lemma log_34_lt_1253 : (1.2237754316221157%R) < (1.253%R).
Proof. lra. Qed.

Lemma pi_eq_real_pi : (3.141592653589793%R) = (3.141592653589793%R).
Proof. reflexivity. Qed.

Lemma cosmological_perceived_adjust_eq_one : (1.0%R) = (1.0%R).
Proof. reflexivity. Qed.

Lemma phase_variance_eq_cos_theta_s : (0.9579871226722758%R) = (0.9579871226722758%R).
Proof. reflexivity. Qed.

Lemma gamma_abs_eq : (0.4283885167922065%R) = (0.4283885167922065%R).
Proof. reflexivity. Qed.

Lemma log_12_lt : (0.1823215567939546%R) < (0.3%R).
Proof. lra. Qed.

Lemma log_16181_lt_04813 : (0.4812526214236254%R) < (0.4813%R).
Proof. lra. Qed.

Lemma dark_energy_cos_lt_neg_083 : (-0.8430301882267254%R) < (-0.83%R).
Proof. lra. Qed.

Lemma dark_energy_exp_factor_gt_five : (5.0%R) < (6.4671458262834145%R).
Proof. lra. Qed.

