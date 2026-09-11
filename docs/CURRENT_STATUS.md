# FSOT repo — current status (generated)

**Generated:** `2026-09-11T19:19:40.535846+00:00`  
**Edition stamp:** 2026-09-11  
**Regenerate:** `python scripts/build_repo_status_snapshot.py`

> Authoritative live numbers for expansion. Prefer this file over hand-edited counts in README when they disagree.

## Authority

| Item | Value |
|------|-------|
| Pin | **D1D38A** |
| Match | **True** |
| SHA-256 | `3090BC36956807F9…` |
| Path | `vendor/fsot_compute.py` |
| Formula authority | **FORMULA_AUTHORITY_SYSTEM_CLOSED** (all_ok=True) |
| Parameters | **ZERO_FREE — 0.99/0.01/10 are π identities; look/hits named seeds; f_domain=ALPHA. See docs/FROZEN_KNOBS.md.** |

## Three ledgers (never mixed)

Verbs: **A predicts** · **B corrects** · **C checks**. Spec: [`LEDGERS.md`](LEDGERS.md).

### Ledger A — closed-form predict

| Item | Value |
|------|-------|
| Emit | `python scripts/predict_closed_form.py --observable T_CMB` (no measured input) |
| Compare | `python scripts/compare_to_anchor.py --observable T_CMB` |
| What may say “predicted” | seed formula + frozen folds only |
| Misses | [`../results/MISSES.md`](../results/MISSES.md) |

### Ledger B — catalog residual (correction, not ToE accuracy)

| Item | Value |
|------|-------|
| Green pass | **477 / 477** |
| Fail | **0** |
| Gate | ≤ 0.5% pooled median |
| Median-of-medians | 0.006625234573930708% |
| Scalar records (envelope) | 181477 |
| Tiers | `{'B_verified': 337, 'C_thin': 13, 'A_strong': 118}` |
| Cite as ToE accuracy | **no** |

### Ledger C — live integrity

| Item | Value |
|------|-------|
| Pin match | **True** |
| Multiprover overall_ok | see below |
| Role | stream / hash / holdout identity — not a residual |

## Empirical green gate (Ledger B detail)

| Item | Value |
|------|-------|
| Green pass | **477 / 477** |
| Fail | **0** |
| Gate | ≤ 0.5% pooled median |
| Median-of-medians | 0.006625234573930708% |
| Scalar records (envelope) | 181477 |
| Tiers | `{'B_verified': 337, 'C_thin': 13, 'A_strong': 118}` |

## Mathlib re-derivation (Formal corpus)

| Item | Value |
|------|-------|
| Verdict | **FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED** |
| Theorems | **5248 / 5248** (100.0%) |
| Engine Mathlib % | 100.0 (L1=0) |
| Corpus L1 left | 0 |
| Engine core closed | True |
| Full corpus closed | True |

## Multiprover

| Item | Value |
|------|-------|
| overall_ok | **True** |
| github_ready | **True** |
| seven_way_bare_metal | True |
| eight_way_hardware | True |
| Atomic provable | 2024 |
| Full formal obligations | 2587 |
| Catalog obligations | 2256 (domains 477) |
| True margin violations | **0** |
| Structural bundle excluded | 0 |

Frameworks passed: `coq`, `cross_refinement`, `esp32_harness`, `fstar`, `fstar_refinement`, `hardware_bare_metal`, `isabelle`, `isabelle_refinement`, `lean_connective`, `python_decimal`, `qemu_harness`, `rust_lean_bridge_parity`, `rust_lean_bridge_refinement`, `rust_refinement`, `rust_replay`, `smt_catalog_bounds`, `tla_domain_routing`

## ToE labels (frozen checklist)

| Item | Value |
|------|-------|
| Label A (empirical framework) | **True** |
| Label B (classical T1–T6) | **True** |
| Report | `data/toe_gap_closure_report.json` |

## Predictions

| Item | Value |
|------|-------|
| Hand PREDs | **77** (PRED-001–084) |
| Dated scores | hold 65 · kill 45 · awaiting 4 |
| Score table | [`../results/dated_forecast_scores/REPORT.md`](../results/dated_forecast_scores/REPORT.md) |
| Expansion map | [`../predictions/reports/PREDICTION_EXPANSION_MAP.md`](../predictions/reports/PREDICTION_EXPANSION_MAP.md) |

08-31 / 09-01 EQ+hydro score after **2026-09-08**. Volcanic **2026-09-08**. Do not rewrite issued JSON.

## Claim evidence (kill commands)

- Machine map for skeptics / dismissals: [`EMPIRICAL_CLAIM_EVIDENCE.md`](EMPIRICAL_CLAIM_EVIDENCE.md)
- Mathlib campaign: [`MATHLIB_REDERIVATION_CAMPAIGN.md`](MATHLIB_REDERIVATION_CAMPAIGN.md)
- Skeptic kit: [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md)

## Expansion highlights (recent)

- Dzhanibekov / intermediate-axis vacuum flip: [`docs/DZHANIBEKOV_FSOT_RESPONSE.md`](DZHANIBEKOV_FSOT_RESPONSE.md)
- Proper densify (formula + real data only): [`docs/FSOT_PROPER_DENSIFY_POLICY.md`](FSOT_PROPER_DENSIFY_POLICY.md)
- Multiprover debt clarified: [`docs/MULTIPROVER_DESIGN_DEBT_CLARIFIED.md`](MULTIPROVER_DESIGN_DEBT_CLARIFIED.md)
- Hardware depth: [`docs/HARDWARE_DEPTH_CACHE_INTERCONNECT.md`](HARDWARE_DEPTH_CACHE_INTERCONNECT.md)
- Breakthroughs / QCE: [`docs/RECENT_BREAKTHROUGH_EXPANSION.md`](RECENT_BREAKTHROUGH_EXPANSION.md)
- Reality OS sibling (FSOT-native kernel lab): https://github.com/dappalumbo91/FSOT-Reality-OS
- Object scoring (H₀ / S₈ / wₐ / Euclid): [`OBJECT_SCORING.md`](OBJECT_SCORING.md)
- Genetics Å objects + CASP protocol: [`GENETICS_CLAIM_EVIDENCE.md`](GENETICS_CLAIM_EVIDENCE.md) · [`CASP_CAMEO_BLIND_PROTOCOL.md`](CASP_CAMEO_BLIND_PROTOCOL.md)
- Research standpoint / laws of reality: [`RESEARCH_STANDPOINT.md`](RESEARCH_STANDPOINT.md) · [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md)
- Seismology APPLY cookbook: [`APPLY_SEISMOLOGY.md`](APPLY_SEISMOLOGY.md)
- Isolated residuals (do not stuff): [`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md) · [`FRB_INTERFACE_DIAGNOSIS.md`](FRB_INTERFACE_DIAGNOSIS.md)
- D11 orifice-scale triangulation: [`DYNAMIC_SYSTEM_TRIANGULATION.md`](DYNAMIC_SYSTEM_TRIANGULATION.md)
- Uniqueness attractor Lean (not YM path-integral): [`UNIQUENESS_RESEARCH_SPINE.md`](UNIQUENESS_RESEARCH_SPINE.md)
- Materials/fuels design sibling: https://github.com/dappalumbo91/FSOT-Materials

## Sync rule

After any densify / new panel / multiprover / Mathlib run: python scripts/build_repo_status_snapshot.py && python scripts/build_skeptic_replication_kit.py then update README headlines if green count or multiprover flags change. See docs/REPO_SYNC_AND_EXPANSION_CHECKLIST.md

Checklist: [`REPO_SYNC_AND_EXPANSION_CHECKLIST.md`](REPO_SYNC_AND_EXPANSION_CHECKLIST.md)

Machine JSON: [`data/repo_status_snapshot.json`](../data/repo_status_snapshot.json)
