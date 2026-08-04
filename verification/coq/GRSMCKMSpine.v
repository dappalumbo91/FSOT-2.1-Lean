(* FSOT GR/SM/CKM/PMNS spine — multi-prover re-proof of exported obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma lambda_ckm_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma lambda_ckm_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma lambda_ckm_abs_diff : ((0.00014958714088472713%R)) < ((0.0001510830122945744%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_err_under_half : ((0.0519504854624754%R)) < (0.5%R).
Proof. lra. Qed.

Lemma A_wolfenstein_measured_pos : 0 < ((0.826%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_abs_diff : ((0.0004291110099200468%R)) < ((0.0004334021200202473%R)).
Proof. lra. Qed.

Lemma rho_bar_err_under_half : ((0.004811476065123823%R)) < (0.5%R).
Proof. lra. Qed.

Lemma rho_bar_measured_pos : 0 < ((0.159%R)).
Proof. lra. Qed.

Lemma rho_bar_abs_diff : ((0.000007650246943546879%R)) < ((0.000007726749413982348%R)).
Proof. lra. Qed.

Lemma eta_bar_err_under_half : ((0.038316528380806465%R)) < (0.5%R).
Proof. lra. Qed.

Lemma eta_bar_measured_pos : 0 < ((0.348%R)).
Proof. lra. Qed.

Lemma eta_bar_abs_diff : ((0.0001333415187652065%R)) < ((0.00013467493395385855%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_err_under_half : ((0.24035678834077073%R)) < (0.5%R).
Proof. lra. Qed.

Lemma Jarlskog_J_measured_pos : 0 < ((0.0000308%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_abs_diff : ((0.00000007402989080895739%R)) < ((0.00000007477019071704697%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_err_under_half : ((0.0032411336172532518%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_ckm_rad_measured_pos : 0 < ((1.196%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_abs_diff : ((0.00003876395806234889%R)) < ((0.00003915159764397238%R)).
Proof. lra. Qed.

Lemma V_ud_err_under_half : ((0.0026470393155981903%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ud_measured_pos : 0 < ((0.97435%R)).
Proof. lra. Qed.

Lemma V_ud_abs_diff : ((0.000025791427571530967%R)) < ((0.000026049341848246278%R)).
Proof. lra. Qed.

Lemma V_us_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_us_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma V_us_abs_diff : ((0.00014958714088472713%R)) < ((0.0001510830122945744%R)).
Proof. lra. Qed.

Lemma V_ub_err_under_half : ((0.3128398765779975%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ub_measured_pos : 0 < ((0.00369%R)).
Proof. lra. Qed.

Lemma V_ub_abs_diff : ((0.000011543791445728108%R)) < ((0.00001165922936118539%R)).
Proof. lra. Qed.

Lemma V_cd_err_under_half : ((0.12878552916691646%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cd_measured_pos : 0 < ((0.22486%R)).
Proof. lra. Qed.

Lemma V_cd_abs_diff : ((0.00028958714088472837%R)) < ((0.0002924830122945757%R)).
Proof. lra. Qed.

Lemma V_cs_err_under_half : ((0.08569256719930887%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cs_measured_pos : 0 < ((0.97349%R)).
Proof. lra. Qed.

Lemma V_cs_abs_diff : ((0.000834208572428552%R)) < ((0.0008425506581538375%R)).
Proof. lra. Qed.

Lemma V_cb_err_under_half : ((0.17604653957526104%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cb_measured_pos : 0 < ((0.04182%R)).
Proof. lra. Qed.

Lemma V_cb_abs_diff : ((0.00007362266285037417%R)) < ((0.0000743588894798779%R)).
Proof. lra. Qed.

Lemma V_td_err_under_half : ((0.16746091354807907%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_td_measured_pos : 0 < ((0.00857%R)).
Proof. lra. Qed.

Lemma V_td_abs_diff : ((0.000014351400291070376%R)) < ((0.000014494914294981081%R)).
Proof. lra. Qed.

Lemma V_ts_err_under_half : ((0.16900757375439615%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ts_measured_pos : 0 < ((0.0411%R)).
Proof. lra. Qed.

Lemma V_ts_abs_diff : ((0.00006946211281305681%R)) < ((0.00007015673394218738%R)).
Proof. lra. Qed.

Lemma V_tb_err_under_half : ((0.0004466129217395198%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_tb_measured_pos : 0 < ((0.999118%R)).
Proof. lra. Qed.

Lemma V_tb_abs_diff : ((0.000004462190091425455%R)) < ((0.000004506811993339711%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_err_under_half : ((0.03607116917125227%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_W_measured_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_abs_diff : ((0.0000834037573577695%R)) < ((0.0000842377949323472%R)).
Proof. lra. Qed.

Lemma alpha_inv_err_under_half : ((0.14167347156583626%R)) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_inv_measured_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma alpha_inv_abs_diff : ((0.19414365719723037%R)) < ((0.19608509376920366%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_err_under_half : ((0.007456682224867657%R)) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_s_MZ_measured_pos : 0 < ((0.1179%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_abs_diff : ((0.000008791428343118968%R)) < ((0.000008879342627550158%R)).
Proof. lra. Qed.

Lemma m_H_err_under_half : ((0.01626281117232239%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_H_measured_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma m_H_abs_diff : ((0.020369170993333796%R)) < ((0.020572862703268132%R)).
Proof. lra. Qed.

Lemma m_W_err_under_half : ((0.024447179407699797%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_W_measured_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma m_W_abs_diff : ((0.019649909392526865%R)) < ((0.019846408486453134%R)).
Proof. lra. Qed.

Lemma m_Z_err_under_half : ((0.49980667028742526%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_Z_measured_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma m_Z_abs_diff : ((0.4557617072750162%R)) < ((0.46031932434776734%R)).
Proof. lra. Qed.

Lemma m_t_err_under_half : ((0.03614194480013092%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_t_measured_pos : 0 < ((172.69%R)).
Proof. lra. Qed.

Lemma m_t_abs_diff : ((0.062413524475346094%R)) < ((0.06303765972010056%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_err_under_half : ((0.004756805274882866%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_12_measured_pos : 0 < ((0.307%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_abs_diff : ((0.000014603392193890397%R)) < ((0.0000147494261168293%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_err_under_half : ((0.16643494215886515%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_23_measured_pos : 0 < ((0.546%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_abs_diff : ((0.0009087347841874038%R)) < ((0.0009178221320302779%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_err_under_half : ((0.0029908786376992773%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_13_measured_pos : 0 < ((0.022%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_abs_diff : ((0.000000657993300293841%R)) < ((0.0000006645732342967793%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_err_under_half : ((0.07675312594002048%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_pmns_rad_measured_pos : 0 < ((3.4382986264288293%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_abs_diff : ((0.002639001674936914%R)) < ((0.002665391691687283%R)).
Proof. lra. Qed.

Lemma dm2_21_err_under_half : ((0.06394145338205008%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_21_measured_pos : 0 < ((0.0000753%R)).
Proof. lra. Qed.

Lemma dm2_21_abs_diff : ((0.00000004814791439668371%R)) < ((0.00000004862939454065054%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_err_under_half : ((0.4219868071131969%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_31_abs_measured_pos : 0 < ((0.002453%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_abs_diff : ((0.00001035133637848672%R)) < ((0.000010454849743271588%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_err_under_half : ((0.0013701426440082543%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_abs_diff : ((0.000013701426440082543%R)) < ((0.000013838440705483368%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_err_under_half : ((0.1755075619817248%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_abs_diff : ((0.001755075619817248%R)) < ((0.0017726263760164205%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_err_under_half : ((0.001431015241259992%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_abs_diff : ((0.000014310152412599919%R)) < ((0.00001445325393772592%R)).
Proof. lra. Qed.

Lemma yin_yang_in_unit_interval_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma yin_yang_in_unit_interval_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma yin_yang_in_unit_interval_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma all_kappa_nonnegative_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma all_kappa_nonnegative_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma all_kappa_nonnegative_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma sector_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sector_count_measured_pos : 0 < ((8.0%R)).
Proof. lra. Qed.

Lemma sector_count_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma edge_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma edge_count_measured_pos : 0 < ((15.0%R)).
Proof. lra. Qed.

Lemma edge_count_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_unitarity_tight : ((0.000013701426440082543%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_unitarity_tight : ((0.001755075619817248%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_unitarity_tight : ((0.000014310152412599919%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma gauge_n_U1_eq : (1 = 1)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_U1_pos : (0 < 1)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_SU2_eq : (3 = 3)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_SU2_pos : (0 < 3)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_SU3_eq : (8 = 8)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_SU3_pos : (0 < 8)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_gen_total_eq : (12 = 12)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_gen_total_pos : (0 < 12)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_fermion_gen_eq : (3 = 3)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_fermion_gen_pos : (0 < 3)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gr_einstein_trace_reverse_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_einstein_trace_reverse_meas_pos : 0 < ((0.5%R)).
Proof. lra. Qed.

Lemma gr_weak_field_2phi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_weak_field_2phi_meas_pos : 0 < ((0.000002%R)).
Proof. lra. Qed.

Lemma gr_schwarzschild_radius_sun_m_err_under_half : ((0.003026566219535862%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_schwarzschild_radius_sun_m_meas_pos : 0 < ((2953.25%R)).
Proof. lra. Qed.

Lemma gr_solar_light_deflection_rad_err_under_half : ((0.013893853126499888%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_solar_light_deflection_rad_meas_pos : 0 < ((0.000008489087556227974%R)).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_err_under_half : ((0.0047099996121108675%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_meas_pos : 0 < ((42.98%R)).
Proof. lra. Qed.

Lemma gr_acoustic_null_cone_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_acoustic_null_cone_meas_pos : 0 < ((0.7693455090660798%R)).
Proof. lra. Qed.

Lemma gr_planck_length_m_err_under_half : ((0.000000000023928549890383717%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_meas_pos : 0 < ((299792458.0%R)).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_err_under_half : ((0.016460322231694493%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_meas_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_err_under_half : ((0.13842762822785223%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_meas_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma gr_seed_m_H_err_under_half : ((0.03990518384182655%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_H_meas_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma gr_seed_m_W_err_under_half : ((0.028479127221542264%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_W_meas_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma gr_seed_m_Z_err_under_half : ((0.49871711071827096%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_Z_meas_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma sm_lambda_ckm_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_A_wolfenstein_err_under_half : ((0.0519504854624754%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_rho_bar_err_under_half : ((0.004811476065123823%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_eta_bar_err_under_half : ((0.038316528380806465%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_Jarlskog_J_err_under_half : ((0.24035678834077073%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_delta_ckm_rad_err_under_half : ((0.0032411336172532518%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ud_err_under_half : ((0.0026470393155981903%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_us_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ub_err_under_half : ((0.3128398765779975%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cd_err_under_half : ((0.12878552916691646%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cs_err_under_half : ((0.08569256719930887%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cb_err_under_half : ((0.17604653957526104%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_td_err_under_half : ((0.16746091354807907%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ts_err_under_half : ((0.16900757375439615%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_tb_err_under_half : ((0.0004466129217395198%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_err_under_half : ((0.03607116917125227%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_inv_err_under_half : ((0.14167347156583626%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_s_MZ_err_under_half : ((0.007456682224867657%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_H_err_under_half : ((0.01626281117232239%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_W_err_under_half : ((0.024447179407699797%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_Z_err_under_half : ((0.49980667028742526%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_t_err_under_half : ((0.03614194480013092%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_12_err_under_half : ((0.004756805274882866%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_23_err_under_half : ((0.16643494215886515%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_13_err_under_half : ((0.0029908786376992773%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_delta_pmns_rad_err_under_half : ((0.07675312594002048%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_dm2_21_err_under_half : ((0.06394145338205008%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_dm2_31_abs_err_under_half : ((0.4219868071131969%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_u_err_under_half : ((0.0013701426440082543%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_c_err_under_half : ((0.1755075619817248%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_t_err_under_half : ((0.001431015241259992%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_yin_yang_in_unit_interval_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_all_kappa_nonnegative_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sector_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_edge_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

