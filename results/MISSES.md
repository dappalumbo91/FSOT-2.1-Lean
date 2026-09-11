# Misses (mandatory)

A theory with zero misses and 477 greens looks like a filter. This file is the filter.

**Pin:** D1D38A · Ledger B greens are **not** listed here. Ledger A / named-object misses are.

| ID | Ledger | Object | What missed | What we did not do |
|----|--------|--------|-------------|--------------------|
| H0-PLANCK-CLASS | A | \(H_0=100(1+S_{\mathrm{cosm}}A_{\mathrm{bleed}}/A_{\mathrm{in}})\) vs 67.4 | **1.55%** (inside kill band [66,69], outside 0.5%) | Did not put 0.99 back into \(K\) |
| LEDGER-B-REBUILD | B | catalog \(c=m(1+\|S\|f)\) | Stored 477/477 residuals are **D1D38A-era** (fitted \(f\)). Not yet rebuilt under \(f=\alpha\) | Did not keep the factor table to hold the green count |
| GLUEBALL-0PP-TEPER | A | \(m(0^{++})/\sqrt{\sigma}\) vs Teper 3.65±0.11 | 4.57% vs lattice precision (1.5σ; inside 2σ, outside 0.5%) | Did not retune 3.5 or add a coefficient |
| RIEMANN-N2-10 | A | Im(ρ_n) n=2..10 spacing walk | Beats RvM (4.26% vs 5.64%) but **outside 0.5%** | Did not stuff into the green gate |
| WX-QUIET-FILL | B/dated | Quiet-fill 24 h persistence | 6/11 hold; OLCN6, 42058, 44078 | Did not drop quiet kills to inflate storm-sector |
| SH0ES-LADDER | A | SH0ES ladder chain pooled | ~0.212% (aspiration 0.05% open) | Did not β-fit the ladder |
| CEPHEID-PL | A | Cepheid PL interconnect | ~0.135% (aspiration 0.05% open) | Did not retune ρ |
| NSE-CLAY | — | 3D NSE smoothness | No native Clay theorem | 1D Stokes at Fluid D=15 is not that theorem |
| BSD-RANK | — | rank = ord L(E,s) | No native rank predictor | Named 11a1/37a1/389a1 only |
| HODGE-CLASS | — | Hodge classes algebraic | No native predictor | Named ℂP² and elliptic curve; did not steal 20 W for K3 |

Dated public scoreboard kills live in [`dated_forecast_scores/REPORT.md`](dated_forecast_scores/REPORT.md). Do not rewrite issued JSON.

Update this file when an audit finds a new Ledger A miss or a named-object miss. Do not delete a miss because a later B residual went green.
