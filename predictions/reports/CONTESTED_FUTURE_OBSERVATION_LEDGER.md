# Contested Future-Observation Ledger

*Generated 2026-08-06T12:48:36.058707+00:00 · pin D1D38A · freeze `TOE-PREREG-20260806`*

Future-observation differentiators for contested sectors. FSOT locks are pre-data; baseline defaults are current-model practice. No personal names. Pin D1D38A.

## Contested panel (current)

| Metric | Value |
|--------|------:|
| Observables | 13 |
| FSOT pooled median % | 0.007871 |
| Typical baseline % | 15.0 |
| Verdict | CONTESTED_SECTORS_FSOT_AHEAD_OF_CURRENT_MODELS |

## Future differentiators (pre-data)

| ID | Observable | FSOT lock | Baseline default | Future observation | Kill if |
|----|------------|-----------|------------------|--------------------|---------|
| FO-H0-ladder | H0_local_vs_CMB | `bridge_scalar_70.75_between_67.4_and_73.04` | separate_Planck_and_SH0ES_posteriors | JWST/HST local ladder + CMB-S4 early-universe H0 | FSOT bridge not strictly between next local and CMB centrals |
| FO-S8-lensing | S8_effective | `0.805_between_Planck_and_DES` | Planck_high_S8_vs_DES_low_S8_tension | Euclid + LSST year-1 weak lensing S8 | FSOT S8 outside next Planck–DES-class band |
| FO-wa-desi-euclid | w_a_CPL | `wa_approx_-1.018` | LCDM_wa_equals_0 | DESI DR2+/DR3 + Euclid BAO joint CPL (w0, wa) | desi_3sigma_exclusion of frozen wa or sign flip vs lock |
| FO-Neff-cmb | N_eff | `3.046` | SM_Neff_3.044_to_3.046 | Simons Observatory / CMB-S4 N_eff | cmb_3sigma_exclusion of frozen N_eff |
| FO-mH-pdg | m_H | `125.25_GeV` | SM_input_not_prediction | next PDG Higgs mass combination | pdg_update_outside_0_5pct of freeze |
| FO-cusp-core | dwarf_core_radius_rc | `0.6_kpc_Fornax_class` | CDM_cusp_vs_cored_baryon_feedback_models | dwarf spheroidal kinematic campaigns | core radius outside 0.5% band of freeze when consensus forms |
| FO-lithium-bbn | lithium_underproduction_factor | `factor_approx_3` | BBN_theory_vs_halo_star_gap | metal-poor star Li + BBN nuclear rate updates | gap factor outside 10% of frozen 3.0 |
| FO-frb-dm | FRB_DM_excess_vs_IGM | `200_pc_cm3_excess_class` | IGM_only_DM_models | CHIME/FRB high-DM catalog refresh | excess outside 0.5% of frozen central on panel refresh |
| FO-sigma8-central | sigma_8 | `0.8111` | LCDM_sigma8_from_Planck_primary | Euclid + LSST combined sigma8 | outside_0_5pct_of_frozen_central |
| FO-omega-lambda | Omega_Lambda | `0.6847` | LCDM_OmegaL_fit_parameter | combined BAO+CMB Omega_Lambda posterior | outside_0_5pct_of_frozen_central |

## Worst-green empirical watch (≤0.5% gate still holding)

| Domain | Pooled median % |
|--------|----------------:|
| Zebrafish_Predictive_Validation_Panel | 0.3579695 |
| Dark_Energy_CPL | 0.280515 |
| Econometrics | 0.12920090413715177 |
| Economics | 0.1292009041371501 |
| orbital_mechanics_benchmark.json | 0.106141 |
| Neuroeconomics | 0.10502056403980387 |
| cosmology_anomalies_benchmark.json | 0.096204 |
| Maillard_Chemistry | 0.09443694019339477 |

Ledger SHA-256: `053005368695e84dcf3f9a02c8613a8f762baff33c8091a604d70821f3ab4429`

Refresh: `python scripts/build_contested_future_observation_ledger.py`

Related: `docs/PREDATA_RISK.md` · `predictions/toe_prereg_freeze.json` · `predictions/reports/CONTESTED_SECTOR_WATCH.md`
