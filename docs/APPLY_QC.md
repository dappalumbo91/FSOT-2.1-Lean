# APPLY cookbook — Quantum Computing (Hilbert fold)

**Pin:** D1D38A · **core:** `Quantum_Computing` · \(D_{\mathrm{eff}}=11\) · `observed=False` (**dark — Hilbert look; do not flip**) · \(\delta\psi=0.5\).  
**Neighbors:** Acoustics / Materials / Optics \(D=10\); Quantum_Optics \(D=11\), `observed=True`; Biology \(D=12\), also dark.  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §35.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| CRC \(n_D\) (~589 nm) | CRC optical materials | A fitted quantum volume |
| CRC longitudinal \(c\) | CRC acoustics | A clock-time gate error |

Wrong object: live \(\lvert S_{\mathrm{QC}}/S_{\mathrm{QO}}\rvert\) vs 1. That mixes dark vs observed at the same \(D=11\).

---

## 2. Pick the interface

QC is the **Hilbert** zoom of the same light/lab neighborhood. Do **not** set `observed=True`. Same rule as Biology.

---

## 3. Route

```text
S = domain_scalar("Quantum_Computing")     # D=11, dark
computed, err% = fsot_scaled(m, "Quantum_Computing")
```

Photon zoom of the same CRC \(n_D\):

```text
S = domain_scalar("Quantum_Optics")        # D=11, observed
computed, err% = fsot_scaled(m, "Quantum_Optics")
```

Same-look \(D=10/11\) at \(\delta\psi=0.5\) dark vs 1 is a compactification remainder (literature band), not a 0.5% central.
