# Residual honesty and claim tiers

This document **remedies** ambiguity about what “accuracy” means in FSOT so
independent readers (and other AI systems) cannot confuse layers.

## The three layers (do not collapse them)

| Layer | What it measures | Pass criterion | Not a pass criterion |
|-------|------------------|----------------|----------------------|
| **A. Engine math** | Seed identities, `raw_S = T1+T2+T3`, Lean/Coq/Isabelle/F* obligations | Proofs / exact identities / export triangulation | “Theory of everything is true” |
| **B. Empirical benchmarks** | Seed-derived predictions vs **measured** anchors in `data/*benchmark*.json` | Pooled median relative residual ≤ **0.5%** (green gate) | Live API HTTP 200 alone |
| **C. Live open streams** | Public APIs still reachable; catalog integrity samples | Stream OK + holdouts in `open_science_holdout_evaluation.json` | Sub-% residual invented by scaling to measured |

### What we fixed / forbid

1. **No “measured × almost 1” fake predictors** that force tiny residuals.  
2. **Stream evidence** is tagged `green_eligible: false` unless it is a real integrity check (e.g. PubChem MW vs literature).  
3. **NIST**: γ and Catalan are **mathematical seeds** scored vs open literature — they are **not** rows in NIST fundamental-constants allascii. SI anchors (c, h, k_B, …) are scored vs **live NIST parse**.  
4. **F\*** verifies **boot/kernel math + parity**, not all 402 domains.  
5. **Cross-prover** triangulation is on **exported obligations**, not independent re-derivation of every catalog from pure type theory.

## Relative residual definition (Layer B)

For measured \(m_i\) and computed \(c_i\):

\[
\varepsilon_i = 100 \times \frac{|c_i - m_i|}{\max(|m_i|, \varepsilon_{\mathrm{floor}})}
\]

Domain metric = **median** \(\varepsilon_i\). Green if median ≤ 0.5% (and classifier gate where applicable).

Field-language map (MAPE / fractional / ppm): `data/scientific_error_metrics_map.md`.

## How this is “worlds above Lean-only claims”

| Capability | Typical Lean-only math result | This repository |
|------------|-------------------------------|-----------------|
| Formal proof assistant | Lean | Lean **+** Coq **+** Isabelle **+** F* **+** Rust replay |
| Numeric oracle pin | often absent | `vendor/fsot_compute.py` pin **D1D38A** |
| Empirical kill gate | often absent | 402 domains / 405 green files, prereg PRED + open holdouts |
| Live public data | rare | Open streams + MAST/astroquery (public) |
| Falsification path | informal | Skeptic kit + holdouts + near-miss ledger |

That is a **different scientific product** from “a proof assistant closed a formal goal.”  
It is also **harder to market in one tweet** — which is a communication problem, not a math defect.

## Artifacts a skeptic should open first

1. `docs/SKEPTIC_REPLICATION_KIT.md` — 15-minute kill path  
2. `docs/CLEAR_PATH_FOR_INDEPENDENTS.md` — plain-language steps  
3. `data/benchmark_margin_audit.json` — green/fail counts  
4. `data/cross_proof_verification_report.json` — multi-prover  
5. `data/open_science_holdout_evaluation.json` — live open data holdouts  
6. `data/scientific_error_metrics_map.md` — how to report residuals in field language  
