# FSOT repo — current status (generated)

**Generated:** `2026-09-09T19:16:40.633073+00:00`  
**Edition stamp:** 2026-09-09  
**Regenerate:** `python scripts/build_repo_status_snapshot.py`

> Authoritative live numbers for expansion. Prefer this file over hand-edited counts in README when they disagree.

## Authority

| Item | Value |
|------|-------|
| Pin | **D1D38A** |
| Match | **True** |
| SHA-256 | `D1D38A185487B452…` |
| Path | `vendor/fsot_compute.py` |
| Formula authority | **FORMULA_AUTHORITY_SYSTEM_CLOSED** (all_ok=True) |
| Parameters | **ZERO_FREE — seed-derived constants and preregistered domain routes** |

## Empirical green gate

| Item | Value |
|------|-------|
| Green pass | **477 / 477** |
| Fail | **0** |
| Gate | ≤ 0.5% pooled median |
| Median-of-medians | 0.006625234573930708% |
| Scalar records (envelope) | 181477 |
| Tiers | `{'B_verified': 338, 'C_thin': 13, 'A_strong': 117}` |

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

## Sync rule

After any densify / new panel / multiprover / Mathlib run: python scripts/build_repo_status_snapshot.py && python scripts/build_skeptic_replication_kit.py then update README headlines if green count or multiprover flags change. See docs/REPO_SYNC_AND_EXPANSION_CHECKLIST.md

Checklist: [`REPO_SYNC_AND_EXPANSION_CHECKLIST.md`](REPO_SYNC_AND_EXPANSION_CHECKLIST.md)

Machine JSON: [`data/repo_status_snapshot.json`](../data/repo_status_snapshot.json)
