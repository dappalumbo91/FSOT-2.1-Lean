# Clean-clone reproducibility report — full corpus Mathlib close

- **When:** 2026-08-05T22:53:07.715460+00:00
- **Repo:** https://github.com/dappalumbo91/FSOT-2.1-Lean.git
- **Commit:** `059f212fd26443d581f338868cbdde4eb326700b`
- **Clone dir:** `C:\Users\damia\Desktop\FSOT-2.1-Lean-clean-repro`
- **Working tree:** `C:\Users\damia\Desktop\FSOT-2.1-Lean`
- **Overall:** **PASS**

## Bootstrap (independent machine path)

1. `git clone --depth 1 https://github.com/dappalumbo91/FSOT-2.1-Lean.git`
2. `pip install -r requirements.txt`
3. `lake exe cache get`  (Mathlib OLEANS; ~8.5k files)
4. `lake build FSOT`
5. `python scripts/run_mathlib_rederivation_campaign.py`
6. `python scripts/run_formula_authority_closure.py`
7. `python scripts/audit_parameter_count.py`
8. `python scripts/audit_all_benchmark_margins.py`

## Side-by-side (working tip vs clean clone re-run)

| Check | Working tree | Clean clone | Match |
|------:|:------------:|:-----------:|:-----:|
| commit | `059f212 (expected)` | `059f212fd264` | yes |
| authority_pin_prefix | `D1D38A` | `D1D38A` | yes |
| pin_match | `True` | `True` | yes |
| mathlib_verdict | `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED` | `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED` | yes |
| engine_mathlib_pct | `100.0` | `100.0` | yes |
| corpus_mathlib_pct | `100.0` | `100.0` | yes |
| engine_l1 | `0` | `0` | yes |
| corpus_l1 | `0` | `0` | yes |
| theorem_count | `5182` | `5182` | yes |
| mathlib_depth_count | `5182` | `5182` | yes |
| by_tier | `{'L0_definitional': 1905, 'L3_chain': 2997, 'L2_analytic': 280}` | `{'L0_definitional': 1905, 'L3_chain': 2997, 'L2_analytic': 280}` | yes |
| formula_authority_verdict | `FORMULA_AUTHORITY_SYSTEM_CLOSED` | `FORMULA_AUTHORITY_SYSTEM_CLOSED` | yes |
| formula_authority_all_ok | `True` | `True` | yes |
| parameter_verdict | `ZERO_FREE — seed-derived constants and preregistered domain routes` | `ZERO_FREE — seed-derived constants and preregistered domain routes` | yes |
| green_pass | `472` | `472` | yes |
| green_fail | `0` | `0` | yes |
| benchmark_files | `472` | `472` | yes |

## Clean-clone gate results

| Gate | Result |
|------|--------|
| Authority pin D1D38A | match (`D1D38A185487B452…`) |
| lake build FSOT | passed (2205 jobs) |
| Mathlib campaign | `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED` engine 100% corpus 100% L1=0 |
| Formula authority | `FORMULA_AUTHORITY_SYSTEM_CLOSED` all_ok=true |
| Parameter audit | ZERO_FREE |
| Benchmark green gate | 472/472 fail=0 |

## Interpretation

Fresh clone of GitHub `main` at the corpus-Mathlib-close commit reproduces the same
depth inventory, campaign verdict, formula-authority system closed state, ZERO_FREE
parameter discipline, and residual green gate as the author working tree. No local
uncommitted patches were required.

## Mismatches

None — all compared fields equal.
