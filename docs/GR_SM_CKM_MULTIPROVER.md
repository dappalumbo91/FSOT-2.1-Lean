# GR / SM / CKM / PMNS — multi-prover layer

**Date:** 2026-08-03  
**Generator:** `python scripts/export_and_generate_gr_sm_ckm_artifacts.py`  
**Obligations:** `verification/obligations/gr_sm_ckm_spine.json` (~181)  
**Benchmark:** `data/toe_ckm_pmns_benchmark.json`

---

## What this layer is

Next technical depth after T3/T4 force package v1:

1. **CKM** quark-mixing magnitudes (PDG) + **row/column unitarity**  
2. **PMNS** neutrino angles / sin²θ + hierarchy structure  
3. **GR** formal anchors (weak-field identity, light deflection residual, perihelion residual)  
4. **SM** charge quantization + gauge generator integers  

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
python scripts/export_and_generate_gr_sm_ckm_artifacts.py
cargo test --manifest-path verification/rust/fsot_gr_sm_ckm_replay/Cargo.toml
# optional:
# z3 verification/smt/gr_sm_ckm_bounds.smt2
# coqc -Q verification/coq "" verification/coq/GRSMCKMSpine.v
python scripts/build_toe_gap_closure.py
python scripts/audit_all_benchmark_margins.py
```

## Honesty

- Multi-prover stack re-proves **exported numeric/structural obligations**, not a uniqueness theorem for the full CKM complex phase or Einstein–Hilbert measure.  
- Complex CKM phases / full seed-only matrix derivation remain open research.  
- See also `docs/T3_T4_GR_SM_DEEPENING.md`.
