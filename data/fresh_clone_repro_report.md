# Fresh-clone repro report

- **When:** 2026-08-03T19:27:52.8478617-04:00
- **Repo:** https://github.com/dappalumbo91/FSOT-2.1-Lean.git
- **Commit:** 63542b26537d9b4e73564e34507aefa4cd2e004a
- **OutDir:** C:\Users\damia\AppData\Local\Temp\fsot_fresh_clone_g5b
- **Gate exit:** 0

## Commands run
1. `git clone --depth 1`
2. `pip install -r requirements.txt`
3. `python scripts/audit_all_benchmark_margins.py`
4. `python scripts/build_tier_scalar_precision_closure.py`
5. `python scripts/build_toe_gap_closure.py`
6. publication bundle skipped

## Result
**PASS** — green gate, tier aspiration, Label A + Label B.
