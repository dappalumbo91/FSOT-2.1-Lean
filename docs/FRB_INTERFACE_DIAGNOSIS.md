# FRB DM excess — retired formula autopsy

*Generated 2026-09-08T00:37:17.044322+00:00 · pin D1D38A*

**Verdict: `REMEDIED_WRONG_APPLY`.** The formula
`200·(1+local_sky_density)` on DM excess is **retired**. Median error
on 10 rows with excess was **66.4%**. That was the
wrong object (IGM path vs H0 angular kernel). The burst object is the
orifice (PRED-084). Do **not** keep this as an open isolate. Do **not**
stuff 66% into 0.5%. Do **not** reuse the formula.

## What was applied (the wrong object)

```text
DM_excess  ≈  200 pc cm⁻³  ·  (1 + local_sky_density)
local_sky_density  =  H0 ladder angular kernel, θ0 = 180°/φ²
```

The kernel is the *same grammar* as H0 sightlines (PRED-076). The
**formula** treats that dimensionless crowding (~±0.2) as a 20% wiggle
around a 200 pc class. That is a local-bubble perturbation, not IGM path.

| Handle | Value |
|--------|------:|
| Density range on this seed | -0.132 … 0.243 |
| Predicted excess band | 174 … 249 pc cm⁻³ |
| Measured excess range | 15 … 1200 pc cm⁻³ |
| Median error | **66.4%** |
| High-density median excess (n=5) | 380.0 |
| Low-density median excess (n=5) | 420.0 |
| Density tracks excess (sign) | **False** |

Worst row: `FRB20171020A` measured 15.0 vs
pred 176.124 (**1074.1619%**).
Best row: `FRB20121102A` **11.5104%** — still not a gate.

## Why the mathematics is off (APPLY, not a new β)

1. **IGM path is Cosmology \(D=25\).** DM excess grows with redshift.
   A nearby FRB can sit at ~15 pc cm⁻³ extra. A distant one at ~580.
   \(200·(1+0.2)\) cannot leave ~160–240. The band is a **ceiling of the formula**,
   not a measurement.
2. **Sign is wrong on this seed.** Higher angular density does **not**
   come with higher median excess (high 380 vs low 420). A bubble-density
   multiplier would have the other sign.
3. **n=10 with excess, 38 with RA, no redshift.** CHIME dump 503s blocked.
   This is a seed, not a catalog. A 0.5% central on ten numbers would be stuffing.

## Correct objects (already locked — do not retune)

| Lock | Object |
|------|--------|
| **PRED-052** | 200 pc cm⁻³ *class* (some sightlines sit near that class) |
| **PRED-076** | Same \(\theta_0=180/\varphi^2\) kernel as H0 — classifier, not a DM residual |
| **PRED-084** | Orifice: width×fluence vs \(e\cdot\mathrm{POOF}\) — the burst object |

## What replaced it (orifice — the burst object)

The burst is not sky crowding. It is the puncture. See
[`FRB_ORIFICE.md`](FRB_ORIFICE.md) · PRED-084.

```text
E_rip = width_ms × fluence     (no DM — DM is IGM path)
repeater if E_rip ≥ e · POOF   (enough outgassing to flop the saloon doors)
T_activity = 5π + 1/φ days     (Particle orifice cycle + Omori rest)
```

## Later Cosmology split (not this 66% sitting open)

```text
DM_obs  =  DM_MW  +  DM_IGM(z)  +  DM_host/bubble
         Cosmology D=25     leftover vs local_sky_density
```

Route `DM_IGM(z)` on Cosmology when redshifts exist. That is a separate
job for the PRED-052 class. It does **not** reopen this retired formula
as an isolate.

## Kill

- Keeping 66% on the open isolate list after the orifice replaced it.
- Stuffing 66% into the 0.5% green gate.
- Fitting β in `200·(1+β·density)` after seeing these 10 rows.
- Retuning the 200 class.
- Calling PRED-076 a 0.5% DM residual.
- Reusing `200·(1+local_sky_density)` as a DM residual.

Refresh: `python scripts/diagnose_frb_dm_interface.py`

Related: [`OBJECT_SCORING.md`](OBJECT_SCORING.md) · [`APPLY.md`](APPLY.md) ·
[`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md) ·
[`FRB_ORIFICE.md`](FRB_ORIFICE.md) · PRED-052 / PRED-076 / PRED-084
