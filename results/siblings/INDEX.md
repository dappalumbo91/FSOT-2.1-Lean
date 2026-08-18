# Sibling embodiment ledgers (pulled into the hub)

Same pin **D1D38A**. These folders are **copies of headline results**, not a second engine.

Refresh:

```powershell
python scripts/sync_sibling_embodiment_ledgers.py
```

Machine report: [`sync_report.json`](sync_report.json)

## Genetics — [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics)

Product freeze **2026-08-17** · `product_vs_alphafold.json`

| Metric | FSOT product | AlphaFold |
|--------|-------------:|----------:|
| Median Cα RMSD (10 proteins) | **0.13 Å** | **0.47 Å** |
| Sub-2 Å / beat AF | **10/10** | — |
| Calmodulin | **0.52 Å** (3CLN) | 6.45 Å |
| No measured map | F01–F15 only — **3-D MDS not emitted** | — |

Product = measured homologs except the eval PDB + residual only when bonds are broken.  
No-map = formulas only; the old ~13.6 Å figure is the retired `--force-bulk` MDS path. Do not mix the two.

Hub skeptic map: [`docs/GENETICS_CLAIM_EVIDENCE.md`](../../docs/GENETICS_CLAIM_EVIDENCE.md)

Files: [`genetics/PRODUCT_FREEZE.md`](genetics/PRODUCT_FREEZE.md) · [`genetics/OPEN.md`](genetics/OPEN.md)

## Quantum — [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum)

| Panel | Result |
|-------|--------|
| BH→WH H₀ replay | Planck **0.024%** · SH0ES **1.00%** (2.5% contested band) · global 68.440 |
| Contested sectors | **14/14** |
| Fold-not-Hilbert / hired QC | hire **29/29** · climb panels through hire7 **22/22** |
| Gset MaxCut family | **11/11 under 1%** · G17 **0.427%** (13 edges short — not champion-matching) |
| Observe path | QC dark → QO look → QM measure |

Files: [`quantum/H0_TENSION.md`](quantum/H0_TENSION.md) · [`quantum/STATUS.md`](quantum/STATUS.md)

## Theory map on this hub

[`docs/CONCEPTS.md`](../../docs/CONCEPTS.md) — BH→WH, bubble bleed, \(\kappa_{ij}\), folds, genetics residual.  
Kill maps: [`BH_WH_CLAIM_EVIDENCE.md`](../../docs/BH_WH_CLAIM_EVIDENCE.md) · [`GENETICS_CLAIM_EVIDENCE.md`](../../docs/GENETICS_CLAIM_EVIDENCE.md) · [`MATTER_ANTIMATTER_CLAIM_EVIDENCE.md`](../../docs/MATTER_ANTIMATTER_CLAIM_EVIDENCE.md)
