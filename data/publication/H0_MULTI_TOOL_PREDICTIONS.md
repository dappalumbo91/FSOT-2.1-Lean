# Multi-tool H₀ predictions (BH→WH bubble bleed)

*Generated 2026-08-06T13:12:34.037967+00:00 · pin D1D38A · 25 tools*

## Why not one number

Expansion rate readouts disagree because tools couple to different BH→WH information-flow / nebula-bleed sectors, not because there are two disconnected cosmologies.

**Global FSOT H₀** = `68.44005682979427` km/s/Mpc  
**Bleed fraction** = `0.015431`  
**Formula** = `H0_tool = H0_global_fsot * (1 + density_model * bubble_bleed_fraction)`

Each row is a **separate preregistered prediction** for that measurement system.
Kill criteria fire per tool — a SH0ES update does not retune Planck, and vice versa.

## Predictions (sorted by FSOT H₀)

| Tool | Class | Method | FSOT H₀ | Literature | Density | Err % |
|------|-------|--------|--------:|-----------:|--------:|------:|
| `planck_cmb_local` | early_universe_cmb | Planck2018_TTTEEE_lowE_lensing | **67.383958** | 67.4 | -1.0 | 0.023801 |
| `tdcosmo_conservative` | strong_lens_time_delay | TDCOSMO_mass_sheet_conservative | **67.436763** | 67.4 | -0.95 | 0.054545 |
| `planck_plus_bao_combo` | early_universe_cmb | Planck_plus_BAO_combo_literature | **67.647983** | 67.66 | -0.75 | 0.017761 |
| `sn_h0_no_local_cal` | snia_early_calibrated | SNIa_with_CMB_or_BAO_absolute_cal | **67.806398** | 67.8 | -0.6 | 0.009436 |
| `act_dr6_cmb` | early_universe_cmb | ACT_DR6_CMB | **67.859203** | 67.9 | -0.55 | 0.060084 |
| `spt3g_cmb` | early_universe_cmb | SPT3G_CMB | **68.281642** | 68.3 | -0.15 | 0.026878 |
| `global_cmb_background` | fsot_global | FSOT_Wave1_CMB | **68.440057** | 68.44005682979427 | 0.0 | 0.0 |
| `desi_bao_rs_anchored` | bao_intermediate | DESI_BAO_sound_horizon_anchor | **68.524545** | 68.52 | 0.08 | 0.006633 |
| `sdss_bao_class` | bao_intermediate | SDSS_BOSS_eBOSS_BAO | **68.598472** | 68.6 | 0.15 | 0.002228 |
| `wmap9_cmb` | early_universe_cmb | WMAP9_CMB | **69.9714** | 70.0 | 1.45 | 0.040858 |
| `gw_standard_siren` | multi_messenger_siren | GW_standard_siren_LVK | **70.024205** | 70.0 | 1.5 | 0.034578 |
| `trgb_ground_class` | intermediate_ladder | TRGB_ground_based_class | **70.256546** | 69.6 | 1.72 | 0.943314 |
| `freedman_jwst` | intermediate_ladder | JWST_TRGB | **70.393839** | 70.39 | 1.85 | 0.005454 |
| `carnegie_h0` | intermediate_ladder | Carnegie_Chicago_TRGB_ladder | **70.594498** | 69.8 | 2.04 | 1.138249 |
| `h0_bridge_scalar` | fsot_bridge | FSOT_bridge_between_planck_and_shoes | **70.763474** | 70.75 | 2.2 | 0.019044 |
| `jagb_miras_class` | intermediate_ladder | JAGB_Miras_distance_indicators | **70.921888** | 70.9 | 2.35 | 0.030872 |
| `fsot_document_local` | fsot_local_bubble | FSOT_local_bubble | **71.766767** | 72.1 | 3.15 | 0.462181 |
| `jwst_cepheid_riess` | local_ladder_cepheid | JWST_Cepheid_Riess_class | **73.456525** | 72.6 | 4.75 | 1.179786 |
| `sh0es_hst_cepheid` | local_ladder_cepheid | SH0ES_HST_Cepheid | **73.773354** | 73.04 | 5.05 | 1.004045 |
| `sh0es_jwst` | local_ladder_cepheid | SH0ES_Cepheid_TRGB_JWST | **73.826159** | 73.04 | 5.1 | 1.076341 |
| `h0licow_tdcosmo` | strong_lens_time_delay | H0LiCOW_TDCOSMO_time_delay_lensing | **73.984574** | 73.3 | 5.25 | 0.933935 |
| `surface_brightness_fluctuations` | local_ladder_sbf | SBF_distance_ladder | **74.037379** | 73.3 | 5.3 | 1.005974 |
| `pantheon_plus_shoes_cal` | local_ladder_snia | PantheonPlus_SNIa_SH0ES_calibration | **74.090184** | 73.5 | 5.35 | 0.802971 |
| `megamaser_cosmology` | geometric_maser | Megamaser_Cosmology_Project | **74.512623** | 73.9 | 5.75 | 0.82899 |
| `tully_fisher_class` | local_ladder_tf | Tully_Fisher_relation_class | **75.146282** | 75.1 | 6.35 | 0.061628 |

FSOT span: **67.383958 – 75.146282** km/s/Mpc  
Literature span: 67.4 – 75.1 km/s/Mpc

Bundle SHA-256: `d39e5cbb3fb947354325ab4b6f9ed39d3f93f1af44f410ea9bc03a339ac353e3`

Refresh: `python scripts/build_h0_multi_tool_predictions.py`

Seed: `data/sector_h0_seed.json` · Physics: `scripts/bubble_bleed_physics.py`
