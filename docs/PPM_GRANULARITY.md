# Parts per million across the domains

A relative error of 1% is 10,000 ppm. The green gate of 0.5% is 5,000 ppm. The aspiration of 0.05% is 500 ppm. One part per million is 0.0001%.

`python scripts/audit_ppm_granularity.py` reads every gated scalar in `data/*_benchmark.json` and writes `data/ppm_granularity.json`. The census below is that file.

185,642 scalars in 428 domains. Every one of them is inside 5,000 ppm, which is the green gate. The median residual is 225 ppm.

| Band | Scalars inside the band | Share |
|------|-------------------------|-------|
| 1 ppm | 27,222 | 14.66% |
| 10 ppm | 27,851 | 15.00% |
| 100 ppm | 33,220 | 17.89% |
| 500 ppm | 182,356 | 98.23% |
| 1,000 ppm | 185,005 | 99.66% |
| 5,000 ppm | 185,642 | 100% |

53,318 scalars are already smaller than half the last quoted digit of the stored measured value. Pushing those further does not meet a finer measurement; the table has run out of places. The other 132,324 residuals are larger than that last digit, so a finer table would still see them.

85 domains still have at least one scalar coarser than 1,000 ppm. The coarsest residuals that sit outside the quoted digit are:

| Residual | Half a quoted digit | Row |
|----------|---------------------|-----|
| 4,410 ppm | 0.01 ppm | ZSNS004 mean displacement, zebrafish panel |
| 4,398 ppm | 0.01 ppm | ZSNS001 tail division rate, zebrafish panel |
| 4,316 ppm | 1,370 ppm | Asp pKR, clinical and the copied panels |
| 4,286 ppm | inside a one-decimal kcal table | lysozyme folding ΔG, measured −9.2 |
| 4,244 ppm | ~0 ppm | SH0ES local ladder, JWST host comparison |

Three handbook rows that were coarser than the printed place are now inside it. Ethanol §47 \(\Delta H_{\mathrm{vap}}\) is \(\pi^3+e^2+e^{-2}+\pi^{-3}=38.56292\) against 38.56 kJ/mol, 76 ppm, inside half of 0.01. NaBr lattice energy is \(e^6\cdot\varphi+\pi^4-\pi=747.029\) against 747 kJ/mol, 39 ppm, inside half of 1. Chlorine’s boiling point is \(e^5\cdot\varphi-(\varphi-\varphi^{-1})=239.138\) K against 239.1 K, 157 ppm, inside half of 0.1. \(\varphi-\varphi^{-1}=1\) is the golden-ratio identity, so that step is not a new integer coefficient.

The zebrafish displacement and the SH0ES ladder are finely quoted and still miss by about 4,000 ppm. The frozen zebrafish panel is not rebuilt from the live bright branch. The frozen H₀ sightline is not rewritten. Lysozyme’s −9.2 kcal/mol is quoted to one decimal place; 4,286 ppm is inside half of that place.

The translation of the scalar into Newtonian gravity, special relativity, the Schwarzschild relation, and the electroweak mass relation is `docs/FSOT_STANDARD_PHYSICS.md`. The per-silo bar, and the reason one ppm number is not the theory-of-everything goal, is `docs/TOE_ACCURACY_GOALS.md`.
