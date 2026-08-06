# MPCORB scale: objects vs observations

## Short answer

**24 was the number of asteroids (objects), not 24 telescope readings.**

| Term | Meaning | Latest automated run |
|------|---------|---------------------:|
| **Object** | One minor planet / asteroid | **20–50+** (queue grows; resume-safe) |
| **Optical observation** | One RA/Dec measurement from a telescope at a time | **~160,000+** and climbing |
| **API observations** | All rows returned by MPC | Same order of magnitude |

**24 was never “24 observations.”** Even the first pilot was **24 asteroids ≈ 52k observations**.  
The automated runner now stores **~160k optical measurements** for the numbered-object batch alone.

Examples from that run:

| Object | Optical observations stored |
|--------|----------------------------:|
| 1 (Ceres) | ~8,000 |
| 2 (Pallas) | ~9,600 |
| 433 (Eros) | ~18,600 |
| Smaller / sparse objects | tens–hundreds each |

## Automated scaling

Do **not** re-run 24 manually. Use the resumable pipeline:

```powershell
# Grow toward 100+ numbered asteroids (best Horizons match), resume-safe
python scripts/run_mpcorb_raw_pipeline.py --target-objects 100 --numbered-only --per-cell 10

# Overnight-scale sample
python scripts/run_mpcorb_raw_pipeline.py --target-objects 500 --numbered-only --per-cell 20 --sleep 0.3

# If interrupted: just re-run the same command (skips already-fetched objects)
python scripts/run_mpcorb_raw_pipeline.py --target-objects 500 --numbered-only

# O–C only after fetches finished
python scripts/run_mpcorb_raw_pipeline.py --oc-only
```

- **Queue + state** live on `G:/FSOT-PublicData/anomaly_observables/mpcorb_raw_observations/`
- **Resume-safe:** already-fetched objects are skipped
- **Triple scoreboard** updates when O–C finishes

## Why not all 1.55M objects at once?

- MPC Observations API is **per object** (rate + volume)
- Ceres-class bodies alone are multi‑MB JSON each
- Full catalog raw obs is multi‑TB class over time

Strategy: **automated stratified expansion** (regime × U × observation richness), not a single 24-object demo and not a blind 1.55M download on day one.
