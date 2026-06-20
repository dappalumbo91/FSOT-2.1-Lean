# Thesis Chapters 5–6 (Draft)

*Draft sections for a thesis on FSOT with a formal verification chapter. Auto-sourced from `FSOT/Formal/*` module headers and `data/proof_ledger.yaml`. Chapters 1–4 cover theory, domain taxonomy, compute engine, and formal encoding.*

---

## Chapter 5: Formal Verification Results

### 5.1 Objectives

The formal verification program had three goals:

1. Encode the FSOT scalar `raw_S = term1 + term2 + term3` in Lean 4 with the same definitions as `fsot_compute.py`.
2. Machine-check **sign certificates** for ledger domains at canonical parameters.
3. Provide **interval certificates** for Wave-1 ΛCDM observables and the baryon drag horizon `r_d` at cached cosmology inputs.

Success criterion: `lake build` on `FSOT.Formal.*` with **zero active `sorry`** and numeric agreement via `fsot_verification_runner.py`.

### 5.2 Formal module architecture

The Lean library splits responsibilities as documented in module headers:

- **`FSOT.Formal.Scalar`** — Noncomputable definitions mirroring the Python engine: constants, `term1_base`, `term1`, `term2`, `term3`, `raw_S`, `scaled_S`, and `get_domain_params`.
- **`FSOT.Formal.Bounds`** — Interval lemmas on transcendentals (π, φ, e, γ) and FSOT composite constants (coherence, bleed, perceived adjust).
- **`FSOT.Formal.Theorems`** — Reusable sign and dominance templates, e.g. `raw_S_positive_of_term1_gt_neg_08`, `raw_S_negative_of_term1_overcomes_term3`, `term3_abs_lt_fifth_default`.
- **`FSOT.Formal.Domains`** — Per-domain parameter lemmas and sign theorems for the ledger subset (cosmological, dark_energy, cmb, ai, neural, quantum, particle, chemical, electron, medical, and others).
- **`FSOT.Formal.Cosmology`** — Wave-1 formulas (`h0_fsot`, `t_cmb_fsot`, `n_s_fsot`, `omega_b_h2_fsot`, `alpha_s_MZ`) and `r_d_canonical` interval proof.
- **`FSOT.Formal.Lab`** — SMILES + NeuroLab integration: Layer-2 K/bleed/inflow alignment, 11 domain sign re-exports, `lab_smiles_domain_sign_bundle`.

### 5.3 Lab data integration (SMILES + NeuroLab)

External rendered labs are ingested into `data/lab_registry.json` and verified in two layers:

| Layer | Artifact | What it certifies |
|-------|----------|-------------------|
| Python numeric | `scripts/verify_lab_registry.py` | 1470/1470 SMILES rows mapped; formula errors ≤5%; thalamic K match; brain-fit gaps &lt;0.15 |
| Lean formal | `FSOT.Formal.Lab` | Domain scalar signs at ledger params; K interval certificates; `lab_smiles_domain_sign_bundle` |

**SMILES crosswalk:** `data/section_domain_map.json` maps all 108 sections (1470 records) to 8 Lean domains (chemical, material, medical, electron, nuclear, neural, particle, quantum).

**Catalog gaps (resolved):** Eight Tier-22 export rows (§90–§95) had `matched=false` with no `error_pct`. Formulas from `data/smiles_catalog_gaps.yaml` fill C3H8/C6H6 combustion, H2O Pc, E_coli membrane, dioxane/acetonitrile DN, Ge/InSb hole mobility — max error 2.78%.

**NeuroLab alignment:** `data/neurolab_ledger_alignment.yaml` patches 17 of 35 NeuroLab domains in `fsot_compute.py` to Lean ledger δψ, hits, D_eff, and observed flags (e.g. Neuroscience δψ 0.1→0.7). Lean oracle remains source of truth for sign proofs.

### 5.4 Sign certificate summary

At canonical ledger parameters, with `term2 = 1` and `|term3| < 0.2` (conservative; oracle gives |term3| ≈ 0):

**Negative or non-positive raw_S (high-D dispersal family):**

| Domain | Lean theorem | Oracle raw_S | Mechanism |
|--------|--------------|--------------|-----------|
| cosmological | `cosmological_raw_S_negative` | −1.20 | term1 ≪ −1 dominates |
| dark_energy | `dark_energy_raw_S_negative` | −1.13 | same, δψ = 1.1 |
| cmb | `cmb_raw_S_negative` | −1.01 | D=24 dispersal + adjust |
| ai | `ai_raw_S_non_positive` | −0.35 | term1 < −0.8 overcomes term2 |

**Positive raw_S (observer-boosted or weak dispersal):**

| Domain | Lean theorem | Oracle raw_S | Mechanism |
|--------|--------------|--------------|-----------|
| medical | `medical_raw_S_positive` | +0.73 | term1 > −0.8, hits=1 |
| chemical | `chemical_raw_S_positive` | +0.80 | term1 > −0.8, quirk+ |
| electron | `electron_raw_S_positive` | +0.97 | near-threshold term1 |
| neural | `neural_raw_S_positive` | +1.22 | negative quirk flips sign |
| quantum | `quantum_raw_S_positive` | +2.27 | low D, high δψ, observed |

The complete ledger mapping lives in `data/proof_ledger.yaml` with oracle floats from `scripts/domain_scalar_oracle.py`.

### 5.5 Wave-1 and cosmology certificates

From `FSOT.Formal.Cosmology`, at cached `S_cosm` and `S_quant`:

- **H₀** — `h0_fsot_cached_approx_value`: |H₀ − 68.440056829794272| < 10⁻⁸
- **T_CMB** — `t_cmb_fsot_cached_approx_value`: ±10⁻⁶ vs cache
- **n_s** — `n_s_fsot_cached_approx_value`: ±10⁻⁴ vs cache
- **Ω_b h²** — `omega_b_h2_fsot_cached_approx_value`: ±10⁻⁵ vs cache
- **α_s(M_Z)** — `alpha_s_MZ_approx_value`: 1/(eπ) matches cache to 10⁻⁸

**Baryon drag horizon:**

- `r_d_canonical = r★(1 + δλ)` with `r★ = π³/p_base − φ`
- Theorem `r_d_approx_value`: |r_d − 147.52| < 0.05 Mpc (interval certificate r_d ∈ (147.48, 147.55))

These are **internal consistency** proofs at pinned scalars, not standalone fits to cosmological data.

### 5.6 Tier 6: Per-formula observable verification

Beyond sign certificates and lab ingests, the verification program now requires **per-formula** checks for FSOT-derived observables (`data/formula_verification_policy.yaml`):

| Tier | Meaning | Lean module | Python verification |
|------|---------|-------------|---------------------|
| `lean_structural` | Sign proofs, bounds, wave intervals | `Domains`, `Cosmology`, `CosmologyLab` | `domain_scalar_oracle.py` |
| `numeric_formula` | formula → computed vs measured | `FormulaCorpusPriors`, `KnowledgeBasePriors` | `verify_formula_corpus.py`, `run_numeric_eval_queue.py` |
| `inventory` | Counts only — not per-formula | `UnifiedDBPriors` | `verify_unified_db.py` (index) |

**Strict-empirical corpus:** 7,941 records in `strict_empirical.jsonl`; all matched; 6,921 within 2%; all within 5%. Certified in `FSOT.Formal.FormulaCorpusPriors`.

**Unified DB numeric queue:** `verification_numeric` table in `FSOT_UNIFIED.db` — 9,607 rows after outcome_json backfill (7,830) and CNC turning MRR gap resolution (54 Kaggle runs). **0** strict_empirical records pending. Report: `data/numeric_eval_queue_report.json`.

**Knowledge base:** 19,213 catalog formulas with per-formula pass (`knowledge_base_formula_verification.jsonl`); 7,941 strict-empirical bridge counts in `KnowledgeBasePriors`.

**Additional Tier 6 labs:** Cellular (`CellularPriors` — Soul Simulator 234k records + 13 mt operons); BlackHole thesis (`BlackHoleThesisPriors` — 28/28 within 2%).

Current certificate: **57 proved claims**, 0 `sorry`, `lean_build_ok: true`.

### 5.7 Verification pipeline and reproducibility

The end-to-end pipeline:

```
fsot_compute.py  →  canonical_constants.json  →  hash gate
       ↓                    ↓                           ↓
fill_smiles_catalog_gaps   align_neurolab_domains   lake build FSOT.Formal.*
       ↓                    ↓                           ↓
Tier 2–6 lab ingests  →  formula/numeric verify  →  certificate.json
```

A clean reproduction is documented in `REPRODUCE.md`. The source-only release (`python scripts/make_source_release.py`) excludes the 3+ GB `.lake/` tree.

### 5.8 What was not proved

- FSOT as a fundamental physical theory
- Sign invariance under arbitrary parameter perturbations
- Magnitude matching to Planck/DESI beyond cached Wave-1 targets
- All 35 domains individually (subset has full theorems in `Domains.lean`)
- r_d to ±0.01 Mpc precision

---

## Chapter 6: Proof Methodology, Knowledge Base, and Portable Certificates

### 6.1 The physics–proof bridge

The hardest obligations were not closed by automation alone. They required identifying **which physical mechanism controls the sign** and choosing the matching **bound strategy**. This methodology is recorded in `data/proof_ledger.yaml` under `playbook_patterns`.

#### Pattern A: Wrong bound direction

*Symptom:* Lean fails to prove an upper bound on term1 when the oracle shows term1 ≈ −0.2.

*Physics:* At moderate D_eff with `observed = true`, quirk and perceived adjustments weaken dispersal; term1 is only slightly negative.

*Fix:* Prove `term1 > −0.8` (lower bound) and apply `raw_S_positive_of_term1_gt_neg_08`.

*Domains:* chemical, electron, medical.

#### Pattern B: Wrong recent-hits template

*Symptom:* `linarith` failure on medical; `rexp` / `growth_term` mismatch.

*Physics:* `recent_hits = 1` enters `exp(−α·hits/N)` and `growth_term`; the hits=0 template underestimates term1 magnitude.

*Fix:* Domain-specific bounds with `recent_hits = 1` in `domain_term1_gt_neg_08_medical`.

#### Pattern C: Dominance is not sign

*Symptom:* `term1 < 0` proved but `raw_S` sign still open.

*Physics:* `term2 = 1` is a positive bias; need |term1| > 1 + |term3|.

*Fix:* `domain_*_term1_overcomes_term3` lemmas (cmb, ai, cosmological).

#### Pattern D: Observer quirk sign algebra

*Symptom:* Wrong multiplication tactic for negative quirk × negative base.

*Physics:* Observed domains with δψ ≥ 0.7 can flip term1 positive via `quirkMod < 0`.

*Fix:* `term1_positive_of_observer_negative_quirk` with `nlinarith`.

### 6.2 Knowledge base design

The proof ledger YAML schema links:

- `id` — stable claim identifier
- `claim` / `status` — statement and proved vs planned
- `lean.module` / `lean.theorem` — certificate pointer
- `oracle` — numeric row from Python mirror
- `physics_note` — mechanism explanation
- `proof_blocker_history` — failed approaches (audit trail)

This KB is version-controlled, diffable, and consumed by `export_certificate.py` to build `data/certificate.json` for portable downstream use.

### 6.3 Portable verification backend

**Phase 1 (implemented):** Certificate manifest

- `certificate.json` records authority SHA-256, Wave-1 cache, proved claim list, formal theorem inventory, and source file digests.
- Other FSOT projects verify against the manifest without running Lean locally.

**Phase 2 (recommended):** CI Docker image

- Reproduce `lake build` + runner in a container; publish image digest alongside certificate.

**Phase 3 (future):** Runtime interval checker

- Export proved bounds to MPFR/interval arithmetic for sub-millisecond checks in applications.

### 6.4 Relation to arXiv publication

Chapter 5–6 material maps directly to an arXiv submission (see `docs/arxiv_outline.md`):

- Narrow claim: machine-checked sign and interval certificates
- Explicit taxonomy: proved / verified / conjectured / interpretation
- Supplementary zip for reproduction

The thesis adds narrative context (Chapters 1–4), full FSOT motivation, and the proof playbook as a methods contribution.

### 6.5 Future work

1. Tighten `r_d` interval to ±0.01 Mpc (sharper bounds on π³, p_base, φ).
2. Complete sign theorems for all 35 ledger domains.
3. Parameter-sensitivity certificates (small intervals on δψ, D_eff).
4. Sync ledger automatically from Lean `theorem` declarations on each CI pass.

---

## Suggested figures for thesis

1. **Pipeline diagram** — authority → oracle → Lean → certificate (§6.3)
2. **Term decomposition** — stacked bar: term1/2/3 for medical, cmb, cosmological
3. **Playbook flowchart** — failure symptom → physics cause → bound strategy
4. **Claim taxonomy table** — from `docs/arxiv_outline.md`