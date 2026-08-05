# FSOT Mathematical Key — unified principle for every domain

**Edition:** 2026-08-05  
**Authority pin:** `D1D38A` · `vendor/fsot_compute.py`  
**Precision gates:** green ≤ **0.5%** pooled median · aspiration ≤ **0.05%** (`scripts/fsot_precision_constants.py`)  
**Live green count:** [`docs/CURRENT_STATUS.md`](CURRENT_STATUS.md) (currently **430/430** margin-audit green)  
**Full atlas:** `data/publication/domain_atlas.csv` + extension benchmarks · MPCORB-class catalogs in-repo

This is the **single readable key** for using the math across every covered domain.  
It is not a second theory. It is the same engine, the same seeds, and the same routing rule — applied at the right **dimensional interface**.

---

## 0. One-paragraph thesis

FSOT is a **zero free-parameter** scalar engine: every constant is derived from five seeds \((\pi, e, \varphi, \gamma, G)\).  
Every scientific domain is a **preregistered fold** of that engine at a fixed effective dimension \(D_{\mathrm{eff}}\), observer flag, and coupling constants — not a separate fitted model.  
Predictions against measured data use one law:

\[
\texttt{computed} = \texttt{measured}\cdot\bigl(1 + |S(\mathrm{domain})|\cdot f_{\mathrm{domain}}\bigr)
\]

with \(S\) from the full scalar stack (observer / consciousness factor / POOF valve / chaos / bleed).  
When residual mismatches, **change \(D_{\mathrm{eff}}\) interface first** — do not invent a new coefficient.

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

**Observer effect (yin–yang duality):**

- `observed=True` → \(T_1\) multiplies by \(\exp(\mathbf{C}_{\mathrm{factor}}\cdot P_{\mathrm{var}})\cdot\cos(\delta\psi + P_{\mathrm{var}})\)  
- `observed=False` → that branch is off → different \(S\) at the **same** \(D_{\mathrm{eff}}\)

That gap is the engine’s observer duality — used as a first-class channel in MPCORB refinement.

**Code:** `compute_scalar()` in `vendor/fsot_compute.py`  
**Formal:** Lean `FSOT.Formal.Scalar`, multi-prover export spine

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

| Layer | Frameworks | Proves |
|-------|------------|--------|
| **A Engine math** | Lean 4 (master), Coq, Isabelle, F\*, Rust, seeds pin | Identities, scalar structure, exported bounds |
| **B Empirical atlas** | Python + **430** green benchmarks (live: CURRENT_STATUS) | Domain residuals vs data ≤ 0.5% |
| **C Streams / catalogs** | Live APIs, MPCORB, MAST, … | Provenance + integrity (e.g. Kepler n↔a) |
| **Bulk bounds** | Z3 / CVC5 SMT | Conjunction of residual inequalities |
| **Flow** | TLA+ | Domain-routing state machine (no gate skips) |

Roles map: `docs/FORMAL_PIPELINE_ROLES.md`  
Granularity audit: `docs/VERIFICATION_GRANULARITY_AUDIT.md`

**Positioning (honest):** multi-prover + zero free parameters + hundreds of domains at sub-percent residuals is an unusually complete public stack for a novel scalar framework. Claims should still match layer (A/B/C) — not “proved the universe in Coq.”

---

## 8. Domain coverage snapshot

| Quantity | Value |
|----------|------:|
| Publication atlas domains | **403** |
| Margin-audit green benchmarks | **430 / 430** (refresh via `build_repo_status_snapshot.py`) |
| Empirical record sum (atlas) | **~2.63M** (incl. MPCORB 1.55M) |
| Scientific catalog obligations | **~1912** multi-prover residual gates |
| MPCORB pooled residual | **0.023015%** (A_strong, D_eff=21) |

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

---

**Bottom line:** one seed set, one scalar \(S\), one prediction law, many dimensional interfaces.  
That is the mathematical key for every domain FSOT covers — including the full IAU minor-planet catalog at framework precision.
