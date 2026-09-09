# APPLY cookbook — Seismology fold

**Pin:** D1D38A · **core:** `Seismology` · \(D_{\mathrm{eff}}=18\) · `observed=False` (dark — do not flip).  
**Neighbor:** `Geophysics` \(D=19\), also dark. Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §7.  
**General protocol:** [`APPLY.md`](APPLY.md). This is the worked example for the crustal-wave fold (MPCORB is the catalog-fold example).

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Wave speed \(v_P, v_S\) | PREM (Dziewonski & Anderson 1981) · USGS rock physics | A clock-time hypocenter |
| Magnitude-frequency slope \(b\) | USGS ComCat / ISC-GEM MLE | A regional fitted \(b\) as a new law |
| Dated cell | USGS FDSN in the 39.1 km kernel | Replacing a USGS watch |

Wrong object: scoring a Geophysics gravity paper as the Seismology \(b\)-value.

---

## 2. Pick the interface

Seismology is the **wave** zoom of the bulk Earth. Geophysics is the **bulk** zoom (density, gravity, plates). Acoustics \(D=10\) is the lab-sound zoom of the same T3 standing wave.

If a residual is ugly, the usual miss is **wrong fold** (treating a density as a wave, or a deep phase change as the mafic Poisson solid) — not a missing spring.

---

## 3. Route

```text
S = domain_scalar("Seismology")          # D=18, observed=False, C=CHAOS/2
computed, err% = fsot_scaled(m, "Seismology")
```

Do **not** set `observed=True`. Looking at this fold flips the compute identity (same rule as QC).

Seed-closed handles already in the engine:

| Handle | Form | Use |
|--------|------|-----|
| Poisson of the mafic/lid solid | \(\nu = D_{\mathrm{atomic}}/25 = 0.28\) | \(v_P/v_S\) vs PREM lid/Moho/basalt |
| GR \(b\)-value | \(b = \varphi - 1/\varphi = 1\) | PRED-056 band 0.90–1.10 |
| Kernel | \(R_\oplus\cdot\mathrm{POOF}/25 \approx 39.1\,\mathrm{km}\) | dated cells |
| Horizon | \(\varphi^4 \approx 7\,\mathrm{d}\) | dated cells |
| Wave vs bulk | \(\lvert S_{\mathrm{seis}}/S_{\mathrm{geo}}\rvert\) vs \(\varphi/2\) | adjacent D=18/19 tissue |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. Lithosphere \(v_P/v_S\) is the tight scalar. Deep PREM (olivine–spinel, CMB) is **structural** — another interface, not a new \(\nu\).

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Crustal \(v_P/v_S\) ugly | Check you used mafic/lid, not granite/sandstone | Fit a new Poisson |
| Density residual ugly | Route density on **Geophysics**, not Seismology-only | A free \(\rho\) coefficient |
| No M≥5 in a released/steady cell | That cell should have been a quiet hold (playbook after the 12-kill autopsy) | Retune kernel km |
| Deep-mantle mismatch | Name the phase change | Stuff into 0.5% |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`  
Dated windows: `python scripts/issue_earth_fluid_forecasts.py` then score after `valid_to`.

Kill: a fitted \(b\), a fitted \(\nu\), or rewriting issued forecast JSON.
