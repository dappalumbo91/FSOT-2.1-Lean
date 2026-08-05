# FSOT mathematician / scientist how-to

**Purpose:** Enough structure for a mathematician or scientific auditor to **reconstruct**, **verify**, and **simulate** the FSOT scalar engine and its domain interfaces without folklore.  
**Companion machine dumps:**  
- [`data/fsot_system_math_audit.json`](../data/fsot_system_math_audit.json) — seeds, layers, 35 domains, consistency  
- [`data/fsot_building_block_hierarchy.json`](../data/fsot_building_block_hierarchy.json) — nodes/edges for hierarchical simulation  
- [`data/fsot_domain_formula_network.json`](../data/fsot_domain_formula_network.json) — domain–domain and seed–domain strings  
- [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) — narrative key  
- [`FSOT_SYSTEM_MATH_AUDIT.md`](FSOT_SYSTEM_MATH_AUDIT.md) — live S table  

**Authority:** `vendor/fsot_compute.py` pin D1D38A · regenerate audit:  
`python scripts/build_fsot_system_math_audit.py`

---

## 0. Ontology (do not substitute textbook frames)

FSOT is **one fluid spacetime continuum** with effective dimension \(D_{\mathrm{eff}}\) and compactification ceiling **25**.  

| Claim | Status in-repo |
|-------|----------------|
| Fluid medium across scales | Load-bearing reality (T2 dynamics + \(C_{\mathrm{eff}}\), valves) |
| Absolute rest frame | Fiction (damps under calibration) |
| Domains as separate theories | **False** — domains are **interfaces** into the same \(S\) |
| Free parameters per domain | **Zero** — only preregistered \((D_{\mathrm{eff}},\mathrm{hits},\delta\psi,\delta\theta,\mathrm{observed})\) |

---

## 1. Algebraic hierarchy (building blocks)

```
L0  Seeds:  π, e, φ, γ, G_Catalan
      ↓  closed form only
L1  Primary derived:  α, ψ_con, η_eff, β, γ_c, Ω, θ_S, Poof
      ↓
L2  Composite:  C_eff, A_bleed, P_var, B_in, A_in, Suction, Chaos,
                P_base, P_new, C_factor, K, C_cosm
      ↓
L3  Formula branches:  T1 (observer base), T2 (linear), T3 (valve–acoustic–phase)
      ↓
L4  Scalar:  S = K · (T1 + T2 + T3)
      ↓
L5a Core domain interfaces (35): DomainConfig → S
L5b Extension interfaces (~371): same ScalarInput from extension_domains_manifest
      ↓  (total ~406 formula interfaces — not core-only)
L6  Residual law:  c = m · (1 + |S| · f)   [f from core / nearest-core inheritance]
L7  Empirical gate:  pooled median ε ≤ 0.5%  (~470 green benchmark panels)
```

**Simulation reading:** L0–L4 is the universal syntax; L5a/L5b choose dimensional folds across the **full expansion**; L6–L7 attach measurement.  
Do **not** stop at 35 — the expansion atlas is first-class.  
Edges: `fsot_building_block_hierarchy.json` · panels: `fsot_domain_formula_network.json`.

---

## 2. Exact master formulas

### 2.1 Seeds (L0)

| Symbol | Definition |
|--------|------------|
| \(\pi\) | circle constant |
| \(e\) | \(\exp 1\) |
| \(\varphi\) | \((1+\sqrt{5})/2\) |
| \(\gamma\) | Euler–Mascheroni |
| \(G\) | Catalan |

### 2.2 Layer 1 (selected)

\[
\begin{aligned}
\alpha &= \frac{\ln\pi}{e\,\varphi^{13}}, &
\psi_{\mathrm{con}} &= 1-e^{-1}, &
\eta_{\mathrm{eff}} &= \frac{1}{\pi-1}, \\
\beta &= \exp\!\bigl(-(\pi^{\pi}+e-1)\bigr), &
\gamma_c &= -\frac{\ln 2}{\varphi}, &
\Omega &= \sin(\pi/e)\,\sqrt{2}, \\
\theta_S &= \sin(\psi_{\mathrm{con}}\eta_{\mathrm{eff}}), &
\mathrm{Poof} &= \exp\!\left(\frac{-\ln\pi/e}{\eta_{\mathrm{eff}}\ln\varphi}\right).
\end{aligned}
\]

### 2.3 Layer 2 (selected)

\[
\begin{aligned}
C_{\mathrm{eff}} &= (1-\mathrm{Poof}\sin\theta_S)\Bigl(1+0.01\frac{G}{\pi\varphi}\Bigr), \\
A_{\mathrm{bleed}} &= \sin(\pi/e)\,\varphi/\sqrt{2}, \\
\mathrm{Suction} &= \mathrm{Poof}\,(-\cos(\theta_S-\pi)), \\
\mathrm{Chaos} &= \gamma_c/\Omega, \\
\mathbf{C}_{\mathrm{factor}} &= C_{\mathrm{eff}}\,P_{\mathrm{new}}, \quad
P_{\mathrm{new}}=(\gamma/e)\sqrt{2}, \\
K &= \varphi\cdot(\gamma/e)\cdot\sqrt{2}/\ln\pi\cdot 0.99.
\end{aligned}
\]

### 2.4 Scalar branches

**T1 — observer-modulated base**

\[
\begin{aligned}
\mathrm{growth} &= \exp\!\bigl(\alpha(1-h/N)\gamma/\varphi\bigr), \\
\mathrm{base} &= \frac{NP}{\sqrt{D}}\cos\frac{\psi_{\mathrm{con}}+\delta\psi}{\eta_{\mathrm{eff}}}
  \exp(-\alpha h/N+\rho+B_{\mathrm{in}}\delta\psi)\,(1+\mathrm{growth}\,C_{\mathrm{eff}}), \\
T_1 &= \mathrm{base}\,(1+P_{\mathrm{new}}\ln(D/25)), \\
T_1 &\leftarrow T_1\cdot\exp(\mathbf{C}_{\mathrm{factor}}P_{\mathrm{var}})\cos(\delta\psi+P_{\mathrm{var}})
  \quad\text{if observed}.
\end{aligned}
\]

**T2 — linear**

\[
T_2 = \mathrm{scale}\cdot\mathrm{amplitude} + \mathrm{trend\_bias}.
\]

**T3 — valve–acoustic–phase (fluid heart)**

\[
\begin{aligned}
\mathrm{valve} &= \beta\cos\delta\psi\cdot\frac{NP}{\sqrt{D}}
  \Bigl(1+\mathrm{Chaos}\frac{D-25}{25}\Bigr)
  \bigl(1+\mathrm{Poof}\cos(\theta_S+\pi)+\mathrm{Suction}\sin\theta_S\bigr), \\
\mathrm{acoustic} &= 1+\frac{A_{\mathrm{bleed}}\sin^2\delta\theta}{\varphi}
  +\frac{A_{\mathrm{in}}\cos^2\delta\theta}{\varphi}, \\
\mathrm{phase} &= 1+B_{\mathrm{in}}P_{\mathrm{var}}, \\
T_3 &= \mathrm{valve}\cdot\mathrm{acoustic}\cdot\mathrm{phase}.
\end{aligned}
\]

**Master**

\[
S = K\,(T_1+T_2+T_3).
\]

**Compactification:** \(D=25\) is the ceiling — \(\ln(D/25)\) and \(\mathrm{Chaos}(D-25)/25\) encode folds about that fluid scale.

### 2.5 Residual prediction law

\[
c = m\bigl(1+|S(\mathrm{domain})|\,f_{\mathrm{domain}}\bigr), \qquad
\varepsilon = 100\frac{|c-m|}{\max(|m|,\varepsilon_{\mathrm{floor}})}.
\]

Domain headline = **median** \(\varepsilon\). Green iff median \(\le 0.5\%\).

---

## 3. Domain interfaces (35 cores + full expansion)

### 3.1 Cores (35)

Each core domain is a fixed tuple in `vendor/fsot_compute.py::DOMAINS`:

\[
(\mathrm{name},\, D_{\mathrm{eff}},\, h,\, \delta\psi,\, \delta\theta,\, \mathrm{observed},\, C_{\mathrm{interp}}).
\]

### 3.2 Extensions (~371)

Each extension in `data/extension_domains_manifest.yaml` is the **same** interface shape:

\[
(\mathrm{name},\, D_{\mathrm{eff}},\, \mathrm{recent\_hits},\, \delta\psi,\, \mathrm{observed},\, \ldots)
\]

\(S\) is computed with the same `compute_scalar` / `ScalarInput`. Residual factor \(f\) is inherited from `routes_to_core` or nearest-core `DOMAIN_FACTORS`.

### 3.3 Atlas + green panels

| Source | Role | Count class |
|--------|------|-------------|
| `extension_domains_manifest.yaml` | Extension interfaces | ~371 |
| `publication/domain_atlas.csv` | Publication atlas rows | ~403 |
| `benchmark_margin_audit.json` | Green residual panels | ~470 |

**Live values of \(S\):** `fsot_system_math_audit.json` → `core_domains` + `extension_domains` (full list).

**Sign syntax (emergence vs damping):**

- \(S>0\): emergence class (e.g. Nuclear, Particle, Neuroscience, …)  
- \(S<0\): damping class (e.g. Cosmology at \(D=25\), Fluid_Dynamics, Seismology, …)  

Formal: `FSOT/Theorems.lean` (`nuclear_is_emergence`, `cosmological_is_damping`, …).

---

## 4. How a domain “attaches” to the formula (string model)

For simulation / network analysis, each domain node is connected by:

1. **Seed strings** — every domain depends on all five L0 seeds via L1–L4.  
2. **Shared branch strings** — all domains share T1/T2/T3 algebra; only interface params differ.  
3. **Neighbor strings** — domains with adjacent \(D_{\mathrm{eff}}\), same band, same sign, or same \(f\) (see `fsot_domain_formula_network.json`).  
4. **Residual strings** — \((S,f)\) pairs fix pure residual floor \(\varepsilon_{\mathrm{floor}}=|S|f\cdot 100\).  
5. **Benchmark strings** — green panels attach to core domains via residual routing (`benchmark_margin_audit.json`).

**Hierarchical order of building blocks of reality (as solved here):**  
sort interfaces by \(D_{\mathrm{eff}}\) ascending (micro → cosmology). That ladder is the default **emergence order** exported as `emergence_ladder_by_D_eff` in the hierarchy JSON.

---

## 5. Reproduction protocol (auditor checklist)

### A. Pin and engine

1. Open `vendor/fsot_compute_AUTHORITY_PIN.json` (expect D1D38A class).  
2. Recompute one seed-derived constant (e.g. \(K\), \(\mathrm{Poof}\)) from definitions in §2.  
3. Recompute `domain_scalar("Nuclear_Physics")` and `domain_scalar("Cosmology")`; check signs.

```powershell
python -c "import sys; sys.path.insert(0,'vendor'); from fsot_compute import domain_scalar; print(float(domain_scalar('Nuclear_Physics')), float(domain_scalar('Cosmology')))"
```

### B. Residual law

```powershell
python -c "import sys; sys.path.insert(0,'scripts'); from fsot_api_predict_lib import fsot_scaled; print(fsot_scaled(1.0, 'Planetary_Science'))"
```

Expect \(\varepsilon \approx |S|f\cdot 100\).

### C. System audit consistency

```powershell
python scripts/build_fsot_system_math_audit.py
```

Require `consistency.all_pass == true`.

### D. Empirical envelope

```powershell
python scripts/audit_all_benchmark_margins.py
```

Require green fail count 0 (live N in `CURRENT_STATUS.md`).

### E. Multiprover (optional layer)

- Residual catalog spine: `run_cross_proof_verification.py`  
- Uniqueness research spine: `run_uniqueness_research_verification.py`  
- GR/SM/CKM: `run_gr_sm_ckm_verification.py`  

Provers certify **exported numeric/structural obligations**, not catalog re-ingest.

---

## 6. What is / is not a theorem

| Class | Example | Status |
|-------|---------|--------|
| Engine identity | \(S=K(T_1+T_2+T_3)\) structure | Code + formal modules |
| Residual gate | \(\varepsilon_{\mathrm{med}}<0.5\) | Empirical multiprover export |
| Fluid omni | \(D_{\mathrm{eff}}\le 25\), \(C_{\mathrm{eff}}\) stack | Architectural + dynamics T2 |
| Free-color dampening candidate | \(\gamma_{\mathrm{color}}>0\), attractor suite | Uniqueness research multiprover |
| Classical continuum YM mass-gap | Path-integral uniqueness | **Not claimed**; necessity meta-claim damped under ToE polarity |

---

## 7. Simulation sketch (your next step)

Goal: from seeds + verified domain applications, recover **network strings** and **hierarchical syntax**.

1. Load L0 seeds from audit JSON.  
2. Derive L1/L2 with exact formulas (or trust `fsot_compute` as oracle).  
3. For **each of ~406 interfaces** (35 core + all extensions), evaluate \(S\) and store  
   \((D_{\mathrm{eff}}, h, \delta\psi, \mathrm{observed}, S, f, \mathrm{sign}, \mathrm{kind})\).  
4. Build graph:  
   - seed → **every** domain  
   - extension → core fold edges  
   - domain ↔ domain neighbors from network JSON  
   - **~470 green benchmark panels** as measurement leaves  
5. Rank **all** interfaces by \(D_{\mathrm{eff}}\) → hierarchical building-block order.  
6. Interpret \(\mathrm{sign}(S)\) as local **emergence/damping bit** of reality-syntax.  
7. Optional: free-color / fiction modes as damped leaves (uniqueness + reality/fiction modules).

**Do not** invent new free coefficients in the sim. If a residual fails, re-route \(D_{\mathrm{eff}}\) / domain first (math key mismatch rule).

---

## 8. Related deep tracks

| Track | Entry |
|-------|--------|
| Residual ToE closure | `docs/RESIDUAL_TOE_CLOSURE.md` |
| Uniqueness / dampening | `docs/UNIQUENESS_RESEARCH_SPINE.md` |
| Reality vs fiction calibration | `data/reality_fiction_calibration.json` |
| GR/SM/CKM multiprover | `docs/GR_SM_CKM_MULTIPROVER.md` |
| Claim boundaries | `docs/TOE_CLAIM_BOUNDARIES.md` |

---

## 9. One-line contract for referees

> One seed set, one fluid continuum with \(D_{\mathrm{eff}}\le 25\), one scalar \(S=K(T_1+T_2+T_3)\), one residual law \(c=m(1+|S|f)\), thirty-five preregistered interfaces, zero free parameters — verified by residual atlas and multiprover export spines; uniqueness research is attractor/dampening under the same fluid, not a second theory.
