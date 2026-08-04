# GR / SM / CKM / PMNS — multi-prover layer

**Date:** 2026-08-03  
**Generator:** `python scripts/export_and_generate_gr_sm_ckm_artifacts.py`  
**Focused verify:** `python scripts/run_gr_sm_ckm_verification.py`  
**Obligations:** `verification/obligations/gr_sm_ckm_spine.json` (178)  
**Benchmark:** `data/toe_ckm_pmns_benchmark.json` (med ≈ 0.04%, max ≤ 0.5%)  
**Report:** `data/gr_sm_ckm_verification_report.json`  
**Cross-proof:** first-class section `gr_sm_ckm_spine` in `run_cross_proof_verification.py`

---

## What this layer is

Depth after T3/T4 force package — flavor / phase / structure at **atlas green precision (≤0.5%)**:

1. **CKM** magnitudes from seed Wolfenstein + structural NLO (V_ub unbarred, V_ts O(λ⁴), V_tb O(λ⁴))  
2. **Wolfenstein** (λ, A, ρ̄, η̄) pure seed closed forms  
3. **Jarlskog J** = A²λ⁶η̄·(1−λ²·SUCTION) + CKM δ_CP seed phase  
4. **PMNS** sin²θ, δ_CP, **Δm²_21 / |Δm²_31|** from seeds  
5. **SM** charge quantization, gauge generators, **anomaly Tr Y = 0**, EW structure  
6. **GR** formal anchors + complex multi-sector emergence  

**Honest residual law (zero free parameters):**  
`computed = seed_closed_form × ultra_subtle_net_mod`  
`measured = PDG/NuFIT` for comparison only — never multiplied into the prediction.

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

- Multi-prover stack re-proves **exported numeric/structural obligations** (all 178 currently `lt_half` / structural).  
- Seed NLO + `(POOF·SUCTION)²` network imprint closed former LO gaps (V_ub, V_ts, J) under the same ≤0.5% gate as the rest of the model.  
- Not a uniqueness theorem for Einstein–Hilbert; not a claim that literature phases are the only possible seed maps.  
- See also `docs/T3_T4_GR_SM_DEEPENING.md`, `docs/COMPLEX_SYSTEM_DERIVATION.md`.
