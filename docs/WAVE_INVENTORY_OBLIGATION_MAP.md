# Wave inventory → obligation map

**Generated:** 2026-08-05T21:42:26.563731+00:00  
**Status:** `MAPPED`  
**Waves:** 10 · **Observables:** 188 · **Linked obligations:** 127

Every `fsot_compute.waveN()` Result is inventoried against Lean modules and multiprover obligation IDs so wave numbers are never orphan atlas entries.

## Master formula

`S = K·(T1+T2+T3)` · structure module: `FSOT/Formal/ScalarEngineStructure.lean`

## Wave summary

| Wave | n | median% | max% | half-pct | Lean modules | #obl | Theme |
|-----:|--:|--------:|-----:|:--------:|--------------|-----:|-------|
| 1 | 5 | 0.11335 | 1.543111 | mixed | ✓ Cosmology, ✓ CosmologyLab | 24 | ΛCDM core (α_s, H0, T_CMB, n_s, Ω_b h²) |
| 2 | 10 | 0.002173 | 0.012986 | yes | ✓ Cosmology, ✓ CosmologyLab, ✓ CosmologyExtendedPriors | 31 | Extended SM / dark-sector anchors |
| 3 | 15 | 0.001927 | 0.240732 | yes | ✓ Cosmology, ✓ CosmologyLab, ✓ CosmologyExtendedPriors | 31 | CKM / age / acoustic-scale anchors |
| 4 | 16 | 0.011586 | 0.234682 | yes | ✓ CosmologyWave4Priors, ✓ CosmologyWave4 | 5 | PMNS + CKM depth |
| 5 | 22 | 0.002077 | 0.090986 | yes | ✓ CosmologyWave5Priors | 4 | Z-pole / electroweak precision |
| 6 | 22 | 0.000344 | 0.031298 | yes | ✓ CosmologyWave6Priors | 4 | Mathematical constants (ζ, Levy, …) |
| 7 | 29 | 0.003988 | 0.298055 | yes | ✓ CosmologyWave7Priors | 4 | Apéry / Soldner / number-theory constants |
| 8 | 52 | 0.014207 | 4.232801 | mixed | ✓ CosmologyWave8Priors, ✓ CosmologyHigherWavesPriors | 8 | CKM unitarity + BR / mass ratios |
| 9 | 7 | 0.014279 | 0.193758 | yes | ✓ CosmologyWave9Priors, ✓ CosmologyHigherWavesPriors | 8 | Top / radiation / fractal geometry |
| 10 | 10 | 0.000656 | 0.004079 | yes | ✓ CosmologyWave10Priors, ✓ CosmologyHigherWavesPriors | 8 | Lepton moments / logistic / triple-point |

## Per-wave observables

### Wave 1 — `wave1`

- **Theme:** ΛCDM core (α_s, H0, T_CMB, n_s, Ω_b h²)
- **Domain route:** `cosmological`
- **Lab key:** `cosmology_wave1_lab`
- **Obligations:** 24 (sample: c_cosm_pos, alpha_s_MZ_pos, p_base_pos, delta_lambda_cosm_pos, c_cosm_lt_061806, p_base_lt_0212371)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `alpha_s(M_Z)` | `1/(e·π)` | 0.678827 | · |
| `H0` | `100·(1 + S_cosm·A_bleed/A_in)` | 1.543111 | · |
| `T_CMB` | `φ² + P_base·\|S_cosm\|` | 0.027577 | ✓ |
| `n_s` | `1 + S_cosm·C_cosm·φ^(1/π)` | 0.11335 | ✓ |
| `Omega_b_h2` | `\|S_cosm\|·(1 − S_quant)` | 0.062029 | ✓ |

### Wave 2 — `wave2`

- **Theme:** Extended SM / dark-sector anchors
- **Domain route:** `cosmological`
- **Lab key:** `cosmology_wave2_lab`
- **Obligations:** 31 (sample: c_cosm_pos, alpha_s_MZ_pos, p_base_pos, delta_lambda_cosm_pos, c_cosm_lt_061806, p_base_lt_0212371)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `1/alpha_em` | `e³·φ⁴ − ψ_con` | 0.000144 | ✓ |
| `sin2_theta_W` | `√e·P_new·η_eff` | 0.012986 | ✓ |
| `M_W/M_Z` | `S_quant·ln(π) − P_base` | 0.002173 | ✓ |
| `Omega_Lambda` | `S_quant/e + γ²` | 0.0016 | ✓ |
| `Omega_m` | `C_eff·C·ln(π)` | 0.000311 | ✓ |
| `Omega_DM_h2` | `(1 − S_quant)·φ·A_in` | 0.000561 | ✓ |
| `sigma_8` | `\|S_cosm\|·S_quant + \|Chaos\|` | 0.00296 | ✓ |
| `tau_reion` | `φ·\|Chaos\| − ln(φ)` | 0.006335 | ✓ |
| `m_pi/m_p` | `K·P_new·ln(π)` | 0.001733 | ✓ |
| `N_eff` | `P_new·e·π + ln(φ)` | 0.009407 | ✓ |

### Wave 3 — `wave3`

- **Theme:** CKM / age / acoustic-scale anchors
- **Domain route:** `particle`
- **Lab key:** `cosmology_wave3_lab`
- **Obligations:** 31 (sample: c_cosm_pos, alpha_s_MZ_pos, p_base_pos, delta_lambda_cosm_pos, c_cosm_lt_061806, p_base_lt_0212371)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `|V_us|` | `θ_S/φ + (1 − S_quant)` | 0.009965 | ✓ |
| `|V_cb|` | `S_quant/C_eff − S_quant` | 0.001927 | ✓ |
| `sin_theta_C` | `φ/e³ + Suction` | 0.000507 | ✓ |
| `Age_Gyr` | `A_in·φ + φ⁵` | 0.001422 | ✓ |
| `z_eq` | `π⁵·φ⁵` | 0.240732 | ✓ |
| `theta_star` | `P_base·φ − γ²` | 0.059941 | ✓ |
| `r_star_Mpc` | `π³/P_base − φ` | 0.020889 | ✓ |
| `Deuteron_binding_MeV` | `√e/e + φ` | 6.1e-05 | ✓ |
| `Neutron_lifetime_s` | `π⁷·θ_S` | 0.021955 | ✓ |
| `Ising2D_beta` | `θ_S/φ⁵ + P_new` | 0.000735 | ✓ |
| `Ising2D_nu` | `√φ/ln(π) − ln(φ)` | 0.005634 | ✓ |
| `Ising2D_gamma` | `(1−S_quant)/ln(φ) + ln(π)` | 0.000674 | ✓ |
| `m_t/m_W` | `\|S_cosm\|/\|Chaos\| + ψ_con` | 0.009464 | ✓ |
| `m_H/m_W` | `S_quant·ψ_con + S_quant` | 9.5e-05 | ✓ |
| `m_tau/m_e` | `π⁷·ln(π) + e³` | 0.000732 | ✓ |

### Wave 4 — `wave4`

- **Theme:** PMNS + CKM depth
- **Domain route:** `particle`
- **Lab key:** `cosmology_wave4_lab`
- **Obligations:** 5 (sample: cosmology_wave4_max_error_under_half_pct, cosmology_wave4_median_error_under_half_pct, cosmology_wave4_observable_count_pos, cosmology_wave4_bundle, wave4_observable_count_pos)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `sin2_theta12` | `2·Poof` | 0.011586 | ✓ |
| `sin2_theta23` | `\|Chaos\|·√e` | 0.042745 | ✓ |
| `sin2_theta13` | `γ⁶·φ/e` | 0.068901 | ✓ |
| `Dm2_21/Dm2_32` | `γ³·Poof` | 0.057666 | ✓ |
| `|V_ub|` | `C_cosm²` | 0.008898 | ✓ |
| `|V_td|` | `√φ/e⁵` | 0.009346 | ✓ |
| `|V_ts|` | `γ⁵·ψ_con` | 0.00816 | ✓ |
| `Jarlskog_J` | `G/(π⁹)` | 0.234682 | ✓ |
| `Feigenbaum_delta` | `ln(π)·(e/G) + √φ` | 4.4e-05 | ✓ |
| `Feigenbaum_alpha` | `\|Chaos\|·φ·e + A_bleed` | 7.4e-05 | ✓ |
| `r_p_fm` | `G⁷ + P_new` | 0.018001 | ✓ |
| `m_n-m_p_MeV` | `γ⁴/\|Chaos\| + P_var` | 0.000217 | ✓ |
| `mu_p_muN` | `π·(1 − γ⁴)` | 7.9e-05 | ✓ |
| `w0` | `−P_new·π/G` | 0.001816 | ✓ |
| `m_c/m_b` | `C_cosm/P_base` | 0.017442 | ✓ |
| `alpha_s_ratio` | `π⁶·γ⁸` | 0.026302 | ✓ |

### Wave 5 — `wave5`

- **Theme:** Z-pole / electroweak precision
- **Domain route:** `particle`
- **Lab key:** `cosmology_wave5_lab`
- **Obligations:** 4 (sample: cosmology_wave5_max_error_under_half_pct, cosmology_wave5_median_error_under_half_pct, cosmology_wave5_observable_count_pos, cosmology_wave5_bundle)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `Gamma_Z/M_Z` | `φ⁵/e⁶` | 0.00079 | ✓ |
| `R_ell` | `G³/γ⁶` | 0.054141 | ✓ |
| `R_b` | `G/φ³` | 0.027673 | ✓ |
| `R_c` | `−ln(2) + e/π` | 0.005113 | ✓ |
| `A_FB_ell` | `A_in/π⁴` | 0.069544 | ✓ |
| `A_ell_SLD` | `γ³/√φ` | 0.073292 | ✓ |
| `m_H/m_t` | `A_bleed·ln(2)` | 0.014722 | ✓ |
| `BR_H_bb` | `C_eff/√e` | 0.004175 | ✓ |
| `BR_H_WW` | `ln(φ)/√5` | 0.002077 | ✓ |
| `BR_H_tautau` | `η_eff/e²` | 0.00988 | ✓ |
| `Y_p_He4` | `θ_S·sin(1)` | 0.048592 | ✓ |
| `D_H_ratio` | `1/(π⁴·e⁶)` | 0.090986 | ✓ |
| `Khinchin_K0` | `A_bleed/ln(3) + 1/γ` | 3e-05 | ✓ |
| `Glaisher_A` | `G⁴√5 − G/π` | 7.2e-05 | ✓ |
| `Twin_prime_C2` | `γ⁴/G⁴ + \|S_cosm\|` | 0.000692 | ✓ |
| `Mertens_M` | `−Poof·ln(2) + 1/e` | 0.001271 | ✓ |
| `Dottie_number` | `−G⁶/e³ + G³` | 9.5e-05 | ✓ |
| `Omega_constant` | `Suction/φ⁴ + sin(γ)` | 0.000316 | ✓ |
| `Conway_lambda` | `G⁵ln(3) + φ/e` | 0.000152 | ✓ |
| `Plastic_number` | `−G³πγ + e` | 0.000339 | ✓ |
| `Landau_Ramanujan` | `−1/(G³π⁵) + G³` | 6.5e-05 | ✓ |
| `Laplace_limit` | `G⁸C_cosm + ψ_con` | 6.2e-05 | ✓ |

### Wave 6 — `wave6`

- **Theme:** Mathematical constants (ζ, Levy, …)
- **Domain route:** `mathematical`
- **Lab key:** `cosmology_wave6_lab`
- **Obligations:** 4 (sample: cosmology_wave6_max_error_under_half_pct, cosmology_wave6_median_error_under_half_pct, cosmology_wave6_observable_count_pos, cosmology_wave6_bundle)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `zeta_5` | `π/3 − π⁻⁴` | 0.000344 | ✓ |
| `zeta_7` | `−√2·cos(1) + √π` | 0.000199 | ✓ |
| `Levy_constant` | `ψ_con·P_base + π` | 6.8e-05 | ✓ |
| `Erdos_Borwein` | `√2/G⁶ − B_in` | 0.000193 | ✓ |
| `Bernstein` | `−γ⁵φ/e + 1/π` | 0.000222 | ✓ |
| `Backhouse` | `√π/3 + e/π` | 7.4e-05 | ✓ |
| `Viswanath` | `πγ/φ³ + G⁴` | 0.000117 | ✓ |
| `Kepler_Bouwkamp` | `−γln(2) + φ/π` | 0.00104 | ✓ |
| `Sphere_packing_3D` | `√2φ/e − 1/π²` | 0.00036 | ✓ |
| `Gauss_AGM` | `A_bleed − P_base` | 0.000102 | ✓ |
| `Lemniscate` | `(e/φ)/G + B_in` | 9.6e-05 | ✓ |
| `Hashing_bound` | `−G⁷√3 + A_bleed` | 0.000712 | ✓ |
| `von_Karman` | `A_bleed/φ²` | 0.022915 | ✓ |
| `Madelung_NaCl` | `e/3 + sin(1)` | 4e-06 | ✓ |
| `Madelung_CsCl` | `G⁸C_cosm + √3` | 9.4e-05 | ✓ |
| `Methane_angle` | `e⁴/G⁷ + eπ` | 0.000407 | ✓ |
| `O_N_electronegativity` | `e⁻⁴ + G⁶` | 0.031298 | ✓ |
| `Water_max_density_C` | `ln(π)/C` | 0.007101 | ✓ |
| `Perc_sq_site` | `−C_cosm·sin(1) + G⁵` | 0.000817 | ✓ |
| `Polya_3D_return` | `√π/2 − sin(γ)` | 0.000851 | ✓ |
| `Random_walk_CN` | `G⁷/K − γ⁴` | 5.3e-05 | ✓ |
| `Nats_per_bit` | `−η_eff·cos(φ) + G⁻⁴` | 0.000567 | ✓ |

### Wave 7 — `wave7`

- **Theme:** Apéry / Soldner / number-theory constants
- **Domain route:** `mathematical`
- **Lab key:** `cosmology_wave7_lab`
- **Obligations:** 4 (sample: cosmology_wave7_max_error_under_half_pct, cosmology_wave7_median_error_under_half_pct, cosmology_wave7_observable_count_pos, cosmology_wave7_bundle)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `Apery_zeta3_w7` | `γ³/θ_S + G⁷` | 5.2e-05 | ✓ |
| `Soldner` | `√5/2 + 1/3` | 0.000504 | ✓ |
| `Mills` | `γ³φ/e + G⁻²` | 0.000709 | ✓ |
| `Sierpinski_const` | `φ³/2 + η_eff` | 0.002948 | ✓ |
| `Niven` | `1/(G³√e) + G` | 0.000988 | ✓ |
| `Artin` | `C_eff/φ⁵ + C` | 0.011736 | ✓ |
| `Hafner_Sarnak` | `ln(2)/e⁴ + φ/e` | 0.010383 | ✓ |
| `Porter` | `1/(πφ⁴) + G⁻⁴` | 0.005355 | ✓ |
| `Thue_Morse` | `C_eff/(eπ) + P_new` | 0.012392 | ✓ |
| `MRB` | `C/φ⁴ + φ⁻⁴` | 0.022176 | ✓ |
| `Gauss_Kuzmin` | `γ/(eπ) + φ⁻³` | 0.019676 | ✓ |
| `Universal_parabolic` | `B_in/G⁷ + G²` | 0.00043 | ✓ |
| `Lieb_square_ice` | `B_in/G⁴ + K` | 7e-06 | ✓ |
| `Komornik_Loreti` | `(π/e)·A_bleed + γ` | 0.001775 | ✓ |
| `Bloch_Landau` | `1/(G²√5) + π⁻⁴` | 0.000395 | ✓ |
| `Golden_angle_deg` | `(φ/π)/cos(φ) + e⁵` | 0.001441 | ✓ |
| `Ising3D_eta` | `√φ/π⁵ + 1/π³` | 0.298055 | ✓ |
| `Ising3D_alpha` | `Suction − γ⁶` | 0.046569 | ✓ |
| `Ising3D_delta` | `√5/η_eff` | 0.021989 | ✓ |
| `XY_nu` | `G⁴ − 1/π³` | 0.050942 | ✓ |
| `XY_eta` | `γ⁵φ/e` | 0.105682 | ✓ |
| `Heisenberg_nu` | `cos(1)/√γ` | 0.005522 | ✓ |
| `Heisenberg_eta` | `C_cosm/√e` | 0.03825 | ✓ |
| `Perc_honeycomb_site` | `π/(3φ) + e⁻³` | 0.001327 | ✓ |
| `Perc_SC_bond` | `G⁷/e + e⁻³` | 0.003988 | ✓ |
| `Perc_SC_site` | `cos(φ)/G² + 1/e` | 0.000781 | ✓ |
| `m_u/m_d` | `√3 − √φ` | 0.093812 | ✓ |
| `m_s/m_d` | `e³ + γ⁴` | 0.002696 | ✓ |
| `m_tau/m_mu` | `π²e/φ + φ⁻³` | 0.000534 | ✓ |

### Wave 8 — `wave8`

- **Theme:** CKM unitarity + BR / mass ratios
- **Domain route:** `particle`
- **Lab key:** `cosmology_wave8_lab`
- **Obligations:** 8 (sample: cosmology_wave8_max_error_under_half_pct, cosmology_wave8_median_error_under_half_pct, cosmology_wave8_observable_count_pos, cosmology_wave8_bundle, cosmology_higher_waves_max_error_under_half_pct, cosmology_higher_waves_total_pos)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `|V_ud|` | `A_in − ln(2)` | 0.000684 | ✓ |
| `|V_cd|` | `√γ·θ_S` | 0.003532 | ✓ |
| `|V_cs|` | `φγ/P_var` | 0.145196 | ✓ |
| `delta_CP_PMNS` | `φ³ − 1/e` | 0.008051 | ✓ |
| `m_t/m_b` | `π⁴·K` | 0.356839 | ✓ |
| `BR_Z_ee` | `γ⁶/ln(3)` | 0.10536 | ✓ |
| `BR_Z_had` | `sin(γ) + Poof` | 0.010734 | ✓ |
| `BR_Z_inv` | `(1/3)/A_in` | 0.011229 | ✓ |
| `BR_H_ZZ` | `1/(e⁴ln(2))` | 0.09046 | ✓ |
| `BR_H_gg` | `φ⁻⁴ − γ⁵` | 4.232801 | · |
| `BR_H_cc` | `Suction/(πφ)` | 0.088084 | ✓ |
| `BR_H_gamgam` | `γ⁶·C_cosm` | 0.255029 | ✓ |
| `BR_H_Zgam` | `η_eff/π⁵` | 0.2708 | ✓ |
| `He4_binding_MeV` | `πγ/γ⁵` | 0.002533 | ✓ |
| `Triton_binding_MeV` | `e² + G⁻¹` | 0.014146 | ✓ |
| `Deuteron_mu_muN` | `G⁴ + Poof` | 0.001001 | ✓ |
| `S_8` | `ψ_con/√γ` | 0.001735 | ✓ |
| `z_reion` | `e³/φ²` | 0.104265 | ✓ |
| `XY_beta` | `ψ_con/(πγ)` | 0.003557 | ✓ |
| `XY_gamma` | `φ − P_new` | 0.002407 | ✓ |
| `Heisenberg_beta` | `φ/π − φ⁻⁴` | 0.064565 | ✓ |
| `Heisenberg_gamma` | `√2 − e⁻⁴` | 0.021636 | ✓ |
| `Perc_BCC_bond` | `G⁷/3` | 0.008553 | ✓ |
| `Perc_FCC_site` | `1/3 − e⁻²` | 0.101892 | ✓ |
| `Perc3D_nu` | `sin(γ) − Chaos` | 0.196229 | ✓ |
| `Perc3D_beta` | `√π/φ³` | 0.07644 | ✓ |
| `Perc3D_gamma` | `γ⁷ + √π` | 0.63138 | · |
| `Brun_B2` | `γ² + eγ` | 0.000672 | ✓ |
| `Copeland_Erdos` | `(1/3)/√2` | 0.000959 | ✓ |
| `Erdos_Tenenbaum_Ford` | `γ³/√5` | 0.224926 | ✓ |
| `Foias_alpha` | `eγ − φ⁻²` | 0.027889 | ✓ |
| `Madelung_ZnS` | `eγ/C_eff` | 0.014207 | ✓ |
| `Madelung_CaF2` | `G⁻⁴ + ln(3)` | 0.005952 | ✓ |
| `Madelung_TiO2` | `G² + eγ` | 0.001155 | ✓ |
| `Ice_Ih_density` | `sin(γ)·e/φ` | 0.026304 | ✓ |
| `H2O_bond_angle` | `e³/γ³` | 0.056897 | ✓ |
| `Lorenz_dim` | `√φ + B_in` | 0.00192 | ✓ |
| `Henon_dim` | `P_var/√γ` | 0.005634 | ✓ |
| `Apollonian_dim` | `ln(3)/sin(1)` | 0.016429 | ✓ |
| `SAW_mu_sq` | `√π + e/π` | 0.01858 | ✓ |
| `SAW_nu_3D` | `cos(1) − cos(φ)` | 0.030219 | ✓ |
| `SAW_gamma_3D` | `G⁻² − π⁻³` | 0.186053 | ✓ |
| `Potts3_beta` | `1/9` | 0.001 | ✓ |
| `KT_T/J` | `A_bleed − Poof` | 0.000961 | ✓ |
| `Quark_condensate` | `1/4` | 0.0 | ✓ |
| `Figure8_knot_vol` | `G⁻² + cos(γ)` | 0.000473 | ✓ |
| `Bessel_J0_zero1` | `A_in/ln(2)` | 0.009905 | ✓ |
| `Airy_Ai_zero1` | `(1/G)/η_eff` | 0.00304 | ✓ |
| `gamma_2_Stieltjes` | `π⁻² − γ⁴` | 2.392656 | · |
| `First_Riemann_zero` | `e/γ³` | 0.003605 | ✓ |
| `Spanning_tree_sq` | `γ⁷ + ln(π)` | 0.019004 | ✓ |
| `Hard_sq_entropy` | `eγ·P_var` | 0.00101 | ✓ |

### Wave 9 — `wave9`

- **Theme:** Top / radiation / fractal geometry
- **Domain route:** `particle`
- **Lab key:** `cosmology_wave9_lab`
- **Obligations:** 8 (sample: cosmology_wave9_max_error_under_half_pct, cosmology_wave9_median_error_under_half_pct, cosmology_wave9_observable_count_pos, cosmology_wave9_bundle, cosmology_higher_waves_max_error_under_half_pct, cosmology_higher_waves_total_pos)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `|V_tb|` | `cos(1/e)/(φγ)` | 0.00235 | ✓ |
| `Omega_r` | `γ⁶/e⁶` | 0.193758 | ✓ |
| `O4_nu` | `(γ/G)/sin(1)` | 0.014279 | ✓ |
| `Gluon_condensate` | `C_cosm − e⁻³` | 0.136088 | ✓ |
| `Mandelbrot_boundary` | `φ + 1/φ²` | 0.0 | ✓ |
| `Sierpinski_dim` | `ln(3)/ln(2)` | 3.2e-05 | ✓ |
| `gamma1_Stieltjes` | `G² + cos(e)` | 0.103075 | ✓ |

### Wave 10 — `wave10`

- **Theme:** Lepton moments / logistic / triple-point
- **Domain route:** `particle`
- **Lab key:** `cosmology_wave10_lab`
- **Obligations:** 8 (sample: cosmology_wave10_max_error_under_half_pct, cosmology_wave10_median_error_under_half_pct, cosmology_wave10_observable_count_pos, cosmology_wave10_bundle, cosmology_higher_waves_max_error_under_half_pct, cosmology_higher_waves_total_pos)

| Observable | Formula | Error% | ≤0.5% |
|------------|---------|-------:|:-----:|
| `m_mu/m_e` | `(π³ − G²)·φ⁴` | 0.000656 | ✓ |
| `(g-2)/2_electron` | `(e/π − ln2)/e⁵` | 0.000859 | ✓ |
| `Logistic_accum` | `e√e + cos(e)` | 0.000256 | ✓ |
| `Cahen_constant` | `(C_eff + K)·η_eff` | 2.9e-05 | ✓ |
| `Reciprocal_Fib` | `(Poof + C_cosm)/γ⁵` | 1.8e-05 | ✓ |
| `Water_triple_K` | `π⁵sin(π/φ)·C_eff` | 0.001435 | ✓ |
| `CO2_bond_angle` | `π⁴/cos(1) − C` | 0.000735 | ✓ |
| `SAW_connective_hex` | `π/A_in − γ⁶` | 1.8e-05 | ✓ |
| `Bessel_J1_zero1` | `ψ_con/G + π` | 1.4e-05 | ✓ |
| `eta_baryon_photon` | `Poof¹¹/(πγ)` | 0.004079 | ✓ |

## Reproduction

```bash
python scripts/build_wave_inventory_obligation_map.py
python -c "import sys; sys.path.insert(0,'vendor'); import fsot_compute as f; print(sum(len(getattr(f,f'wave{i}')()) for i in range(1,11)))"
```

## Artifacts

- `data/wave_inventory_obligation_map.json`
- `verification/obligations/wave_inventory_spine.json`
- `docs/WAVE_INVENTORY_OBLIGATION_MAP.md`
