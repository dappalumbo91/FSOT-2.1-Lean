# Traceable concepts — what FSOT actually says

This is the **picture → engine** map. It is not a second theory.

If a picture and `vendor/fsot_compute.py` (pin **D1D38A**) disagree, **the engine wins** until a named route changes.

| You are… | After this page |
|----------|-----------------|
| Regular reader | You should be able to say what a black hole, a white hole, and a bubble *do* in FSOT |
| Scientist | You should know which file implements each picture |
| Mathematician | You should know the closed forms and what is *not* a free parameter |

Live counts stay in [`CURRENT_STATUS.md`](CURRENT_STATUS.md). Sibling folds: [`../RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md).

---

## C1 — One fluid, three strings

**Said:** Spacetime is a compressible fluid. Everything is a pattern in that fluid at a different zoom.

**Engine:**

\[
S = K\,(T_1 + T_2 + T_3)
\]

| String | Role | Where it lives |
|--------|------|----------------|
| \(T_1\) | Look / observer | `observed` flips quirk / \(C_{\mathrm{factor}}\) |
| \(T_2\) | Body / scale | amplitude, linear bias |
| \(T_3\) | Strum / valve | POOF, SUCTION, acoustic bleed, phase |

\(K \approx 0.420222\) is frozen from \(\pi,e,\varphi,\gamma\). No new dial per observable.

**Code:** `vendor/fsot_compute.py` · Lean `FSOT/Scalar.lean`

---

## C2 — Black hole → white hole (the valve)

**Said:** A black hole is not a trash can. It is an **infall / compression / POOF** valve. A white hole is the **outflow / suction / re-solidification** of the same information.

```text
infall (BH)  →  POOF (orifice)  →  outflow (WH)
   compress        tunnel           lens + suction + C_eff
```

| Constant | ≈ | Job in the cycle |
|----------|--:|------------------|
| POOF | 0.1535 | tunneling / orifice open |
| SUCTION | 0.1470 | re-compaction on the way out |
| \(C_{\mathrm{eff}}\) | 0.9577 | coherence / re-solidification |
| \(T_3\) | valve × acoustic × phase | when the orifice opens and how hard it sucks |

**Conservation claim:** core scalars \(S, T_1, T_3\) are the invariants. Representation can change. The cycle cost is an engineering proxy, not a new seed.

**Code:** `scripts/bubble_bleed_physics.py` · panel `data/blackhole_whitehole_cycle_live_panel_benchmark.json`  
**Desktop prototype:** `Desktop/FSOT_BlackHole_WhiteHole/`  
**Predictions that use this:** [`../predictions/EXPLAINED.md`](../predictions/EXPLAINED.md) §3

---

## C3 — Bubble bleed (why Hubble tools disagree)

**Said:** Expanding nebulae and sightlines sit in different **bubble-density sectors** of the same fluid. CMB, TRGB, and Cepheids are not measuring two universes. They couple to different BH→WH outgassing sectors.

\[
H_0^{\mathrm{global}} \approx 68.4401,\qquad
\varepsilon = H_0^{\mathrm{global}}/67.4 - 1 \approx 0.015431
\]

\[
H_0^{\mathrm{tool}} = H_0^{\mathrm{global}}\,(1 + \rho_{\mathrm{sector}}\,\varepsilon)
\]

| Tool class | Sector density \(\rho\) | FSOT readout | Published class |
|------------|------------------------:|-------------:|-----------------|
| Planck CMB | −1 (depleted) | 67.384 | ~67.4 |
| Carnegie / TRGB | ~2 | ~70.6 | ~69.8–70.4 |
| SH0ES local | 5.05 (inflated) | 73.773 | ~73.0–73.5 |
| PRED-001 bridge | between | **70.75** | between the two walls |

There is **not** one H₀ every instrument is “supposed” to see. Kill a *tool row*, not the whole sky.

**Code:** `scripts/bubble_bleed_physics.py` · `predictions/h0_multi_tool_predictions.json`  
**Sibling replay:** FSOT-Quantum `docs/H0_TENSION.md` (Planck 0.024%, SH0ES 1.00% on the 2.5% contested band)

---

## C4 — Bleed between domains (not one \(D\) forever)

**Said:** Tanks connect. Quantum, optics, chemistry, and cosmology are not isolated formulas.

\[
\kappa_{ij} = A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i|\,|S_j|
\big/\bigl(1+|D_i-D_j|/25\bigr)
\]

Then \(S\) relaxes. The wave is \(\Delta S\), not a new coefficient.

**Code:** `docs/COMPLEX_SYSTEM_DERIVATION.md` · `vendor/fsot_complex_interaction.py`  
**Sibling:** FSOT-Quantum `fsot_quantum/quantum_bleed.py`

---

## C5 — Folds, not Hilbert \(2^n\)

**Said:** Quantum computing jobs do not require expanding \(2^n\) amplitudes. Change **domain / \(D_{\mathrm{eff}}\) / observed**.

| Fold | \(D_{\mathrm{eff}}\) | \(S\) | Job |
|------|---------------------:|------:|-----|
| Quantum_Mechanics | 6, observed | +0.9555 | measure / spin resolve |
| Quantum_Computing | 11, dark | −0.1477 | compute substrate |
| Quantum_Optics | 11, look | +0.4082 | phase / look path |

**Observe path:** QC (dark) → Quantum_Optics (look) → QM (measure).  
Looking at QC flips the compute identity. That is the Hilbert move. Do not do it.

**Repo:** [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum) · ledger [`../results/siblings/`](../results/siblings/)

---

## C6 — Genetics residual (not a trained fold)

**Said:** A protein interface does not get a fitted spring. Residual **scales the named ChemLink**.

\[
r = 1 + |S_{\mathrm{domain}}|\cdot P_{\mathrm{NEW}},\qquad P_{\mathrm{NEW}}=(\gamma/e)\sqrt{2}
\]

Two regimes, keep them separate:

| Regime | What it is | Freeze (2026-08-13) |
|--------|------------|---------------------:|
| **Product** | measured homolog Cα except the eval PDB + residual only when bonds are broken | median **0.13 Å** vs AF **0.47 Å** (10/10) |
| **Bulk / orphan** | sequence-only F01–F15 | median **~13.6 Å** — information ceiling, not a bug |

The 2026-08-07 Lean file `predictions/reports/FSOT_VS_ALPHAFOLD_STRUCTURE.md` is the **bulk** snapshot (~15 Å). Do not quote it as the product.

**Repo:** [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics)

---

## C7 — Trinary (the shared alphabet)

Spins and codons use the same three symbols:

| Trit | Meaning |
|------|---------|
| \(+1\) / \(−1\) | collapsed observations (`trit_not` of each other) |
| \(0\) | superposed — do not average the two collapses |

DFG-in vs DFG-out, compact vs extended calmodulin, QC-dark vs QM-look: one apparatus, two collapses. Residual must not pick the observation.

---

## How to add the next picture

1. Write it here in plain words (C8, C9, …).
2. Map each phrase to **one existing** engine object.
3. If nothing maps, stop — do not invent a coefficient.
4. Add a live check that can fail.
