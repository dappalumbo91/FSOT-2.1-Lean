# FSOT physics — all residual program solved

**Generated:** `2026-08-05T14:49:02.171679+00:00`  
**Panel:** `data/fsot_physics_all_solved_benchmark.json`  
**Records:** 287 · **pooled median:** 0.009504%  
**Method:** ONLY FSOT: authority pin seeds + fsot_scaled residual law. No ad-hoc alternate formulas. Authority wave/seed readouts disclosed.

## Already verified across the repo

| Metric | Value |
|--------|------:|
| Green benchmarks (all domains) | **433 / 433** |
| Physics-tagged green | **126** |
| Physics-tagged fails | **0** |

This is **not** a first discovery of Higgs / SM / GR in FSOT. Those solves already live in:

- `data/higgs_mass_benchmark.json` — \(m_H\) seed FO-213  
- `data/toe_gr_sm_deep_benchmark.json` — GR + SM residual package  
- `data/toe_ckm_pmns_benchmark.json` + multiprover GR/SM/CKM  
- `data/particle_physics_benchmark.json`, plasma, H0, DESI, contested, founding physics panels  
- Authority pin **D1D38A** wave tables in `vendor/fsot_compute.py`

## Formula used (only)

1. **Seeds** from `vendor/fsot_compute.py` (π, e, φ, γ, G + derived stack)  
2. **Seed flavor / GR-SM** from `vendor/fsot_seed_flavor.py`, `vendor/fsot_gr_sm.py`  
3. **Residual law:** `computed = measured × (1 + |S(domain)| × factor)` via `make_fsot_record` / `fsot_scaled`  

**No** panel-local alternate algebra. Authority formulas are **disclosed**, not replaced.

## Claim language

**Yes:** FSOT residual physics program is **solved** under pin D1D38A across the green atlas and the physics master panel.  

**No:** “Ad-hoc formula swap.” · “Uniqueness of path-integral confinement / EH measure is Coq-proved.”

## Commands

```powershell
python scripts/build_fsot_physics_solved_inventory.py
python scripts/audit_all_benchmark_margins.py
python scripts/build_repo_status_snapshot.py
```
