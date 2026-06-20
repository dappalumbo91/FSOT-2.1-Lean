# Genomic & Brain-Prior Verification — Findings & Results

**Last verified:** 2026-06-20  
**Repo:** `FSOT-2.1-Lean-main`  
**Authority:** `C:\Users\damia\Desktop\FSOT document update\fsot_compute.py`  
**Runner:** `python scripts/fsot_verification_runner.py`

---

## Executive summary

We extended the FSOT formal verification pipeline with:

1. **Machine-checked genomic exact identities** (64 codons, 27 trinary patterns, 20 amino acids, autosome ≈ 22).
2. **Brain component prior ingestion** — 10 NeuroLab components with 72bp `dna_proxy` trinary genetic signatures.
3. **Auto-generated Lean certificates** — `BrainPriors.lean` from registry data; φ-interval brackets synced into `Genomic.lean`.
4. **Protein amino-acid trinary stack** — 20 canonical phases from `Genetics/fsot_protein`, auto-generated `ProteinPriors.lean`.
5. **End-to-end green build** — 33 proved claims, 0 `sorry`, `lean_build_ok: true`.

---

## What is saved in JSON (and what is not)

Each successful run **overwrites** the latest snapshot artifacts and **appends** one line to the run history log.

| File | Updated when | Contents |
|------|----------------|----------|
| `data/certificate.json` | Every full runner pass | Lean build status, proved claims, theorem inventory, authority SHA-256, Wave-1 cache, lab summary |
| `data/lab_registry.json` | `ingest_lab_data.py` / runner | Full SMILES + NeuroLab ingest including `neurolab_bio.brain_component_priors` rows + `trinary_signature` |
| `data/neurolab_translations_bio.json` | `parse_neurolab_translations.py` | 38 Julia translations (10 Neuro + 13 Biophysics + 15 Genomic) |
| `data/canonical_constants.json` | `sync_canonical_constants.py` | Pinned Wave-1 + domain scalars + hash gate |
| `data/section_domain_map.json` | `build_section_domain_map.py` | 1470 SMILES records → Lean domains |
| `data/verification_runs.jsonl` | Every runner pass (append) | Timestamped run summary — pass/fail, counts, authority digest |
| `FSOT/Formal/BrainPriors.lean` | `gen_brain_priors_lean.py` | Auto-generated per-component genetic count theorems |
| `FSOT/Formal/ProteinPriors.lean` | `gen_protein_priors_lean.py` | Auto-generated per-amino-acid trinary phase theorems |
| `scripts/_genomic_bounds_snippet.lean` | `gen_genomic_bounds.py` | Reference φ-bracket lemmas |

**Not persisted today:** full Lean build logs, per-stage stderr, or raw `brain_component_priors.csv` (only digest + ingested copy in `lab_registry.json`).

---

## Genomic exact identities (Lean: `FSOT.Formal.Genomic`)

| Identity | Lean theorem | Method |
|----------|--------------|--------|
| 4³ = 64 codons | `codon_table_size_eq_sixty_four` | `norm_num` |
| 3³ = 27 trinary patterns | `trinary_pattern_count_eq_twenty_seven` | `norm_num` |
| 3/64 stop fraction | `stop_codons_fraction_eq` | `norm_num` |
| (4/3)³ = 64/27 degeneracy | `codon_trinary_degeneracy_eq` | `norm_num` |
| 4φ³ + 8φ⁻² = 20 amino acids | `amino_acids_canonical_eq_twenty` | φ algebra |
| 2(φ⁵ − φ⁻⁵) ≈ 22 autosomes | `autosome_haploid_count_eq_twenty_two` | interval certificate |

**φ-brackets (Python-certified, synced via `--write-lean`):**

- φ⁵ ∈ (11.089, 11.09244)
- φ⁻⁵ ∈ (0.09015, 0.09018)
- Autosome interval: (21.997640, 22.004580) ⊂ 22 ± 0.01

**Structural link to brain priors:**

- `genetic_trinary_alphabet_card = 3` (A→+1, G/C→0, T→−1)
- `codon_genetic_pattern_space_eq_twenty_seven` — each 3-base codon ∈ {−1,0,+1}³
- `codon_genetic_degeneracy` — 64 codons / 27 patterns = 64/27

---

## Brain component priors (Lean: `FSOT.Formal.BrainPriors`)

**Source:** `FSOT NeuroLab/DataAnalysisExpert/data/brain_public_sources/brain_component_priors.csv`

**Registry key:** `neurolab_bio.brain_component_priors` in `lab_registry.json`

| Field | Value |
|-------|-------|
| Components | 10 (Neocortex, Cerebellum, Brainstem Arousal, …) |
| DNA length | 72 bp per component |
| Codons | 24 per component (72 ÷ 3) |
| Genetic alphabet | 3 trits (+1 / 0 / −1) |
| Codon pattern space | 3³ = 27 |

**Per-component certified facts (auto-generated):**

- `*_genetic_counts_sum` — plus + zero + minus = 72
- `*_genetic_zero_is_superposition` — zero_count/72 = superposition_ratio (definitional)
- `*_spin_counts_sum` — purine/pyrimidine spin partition = 72

**Bundle theorem:** `brain_component_priors_trinary_bundle`  
**Ledger id:** `neurolab_brain_component_priors`

---

## Protein amino-acid trinary (Lean: `FSOT.Formal.ProteinPriors`)

**Source:** `Genetics/fsot_protein/src/secondary.rs` (`trinary_phase`) + `fsot_protein_formulas.json`

**Registry key:** `protein_formulas` in `lab_registry.json`

| Field | Value |
|-------|-------|
| Amino acids | 20 canonical |
| Trinary coordinates | [Charge, Polarity, Volume] ∈ {-1, 0, +1} |
| Distinct patterns | 10 (subset of 3³ = 27 genomic codon patterns) |
| Genomic link | `4φ³ + 8φ⁻² = 20` via `amino_acids_canonical_eq_twenty` |

**Bundle theorem:** `protein_amino_acid_trinary_bundle`  
**Ledger id:** `protein_amino_acid_trinary`

**Python verification** (`verify_protein_formulas.py`):

- Cross-checks registry rows against `protein_trinary.py` source table
- Validates distinct pattern count ≤ 27 and formulas JSON catalog presence

---

## Brain priors — Python verification

**Python verification** (`verify_neurolab_bio.py`):

- Recomputes trinary signatures from `dna_proxy` via `genomic_trinary.py`
- Checks gc_content == superposition_ratio, ATCG bases, coupling ∈ [0,1]
- Does **not** re-validate `entropy_norm` (CSV uses a different feature epoch)

---

## Automation pipeline

```powershell
python scripts/automate_verification.py --list-stages
```

| Stage | Script | Notes |
|-------|--------|-------|
| `genomic` | `gen_genomic_bounds.py --write-lean` | Validates identities + syncs φ brackets |
| `ingest` | `ingest_lab_data.py` | Builds `lab_registry.json` |
| `brain_priors_lean` | `gen_brain_priors_lean.py` | Regenerates `BrainPriors.lean` |
| `protein_ingest` | `ingest_protein_formulas.py` | Writes `protein_formulas` into registry |
| `protein_priors_lean` | `gen_protein_priors_lean.py` | Regenerates `ProteinPriors.lean` |
| `verify_bio` | `verify_neurolab_bio.py` | 10 priors + translations + pathways |
| `verify_protein` | `verify_protein_formulas.py` | 20 amino acids + formulas catalog |
| `runner` | `fsot_verification_runner.py` | Full hash gate + Lean + certificate |

---

## Latest results (2026-06-20)

```
SMILES records:        1470 (1470 mapped)
NeuroLab nuclei:       7
Brain fit domains:     15
Brain component priors: 10 (trinary signatures)
Translation total:     38 (all within 5%)
Brain pathways:        25 (max abs_gap < 0.15)
Lean build:            OK
Proved claims:         32
sorry_count_formal:    0
Authority SHA-256:     D1D38A185487B452E470AC68ECE2EB45AEB1CA9CE25FC9BF9564C19633FFBE70
```

---

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\New folder (9)\FSOT-2.1-Lean-main\FSOT-2.1-Lean-main"
python scripts/fsot_verification_runner.py
```

See also `REPRODUCE.md` and `data/proof_ledger.yaml` for claim ↔ theorem mapping.