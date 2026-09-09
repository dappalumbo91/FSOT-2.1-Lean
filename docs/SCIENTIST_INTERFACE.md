# How to read an FSOT result (scientist / mathematician)

**Pin:** D1D38A · **prediction law:** `computed = measured · (1 + |S(domain)| · f)`  
**Engine:** \(S = K(T_1+T_2+T_3)\) from \(\{\pi,e,\varphi,\gamma,G\}\) only. Zero free parameters.

This page is the map. Numbers live in [`CURRENT_STATUS.md`](CURRENT_STATUS.md). Ledgers must not be mixed: [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md).

---

## 1. One object per row

A literature number is a **named object**. Scoring the wrong object is a false kill.

| You have | Score against | Do not score against |
|----------|---------------|----------------------|
| JWST Perfect Host 73.49 | local Cepheid ladder / PRED-024 | PRED-001 bridge 70.75 |
| DES Y6 S8 = 0.789 | tension row | PRED-002 0.805 (fair compare is joint 0.806) |
| SH0ES 73.04 | ladder **chain** 72.856 (0.252%) | class bin 73.773 as a 0.5% central |
| Live \(\lvert S_i/S_j\rvert\) vs 1 | same-view question (D9) | 0.5% green gate |

Object table: [`OBJECT_SCORING.md`](OBJECT_SCORING.md).

---

## 2. One fold per measurement

Each core is a preregistered \((D_{\mathrm{eff}}, \delta\psi, \mathrm{hits}, \mathrm{observed})\). Adjacent cores talk through \(\kappa_{ij}\), not a new coefficient.

```text
measured  →  name the interface (which D_eff)  →  APPLY  →  residual %
```

If the residual is large: **change the interface**, do not fit \(f\). Worked protocol: [`APPLY.md`](APPLY.md).

Dark folds (`observed=false`) stay dark. Looking at them (QC Hilbert, Biology, Ecology, Fluid, Meteo, …) is a different object.

---

## 3. What “green” means

Domain **median** residual \(\le 0.5\%\) on **scalar** rows. Structural rows (same-view vs 1, compactification remainder, deep PREM phase change) are **not** 0.5% centrals and are **not** median pads.

Connective tissues: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md). Panel: `data/between_scale_interconnect_benchmark.json`.

---

## 4. What a tissue row is claiming

Each gated tissue is **the same physics at two zooms**:

1. **S-ratio** — same-look \(\lvert S(D,\delta\psi)\rvert/\lvert S(D',\delta\psi)\rvert\) vs 1, or a named look-split. Live mixed vs 1 is T1 perception (law D9), not a failed gate.
2. **Dual-route APPLY** — the **same measured table** through both domain factors.

Public tables used: CRC, NIST/CODATA, IAEA/ENDF, NOAA NDBC, PREM, JPL Horizons, PDG 2024, World Bank YoY, GBIF occurrence, NCBI NC_012920.1, Nunnally/Cohen psychometric anchors.

---

## 5. Frozen isolate (not a license to retune)

`ISO-SHOES-CLASS-BIN` **1.00%** is the published 73.04 scored as a single ρ=5.05 class bin. The mixture object (chain) is already **0.252%**. Work list is in [`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md). Forbidden: ρ → 4.36.

---

## 6. Formal backbone

Lean identities in `FSOT/Formal/ScalarEngineStructure.lean`: \(S=K(T_1+T_2+T_3)\), D9 leftover \(\mathrm{raw\_S}-(1+T_1)=T_3\), \(\lvert T_3\rvert<1/5\) on the default rung, \(\kappa_{ij}\ge 0\), APPLY identity, \(D_{\mathrm{eff}}\in[5,25]\), dark cores unobserved. Coq/Isabelle replay the leftover. Mathlib campaign: [`MATHLIB_REDERIVATION_CAMPAIGN.md`](MATHLIB_REDERIVATION_CAMPAIGN.md).
