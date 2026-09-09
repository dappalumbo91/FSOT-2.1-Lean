# APPLY cookbook — Acoustics fold

**Pin:** D1D38A · **core:** `Acoustics` · \(D_{\mathrm{eff}}=10\) · `observed=True` · \(C=A_{\mathrm{bleed}}/\sqrt{2}\) · \(\delta\psi=0.3\).  
**Same rung:** `Optics` \(\delta\psi=0.6\) (light); `Materials_Science` \(\delta\psi=0.5\) (bulk).  
**Crustal zoom:** `Seismology` \(D=18\), dark. Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §1.  
**General protocol:** [`APPLY.md`](APPLY.md). Lab sound is the T3 standing wave; PREM is the same wave in the lid.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Longitudinal \(c\) (m/s) | CRC / ISO 20 °C (water, ice, silica, ethanol, NaCl) | A fitted \(c(T)\) polynomial as a new law |
| \(c_{\mathrm{water}}/c_{\mathrm{air}}\) | CRC/ISO 20 °C 1482.4 / 343.2 | A new viscosity coefficient |
| Crustal \(v_P/v_S\) | PREM lid/Moho + basalt/gabbro | A clock-time hypocenter |

Wrong object: \(\lvert S_{\mathrm{ac}}/S_{\mathrm{opt}}\rvert\) vs 1 (~24%). That is \(\delta\psi=0.3\) vs \(0.6\) at the same \(D=10\). Fold onto \(D=9\).

---

## 2. Pick the interface

Acoustics is the **lab-sound** zoom of the T3 standing wave. Seismology is the **crustal-wave** zoom (dark). Optics is the **light** look at the same rung. Materials is the **bulk** look.

If a residual is ugly, the usual miss is **wrong fold** (density as sound, or granite as the mafic Poisson solid) — not a missing spring.

---

## 3. Route

```text
S = domain_scalar("Acoustics")             # D=10, δψ=0.3
computed, err% = fsot_scaled(m, "Acoustics")
```

Crustal zoom of the same wave (do **not** flip Seismology observed):

```text
S = domain_scalar("Seismology")            # D=18, dark
computed, err% = fsot_scaled(vp_over_vs, "Seismology")
```

Look-split vs light **folds onto \(D=9\)**:

```text
|S_ac|/|S_opt|  vs  S(D=9, δψ=0.3)/S(D=9, δψ=0.6)
```

| Handle | Form | Use |
|--------|------|-----|
| Poisson of the mafic solid | \(\nu=D_{\mathrm{atomic}}/25=0.28\) | \(v_P/v_S\) vs PREM lid |
| Two viscosities | \(c_{\mathrm{water}}/c_{\mathrm{air}}=e+\varphi\) | CRC/ISO 20 °C |
| Sound vs light | look-split onto \(D=9\) | CRC \(c\) vs \(n_D\) |
| Sound vs bulk | look-split 0.3/0.5 onto \(D=9\) | CRC \(c\) vs \(\rho\) |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. CRC \(c\) dual-route is the tight scalar. Lithosphere \(v_P/v_S\) is the crustal tight scalar. Live vs 1 stays **retired**. Water/air \(e+\varphi\) is a **named seed** (under 0.5%) — do not retune it.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live \(S\) vs 1 ~24% | Fold 0.3/0.6 onto \(D=9\) | Stuff \(\sqrt{\varphi}\) |
| Crustal \(v_P/v_S\) ugly | Mafic/lid, not granite/sandstone | Fit a new Poisson |
| Water/air ~0.4% | Named \(e+\varphi\) object; leave it | A new viscosity \(f\) |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: a fitted \(c(T)\); stuffing vs 1; retuning \(\delta\psi=0.3\).
