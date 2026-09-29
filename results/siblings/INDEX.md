# Sibling embodiment ledgers (pulled into the hub)

Same pin **D1D38A**. These folders are **copies of headline results**, not a second engine.

Refresh:

```powershell
python scripts/sync_sibling_embodiment_ledgers.py
```

Machine report: [`sync_report.json`](sync_report.json)

## Genetics — [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics)

Product freeze **2026-08-17** · `product_vs_alphafold.json`  
Medical panel **2026-09-21** · `wetlab_af_eval.json` · pin D1D38A

| Metric | FSOT product | AlphaFold |
|--------|-------------:|----------:|
| Median Cα RMSD (10 proteins) | **0.13 Å** | **0.47 Å** |
| Hemoglobin alpha on that freeze | **0.21 Å** | **0.27 Å** |
| Sub-2 Å / beat AF | **10/10** | — |
| Medical panel median (19 proteins) | **0.26 Å** | **3.98 Å** |
| Medical panel, targets with an AF model | beats AF **16/16** | — |
| Calmodulin | **0.52 Å** (3CLN) | 6.45 Å |
| No measured map | F01–F15 only — **3-D MDS not emitted** | — |

Product = measured homologs except the eval PDB + residual only when bonds are broken.  
The 19-protein panel is the same law on wet-lab chains. It is not the 10-protein freeze.  
No-map = formulas only; the old ~13.6 Å figure is the retired `--force-bulk` MDS path. Do not mix the two.

`data/structure_calibration_benchmark.json` stores 40.53 as 100 minus burial accuracy on 68 proteins. That number is not a Cα RMSD.

**Do not cross-cite:** product **0.13 Å** · medical **0.26 Å** · AF on the ten **0.47 Å** · AF on the nineteen **3.98 Å** · cryo-EM FSC **~1.2 Å** · bulk **~13 Å**. CASP/CAMEO blind: [`../../docs/CASP_CAMEO_BLIND_PROTOCOL.md`](../../docs/CASP_CAMEO_BLIND_PROTOCOL.md). Formulas pulled: [`genetics/formulas/`](genetics/formulas/).

Hub skeptic map: [`docs/GENETICS_CLAIM_EVIDENCE.md`](../../docs/GENETICS_CLAIM_EVIDENCE.md)

Files: [`genetics/PRODUCT_FREEZE.md`](genetics/PRODUCT_FREEZE.md) · [`genetics/OPEN.md`](genetics/OPEN.md)

## Quantum — [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum)

| Panel | Result |
|-------|--------|
| BH→WH H₀ replay | Planck **0.024%** · SH0ES **1.00%** (2.5% contested band) · global 68.440 |
| Contested sectors | **14/14** |
| Fold-not-Hilbert / hired QC | hire **29/29** · climb panels through hire7 **22/22** |
| Gset MaxCut family | **11/11 under 1%** · G17 **0.427%** (13 edges short — not champion-matching). Do not copy a 10/11 wrap into neuron-zig. |
| Observe path | QC dark → QO look → QM measure |

Files: [`quantum/H0_TENSION.md`](quantum/H0_TENSION.md) · [`quantum/STATUS.md`](quantum/STATUS.md)

## Theory map on this hub

[`docs/CONCEPTS.md`](../../docs/CONCEPTS.md) — BH→WH, bubble bleed, \(\kappa_{ij}\), folds, genetics residual.  
Kill maps: [`BH_WH_CLAIM_EVIDENCE.md`](../../docs/BH_WH_CLAIM_EVIDENCE.md) · [`GENETICS_CLAIM_EVIDENCE.md`](../../docs/GENETICS_CLAIM_EVIDENCE.md) · [`MATTER_ANTIMATTER_CLAIM_EVIDENCE.md`](../../docs/MATTER_ANTIMATTER_CLAIM_EVIDENCE.md)
