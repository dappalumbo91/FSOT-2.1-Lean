# FSOT repo — current status (generated)

**Generated:** `2026-08-06T13:12:54.390448+00:00`  
**Edition stamp:** 2026-08-06  
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
| Green pass | **472 / 472** |
| Fail | **0** |
| Gate | ≤ 0.5% pooled median |
| Median-of-medians | 0.006607% |
| Scalar records (envelope) | 179914 |
| Tiers | `{'B_verified': 318, 'C_thin': 29, 'A_strong': 116}` |

## Mathlib re-derivation (Formal corpus)

| Item | Value |
|------|-------|
| Verdict | **FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED** |
| Theorems | **5182 / 5182** (100.0%) |
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
| Atomic provable | 2022 |
| Full formal obligations | 2585 |
| Catalog obligations | 2222 (domains 472) |
| True margin violations | **0** |
| Structural bundle excluded | 0 |

Frameworks passed: `coq`, `cross_refinement`, `esp32_harness`, `fstar`, `fstar_refinement`, `hardware_bare_metal`, `isabelle`, `isabelle_refinement`, `lean_connective`, `python_decimal`, `qemu_harness`, `rust_lean_bridge_parity`, `rust_lean_bridge_refinement`, `rust_refinement`, `rust_replay`, `smt_catalog_bounds`, `tla_domain_routing`

## ToE labels (frozen checklist)

| Item | Value |
|------|-------|
| Label A (empirical framework) | **True** |
| Label B (classical T1–T6) | **True** |
| Report | `data/toe_gap_closure_report.json` |

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

## Sync rule

After any densify / new panel / multiprover / Mathlib run: python scripts/build_repo_status_snapshot.py && python scripts/build_skeptic_replication_kit.py then update README headlines if green count or multiprover flags change. See docs/REPO_SYNC_AND_EXPANSION_CHECKLIST.md

Checklist: [`REPO_SYNC_AND_EXPANSION_CHECKLIST.md`](REPO_SYNC_AND_EXPANSION_CHECKLIST.md)

Machine JSON: [`data/repo_status_snapshot.json`](../data/repo_status_snapshot.json)
