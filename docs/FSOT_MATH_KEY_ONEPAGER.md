# FSOT Mathematical Key — one page (scientists)

**Fluid Spacetime Omni-Theory** · pin **D1D38A** (match=True) · 2026-08-05  
Full key: `docs/FSOT_MATH_KEY.md` · Live status: `docs/CURRENT_STATUS.md` · Map: `docs/DOCUMENTATION_MAP.md`  
Repo: https://github.com/dappalumbo91/FSOT-2.1-Lean

## Unified principle

One seed-derived scalar engine — **zero free parameters** — evaluated at preregistered dimensional interfaces \(D_{\mathrm{eff}}\).  
Every domain uses the **same** prediction law; mismatches mean wrong interface, not a new fit coefficient.

**Seeds:** \(\pi,\ e,\ \varphi,\ \gamma,\ G\) (Catalan)

**Scalar:** \(S = K\cdot(T_1 + T_2 + T_3)\)  
\(T_1\) observer-modulated base (includes **consciousness factor** \(C_{\mathrm{factor}}\) when `observed`) · \(T_2\) linear · \(T_3\) valve–acoustic–phase (**Poof**, Suction, Chaos, bleed)

**Prediction law (all domains):**

```
computed = measured × (1 + |S(domain)| × factor)
```

`S(domain)` = full `compute_scalar` at that domain’s \(D_{\mathrm{eff}}\), hits, \(\delta\psi\), observer flag.  
Factors: `scripts/fsot_api_predict_lib.py`. Engine: `vendor/fsot_compute.py`.

## How to use the math in any domain

| Step | Action |
|------|--------|
| 1 | Name measured \(m\) (public/lab provenance) |
| 2 | Pick **domain / \(D_{\mathrm{eff}}\)** (micro → meso → geo → astro ladder) |
| 3 | `S = domain_scalar(name)` |
| 4 | `computed, err% = fsot_scaled(m, name)` |
| 5 | Green if domain **median** residual ≤ **0.5%** (aspiration ≤ **0.05%**) |
| 6 | Optional: export gate → Lean / Coq / Isabelle / SMT |

**Mismatch rule:** first check dimensional interface (e.g. NEO vs belt vs distant), then observer / \(C_{\mathrm{factor}}\) / Poof — never add free parameters.

## Snapshot (regenerated — prefer CURRENT_STATUS if conflict)

| Quantity | Value |
|----------|------:|
| Pin | D1D38A (match=True) |
| Atlas domains | 403 |
| Green benchmarks | 430/432 |
| Scalar-record envelope | 61,445 (envelope) |
| MPCORB objects · residual | 1,554,101 · 0.023% |
| Scientific catalog obligations | 2040 |
| π/e inventory decimal-verified | 68/68 |
| Multiprover overall_ok | True |

## Verification stack (not decoration)

Lean 4 (master) · Coq (Interval-native π/e) · Isabelle · F* · Rust replay · SMT (Z3/CVC5) · TLA+ routing · hardware/QEMU  
Layers: **A** engine math · **B** empirical residuals · **C** streams/catalog integrity  

Honesty: multi-prover locks **exported residual gates**; Python/data own measurements.  
Reproduce: `docs/REPRODUCIBILITY.md` · Kill path: `python scripts/run_publication_verification_bundle.py`

---
*Not a second theory — the same key applied at every domain fold. PhD scope notes: FSOT_MATH_KEY.md §14.*
