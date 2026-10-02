# Look-elsewhere count

For each closed-form target, how many other formulas built from the same five seeds land at least as close to the target as the FSOT expression does?

The enumeration is the FSOT-2.1-Cpp audit at pin AEB2AD: [docs/LOOK_ELSEWHERE.md](https://github.com/dappalumbo91/FSOT-2.1-Cpp/blob/main/docs/LOOK_ELSEWHERE.md) and `audit/look_elsewhere.tsv`. This repository stores that table at [`data/look_elsewhere.tsv`](../data/look_elsewhere.tsv). The grammar was not rerun here, and no formula was changed to move a count.

## Grammars

| Grammar | Form | Size |
|---|---|---|
| **M** (monomials) | (p/q)·s1^a·s2^b·s3^c, up to 3 distinct seeds from {π, e, φ, γ, Catalan's G}; exponents {−6…6} except 0, plus ±1/2 and ±1/3; p, q ≤ 12 and coprime | 3,967,691 distinct values |
| **S** (two-term) | u ± v, unit monomials of up to 2 seeds, same exponents | about 10.5 million |

- Tolerance is the FSOT expression's own relative error, |c − t| / |t|.
- Chance expectation is the local density of M values between |t|/1.05 and |t|·1.05, scaled to the window ± that tolerance.
- For Ledger A rows the same count is also taken inside the published kill band.
- Forms such as (a − b)/(c + d), and forms that use derived constants (S_cosm, K, C_EFF), come from a larger space. These counts are a lower bound on the trials factor.
- Twenty-one non-prediction rows (computed equal to the target, or a measured input) are left out.

## Result

Closed forms plus Ledger A: 343 targets.

- 325 targets have at least one M value as close as the FSOT expression.
- The median of that count is 66.
- 18 targets have none. Sixteen are closed forms and two are Ledger A (`inv_alpha_em`, `m_mu_over_m_e`).

Zero is not a hidden case. Every target with M = 0 is listed here, with the chance expectation beside it.

| Source | Target | Relative error | M as close | M expected | S as close |
|---|---|---:|---:|---:|---:|
| `closed_form:validation_suite` | **Golden_angle** | 1.716e-06 | **0** | 0.652 | 4 |
| `closed_form:validation_suite` | **Richardson_D=4** | 6.522e-08 | **0** | 0.0469 | 0 |
| `closed_form:wave2` | **1/alpha_em** | 1.442e-06 | **0** | 0.55 | 2 |
| `closed_form:wave4` | **Feigenbaum_delta** | 4.375e-07 | **0** | 0.288 | 1 |
| `closed_form:wave4` | **mu_p_muN** | 7.935e-07 | **0** | 0.549 | 0 |
| `closed_form:wave5` | **Khinchin_K0** | 3.045e-07 | **0** | 0.211 | 1 |
| `closed_form:wave6` | **Levy_constant** | 6.764e-07 | **0** | 0.462 | 0 |
| `closed_form:wave6` | **Backhouse** | 7.350e-07 | **0** | 0.53 | 1 |
| `closed_form:wave6` | **Gauss_AGM** | 1.024e-06 | **0** | 0.742 | 2 |
| `closed_form:wave6` | **Madelung_NaCl** | 4.141e-08 | **0** | 0.0297 | 0 |
| `closed_form:wave7` | **Apery_zeta3_w7** | 5.199e-07 | **0** | 0.377 | 0 |
| `closed_form:wave8` | **Lorenz_dim** | 9.035e-07 | **0** | 0.639 | 1 |
| `closed_form:wave10` | **Bessel_J1_zero1** | 1.360e-07 | **0** | 0.0912 | 0 |
| `closed_form:wave10` | **eta_baryon_photon** | 4.079e-05 | **0** | 0 | 0 |
| `closed_form:lepton_ratios` | **m_mu/m_e_lepton** | 1.363e-06 | **0** | 0.476 | 1 |
| `closed_form:chemistry_radii` | **R_Cl** | 4.487e-07 | **0** | 0.326 | 2 |
| `ledger_a:FORECAST` | **inv_alpha_em** | 1.442e-06 | **0** | 0.55 | 2 |
| `ledger_a:FORECAST` | **m_mu_over_m_e** | 1.363e-06 | **0** | 0.476 | 1 |

`inv_alpha_em` and `m_mu/m_e_lepton` (Ledger A id `m_mu_over_m_e`) are the two the audit called out. Their expectations are 0.55 and 0.476. `m_mu/m_e` uses the integer coefficients 35 and 145, which grammar M does not contain. See [`AUTHORITY_REVISION_NOTES.md`](AUTHORITY_REVISION_NOTES.md).

## Ledger A

High counts stay in the table. `H0_PLANCK_CLASS` has 6,812 monomials as close (expectation 6,790). `Dark_energy_wa` has 10 as close and 202,325 monomials inside its kill band.

| Target | Relative error | M as close | M expected | S as close | M inside band | S inside band |
|---|---:|---:|---:|---:|---:|---:|
| `T_CMB` | 2.819e-04 | 196 | 195 | 486 | 375 | 959 |
| `H0_PLANCK_CLASS` | 1.550e-02 | 6812 | 6.79e+03 | 12576 | 9731 | 19570 |
| `alpha_s_MZ` | 6.788e-03 | 4197 | 4.21e+03 | 4457 | 10427 | 11244 |
| `n_s` | 1.623e-03 | 1169 | 1.18e+03 | 3171 | 11308 | 31782 |
| `Omega_b_h2` | 4.096e-03 | 1921 | 1.95e+03 | 943 | 18155 | 9075 |
| `Omega_DM_h2` | 4.882e-03 | 3067 | 3.03e+03 | 3268 | 51762 | 55057 |
| `First_Riemann_zero` | 1.661e-05 | 11 | 9.64 | 80 | 238 | 1211 |
| `Dark_energy_wa` | 1.209e-05 | 10 | 8.77 | 21 | 202325 | 512694 |
| `sigma_8` | 3.351e-03 | 2463 | 2.43e+03 | 6747 | 31163 | 81099 |
| `N_eff` | 9.407e-05 | 88 | 64.5 | 160 | 66432 | 166092 |
| **inv_alpha_em** | 1.442e-06 | 0 | 0.55 | 2 | 423 | 816 |
| `sin2_theta_W` | 1.299e-04 | 73 | 86.2 | 108 | 28858 | 38116 |
| `Omega_Lambda` | 2.868e-03 | 2053 | 2.06e+03 | 4591 | 36811 | 86477 |
| `m_pi_over_m_p` | 2.860e-04 | 170 | 181 | 185 | 21784 | 24227 |
| **m_mu_over_m_e** | 1.363e-06 | 0 | 0.476 | 1 | 1310 | 952 |
| `m_tau_over_m_e` | 9.541e-06 | 1 | 1.36 | 0 | 774 | 140 |
| `IE_H` | 7.038e-04 | 403 | 410 | 1075 | 4291 | 11659 |
| `H2O_bond_angle` | 5.690e-04 | 242 | 228 | 1961 | 1845 | 6171 |
| `Water_triple_K` | 3.349e-05 | 13 | 10.9 | 10 | 168 | 206 |
| `BP_H2O` | 1.950e-03 | 644 | 591 | 1212 | — | — |
| `tau_reion` | 6.335e-05 | 34 | 35.2 | 25 | 155136 | 124023 |

## Reading the counts

- When M as close is about the chance expectation, the match is typical of a random monomial at that magnitude. `T_CMB` is 196 against 195. `First_Riemann_zero` is 11 against 9.64.
- M as close = 0 with expectation below 1 is tighter than grammar M usually reaches. `inv_alpha_em` and `m_mu_over_m_e` are that case. The expression's own grammar can still be larger than M.
- Kill bands hold from hundreds to hundreds of thousands of grammar values. `Dark_energy_wa` holds 202,325 monomials and 512,694 two-term values. A value that stays inside such a band does little to separate one formula from another.

## Every target

Same columns as [`data/look_elsewhere.tsv`](../data/look_elsewhere.tsv). Names in bold have zero M alternatives.

| Source | Target | Relative error | M as close | M expected | S as close |
|---|---|---:|---:|---:|---:|
| `closed_form:wave1` | `alpha_s(M_Z)` | 6.788e-03 | 4197 | 4.21e+03 | 4457 |
| `closed_form:wave1` | `H0` | 1.550e-02 | 6812 | 6.79e+03 | 12576 |
| `closed_form:wave1` | `T_CMB` | 2.819e-04 | 196 | 195 | 486 |
| `closed_form:wave1` | `n_s` | 1.623e-03 | 1169 | 1.18e+03 | 3171 |
| `closed_form:wave1` | `Omega_b_h2` | 4.096e-03 | 1921 | 1.95e+03 | 943 |
| `closed_form:validation_suite` | `alpha_FSOT` | 3.635e-04 | 81 | 76.6 | 11 |
| `closed_form:validation_suite` | `Tetrahedral_refined` | 2.015e-06 | 2 | 0.803 | 3 |
| `closed_form:validation_suite` | `Tetrahedral_FSOT` | 5.070e-03 | 2016 | 2.03e+03 | 6498 |
| `closed_form:validation_suite` | `Water_bond_angle` | 3.522e-04 | 146 | 141 | 1236 |
| `closed_form:validation_suite` | **Golden_angle** | 1.716e-06 | 0 | 0.652 | 4 |
| `closed_form:validation_suite` | `Dark_energy_wa` | 1.209e-05 | 10 | 8.77 | 21 |
| `closed_form:validation_suite` | **Richardson_D=4** | 6.522e-08 | 0 | 0.0469 | 0 |
| `closed_form:validation_suite` | `Richardson_D=13` | 2.022e-05 | 15 | 14.6 | 41 |
| `closed_form:validation_suite` | `sin2_theta_W` | 8.776e-06 | 3 | 5.82 | 5 |
| `closed_form:validation_suite` | `M_Z/M_W` | 5.299e-04 | 415 | 384 | 1008 |
| `closed_form:validation_suite` | `Feigenbaum_delta` | 2.337e-06 | 3 | 1.54 | 4 |
| `closed_form:validation_suite` | `Feigenbaum_alpha` | 2.682e-05 | 22 | 18.7 | 63 |
| `closed_form:validation_suite` | `Apery_zeta3` | 1.026e-05 | 7 | 7.43 | 19 |
| `closed_form:validation_suite` | `Water_anomaly_C` | 6.655e-06 | 4 | 4.45 | 15 |
| `closed_form:validation_suite` | `GUT_coupling` | 1.671e-05 | 8 | 8.57 | 4 |
| `closed_form:validation_suite` | `Identity_pi_4` | 2.080e-07 | 2 | 0.151 | 1 |
| `closed_form:validation_suite` | `Identity_2sqrtpi_5` | 6.483e-07 | 3 | 0.467 | 1 |
| `closed_form:validation_suite` | `Age_over_T_CMB` | 3.396e-03 | 2239 | 2.22e+03 | 6526 |
| `closed_form:validation_suite` | `CMB_asymmetry` | 3.440e-02 | 19943 | 1.99e+04 | 17125 |
| `closed_form:validation_suite` | `Mantle_Vp_Vs` | 1.865e-03 | 1279 | 1.33e+03 | 4586 |
| `closed_form:validation_suite` | `V24_alpha_s(M_Z)` | 6.788e-03 | 4197 | 4.21e+03 | 4457 |
| `closed_form:validation_suite` | `V25_H0` | 1.550e-02 | 6812 | 6.79e+03 | 12576 |
| `closed_form:validation_suite` | `V26_T_CMB` | 2.819e-04 | 196 | 195 | 486 |
| `closed_form:validation_suite` | `V27_n_s` | 1.623e-03 | 1169 | 1.18e+03 | 3171 |
| `closed_form:validation_suite` | `V28_Omega_b_h2` | 4.096e-03 | 1921 | 1.95e+03 | 943 |
| `closed_form:wave2` | **1/alpha_em** | 1.442e-06 | 0 | 0.55 | 2 |
| `closed_form:wave2` | `sin2_theta_W` | 1.299e-04 | 73 | 86.2 | 108 |
| `closed_form:wave2` | `M_W/M_Z` | 6.916e-03 | 5039 | 5.01e+03 | 12833 |
| `closed_form:wave2` | `Omega_Lambda` | 2.868e-03 | 2053 | 2.06e+03 | 4591 |
| `closed_form:wave2` | `Omega_m` | 9.257e-05 | 85 | 63.3 | 77 |
| `closed_form:wave2` | `Omega_DM_h2` | 4.882e-03 | 3067 | 3.03e+03 | 3268 |
| `closed_form:wave2` | `sigma_8` | 3.351e-03 | 2463 | 2.43e+03 | 6747 |
| `closed_form:wave2` | `tau_reion` | 6.335e-05 | 34 | 35.2 | 25 |
| `closed_form:wave2` | `m_pi/m_p` | 2.860e-04 | 170 | 181 | 185 |
| `closed_form:wave2` | `N_eff` | 9.407e-05 | 88 | 64.5 | 160 |
| `closed_form:wave3` | `\|V_us\|` | 2.357e-02 | 15618 | 1.56e+04 | 20444 |
| `closed_form:wave3` | `\|V_cb\|` | 6.662e-03 | 3584 | 3.55e+03 | 2541 |
| `closed_form:wave3` | `sin_theta_C` | 5.072e-06 | 4 | 3.36 | 5 |
| `closed_form:wave3` | `Age_Gyr` | 1.422e-05 | 8 | 8.28 | 32 |
| `closed_form:wave3` | `z_eq` | 2.407e-03 | 342 | 347 | 2132 |
| `closed_form:wave3` | `theta_star` | 5.994e-04 | 232 | 245 | 77 |
| `closed_form:wave3` | `r_star_Mpc` | 2.089e-04 | 79 | 78.8 | 116 |
| `closed_form:wave3` | `Deuteron_binding_MeV` | 6.076e-07 | 1 | 0.427 | 2 |
| `closed_form:wave3` | `Neutron_lifetime_s` | 2.195e-04 | 47 | 51.8 | 255 |
| `closed_form:wave3` | `Ising2D_beta` | 7.354e-06 | 6 | 5.03 | 5 |
| `closed_form:wave3` | `Ising2D_nu` | 5.634e-05 | 47 | 40.5 | 91 |
| `closed_form:wave3` | `Ising2D_gamma` | 8.910e-03 | 6508 | 6.46e+03 | 19816 |
| `closed_form:wave3` | `m_t/m_W` | 1.585e-05 | 12 | 11.2 | 35 |
| `closed_form:wave3` | `m_H/m_W` | 5.555e-03 | 3995 | 4e+03 | 11393 |
| `closed_form:wave3` | `m_tau/m_e` | 7.321e-06 | 1 | 1.04 | 0 |
| `closed_form:wave4` | `sin2_theta12` | 1.159e-04 | 71 | 79.1 | 119 |
| `closed_form:wave4` | `sin2_theta23` | 4.275e-04 | 332 | 305 | 636 |
| `closed_form:wave4` | `sin2_theta13` | 6.890e-04 | 320 | 327 | 158 |
| `closed_form:wave4` | `Dm2_21/Dm2_32` | 5.767e-04 | 308 | 289 | 182 |
| `closed_form:wave4` | `\|V_ub\|` | 2.651e-02 | 8732 | 8.75e+03 | 2137 |
| `closed_form:wave4` | `\|V_td\|` | 9.346e-05 | 37 | 36.7 | 12 |
| `closed_form:wave4` | `\|V_ts\|` | 8.160e-05 | 46 | 43.2 | 34 |
| `closed_form:wave4` | `Jarlskog_J` | 2.347e-03 | 108 | 115 | 2 |
| `closed_form:wave4` | **Feigenbaum_delta** | 4.375e-07 | 0 | 0.288 | 1 |
| `closed_form:wave4` | `Feigenbaum_alpha` | 7.379e-07 | 1 | 0.515 | 4 |
| `closed_form:wave4` | `r_p_fm` | 1.800e-04 | 134 | 130 | 347 |
| `closed_form:wave4` | `m_n-m_p_MeV` | 2.165e-06 | 1 | 1.57 | 5 |
| `closed_form:wave4` | **mu_p_muN** | 7.935e-07 | 0 | 0.549 | 0 |
| `closed_form:wave4` | `w0` | 1.816e-05 | 15 | 13.2 | 27 |
| `closed_form:wave4` | `m_c/m_b` | 1.339e-02 | 9109 | 9.08e+03 | 12920 |
| `closed_form:wave4` | `alpha_s_ratio` | 2.630e-04 | 168 | 156 | 722 |
| `closed_form:wave5` | `Gamma_Z/M_Z` | 7.898e-06 | 8 | 3.89 | 4 |
| `closed_form:wave5` | `R_ell` | 5.414e-04 | 284 | 296 | 1004 |
| `closed_form:wave5` | `R_b` | 2.767e-04 | 178 | 182 | 235 |
| `closed_form:wave5` | `R_c` | 5.113e-05 | 34 | 33 | 45 |
| `closed_form:wave5` | `A_FB_ell` | 6.954e-04 | 321 | 314 | 127 |
| `closed_form:wave5` | `A_ell_SLD` | 7.329e-04 | 500 | 467 | 554 |
| `closed_form:wave5` | `m_H/m_t` | 1.472e-04 | 109 | 106 | 235 |
| `closed_form:wave5` | `BR_H_bb` | 6.093e-06 | 3 | 4.37 | 4 |
| `closed_form:wave5` | `BR_H_WW` | 2.077e-05 | 14 | 13.7 | 25 |
| `closed_form:wave5` | `BR_H_tautau` | 9.880e-05 | 57 | 56.3 | 57 |
| `closed_form:wave5` | `Y_p_He4` | 4.859e-04 | 305 | 324 | 481 |
| `closed_form:wave5` | `D_H_ratio` | 9.099e-04 | 48 | 40.3 | 0 |
| `closed_form:wave5` | **Khinchin_K0** | 3.045e-07 | 0 | 0.211 | 1 |
| `closed_form:wave5` | `Glaisher_A` | 7.208e-07 | 1 | 0.521 | 2 |
| `closed_form:wave5` | `Twin_prime_C2` | 1.260e-04 | 82 | 90.7 | 237 |
| `closed_form:wave5` | `Mertens_M` | 1.271e-05 | 4 | 8.52 | 11 |
| `closed_form:wave5` | `Dottie_number` | 9.504e-07 | 1 | 0.686 | 1 |
| `closed_form:wave5` | `Omega_constant` | 3.161e-06 | 1 | 2.26 | 5 |
| `closed_form:wave5` | `Conway_lambda` | 1.516e-06 | 2 | 1.1 | 4 |
| `closed_form:wave5` | `Plastic_number` | 3.394e-06 | 3 | 2.45 | 5 |
| `closed_form:wave5` | `Landau_Ramanujan` | 6.532e-07 | 2 | 0.473 | 2 |
| `closed_form:wave5` | `Laplace_limit` | 6.111e-04 | 417 | 440 | 1145 |
| `closed_form:wave6` | `zeta_5` | 3.442e-06 | 3 | 2.5 | 5 |
| `closed_form:wave6` | `zeta_7` | 1.986e-06 | 2 | 1.45 | 3 |
| `closed_form:wave6` | **Levy_constant** | 6.764e-07 | 0 | 0.462 | 0 |
| `closed_form:wave6` | `Erdos_Borwein` | 2.153e-05 | 20 | 15.5 | 33 |
| `closed_form:wave6` | `Bernstein` | 2.218e-06 | 1 | 1.5 | 4 |
| `closed_form:wave6` | **Backhouse** | 7.350e-07 | 0 | 0.53 | 1 |
| `closed_form:wave6` | `Viswanath` | 1.170e-06 | 2 | 0.848 | 1 |
| `closed_form:wave6` | `Kepler_Bouwkamp` | 1.040e-05 | 5 | 6.42 | 6 |
| `closed_form:wave6` | `Sphere_packing_3D` | 3.602e-06 | 2 | 2.6 | 9 |
| `closed_form:wave6` | **Gauss_AGM** | 1.024e-06 | 0 | 0.742 | 2 |
| `closed_form:wave6` | `Lemniscate` | 1.534e-05 | 11 | 10.7 | 24 |
| `closed_form:wave6` | `Hashing_bound` | 7.119e-06 | 5 | 4.38 | 6 |
| `closed_form:wave6` | `von_Karman` | 2.291e-04 | 166 | 160 | 270 |
| `closed_form:wave6` | **Madelung_NaCl** | 4.141e-08 | 0 | 0.0297 | 0 |
| `closed_form:wave6` | `Madelung_CsCl` | 2.305e-04 | 188 | 165 | 487 |
| `closed_form:wave6` | `Methane_angle` | 4.072e-06 | 3 | 1.62 | 8 |
| `closed_form:wave6` | `O_N_electronegativity` | 3.130e-04 | 202 | 225 | 438 |
| `closed_form:wave6` | `Water_max_density_C` | 2.317e-05 | 11 | 15.5 | 39 |
| `closed_form:wave6` | `Perc_sq_site` | 1.151e-03 | 819 | 824 | 1973 |
| `closed_form:wave6` | `Polya_3D_return` | 8.509e-06 | 6 | 5.83 | 7 |
| `closed_form:wave6` | `Random_walk_CN` | 2.936e-04 | 220 | 212 | 550 |
| `closed_form:wave6` | `Nats_per_bit` | 5.667e-06 | 7 | 4.08 | 17 |
| `closed_form:wave7` | **Apery_zeta3_w7** | 5.199e-07 | 0 | 0.377 | 0 |
| `closed_form:wave7` | `Soldner` | 5.045e-06 | 4 | 3.63 | 12 |
| `closed_form:wave7` | `Mills` | 7.093e-06 | 3 | 5.13 | 16 |
| `closed_form:wave7` | `Sierpinski_const` | 2.948e-05 | 19 | 20.6 | 44 |
| `closed_form:wave7` | `Niven` | 9.876e-06 | 2 | 7.06 | 22 |
| `closed_form:wave7` | `Artin` | 6.953e-05 | 52 | 48.2 | 53 |
| `closed_form:wave7` | `Hafner_Sarnak` | 1.038e-04 | 80 | 74.6 | 139 |
| `closed_form:wave7` | `Porter` | 5.355e-05 | 39 | 38.5 | 103 |
| `closed_form:wave7` | `Thue_Morse` | 1.109e-04 | 78 | 77.6 | 129 |
| `closed_form:wave7` | `MRB` | 2.111e-04 | 134 | 138 | 170 |
| `closed_form:wave7` | `Gauss_Kuzmin` | 1.968e-04 | 138 | 134 | 192 |
| `closed_form:wave7` | `Universal_parabolic` | 2.606e-05 | 16 | 18.3 | 49 |
| `closed_form:wave7` | `Lieb_square_ice` | 3.847e-05 | 19 | 27.7 | 72 |
| `closed_form:wave7` | `Komornik_Loreti` | 1.775e-05 | 10 | 12.7 | 40 |
| `closed_form:wave7` | `Bloch_Landau` | 3.953e-06 | 1 | 2.82 | 5 |
| `closed_form:wave7` | `Golden_angle_deg` | 1.441e-05 | 5 | 5.48 | 14 |
| `closed_form:wave7` | `Ising3D_eta` | 2.981e-03 | 1533 | 1.55e+03 | 977 |
| `closed_form:wave7` | `Ising3D_alpha` | 4.657e-04 | 305 | 287 | 250 |
| `closed_form:wave7` | `Ising3D_delta` | 2.199e-04 | 146 | 145 | 380 |
| `closed_form:wave7` | `XY_nu` | 5.094e-04 | 383 | 367 | 794 |
| `closed_form:wave7` | `XY_eta` | 1.057e-03 | 555 | 555 | 427 |
| `closed_form:wave7` | `Heisenberg_nu` | 5.522e-05 | 39 | 39.8 | 82 |
| `closed_form:wave7` | `Heisenberg_eta` | 1.282e-02 | 6700 | 6.71e+03 | 4538 |
| `closed_form:wave7` | `Perc_honeycomb_site` | 1.327e-05 | 7 | 9.56 | 20 |
| `closed_form:wave7` | `Perc_SC_bond` | 3.988e-05 | 34 | 26.6 | 33 |
| `closed_form:wave7` | `Perc_SC_site` | 7.806e-06 | 7 | 5.32 | 11 |
| `closed_form:wave7` | `m_u/m_d` | 9.381e-04 | 612 | 660 | 1226 |
| `closed_form:wave7` | `m_s/m_d` | 2.696e-05 | 20 | 14.8 | 24 |
| `closed_form:wave7` | `m_tau/m_mu` | 5.339e-06 | 4 | 3.02 | 5 |
| `closed_form:wave8` | `\|V_ud\|` | 6.844e-06 | 5 | 4.96 | 13 |
| `closed_form:wave8` | `\|V_cd\|` | 3.532e-05 | 28 | 23.4 | 31 |
| `closed_form:wave8` | `\|V_cs\|` | 1.452e-03 | 1019 | 1.05e+03 | 2956 |
| `closed_form:wave8` | `delta_CP_PMNS` | 8.051e-05 | 57 | 54 | 150 |
| `closed_form:wave8` | `m_t/m_b` | 3.836e-03 | 1909 | 1.85e+03 | 4019 |
| `closed_form:wave8` | `BR_Z_ee` | 1.054e-03 | 538 | 539 | 327 |
| `closed_form:wave8` | `BR_Z_had` | 1.073e-04 | 81 | 77.5 | 176 |
| `closed_form:wave8` | `BR_Z_inv` | 1.123e-04 | 66 | 73.5 | 98 |
| `closed_form:wave8` | `BR_H_ZZ` | 9.046e-04 | 452 | 444 | 252 |
| `closed_form:wave8` | `BR_H_gg` | 4.233e-02 | 24916 | 2.49e+04 | 24155 |
| `closed_form:wave8` | `BR_H_cc` | 8.808e-04 | 459 | 439 | 267 |
| `closed_form:wave8` | `BR_H_gamgam` | 1.580e-02 | 4608 | 4.59e+03 | 824 |
| `closed_form:wave8` | `BR_H_Zgam` | 2.708e-03 | 653 | 702 | 96 |
| `closed_form:wave8` | `He4_binding_MeV` | 2.533e-05 | 11 | 13.1 | 128 |
| `closed_form:wave8` | `Triton_binding_MeV` | 1.415e-04 | 94 | 87.7 | 183 |
| `closed_form:wave8` | `Deuteron_mu_muN` | 1.001e-05 | 5 | 7.25 | 25 |
| `closed_form:wave8` | `S_8` | 1.735e-05 | 16 | 12.6 | 43 |
| `closed_form:wave8` | `z_reion` | 1.043e-03 | 651 | 651 | 2162 |
| `closed_form:wave8` | `XY_beta` | 3.557e-05 | 27 | 24.5 | 38 |
| `closed_form:wave8` | `XY_gamma` | 2.407e-05 | 13 | 17.4 | 57 |
| `closed_form:wave8` | `Heisenberg_beta` | 6.457e-04 | 454 | 447 | 702 |
| `closed_form:wave8` | `Heisenberg_gamma` | 2.164e-04 | 153 | 156 | 471 |
| `closed_form:wave8` | `Perc_BCC_bond` | 8.553e-05 | 65 | 55.6 | 57 |
| `closed_form:wave8` | `Perc_FCC_site` | 1.019e-03 | 675 | 667 | 900 |
| `closed_form:wave8` | `Perc3D_nu` | 1.962e-03 | 1443 | 1.42e+03 | 3856 |
| `closed_form:wave8` | `Perc3D_beta` | 7.644e-04 | 494 | 534 | 1011 |
| `closed_form:wave8` | `Perc3D_gamma` | 6.314e-03 | 4503 | 4.5e+03 | 14240 |
| `closed_form:wave8` | `Brun_B2` | 6.717e-06 | 3 | 4.77 | 20 |
| `closed_form:wave8` | `Copeland_Erdos` | 9.590e-06 | 6 | 6.39 | 6 |
| `closed_form:wave8` | `Erdos_Tenenbaum_Ford` | 2.249e-03 | 1318 | 1.34e+03 | 1431 |
| `closed_form:wave8` | `Foias_alpha` | 2.789e-04 | 207 | 202 | 527 |
| `closed_form:wave8` | `Madelung_ZnS` | 9.422e-05 | 64 | 67.8 | 180 |
| `closed_form:wave8` | `Madelung_CaF2` | 5.952e-05 | 42 | 41.5 | 151 |
| `closed_form:wave8` | `Madelung_TiO2` | 1.155e-05 | 9 | 8.07 | 23 |
| `closed_form:wave8` | `Ice_Ih_density` | 2.630e-04 | 180 | 191 | 487 |
| `closed_form:wave8` | `H2O_bond_angle` | 5.690e-04 | 242 | 228 | 1961 |
| `closed_form:wave8` | **Lorenz_dim** | 9.035e-07 | 0 | 0.639 | 1 |
| `closed_form:wave8` | `Henon_dim` | 5.634e-05 | 45 | 40.8 | 106 |
| `closed_form:wave8` | `Apollonian_dim` | 1.643e-04 | 103 | 119 | 328 |
| `closed_form:wave8` | `SAW_mu_sq` | 1.858e-04 | 119 | 129 | 350 |
| `closed_form:wave8` | `SAW_nu_3D` | 3.022e-04 | 207 | 216 | 482 |
| `closed_form:wave8` | `SAW_gamma_3D` | 1.861e-03 | 1330 | 1.35e+03 | 4237 |
| `closed_form:wave8` | `Potts3_beta` | 1.000e-05 | 6 | 6.16 | 5 |
| `closed_form:wave8` | `KT_T/J` | 9.608e-06 | 9 | 6.97 | 17 |
| `closed_form:wave8` | `Figure8_knot_vol` | 4.735e-06 | 4 | 3.35 | 10 |
| `closed_form:wave8` | `Bessel_J0_zero1` | 9.905e-05 | 70 | 69.2 | 172 |
| `closed_form:wave8` | `Airy_Ai_zero1` | 3.040e-05 | 16 | 21.2 | 51 |
| `closed_form:wave8` | `gamma_2_Stieltjes` | 2.393e-02 | 9569 | 9.59e+03 | 3314 |
| `closed_form:wave8` | `First_Riemann_zero` | 3.605e-05 | 19 | 20.9 | 157 |
| `closed_form:wave8` | `Spanning_tree_sq` | 1.900e-04 | 121 | 138 | 411 |
| `closed_form:wave8` | `Hard_sq_entropy` | 1.010e-05 | 5 | 7.27 | 15 |
| `closed_form:wave9` | `\|V_tb\|` | 2.350e-05 | 21 | 17.1 | 33 |
| `closed_form:wave9` | `Omega_r` | 1.938e-03 | 153 | 167 | 1 |
| `closed_form:wave9` | `O4_nu` | 1.428e-04 | 97 | 103 | 276 |
| `closed_form:wave9` | `Gluon_condensate` | 6.941e-02 | 29257 | 2.92e+04 | 11329 |
| `closed_form:wave9` | `Sierpinski_dim` | 3.150e-07 | 1 | 0.226 | 1 |
| `closed_form:wave9` | `gamma1_Stieltjes` | 1.031e-03 | 626 | 600 | 550 |
| `closed_form:wave10` | `m_mu/m_e` | 6.556e-06 | 2 | 2.29 | 3 |
| `closed_form:wave10` | `(g-2)/2_electron` | 8.593e-06 | 2 | 2.04 | 0 |
| `closed_form:wave10` | `Logistic_accum` | 2.565e-06 | 2 | 1.73 | 3 |
| `closed_form:wave10` | `Cahen_constant` | 4.898e-05 | 49 | 35.3 | 84 |
| `closed_form:wave10` | `Reciprocal_Fib` | 3.793e-03 | 2537 | 2.58e+03 | 5567 |
| `closed_form:wave10` | `Water_triple_K` | 3.349e-05 | 13 | 10.9 | 10 |
| `closed_form:wave10` | `CO2_bond_angle` | 7.429e-06 | 3 | 2.67 | 8 |
| `closed_form:wave10` | `SAW_connective_hex` | 1.817e-07 | 1 | 0.13 | 0 |
| `closed_form:wave10` | **Bessel_J1_zero1** | 1.360e-07 | 0 | 0.0912 | 0 |
| `closed_form:wave10` | **eta_baryon_photon** | 4.079e-05 | 0 | 0 | 0 |
| `closed_form:lepton_ratios` | `m_tau/m_e_lepton` | 9.541e-06 | 1 | 1.36 | 0 |
| `closed_form:lepton_ratios` | `m_tau/m_mu_lepton` | 1.695e-05 | 11 | 9.6 | 19 |
| `closed_form:lepton_ratios` | **m_mu/m_e_lepton** | 1.363e-06 | 0 | 0.476 | 1 |
| `closed_form:dynamical_systems` | `Logistic_R_inf` | 1.297e-05 | 17 | 8.77 | 24 |
| `closed_form:dynamical_systems` | `Ising2D_Tc_J` | 6.285e-06 | 7 | 4.41 | 14 |
| `closed_form:dynamical_systems` | `Ising3D_beta_dyn` | 5.812e-05 | 33 | 39.8 | 70 |
| `closed_form:dynamical_systems` | `Ising3D_nu_dyn` | 4.609e-05 | 35 | 33.1 | 74 |
| `closed_form:dynamical_systems` | `Henon_Lyapunov` | 2.168e-03 | 1509 | 1.51e+03 | 2884 |
| `closed_form:neural_architecture` | `Lateral_Inhibition` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:neural_architecture` | `Spike_Threshold` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:neural_architecture` | `Prediction_Gain` | 5.087e-05 | 38 | 36.9 | 95 |
| `closed_form:neural_architecture` | `TD_BU_Ratio` | 2.101e-05 | 19 | 15.1 | 53 |
| `closed_form:neural_architecture` | `Recurrent_Decay` | 5.588e-05 | 32 | 38.6 | 63 |
| `closed_form:neural_architecture` | `Hebbian_LR` | 1.821e-04 | 119 | 118 | 147 |
| `closed_form:neural_architecture` | `Consciousness_Threshold` | 1.532e-05 | 11 | 9.18 | 47 |
| `closed_form:neural_architecture` | `Consciousness_Gate` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:neural_architecture` | `Sync_Decay` | 8.898e-05 | 66 | 62 | 105 |
| `closed_form:neural_architecture` | `Cross_Modal_Gain` | 5.087e-05 | 38 | 36.9 | 95 |
| `closed_form:neural_architecture` | `Circulant_Spectral_R` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:neural_architecture` | `EEG_1_over_f` | 2.101e-05 | 19 | 15.1 | 53 |
| `closed_form:consciousness_model` | `Consciousness_Gate` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:consciousness_model` | `Resonance_Persistence` | 5.087e-05 | 38 | 36.9 | 95 |
| `closed_form:consciousness_model` | `Resonance_Rate` | 2.553e-04 | 175 | 168 | 230 |
| `closed_form:consciousness_model` | `Resonance_Eq_Factor` | 1.259e-05 | 9 | 9.05 | 25 |
| `closed_form:consciousness_model` | `Ignition_Coherence` | 6.759e-05 | 38 | 47 | 74 |
| `closed_form:consciousness_model` | `W_Integration` | 2.101e-05 | 19 | 15.1 | 53 |
| `closed_form:consciousness_model` | `W_Complexity` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:consciousness_model` | `W_Binding` | 5.087e-05 | 38 | 36.9 | 95 |
| `closed_form:consciousness_model` | `W_Phase_Sync` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:consciousness_model` | `Hub_coupling` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:consciousness_model` | `Inner_coupling` | 8.898e-05 | 66 | 62 | 105 |
| `closed_form:consciousness_model` | `Radial_coupling` | 5.087e-05 | 38 | 36.9 | 95 |
| `closed_form:consciousness_model` | `Outer_coupling` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:consciousness_model` | `Cross_coupling` | 2.714e-05 | 15 | 19.4 | 48 |
| `closed_form:homeostasis` | `Novelty_Threshold` | 5.500e-05 | 44 | 39.6 | 78 |
| `closed_form:homeostasis` | `Consolidation_Rate` | 1.821e-04 | 119 | 118 | 147 |
| `closed_form:homeostasis` | `Attention_Inhibition` | 9.962e-05 | 89 | 72.1 | 193 |
| `closed_form:homeostasis` | `Cross_Lobe_Coupling` | 1.821e-04 | 119 | 118 | 147 |
| `closed_form:trinary` | `Collapse_Threshold` | 1.202e-04 | 84 | 87.2 | 226 |
| `closed_form:predictions` | `CMB_tau` | 9.050e-06 | 6 | 5.03 | 6 |
| `closed_form:predictions` | `Dark_energy_wa` | 2.637e-02 | 19055 | 1.91e+04 | 50860 |
| `closed_form:predictions` | `Tau_g-2` | 9.583e-03 | 2248 | 2.29e+03 | 315 |
| `closed_form:predictions` | `Cross_MatSci_CM` | 1.316e-02 | 9599 | 9.58e+03 | 23899 |
| `closed_form:predictions` | `Cross_Astro_PS` | 4.932e-03 | 3576 | 3.59e+03 | 8569 |
| `closed_form:chemistry_ionization` | `IE_H` | 7.038e-04 | 403 | 410 | 1075 |
| `closed_form:chemistry_ionization` | `IE_He` | 7.482e-04 | 353 | 396 | 864 |
| `closed_form:chemistry_ionization` | `IE_Li` | 1.928e-05 | 15 | 12.5 | 30 |
| `closed_form:chemistry_ionization` | `IE_Be` | 9.778e-05 | 63 | 59.8 | 146 |
| `closed_form:chemistry_ionization` | `IE_B` | 7.820e-04 | 433 | 485 | 1251 |
| `closed_form:chemistry_ionization` | `IE_C` | 1.762e-04 | 112 | 105 | 263 |
| `closed_form:chemistry_ionization` | `IE_N` | 1.314e-03 | 755 | 760 | 1809 |
| `closed_form:chemistry_ionization` | `IE_O` | 1.324e-02 | 7713 | 7.71e+03 | 21707 |
| `closed_form:chemistry_ionization` | `IE_F` | 2.463e-04 | 135 | 139 | 709 |
| `closed_form:chemistry_ionization` | `IE_Ne` | 1.493e-03 | 803 | 810 | 3048 |
| `closed_form:chemistry_ionization` | `IE_Na` | 3.564e-04 | 237 | 233 | 483 |
| `closed_form:chemistry_ionization` | `IE_Mg` | 5.126e-04 | 330 | 321 | 812 |
| `closed_form:chemistry_ionization` | `IE_Al` | 2.552e-04 | 162 | 164 | 574 |
| `closed_form:chemistry_ionization` | `IE_Si` | 3.921e-04 | 235 | 244 | 659 |
| `closed_form:chemistry_ionization` | `IE_P` | 6.087e-05 | 37 | 36.7 | 112 |
| `closed_form:chemistry_ionization` | `IE_S` | 1.257e-05 | 11 | 7.59 | 23 |
| `closed_form:chemistry_ionization` | `IE_Cl` | 1.280e-03 | 747 | 751 | 2488 |
| `closed_form:chemistry_ionization` | `IE_Ar` | 7.854e-06 | 4 | 4.49 | 4 |
| `closed_form:chemistry_ionization` | `IE_K` | 8.318e-04 | 553 | 551 | 1310 |
| `closed_form:chemistry_ionization` | `IE_Ca` | 2.692e-04 | 198 | 172 | 441 |
| `closed_form:chemistry_electronegativity` | `EN_H` | 2.741e-04 | 167 | 193 | 530 |
| `closed_form:chemistry_electronegativity` | `EN_Li` | 4.171e-05 | 28 | 30.3 | 71 |
| `closed_form:chemistry_electronegativity` | `EN_Na` | 2.013e-04 | 139 | 146 | 434 |
| `closed_form:chemistry_electronegativity` | `EN_C` | 5.594e-05 | 31 | 38.9 | 100 |
| `closed_form:chemistry_electronegativity` | `EN_N` | 8.930e-05 | 69 | 61.2 | 150 |
| `closed_form:chemistry_electronegativity` | `EN_O` | 2.013e-04 | 130 | 137 | 451 |
| `closed_form:chemistry_electronegativity` | `EN_F` | 2.317e-05 | 11 | 15.5 | 39 |
| `closed_form:chemistry_electronegativity` | `EN_S` | 4.065e-04 | 289 | 283 | 635 |
| `closed_form:chemistry_electronegativity` | `EN_Cl` | 2.902e-05 | 16 | 19.8 | 41 |
| `closed_form:chemistry_electronegativity` | `EN_Br` | 1.257e-03 | 857 | 863 | 2018 |
| `closed_form:chemistry_bond_lengths` | `BL_H−H` | 2.024e-04 | 143 | 146 | 406 |
| `closed_form:chemistry_bond_lengths` | `BL_C−H` | 3.319e-04 | 253 | 241 | 624 |
| `closed_form:chemistry_bond_lengths` | `BL_C−C` | 9.039e-05 | 68 | 65 | 187 |
| `closed_form:chemistry_bond_lengths` | `BL_C=C` | 3.497e-05 | 13 | 25.3 | 81 |
| `closed_form:chemistry_bond_lengths` | `BL_C≡C` | 1.532e-05 | 15 | 11.1 | 37 |
| `closed_form:chemistry_bond_lengths` | `BL_O−H` | 2.362e-04 | 160 | 172 | 417 |
| `closed_form:chemistry_bond_lengths` | `BL_N−H` | 1.151e-05 | 7 | 8.37 | 20 |
| `closed_form:chemistry_bond_lengths` | `BL_C−N` | 3.969e-05 | 29 | 28.5 | 80 |
| `closed_form:chemistry_bond_lengths` | `BL_C−O` | 2.542e-04 | 172 | 183 | 472 |
| `closed_form:chemistry_bond_lengths` | `BL_C=O` | 1.896e-04 | 132 | 137 | 430 |
| `closed_form:chemistry_bond_energies` | `BE_H−H` | 2.486e-03 | 721 | 722 | 1427 |
| `closed_form:chemistry_bond_energies` | `BE_C−H` | 7.225e-04 | 240 | 213 | 812 |
| `closed_form:chemistry_bond_energies` | `BE_C−C` | 2.387e-03 | 735 | 734 | 745 |
| `closed_form:chemistry_bond_energies` | `BE_C=C` | 1.620e-03 | 452 | 430 | 429 |
| `closed_form:chemistry_bond_energies` | `BE_C≡C` | 7.627e-04 | 174 | 183 | 1234 |
| `closed_form:chemistry_bond_energies` | `BE_O−H` | 7.951e-04 | 222 | 226 | 206 |
| `closed_form:chemistry_bond_energies` | `BE_N−H` | 3.424e-03 | 1042 | 1.03e+03 | 4655 |
| `closed_form:chemistry_bond_energies` | `BE_N≡N` | 8.281e-04 | 174 | 191 | 146 |
| `closed_form:chemistry_bond_energies` | `BE_O=O` | 5.722e-03 | 1590 | 1.6e+03 | 3614 |
| `closed_form:chemistry_bond_energies` | `BE_F−F` | 3.166e-03 | 1165 | 1.16e+03 | 1738 |
| `closed_form:chemistry_molecular` | `BP_H₂O` | 1.950e-03 | 644 | 591 | 1212 |
| `closed_form:chemistry_molecular` | `BP_NH₃` | 1.324e-03 | 428 | 445 | 1989 |
| `closed_form:chemistry_molecular` | `BP_CH₄` | 4.149e-04 | 167 | 165 | 240 |
| `closed_form:chemistry_molecular` | `BP_C₂H₅OH` | 1.435e-03 | 433 | 440 | 511 |
| `closed_form:chemistry_molecular` | `BP_CO₂_sub` | 2.647e-03 | 897 | 934 | 1667 |
| `closed_form:chemistry_molecular` | `dipole_H₂O` | 1.003e-04 | 75 | 71.5 | 211 |
| `closed_form:chemistry_molecular` | `dipole_NH₃` | 3.969e-05 | 29 | 28.5 | 80 |
| `closed_form:chemistry_molecular` | `dipole_HCl` | 1.146e-04 | 74 | 83.2 | 244 |
| `closed_form:chemistry_molecular` | `pKw_water` | 8.137e-04 | 497 | 473 | 1167 |
| `closed_form:chemistry_radii` | `R_H` | 4.889e-05 | 37 | 33.3 | 41 |
| `closed_form:chemistry_radii` | `R_C` | 1.700e-05 | 13 | 12.3 | 34 |
| `closed_form:chemistry_radii` | `R_N` | 2.177e-07 | 2 | 0.157 | 0 |
| `closed_form:chemistry_radii` | `R_O` | 4.096e-05 | 31 | 29.5 | 60 |
| `closed_form:chemistry_radii` | `R_F` | 5.629e-05 | 31 | 40.6 | 108 |
| `closed_form:chemistry_radii` | `R_Na` | 9.039e-05 | 68 | 65 | 187 |
| `closed_form:chemistry_radii` | **R_Cl** | 4.487e-07 | 0 | 0.326 | 2 |
| `closed_form:chemistry_radii` | `R_Fe` | 1.236e-04 | 92 | 89.6 | 228 |
| `ledger_a:FORECAST` | `T_CMB` | 2.819e-04 | 196 | 195 | 486 |
| `ledger_a:FORECAST` | `H0_PLANCK_CLASS` | 1.550e-02 | 6812 | 6.79e+03 | 12576 |
| `ledger_a:FORECAST` | `alpha_s_MZ` | 6.788e-03 | 4197 | 4.21e+03 | 4457 |
| `ledger_a:FORECAST` | `n_s` | 1.623e-03 | 1169 | 1.18e+03 | 3171 |
| `ledger_a:FORECAST` | `Omega_b_h2` | 4.096e-03 | 1921 | 1.95e+03 | 943 |
| `ledger_a:FORECAST` | `Omega_DM_h2` | 4.882e-03 | 3067 | 3.03e+03 | 3268 |
| `ledger_a:FORECAST` | `First_Riemann_zero` | 1.661e-05 | 11 | 9.64 | 80 |
| `ledger_a:FORECAST` | `Dark_energy_wa` | 1.209e-05 | 10 | 8.77 | 21 |
| `ledger_a:FORECAST` | `sigma_8` | 3.351e-03 | 2463 | 2.43e+03 | 6747 |
| `ledger_a:FORECAST` | `N_eff` | 9.407e-05 | 88 | 64.5 | 160 |
| `ledger_a:FORECAST` | **inv_alpha_em** | 1.442e-06 | 0 | 0.55 | 2 |
| `ledger_a:FORECAST` | `sin2_theta_W` | 1.299e-04 | 73 | 86.2 | 108 |
| `ledger_a:FORECAST` | `Omega_Lambda` | 2.868e-03 | 2053 | 2.06e+03 | 4591 |
| `ledger_a:FORECAST` | `m_pi_over_m_p` | 2.860e-04 | 170 | 181 | 185 |
| `ledger_a:FORECAST` | **m_mu_over_m_e** | 1.363e-06 | 0 | 0.476 | 1 |
| `ledger_a:FORECAST` | `m_tau_over_m_e` | 9.541e-06 | 1 | 1.36 | 0 |
| `ledger_a:FORECAST` | `IE_H` | 7.038e-04 | 403 | 410 | 1075 |
| `ledger_a:FORECAST` | `H2O_bond_angle` | 5.690e-04 | 242 | 228 | 1961 |
| `ledger_a:FORECAST` | `Water_triple_K` | 3.349e-05 | 13 | 10.9 | 10 |
| `ledger_a:CONSTANT_IDENTITY` | `BP_H2O` | 1.950e-03 | 644 | 591 | 1212 |
| `ledger_a:FORECAST` | `tau_reion` | 6.335e-05 | 34 | 35.2 | 25 |
