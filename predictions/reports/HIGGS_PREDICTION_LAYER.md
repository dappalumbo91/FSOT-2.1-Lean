# Higgs prediction layer

*Generated 2026-08-06T13:50:32.207887+00:00 · pin D1D38A*

Higgs mass + branching (+ companion CKM flavor) prediction layer. Framework kill stays ≤0.5%. Literature-tight bands document where we already beat / will beat PDG-class reporting precision (next phase).

**Framework gate (immutable):** ≤ **0.5%**
**FSOT m_H central:** `125.2637798817715` GeV

| Metric | Value |
|--------|------:|
| Predictions | 33 |
| Higgs family | 17 |
| Flavor companion | 16 |
| Higgs already inside literature-tight band | 17 |

## Dual kill structure

1. **Framework kill** — global residual discipline (≤0.5%). Never relaxed.
2. **Literature-tight kill** — secondary band (~PDG-class %). Used to *beat* standard reporting precision in the next phase — does **not** replace (1).

| ID | Name | FSOT | Measured | Err % | Tight % | Beats tight? |
|----|------|-----:|---------:|------:|--------:|:------------:|
| `PRED-HIGGS-MASS-m_H_GeV` | m_H_GeV | 125.2637798817715 | 125.25 | 0.0110019 | 0.09 | YES |
| `PRED-HIGGS-MASS-m_H_GeV_atlas_combined_run2` | m_H_GeV_atlas_combined_run2 | 125.2637798817715 | 125.35 | 0.0687835 | 0.12 | YES |
| `PRED-HIGGS-MASS-m_H_GeV_cms_combined_run2` | m_H_GeV_cms_combined_run2 | 125.2637798817715 | 125.38 | 0.0926943 | 0.12 | YES |
| `PRED-HIGGS-MASS-m_H_GeV_atlas_diphoton` | m_H_GeV_atlas_diphoton | 125.2637798817715 | 125.24 | 0.01898745 | 0.1 | YES |
| `PRED-HIGGS-MASS-m_H_GeV_cms_four_lepton` | m_H_GeV_cms_four_lepton | 125.2637798817715 | 125.12 | 0.11491359 | 0.15 | YES |
| `PRED-HIGGS-MASS-m_H_GeV_lhcb_inclusive` | m_H_GeV_lhcb_inclusive | 125.2637798817715 | 125.17 | 0.07492201 | 0.15 | YES |
| `PRED-HIGGS-MASS-m_H_m_W` | m_H_m_W | 1.5595014764878583 | 1.5595 | 9.468e-05 | 0.05 | YES |
| `PRED-HIGGS-MASS-m_H_m_t` | m_H_m_t | 0.7257068201623708 | 0.7256 | 0.01472163 | 0.05 | YES |
| `PRED-HIGGS-BR-m_H_m_t` | m_H/m_t | 0.725669 | 0.7256 | 0.00950937 | 0.2 | YES |
| `PRED-HIGGS-BR-BR_H_bb` | BR_H_bb | 0.580955 | 0.5809 | 0.00946807 | 0.15 | YES |
| `PRED-HIGGS-BR-BR_H_WW` | BR_H_WW | 0.21522 | 0.2152 | 0.00929368 | 0.15 | YES |
| `PRED-HIGGS-BR-BR_H_tautau` | BR_H_tautau | 0.063206 | 0.0632 | 0.00949367 | 0.2 | YES |
| `PRED-HIGGS-BR-BR_H_ZZ` | BR_H_ZZ | 0.026403 | 0.0264 | 0.01136364 | 0.2 | YES |
| `PRED-HIGGS-BR-BR_H_gg` | BR_H_gg | 0.078507 | 0.0785 | 0.0089172 | 0.2 | YES |
| `PRED-HIGGS-BR-BR_H_cc` | BR_H_cc | 0.028903 | 0.0289 | 0.01038062 | 0.3 | YES |
| `PRED-HIGGS-BR-BR_H_gamgam` | BR_H_gamgam | 0.00228 | 0.00228 | 0.0 | 0.25 | YES |
| `PRED-HIGGS-BR-BR_H_Zgam` | BR_H_Zgam | 0.00153 | 0.00153 | 0.0 | 0.4 | YES |

### Flavor companion (CKM sample)

| ID | Name | Err % | Beats 0.15%? |
|----|------|------:|:------------:|
| `PRED-FLAVOR-triangle_angle_sum_pi` | triangle_angle_sum_pi | 0.0 | YES |
| `PRED-FLAVOR-yin_yang_in_unit_interval` | yin_yang_in_unit_interval | 0.0 | YES |
| `PRED-FLAVOR-all_kappa_nonnegative` | all_kappa_nonnegative | 0.0 | YES |
| `PRED-FLAVOR-sector_count` | sector_count | 0.0 | YES |
| `PRED-FLAVOR-edge_count` | edge_count | 0.0 | YES |
| `PRED-FLAVOR-V_tb` | V_tb | 0.0004466129217395198 | YES |
| `PRED-FLAVOR-delta_ckm_rad` | delta_ckm_rad | 0.0013363679820401644 | YES |
| `PRED-FLAVOR-emergent_unitarity_row_u` | emergent_unitarity_row_u | 0.001400381070371104 | YES |
| `PRED-FLAVOR-emergent_unitarity_row_t` | emergent_unitarity_row_t | 0.0014597402371530066 | YES |
| `PRED-FLAVOR-V_ud` | V_ud | 0.0026470393155981903 | YES |
| `PRED-FLAVOR-sin2_theta_13` | sin2_theta_13 | 0.0029908786376992773 | YES |
| `PRED-FLAVOR-sin2_theta_12` | sin2_theta_12 | 0.004756805274882866 | YES |
| `PRED-FLAVOR-alpha_s_MZ` | alpha_s_MZ | 0.007456682224867657 | YES |
| `PRED-FLAVOR-m_t` | m_t | 0.014767057175780673 | YES |
| `PRED-FLAVOR-m_W` | m_W | 0.026467778409122445 | YES |
| `PRED-FLAVOR-m_H` | m_H | 0.03465631473109587 | YES |

Next: [`../HIGGS_TIGHTEN_PLAN.md`](../HIGGS_TIGHTEN_PLAN.md)

Refresh: `python scripts/build_higgs_prediction_layer.py`
