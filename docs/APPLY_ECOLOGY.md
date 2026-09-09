# APPLY cookbook — Ecology (habitat fold)

**Pin:** D1D38A · **core:** `Ecology` · \(D_{\mathrm{eff}}=15\) · `observed=False` (**dark — do not flip**) · \(\delta\psi=0.2\).  
**Neighbors:** Condensed_Matter / Neuroscience \(D=14\); Fluid / Nuclear / Thermo \(D=15\); Meteorology / Psychology \(D=16\).  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §36.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Occurrence latitude | GBIF `decimalLatitude` (`data/ecology_gap_fill_benchmark.json`, `source: gbif_api`) | Invented plant/bee watts |
| Occurrence longitude | GBIF `decimalLongitude` | A clock-time range |

Wrong object: live \(\lvert S_{\mathrm{eco}}/S_{\mathrm{neighbor}}\rvert\) vs 1 on mixed observed/dark scalars.

---

## 2. Pick the interface

Ecology is the **habitat** zoom of the same fluid. Do **not** set `observed=True`. Do **not** invent metabolic watts to fill a residual.

---

## 3. Route

```text
S = domain_scalar("Ecology")               # D=15, dark
computed, err% = fsot_scaled(m, "Ecology")
```

Dual-route the **same GBIF latitude** onto the adjacent core (CM density, NDBC pressure, ENDF keV, Carnot, Nunnally/Cohen). That is one neighborhood, two zooms.
