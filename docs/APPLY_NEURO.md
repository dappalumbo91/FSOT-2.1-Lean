# APPLY cookbook — Neuroscience fold

**Pin:** D1D38A · **core:** `Neuroscience` · \(D_{\mathrm{eff}}=14\) · `observed=True` · \(C=C_{\mathrm{factor}}\) · \(\delta\psi=0.7\) · hits=1.  
**Neighbor:** `Biochemistry` \(D=13\) (molecule zoom). Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §20.  
**Same rung:** `Condensed_Matter` \(\delta\psi=0.5\) (solid). Fold 0.5/0.7 onto \(D=13\).  
**Social tank:** `Economics` \(D=20\) (same World Bank YoY; as-above-so-below).  
**Observer:** 20 W is TISSUE-OBSERVER, not Psychology watts.  
**General protocol:** [`APPLY.md`](APPLY.md).

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Transmitter amino-acid MW | CRC / IUPAC (Gly, Asp, Glu, Tyr, Trp, His) | Invented brain watts |
| Observer load | 20.003601 vs 20.0 W | Psychology Cronbach \(\alpha\) |
| Market YoY | World Bank (dual-route, social tank) | A fitted neural coupling |

Wrong object: \(\lvert S_{\mathrm{cm}}/S_{\mathrm{neuro}}\rvert\) vs 1. Same \(D=14\); \(\delta\psi=0.5\) vs \(0.7\) (solid vs signaling). Fold onto \(D=13\). Genetics 0.13 Å is **not** this tissue.

---

## 2. Pick the interface

Neuroscience is the **signaling** zoom (observer string on, hits=1). Biochemistry is the **molecule** zoom of the transmitter. Condensed_Matter is the **solid** look at the same rung. Economics is the **social tank** of the same fluid, not a different medium.

Do **not** invent watts. Consciousness 20 W is the observer-string readout, not a psychometric scale.

---

## 3. Route

```text
S = domain_scalar("Neuroscience")          # D=14, δψ=0.7, hits=1
computed, err% = fsot_scaled(m, "Neuroscience")
```

Molecule zoom of the same transmitter AA:

```text
S = domain_scalar("Biochemistry")          # D=13, δψ=0.35
computed, err% = fsot_scaled(m, "Biochemistry")
```

Look-split vs solid **folds onto \(D=13\)**:

```text
|S_CM|/|S_Neuro|  vs  S(D=13, δψ=0.5, hits=0)/S(D=13, δψ=0.7, hits=1)
```

| Handle | Form | Use |
|--------|------|-----|
| Transmitter AA | CRC MW on Neuro and Biochem | signaling vs molecule |
| Solid vs signaling | look-split onto \(D=13\) | CRC metal \(\rho\) vs AA |
| Social tank | same World Bank YoY | Economics dual-route; siloed 0.129% not retuned |
| Observer | \(C_{\mathrm{factor}}\) string | 20 W; not Psychology |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. Transmitter AA dual-route is the tight scalar. CM–Neuro look-split is the intended named object (under 0.5%). Live vs 1 stays **retired**. D9 T1 leftover at \(D=13\) is the closed form for that ~0.4% ratio.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live CM/Neuro vs 1 | Fold 0.5/0.7 onto \(D=13\) | Stuff \(\sqrt{\varphi}\); invent watts |
| 20 W ugly | Observer tissue, not this dual-route | Psychology \(\alpha\) as watts |
| Å residual | Genetics product (sibling) | Quote 0.13 Å as signaling |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: invented watts; stuffing vs 1; retuning \(\delta\psi=0.7\); flipping a dark neighbor.
