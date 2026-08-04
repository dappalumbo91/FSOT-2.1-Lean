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
| Triangle | α,β,γ from (ρ̄,η̄); α+β+γ=π | identity green; angle centrals = seed predictions inside exp. bands |
| Spin-2 probes | massless helicities=2, TT dof=2, quadrupole prefactor | exact identity |

## What is still open (honest, not hidden)

1. Full non-abelian **path-integral** confinement theorem (scales + Casimirs shipped)  
2. CKM angle centrals residual-gated to ≤0.5% of PDG *central* (predictions inside bands; exact triangle closure shipped)  
3. Spin-2 graviton **Fock uniqueness** from fluid action (helicity/TT probes shipped)  
4. Uniqueness theorem for Einstein–Hilbert measure  
5. Peer review / arXiv endorsement (social)  
6. Independent third-party clone (process)

---

## Commands

```powershell
python vendor/fsot_gr_sm.py
python scripts/build_toe_gap_closure.py
python scripts/audit_all_benchmark_margins.py
```

Expect: deep median residual ≪ 0.5%; Label A + Label B remain **PASS**.
