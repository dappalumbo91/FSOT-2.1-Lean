# TOE gap closure runbook

Generated: `2026-08-04T03:00:34.692232+00:00`

Frozen boundaries: [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md).

## Status snapshot

- **Label A (empirical multi-domain framework):** **PASS**
- **Label B (classical ToE T1–T6):** **PASS**

| Criterion | Pass | Artifact |
|-----------|:----:|----------|
| T1_ontology | YES | `data/foundational_ontology_axioms.yaml` |
| T2_dynamics | YES | `vendor/fsot_dynamics.py + data/toe_dynamics_benchmark.json` |
| T3_limit_recovery | YES | `data/toe_limit_recovery_benchmark.json + vendor/fsot_gr_sm.py` |
| T4_force_or_scope | YES | `vendor/fsot_gr_sm.py + data/toe_force_package_manifest.json` |
| T5_prereg_freeze | YES | `data/toe_prereg_freeze.json` |
| T6_falsification | YES | `data/falsification_registry_closure.json` |

## T2 Dynamics (what was added)

Module: `vendor/fsot_dynamics.py`

- Continuity + momentum with seed-locked viscosity μ(D_eff)
- Scalar transport toward S_eq(D_eff) with bleed κ and observer source J_obs
- Benchmark: `data/toe_dynamics_benchmark.json`

## T3 Limit recovery — deep GR map

Modules: `vendor/fsot_dynamics.py` + **`vendor/fsot_gr_sm.py`**

- Einstein tensor structure identity (trace-reverse)
- Weak-field g₀₀ / gᵢᵢ
- Poisson continuum source
- Schwarzschild radius (Sun)
- Solar light deflection
- Mercury perihelion advance (arcsec/century)
- Friedmann H² bridge
- Acoustic null cone (fluid GR)
- Geodesic deviation scale
- Planck length + G + c
- Plus atlas domain-routed cosmo/QM probes
- Benchmark: `data/toe_limit_recovery_benchmark.json`
- Deep panel: `data/toe_gr_sm_deep_benchmark.json`

**Honest scope:** executable recovery map + residual gates. **Not** a uniqueness theorem for the Einstein–Hilbert action or full spin-2 Fock quantization.

## T4 Force / matter package (v1)

Status: **`force_package_v1`**

Module: **`vendor/fsot_gr_sm.py`**  
Manifest: `data/toe_force_package_manifest.json`

### Package includes

1. Gauge group **U(1)_Y × SU(2)_L × SU(3)_c** (generator counts 1+3+8)
2. Couplings: α_em⁻¹, α_s(M_Z), sin²θ_W MS-bar + on-shell schemes (seed-closed)
3. Electroweak mass ladder: m_W, m_Z (on-shell), m_H, m_t
4. CKM/PMNS seed+NLO magnitudes, unitarity, complex multi-sector emergence
5. Three fermion generations (structural)
6. Electric charge quantization Q = T₃ + Y/2
7. Confinement scales: Λ_QCD, √σ; SU(3) Casimirs + β₀(n_f=5)
8. N_eff = 3 + 2·POOF·SUCTION; triangle α+β+γ=π
9. Spin-2 massless helicity / TT dof probes

### Depth shipped (granular expansion)

1. On-shell vs MS-bar Weinberg schemes → m_Z headroom
2. Λ_QCD, √σ, SU(3) Casimirs, β₀(n_f=5)
3. N_eff seed map; unitarity-triangle closure; spin-2 helicity/TT probes
4. CKM NLO magnitudes + multiprover spine
5. CKM α,β,γ residual-gated vs geometric PDG(ρ̄,η̄) centrals (≤0.5%)

### Closed on the executable probe / residual layer

1. CKM α,β,γ residual-gated vs **geometric** PDG(ρ̄,η̄) (≤0.5%)
2. Contested-sector FSOT panel green (13 hard problems have seed readouts; not external consensus)
3. Confinement + spin-2 **probe** inventories (Wilson/Polyakov/instanton/TT/Bianchi/…)

### Still open (theorems / social — not claimed)

1. Full non-abelian **path-integral** confinement *theorem*
2. Spin-2 graviton **Fock uniqueness** theorem from the fluid action
3. Uniqueness theorem for Einstein–Hilbert measure
4. Published CKM angle-*fit* centrals as residual gate (≠ geometric PDG ρ̄,η̄ by construction)


See also: [`docs/T3_T4_GR_SM_DEEPENING.md`](T3_T4_GR_SM_DEEPENING.md).

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
- GR classic tests: solar deflection, Mercury perihelion, Schwarzschild

## Commands

```powershell
python scripts/build_toe_gap_closure.py
python vendor/fsot_gr_sm.py
python scripts/audit_all_benchmark_margins.py
```
