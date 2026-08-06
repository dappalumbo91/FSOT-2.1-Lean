# MPCORB scale: objects vs observations

## Short answer

**Object count ≠ observation count.** We expand **asteroids**; each can carry thousands of optical measurements.

| Term | Meaning | Latest throttled expansion |
|------|---------|---------------------------:|
| **Object** | One minor planet / asteroid | **45** fetched OK · queue **62** |
| **Optical observation** | One RA/Dec from a telescope | **240,415** stored |
| **FSOT residual (model law)** | `computed = measured·(1+\|S\|·f)` at regime `D_eff` | **59/59 pass** · pooled **~0.023%** |
| **Standard O–C** | MPC optical vs JPL Horizons (clock ephemeris) | **35** objects · median **~3.44″** |

## Model-correct residual (do not regress)

- FSOT residual is the **atlas residual law** at preregistered `D_eff` — **not** secular `Δn × calendar years` sky drift.
- Time in the model is **dimensional folds** `ln(D/25)` / chaos `(D−25)/25` + **Fluid Phase Current** — not Newtonian clock accumulation.
- Multi-epoch rule: residual-match at the interface; bad residuals → re-route `D_eff`, never invent a rate×time integrator.
- Per-object verify: `python scripts/run_mpcorb_raw_pipeline.py --verify-only`  
  Full report: `G:/…/fsot_per_object_verify.json` · slim: `data/mpcorb_fsot_per_object_verify.json`

All checked objects currently sit in **~0.022–0.026%** element residual (framework gate **0.5%**).

## Automated scaling (rate-limit aware)

```powershell
# Throttled expansion (recommended until gates stay green)
python scripts/run_mpcorb_raw_pipeline.py `
  --target-objects 100 --numbered-only --per-cell 10 `
  --fetch-limit 25 --sleep 0.75 --skip-oc

# FSOT residual gate on every stored object (halts if any over 0.5%)
python scripts/run_mpcorb_raw_pipeline.py --verify-only

# Horizons O–C in small batches (resume-safe; does not re-score old objects)
python scripts/run_mpcorb_raw_pipeline.py --oc-only --oc-limit 15 --sleep 0.75

# Open throttle only after multi-batch all_pass (watch MPC + Horizons limits)
# python scripts/run_mpcorb_raw_pipeline.py --target-objects 500 --numbered-only --per-cell 20 --fetch-limit 50 --sleep 0.75
```

| Control | Purpose |
|---------|---------|
| `--fetch-limit N` | Cap new MPC API downloads this run |
| `--oc-limit N` | Cap **new** Horizons O–C scores this run |
| `--sleep S` | Pause between external calls (default **0.75 s**) |
| `--resume` (default) | Keep prior O–C scores — **do not re-burn Horizons** |
| `--skip-oc` | Fetch + FSOT verify only |
| `--verify-only` | Residual law gate only (no network) |

- **Queue + state + bulk obs** live on `G:/FSOT-PublicData/anomaly_observables/mpcorb_raw_observations/`
- **Repo** keeps indices, O–C summaries, and slim FSOT verify for GitHub

## Why not all 1.55M objects at once?

- MPC Observations API is **per object** (rate + volume)
- Horizons is **per epoch batch** (rate-limited; O–C is expensive)
- Ceres-class bodies alone are multi‑MB JSON each
- Full catalog raw obs is multi‑TB class over time

Strategy: **stratified expansion** (regime × U) + **model residual gate per object** + **batched external APIs**.  
Open the throttle only while `all_pass=True` on FSOT verify and API error rates stay clean.
