# APPLY cookbook — Electromagnetism fold

**Pin:** D1D38A · **core:** `Electromagnetism` · \(D_{\mathrm{eff}}=9\) · `observed=True` · \(C=e/\pi\) · \(\delta\psi=0.7\).  
**Neighbor:** `Optics` \(D=10\), \(C=\pi/e\), \(\delta\psi=0.6\) (wave readout). \(C_{\mathrm{em}}C_{\mathrm{opt}}=1\).  
**Tissue:** [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §11.  
**General protocol:** [`APPLY.md`](APPLY.md). CRC \(n_D\) specimens are the table (same list as Materials↔Optics).

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Sodium-D index \(n_D\) | CRC / NIST ~589 nm | A fitted Sellmeier \(B\) |
| Optical permittivity \(\varepsilon_{\mathrm{opt}}=n^2\) | Maxwell, non-magnetic | Static \(\varepsilon_r\) (water ~80 is orientational, not \(n^2\)) |
| Ice Ih \(\varepsilon_{\mathrm{opt}}\) | \(n_o=1.309\), \(\varepsilon=n^2\) vs \((\varphi^2/2)^2\) | Air \(n-1\) |

Wrong object: \(|S_{\mathrm{EM}}|/|S_{\mathrm{opt}}|\) vs 1 on the **live** scalars. That mixes the \(D=9/10\) step with \(\delta\psi=0.7\) vs \(0.6\). Do not stuff \(\sqrt{\varphi}\) onto that mix.

---

## 2. Pick the interface

Electromagnetism is the **source** zoom of light. Optics is the **readout** zoom (\(n\)). Same light, inverse \(C\). If a residual is ugly, the usual miss is static \(\varepsilon_r\) as optical \(n^2\), or mixing the look with the rung.

---

## 3. Route

```text
S = domain_scalar("Electromagnetism")     # D=9, δψ=0.7, source look
computed, err% = fsot_scaled(m, "Electromagnetism")
```

Wave readout of the same specimen:

```text
S = domain_scalar("Optics")               # D=10, δψ=0.6
computed, err% = fsot_scaled(n, "Optics")
computed, err% = fsot_scaled(n*n, "Electromagnetism")   # ε_opt
```

Adjacent-rung test **equalizes the look** at the optical readout (\(\delta\psi=0.6\)):

```text
|S(D=9, δψ=0.6)| / |S(D=10, δψ=0.6)|  vs  1
```

| Handle | Form | Use |
|--------|------|-----|
| Maxwell | \(\varepsilon_{\mathrm{opt}}=n^2\) | CRC \(n_D\) on Optics, \(n^2\) on EM |
| Ice permittivity | \(n^2\) vs \((\varphi^2/2)^2\) | solid-water optical fold |
| Same-look rung | \(\lvert S_{D=9}/S_{D=10}\rvert\) at \(\delta\psi=0.6\) vs 1 | compactification 9→10 |
| Inverse \(C\) | \(C_{\mathrm{em}}C_{\mathrm{opt}}=1\) | source vs readout grammar |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. Same-look \(D=9/10\) vs 1 is the tight scalar. Live mixed \(|S|\) vs 1 stays **retired**. Static water \(\varepsilon\sim 80\) is **structural** (another interface).

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| Live \(S\) ratio ~27% vs 1 | Equalize \(\delta\psi\); score the \(D\)-step | Stuff \(\sqrt{\varphi}\) |
| Static \(\varepsilon_r\) ugly | EM/orientational interface, not optical \(n^2\) | Stuff water 80 as \(n^2\) |
| \(n_D\) ugly | Sodium-D ~589 nm | A new Cauchy \(B\) |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: stuffing the mixed vs 1; static \(\varepsilon\) as \(n^2\); retuning \(C=e/\pi\).
