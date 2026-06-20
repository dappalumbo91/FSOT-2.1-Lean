# FSOT Formal Verification — Reproduction Guide

This repository machine-checks FSOT domain scalar **signs** and Wave-1 ΛCDM **numeric certificates** at canonical parameters. The formal source is ~0.3 MB; the first Lean build downloads Mathlib (~3 GB under `.lake/`).

## Prerequisites

- **Lean 4** via [elan](https://github.com/leanprover/elan): toolchain `leanprover/lean4:v4.31.0` (see `lean-toolchain`)
- **Python 3.11+** with `pip install -r requirements.txt`
- **fsot_compute.py** authority (or use cached `data/canonical_constants.json`)
- **External corpora** (optional for full Tier 6): FSOT unified DB, Knowledge base transfer, CNC `Exp1.csv`, BlackHole thesis MD (paths in manifests)

## Quick verify (recommended)

```powershell
cd <repo-root>
pip install -r requirements.txt
python scripts/fsot_verification_runner.py
```

On success this:

1. Fills 8 SMILES catalog gaps (`scripts/fill_smiles_catalog_gaps.py`)
2. Aligns NeuroLab 35-domain table to Lean ledger (`scripts/align_neurolab_domains.py`)
3. Checks SHA-256 hash gate on `fsot_compute.py`
4. Ingests SMILES + NeuroLab data; verifies `data/lab_registry.json`
5. Ingests Tier 2–6 labs (cosmology, fuel, species, CAMEO, trinary OS, photonic forge, vibra, magnetic strings, evolution, weather, linguistics, unified DB, wave4, kronos, knowledge base, math generator, trinary fluid, soul sibling, lean proofs bridge, formula corpus, cellular, blackhole thesis)
6. Resolves strict-empirical numeric gap (`scripts/resolve_strict_empirical_gap.py`) and backfills `verification_numeric` (`scripts/backfill_numeric_from_outcomes.py`)
7. Runs KB per-formula verification (`scripts/run_knowledge_base_formula_verify.py`)
8. Compares Wave-1 and domain scalars to `data/canonical_constants.json`
9. Validates genomic identities and syncs φ brackets (`gen_genomic_bounds.py --write-lean`)
10. Runs `lake build` on all `FSOT.Formal.*` targets in `certificate.json`
11. Writes `data/certificate.json` and appends a line to `data/verification_runs.jsonl`

**Expected:** 57 proved claims, 0 `sorry`, `lean_build_ok: true`.

## Step-by-step

### 1. Sync canonical constants (optional)

If you have the authority compute engine locally:

```powershell
python scripts/sync_canonical_constants.py
```

### 2. Domain scalar oracle (numeric reference)

```powershell
python scripts/domain_scalar_oracle.py
```

Mirrors `FSOT.Formal.Scalar` term1/term2/term3/raw_S per ledger domain.

### 3. Lean build

```powershell
lake exe cache get
lake build FSOT.Formal.Bounds FSOT.Formal.Theorems FSOT.Formal.Cosmology FSOT.Formal.Domains FSOT.Formal.Lab FSOT
```

### 4. Export certificate only

```powershell
python scripts/export_certificate.py --lean-ok
```

### 5. Source-only release zip

```powershell
python scripts/make_source_release.py
```

Output: `dist/fsot-lean-source-YYYYMMDD.zip` (no `.lake/`).

## Tier 6 — Formula & numeric verification

Honest per-formula checks (not inventory-only counts). Policy: `data/formula_verification_policy.yaml`.

### Strict-empirical corpus (7,941 formulas)

```powershell
python scripts/ingest_formula_corpus.py
python scripts/gen_formula_corpus_lean.py
python scripts/verify_formula_corpus.py
```

Source: `strict_empirical.jsonl` — each row has `formula_canonical`, `target_value`, `computed_value`, `error_pct`, `matched`.

### Unified DB numeric eval queue

```powershell
# Full: observable pipeline + CNC gap + outcome_json backfill
python scripts/run_numeric_eval_queue.py

# Backfill only (no network / no full pipeline scan)
python scripts/run_numeric_eval_queue.py --skip-pipeline

# CNC turning MRR gap (54 Kaggle runs)
python scripts/resolve_strict_empirical_gap.py

# Backfill verification_numeric from records.outcome_json
python scripts/backfill_numeric_from_outcomes.py
```

Report: `data/numeric_eval_queue_report.json` — target state: `strict_empirical_pending_numeric: 0`.

### Knowledge base (19,213 catalog formulas)

```powershell
python scripts/run_knowledge_base_formula_verify.py
python scripts/ingest_knowledge_base.py
python scripts/gen_knowledge_base_lean.py
python scripts/verify_knowledge_base.py
```

Outputs: `data/knowledge_base_formula_verification.jsonl`, `data/knowledge_base_formula_verification_summary.json`.

### Cellular + BlackHole thesis labs

```powershell
python scripts/ingest_cellular_lab.py
python scripts/gen_cellular_priors_lean.py
python scripts/verify_cellular_lab.py

python scripts/ingest_blackhole_thesis.py
python scripts/gen_blackhole_thesis_lean.py
python scripts/verify_blackhole_thesis.py
```

## Staged automation

```powershell
python scripts/automate_verification.py --list-stages
python scripts/automate_verification.py --stage parse_bio --stage verify_bio
python scripts/automate_verification.py   # full pipeline
```

NeuroLab biological-only:

```powershell
python scripts/parse_neurolab_translations.py
python scripts/verify_neurolab_bio.py
```

## Lab integration (SMILES + NeuroLab)

```powershell
python scripts/ingest_lab_data.py      # build data/lab_registry.json
python scripts/verify_lab_registry.py    # cross-check labs vs canonical + Lean signs
```

Sources (see `data/lab_domain_crosswalk.yaml`):

- **FSOT SMILES Lab** — 1470 chemical/biological constants (`FSOT_SMILES_Lab_Dataset.json`)
- **FSOT NeuroLab** — thalamic gate (7 nuclei), brain fit dashboard (15 domains), articulation targets

The full runner (`fsot_verification_runner.py`) ingests and verifies labs automatically.

## Key artifacts

| File | Role |
|------|------|
| `data/lab_registry.json` | Unified lab ingest (generated) |
| `data/lab_domain_crosswalk.yaml` | Lab section → Lean domain mapping |
| `data/proof_ledger.yaml` | Claim ↔ Lean theorem ↔ oracle ↔ physics notes |
| `data/canonical_constants.json` | Pinned numeric cache from authority engine |
| `data/certificate.json` | Portable verification manifest (generated) |
| `data/verification_runs.jsonl` | Append-only run history (one JSON object per runner pass) |
| `data/formula_verification_policy.yaml` | lean_structural / numeric_formula / inventory tiers |
| `data/numeric_eval_queue_report.json` | Unified DB `verification_numeric` before/after stats |
| `data/knowledge_base_formula_verification.jsonl` | Per-formula KB catalog pass (19,213 rows) |
| `data/domain_coverage_map.yaml` | 26-domain ledger vs lab coverage index |
| `data/neurolab_translations_bio.json` | Parsed NeuroLab Julia translations (38 rows) |
| `FSOT/Formal/Domains.lean` | Per-domain sign theorems incl. `cellular_raw_S_positive` |
| `FSOT/Formal/FormulaCorpusPriors.lean` | 7941 strict-empirical observable certificates |
| `FSOT/Formal/KnowledgeBasePriors.lean` | KB catalog + per-formula + strict-empirical bridge |
| `FSOT/Formal/CellularPriors.lean` | Soul Simulator + evolution operon certificates |
| `FSOT/Formal/BlackHoleThesisPriors.lean` | 28 BH thermo thesis observable certificates |
| `docs/genomic_brain_priors_verification.md` | Findings, JSON artifact map, latest results |

## Claim scope (read before citing)

**Proved in Lean:** sign statements and interval bounds at **canonical** domain parameters; Wave-1 formulas at cached `S_cosm`, `S_quant`.

**Numerically verified:** oracle agreement with `fsot_compute.py` via hash gate; per-formula strict-empirical checks; lab ingest tolerances.

**Inventory only:** `UnifiedDBPriors` record/project counts — does **not** prove individual formulas. Use `FormulaCorpusPriors` for observable-checked formulas.

**Not proved:** full FSOT physical interpretation, parameter-space exhaustiveness, or tight r_d ±0.01 Mpc (current certificate: ±0.05 Mpc).

See `docs/arxiv_outline.md` for the full proved / verified / conjectured taxonomy.