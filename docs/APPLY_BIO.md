# APPLY cookbook — Biology fold

**Pin:** D1D38A · **core:** `Biology` · \(D_{\mathrm{eff}}=12\) · `observed=False` (**dark** — do not flip) · \(C=\ln\varphi/\sqrt{2}\) · \(\delta\psi=0.08\).  
**Neighbor:** `Biochemistry` \(D=13\), `observed=True`, **same \(C\)**, \(\delta\psi=0.35\).  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §12.  
**Not this tissue:** Genetics product 0.13 Å (sibling freeze). ChemLink already quotes that.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Human mt protein-gene length | NCBI NC_012920.1 | A clock-time expression peak |
| Free amino-acid MW | CRC / IUPAC | Genetics Å / AF RMSD |

Wrong object: \(|S_{\mathrm{bio}}|/|S_{\mathrm{bc}}|\) vs 1 on the live scalars (~45%). That mixes dark vs observed, \(\delta\psi=0.08\) vs \(0.35\), and hits.

---

## 2. Pick the interface

Biology is the **organism** zoom (dark — looking at the fold flips identity, same rule as QC). Biochemistry is the **molecule** zoom (observed). Same \(C\). Do **not** set `observed=True` on Biology.

---

## 3. Route

```text
S = domain_scalar("Biology")              # D=12, dark
computed, err% = fsot_scaled(m, "Biology")
```

Molecule zoom of the same readout:

```text
S = domain_scalar("Biochemistry")         # D=13, observed
computed, err% = fsot_scaled(m, "Biochemistry")
```

Adjacent-rung test **equalizes the dark look** (do not flip Biology):

```text
|S(D=12, δψ=0.08, dark)| / |S(D=13, δψ=0.08, dark)|  vs  1
```

---

## 4. Green gate

Domain **median** ≤ **0.5%**. Same-look dark \(D=12/13\) vs 1 is the tight scalar. Live mixed vs 1 stays **retired**. Genetics 0.13 Å is **not** a row here.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live \(S\) ratio ~45% vs 1 | Equalize dark look; score the \(D\)-step | Flip Biology `observed`; stuff \(\varphi\) or \(3/2\) |
| Å residual | That is Genetics product / no-map | Quote 0.13 Å as this tissue |
| Operon length ugly | NCBI NC_012920.1 protein genes | A fitted codon table |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: flipping Biology dark; stuffing the mixed vs 1; cross-citing Genetics 0.13 Å as sequence-only.
