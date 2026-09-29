# Parts per million across the domains

A relative error of 1% is 10,000 ppm. The green gate of 0.5% is 5,000 ppm. The aspiration of 0.05% is 500 ppm. One part per million is 0.0001%.

`python scripts/audit_ppm_granularity.py` reads every gated scalar in `data/*_benchmark.json` and writes `data/ppm_granularity.json`. The census below is that file.

185,642 scalars in 428 domains. Every one of them is inside 5,000 ppm, which is the green gate. The median residual is 225 ppm.

| Band | Scalars inside the band | Share |
|------|-------------------------|-------|
| 1 ppm | 27,222 | 14.66% |
| 10 ppm | 27,851 | 15.00% |
| 100 ppm | 33,217 | 17.89% |
| 500 ppm | 182,352 | 98.23% |
| 1,000 ppm | 185,001 | 99.65% |
| 5,000 ppm | 185,642 | 100% |

53,314 scalars are already smaller than half the last quoted digit of the stored measured value. Pushing those further does not meet a finer measurement; the table has run out of places. The other 132,328 residuals are larger than that last digit, so a finer table would still see them.

85 domains still have at least one scalar coarser than 1,000 ppm. The coarsest residuals that sit outside the quoted digit are:

| Residual | Half a quoted digit | Row |
|----------|---------------------|-----|
| 4,410 ppm | 0.01 ppm | ZSNS004 mean displacement, zebrafish panel |
| 4,398 ppm | 0.01 ppm | ZSNS001 tail division rate, zebrafish panel |
| 4,339 ppm | 209 ppm | Cl₂ boiling point, morphogenetic scaling |
| 4,316 ppm | 1,370 ppm | Asp pKR, clinical and the copied panels |
| 4,286 ppm | ~0 ppm | lysozyme folding ΔG |
| 4,270 ppm | 130 ppm | ethanol §47 ΔHvap, CRC |
| 4,244 ppm | 669 ppm | NaBr lattice energy, CRC |
| 4,244 ppm | ~0 ppm | SH0ES local ladder, JWST host comparison |

The zebrafish displacement and the SH0ES ladder are finely quoted and still miss by about 4,000 ppm. The frozen zebrafish panel is not rebuilt from the live bright branch. The frozen H₀ sightline is not rewritten. Ethanol’s vaporization leaf \(\pi^3+e^2=38.395\) against 38.56 kJ/mol is a handbook row the printed digits can still resolve: the miss is about thirty times half the last place.

The translation of the scalar into Newtonian gravity, special relativity, the Schwarzschild relation, and the electroweak mass relation is `docs/FSOT_STANDARD_PHYSICS.md`.
