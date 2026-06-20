# FSOT Formal Verification — Reproduction Guide

This repository machine-checks FSOT domain scalar **signs** and Wave-1 ΛCDM **numeric certificates** at canonical parameters. The formal source is ~0.3 MB; the first Lean build downloads Mathlib (~3 GB under `.lake/`).

## Prerequisites

- **Lean 4** via [elan](https://github.com/leanprover/elan): toolchain `leanprover/lean4:v4.31.0` (see `lean-toolchain`)
- **Python 3.11+** with `pip install -r requirements.txt`
- **fsot_compute.py** authority (or use cached `data/canonical_constants.json`)

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
5. Compares Wave-1 and domain scalars to `data/canonical_constants.json`
6. Validates genomic identities and syncs φ brackets (`gen_genomic_bounds.py --write-lean`)
7. Generates `FSOT/Formal/BrainPriors.lean` from ingested brain component priors
8. Ingests protein trinary phases and generates `FSOT/Formal/ProteinPriors.lean`
9. Runs `lake build` on `FSOT.Formal.*` (Genomic, BrainPriors, ProteinPriors, Lab)
10. Writes `data/certificate.json` and appends a line to `data/verification_runs.jsonl`

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
lake build FSOT.Formal.Bounds FSOT.Formal.Theorems FSOT.Formal.Cosmology FSOT.Formal.Domains FSOT
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
| `data/lab_registry.json` | Unified SMILES + NeuroLab data (generated) |
| `data/lab_domain_crosswalk.yaml` | Lab section → Lean domain mapping |
| `data/proof_ledger.yaml` | Claim ↔ Lean theorem ↔ oracle ↔ physics notes |
| `data/canonical_constants.json` | Pinned numeric cache from authority engine |
| `data/certificate.json` | Portable verification manifest (generated) |
| `data/verification_runs.jsonl` | Append-only run history (one JSON object per runner pass) |
| `data/neurolab_translations_bio.json` | Parsed NeuroLab Julia translations (38 rows) |
| `FSOT/Formal/Domains.lean` | Per-domain sign theorems |
| `FSOT/Formal/Theorems.lean` | Shared sign/dominance lemmas |
| `FSOT/Formal/Cosmology.lean` | Wave-1 and r_d interval certificates |
| `FSOT/Formal/Genomic.lean` | 64/27/20 exact identities + φ autosome certificate |
| `FSOT/Formal/BrainPriors.lean` | Auto-generated brain component trinary certificates |
| `FSOT/Formal/ProteinPriors.lean` | Auto-generated amino-acid trinary phase certificates |
| `docs/genomic_brain_priors_verification.md` | Findings, JSON artifact map, latest results |

## Claim scope (read before citing)

**Proved in Lean:** sign statements and interval bounds at **canonical** domain parameters; Wave-1 formulas at cached `S_cosm`, `S_quant`.

**Numerically verified:** oracle agreement with `fsot_compute.py` via hash gate.

**Not proved:** full FSOT physical interpretation, parameter-space exhaustiveness, or tight r_d ±0.01 Mpc (current certificate: ±0.05 Mpc).

See `docs/arxiv_outline.md` for the full proved / verified / conjectured taxonomy.