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
- `vendor/smiles/FSOT_SMILES_Lab_Dataset.json` — SMILES Lab catalog
- `vendor/evolution/biological_mt_operons.json` — evolution operon source
- Pre-built benchmarks under `data/` (climate, space weather, pharmacology, etc.)

See `data/external_data_manifest.yaml` for the full bundled vs cached vs optional breakdown.

## Requirements

- **Lean 4** + `lake` on `PATH`
- **Python 3.10+** with `PyYAML` (`pip install PyYAML`)

## Verification modes

| Mode | Command | When to use |
|------|---------|-------------|
| Portable | `python scripts/fsot_verification_runner.py --portable` | CI, external clones, cross-project references |
| Full | `python scripts/fsot_verification_runner.py` | Author machine with optional Desktop lab mirrors |

Portable mode skips Desktop-only rebuild steps (lab ingest, NOAA re-fetch, Lean regeneration) and verifies against bundled assets plus cached `data/` benchmarks.

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