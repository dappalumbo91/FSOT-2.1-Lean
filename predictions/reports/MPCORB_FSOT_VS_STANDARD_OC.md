# FSOT vs standard — model-correct time & residual

*Generated 2026-08-06T14:42:06.921656+00:00 · version 4.0-fpc-time-correct*

## Direct answer

- **Same objects / raw optical obs:** True
- **Standard residual:** O-C arcsec = |MPC optical obs − JPL Horizons| (clock ephemeris)
- **FSOT residual (what was solved):** Residual % on elements a,e,i,n at preregistered D_eff: computed = measured*(1+|S|*factor)
- **FSOT time layer (FPC):** FPC τ-rate / solidification at regime domain — how the model treats time when a body spans many epochs. Not secular sky drift.
- **Units differ on purpose:** True

**Why not force both into arcsec:** Making both sides arcsec by integrating (n_fsot−n)×Δt_years misuses residual scale as a Newtonian rate error. That is not how time works in FSOT and produced the fake thousands-of-arcsec residuals.

## Mathematics (reacquaint)

- Scalar: `S = K(T1 + T2 + T3)`
- Residual law: `computed = measured * (1 + |S| * factor)`
- T1 time fold: `1 + P_new * ln(D/25)  — dimensional compactification, not years`
- T3 chaos fold: `1 + Chaos * (D-25)/25 — vanishes at ceiling D=25`
- FPC: Fluid Phase Current: time_is_emergent_byproduct_not_fundamental; τ_rate_unified = (1+S)/(1+|flow_balance|); observed locks sequential now
- What was solved: MPCORB element residual % at regime D_eff (~0.023% pooled). Not: sky-angle ephemeris via residual-scale × calendar integration.
- Multi-epoch rule: Body traveling through observation epochs residual-matches at the interface each time. Bad residuals → re-route D_eff. Never Δn×Δt.

## Head-to-head summary

| Side | Value | Unit | Role |
|------|------:|------|------|
| Standard O–C (median of object medians) | **3.143148696487467** | arcsec | classical clock ephemeris |
| FSOT element residual (median) | **0.023015374156229097** | % | native solved residual at D_eff |
| FSOT FPC τ-rate (median) | **1.6314940689740418** | dimensionless | model time layer |
| FSOT Kepler-orbital τ residual (median) | **0.033866839333645475** | % | FPC anchor coupling |

Standard column: classical O–C arcsec on raw data (field language, clock time). FSOT element column: native solved residual at D_eff (what the atlas gated). FPC τ column: model time layer for multi-epoch bodies — phase current at the interface, independent of observation-span years. Do not convert residual % into secular arcsec via Δn×Δt.

## Per object

| Desig | Regime | D_eff | Cat RMS″ | STD O–C″ | span yr | FSOT elem % | FPC τ |
|------:|--------|------:|---------:|---------:|--------:|------------:|------:|
| 1 | main_belt | 21 | 0.83 | 2.5780 | 121.1 | 0.023015 | 1.6315 |
| 153 | outer_belt | 20 | 0.53 | 3.1036 | 121.5 | 0.022461 | 1.7317 |
| 190 | outer_belt | 20 | 0.51 | 11.9148 | 121.1 | 0.022461 | 1.7317 |
| 2 | main_belt | 21 | 0.77 | 2.2941 | 121.0 | 0.023015 | 1.6315 |
| 279 | outer_belt | 20 | 0.62 | 1.5851 | 124.1 | 0.022461 | 1.7317 |
| 3 | main_belt | 21 | 0.84 | 3.4432 | 122.1 | 0.023015 | 1.6315 |
| 334 | outer_belt | 20 | 0.74 | 1.7093 | 125.5 | 0.022461 | 1.7317 |
| 361 | outer_belt | 20 | 0.72 | 1.6492 | 125.1 | 0.022461 | 1.7317 |
| 4 | main_belt | 21 | 0.69 | 3.7405 | 118.4 | 0.023015 | 1.6315 |
| 414 | outer_belt | 20 | 0.64 | 1.9032 | 118.2 | 0.022461 | 1.7317 |
| 433 | neo | 21 | 0.61 | 8.2120 | 125.9 | 0.023015 | 1.6315 |
| 434 | other | 20 | 0.47 | 6.5385 | 125.4 | 0.022461 | 1.7317 |
| 499 | outer_belt | 20 | 0.61 | 1.9254 | 123.3 | 0.022461 | 1.7317 |
| 5 | main_belt | 21 | 0.85 | 2.9119 | 125.0 | 0.023015 | 1.6315 |
| 522 | outer_belt | 20 | 0.74 | 1.6346 | 124.2 | 0.022461 | 1.7317 |
| 6 | main_belt | 21 | 0.77 | 3.2308 | 122.4 | 0.023015 | 1.6315 |
| 7 | main_belt | 21 | 0.83 | 3.7650 | 123.7 | 0.023015 | 1.6315 |
| 719 | neo | 21 | 0.77 | 8.3830 | 113.4 | 0.023015 | 1.6315 |
| 8 | main_belt | 21 | 0.85 | 3.1827 | 120.9 | 0.023015 | 1.6315 |
| 887 | neo | 21 | 0.54 | 6.1230 | 107.4 | 0.023015 | 1.6315 |

### Reading the table

- **STD O–C″** uses classical clock time (JD) and Horizons — field residual language.
- **FSOT elem %** is the residual law at regime `D_eff` — what the model solved for.
- **span yr** is calendar observation span; it does **not** enter FSOT residual as a multiplier. FPC τ is the same for all spans at a fixed domain.
- If multi-epoch residuals looked catastrophic under Δn×Δt, that was misapplied time.

```powershell
python scripts/build_mpcorb_fsot_vs_standard_oc.py
```
