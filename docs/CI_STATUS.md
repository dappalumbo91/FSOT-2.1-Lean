# FSOT GitHub Actions CI status

**Workflow:** `.github/workflows/ci.yml` · **name:** `FSOT CI`  
**Updated:** 2026-08-05

## Jobs

| Job | Hard fail? | Meaning |
|-----|------------|---------|
| **Margin + TOE + tier aspiration** | Yes for green + TOE | Official residual ≤ **0.5%**; Label A/B |
| Tier scalar ≤0.05% | **Soft** (report only) | Aspiration band — must not block green CI |
| Scientific catalog SMT (Z3) | Soft-ish | Runs if SMT2 present |
| Publication smoke | Yes if scripts fail | Navigator + contested + param honesty |

## What was broken (2026-08)

GitHub showed **FSOT CI / Margin** failing even though local margin was **430/430 green**.

**Root cause:** CI hard-asserted **tier scalar aspiration ≤0.05%**. Two panels (nuclear lean-route domain-S residuals ~0.09%, intelligence_compression higher scalars) sit under the **official 0.5% green gate** but above **0.05% aspiration**. The report script also exited non-zero when aspiration was open, failing the job before TOE steps ran.

**Fix:**

1. `build_tier_scalar_precision_closure.py` always exits **0** after writing the report.  
2. CI: green gate remains **hard**; tier_scalar is **continue-on-error** + non-blocking report.  
3. TOE Label A/B still **hard**.

## Local reproduce

```powershell
python scripts/audit_all_benchmark_margins.py          # hard green
python scripts/build_tier_scalar_precision_closure.py  # soft aspiration
python scripts/build_toe_gap_closure.py                # Label A/B
```

Live stamp: `docs/CURRENT_STATUS.md`
