# APPLY cookbook — Nuclear_Physics fold

**Pin:** D1D38A · **core:** `Nuclear_Physics` · \(D_{\mathrm{eff}}=15\) · `observed=True` · \(C=\alpha/\varphi\) · \(\delta\psi=1\) · hits=1.  
**Far zoom:** `Particle_Physics` \(D=5\) (same orifice, two compactification ends). Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §4.  
**Same rung:** `Thermodynamics` \(\delta\psi=0.9\) (heat). Fold 1/0.9 onto \(D=14\).  
**Neighbor:** `Condensed_Matter` \(D=14\) (lattice; Fe is the shared class).  
**General protocol:** [`APPLY.md`](APPLY.md).

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Level energy (keV) | IAEA/ENDF (He, C, O, Si, Al, Fe) | A fitted Yukawa |
| Fe as shared class | ENDF Fe + CRC Fe density | A per-nuclide \(\varepsilon\) |

Wrong object: \(\lvert S_{\mathrm{nuc}}/S_{\mathrm{thermo}}\rvert\) vs 1. Same \(D=15\); the split is \(\delta\psi=1\) vs \(0.9\) (orifice vs heat). Fold onto \(D=14\).

---

## 2. Pick the interface

Nuclear is the **orifice** zoom (level energies). Particle is the **puncture** zoom of the same valve at \(D=5\). Thermo is the **heat** look at the same \(D=15\). \(C\) does not enter \(S\).

If a residual is ugly, the usual miss is **mixing the look with the rung**, or stuffing dark-matter into FRB puncture energy — not a missing coupling.

---

## 3. Route

```text
S = domain_scalar("Nuclear_Physics")       # D=15, δψ=1, orifice
computed, err% = fsot_scaled(m, "Nuclear_Physics")
```

Particle zoom of the same keV:

```text
S = domain_scalar("Particle_Physics")      # D=5
computed, err% = fsot_scaled(m, "Particle_Physics")
```

Look-split vs heat **folds onto \(D=14\)**:

```text
|S_nuc|/|S_thermo|  vs  S(D=14, δψ=1, hits=1)/S(D=14, δψ=0.9, hits=1)
```

| Handle | Form | Use |
|--------|------|-----|
| ENDF dual-route | same keV on Nuclear and Particle | two zooms of one orifice |
| Orifice vs heat | look-split onto \(D=14\) | ENDF + Carnot |
| Lattice vs orifice | same-look \(D=14/15\) at \(\delta\psi=0.5\) | CRC Fe \(\rho\) + ENDF Fe |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. ENDF dual-route is the tight scalar (nuclear ~0.046%, particle ~0.010%). Live vs 1 stays **retired**. D9 T1 leftover at the \(D=14\) look-split is the closed form for the remaining ~0.4% named ratio.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live \(S\) vs Thermo ~ugly | Fold 1/0.9 onto \(D=14\) | Stuff \(\varphi/2\); a new Yukawa |
| keV ugly | Check IAEA/ENDF level, not a Q-value mix | A per-channel \(\varepsilon\) |
| FRB energy ugly | Orifice outgassing (PRED/FRB docs) | Dark matter in the puncture |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: stuffing vs 1; a fitted coupling; retuning \(\delta\psi=1\).
