# MPCORB diversity pack (storage-capped)

*Generated 2026-08-07T00:10:11.033522+00:00*

## Secular sky drift (what we refuse)

Wrong method: treat residual scale on mean motion as a constant rate error and multiply by observation span in years so predicted sky position drifts (fake arcsec blow-up). FSOT does not do this. Time is dimensional fold ln(D/25) / chaos (D-25)/25 + Fluid Phase Current; residual matching is at D_eff.

## Storage

- Path: `G:/FSOT-PublicData/anomaly_observables/mpcorb_diversity_pack`
- Used: **0.24 MB** / budget 80.0 MB
- Within budget: True

## Sample sizes

| Cell | n |
|------|--:|
| neo | 35 |
| distant | 35 |
| outer_belt | 35 |
| high_u | 25 |
| comet | 50 |

## FSOT residual (model law)

- Objects: **180**
- Pooled median: **0.026472323952538984%**
- Over 0.5% gate: **0**
- all_pass: **True**

| Regime | n | median residual % |
|--------|--:|------------------:|
| comet | 50 | 0.029099821250810898 |
| distant | 35 | 0.026472323952539817 |
| high_u | 25 | 0.026472323952541045 |
| neo | 35 | 0.02301537415623265 |
| outer_belt | 35 | 0.02246148920415081 |

## Domain routing

- **neo** → Planetary_Science D=21
- **main_belt / high_u** → Planetary_Science D=21
- **outer_belt** → Astronomy D=20
- **distant** → Astrophysics D=24
- **comet** → Meteorology D=16 (chaos/T3)

## Not in this pack

- Major planets
- Moons
- Stars / exoplanets
- Full 1.55M MPCORB optical history

```powershell
python scripts/run_mpcorb_diversity_pack.py --budget-mb 100 --per-cell 35
python scripts/run_mpcorb_diversity_pack.py --skip-optical   # elements only, tiny disk
```
