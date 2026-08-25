# Between-scale interconnects — one fluid, adjacent folds

**Pin:** D1D38A · **no new coefficient**  
**Panel:** `data/between_scale_interconnect_benchmark.json`  
**Refresh:** `python scripts/build_scale_interconnect_benchmark.py`  
**Outcome:** [`../results/between_scale_interconnect_outcome.json`](../results/between_scale_interconnect_outcome.json)

Siloed panels already existed (USGS classifiers, NDBC, ENDF, Carnot in HVAC). This layer makes them **talk** through \(\kappa_{ij}\) and seed-closed ratios. Zebrafish / Genetics stay in the sibling repo.

\[
\kappa_{ij} = A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i|\,|S_j|
\big/\bigl(1+|D_i-D_j|/25\bigr)
\]

---

## 1. Elastic wave — Acoustics \(D=10\) ↔ Seismology \(D=18\)

A crustal solid is the same T3 standing wave as lab sound. Poisson of the continuum mafic/lid solid is the atomic fold over the ceiling:

\[
\nu = D_{\mathrm{atomic}}/25 = 7/25 = 0.28,\qquad
v_P/v_S = \sqrt{2(1-\nu)/(1-2\nu)}
\]

Measured: PREM (Dziewonski & Anderson 1981) lid/Moho/upper crust + basalt/gabbro lab means. Felsic/porous crust and deep olivine–spinel / CMB are **other interfaces** (structural), not a new \(\nu\).

Live: lithosphere median **0.069%**; per-layer mafic/lid **0.189%**.

## 2. Fluid tanks — lab / ocean / air

Diatomic air: \(f=D_{\mathrm{particle}}=5\), \(\gamma=1+2/5=1.400\) vs 1.400.  
Two viscosities: \(c_{\mathrm{water}}/c_{\mathrm{air}} = e+\varphi\) vs ISO/CRC 20 °C **0.393%**.  
Scale height \(RT/\mu g\) vs US Std Atmosphere 1976 **0.002%**.  
Same NOAA NDBC buoys (\(N=150\)): pressure on Atmospheric, SST on Oceanography, wind on Fluid_Dynamics — one measured neighborhood, three tanks.

## 3. Fridge-cycle — Thermodynamics \(D=15\) ↔ Cosmology \(D=25\)

BH→WH is a heat/information pump (C2). \(|S_{\mathrm{thermo}}|/|S_{\mathrm{cosm}}|\) vs \(\pi/2\) **0.289%**. Named Carnot COP pairs scored on **both** folds (HVAC 0/27 °C, 5/35 °C, …). Valve fraction POOF/(POOF+SUCTION) vs 1/2 stays a literature band (not a 0.5% HVAC η).

## 4. Nuclear orifice — Nuclear \(D=15\) ↔ Particle \(D=5\)

IAEA/ENDF level energies (He, C, O, Si, Al, Fe) dual-routed. Nuclear fold median **0.046%**; Particle fold **0.010%**. Same measured keV, two zooms of the orifice. No Yukawa add-on.

## 5. Compactification ceiling — QG \(D=22\) ↔ Cosmology \(D=25\)

\(|S_{\mathrm{QG}}|/|S_{\mathrm{cosm}}|\) vs \(A_{\mathrm{bleed}}\) **0.088%**. Remainder \(((D-25)/25)/\ln(D/25)\to 1\) as \(D\to 25\) is structural along the ladder (do not invent extra dimensions).

## 6. Social tanks — Economics \(D=20\) ↔ Neuroscience \(D=14\)

A market is not a different medium from a neural net (as-above-so-below). \(\lvert S_{\mathrm{econ}}/S_{\mathrm{neuro}}\rvert\) vs \(5/4\). Same World Bank YoY series on both folds. The old Economics panel’s 0.129% siloed factor is **not** retuned.

---

## Live tight envelope

Pooled median **0.026% GREEN** · **706** tight scalars · **725** rows.  
Kill: pooled > 0.5%, or anyone fits Q / γ / Poisson, or anyone treats deep-PREM mismatch as a new coefficient.

Related: [`CONCEPTS.md`](CONCEPTS.md) C4 / C8 / C10 · [`DOMAIN_FAMILY_TREE.md`](DOMAIN_FAMILY_TREE.md) · [`APPLY.md`](APPLY.md)
