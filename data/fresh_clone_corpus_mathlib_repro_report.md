# Clean-clone reproducibility report — Mathlib stamp on GitHub tip

- **When:** 2026-09-09T16:53:43.136189+00:00
- **Repo:** https://github.com/dappalumbo91/FSOT-2.1-Lean.git
- **Commit:** `e23a2c73461ffdf8e2c9dddf7b8b02d969fc8137`
- **Clone dir:** `C:\Users\damia\Desktop\FSOT-2.1-Lean-clean-repro-20260909`
- **Working tree:** `C:\Users\damia\Desktop\FSOT-2.1-Lean`
- **Overall:** **PASS**

## Bootstrap (independent machine path)

1. `git clone --depth 1 https://github.com/dappalumbo91/FSOT-2.1-Lean.git`
2. `pip install -r requirements.txt`
3. `lake exe cache get`
4. `lake build FSOT`
5. `python scripts/run_mathlib_rederivation_campaign.py`
6. `python scripts/run_formula_authority_closure.py`
7. `python scripts/audit_parameter_count.py`
8. `python scripts/audit_all_benchmark_margins.py`

## Side-by-side (working tip vs clean clone re-run)

| Check | Working tree | Clean clone | Match |
|------:|:------------:|:-----------:|:-----:|
| commit | `e23a2c7` | `e23a2c73461f` | yes |
| mathlib_verdict | `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED` | `FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED` | yes |
| engine_mathlib_pct | `100.0` | `100.0` | yes |
| corpus_mathlib_pct | `100.0` | `100.0` | yes |
| theorem_count | `5229` | `5229` | yes |
| mathlib_depth_count | `5229` | `5229` | yes |
| corpus_l1 | `0` | `0` | yes |
| formula_authority_verdict | `FORMULA_AUTHORITY_SYSTEM_CLOSED` | `FORMULA_AUTHORITY_SYSTEM_CLOSED` | yes |
| green_pass | `477` | `477` | yes |
| green_fail | `0` | `0` | yes |

Prior stamp on `56f6526` was PASS at corpus 69.32% (bare `norm_num` L1 in generated spines). This tip upgrades those generators to term-mode L3. Same statements. No residual retune.
