# Mathlib re-derivation campaign

**Generated:** 2026-08-05T22:31:00.257203+00:00  
**Verdict:** `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED`  
**Engine core closed:** True  
**Corpus Mathlib-depth %:** 56.1%  (2907/5182)

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
| `W0_scalar_defs` | engine | 32 | 100.0 | passed | ✓ |
| `W1_bounds` | engine | 277 | 99.28 | passed | ✓ |
| `W2_theorems` | engine | 54 | 94.44 | passed | ✓ |
| `W3_domains` | engine | 43 | 97.67 | passed | ✓ |
| `W4_cosmology` | engine | 64 | 90.62 | passed | ✓ |
| `W5_bridge` | engine | 54 | 96.3 | passed | ✓ |
| `W6_priors_00` | priors | 171 | 63.16 | passed | ✓ |
| `W6_priors_01` | priors | 271 | 39.85 | passed | ✓ |
| `W6_priors_02` | priors | 148 | 74.32 | passed | ✓ |
| `W6_priors_03` | priors | 138 | 78.26 | passed | ✓ |
| `W6_priors_04` | priors | 128 | 71.88 | passed | ✓ |
| `W6_priors_05` | priors | 138 | 73.91 | passed | ✓ |
| `W6_priors_06` | priors | 138 | 72.46 | passed | ✓ |
| `W6_priors_07` | priors | 151 | 72.85 | passed | ✓ |
| `W6_priors_08` | priors | 158 | 74.68 | passed | ✓ |
| `W6_priors_09` | priors | 160 | 69.38 | passed | ✓ |
| `W6_priors_10` | priors | 137 | 78.1 | passed | ✓ |
| `W6_priors_11` | priors | 144 | 73.61 | passed | ✓ |
| `W6_priors_12` | priors | 139 | 64.03 | passed | ✓ |
| `W6_priors_13` | priors | 60 | 68.33 | passed | ✓ |

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
| `Bounds` | `sqrt_25_eq_five` |
| `Bounds` | `sqrt_9_eq_3` |
| `Cosmology` | `omega_b_h2_fsot_cached_pos` |
| `CosmologyExtendedPriors` | `cosmology_extended_components_sum` |
| `CosmologyExtendedPriors` | `cosmology_extended_within_le_total` |
| `CosmologyHigherWavesPriors` | `cosmology_higher_waves_partition` |
| `CosmologyLab` | `lambda_cdm_wave_partition` |
| `CosmologyWave4` | `wave4_observable_count_pos` |
| `Domains` | `dark_energy_delta_bounds` |
| `LeanProofsBridge` | `lean_proofs_domain_proven_le_formal` |
| `PhotonicForge` | `photonic_trinary_partition` |
| `Theorems` | `cosmological_delta_bounds` |
| `Theorems` | `cosmological_D_bounds` |
| `Theorems` | `cmb_delta_bounds` |

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
