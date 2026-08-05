# Mathlib re-derivation campaign

**Generated:** 2026-08-05T22:17:26.616833+00:00  
**Verdict:** `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED`  
**Engine core closed:** True  
**Corpus Mathlib-depth %:** 16.6%  (860/5182)

## What this campaign is

Automated, wave-ordered campaign to drive **independent Mathlib-style proof depth**
across `FSOT/Formal` — beyond residual multiprover numeric certificate replay.

| Tier | Meaning |
|------|---------|
| L0_definitional | `rfl` / decide structural identities |
| L1_certificate | `norm_num` numeric certificates (typical priors) |
| L2_analytic | `linarith` / `nlinarith` / `ring` / `positivity` |
| L3_chain | multi-step `exact` / `have` / `refine` chains |

## Wave results

| Wave | Role | Thms | Mathlib% | Lake | OK |
|------|------|-----:|---------:|:----:|:--:|
| `W0_scalar_defs` | engine | 32 | 43.75 | passed | ✓ |
| `W1_bounds` | engine | 277 | 76.53 | passed | ✓ |
| `W2_theorems` | engine | 54 | 79.63 | passed | ✓ |
| `W3_domains` | engine | 43 | 23.26 | passed | ✓ |
| `W4_cosmology` | engine | 64 | 34.38 | passed | ✓ |
| `W5_bridge` | engine | 54 | 35.19 | passed | ✓ |
| `W6_priors_00` | priors | 171 | 4.68 | passed | ✓ |
| `W6_priors_01` | priors | 271 | 1.85 | passed | ✓ |
| `W6_priors_02` | priors | 148 | 4.73 | passed | ✓ |
| `W6_priors_03` | priors | 138 | 5.07 | passed | ✓ |
| `W6_priors_04` | priors | 128 | 0.78 | passed | ✓ |
| `W6_priors_05` | priors | 138 | 1.45 | passed | ✓ |
| `W6_priors_06` | priors | 138 | 2.9 | passed | ✓ |
| `W6_priors_07` | priors | 151 | 3.31 | passed | ✓ |
| `W6_priors_08` | priors | 158 | 2.53 | passed | ✓ |
| `W6_priors_09` | priors | 160 | 3.12 | passed | ✓ |
| `W6_priors_10` | priors | 137 | 3.65 | passed | ✓ |
| `W6_priors_11` | priors | 144 | 2.78 | passed | ✓ |
| `W6_priors_12` | priors | 139 | 2.88 | passed | ✓ |
| `W6_priors_13` | priors | 60 | 5.0 | passed | ✓ |

## Engine core modules

```text
W0 Scalar + ScalarEngineStructure
W1 Bounds          ← Mathlib exp/pi backbone
W2 Theorems        ← T1/T2/T3 analytic depth
W3 Domains
W4 Cosmology + waves
W5 Lab / Genomic / bridges
W6+ Priors batches (certificate-heavy by design)
```

## Upgrade queue (engine L1 → analytic)

| Module | Theorem |
|--------|---------|
| `Bounds` | `gamma_euler_pos` |
| `Bounds` | `pi_sub_one_pos` |
| `Bounds` | `exp_neg_one_lt_368` |
| `Bounds` | `log_08_gt_m0298` |
| `Bounds` | `log_12_lt` |
| `Bounds` | `sqrt_two_lt_14142135624` |
| `Bounds` | `new_perceived_param_lt_031` |
| `Bounds` | `new_perceived_param_lt_3009` |
| `Bounds` | `new_perceived_param_lt_30032` |
| `Bounds` | `new_perceived_param_pos` |
| `Bounds` | `cosmological_perceived_adjust_eq_one` |
| `Bounds` | `psi_con_pos` |
| `Bounds` | `psi_con_eta_pos` |
| `Bounds` | `sin_theta_s_nonneg` |
| `Bounds` | `exp_1144_lt_31415` |
| `Bounds` | `log_31415_gt_1144` |
| `Bounds` | `log_pi_gt_11445` |
| `Bounds` | `exp_049_gt_16181` |
| `Bounds` | `log_16181_lt_04813` |
| `Bounds` | `log_phi_lt_0482` |
| `Bounds` | `eta_log_phi_lt_0225` |
| `Bounds` | `exp_neg_185_lt_016` |
| `Bounds` | `log_016_gt_m185` |
| `Bounds` | `coherence_efficiency_gt_seven_tenths` |
| `Bounds` | `log_five_lt_one_seven_seven` |
| `Bounds` | `growth_term_cosmological_gt_one` |
| `Bounds` | `sqrt_25_eq_five` |
| `Bounds` | `sqrt_9_eq_3` |
| `Bounds` | `cosmological_N_pos` |
| `Bounds` | `cosmological_P_pos` |
| `Bounds` | `phase_variance_abs_le_one` |
| `Bounds` | `acoustic_bleed_lt_phi` |
| `Bounds` | `sin_eq_cos_pi_div_two_sub` |
| `Bounds` | `exp_04807_lt_1618` |
| `Bounds` | `log_1618_gt_04807` |
| `Bounds` | `exp_01534_lt_1168` |
| `Bounds` | `phase_variance_eq_cos_theta_s` |
| `Bounds` | `log_31416_lt_1146` |
| `Bounds` | `log_pi23847_lt_11453` |
| `Bounds` | `exp_neg_1434_lt_24_div_25` |

## Reproduction

```bash
python scripts/run_mathlib_rederivation_campaign.py --engine-only
python scripts/run_mathlib_rederivation_campaign.py
python scripts/run_mathlib_rederivation_campaign.py --wave W2_theorems
```

## Artifacts

- `data/mathlib_rederivation_inventory.json`
- `data/mathlib_rederivation_campaign_report.json`
- `docs/MATHLIB_REDERIVATION_CAMPAIGN.md`

## Honest boundary

Priors modules remain largely **L1 certificate** depth by design (multiprover
export pins). Engine waves are the Mathlib analytic spine. The flag
`full_mathlib_rederivation_of_all_lemmas` becomes true only when the campaign
verdict reaches full-corpus closure criteria (see report).
