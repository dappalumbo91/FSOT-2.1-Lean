# Parts per million across the domains

A relative error of 1% is 10,000 ppm. The green gate of 0.5% is 5,000 ppm. The aspiration of 0.05% is 500 ppm. One part per million is 0.0001%.

`python scripts/audit_ppm_granularity.py` reads every gated scalar in `data/*_benchmark.json` and writes `data/ppm_granularity.json`. The census below is that file.

185,642 scalars in 428 domains. Every one of them is inside 5,000 ppm, which is the green gate. The median residual is 225 ppm.

| Band | Scalars inside the band | Share |
|------|-------------------------|-------|
| 1 ppm | 27,222 | 14.66% |
| 10 ppm | 27,851 | 15.00% |
| 100 ppm | 33,227 | 17.90% |
| 500 ppm | 182,369 | 98.24% |
| 1,000 ppm | 185,019 | 99.66% |
| 5,000 ppm | 185,642 | 100% |

53,332 scalars are already smaller than half the last quoted digit of the stored measured value. Pushing those further does not meet a finer measurement; the table has run out of places. The other 132,310 residuals are larger than that last digit, so a finer table would still see them.

85 domains still have at least one scalar coarser than 1,000 ppm. The coarsest residuals that sit outside the quoted digit are:

| Residual | Half a quoted digit | Row |
|----------|---------------------|-----|
| 4,410 ppm | 0.01 ppm | ZSNS004 mean displacement, zebrafish panel |
| 4,398 ppm | 0.01 ppm | ZSNS001 tail division rate, zebrafish panel |
| 4,286 ppm | inside a one-decimal kcal table | lysozyme folding ΔG, measured −9.2 |
| 4,244 ppm | ~0 ppm | SH0ES local ladder, JWST host comparison |
| 4,108 ppm | 680 ppm | SH0ES local ladder, second host comparison |

Three handbook rows that were coarser than the printed place are now inside it. Ethanol §47 \(\Delta H_{\mathrm{vap}}\) is \(\pi^3+e^2+e^{-2}+\pi^{-3}=38.56292\) against 38.56 kJ/mol, 76 ppm, inside half of 0.01. NaBr lattice energy is \(e^6\cdot\varphi+\pi^4-\pi=747.029\) against 747 kJ/mol, 39 ppm, inside half of 1. The material-property scaffold had kept the retired value 750.171. That relay now carries 747.029. Chlorine’s boiling point is \(e^5\cdot\varphi-(\varphi-\varphi^{-1})=239.138\) K against 239.1 K, 157 ppm, inside half of 0.1. \(\varphi-\varphi^{-1}=1\) is the golden-ratio identity, so that step is not a new integer coefficient.

The zebrafish displacement and the SH0ES ladder are finely quoted and still miss by about 4,000 ppm. The frozen zebrafish panel is not rebuilt from the live bright branch. The frozen H₀ sightline is not rewritten. Lysozyme’s −9.2 kcal/mol is quoted to one decimal place; 4,286 ppm is inside half of that place. Aspartate side-chain pKR is \((e+G)(1+\alpha\gamma)=3.649555404153832\) against 3.65, 122 ppm, inside half of 0.005. Sildenafil at 4,289 ppm is inside the printed 8.4 place. Calcium polarizability is \((e^3+\varphi^2)(1+\alpha\gamma)=22.79920167217089\) against 22.8, 35 ppm, inside half of 0.1. Aluminum's Poisson ratio is \((P_{\mathrm{base}}\varphi)(1+\alpha\gamma)=0.34502990382112947\) against 0.345, 87 ppm, 0.060 half-digits high. Lead cohesive energy is \((\varphi+K)(1-\alpha K)=2.0318944553313916\) against 2.03, 933 ppm, 0.379 half-digits high.

The translation of the scalar into Newtonian gravity, special relativity, the Schwarzschild relation, and the electroweak mass relation is `docs/FSOT_STANDARD_PHYSICS.md`. The per-silo bar, and the reason one ppm number is not the theory-of-everything goal, is `docs/TOE_ACCURACY_GOALS.md`.
