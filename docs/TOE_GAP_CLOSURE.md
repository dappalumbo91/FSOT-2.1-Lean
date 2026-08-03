# TOE gap closure runbook

Generated: `2026-08-03T23:12:23.264967+00:00`

Frozen boundaries: [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md).

## Status snapshot

- **Label A (empirical multi-domain framework):** **PASS**
- **Label B (classical ToE T1–T6):** **PASS**

| Criterion | Pass | Artifact |
|-----------|:----:|----------|
| T1_ontology | YES | `data/foundational_ontology_axioms.yaml` |
| T2_dynamics | YES | `vendor/fsot_dynamics.py + data/toe_dynamics_benchmark.json` |
| T3_limit_recovery | YES | `data/toe_limit_recovery_benchmark.json` |
| T4_force_or_scope | YES | `docs/TOE_GAP_CLOSURE.md §T4` |
| T5_prereg_freeze | YES | `data/toe_prereg_freeze.json` |
| T6_falsification | YES | `data/falsification_registry_closure.json` |

## T2 Dynamics (what was added)

Module: `vendor/fsot_dynamics.py`

- Continuity + momentum with seed-locked viscosity μ(D_eff)
- Scalar transport toward S_eq(D_eff) with bleed κ and observer source J_obs
- Benchmark: `data/toe_dynamics_benchmark.json`

## T3 Limit recovery (what was added)

- GR weak-field probe (2Φ folded with K·|S|·Poof)
- QM de Broglie scale probe
- SM bridges (Weinberg sin²θ_W, α⁻¹, Higgs route)
- SI exact c
- Benchmark: `data/toe_limit_recovery_benchmark.json`

**Honest scope:** probes and bridges, not full Einstein–Hilbert or full SM Lagrangian derivation.

## T4 Force / matter package **or** scope

### Explicit scope (until full interaction Lagrangian exists)

FSOT Label B work **includes**:

1. Seed-locked scalar + dimensional interface field D_eff(x)
2. Fluid continuum dynamics with observer coupling
3. Multi-domain residual law across the scientific atlas
4. Contested-sector public anchors (H₀, dark energy, N_eff, σ₈, m_H, …)

FSOT Label B work **does not yet claim**:

1. Complete non-abelian gauge sector derivation of the Standard Model
2. Full quantized spin-2 graviton from the fluid action
3. Finished resolution of all 13 contested open problems

This scope statement is intentional and frozen until T3 deepens into full recovery theorems.

## T5 Prereg freeze

File: `data/toe_prereg_freeze.json` (SHA-256 bundle).  
Do not retune sector predictions without a new freeze id.

## Data pulled / cited

- Planck 2018 cosmology anchors (arXiv:1807.06209)
- SH0ES local H₀ (arXiv:2112.04510)
- PDG particle properties (pdg.lbl.gov)
- CODATA SI constants (NIST)
- DESI public data portal (data.desi.lbl.gov)
- Contested refresh: `data/toe_contested_sector_refresh.json`

## Commands

```powershell
python scripts/build_toe_gap_closure.py
python scripts/audit_all_benchmark_margins.py
```
