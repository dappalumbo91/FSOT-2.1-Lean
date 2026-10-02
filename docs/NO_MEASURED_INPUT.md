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
| `First_Riemann_zero` | FORECAST | 1 | `e/gamma**3` |
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

`BP_H2O` is registered as `CONSTANT_IDENTITY` (inventory). The others are registered as `FORECAST`.

Held-out scores for preregistered rows, with the freeze date and hash, are in [`data/held_out_prereg_report.json`](../data/held_out_prereg_report.json). Regenerate with `python scripts/held_out_prereg_report.py`. Those rows stay out of the scalar-gate green count.

<!-- TODO: published uncertainty for each anchor is not copied here. Do not fill one in. -->

<!-- TODO: formulas outside this Ledger A registry are not counted here. Do not state a formula count for the rest of the repo. -->
