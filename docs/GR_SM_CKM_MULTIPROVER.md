# GR / SM / CKM / PMNS — multi-prover layer

**Date:** 2026-08-04  
**Generator:** `python scripts/export_and_generate_gr_sm_ckm_artifacts.py`  
**Focused verify:** `python scripts/run_gr_sm_ckm_verification.py`  
**Obligations:** `verification/obligations/gr_sm_ckm_spine.json` (~250)  
**Benchmark:** `data/toe_ckm_pmns_benchmark.json`  
**Report:** `data/gr_sm_ckm_verification_report.json`  
**Cross-proof:** first-class section `gr_sm_ckm_spine` in `run_cross_proof_verification.py`

---

## What this layer is

Depth after T3/T4 force package v1 — filling flavor / phase / structure voids:

1. **CKM** magnitudes (PDG) + **row/column unitarity**  
2. **Wolfenstein** (λ, A, ρ̄, η̄) + LO maps (V_us, V_cb, V_ub) with documented truncation band  
3. **Jarlskog J** + CKM δ_CP (deg/rad) + unitary-triangle sides R_b, R_t  
4. **PMNS** sin²θ, angles, δ_CP, sin δ_CP, **Δm²_21 / |Δm²_31|** hierarchy  
5. **SM** charge quantization, gauge generators, **anomaly Tr Y = 0**, EW cos θ_W structure  
6. **GR** formal anchors (weak-field, light deflection, perihelion residuals)  

All residual magnitudes use the atlas law  
`computed = measured × (1 + |S|·factor)` with Particle_Physics / Cosmology factors.

## Multi-prover map

| System | Artifact | Discharge |
|--------|----------|-----------|
| **Python** | suite in `vendor/fsot_ckm_pmns.py` | residual gate + triangulation |
| **Lean** | `FSOT/Formal/GRSMCKMSpine.lean` | `norm_num` / `decide` |
| **Coq** | `verification/coq/GRSMCKMSpine.v` | `lra` / reflexivity |
| **Isabelle** | `verification/isabelle/GRSMCKMSpine.thy` | `simp` / `eval` |
| **F\*** | `verification/fstar/FSOTGRSMCKM.fst` | squash literals |
| **Rust** | `verification/rust/fsot_gr_sm_ckm_replay` | `cargo test` f64 asserts |
| **SMT** | `verification/smt/gr_sm_ckm_bounds.smt2` | Z3/CVC5 `check-sat` → sat |
| **TLA+** | `verification/tla/FSOTGRSMCKM.tla` | sector routing flow (no skipped gates) |

## Commands

```powershell
# One-shot multi-prover (Python + Rust + Z3 + Coq if installed)
python scripts/run_gr_sm_ckm_verification.py

# Or regenerate only
python scripts/export_and_generate_gr_sm_ckm_artifacts.py
cargo test --manifest-path verification/rust/fsot_gr_sm_ckm_replay/Cargo.toml

python scripts/build_toe_gap_closure.py
python scripts/audit_all_benchmark_margins.py
# Full Tier-91 cross-proof also runs the GR/SM/CKM layer in its pipeline
```

## Honesty

- Multi-prover stack re-proves **exported numeric/structural obligations**, not a uniqueness theorem for Einstein–Hilbert or a unique seed-only derivation of every complex CKM phase.  
- LO Wolfenstein maps store full truncation error as `lo_error_pct` while green residual stays inside band.  
- See also `docs/T3_T4_GR_SM_DEEPENING.md`.
