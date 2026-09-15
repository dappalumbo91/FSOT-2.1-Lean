# Misses (mandatory)

A theory with zero misses and 477 greens looks like a filter. This file is the filter.

**Pin:** AEB2AD (file opened under D1D38A). Ledger B greens are **not** listed here. Ledger A / named-object misses are.

| ID | Ledger | Object | What missed | What we did not do |
|----|--------|--------|-------------|--------------------|
| H0-PLANCK-CLASS | A | \(H_0=100(1+S_{\mathrm{cosm}}A_{\mathrm{bleed}}/A_{\mathrm{in}})\) vs 67.4 | **1.55%** (inside kill band [66,69], outside 0.5%) | Did not put 0.99 back into \(K\) |
| LEDGER-B-REBUILD | B | catalog \(c=m(1+\|S\|\alpha)\) | 2733 `fsot_prediction` rows rescored under \(f=\alpha\) and derived \(D_{\mathrm{eff}}\). File gate still 477/477. Cite as correction, not ToE. | Did not keep the old \(f\) table |
| ALPHA-S-MZ | A | \(1/(e\pi)\) vs PDG 0.1179 | **0.679%** (outside 0.5%) | Did not add a decimal polish |
| OMEGA-B-H2-QM-CLASS | A | \(\lvert S_{\mathrm{cosm}}\rvert(1-S_{\mathrm{quant}})\) vs 0.02237 | **11.84%** after nest collapse (QM shares Particle \(D=5\)) | Did not re-assign QM to \(D=6\). **Superseded:** live object is Chemistry rung ([`docs/MATTER_BUDGET_OBJECT.md`](../docs/MATTER_BUDGET_OBJECT.md)) |
| GLUEBALL-0PP-TEPER | A | closed gluonic mode \(\varphi^2+1\) vs Teper 3.65±0.11 | **Superseded object:** old \(\varphi^2+e/\pi\) was the Atomic well look (4.57%, 1.5σ). Closed mode \(\varphi^2+1\) is inside Teper 1σ, **outside FSOT 0.5%** (accuracy WIP). | Did not retune 3.5. Λ_QCD is a different object. |
| RIEMANN-N2-10 | A | Im(ρ_n) n=2..10 spacing walk | Beats RvM (4.26% vs 5.64%) but **outside 0.5%** | Did not stuff into the green gate |
| WX-QUIET-FILL | B/dated | Quiet-fill 24 h persistence | 6/11 hold; OLCN6, 42058, 44078 | Did not drop quiet kills to inflate storm-sector |
| SH0ES-LADDER | A | SH0ES ladder chain pooled | ~0.212% (aspiration 0.05% open) | Did not β-fit the ladder |
| CEPHEID-PL | A | Cepheid PL interconnect | ~0.135% (aspiration 0.05% open) | Did not retune ρ |
| NSE-CLAY | — | 3D NSE smoothness | No native Clay theorem | 1D Stokes at Fluid nest D=12 (dark) is not that theorem |
| PREM-POISSON-ATOMIC | A/named | \(\nu=D_{\mathrm{atomic}}/25\) vs PREM lid | **Superseded object:** Atomic well \(D=6\) gave 5.43%. Continuum solid is Molecular \(D=7\), \(\nu=7/25=0.28\). | Did not put Atomic back to 7. |
| BSD-RANK | — | rank = ord L(E,s) | No native rank predictor | Named 11a1/37a1/389a1 only |
| HODGE-CLASS | — | Hodge classes algebraic | No native predictor | Named ℂP² and elliptic curve; did not steal 20 W for K3 |

Dated public scoreboard kills live in [`dated_forecast_scores/REPORT.md`](dated_forecast_scores/REPORT.md). Do not rewrite issued JSON.

Update this file when an audit finds a new Ledger A miss or a named-object miss. Do not delete a miss because a later B residual went green.
