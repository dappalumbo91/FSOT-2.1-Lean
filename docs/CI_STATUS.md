# CI status — why GitHub Actions shows failure

**Last checked:** 2026-08-03  
**Workflow:** `.github/workflows/ci.yml` (`FSOT CI`)  
**Example failed run:** https://github.com/dappalumbo91/FSOT-2.1-Lean/actions/runs/30862351006  

## Root cause (not the tests)

Every job on recent runs finished in **~2 seconds** with:

- **0 steps executed**
- **no runner assigned** (`runner_id: 0`)
- Annotation on each job:

> **The job was not started because your account is locked due to a billing issue.**

So GitHub never checked out the repo or ran Python. This is an **account billing lock**, not a green-gate / ToE / SMT failure.

### What to fix on GitHub (account owner)

1. Open https://github.com/settings/billing  
2. Clear any failed payment / spending limit / Actions minutes lock  
3. Confirm Actions enabled: repo → **Settings → Actions → General → Allow all actions**  
4. Re-run a workflow: Actions → FSOT CI → **Re-run all jobs**, or push a no-op commit  

Until that is fixed, **every** Actions run on this account will fail the same way.

## Local verification (authoritative until billing is unlocked)

The CI script content **does** pass on a clean machine / local workspace:

```powershell
pwsh scripts/run_ci_local.ps1
# or lean gates only:
pwsh scripts/fresh_clone_repro.ps1 -SkipBundle
```

Expected:

| Gate | Expected |
|------|----------|
| Green | 412/412 fail 0 |
| Tier scalar | `closed: true` |
| Label A | true |
| Label B | true |

## Workflow design notes

- Three parallel jobs: margin+ToE, SMT catalog, publication smoke  
- Assert steps fail the job if green fails or labels drop  
- When billing is fixed, the first real run will exercise checkout + `pip install` + scripts on `ubuntu-latest`  

## History of “failed” runs (billing lock)

| Run | Commit | Duration | Real cause |
|-----|--------|----------|------------|
| #1 ebc7264 | Close publish/repro gaps… | ~2s | Billing lock |
| #2 63542b2 | Fix fresh-clone gate… | ~2s | Billing lock |
| #3 de5f8bc | Record clean-clone PASS… | ~2s | Billing lock |
