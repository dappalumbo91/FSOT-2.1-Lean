# APPLY cookbook — Chemistry ladder (composition / thermo / molecule)

**Pin:** live SHA of `vendor/fsot_compute.py` · **cores:** `Chemistry` nest \(D=6\), `Physical_Chemistry` nest \(D=6\), `Molecular_Chemistry` nest \(D=7\). All look \(1\), hits \(0\), `observed=True`. \(C\) does not enter \(S\).  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §14–15, 22–23.  
**Same generation as Atomic/HEP** (\(D=6\)); those two are the remaining look-split (bound well vs collision). Chemistry and PhysChem are the **same** default-look specimen — live \(S\) is identical.  
**General protocol:** [`APPLY.md`](APPLY.md). One CRC table family. Assigned \(\delta\psi=0.5/0.6\) is retired.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Molecular weight | CRC / IUPAC (water, methanol, ethanol, acetone, acetic acid, hexane, benzene, toluene, NaCl) | A fitted group-additivity \(B\) |
| Melting / boiling \(T\) | CRC \(T_m\), \(T_b\) | A per-species Trouton constant |
| Density | CRC \(\rho\) | Optical \(n_D\) (that is Optics) |

Wrong object: \(\lvert S_{\mathrm{chem}}/S_{\mathrm{pc}}\rvert\) vs 1 on the *old assigned looks*. Live they share nest \(D=6\) and look \(1\), so that ratio is an identity. Do not gate it. Scoring \(n_D\) as MW is still the wrong fold.

---

## 2. Pick the interface

Chemistry is the **composition** look. Physical_Chemistry is the **thermo** look of the same rung. Molecular_Chemistry is the **molecule** zoom (one compactification step, already sharing PhysChem’s \(\delta\psi=0.5\)).

If a residual is ugly, the usual miss is **scoring \(n_D\) or ionization as MW**, or stuffing the 0.5/0.6 split vs 1.

---

## 3. Route

```text
S = domain_scalar("Chemistry")             # nest D=6, look=1, composition
computed, err% = fsot_scaled(MW, "Chemistry")

S = domain_scalar("Physical_Chemistry")    # nest D=6, look=1, thermo (same S as Chemistry)
computed, err% = fsot_scaled(Tm, "Physical_Chemistry")

S = domain_scalar("Molecular_Chemistry")   # nest D=7, look=1, molecule
computed, err% = fsot_scaled(MW, "Molecular_Chemistry")
```

Composition vs thermo (same 0.5/0.6 as Materials/Optics):

```text
|S_PhysChem|/|S_Chem|  vs  |S_mat|/|S_opt|
```

Composition vs molecule, **equalize the chemistry look**:

```text
|S(D=8, δψ=0.6)| / |S(D=9, δψ=0.6)|  vs  1
```

| Handle | Form | Use |
|--------|------|-----|
| CRC dual-route | \(\rho\)/MW on Chemistry; \(T_m\)/\(T_b\) on PhysChem; MW on Mol | one specimen, three zooms |
| Look-split | vs Materials/Optics | 0.5/0.6 at two rungs; vs 1 retired |
| Matched-look rung | PhysChem–Mol live \(\lvert S\rvert\) vs 1 | already share \(\delta\psi=0.5\) |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. CRC dual-route is the tight scalar. Look-split vs Materials/Optics is the intended named object (under 0.5%). Live vs 1 stays **retired**. D9 T1 leftover is the closed form for the live view.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live Chem/PC ~22% vs 1 | Fold onto Materials/Optics | Identity-pad equalized \(\delta\psi\) at \(D=8\) |
| \(n_D\) on this fold | Route \(n\) on Optics | A new Cauchy on Chemistry |
| IE on this fold | Route on Atomic / HEP | A fitted Rydberg per molecule |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: stuffing vs 1; a fitted Trouton; retuning \(\delta\psi\).
