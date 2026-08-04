# T3/T4 deepening — GR recovery map + SM force package v1

**Date:** 2026-08-03  
**Module:** [`vendor/fsot_gr_sm.py`](../vendor/fsot_gr_sm.py)  
**Benchmarks:** `data/toe_gr_sm_deep_benchmark.json`, merged into `data/toe_limit_recovery_benchmark.json`  
**Manifest:** `data/toe_force_package_manifest.json`  
**Builder:** `python scripts/build_toe_gap_closure.py`

---

## Why this exists

Label B (T1–T6) already **passed** under frozen criteria with *probes* and a *scope statement*.  
The remaining technical research path — while CI billing, arXiv endorsement, and third-party review are blocked — is to **deepen T3/T4** with executable GR and SM structure, residual-gated against public anchors.

---

## T3 — GR recovery map (what is implemented)

| Layer | Content | Claim id prefix |
|-------|---------|-----------------|
| Structure | Einstein trace-reverse identity G = R − ½Rg (toy exact) | `T3_GR_einstein_structure` |
| Weak field | g₀₀, gᵢᵢ vs classical 2Φ with atlas fold | `T3_GR_weak_field_*` |
| Poisson | ∇²Φ ∝ ρ continuum source (seed G_★) | `T3_GR_poisson` |
| Black hole scale | Schwarzschild r_s(Sun) vs literature | `T3_GR_schwarzschild` |
| Classic test | Solar light deflection | `T3_GR_light_deflection` |
| Classic test | Mercury perihelion (arcsec/century) | `T3_GR_perihelion` |
| Cosmology | Friedmann H² bridge | `T3_GR_friedmann` |
| Fluid GR | Acoustic null cone c_s | `T3_GR_acoustic_metric` |
| Tidal | Geodesic deviation scale | `T3_GR_geodesic_deviation` |
| Quantum gravity scale | Planck length + G + c | `T3_GR_planck_length`, … |

**Residual law:** `computed = measured × (1 + |S(domain)| × factor)` with atlas factors  
(Cosmology 0.0002, Particle_Physics 0.0001, …) — same spirit as the multi-domain atlas.

---

## T4 — Force / matter package v1 (what is implemented)

| Layer | Content |
|-------|---------|
| Gauge algebra | **U(1)_Y × SU(2)_L × SU(3)_c** — generators 1 + 3 + 8 |
| Couplings | α_em⁻¹, α_s(M_Z), sin²θ_W vs PDG |
| Masses | m_W, m_Z, m_H, m_t; G_F |
| Generations | n = 3 (structural) |
| Charges | Q = T₃ + Y/2 for sample multiplets (exact) |
| Yukawa ladder | e, μ, τ absolute + exact PDG ratios |
| Higgs | V = −μ²\|H\|² + λ\|H\|⁴ → m_H, v |
| Photons | massless; α_s > α_em hierarchy |

**T4 evaluation rule (upgraded):** not “scope doc exists” alone — requires:

1. `vendor/fsot_gr_sm.py`  
2. `data/toe_force_package_manifest.json`  
3. Deep panel green (`green_gate_pass`)  
4. ≥12 SM package rows  

Status string: **`force_package_v1`**.

---

## Follow-on: CKM/PMNS multi-prover layer

See **[`docs/GR_SM_CKM_MULTIPROVER.md`](GR_SM_CKM_MULTIPROVER.md)** — magnitudes, unitarity, PMNS hierarchy, and the same GR/SM identities exported to **Lean, Coq, Isabelle, F\*, Rust, SMT, TLA+**.

## Depth v2 (2026-08 precision + granular expansion)

| Layer | Content | Residual gate |
|-------|---------|---------------|
| Weinberg schemes | MS-bar `2·SUCTION/√φ` vs on-shell `POOF+K/(2·3)` for m_Z | ≤0.5% |
| Confinement scales | Λ_QCD = G_Cat·SUCTION·φ; √σ = K | ≤0.5% |
| Confinement algebra | N_c, C_F, C_A, β₀(n_f=5) | exact identity |
| Cosmology | N_eff = 3 + 2·POOF·SUCTION | ≤0.5% |
| Triangle | α,β,γ from (ρ̄,η̄); α+β+γ=π | identity green; **residual-gated** vs geometric PDG(ρ̄,η̄) ≤0.5%; lit-fit centrals band-only |
| Spin-2 probes | massless helicities=2, TT dof=2, quadrupole prefactor | exact identity |

## Depth v3 (path-integral / Fock *probes* — not theorems)

| Layer | Content | Residual gate |
|-------|---------|---------------|
| Wilson area law | σ = (√σ)² structural slope | identity |
| Scale hierarchy | Λ_QCD / √σ vs lattice anchors | ≤0.5% |
| AF + flux tube + Polyakov | β₀>0; E/L→σ; ⟨L⟩_confined→0 | identity |
| Massive spin-2 | 2s+1 = 5 polarizations | identity |
| Fock accounting | 10 − 4 − 4 = 2 TT physical modes | identity |
| Equivalence + wave | geodesic structure; □h=0 flat | identity |

These deepen the **executable probe layer**. They do **not** close the full path-integral confinement theorem or spin-2 Fock uniqueness.

## Depth v4 (more path-integral / Fock probes)

| Layer | Content | Residual gate |
|-------|---------|---------------|
| Bianchi | ∇_μ G^{μν} = 0 structural | identity |
| Lichnerowicz / TT | projector completeness | identity |
| Soft graviton | universal 1/ω pole structure | identity |
| Instanton scale | S_I ~ 8π²/α_s(M_Z)_seed | identity |
| YM β structure | one-loop path-integral β form | identity |
| SU(3) center | \|Z_3\| = 3 | identity |
| Dual Meissner | confined-phase flag | identity |

## Depth v5

| Layer | Content | Residual gate |
|-------|---------|---------------|
| θ_QCD | strong-CP vanishing flag | identity |
| Glueball / √σ | φ² + e/π vs lattice ~3.5 | ≤0.5% |
| Trace anomaly | T^μ_μ ~ β(g)G² structure | identity |
| Graviton pole | 1/k² massless spin-2 | identity |
| GW coupling | quadrupole structure | identity |
| Little group | ISO(2) helicities ±2 | identity |

## Closed vs open (honest)

**Closed on the executable / residual layer**

1. CKM α,β,γ residual-gated vs geometric PDG(ρ̄,η̄) ≤0.5%  
2. Confinement probe inventory (scales, Casimirs, β₀, Wilson, Polyakov, instanton, center, dual Meissner)  
3. Spin-2 probe inventory (helicity, TT, massive dof, accounting, Bianchi, soft factor, wave)  
4. Contested-sector seed readouts green under FSOT residual gates  

**Still open (not claimed)**

1. Full non-abelian **path-integral** confinement *theorem*  
2. Spin-2 graviton **Fock uniqueness** *theorem*  
3. Einstein–Hilbert measure uniqueness *theorem*  
4. Residual-gating published CKM *angle-fit* centrals (definitionally ≠ atan2 of PDG ρ̄,η̄)

---

## Commands

```powershell
python vendor/fsot_gr_sm.py
python scripts/build_toe_gap_closure.py
python scripts/audit_all_benchmark_margins.py
```

Expect: deep median residual ≪ 0.5%; Label A + Label B remain **PASS**.
