# Traceable concepts — what FSOT actually says

This is the **picture → engine** map. It is not a second theory.

If a picture and `vendor/fsot_compute.py` (pin **D1D38A**) disagree, **the engine wins** until a named route changes.

| You are… | After this page |
|----------|-----------------|
| Regular reader | You should be able to say what a black hole, a white hole, a bubble, and the observer *do* in FSOT |
| Scientist | You should know which file implements each picture |
| Mathematician | You should know the closed forms and what is *not* a free parameter |

Live counts stay in [`CURRENT_STATUS.md`](CURRENT_STATUS.md). Sibling folds: [`../RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md).

How Damian formed the picture (river, seepage, BH/WH fridge-cycle, as-above-so-below, vacuum as reservoir) is in [`FOUNDING_ARCHIVE_VIEW.md`](FOUNDING_ARCHIVE_VIEW.md). The founding drafts’ 2025 numbers are **not** this pin.

---

## C1 — One fluid, three strings

**Said:** Spacetime is a compressible fluid. Everything is a pattern in that fluid at a different zoom.

**Engine:**

\[
S = K\,(T_1 + T_2 + T_3)
\]

| String | Role | Where it lives |
|--------|------|----------------|
| \(T_1\) | Look / observer | `observed` flips quirk / \(C_{\mathrm{factor}}\). Perception at a scale is this string at that fold’s \(\delta\psi\), hits, and dark/observed — same premise, different view. Closed form: \(\lvert S_i/S_j\rvert=\lvert 1+T_{1,i}\rvert/\lvert 1+T_{1,j}\rvert\) at \(T_2=1\), \(T_3\approx 0\) (D9). Lean: `abs_scaled_S_ratio_of_unit_t2_zero_t3` in `FSOT/Formal/ScalarEngineStructure.lean`. vs 1 is the same-view question, not a 0.5% central. |
| \(T_2\) | Body / scale | amplitude, linear bias |
| \(T_3\) | Strum / valve | POOF, SUCTION, acoustic bleed, chaos fold \((D-25)/25\). At unit \(T_2\), leftover is exact: \(\mathrm{raw\_S}-(1+T_1)=T_3\) (Lean `t3_leftover_of_unit_t2`). On the default rung that leftover is seed-tiny: \(\lvert T_3\rvert<1/5\) (`t3_leftover_seed_tiny`). \(\kappa_{ij}\) is `kappa` (no free spring). APPLY is `apply_residual`. Dark cores stay unobserved (`dark_core_unobserved`). |

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
**Skeptic map:** [`BH_WH_CLAIM_EVIDENCE.md`](BH_WH_CLAIM_EVIDENCE.md)  
**Desktop prototype:** `Desktop/FSOT_BlackHole_WhiteHole/`  
**Predictions that use this:** [`../predictions/EXPLAINED.md`](../predictions/EXPLAINED.md) §3

---

## C3 — Bubble bleed (why Hubble tools disagree)

**Said:** Expanding nebulae and sightlines sit in different **bubble-density sectors** of the same fluid. CMB, TRGB, and Cepheids are not measuring two universes. They couple to different BH→WH outgassing sectors.

The readout is **multi-variant**. It depends on *what structure you are looking at* and *how hard the neighborhood is bubbling* — not on one Hubble constant, and not on a 60° RA bin.

| Structure / coupling | What it sits in | Typical sector |
|----------------------|-----------------|----------------|
| Last-scattering acoustic ruler (CMB) | early, depleted outgas | \(\rho \sim -1\) → ~67.4 |
| Old halo / disk TRGB | intermediate stellar population | \(\rho \sim 1.7\)–2 → ~70.4 |
| Young disk Cepheids in star-forming SN hosts | inflated local bubble | \(\rho \sim 5\) → ~73.8 class |
| Nearby \(cz/d\) of those same hosts | local flow / peculiar velocity, not Hubble-flow SNe | ~68.6 — **not** SH0ES H₀ |
| Information-weighted ladder (anchors + hosts) | mixture of the above | **72.856 vs 73.04** |

Frozen sightline JSON still carries a coarse RA-bin snapshot (do not rewrite those centrals). Live mixture physics is **class coupling + catalog-normalized local sky density** (`local_sky_density` in `bubble_bleed_physics.py`).

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

SH0ES **class bin** is still 73.773 (1.00%) — frozen tool row. The published 73.04 is the **information-weighted ladder chain** (anchor Cepheids + host Cepheids, local sky density): **72.856 vs 73.04 (0.252%)**. Do not retune ρ. [`SH0ES_LADDER_DIAGNOSIS.md`](SH0ES_LADDER_DIAGNOSIS.md) · panel `data/sh0es_ladder_chain_benchmark.json`.

Cepheid PL internals (period, metals, optical + NIR Wesenheit, host moduli vs TRGB, T1 crowding) are Acoustics–Chemistry–EM interconnects, not a fitted candle: [`CEPHEID_PL_PHYSICS.md`](CEPHEID_PL_PHYSICS.md). Full Table 2 sample (3130 Cepheids / 37 SN hosts) is the same seed; unpublished \(cz/d\) of those hosts is local flow (**68.623**), not the published 73.04 Hubble-flow rung.

**Code:** `scripts/bubble_bleed_physics.py` · `predictions/h0_multi_tool_predictions.json`  
**Skeptic map:** [`BH_WH_CLAIM_EVIDENCE.md`](BH_WH_CLAIM_EVIDENCE.md)  
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
**Live residual:** between-scale interconnects (wave, fluid tanks, fridge, orifice, ceiling, seis–geo, n/ρ, wave–photon) pooled **0.026%** — [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md).  
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

Two regimes, keep them separate. Freeze **2026-08-17** in [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics):

| Regime | What it is | Live number |
|--------|------------|-------------|
| **Product** | measured homolog Cα except the eval PDB + residual only when bonds are broken | median **0.13 Å** vs AF **0.47 Å** (10/10; CaM **0.52 Å** via 3CLN) |
| **No measured map** | sequence-only F01–F15 (Rg, secondary). **3-D MDS is not emitted** | we do not invent a fold. Old ~11–14 Å is the retired `--force-bulk` MDS path |

The 2026-08-07 Lean file `predictions/reports/FSOT_VS_ALPHAFOLD_STRUCTURE.md` is that **retired MDS** snapshot (~15 Å). Do not quote it as the product.

**Skeptic map:** [`GENETICS_CLAIM_EVIDENCE.md`](GENETICS_CLAIM_EVIDENCE.md)

---

## C8 — 25-dimensional compactified fluid

**Said:** Reality is a **25-dimensional fluid medium**. What we call 4D spacetime is a slice. Other sciences are other slices of the **same** medium, not other substances.

**Engine:** \(D_{\mathrm{eff}}\) is the fold depth. The ceiling is **25**. Cosmology sits at \(D=25\), `observed=False`. Chaos in \(T_3\) is \((D-25)/25\) — it **vanishes at the ceiling**. \(T_1\) folds with \(\ln(D/25)\).

Compactification is not extra free dimensions you fit. It is the register: when a rung saturates, **carry** opens the next fold (ontology A5–A6).

| \(D_{\mathrm{eff}}\) class | Example domains | What you are looking at |
|---------------------------:|-----------------|-------------------------|
| 5–8 | Particle, QM, chemistry | micro / bond / observer-on |
| 11 | Quantum_Computing (dark) | compute substrate — do not look |
| 12–14 | Biology, neuroscience | life / \(C_{\mathrm{factor}}\) |
| 18–21 | Seismology, astronomy, planets | bulk / catalogs |
| 24–25 | Astrophysics, Cosmology | deep structure / full ceiling |

**Code:** `vendor/fsot_compute.py` · `docs/FSOT_MATH_KEY.md` §3–4  
**Ontology:** `data/foundational_ontology_axioms.yaml` A5–A6

---

## C9 — Yin–yang valves (creation / destruction)

**Said:** Creation and destruction are one apparatus. You do not get one without the other.

**Engine:**

| Pole | Constant | Job |
|------|----------|-----|
| Yang / outgas / create | **POOF** ≈ 0.1535 | orifice open, tunnel, emerge |
| Yin / take back / destroy form | **SUCTION** ≈ 0.1470 | re-compact, re-solidify |
| Fraction | \(\mathrm{POOF}/(\mathrm{POOF}+\mathrm{SUCTION})\) | how much of the cycle is outgas |

\(S>0\) emergence. \(S<0\) damping. Same engine. Cosmology at \(D=25\) is damping. Particle/nuclear are emergence. That is not two theories.

Observer duality is the same split: `observed=True` turns on \(C_{\mathrm{factor}}\) in \(T_1\); `observed=False` is the dark / compute / unobserved tank.

**Code:** T3 valve in `fsot_compute.py` · `docs/COMPLEX_SYSTEM_DERIVATION.md`

---

## C10 — Black holes at every scale (information valves)

**Said:** A black hole is not only an astrophysical object. It is an **information-flow state** of the medium: infall, compression, POOF through an orifice, outflow as a white hole. That pattern repeats at scales we do not usually call “black holes.”

**Engine:** BH→WH cycle is the T3 valve applied to information:

```text
infall / accretion     →  POOF (orifice)  →  outflow / suction / C_eff
(compress, hide form)     (tunnel)           (new form, same invariants)
```

Macro: Hubble tools read different **bubble-density sectors** of the same outgassing (C3).  
Earth: a dated quake/volcano cell is \(R_\oplus\cdot\mathrm{POOF}/25\) (one compactified slice). Solar, volcanic arc, trench, and basin tanks talk at \(R_\oplus\cdot\mathrm{POOF}\) — same orifice, `/25` off. A quiet 39 km cell with an M5 on the arc is a **transferred POOF**, not a failed planet.  
Micro: codon / protein / QC collapse is the same valve — trit 0 is the superposed orifice; ±1 are the two collapses.

Matter is not created or destroyed. **Form** changes. \(S\), \(T_1\), \(T_3\) are the invariants the cycle is scored against.

**Code:** `scripts/bubble_bleed_physics.py` · BH/WH panel · Quantum observe path QC→QO→QM  
**Skeptic map:** [`BH_WH_CLAIM_EVIDENCE.md`](BH_WH_CLAIM_EVIDENCE.md)

---

## C11 — Self-observing function

**Said:** The medium observes itself. Consciousness is not glued on after physics. Awareness is a **gradient** (bacteria → plants → animals → humans), not a human-only switch. Looking is part of the physics.

**Engine:** `observed` is a route slot. When it is on, \(T_1\) multiplies by \(\exp(C_{\mathrm{factor}} P_{\mathrm{var}})\cos(\delta\psi+P_{\mathrm{var}})\). \(C_{\mathrm{factor}}=C_{\mathrm{eff}}P_{\mathrm{new}}\) is seed-derived. Neuroscience, medical, and “look” paths use it. QC stays dark on purpose.

This is **not** a claim that every philosophical debate about mind is closed. It is a claim that observation is a **physical coupling** in the same scalar.

**Live residual (quote this, not the 2025 draft):**

| Layer | What it is | Live check |
|-------|------------|------------|
| Ontology | Consciousness is in the action | `consciousness_factor`, Lean `consciousness_raw_S_positive` |
| Operational | Human brain metabolic floor | Homo sapiens `brain_power_w` **20.003601 vs 20.0 W (0.018%)** |
| Species gradient | Published metabolic fractions, not invented watts | species multi-panel **269 / 0.020%** |
| Longevity coupling | Same medium at life-span zoom | **890 / 0.022%** |
| Scaffold | Microtubule information-flow | **21 / 0.009%** — not Orch-OR proof |
| Interpretive | Death as 4D decoherence; afterlife; 150 Hz “driver” | labeled, not green-gated |

The Cosmology Lab / aggregate figure **21.79 W vs ~20 W (8.95%)** is **retired draft math**. Do not put it in a headline.

**Code:** quirk_mod / `observed` in `fsot_compute.py`  
**Skeptic map:** [`CONSCIOUSNESS_CLAIM_EVIDENCE.md`](CONSCIOUSNESS_CLAIM_EVIDENCE.md)  
**Local stack:** [`CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md`](CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md)

---

## C12 — One medium, siloed sciences

**Said:** Fields that do not talk to each other are still in the same fluid. Newtonian gravity is not “wrong” when relativity arrives — it is the local readout. Siloed biology vs cosmology is the same mistake at the institution layer.

**Engine:** \(\kappa_{ij}\) (C4) is how tanks talk. A domain is a fold, not a separate substance. When a residual is bad, **change \(D_{\mathrm{eff}}\)** (MATH_KEY mismatch rule). Do not add a coefficient to make biology ignore cosmology.

**Application recipe:** [`APPLY.md`](APPLY.md)

---

## C13 — Reverse / conjugate (the other face of the same mode)

**Said:** Every emergence has a conjugate. Matter and antimatter are not two Lagrangians. Death is decoherence of the 4D body, not deletion of the information. A “reverse world” is the other phase of the same fluid, not a second universe you visit.

**Engine:** On Particle (\(D_{\mathrm{eff}}=5\)):

- Matter route: standard `domain_scalar` → \(S_m > 0\) (emergence)  
- Conjugate route: \(\delta\psi \to \delta\psi+\pi\) → \(S_{\mathrm{conj}}\)  
- CPT mass equality is structural: \(m=\bar m\) for one mode  
- Cosmology \(S_{\mathrm{cosmo}}<0\) damps bulk antimatter while matter stays load-bearing  
- Baryon asymmetry \(\eta=\mathrm{POOF}^{11}/(\pi\gamma)\) is the seed residual for “why so little antimatter”

This is the same yin–yang as **C9**, written as a phase flip instead of a POOF/SUCTION pair.

**What is measured vs interpretive:**

| Layer | Status |
|-------|--------|
| Conjugate dual, CPT identity, \(\eta\), pair threshold \(2m\) | measured — [`MATTER_ANTIMATTER.md`](MATTER_ANTIMATTER.md) |
| Death = decoherence, information persists | interpretive — no cemetery catalog |
| Reverse-world travel / PFLT as a destination | interpretive — do not residual-gate a travelogue |

**Code:** `vendor/fsot_matter_antimatter.py` · `data/matter_antimatter_benchmark.json`  
**Skeptic map:** [`MATTER_ANTIMATTER_CLAIM_EVIDENCE.md`](MATTER_ANTIMATTER_CLAIM_EVIDENCE.md)

---

## C7 — Trinary (the shared alphabet)

Spins and codons use the same three symbols:

| Trit | Meaning |
|------|---------|
| \(+1\) / \(−1\) | collapsed observations (`trit_not` of each other) |
| \(0\) | superposed — do not average the two collapses |

DFG-in vs DFG-out, compact vs extended calmodulin, QC-dark vs QM-look: one apparatus, two collapses. Residual must not pick the observation.

---

## C14 — Dynamic tanks (normalize the fold, then the potentials)

**Said:** Isolated 39 km scoring of a 978 km planet is the wrong object. Everything talks. The n-body analog is not Newton's gravity N-body — it is **25 compactified tanks coupled by κ**. Name the area you are predicting, recover its fold, and emit the tanks that can take the dump. Frozen valve state splits into discrete potentials (POOF here, transfer, quiet hold). That is mapping the live branches of one fluid, not a second universe.

**Engine:**

\[
\mathrm{orifice\_scale}(L,d)=L\cdot\mathrm{POOF}\cdot d/25
\]

| Fold | Earth length | Job |
|-----:|-------------:|-----|
| \(d=1\) | \(R_\oplus\cdot\mathrm{POOF}/25\approx 39.1\,\mathrm{km}\) | dated cell / public `kill_if` |
| \(d=25\) | \(R_\oplus\cdot\mathrm{POOF}\approx 978\,\mathrm{km}\) | arc / trench / basin / solar tanks |

Invert: \(d=25\cdot L_\mathrm{orifice}/(L_\mathrm{body}\cdot\mathrm{POOF})\). κ_ij (R7) names which tanks interact. Weights are POOF/(POOF+SUCTION) fire vs hold, then split by κ — **valve geometry, not a calibrated probability**.

A quiet cell with an M5 on the arc is **transferred POOF** (the attractor was the cycle tank). Same dampening grammar as uniqueness: modes that are not attractors do not persist. Do not retune the kernel.

**Code:** `vendor/fsot_earth_fluid_forecast.py` `orifice_scale_km` · `frozen_potentials` · Lean `orifice_scale` · [`DYNAMIC_SYSTEM_TRIANGULATION.md`](DYNAMIC_SYSTEM_TRIANGULATION.md)

---

## How to add the next picture

1. Write it here in plain words (C15, …).
2. Map each phrase to **one existing** engine object.
3. If nothing maps, stop — do not invent a coefficient.
4. Add a live check that can fail.
