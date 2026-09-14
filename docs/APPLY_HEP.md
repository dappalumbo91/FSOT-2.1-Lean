# APPLY cookbook — High_Energy_Physics fold

**Pin:** live SHA of `vendor/fsot_compute.py` · **core:** `High_Energy_Physics` · nest \(D=6\) · `observed=True` · look \(1-\mathrm{POOF}/\pi\) · hits \(=1\). \(C\) does not enter \(S\).  
**Neighbor:** `Atomic_Physics` nest \(D=6\), look \(e/\pi\), hits \(0\). **Same compactification generation — this is the remaining live look-split.**  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §13.  
**General protocol:** [`APPLY.md`](APPLY.md).

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Electron / proton mass | CODATA | A fitted Yukawa |
| H first ionization | NIST 13.598 eV | A per-channel \(\varepsilon\) at the LHC |

Wrong object: \(|S_{\mathrm{atomic}}|/|S_{\mathrm{HEP}}|\) vs 1. Same nest \(D=6\); the split is bound well \(e/\pi\) vs collision \(1-\mathrm{POOF}/\pi\) with one hit. Equalizing look at the same \(D\) is an identity pad — do not gate that.

---

## 2. Pick the interface

Atomic is the **bound well**. HEP is the **collision** look of the same nest \(D=6\) lepton/baryon. \(C\) does not enter \(S\).

---

## 3. Route

```text
S = domain_scalar("High_Energy_Physics")
computed, err% = fsot_scaled(m, "High_Energy_Physics")
```

Bound-well zoom of the same mass:

```text
S = domain_scalar("Atomic_Physics")
computed, err% = fsot_scaled(m, "Atomic_Physics")
```

Look-split test **folds onto the adjacent QM rung** (same 0.85/0.95, \(D=6\)):

```text
|S_Atomic|/|S_HEP|  vs  S(D=6, δψ=0.85)/S(D=6, δψ=0.95)
```

---

## 4. Green gate

Domain **median** ≤ **0.5%**. Look-split vs QM rung is the tight scalar. Live vs 1 stays **retired**.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live \(S\) ratio ~17% vs 1 | Fold onto QM 0.85/0.95 | Stuff \(\varphi/2\); identity-pad equalized \(\delta\psi\) at \(D=7\) |
| Mass residual ugly | CODATA \(m_e\), \(m_p\) | A new Yukawa |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: stuffing vs 1; a fitted coupling; retuning \(\delta\psi\).
