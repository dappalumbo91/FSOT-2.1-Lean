# Audit gauntlet — 2026-09-09

Living-tree verification after D9 perception + interconnect work. Pin **D1D38A**.

| Gate | Result |
|------|--------|
| Authority pin | **D1D38A** match |
| Parameters | **ZERO_FREE** |
| Green residual files | **477 / 477** fail 0 |
| Median-of-medians | 0.006625% |
| Scalar-record envelope | 181,477 |
| Lean 4 `lake build` | 2205 jobs, ok |
| Cross-proof `overall_ok` | **true** (seven-way + eight-way hardware) |
| Catalog spine | **2256** obligations / **477** domains; Z3 checked 2256 |
| Atomic / full formal | **2024** / **2587**; margin violations **0** |
| Label A / B | True / True |

Refresh: `python scripts/audit_all_benchmark_margins.py` then `python scripts/run_cross_proof_verification.py` then `python scripts/build_repo_status_snapshot.py`.

Live authority: [`docs/CURRENT_STATUS.md`](../docs/CURRENT_STATUS.md).
