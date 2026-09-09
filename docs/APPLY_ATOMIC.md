# APPLY cookbook — Atomic_Physics fold

**Pin:** D1D38A · **core:** `Atomic_Physics` · \(D_{\mathrm{eff}}=7\) · `observed=True` · \(C=e/\pi\) · \(\delta\psi=0.85\).  
**Neighbor:** `Quantum_Mechanics` \(D=6\), \(C=\gamma/\varphi\), \(\delta\psi=1\) (free-orbit look, same as Particle).  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §10.  
**General protocol:** [`APPLY.md`](APPLY.md). Hydrogen is the specimen for \(a_0\) and \(R_\infty\) (one atom, three readouts). First-ionization dual-route is the engine table **H–Ca (Z=1–20)**. Z=21–118 already lives on the Atomic/periodic panel — that is the Atomic fold in isolation, not this QM tissue.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| H first ionization | NIST 13.598 eV | A fitted Rydberg \(R\) per element |
| Bohr radius \(a_0\) | CODATA 0.529177 Å | A new \(\hbar\) |
| Rydberg \(R_\infty\) | CODATA 10973731.568157 m⁻¹ | Stuffing \(E=hcR\) as a second 0.5% central of IE |

Wrong object: \(|S_{\mathrm{QM}}|/|S_{\mathrm{atomic}}|\) vs 1 on the **live** scalars. That mixes the \(D=6/7\) step with the \(\delta\psi=1\) vs \(0.85\) look (free orbit vs bound well).

---

## 2. Pick the interface

Quantum_Mechanics is the **orbit** zoom (unbound look, \(\delta\psi=1\)). Atomic_Physics is the **bound well** zoom (\(\delta\psi=0.85\)). Same compactification step as Particle \(D=5\) → QM \(D=6\) → atom \(D=7\). \(C\) does not enter \(S\).

If a residual is ugly, the usual miss is **mixing the look with the rung** — not a missing fine-structure coefficient.

---

## 3. Route

```text
S = domain_scalar("Atomic_Physics")       # D=7, δψ=0.85, bound look
computed, err% = fsot_scaled(m, "Atomic_Physics")
```

Orbit zoom of the same hydrogen readout:

```text
S = domain_scalar("Quantum_Mechanics")    # D=6, δψ=1, free look
computed, err% = fsot_scaled(m, "Quantum_Mechanics")
```

Adjacent-rung test **equalizes the look** (\(\delta\psi=1\)):

```text
|S(D=6, δψ=1)| / |S(D=7, δψ=1)|  vs  1
```

Seed-closed handles already in the engine:

| Handle | Form | Use |
|--------|------|-----|
| H ionization | \(\gamma^{-5}-G^{-8}\) vs 13.598 eV | bound-well seed |
| Same-look rung | \(\lvert S_{D=6}/S_{D=7}\rvert\) at \(\delta\psi=1\) vs 1 | compactification 6→7 |
| Hydrogen dual-route | IE, \(a_0\), \(R_\infty\) on both folds | orbit vs well |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. Same-look \(D=6/7\) vs 1 is the tight scalar. Live mixed \(|S_{\mathrm{QM}}|/|S_{\mathrm{atomic}}|\) vs 1 stays **retired** (~30%, look+rung mixed). Do not stuff \(\sqrt{e/\varphi}\) onto that mixed residual.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live \(S\) ratio ~30% vs 1 | Equalize \(\delta\psi\); score the \(D\)-step | Stuff \(\sqrt{e/\varphi}\) or \(13/10\) |
| IE ugly | Check NIST first ionization, not a fitted \(R(Z)\) | A new Rydberg per element |
| \(a_0\) vs \(R_\infty\) disagree | They are \(E=hcR\); one hydrogen, two readouts | A free \(\hbar\) |
| \(\delta\psi=0.85\) looks off | Bound-well look; do not retune to \(e/\pi\) | Rewrite DomainConfig |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: stuffing the mixed vs 1; retuning Atomic \(\delta\psi\); a fitted Rydberg slope.
