# Scientist reproduction — MPCORB domain paper (Paper 04)

## Claim

FSOT predicts the full public MPCORB catalog at ~0.023% pooled median residual with zero free parameters (numbers in `FREEZE.yaml`).

## Reproduce

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
# If MPCORB.DAT not vendored, place under vendor/mpcorb/
python scripts/ingest_mpcorb_catalog.py
python scripts/build_mpcorb_fsot_benchmark.py
```

Expect `data/mpcorb_fsot_benchmark.json` pooled median ≈ 0.023% and green under margin audit.

## Process doc

`docs/MPCORB_REFINEMENT_PROCESS.md`
