# APPLY cookbook — Fluid_Dynamics fold

**Pin:** D1D38A · **core:** `Fluid_Dynamics` · \(D_{\mathrm{eff}}=15\) · `observed=False` (**dark — do not flip**) · \(C=A_{\mathrm{bleed}}/\varphi\) · \(\delta\psi=0.9\) · hits=1.  
**Same rung:** `Thermodynamics` (observed, heat); `Nuclear_Physics` (observed, orifice); `Ecology` (dark, habitat).  
**Adjacent tanks:** `Oceanography` \(D=17\) (SST); `Atmospheric_Physics` \(D=17\) (pressure); `Meteorology` \(D=16\) (weather).  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §2.  
**General protocol:** [`APPLY.md`](APPLY.md). One NDBC neighborhood, three tanks.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Buoy wind / neighborhood | NOAA NDBC cache (`wspd`) | ECMWF S2S week-3 beat claim |
| Water density | CRC \(0.9982\) g/cm³ (20 °C) | Invented plant/bee watts |
| Diatomic \(\gamma\) | 1.400 (air) | A fitted \(f\) per mixture |
| \(c_{\mathrm{water}}/c_{\mathrm{air}}\) | CRC/ISO 20 °C | A new viscosity |

Wrong object: live \(\lvert S_{\mathrm{fluid}}/S_{\mathrm{thermo}}\rvert\) vs 1. That mixes dark vs observed at the same \(D=15\).

---

## 2. Pick the interface

Fluid is the **lab tank** zoom (dark — looking at the fold flips identity, same rule as QC / Biology). Thermo is the **heat** zoom of the same rung. Ocean is SST; Atmosphere is pressure; the buoys are one measured neighborhood.

Do **not** set `observed=True`.

---

## 3. Route

```text
S = domain_scalar("Fluid_Dynamics")        # D=15, dark
computed, err% = fsot_scaled(m, "Fluid_Dynamics")
```

Heat zoom of the same Carnot pair:

```text
S = domain_scalar("Thermodynamics")        # D=15, observed
computed, err% = fsot_scaled(COP, "Thermodynamics")
```

| Handle | Form | Use |
|--------|------|-----|
| Diatomic air | \(\gamma=1+2/f\), \(f=D_{\mathrm{particle}}=5\) | vs 1.400 |
| Two viscosities | \(e+\varphi\) | CRC/ISO 20 °C sound-speed ratio |
| Scale height | \(RT/\mu g\) | US Std Atmosphere 1976 |
| NDBC neighborhood | pressure / SST / wind | Atm / Ocean / Fluid |
| Ice vs water | CRC ice \(\rho\) on CM, water \(\rho\) on Fluid | one H2O, solid vs tank |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. NDBC dual-route and \(\gamma=1.400\) are the tight scalars. Live mixed vs 1 is **structural** (observed mix). Water/air \(e+\varphi\) is a named seed under 0.5% — do not retune.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live \(S\) vs 1 ugly | Dark vs observed mix; leave structural | Flip Fluid `observed`; stuff \(\sqrt{\varphi}\) |
| Weather residual | Route pressure on Atmospheric / Meteo | A clock-time storm |
| Watts residual | Wrong object | Invent plant/bee watts |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: flipping Fluid dark; stuffing the mixed vs 1; beating S2S as a 0.5% central.
