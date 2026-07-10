# Contributing to FSOT 2.1 Lean

This repository is designed to be **clone-and-verify** without the author's Desktop folder layout. External projects can reference [github.com/dappalumbo91/FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) as a standalone verification artifact.

## Quick start (portable verification)

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
lake build
python scripts/fsot_verification_runner.py --portable
```

Portable mode uses:

- `vendor/fsot_compute.py` — canonical numeric oracle
- `vendor/formula_corpus/by_domain/strict_empirical.jsonl` — **7,941** per-formula strict-empirical verification corpus
- `vendor/smiles/FSOT_SMILES_Lab_Dataset.json` — SMILES Lab catalog
- `vendor/evolution/biological_mt_operons.json` — evolution operon source
- `vendor/fsot_aggregate/` — unified mathematical database + prediction re-derivation summary
- Pre-built benchmarks under `data/` (climate, space weather, pharmacology, etc.)

See `data/external_data_manifest.yaml` for the full bundled vs cached vs optional breakdown.

**API sources and full rebuild:** `data/api_requirements.yaml` lists every public ingest endpoint, optional API keys, and the ordered rebuild pipeline.

**Expansion roadmap:** `data/expansion_roadmap.yaml` documents planned tiers (stellar multiplicity, materials, genetics) and the proprietary/discoverability boundary.

## Requirements

- **Lean 4** + `lake` on `PATH` (see `lean-toolchain`)
- **Python 3.10+** with `PyYAML` (`pip install PyYAML`)
- **Network** — only required for full data re-ingest; portable verify uses bundled `vendor/` + `data/` caches

## Verification modes

| Mode | Command | When to use |
|------|---------|-------------|
| Portable | `python scripts/fsot_verification_runner.py --portable` | CI, external clones, cross-project references |
| Full | `python scripts/fsot_verification_runner.py` | Author machine with optional Desktop lab mirrors |

Portable mode skips Desktop-only rebuild steps (lab ingest, NOAA re-fetch, Lean regeneration) and verifies against bundled assets plus cached `data/` benchmarks.

## Full reproducibility (clone → rebuild → verify)

```bash
# 1. Portable verify (no network, no Desktop mirrors)
lake build
python scripts/fsot_verification_runner.py --portable
python scripts/verify_extension_domains.py

# 2. Regenerate all Lean certificates from benchmark JSON
python scripts/rebuild_all_lean.py
lake build
python scripts/export_certificate.py --lean-ok

# 3. Full data rebuild (network + optional FSOT_EXTERNAL_DATA_ROOT)
python scripts/sync_canonical_constants.py
python scripts/ingest_tier38_public_data.py          # see data/api_requirements.yaml
python scripts/build_astrophysical_structure_crosswalk_benchmark.py
python scripts/rebuild_all_lean.py
python scripts/build_fsot_verification_progress.py
```

Lean priors under `FSOT/Formal/*Priors.lean` are **generated** — edit benchmarks and `scripts/*_lib.py`, then run `rebuild_all_lean.py`. Hand-edit only core spine modules (`Domains.lean`, `Bounds.lean`, `Theorems.lean`).

## Path resolution

All scripts resolve external inputs through `scripts/fsot_paths.py`:

| Asset | Default (repo) | Override env var |
|-------|----------------|------------------|
| Compute oracle | `vendor/fsot_compute.py` | `FSOT_COMPUTE_PATH` |
| SMILES dataset | `vendor/smiles/FSOT_SMILES_Lab_Dataset.json` | `FSOT_SMILES_DATASET` |
| Evolution operons | `vendor/evolution/biological_mt_operons.json` | `FSOT_EVOLUTION_OPERONS` |
| Neuron cohort (rebuild) | `vendor/neuron_cohort/` | `FSOT_NEURON_COHORT_ROOT` |
| NeuroLab (rebuild) | `vendor/neurolab/` | `FSOT_NEUROLAB_ROOT` |

On the author's machine, Desktop paths are still tried as fallbacks when vendor copies are absent.

## Regenerating canonical constants

After updating `vendor/fsot_compute.py`:

```bash
python scripts/sync_canonical_constants.py
```

This writes repo-relative paths into `data/canonical_constants.json`.

## Adding a new verification domain

Follow the established pipeline documented in `README.md`:

1. Manifest → ingest script → `data/*_benchmark.json`
2. `gen_*_lean.py` → `FSOT/Formal/*Priors.lean`
3. Register in `data/extension_domains_manifest.yaml` and `scripts/fsot_verification_runner.py`
4. `lake build` + `python scripts/fsot_verification_runner.py --portable`

Keep all new source paths **repo-relative** in manifests. Bundle small inputs under `vendor/`; commit large observational caches under `data/`.

## Hash gate

The authority SHA-256 for `vendor/fsot_compute.py` is pinned in `scripts/fsot_hash_gate.py`. If you intentionally update the oracle, run `sync_canonical_constants.py` and update the documented hash in `data/external_data_manifest.yaml`.

## Questions

Open an issue on GitHub or reference `data/FSOT_VERIFIED_SCOPE.yaml` for the current capability map.