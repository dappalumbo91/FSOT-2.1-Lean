# Verification granularity audit (deep cut)

> **Session snapshot 2026-08-03.** Live green is **472/472**, atomic **2022**, full formal **2585**. See [`CURRENT_STATUS.md`](CURRENT_STATUS.md) and [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md). Layer numbers below are the August 3 cut, not the live gate.

**Generated:** `2026-08-03T21:20:28.623027+00:00`  
**Repo:** FSOT-2.1-Lean  

This is not a skim. It separates **engine math**, **domain residuals**, **dataset provenance**, and **multi-prover export re-proof**.

---

## Executive answer

| Question | Answer |
|----------|--------|
| Is verification *only* pure math? | **No.** Layer B audits **405** domain residual rows; **405** currently green under ≤0.5% pooled median. |
| Are all ~402 domains checked? | **Yes at the green-gate layer** (atlas **402**, margin audit **405**). |
| Against multiple datasets? | **Yes, via ~411 `*_benchmark.json` files** and live/open streams — but depth varies per domain. |
| Do Lean/Coq/Isabelle re-ingest raw catalogs? | **No.** They re-prove **exported gate literals** (and engine math). |
| Zero-residual domains (inspect!) | **136** domains report 0% pooled median — not automatically 'strong prediction'. |
| MPCORB integrated? | **Yes** — objects=1554101, Kepler med%=1.5875572596619725e-06 |

---

## Layer map (do not collapse)

### Layer A — Engine math

- Seeds π, e, φ, γ, Catalan; `raw_S = term1+term2+term3`; pin **D1D38A**.
- Lean primary (`FSOT/Formal/*`), Isabelle `FSOTScalarMath`, F* boot kernel, Rust replay.
- Full formal spine: **2370** obligations across **500** modules (1863 atomic provable in last cross-proof report).

### Layer B — Empirical domain residuals

- Margin audit: **405/405** green (fail **0**), threshold **0.5%**.
- Record sum (margin domains): **762,478**.
- Median of per-domain medians: **0.011093889935064888**.
- Max domain median: **0.3579695** (still under gate if green).
- Atlas: **402** rows — core **35**, extension **367**.
- Coverage tiers: `{'A_strong': 115, 'B_verified': 287}`.

### Layer C — Live / catalog streams

- Open science holdouts, MAST, public APIs, **now MPCORB/AllCometEls** under `vendor/mpcorb/`.
- HTTP 200 ≠ residual green (`docs/RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`).

### Multi-prover translation layer

- **Scientific catalog spine:** 1980 obligations / 405 domains.
- Claim mix: `{'seed_identity': 5, 'seed_positive': 5, 'catalog_nonempty': 404, 'empirical_pooled_median_gate': 804, 'empirical_max_scalar_gate': 357, 'green_gate_pass_flag': 405}`.
- **What a catalog lemma actually is:** e.g. `0.0176 < 0.5` for domain pooled median — discharged by `lra`/`norm_num`/SMT.
- **What it is not:** re-running the domain builder or re-downloading NIST inside Coq.
- SMT bulk: overall_ok=True solver=z3.
- TLA+ routing: overall_ok=True.
- Last cross-proof `overall_ok`: **True** (re-run after major changes).

---

## Residual honesty inside benchmarks (sampled)

Scanned **300331** record rows across **411** benchmark files:

| Pattern | Count |
|---------|------:|
| Nonzero `error_pct` | 2962 |
| Zero `error_pct` | 297369 |
| `measured == computed` | 18739 |
| Missing `measured` | 278655 |

**Interpretation:** A large zero/`measured==computed` fraction means some panels are integrity, classifier, or identity-style checks. That is allowed **if labeled** — it is **not** the same epistemic weight as an independent predictive residual.

### Zero-residual domains (sample of 25)

- `Creative_Arts_Math_Spine`
- `Information_Theory_Public_Panel`
- `Music_Harmonics_Public_Panel`
- `Formula_Precision_Spine`
- `Periodic_Table_Completion_Spine`
- `Z164_Distant_Island_Prereg_Scaffold`
- `Fuel_Thermochemistry_Public_Anchors`
- `Materials_Genome_Crosswalk`
- `materials_species_bridge_benchmark.json`
- `Econophysics`
- `FSOT_Aggregate_Organized_Panel`
- `FSOT_Aggregate_Unified_DB`
- `Initiation_Transformation_Archetype`
- `Proof_Ledger_Closure_Spine`
- `Pure_Mathematics`
- `Quantum_Information`
- `evolution_operon_benchmark.json`
- `synthetic_biology_benchmark.json`
- `planetary_atmospheres_benchmark.json`
- `Domain_Coupling_Simulation_Refresh_Panel`
- `Observer_Effect_Cross_Species_Panel`
- `Ecology`
- `Robotics_Control_Systems`
- `Time_Emergence_Simulation`
- `Fluid_Spacetime_Prereg_Validation_Panel`

---

## MPCORB / comets (this session)

- Objects: **1,554,101**
- Comets parsed: **4645**
- Kepler integrity median residual: **1.5875572596619725e-06%**
- FSOT structural median residual: **2.25109%**
- Details: `data/mpcorb_fsot_benchmark.json`, `data/mpcorb_fsot_summary.md`

---

## Bottom line (granular)

1. **Math is real** — Layer A is multi-prover engine verification, not theater.
2. **Domains are real** — Layer B green-gates the atlas-scale residual ledger.
3. **Datasets are real but uneven** — some domains are deep empirical; some are thin scaffolds or identity-adjacent.
4. **Multi-prover scientific catalog re-proof is real and limited** — it locks residual *numbers* against silent drift; it does not replace Python/data pipelines.
5. **Your job as author/reviewer** is to keep claim language matched to layer (A/B/C) and to pressure-test zero-residual domains.

Machine-readable twin: `data/verification_granularity_audit.json`.
