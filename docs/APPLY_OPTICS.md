# APPLY cookbook — Optics fold

**Pin:** D1D38A · **core:** `Optics` · \(D_{\mathrm{eff}}=10\) · `observed=True` · \(C=\pi/e\).  
**Neighbor:** `Quantum_Optics` \(D=11\), same \(C=\pi/e\). Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §9.  
**Same rung, other \(C\):** `Materials_Science` \(D=10\), \(C=A_{\mathrm{in}}/e\). Tissue: §8.  
**General protocol:** [`APPLY.md`](APPLY.md). This is the worked example for the light fold (MPCORB is catalog; Seismology is crustal-wave).

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Sodium-D index \(n_D\) (~589 nm) | CRC / NIST handbook | A fitted Cauchy/Sellmeier \(B\) as a new law |
| Ice Ih ordinary-ray \(n\) | CRC / literature \(n_o=1.309\) | Air \(n-1\) (different interface) |
| Density of the same specimen | CRC (route on **Materials**, not Optics) | Stuffing \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) vs 1 |

Wrong object: scoring a dielectric-static \(\varepsilon_r\) paper as optical \(n^2\) (orientational vs electronic).

---

## 2. Pick the interface

Optics is the **wave** zoom of light. Quantum_Optics is the **photon** zoom of the same light (one compactification step, same interpretation constant). Materials is the **bulk** zoom of the same specimen (same \(D=10\), different \(C\)).

If a residual is ugly, the usual miss is **wrong fold** (static \(\varepsilon\) as \(n\), or Materials \(C\) as if it were Optics \(C\)) — not a missing oscillator strength.

---

## 3. Route

```text
S = domain_scalar("Optics")                 # D=10, observed=True, C=π/e
computed, err% = fsot_scaled(m, "Optics")
```

Photon zoom of the same \(n_D\):

```text
S = domain_scalar("Quantum_Optics")         # D=11, observed=True, C=π/e
computed, err% = fsot_scaled(m, "Quantum_Optics")
```

Seed-closed handles already in the engine:

| Handle | Form | Use |
|--------|------|-----|
| Ice ordinary-ray \(n\) | \(\varphi^2/2\) | solid-water optical fold |
| Wave vs photon | \(\lvert S_{\mathrm{opt}}/S_{\mathrm{qo}}\rvert\) vs 1 | adjacent D=10/11, **same** \(C\) |
| Wave vs bulk | CRC \(n_D\) on Optics, density on Materials | same specimen, two zooms |
| Same-\(D\) look-split | \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) vs \(\lvert S_{\mathrm{PhysChem}}/S_{\mathrm{Chem}}\rvert\) | 0.5/0.6 observer fold at two rungs; vs 1 is the wrong object |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. CRC \(n_D\) on both light folds is the tight scalar. \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) vs 1 is **retired** (wrong object). Fold it onto the Physical_Chemistry/Chemistry look-split.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| \(n_D\) ugly | Check sodium-D (~589 nm), not a fitted Sellmeier at another λ | A new Cauchy \(B\) |
| Static \(\varepsilon_r\) ugly | That is the EM/orientational interface, not optical \(n^2\) | Stuff water \(\varepsilon\sim 80\) as \(n^2\) |
| \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) ~18% vs 1 | Fold onto PhysChem/Chem (same 0.5/0.6 look). Keep n/ρ dual-route | Stuff into 0.5%; retune \(C\) or \(\delta\psi\) |
| Photon residual ugly | Route the same \(n\) on Quantum_Optics, not a new \(D_{\mathrm{eff}}\) | A free \(\hbar\) coefficient |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: a fitted Sellmeier, stuffing the Materials \(C\)-split, or retuning \(C=\pi/e\).
