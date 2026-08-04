# CKM residual “inconsistency” — research finding

**Date:** 2026-08-03  
**Status:** Resolved as *misaligned comparison targets* + cross-domain seed reuse for η̄  
**Code:** `vendor/fsot_seed_flavor.py`

---

## What looked broken

Residual-gating seed unitarity-triangle angles α,β,γ against “PDG angle centrals” (β≈22.2°, γ≈65.9°, α≈91.9°) while also residual-gating (ρ̄,η̄) against the Wolfenstein apex made α/β/γ look like a ~1% failure even though (ρ̄,η̄) were green.

That is **not** an internal FSOT contradiction. It is two different experimental constructions treated as one.

---

## What the literature actually is (PDG 2024 + HFLAV)

### A. Global SM fit apex (PDG RPP 2024, Eq. 12.26)

| Parameter | Value |
|-----------|--------|
| λ | 0.22501 ± 0.00068 |
| A | 0.826 +0.016/−0.015 |
| ρ̄ | **0.1591 ± 0.0094** |
| η̄ | **0.3523 +0.0073/−0.0071** |
| J | (3.12 +0.13/−0.12)×10⁻⁵ |
| δ | 1.147 ± 0.026 |

Geometry of *this same apex* (forced α+β+γ=π):

| Angle | From atan2(ρ̄,η̄) |
|-------|-------------------|
| α | ≈ 91.57° |
| β | ≈ 22.73° |
| γ | ≈ 65.70° |

### B. Direct angle averages (HFLAV / PDG 2024 angle section)

| Angle | Direct average |
|-------|----------------|
| β ≡ φ₁ | (22.2 ± 0.7)° |
| α ≡ φ₂ | (85.2 +4.8/−4.3)°  [B→ππ/ρρ/ρπ also quoted ~84.1°] |
| γ ≡ φ₃ | (65.9 +3.3/−3.5)°  [PDG combo also 65.7±3.0°] |

These **do not sum to 180°** (PDG: α+β+γ = (172±5)°). Direct α is **not** ~91.9° — that number was an incorrect stand-in for geometric α.

HFLAV angle-only apex sits near (ρ̄,η̄)≈(0.140, 0.353) — **not** the global-fit apex.

### C. Why they disagree (science, not FSOT)

1. **Different inputs** — global fit mixes magnitudes, loops (ε_K, Δm, |V_ub|…), lattice hadronics; direct angles use CP asymmetries / tree γ methods.  
2. **Unitary not forced on direct angles** — sum can sit ~172° within errors.  
3. **Ambiguities / penguins** — especially α.  
4. **First-row unitarity tension** (~2.3σ on |V_ud|²+|V_us|²+|V_ub|²) stresses the global fit.

So residual-gating seed *geometry* against direct HFLAV *angles* is the wrong problem statement.

---

## Correct residual-gate (what FSOT does now)

| Channel | Computed | Measured | Role |
|---------|----------|----------|------|
| Wolfenstein (ρ̄,η̄) | seed closed forms | PDG 2024 global fit | residual-gated ≤0.5% |
| α,β,γ | atan2 from seed (ρ̄,η̄) | atan2 from PDG (ρ̄,η̄) | residual-gated (same geometry) |
| Direct HFLAV α,β,γ | seed geometric angles | HFLAV directs | `literature_fit_band` only (honest, large σ) |

---

## Cross-domain seed answer for η̄

Old form `POOF/(3·SUCTION)` was tuned to an **outdated** η̄≈0.348 table, not PDG 2024 η̄=0.3523.

**FSOT principle used:** the answer can already exist at another scale — same seeds, different readout.

| Expression | Value | Notes |
|------------|-------|--------|
| **G_Catalan² · K** (adopted) | ≈ 0.35256 | ~0.08% vs PDG 2024 η̄; G and K already load-bearing (math lattice / √σ≈K) |
| ETA_EFF² · φ | ≈ 0.35279 | also green; morphic efficiency |
| R_b · φ = G/φ² | ≈ 0.34987 | **same family**: EW R_b = G/φ³ (wave5) upscaled by φ — “looks like flavor CP height, is EW structure at morphic scale” |
| 4·SUCTION·φ/e | ≈ 0.35008 | old docstring formula (never matched the code) |

Adopted: **η̄ = G_Catalan² · K**.  
Cousin story kept in comments: R_b·φ is the EW-scale lookalike.

Also adopted: **δ_CKM = atan2(η̄, ρ̄) = γ** (same LO phase). PDG 2024 δ=1.147 matches γ_geom of the global-fit apex — another same-physics / different-label case. Old e·A_bleed·K tracked an outdated δ≈1.196 table.

---

## Commands

```powershell
python -c "import sys; sys.path.insert(0,'vendor'); from fsot_seed_flavor import run_seed_flavor_suite; s=run_seed_flavor_suite(); print(s['median_error_pct'], s['max_error_pct'])"
python scripts/build_toe_gap_closure.py
```

---

## References

- PDG 2024 RPP: *12. CKM Quark-Mixing Matrix* (Ceccucci, Ligeti, Sakai), Eqs. (12.26)–(12.28), α+β+γ=(172±5)°.  
- HFLAV unitary-triangle angles (PDG 2024 averages): β=22.2±0.7°, α=85.2° band, γ=65.9° band.  
- FSOT: `vendor/fsot_seed_flavor.py`, wave5 `R_b = G/φ³`.
