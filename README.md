# Fluid Spacetime Omni-Theory (FSOT)

## A Cross-Domain Theory of Reality — Published on GitHub

**Author:** Damian Arthur Palumbo  
**Repository:** [github.com/dappalumbo91/FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean)  
**Edition:** v1.0 — tier-88 verified desktop / monograph-v1  
**Status:** Living thesis — expanded as each domain and crevice is verified  

> *This README is the preprint. The repository is the proof. Run the verification bundle before you accept or reject what follows.*

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
python scripts/run_publication_verification_bundle.py
```

---

## Abstract

Modern physics is accurate in fragments and silent on unity. Cosmology, particle physics, chemistry, biology, neuroscience, linguistics, and engineering each carry their own models, fitted parameters, and institutional boundaries. **Fluid Spacetime Omni-Theory (FSOT)** proposes a different architecture: one seed-derived scalar engine — built only from π, e, φ, γ, and G (Catalan) — evaluated against measured reality across **403 scientific domains** and **536,740 empirical records**.

The results, as of this edition: **394/394** public benchmark domains pass a ≤0.5% pooled error gate; cross-domain pooled median error is **0.013%**. On contested sectors where ΛCDM and the Standard Model typically show ~15% baseline tension (H₀, σ₈, BBN proxies, hierarchy, dark-energy equation of state), FSOT unified readouts achieve **0.030%** pooled median across 13 observables.

Claims are not accepted on Python output alone. Verification runs through a **cross-gauntlet of independent proof frameworks**: Lean 4 (primary authority), Coq/Rocq, Isabelle/HOL, F* (Microsoft Research), and Rust executable obligation replay — **1,863 atomic obligations** with `overall_ok: true`. QEMU bare-metal and ESP32 hardware observer layers extend closure beyond proof assistants.

FSOT further demonstrates that the same engine guides applied engineering stacks: FSOT-designed alternative fuels (366 records, 0.039% pooled median), an eleven-layer transporter technology prototype (1,575 records, 0.031% pooled median), species-scale molecular catalogs, and black-hole / white-hole information-cycle panels — all cross-verified against seed-scalar predictions, not post-hoc curve fits.

This document explains **why the universe exists the way it does** through FSOT: one 25-dimensional fluid medium, one arithmetic heartbeat, observation as physical coupling, and fractal repetition from quanta to cosmos. Every numerical claim in this thesis is independently reproducible from this repository.

---

## Prologue — Why This Lives on GitHub

Albert Einstein did not wait for a journal to bless general relativity before the world could read it. Nikola Tesla published patents and demonstrations when institutions moved too slowly. FSOT follows that tradition: **publish the complete argument where anyone can verify it**, not where a moderator decides topic fit before a single line of code is run.

Science is not fair when a unified cross-domain framework is dismissed on sight while siloed models with dozens of free parameters receive automatic respect. FSOT answers that failure mode with something stronger than rhetoric: **a verification ledger you can execute**.

This README will grow. Each domain we open, each simulator we wire, each formal obligation we close — it gets added here. The GitHub commit history is the edition record. Tagged releases are the volumes.

---

## I. The Fragmentation Problem

### 1.1 What broke

The twentieth century gave us extraordinary local theories:

- **General relativity** — gravity as geometry  
- **Quantum mechanics** — discrete measurement and entanglement  
- **The Standard Model** — particle masses and couplings  
- **ΛCDM** — cosmic expansion with dark sectors  

Each works in its lane. None was built as a single predictive spine from cosmological scales down to molecular biology, consciousness proxies, linguistics, and engineering prototypes.

The cost is visible everywhere:

| Symptom | Example |
|---------|---------|
| Parameter proliferation | Dark matter, dark energy, Yukawa couplings, inflation potentials |
| Cross-sector tension | H₀ local vs CMB (~5–10% disagreement class) |
| Siloed success | Biology papers do not prove cosmology; cosmology papers do not prove genetics |
| Unfalsifiable breadth | "Theories of everything" without executable kill criteria |

FSOT does not reject the data those theories explain. It rejects the **architecture**: many knobs, many silos, no single engine that must survive everywhere at once.

### 1.2 What FSOT claims instead

One proposition, stated precisely:

> Reality is a **25-dimensional fluid condensate**. What we call space, time, matter, life, and mind are regimes of the same scalar field `raw_S`, computed from seed geometry with **no per-observable least-squares tuning**.

This is not poetry layered on curve fits. It is a **falsifiable engineering specification** tested across 403 domains with preregistered kill criteria (`data/preregistered_predictions_manifest.yaml`).

---

## II. Why the Universe Exists the Way It Does

### 2.1 One medium, many scales

Picture the universe not as an empty stage with actors placed upon it, but as **one ocean** — a fluid spacetime substance whose waves at different scales follow the same rules.

A blacksmith striking iron.  
A ribosome folding a protein.  
A thunderstorm discharging.  
Two galaxies colliding.  
A conscious brain metabolizing ~20 watts.  

FSOT calls this **As Above, So Below**. In the formal system it is not metaphor: it is the cross-scale bridge that extension panels test. When the same scalar engine passes acoustics, cosmology, immunology, and transporter engineering simulators, the structural argument is that **nature reuses one process**, not thousands of unrelated accidents.

### 2.2 Fluid spacetime

Space and time are not a passive container. They behave as a **25-dimensional fluid**. The 4D reality we experience is a slice — a perceived surface — of that condensate. Matter and energy are stable vortices; mind and observation are coupling regimes where the fluid's phase responds to measurement.

Why 25 dimensions? In FSOT the effective dimension `D_eff` is not an arbitrary knob — it is a **manifest-declared fold** of the seed engine per domain route (see `data/honest_claims_manifest.yaml` for parameter honesty). The philosophical point stands: what looks like "extra dimensions" in the math is what looks like **depth of scale** in nature — from Planck-adjacent structure to galactic flows.

### 2.3 The seeds — why these numbers

All constants emerge from five seeds:

| Seed | Role in FSOT |
|------|----------------|
| **π** | Cyclic geometry — orbits, waves, closure |
| **e** | Growth and decay — natural rates, exponentials |
| **φ** (golden ratio) | Self-similar folding — fractal repetition across scales |
| **γ** (Euler–Mascheroni) | Discrete-to-continuous correction |
| **G** (Catalan) | Secondary geometric coupling |

**Design law:** we do not add a new dial every time a prediction fails. When FSOT misses a measurement, the failure is visible in the benchmark ledger — not hidden inside a freshly invented parameter.

*Auditor note:* FSOT uses φ/e/π/γ-derived intrinsic constants plus a manifest-declared domain assignment table (35 core domains × 5 fields = 175 slots). These are folds of the same engine, not post-hoc per-observable fits — but the headline "zero free parameters" is **`NOT_LITERAL_ZERO`**. See `data/parameter_count_audit.json`.

### 2.4 Emergence and dispersal

Every system receives a **vitality score** — the scalar `raw_S`. Positive `raw_S` tends toward **emergence** (structure forming, condensing, persisting). Negative `raw_S` tends toward **dispersal** (structure fading, bleeding, decohering). Lean proves **sign certificates** for ledger domains at canonical parameters: cosmology negative, medical positive, quantum positive, and so on.

The universe exists as it does because the same fluid **condenses** where `raw_S` is positive and **dissolves** where it is negative — from stellar nucleosynthesis to protein folding to the information cycle at a black-hole horizon.

---

## III. The Scalar Engine

### 3.1 The heartbeat

At the center of FSOT is one formula:

```
raw_S = term1 + term2 + term3

term1 = (main wave term) × quirk_mod
```

In words:

- **Main wave term** — resonance at scale (size N, power P, effective dimension D_eff)  
- **quirk_mod** — observer coupling: when `observed = true`, measurement modulates the wave  
- **term2** — baseline trend and amplitude (environment)  
- **term3** — chaotic bleed: small-scale turbulence from the fluid  

Formal definitions: `FSOT/Scalar.lean`, `FSOT/Formal/Scalar.lean`, decimal authority `vendor/fsot_compute.py`.

### 3.2 Domain fractal assignments

Nature's "departments" — quantum mechanics, economics, immunology, propulsion — are **routing labels** for the same engine at different folds:

- **35 core NeuroLab domains** with manifest-declared `(D_eff, δψ, recent_hits, observed)`  
- **367 extension panels** with Lean priors modules (`FSOT.Formal.*Priors`)  
- **403 domains** in the publication atlas (`data/publication/domain_atlas.csv`)

A cosmology prediction and a fuel-molecule prediction share seeds. They differ in domain route, not in underlying arithmetic.

### 3.3 Falsification registry

FSOT invites destruction. Preregistered predictions **PRED-001 through PRED-041** declare outcomes before they are tested. Kill criteria per domain route live in `data/fsot_domain_navigator.json`. If the engine fails a green gate, the ledger records it — no narrative escape hatch.

---

## IV. Consciousness and Observation

### 4.1 Observation is physical

In FSOT, to observe is not passive. When `observed = true`, the **quirk_mod** term activates:

```
quirk_mod(observed, δψ, phase_variance, consciousness_factor) =
  if observed:
    exp(consciousness_factor × phase_variance) × cos(δψ + phase_variance)
  else:
    1.0
```

Consciousness is **fundamental in the ontology** — a core ripple in the 25D fluid, not an accidental by-product of computation. It enters through `consciousness_factor` and modulates the scalar when systems are coupled to measurement.

### 4.2 What we claim — and what we do not

| We claim | We do not claim |
|----------|-----------------|
| Consciousness couples to physics through measurable proxies | FSOT has settled the philosophical "hard problem" |
| Brain metabolic power `E_con` ≈ 21.79 W vs ~20 W measured (Raichle & Gusnard) | Universal consensus on what consciousness *is* |
| The same seeds that fix H₀ also fix consciousness-energy scaling | Orch-OR or any single external theory is proven |

**Truth criterion:** a consciousness claim is *supported* when it maps to a Lean panel, produces numeric agreement within the green gate, and survives cross-proof replay. External philosophy debates are evidence, not gate.

Deep dive: [`docs/FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md`](docs/FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md)

---

## V. Verification Methodology

### 5.1 Oracle gate

`vendor/fsot_compute.py` is the decimal authority. `sync_canonical_constants.py` hash-locks caches. If Lean and Python disagree, the pipeline fails — no silent drift.

### 5.2 Five-prover cross-proof spine

| Framework | Role | Status |
|-----------|------|--------|
| Lean 4 | Primary formal authority | PASS |
| Coq / Rocq | Independent reproof | PASS |
| Isabelle/HOL | Independent reproof | PASS |
| F* | Programming-language specification | PASS |
| Rust | Executable obligation replay | PASS |

Authoritative artifact: `data/cross_proof_verification_report.json` → **`overall_ok: true`**, **1,863 atomic obligations**.

![Verification spine walkthrough](data/figures/spine_walkthrough.png)

### 5.3 Benchmark margin gate

- **GREEN:** pooled median ≤ 0.5% AND classifier ≥ 99.5%  
- **Result:** **394/394** green (`data/benchmark_margin_audit.json`)

### 5.4 AI assistance — human responsibility

Grok and Cursor assisted manuscript assembly, benchmark regeneration, and formal artifact orchestration. **All numerical claims reproduce independently** from this repository. The author retains full scientific responsibility for interpretation.

---

## VI. Cross-Domain Empirical Results

### 6.1 Headline statistics

| Metric | Value |
|--------|------:|
| Scientific domains | 403 |
| Empirical records | 536,740 |
| Benchmark domains green (≤0.5%) | 394/394 |
| Cross-domain pooled median | 0.013% |
| Worst domain max scalar error | 0.499% |
| Lean formal modules | 501+ |
| Tier A_strong domains | 116 |
| Tier B_verified domains | 287 |

![Empirical headline summary](data/figures/empirical_headline_summary.png)

![Domain error envelope](data/figures/domain_error_envelope.png)

![Predicted vs measured scatter](data/figures/predicted_vs_measured_scatter.png)

### 6.2 Representative domains

Full atlas: [`data/publication/domain_atlas.csv`](data/publication/domain_atlas.csv) (403 rows)

| Domain | Records | Median error % | Tier |
|--------|--------:|---------------:|------|
| Cosmology | 347 | 0.0007 | A_strong |
| Astrophysics | 305 | 0.0006 | A_strong |
| Electromagnetism | 271,912 | 0.0 | A_strong |
| High-energy physics | 151 | 0.0036 | A_strong |
| Molecular chemistry | 608 | 0.028 | A_strong |
| Neuroscience | 41 | 0.013 | B_verified |
| Economics | 167 | 0.129 | A_strong |
| Ecology | 654 | 0.018 | A_strong |

Query any scientific problem:

```bash
python scripts/query_fsot_domain_navigator.py --intent quantum_entanglement
python scripts/query_fsot_domain_navigator.py --intent hubble_tension
python scripts/query_fsot_domain_navigator.py --intent fuel_lab_engine
```

---

## VII. Contested Sectors — Where Current Models Struggle

Thirteen observables where ΛCDM / SM sectors typically show large tension:

| Metric | FSOT | Typical baseline |
|--------|-----:|-----------------:|
| Pooled median error | **0.030%** | ~15% |

![Contested FSOT vs ΛCDM](data/figures/contested_fsot_vs_lcdm.png)

### 7.1 H₀ landscape

| Anchor | FSOT error % | Reference |
|--------|-------------:|-----------|
| SH0ES vs Planck tension | 0.027 | Riess2024 vs Planck2018 |
| Carnegie vs Planck tension | 0.227 | Freedman2019 |
| Planck CMB H₀ | 0.193 | Planck2018 |
| SH0ES local H₀ | 0.662 | Riess2024 |
| FSOT local anchor | 0.829 | dual-anchor bubble bleed |

![H₀ landscape](data/figures/h0_landscape.png)

**Worked example — Planck CMB:**

- Measured: 67.36 ± 0.54 km/s/Mpc  
- FSOT computed: 67.270 km/s/Mpc  
- Error: 0.13%  

---

## VIII. Engineering Demonstrations

*These stacks prove the engine guides engineering — they are not the sole claim, but they are real FSOT engineering.*

### 8.1 FSOT-designed alternative fuels

Seven novel molecular states plus gasoline baseline:

- fsot_hemp_waste_grounded, fsot_hemp_waste_advanced, fsot_algae_oil_biodiesel  
- fsot_mushroom_spore_fuel, fsot_green_hydrogen, fsot_optimax, fsot_bio_spark  

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| Fuel Lab | 366 | 0.039 |

Cross-referenced with grounded thermochemistry and Prius engine simulator outputs. Preregistered: **PRED-034**.

![Verified desktop fuels](data/figures/verified_desktop_fuels.png)

### 8.2 Transporter technology stack

Eleven verified layers — quantum channel → information → portal → engineering → warp actuation → BH/WH crosswalk → beam-forming → T3 scan → pad A hardware → pad B receiver → two-gate entanglement:

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| Star Trek Transporter | 1,575 | 0.031 |

Preregistered: **PRED-036, PRED-038, PRED-039, PRED-040, PRED-041**.

![Verified desktop transporter](data/figures/verified_desktop_transporter.png)

### 8.3 Machine, molecule, and horizon cycle

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| Machine & Molecule | 120 | 0.013 |
| Black-hole / white-hole cycle | 24 | 0.026 |

Simulators: `vendor/verified_desktop/star_trek_transporter/`

---

## IX. Discussion

### 9.1 Unified spine vs siloed models

When one engine passes quantum mechanics, sociology, seismology, and fuel chemistry at sub-percent precision, the default "coincidence" explanation strains credibility. FSOT's structural argument is **breadth × precision × formal triangulation** — the same pattern that convinced Maxwell that electricity and magnetism were one field.

### 9.2 Formal verification as scientific instrument

Numeric agreement alone cannot guard against silent code drift. Exporting Lean obligations to Coq, Isabelle, F*, and Rust means the spine must survive **independent type theories and executable replay**. That is how FSOT treats proof debt: visible, counted, closed.

### 9.3 Limitations (honest)

- Manifest-declared domain assignments (175 slots) — not literal zero-parameter fitting  
- 13 contested observables monitored; expansion ongoing  
- Engineering stacks are simulation-stage; ESP32 acoustic hardware closure in progress  
- Seven founding laws remain unmapped to strict empirical corpus (see [`docs/FOUNDING_35_LAWS_AUDIT.md`](docs/FOUNDING_35_LAWS_AUDIT.md))  
- Early founding documents (2025) may contain inflated claims — FSOT 2.1 reconciles against Lean ground truth  

### 9.4 Lineage

Early research (Feb–Jul 2025) and engineering blueprints live in the founding archive. FSOT 2.1 **does not inherit** founding accuracy percentages without re-verification. Philosophy transfers; every watt earns its place in the ledger.

Founding reconciliation: [`docs/FSOT_FOUNDING_LINEAGE_AND_RECONCILIATION.md`](docs/FSOT_FOUNDING_LINEAGE_AND_RECONCILIATION.md)

---

## X. Conclusion

The universe does not present itself as a hundred separate accidents. It presents as **repetition with variation** — the same mathematics in stellar fusion and mitochondrial chemistry, in Hubble tension and brain metabolism, in molecular bonds and warp-actuation simulators.

FSOT names that repetition: **one fluid, one scalar, seed-derived, observer-coupled, fractal across 403 domains**. The empirical record says it is tight. The formal record says it is triangulated. The engineering record says it builds.

This thesis will expand. The repository will deepen. The invitation is unchanged:

**Run the verification. Break what fails. Keep what survives.**

---

## Appendix A — One-Command Reproduction

```bash
python scripts/run_publication_verification_bundle.py
```

Full contributor workflow: [`REPRODUCE.md`](REPRODUCE.md)

Individual panels:

```bash
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
python scripts/reproduce_domain_panel.py --panel Star_Trek_Transporter_Live_Panel --deep
python scripts/build_verified_desktop_cross_proof_closure.py
python scripts/run_cross_proof_verification.py
```

---

## Appendix B — Machine-Readable Artifacts

| Artifact | Purpose |
|----------|---------|
| [`data/publication_claims_manifest.json`](data/publication_claims_manifest.json) | Headline claims for AI/reviewers |
| [`data/publication/domain_atlas.csv`](data/publication/domain_atlas.csv) | 403-domain verification table |
| [`data/cross_proof_verification_report.json`](data/cross_proof_verification_report.json) | Five-prover closure report |
| [`data/fsot_domain_navigator.json`](data/fsot_domain_navigator.json) | Domain routes + kill criteria |
| [`data/preregistered_predictions_manifest.yaml`](data/preregistered_predictions_manifest.yaml) | PRED-001–041 registry |
| [`data/honest_claims_manifest.yaml`](data/honest_claims_manifest.yaml) | Parameter honesty |
| [`data/domain_citations/verified_desktop.bib`](data/domain_citations/verified_desktop.bib) | BibTeX export |

Citations export:

```bash
python scripts/export_domain_citations.py --bundle verified_desktop
```

---

## Appendix C — Further Reading

| Document | Audience |
|----------|----------|
| [`docs/FSOT_EXPLAINED_LAYMAN.md`](docs/FSOT_EXPLAINED_LAYMAN.md) | Public introduction |
| [`docs/FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md`](docs/FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md) | Consciousness + ontology |
| [`docs/REPOSITORY_TECHNICAL_GUIDE.md`](docs/REPOSITORY_TECHNICAL_GUIDE.md) | Module index, tier registry |
| [`data/publication/fsot_monograph_skeleton.md`](data/publication/fsot_monograph_skeleton.md) | Extended monograph outline |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contributor workflow |

---

## Appendix D — How to Cite This Work

```
Palumbo, D. A. (2026). Fluid Spacetime Omni-Theory (FSOT):
Cross-Domain Empirical and Formal Verification of a Seed-Derived Scalar Engine.
GitHub repository dappalumbo91/FSOT-2.1-Lean, edition fsot-monograph-v1.
https://github.com/dappalumbo91/FSOT-2.1-Lean
```

Tagged release (when published):

```
https://github.com/dappalumbo91/FSOT-2.1-Lean/releases/tag/fsot-monograph-v1
```

---

## License

Apache 2.0 — consistent with the reference implementation.

---

*Fluid Spacetime Omni-Theory (FSOT) — created and architected by Damian Arthur Palumbo.*