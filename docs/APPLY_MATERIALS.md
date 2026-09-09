# APPLY cookbook — Materials_Science fold

**Pin:** D1D38A · **core:** `Materials_Science` · \(D_{\mathrm{eff}}=10\) · `observed=True` · \(C=A_{\mathrm{in}}/e\) · \(\delta\psi=0.5\).  
**Same rung, other \(C\):** `Optics` \(D=10\), \(C=\pi/e\), \(\delta\psi=0.6\) (light look). Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §8.  
**Same rung, lab sound:** `Acoustics` \(D=10\), \(\delta\psi=0.3\). Tissue: §17.  
**Neighbor:** `Electromagnetism` \(D=9\) (field zoom). Tissue: §19.  
**General protocol:** [`APPLY.md`](APPLY.md). This is the bulk / density fold of the same specimen Optics reads as \(n_D\).

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Density \(\rho\) (g/cm³) | CRC handbook (water, ice, silica, NaCl, metals) | A fitted equation of state |
| Ice Ih density | CRC \(0.917\) | Ice optical \(n\) (that is Optics) |
| Metal density (Al, Cu, Fe, Au, Ag, Pb) | CRC | Static electrical conductivity |

Wrong object: \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) vs 1 (~18%). That is two looks at one rung (body \(\delta\psi=0.5\) vs light \(\delta\psi=0.6\)). Fold onto Physical_Chemistry/Chemistry. Static metal conductivity is another interface.

---

## 2. Pick the interface

Materials is the **bulk / mass** zoom. Optics is the **wave** zoom of the same specimen. Acoustics is the **lab-sound** zoom. \(C\) does not enter \(S\).

If a residual is ugly, the usual miss is **wrong fold** (scoring \(n_D\) on Materials, or conductivity as density) — not a missing bulk modulus.

---

## 3. Route

```text
S = domain_scalar("Materials_Science")     # D=10, δψ=0.5, body look
computed, err% = fsot_scaled(m, "Materials_Science")
```

Light zoom of the same CRC specimen:

```text
S = domain_scalar("Optics")                # D=10, δψ=0.6
computed, err% = fsot_scaled(n, "Optics")
```

Look-split test **folds onto the chemistry rung** (same 0.5/0.6):

```text
|S_mat|/|S_opt|  vs  |S_PhysChem|/|S_Chem|
```

| Handle | Form | Use |
|--------|------|-----|
| Density dual-route | CRC \(\rho\) on Materials | bulk of the optical specimen |
| Ice \(n\) | \(\varphi^2/2\) on Optics | solid-water optical fold, not this \(C\) |
| Same-\(D\) look-split | vs PhysChem/Chem | 0.5/0.6 body vs light; vs 1 is the wrong object |
| Sound vs bulk | CRC \(c\) on Acoustics, \(\rho\) on Materials | fold 0.3/0.5 onto \(D=9\) |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. CRC density is the tight scalar. \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) vs 1 stays **retired**. The named look-split vs PhysChem/Chem is the intended object (under 0.5%). D9: T1 leftover at both rungs is the closed form; do not stuff the ~18%.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) ~18% vs 1 | Fold onto PhysChem/Chem | Stuff into 0.5%; retune \(C\) or \(\delta\psi\) |
| Conductivity ugly | That is the EM/transport interface | Stuff \(\sigma\) as \(\rho\) |
| \(n_D\) ugly on this fold | Route \(n\) on **Optics** | A new Cauchy \(B\) on Materials |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: stuffing the mixed vs 1; retuning \(C=A_{\mathrm{in}}/e\); a fitted EOS.
