# Fresh-clone repro report

- **When:** 2026-08-03 (local)
- **Repo:** https://github.com/dappalumbo91/FSOT-2.1-Lean.git
- **Commit:** ebc7264e41e0bbd51e0db7722c8d0d83c7f25332
- **OutDir:** %TEMP%\fsot_fresh_clone_g5
- **Gate:** **PASS** (after fail_count==0 fix)

## Results from clean clone
| Check | Result |
|-------|--------|
| Green gate | 412/412 fail=0 |
| Tier scalar closed | true |
| Label A | true |
| Label B | true |
| Cross overall_ok | true |

## Commands
1. git clone --depth 1
2. pip install -r requirements.txt
3. python scripts/audit_all_benchmark_margins.py
4. python scripts/build_tier_scalar_precision_closure.py
5. python scripts/build_toe_gap_closure.py

Note: first gate script treated `fail_count=0` as missing due to Python falsy `or`; fixed in `scripts/fresh_clone_repro.ps1`.
