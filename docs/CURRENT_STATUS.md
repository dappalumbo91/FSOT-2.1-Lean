# FSOT repo — current status (generated)

**Generated:** `2026-08-05T12:36:16.765934+00:00`  
**Edition stamp:** 2026-08-05  
**Regenerate:** `python scripts/build_repo_status_snapshot.py`

> Authoritative live numbers for expansion. Prefer this file over hand-edited counts in README when they disagree.

## Authority

| Item | Value |
|------|-------|
| Pin | **D1D38A** |
| Match | **True** |
| SHA-256 | `D1D38A185487B452…` |
| Path | `vendor/fsot_compute.py` |

## Empirical green gate

| Item | Value |
|------|-------|
| Green pass | **432 / 432** |
| Fail | 0 |
| Gate | ≤ 0.5% pooled median |
| Median-of-medians | 0.000561846% |
| Scalar records (envelope) | 61335 |
| Tiers | `{'B_verified': 329, 'A_strong': 95}` |

## Multiprover

| Item | Value |
|------|-------|
| overall_ok | **True** |
| github_ready | **True** |
| seven_way_bare_metal | True |
| eight_way_hardware | True |
| Atomic provable | 1904 |
| Catalog obligations | 2025 |
| True margin violations | **0** |
| Structural bundle excluded | 54 (export indices, not residual fails) |

Frameworks passed: `coq`, `cross_refinement`, `esp32_harness`, `fstar`, `fstar_refinement`, `hardware_bare_metal`, `isabelle`, `isabelle_refinement`, `lean_connective`, `python_decimal`, `qemu_harness`, `rust_lean_bridge_parity`, `rust_lean_bridge_refinement`, `rust_refinement`, `rust_replay`, `smt_catalog_bounds`, `tla_domain_routing`

## Expansion highlights (recent)

- **Documentation accuracy pass:** DOCUMENTATION_MAP + REPRODUCIBILITY; math key §14 PhD; live green/pin in generators
- Dzhanibekov / intermediate-axis vacuum flip: [`docs/DZHANIBEKOV_FSOT_RESPONSE.md`](DZHANIBEKOV_FSOT_RESPONSE.md)
- Proper densify (formula + real data only): [`docs/FSOT_PROPER_DENSIFY_POLICY.md`](FSOT_PROPER_DENSIFY_POLICY.md)
- Multiprover debt clarified: [`docs/MULTIPROVER_DESIGN_DEBT_CLARIFIED.md`](MULTIPROVER_DESIGN_DEBT_CLARIFIED.md)
- Hardware depth: [`docs/HARDWARE_DEPTH_CACHE_INTERCONNECT.md`](HARDWARE_DEPTH_CACHE_INTERCONNECT.md)
- Breakthroughs / QCE: [`docs/RECENT_BREAKTHROUGH_EXPANSION.md`](RECENT_BREAKTHROUGH_EXPANSION.md)

## Sync rule

After any densify / new panel / multiprover run: python scripts/build_repo_status_snapshot.py then update README headlines if green count or multiprover flags change. See docs/REPO_SYNC_AND_EXPANSION_CHECKLIST.md

Checklist: [`REPO_SYNC_AND_EXPANSION_CHECKLIST.md`](REPO_SYNC_AND_EXPANSION_CHECKLIST.md)

Machine JSON: [`data/repo_status_snapshot.json`](../data/repo_status_snapshot.json)
