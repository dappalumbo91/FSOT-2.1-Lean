# Mathlib re-derivation campaign

**Generated:** 2026-08-05T22:38:08.205071+00:00  
**Verdict:** `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED`  
**Engine core closed:** True  
**Corpus Mathlib-depth %:** 57.29%  (2969/5182)

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
| `W1_bounds` | engine | 277 | 100.0 | passed | ✓ |
| `W2_theorems` | engine | 54 | 100.0 | passed | ✓ |
| `W3_domains` | engine | 43 | 100.0 | passed | ✓ |
| `W4_cosmology` | engine | 64 | 100.0 | passed | ✓ |
| `W5_bridge` | engine | 54 | 100.0 | passed | ✓ |
| `W6_priors_00` | priors | 171 | 75.44 | passed | ✓ |
| `W6_priors_01` | priors | 271 | 41.7 | passed | ✓ |
| `W6_priors_02` | priors | 148 | 76.35 | passed | ✓ |
| `W6_priors_03` | priors | 138 | 78.99 | passed | ✓ |
| `W6_priors_04` | priors | 128 | 72.66 | passed | ✓ |
| `W6_priors_05` | priors | 138 | 77.54 | passed | ✓ |
| `W6_priors_06` | priors | 138 | 76.09 | passed | ✓ |
| `W6_priors_07` | priors | 151 | 73.51 | passed | ✓ |
| `W6_priors_08` | priors | 158 | 74.68 | passed | ✓ |
| `W6_priors_09` | priors | 160 | 70.0 | passed | ✓ |
| `W6_priors_10` | priors | 137 | 80.29 | passed | ✓ |
| `W6_priors_11` | priors | 144 | 72.22 | passed | ✓ |
| `W6_priors_12` | priors | 139 | 65.47 | passed | ✓ |
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

_No engine L1 upgrade candidates listed (or queue empty)._

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
