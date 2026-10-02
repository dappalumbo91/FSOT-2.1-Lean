# Observables with no measured input of the same dimension

Ledger A (`scripts/fsot_ledger_a_lib.py`) emits a value from the seed engine. `fsot_predict` sets `measured_in_formula` to false. The anchor on each entry is a compare step. It is not an input, and it is not the same quantity fed back into the expression.

The output's dimension is the `units` field. None of these expressions take a measured quantity in that dimension. Seeds and the derived scalars (`S_cosm`, `S_chem`, `S_quant`, `C_eff`, and the rest of the pin) are not measured inputs.

`DNA_base_pair` in `vendor/fsot_compute.py` multiplies by the measured Bohr radius `a0 = mpf("0.529177")` angstroms and reports a length. That row uses a measured input of the same dimension, so it is absent from this registry. See [`AUTHORITY_REVISION_NOTES.md`](AUTHORITY_REVISION_NOTES.md).

| Id | Kind | Units | Expression |
|----|------|-------|------------|
| `T_CMB` | FORECAST | K | `phi**2 + P_base*\|S_cosm\|` |
| `H0_PLANCK_CLASS` | FORECAST | km s^-1 Mpc^-1 | `100*(1 + S_cosm*A_bleed/A_in)` |
| `alpha_s_MZ` | FORECAST | 1 | `1/(e*pi)` |
| `n_s` | FORECAST | 1 | `1 + S_cosm*C_cosm*phi**(1/pi)` |
| `Omega_b_h2` | FORECAST | 1 | `\|S_cosm\|*(1 - S_chem)` |
| `Omega_DM_h2` | FORECAST | 1 | `(1 - S_chem)*phi*A_in` |
| `First_Riemann_zero` | MATH_IDENTITY | 1 | `e/gamma**3` |
| `Dark_energy_wa` | FORECAST | 1 | `-gamma*e*phi/pi` |
| `sigma_8` | FORECAST | 1 | `\|S_cosm\|*S_quant + \|Chaos\|` |
| `N_eff` | FORECAST | 1 | `P_new*e*pi + ln(phi)` |
| `inv_alpha_em` | FORECAST | 1 | `e**3 * phi**4 - psi_con` |
| `sin2_theta_W` | FORECAST | 1 | `sqrt(e)*P_new*eta_eff` |
| `Omega_Lambda` | FORECAST | 1 | `S_quant/e + gamma**2` |
| `m_pi_over_m_p` | FORECAST | 1 | `K*P_new*ln(pi)` |
| `m_mu_over_m_e` | FORECAST | 1 | `(35*phi**(-5)+145)*e**(1/3)` |
| `m_tau_over_m_e` | FORECAST | 1 | `9*pi*phi**10` |
| `IE_H` | FORECAST | eV | `gamma**(-5) - G**(-8)` |
| `H2O_bond_angle` | FORECAST | deg | `e**3 / gamma**3` |
| `Water_triple_K` | FORECAST | K | `pi**5 * sin(pi/phi) * C_eff` |
| `BP_H2O` | CONSTANT_IDENTITY | K | `e**6 - pi**3` |
| `tau_reion` | FORECAST | 1 | `phi*\|Chaos\| - ln(phi)` |

`BP_H2O` is registered as `CONSTANT_IDENTITY` (inventory). `First_Riemann_zero` is registered as `MATH_IDENTITY`. Im(ρ₁) = 14.134725… is a mathematical constant. The expression is compared with that constant. It is not a forecast of a future measurement. `predictions/LEDGER_A_FREEZE.yaml` still says `FORECAST` for this row. That freeze file was not rewritten. The other rows are registered as `FORECAST`.

## Literature anchors

Each anchor below is a published value typed into `scripts/fsot_ledger_a_lib.py` and used only by `compare_anchor`. The anchor is not an input to the expression. The number in the code is the rounded literature value. CODATA 2022 gives 1/α = 137.035999177(21). The code stores 137.036. Kill-band width is the length of the interval already written in `kill_band`. Those intervals are wider than the measurement uncertainties. `First_Riemann_zero` is the exception: its anchor is a math identity (Odlyzko / LMFDB), so its role is not "literature anchor".

| Id | Anchor role | Citation | Kill-band width |
|----|-------------|----------|----------------:|
| `T_CMB` | literature anchor | CODATA/PDG CMB monopole | 0.003 K |
| `H0_PLANCK_CLASS` | literature anchor | Planck 2018 TT,TE,EE+lowE+lensing | 3 km s^-1 Mpc^-1 |
| `alpha_s_MZ` | literature anchor | PDG α_s(M_Z) | 0.004 |
| `n_s` | literature anchor | Planck 2018 n_s | 0.03 |
| `Omega_b_h2` | literature anchor | Planck 2018 Ω_b h² | 0.0017 |
| `Omega_DM_h2` | literature anchor | Planck 2018 Ω_c h² class | 0.020 |
| `First_Riemann_zero` | math identity | Odlyzko / LMFDB Im(ρ₁) | 0.01 |
| `Dark_energy_wa` | literature anchor | w_a class (DESI/Planck-style) | 0.45 |
| `sigma_8` | literature anchor | Planck 2018 σ₈ | 0.07 |
| `N_eff` | literature anchor | Planck N_eff | 0.6 |
| `inv_alpha_em` | literature anchor | CODATA 1/α | 0.3 |
| `sin2_theta_W` | literature anchor | PDG sin²θ_W | 0.02 |
| `Omega_Lambda` | literature anchor | Planck Ω_Λ | 0.07 |
| `m_pi_over_m_p` | literature anchor | PDG m_π⁺/m_p | 0.01 |
| `m_mu_over_m_e` | literature anchor | CODATA m_μ/m_e | 1.5 |
| `m_tau_over_m_e` | literature anchor | PDG m_τ/m_e | 40 |
| `IE_H` | literature anchor | NIST H ionization energy | 0.2 eV |
| `H2O_bond_angle` | literature anchor | CRC H₂O bond angle | 1 deg |
| `Water_triple_K` | literature anchor | ITS-90 water triple point | 0.3 K |
| `BP_H2O` | literature anchor | CRC boiling point of water | none (inventory text only) |
| `tau_reion` | literature anchor | Planck τ_reion | 0.03 |

The integers 35 and 145 in `m_mu_over_m_e`, and the twelve-digit exponent behind `e**(1/3)`, have no recorded derivation. See [`AUTHORITY_REVISION_NOTES.md`](AUTHORITY_REVISION_NOTES.md).

Held-out scores for preregistered rows, with the freeze date and hash, are in [`data/held_out_prereg_report.json`](../data/held_out_prereg_report.json). Regenerate with `python scripts/held_out_prereg_report.py`. Those rows stay out of the scalar-gate green count.

<!-- TODO: published uncertainty for each anchor is not copied here. Do not fill one in. -->

<!-- TODO: formulas outside this Ledger A registry are not counted here. Do not state a formula count for the rest of the repo. -->
