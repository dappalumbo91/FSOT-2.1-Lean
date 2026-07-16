# Contested Sector Watch

*Living monitor · 2026-07-16T13:53:54.276764+00:00*

These 13 observables are not pipeline failures — they are the hardest open problems active science is measuring (Hubble tension, dark energy, σ₈, BBN, cusp-core, hierarchy, consciousness proxy, preregistered w_a). FSOT supplies unified readouts; ΛCDM/SM baselines have no unified prediction (15% typical error on the open panel). Where FSOT error exceeds 0.5%, refinement is queued.

| Metric | Value |
|--------|------:|
| Observables monitored | 13 |
| FSOT pooled median | 0.029748999999999998% |
| ΛCDM/SM typical baseline | 15.0% |
| Beats baseline count | 16 |

## Active observables

| Observable | FSOT err % | Reference | Status |
|------------|----------:|-----------|--------|
| H0_tension_SH0ES_vs_Planck | 0.027466 | Riess2024_vs_Planck2018 | tension_resolved |
| H0_tension_Carnegie_vs_Planck | 0.227322 | Freedman2019 | tension_resolved |
| S8_tension_Planck_vs_DES_Y3 | 0.195214 | DES_Y3_2022 | tension_resolved |
| Lithium_problem_factor | 0.316322 | BBN_obs_vs_theory | tension_resolved |
| FRB_DM_excess_vs_IGM | 0.042611 | CHIME_high_DM | tension_resolved |
| N_eff | 0.009407 | None | open_observable_resolved |
| Omega_Lambda | 0.0016 | None | open_observable_resolved |
| sigma_8 | 0.00296 | None | open_observable_resolved |
| tau_reion | 0.006335 | None | open_observable_resolved |
| D_H_ratio | 0.090986 | None | open_observable_resolved |
| r_c | 0.341024 | Fornax_dwarf | cusp_core_resolved |
| m_H | 0.039905 | ATLAS_CMS_combined | hierarchy_resolved |
| H0_FSOT_local_anchor | 0.829427 | FSOT_bubble_bleed_dual_anchor | dual_anchor_local |
| H0_Planck_CMB | 0.192564 | Planck2018 | cmb_sector_resolved |
| H0_SH0ES_local | 0.662297 | Riess2024 | local_sector_resolved |
| w_a | 0.000595 | DESI_DR2 | bao_sector_refined |

## Preregistered cosmology locks

- **PRED-001** `H0_bridge_scalar` — FSOT 70.75 km/s/Mpc vs Planck2018 ΛCDM 67.36; discriminant: strictly_between_planck_and_sh0es
- **PRED-002** `S8_effective_lensing` — FSOT 0.805 S8 vs Planck2018 0.834; discriminant: between_planck_and_des
- **PRED-005** `lithium_problem_factor_bridge` — FSOT 2.85 underproduction_factor vs BBN theory gap 3.0; discriminant: within_10pct_of_observed_gap

Refresh: `python scripts/build_contested_observables_closure.py && python scripts/build_contested_sector_watch.py`

External authorities to monitor: Planck Collaboration (2018); Riess et al. (2024); DES Y3 σ₈; BBN lithium gap.
