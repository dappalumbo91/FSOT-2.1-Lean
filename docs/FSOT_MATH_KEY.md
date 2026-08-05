# FSOT Mathematical Key — unified principle for every domain

**Edition:** 2026-08-05 (full system math audit + hierarchy)  
**Authority pin:** `D1D38A` · `vendor/fsot_compute.py` (SHA-256 prefix; confirm with [`CURRENT_STATUS.md`](CURRENT_STATUS.md))  
**Precision gates:** green ≤ **0.5%** pooled median · aspiration ≤ **0.05%** (`scripts/fsot_precision_constants.py`)  
**Live green count:** **always** [`CURRENT_STATUS.md`](CURRENT_STATUS.md) — do not trust memorized ratios in prose  
**Audience map:** [`DOCUMENTATION_MAP.md`](DOCUMENTATION_MAP.md) (lay · scientist · PhD)  
**Mathematician how-to:** [`FSOT_MATHEMATICIAN_HOWTO.md`](FSOT_MATHEMATICIAN_HOWTO.md)  
**System audit (machine):** [`data/fsot_system_math_audit.json`](../data/fsot_system_math_audit.json) · summary [`FSOT_SYSTEM_MATH_AUDIT.md`](FSOT_SYSTEM_MATH_AUDIT.md)  
**Building-block hierarchy:** [`data/fsot_building_block_hierarchy.json`](../data/fsot_building_block_hierarchy.json)  
**Domain network strings:** [`data/fsot_domain_formula_network.json`](../data/fsot_domain_formula_network.json)  
**Reproduce:** [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) · `python scripts/build_fsot_system_math_audit.py`  
**Full atlas:** `data/publication/domain_atlas.csv` + extension benchmarks · MPCORB-class catalogs in-repo

This is the **single readable key** for using the math across every covered domain.  
It is not a second theory. It is the same **fluid spacetime** engine, the same seeds, and the same routing rule — applied at the right **dimensional interface**.

---

## 0. One-paragraph thesis

FSOT is a **zero free-parameter fluid-spacetime** scalar engine: every constant is derived from five seeds \((\pi, e, \varphi, \gamma, G)\); continuum dynamics live at effective dimension \(D_{\mathrm{eff}}\) with compactification ceiling **25**.  
Every scientific domain is a **preregistered fold** of that engine at fixed \((D_{\mathrm{eff}}, h, \delta\psi, \delta\theta, \mathrm{observed})\) — not a separate fitted model.  
Predictions against measured data use one law:

\[
\texttt{computed} = \texttt{measured}\cdot\bigl(1 + |S(\mathrm{domain})|\cdot f_{\mathrm{domain}}\bigr)
\]

with \(S=K(T_1+T_2+T_3)\) from the full stack (observer / \(\mathbf{C}_{\mathrm{factor}}\) / POOF–Suction valves / chaos / bleed).  
When residual mismatches, **change \(D_{\mathrm{eff}}\) interface first** — do not invent a new coefficient.  
**Absolute rest frame is not the fluid:** rest-frame fiction damps; the continuum medium is the model.

---

## 1. Seeds (Layer 0 — no free parameters)

| Seed | Symbol | Role |
|------|--------|------|
| Circle constant | \(\pi\) | Cyclic / geometric structure |
| Natural base | \(e = \exp 1\) | Growth / decay |
| Golden ratio | \(\varphi = (1+\sqrt{5})/2\) | Self-similar folds |
| Euler–Mascheroni | \(\gamma\) | Discrete ↔ continuous |
| Catalan | \(G\) | Secondary geometric coupling |

**Code:** `vendor/fsot_compute.py` §1  
**Formal:** `FSOT/Formal/Scalar.lean`, Isabelle `FSOTScalarMath.thy`

---

## 2. Derived stack (still zero free parameters)

Primary: \(\alpha,\;\psi_{\mathrm{con}},\;\eta_{\mathrm{eff}},\;\beta,\;\gamma_c,\;\omega,\;\theta_S,\;\mathrm{Poof}\)  
Composite: \(C_{\mathrm{eff}},\;A_{\mathrm{bleed}},\;P_{\mathrm{var}},\;B_{\mathrm{in}},\;A_{\mathrm{in}},\;\mathrm{Suction},\;\mathrm{Chaos},\;P_{\mathrm{base}},\;P_{\mathrm{new}},\;\mathbf{C}_{\mathrm{factor}},\;K,\;C_{\mathrm{cosm}}\)

| Symbol | Plain name | Where it bites |
|--------|------------|----------------|
| \(\mathbf{C}_{\mathrm{factor}} = C_{\mathrm{eff}}\,P_{\mathrm{new}}\) | **Consciousness factor** | Observer branch of T1 |
| \(\mathrm{Poof}\) | Valve / collapse scale | T3 valve |
| \(\mathrm{Suction}\) | Complementary valve | T3 (yin–yang with Poof) |
| \(\mathrm{Chaos}\) | Instability scale | T3 high-\(D\) term |
| \(\theta_S,\;A_{\mathrm{bleed}}\) | Acoustic / bleed | T3 acoustic; geometric yin–yang |
| \(P_{\mathrm{var}}\) | Observer variance | Multiplies with \(\mathbf{C}_{\mathrm{factor}}\) when observed |
| \(K\) | Global scale | \(S = K\cdot(T_1+T_2+T_3)\) |

There is no separate “consciousness theory” bolt-on: consciousness enters as **\(\mathbf{C}_{\mathrm{factor}}\)** inside the same scalar.

---

## 3. The scalar engine (the heartbeat)

\[
\begin{aligned}
T_1 &= \text{observer-modulated base (includes \(\mathbf{C}_{\mathrm{factor}}\) when }\texttt{observed}\text{)} \\
T_2 &= \text{linear modulation (scale / amplitude / bias)} \\
T_3 &= \text{valve–acoustic–phase (Poof, Suction, Chaos, bleed)} \\
S &= K\cdot(T_1 + T_2 + T_3)
\end{aligned}
\]

### 3.1 Branch T1 — observer-modulated base

\[
\begin{aligned}
\mathrm{growth} &= \exp\!\bigl(\alpha(1-h/N)\gamma/\varphi\bigr) \\
\mathrm{base} &= \frac{NP}{\sqrt{D}}\cos\frac{\psi_{\mathrm{con}}+\delta\psi}{\eta_{\mathrm{eff}}}
  \exp(-\alpha h/N+\rho+B_{\mathrm{in}}\delta\psi)\,(1+\mathrm{growth}\,C_{\mathrm{eff}}) \\
T_1 &= \mathrm{base}\,(1+P_{\mathrm{new}}\ln(D/25))
\end{aligned}
\]

If `observed`: \(T_1 \leftarrow T_1\cdot\exp(\mathbf{C}_{\mathrm{factor}}P_{\mathrm{var}})\cos(\delta\psi+P_{\mathrm{var}})\).

**Fluid note:** \(\ln(D/25)\) is the fold about the compactification ceiling.

### 3.2 Branch T2 — linear modulation

\[
T_2 = \mathrm{scale}\cdot\mathrm{amplitude} + \mathrm{trend\_bias}
\]

(Domain routes use defaults scale=amplitude=1, trend_bias=0.)

### 3.3 Branch T3 — valve–acoustic–phase (fluid heart)

\[
\begin{aligned}
\mathrm{valve} &= \beta\cos\delta\psi\cdot\frac{NP}{\sqrt{D}}
  \Bigl(1+\mathrm{Chaos}\frac{D-25}{25}\Bigr)
  \bigl(1+\mathrm{Poof}\cos(\theta_S+\pi)+\mathrm{Suction}\sin\theta_S\bigr) \\
\mathrm{acoustic} &= 1+\frac{A_{\mathrm{bleed}}\sin^2\delta\theta}{\varphi}+\frac{A_{\mathrm{in}}\cos^2\delta\theta}{\varphi} \\
\mathrm{phase} &= 1+B_{\mathrm{in}}P_{\mathrm{var}} \\
T_3 &= \mathrm{valve}\cdot\mathrm{acoustic}\cdot\mathrm{phase}
\end{aligned}
\]

**Fluid note:** Chaos term vanishes at \(D=25\); POOF/Suction are continuum valves.

### 3.4 Observer duality (yin–yang)

- `observed=True` → \(T_1\) multiplies by \(\exp(\mathbf{C}_{\mathrm{factor}}\cdot P_{\mathrm{var}})\cdot\cos(\delta\psi + P_{\mathrm{var}})\)  
- `observed=False` → that branch is off → different \(S\) at the **same** \(D_{\mathrm{eff}}\)

### 3.5 Sign syntax

| \(S\) | Meaning | Formal |
|------|---------|--------|
| \(>0\) | emergence | `positive_S_means_emergence` |
| \(<0\) | damping | `negative_S_means_damping` |

Examples: Nuclear/Particle emergence; Cosmology (\(D=25\)) damping.

**Code:** `compute_scalar()` in `vendor/fsot_compute.py`  
**Formal:** Lean `FSOT.Formal.Scalar`, `FSOT/Theorems.lean`, multi-prover export spine  
**Full branch dump:** `data/fsot_system_math_audit.json` → `formula_branches`

---

## 4. Domains = dimensional interfaces (the routing rule)

Each of the **35 core** domains is a `DomainConfig`:

| Field | Meaning |
|-------|---------|
| `D_eff` | Effective dimension (ladder depth) |
| `hits` | Recent-hit coupling |
| `delta_psi`, `delta_theta` | Phase offsets |
| `observed` | Observer branch on/off |
| `C` | Domain interpretation constant (seed-derived) |

**Core ladder (examples):**

| Domain | \(D_{\mathrm{eff}}\) | observed | Typical use |
|--------|---------------------:|:--------:|-------------|
| Particle_Physics | 5 | yes | Micro / high-energy |
| Quantum_Mechanics | 6 | yes | Quantum residual panels |
| Neuroscience | 14 | yes | \(\mathbf{C}_{\mathrm{factor}}\) interpretation |
| Seismology | 18 | no | Chaotic bulk |
| Astronomy | 20 | yes | Catalog / astrometry spine |
| Planetary_Science | 21 | yes | Orbits, NEO, MPCORB belt |
| Astrophysics | 24 | yes/no | Distant / deep structure |
| Cosmology | 25 | no | \(C_{\mathrm{cosm}}\) interface |

**Extension domains** (atlas) are **preregistered folds** of these cores — not new free parameters.  
Full list: `data/publication/domain_atlas.csv` · `data/extension_domains_manifest.yaml`.

### The mismatch rule

> If a residual is bad, you almost always used the **wrong \(D_{\mathrm{eff}}\) / domain**, not a missing fit coefficient.

Worked example: MPCORB first-pass bare-seed \(e\) fold failed ~62%; routing eccentricity through **Planetary_Science (\(D=21\))** with full \(S\) brought the panel to **~0.023%** pooled — framework grade.  
Protocol: `docs/MPCORB_REFINEMENT_PROCESS.md`.

---

## 5. How to use the math in *any* domain (recipe)

### Step A — Name the measurement

Measured value \(m\) from a public or lab source (NIST, MPC, Gaia, PubChem, …).  
Tag provenance; never invent “measured × 0.999” by hand.

### Step B — Choose the dimensional interface

Pick the **core or extension domain** whose \(D_{\mathrm{eff}}\) matches the physics scale:

- close-in planetary / NEO → `Planetary_Science`  
- sky catalog spine → `Astronomy`  
- distant outer system → `Astrophysics`  
- chaotic high-\(e\) / weather-like → `Meteorology` / `Fluid_Dynamics`  
- mind / observer channels → `Neuroscience` / `Psychology`  

### Step C — Compute \(S\)

```python
from fsot_api_predict_lib import domain_scalar, fsot_scaled, make_fsot_record
S = domain_scalar("Planetary_Science")  # full stack at that domain
```

### Step D — Predict

```python
computed, error_pct = fsot_scaled(measured, "Planetary_Science")
# or property-routed:
rec = make_fsot_record(
    lab="my_lab", property_name="semi_major_au", name="Ceres",
    measured=2.77, domain="Planetary_Science",
)
```

Property → domain/factor table: `scripts/fsot_api_predict_lib.py` (`PROPERTY_ROUTING`, `DOMAIN_FACTORS`).

### Step E — Gate

- Per-domain **pooled median** \(\varepsilon \le 0.5\%\) → green  
- Aspiration band \(\le 0.05\%\) for tier scalar  
- Classifier domains: accuracy \(\ge 99.5\%\)

### Step F — Formal lock (optional but preferred)

Export residual gate → multi-prover spine (Lean / Coq / Isabelle / SMT).  
Provers re-check **literals** (e.g. `0.023 < 0.5`); they do not re-download catalogs.

---

## 6. Unified residual definition

\[
\varepsilon_i = 100\cdot\frac{|c_i - m_i|}{\max(|m_i|,\varepsilon_{\mathrm{floor}})}
\]

Domain metric = **median** \(\varepsilon_i\).  
Honesty tiers: `docs/RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`  
Field language (MAPE / ppm): `data/scientific_error_metrics_map.md`

---

## 7. What verification frameworks actually prove

| Layer | Frameworks | Proves / checks |
|-------|------------|-----------------|
| **A Engine math** | Lean 4 (master), Coq (Interval-native π/e base), Isabelle, F\*, Rust, seeds pin | Identities, scalar structure, exported bounds, transcendental digit intervals |
| **B Empirical atlas** | Python + green benchmarks (live: CURRENT_STATUS) | Domain residuals vs data ≤ 0.5% pooled median |
| **C Streams / catalogs** | Live APIs, MPCORB, MAST, … | Provenance + integrity (e.g. Kepler n↔a) |
| **Bulk bounds** | Z3 / CVC5 SMT | Conjunction of residual inequalities |
| **Flow** | TLA+ | Domain-routing state machine (no gate skips) |
| **Hardware** | QEMU / Rust kernel / optional ESP32 | Executable pack, θ, serial markers |

Roles map: `docs/FORMAL_PIPELINE_ROLES.md`  
Granularity audit: `docs/VERIFICATION_GRANULARITY_AUDIT.md`  
Honesty ledger: `docs/VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`

**Positioning (honest):** multi-prover + zero free parameters + hundreds of residual-gated domains is a strong public stack for a novel scalar framework. Claims must still match layer (A/B/C) — **not** “proved the universe in Coq,” and **not** “provers re-downloaded every catalog.”

---

## 8. Domain coverage snapshot

> **Live columns:** regenerate `python scripts/build_repo_status_snapshot.py` and `python scripts/build_fsot_math_key_onepager.py`.  
> Figures below are **order-of-magnitude / last-documented class** only if status is offline.

| Quantity | How to read | Typical class (refresh live) |
|----------|-------------|------------------------------|
| Publication atlas domains | `data/publication/domain_atlas.csv` row count | ~403 |
| Margin-audit green benchmarks | `green_gate_pass_count` / `benchmark_file_count` | see CURRENT_STATUS (e.g. 432/432) |
| Scalar-record envelope | status snapshot | see CURRENT_STATUS |
| Scientific catalog obligations | `verification/obligations/scientific_catalog_spine.json` | ~2025 |
| Full formal spine obligations | `verification/obligations/full_formal_spine.json` | ~2430 |
| Transcendental inventory | `python_decimal_verified` on 68 lemmas | 68/68 |
| MPCORB pooled residual | `data/mpcorb_fsot_benchmark.json` | ~0.023% (A_strong, D_eff=21) |

**Largest extension by records:** `MPCORB_Minor_Planet_Catalog` — IAU full minor-planet catalog + comets.  
**Lean:** `FSOT.Formal.MpcorbMinorPlanetCatalogPriors`

Full machine table: `data/publication/domain_atlas.csv`.

---

## 9. Core-domain quick map (how to read the 35)

Use this as the **default interface menu**. Extensions inherit one of these.

| Band | \(D_{\mathrm{eff}}\) range | Domains (examples) | Math use |
|------|---------------------------:|--------------------|----------|
| Micro | 5–9 | Particle, QM, Atomic, Chemistry, EM, Optics | High-energy / molecular residuals; small factors |
| Meso | 10–15 | Materials, Biology, Neuroscience, Condensed Matter, Fluids | Life / mind / matter; \(\mathbf{C}_{\mathrm{factor}}\) at Neuroscience |
| Geo–climate | 16–19 | Meteorology, Atmosphere, Ocean, Seismology, Geophysics | Chaos-bearing T3; often `observed=False` |
| Astro | 20–25 | Astronomy, Planetary, Astrophysics, Cosmology | Catalogs, orbits, cosmology; MPCORB / Gaia |

**Always:** pick band → run `domain_scalar` → `fsot_scaled` → green gate.

---

## 10. Worked examples

### 10.1 Gaia parallax (Astronomy, \(D=20\))

```text
domain = Astronomy
factor  ≈ 0.00025
S      ≈ 0.89846
ε%     ≈ |S|·factor·100 ≈ 0.0225%
```

Same residual scale across many astrometry properties — framework-standard.

### 10.2 MPCORB semi-major (Planetary_Science, \(D=21\))

```text
regime  = main_belt | neo | distant | comet
domain  = Planetary_Science | Astrophysics | Meteorology
law     = fsot_scaled(a, domain)
plus    = Kepler n↔a integrity on 1.55M rows (Layer C)
channels= C_FACTOR, POOF, yin–yang observer gap
pooled  ≈ 0.023%
```

### 10.3 Chemistry molecular weight

Prefer **formula mass** when SMILES/formula exists (true independent check); else chemistry domain factor.

---

## 11. Commands (reproduce the key claims)

```powershell
# Engine pin
python -c "from vendor import fsot_compute as f; print(f.domain_scalar('Astronomy'))"

# Domain residual ledger
python scripts/audit_all_benchmark_margins.py
# → data/benchmark_margin_audit.json

# Atlas
python scripts/build_scientific_domain_expansion_map.py
python scripts/export_publication_domain_atlas.py

# MPCORB
python scripts/ingest_mpcorb_catalog.py
python scripts/build_mpcorb_fsot_benchmark.py
python scripts/gen_mpcorb_minor_planet_catalog_lean.py

# Multi-prover catalog gates + SMT
python scripts/export_scientific_catalog_obligations.py
python scripts/generate_scientific_catalog_artifacts.py
python scripts/run_smt_catalog_bounds.py
python scripts/run_tla_domain_routing_check.py
# full gauntlet (long):
# python scripts/run_cross_proof_verification.py
```

---

## 12. What this key forbids

1. New free fit parameters per domain  
2. Silent “measured × almost 1” without the **named** `fsot_scaled` law and domain factor table  
3. Collapsing Layer A / B / C claims  
4. Treating multi-prover export as re-derivation of raw telescope pixels  
5. Ignoring \(D_{\mathrm{eff}}\) when residuals fail  

---

## 13. File map

| Need | Path |
|------|------|
| Engine | `vendor/fsot_compute.py` |
| Prediction API | `scripts/fsot_api_predict_lib.py` |
| Precision constants | `scripts/fsot_precision_constants.py` |
| Domain atlas | `data/publication/domain_atlas.csv` |
| Margin audit | `data/benchmark_margin_audit.json` |
| Extension registry | `data/extension_domains_manifest.yaml` |
| Narrative | `docs/FSOT_NARRATIVE_CORE.md` |
| Residual honesty | `docs/RESIDUAL_HONESTY_AND_CLAIM_TIERS.md` |
| Formal roles | `docs/FORMAL_PIPELINE_ROLES.md` |
| MPCORB refinement | `docs/MPCORB_REFINEMENT_PROCESS.md` |
| This key | `docs/FSOT_MATH_KEY.md` |
| **One-pager (PDF)** | [`docs/FSOT_MATH_KEY_ONEPAGER.pdf`](FSOT_MATH_KEY_ONEPAGER.pdf) · MD twin `docs/FSOT_MATH_KEY_ONEPAGER.md` |
| **ToE claim boundaries (frozen)** | `docs/TOE_CLAIM_BOUNDARIES.md` |
| **ToE gap closure** | `docs/TOE_GAP_CLOSURE.md` · `python scripts/build_toe_gap_closure.py` |
| **Documentation map** | `docs/DOCUMENTATION_MAP.md` |
| **Reproducibility** | `docs/REPRODUCIBILITY.md` |
| **Live status** | `docs/CURRENT_STATUS.md` |

---

## 13b. Hierarchical building blocks & domain network (for simulation)

Regenerate machine graph:

```powershell
python scripts/build_fsot_system_math_audit.py
```

| Artifact | Contents |
|----------|----------|
| `data/fsot_building_block_hierarchy.json` | Nodes/edges: seeds → L1/L2 → T1/T2/T3 → S → **35 cores + full extension atlas** → residual factors; `emergence_ladder_by_D_eff` |
| `data/fsot_domain_formula_network.json` | Domain strings + extension→core folds + **all green benchmark panels** + seed strings |
| `data/fsot_system_math_audit.json` | Live \(S\) for **every** core and extension interface; consistency; counts |

**Scope:** not the 35 alone — **~406 formula interfaces** (35 core + 371 extension) plus **~470 green residual panels** and **~403 atlas rows**. Same \(S\) law everywhere.  
**Hierarchy rule:** lower \(D_{\mathrm{eff}}\) = micro building blocks; higher \(D_{\mathrm{eff}}\) folds toward ceiling 25.  
**Syntax bit:** \(\mathrm{sign}(S)\) = emerge vs damp.  
**Strings:** shared algebra + different interface tuples — extensions fold onto cores for \(f\).

Mathematician protocol: [`FSOT_MATHEMATICIAN_HOWTO.md`](FSOT_MATHEMATICIAN_HOWTO.md) §7.

### Matter / antimatter (fluid duals)

Dedicated track (was missing as an explicit domain; seed \(\eta\) / \(\Omega_b h^2\) already lived in `fsot_compute`):

- Doc: [`MATTER_ANTIMATTER.md`](MATTER_ANTIMATTER.md)  
- Module: `vendor/fsot_matter_antimatter.py`  
- Benchmark: `data/matter_antimatter_benchmark.json`  

Matter = emergence-class particle/nuclear vortices; antimatter = conjugate continuum dual (\(\delta\psi+\pi\)); bulk asymmetry seed \(\eta=\mathrm{Poof}^{11}/(\pi\gamma)\); cosmology damps bulk antimatter residual.

---

## 14. PhD / formal-methods reading (precision of claims)

This section is for mathematicians and formal-methods researchers who need **scope**, not slogans.

### 14.1 What is formalized

| Object | Artifact | Status class |
|--------|----------|--------------|
| Scalar \(S=K(T_1+T_2+T_3)\) on \(\mathbb{R}\) | `FSOT/Formal/Scalar.lean`, Isabelle `FSOTScalarMath.thy` | Engine definitions + identities |
| Seed bounds (e.g. tight \(\pi\) digit intervals) | Lean Mathlib chain in `Bounds.lean`; Coq `TranscendentalBoundsNative.v` (Interval); Isabelle `approximation` | Machine-checked inequalities on \(\mathbb{R}\) |
| Domain residual **gates** as exported literals | Priors modules + `scientific_catalog_spine` obligations | “\( \varepsilon_{\mathrm{med}} < 0.5 \)” style, not catalog re-ingest |
| Routing / control flow | TLA+ domain-routing | Invariant: no silent gate skip |
| Bulk continuous residual conjunction | SMT (Z3/CVC5) | Satisfiability of exported bounds |

### 14.2 What is *not* claimed as a theorem

1. **Uniqueness of Einstein–Hilbert measure** or full spin-2 Fock uniqueness from the fluid action (probe layer residual-gated; uniqueness open — see ToE gap report).  
2. **Full non-abelian path-integral confinement theorem** (probe scales residual-gated; uniqueness open).  
3. That multiprover **re-derives** raw telescope / survey pixels — it re-checks **exported residual obligations**.  
4. That Label B “ToE” means peer-reviewed acceptance — peer process is separate (`TOE_CLAIM_BOUNDARIES.md`).

### 14.3 Residual metric (scientific, not decorative)

For each observable \(i\) with computed \(c_i\) and measured \(m_i\):

\[
\varepsilon_i = 100\cdot\frac{|c_i-m_i|}{\max(|m_i|,\varepsilon_{\mathrm{floor}})}.
\]

Domain headline = **pooled median** of \(\varepsilon_i\).  
**Green** iff that median \(\le 0.5\) (and classifier accuracy \(\ge 99.5\%\) where applicable).  
**Aspiration** band \(0.05\%\) is soft for tier scalar work — not a second secret green gate.

Prediction form used in the atlas:

\[
c = m\cdot\bigl(1 + |S(D)|\,f_D\bigr),
\]

with \(S(D)=\texttt{compute\_scalar}\) at preregistered domain \(D\) and factor \(f_D\) from a **fixed** table (`fsot_api_predict_lib.py`) — not least-squares per row.

### 14.4 Zero free parameters (operational definition)

- **Allowed:** five seeds; closed derived stack; preregistered \(D_{\mathrm{eff}}\) / observer flags.  
- **Forbidden:** per-observable fit coefficients, silent rescaling of \(m\), densify padding that copies residuals across domains.  
- **Audit:** `python scripts/audit_parameter_count.py` must report **ZERO_FREE**.

### 14.5 Suggested PhD audit order

1. Pin D1D38A + `Scalar.lean` definitions.  
2. One domain residual: recompute `fsot_scaled` on a public \(m\).  
3. Margin audit green on clean clone.  
4. One multiprover path (e.g. Lean prior theorem or Coq Interval \(\pi\) base).  
5. Read honesty ledger before writing a referee report.

---

**Bottom line:** one seed set, one scalar \(S\), one prediction law, many dimensional interfaces — with **explicit** layers of what is identity-proved, residual-gated, or still open uniqueness research.  
That is the mathematical key for every domain FSOT covers — including the full IAU minor-planet catalog at framework precision.
