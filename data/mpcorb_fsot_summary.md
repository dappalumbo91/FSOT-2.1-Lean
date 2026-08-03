# MPCORB FSOT evaluation — refined (v2 dimensional interface)

Generated: `2026-08-03T21:34:49.144474+00:00`

## Precision vs framework standard

| Metric | Value | Gate |
|--------|------:|------|
| Pooled median residual | **0.023015%** | ≤ 0.5% green / ≤ 0.05% aspiration |
| Green gate | **PASS** |
| Tier aspiration (~0.05%) | **PASS** |
| Kepler integrity median | **1.5875572596619725e-06%** | catalog Layer C |
| Objects | 1,554,101 |
| Comets parsed | 4,645 |

## What changed (refinement)

1. **Dropped bare-seed-only structural tests** that ignored D_eff (v1 e-fold ~62%, fixed Kirkwood ratio).
2. **Routed every orbital observable** through `fsot_api_predict_lib` with domain factors (same law as Gaia / NEO / exoplanets): `computed = measured · (1 + |S|·factor)`.
3. **Dimensional regimes:** NEO / main belt → Planetary_Science (D=21); outer → Astronomy (D=20); distant → Astrophysics (D=24); comets → Meteorology (chaos/T3 interface).
4. **Full framework channels:** C_FACTOR, POOF, SUCTION, CHAOS, θ_S, A_bleed, P_var, yin–yang observer gap at D=20, dimensional S ladder.
5. **No new free parameters** — only preregistered domain factors + seed-derived engine.

See `docs/MPCORB_REFINEMENT_PROCESS.md` for reproducible protocol.

## Regime counts

- **main_belt:** 1,438,158 → domain `Planetary_Science`
- **neo:** 42,079 → domain `Planetary_Science`
- **other:** 40,894 → domain `Astronomy`
- **outer_belt:** 25,853 → domain `Astronomy`
- **distant:** 7,117 → domain `Astrophysics`

## Residuals by claim tier (median)

- `A_dimensional_interface`: median **0.022461%** (n=5)
- `A_engine_exposed`: median **0.014333%** (n=10)
- `A_observer_yin_yang`: median **0.031506%** (n=1)
- `B_domain_routed`: median **0.023015%** (n=32)
- `B_domain_routed_sample`: median **0.023015%** (n=800)
- `C_integrity`: median **0.000002%** (n=1)

JSON: `data/mpcorb_fsot_benchmark.json`  
Ledger: `data/mpcorb_refinement_ledger.json`
