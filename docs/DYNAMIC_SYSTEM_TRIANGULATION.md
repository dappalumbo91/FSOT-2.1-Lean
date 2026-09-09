# Dynamic-system triangulation — fold, tanks, frozen potentials

*Generated 2026-09-09T19:42:56.656676+00:00 · pin D1D38A*

Matching known tables is already green. Dated misses were **wrong fold**,
not a broken kernel. Normalize the prediction to the area you are scoring,
then emit the tanks that talk at the unfolded valve. That is the n-body
analog: **25 compactified tanks coupled by κ**, not Newton's gravity N-body.

**Refresh:** `python scripts/build_dynamic_system_triangulation.py`

Lean: `orifice_scale` · `kernel_km_eq_orifice_scale_one` ·
`cycle_km_eq_orifice_scale_ceiling` in `FSOT/Formal/ScalarEngineStructure.lean`.
Law **D11**. Picture **C14**.

## Closed form

\[
\mathrm{orifice\_scale}(L,d)=L\cdot\mathrm{POOF}\cdot d/25
\]

| Fold | Object | km | Job |
|-----:|--------|---:|-----|
| 1 | dated cell (score / kill_if) | **39.1** | one compactified slice |
| 25 | planetary cycle (coupled tanks) | **977.8** | arc / trench / basin / solar |

Identity: cycle / cell = **25.000000** (must be 25).
Invert: \(d = 25\cdot L_\mathrm{orifice}/(L_\mathrm{body}\cdot\mathrm{POOF})\).
Solar Kp is issued on the body — that is the planetary tank, not an orifice length.

## How to normalize to the area you are predicting

1. Name the **score object** (cell, buoy, gage, Kp). That radius is `kill_if`.
2. Recover its fold \(d_\mathrm{score}=25\cdot r/(R_\oplus\cdot\mathrm{POOF})\).
3. Coupled tanks always talk at \(d=25\). If \(d_\mathrm{score}\ll 25\), the load can dump next door.
4. κ_ij says **which** tanks can take it. Dark folds still couple; silos are institutional.
5. Frozen `valve_state` splits into discrete **potentials**. Weights are
   POOF/(POOF+SUCTION)=**0.5107** fire and
   SUCTION/(POOF+SUCTION)=**0.4893** hold, then split across tanks by κ.
   That is valve geometry, **not** a calibrated event probability.

Do not retune the 39 km kernel to swallow a 978 km dump. Record the transfer.

## Where tanks interact

| Kind | Core fold | Strongest other tank (κ) |
|------|-----------|--------------------------|
| earthquake | Seismology | solar (0.04908079) |
| volcanic | Geophysics | solar (0.0626778) |
| weather | Meteorology | solar (0.04982513) |
| solar | Planetary_Science | volcanic (0.0626778) |
| tide | Oceanography | solar (0.04008272) |
| hydrology | Fluid_Dynamics | solar (0.05594637) |

Self-κ is always the largest (ΔD=0). Interaction is the off-diagonal.
A tank that does not take the dump is not a failed planet — the attractor
was the coupled tank. Same dampening grammar as uniqueness (free color is
not an attractor). Uniqueness of continuum YM stays `OPEN_NOT_CLAIMED`.

## Frozen-state potentials (the branches)

| Valve at issue | Live branches |
|----------------|---------------|
| `loading_suction` | cell_poof · transferred_poof · quiet_hold |
| `post_poof_aftershock` | quiet_hold · omori_aftershock · transferred_poof. **Not** a new mainshock. |
| `released` / `steady` | quiet_hold · unexpected_poof · transferred_poof |

New issues carry these on `predicted.potentials`. Issued JSON is not rewritten.

## Closed kills → which branch fired

Diagnosis already named the why. This table is the same why as a **scored branch**.

| Branch | Closed kills |
|--------|-------------:|
| `transferred_poof` | 18 |
| `quiet_hold` | 6 |
| `cell_poof` | 2 |
| `unexpected_poof` | 2 |

Closed kills with a mapped diagnosis: **29**. Still-open / awaiting (forward potentials): **30**.
2026-09-09 stays frozen; score after `valid_to`. These rows are the live
potentials from that freeze, not a rewrite.

## Forward sample (open windows)

| ID | Kind | Valve | Hold | Fire here | Transfer |
|----|------|-------|-----:|----------:|---------:|
| `FCAST-WX-20260825T0121-04` | weather | steady | 0.489 | 0.085 | 0.426 |
| `FCAST-WX-20260825T0222-02` | weather | loading_suction | 0.489 | 0.085 | 0.426 |
| `FCAST-WX-20260825T0222-04` | weather | steady | 0.489 | 0.085 | 0.426 |
| `FCAST-WX-20260901T0032-05` | weather | steady | 0.489 | 0.085 | 0.426 |
| `FCAST-EQ-20260909T1854-01` | earthquake | released | 0.489 | 0.077 | 0.434 |
| `FCAST-EQ-20260909T1854-02` | earthquake | released | 0.489 | 0.077 | 0.434 |
| `FCAST-EQ-20260909T1854-03` | earthquake | steady | 0.489 | 0.077 | 0.434 |
| `FCAST-EQ-20260909T1854-04` | earthquake | steady | 0.489 | 0.077 | 0.434 |
| `FCAST-EQ-20260909T1854-05` | earthquake | steady | 0.489 | 0.077 | 0.434 |
| `FCAST-EQ-20260909T1854-06` | earthquake | steady | 0.489 | 0.077 | 0.434 |
| `FCAST-EQ-20260909T1854-07` | earthquake | released | 0.489 | 0.077 | 0.434 |
| `FCAST-EQ-20260909T1854-08` | earthquake | released | 0.489 | 0.077 | 0.434 |

## What this is not

- A fitted 150 km or 1000 km spring.
- A calibrated probability of the next earthquake.
- Many-worlds / a second H0.
- Rewriting `kill_if` onto `cycle_km`.
- Clock-time hypocenter. S2S vs ECMWF. Prices. Diagnoses.

Related: [`PLANETARY_CYCLE_CONNECTIVE.md`](PLANETARY_CYCLE_CONNECTIVE.md) ·
[`CONCEPTS.md`](CONCEPTS.md) C14 · [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md) D11 ·
[`UNIQUENESS_RESEARCH_SPINE.md`](UNIQUENESS_RESEARCH_SPINE.md).
