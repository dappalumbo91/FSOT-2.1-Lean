# Misses (mandatory)

A theory with zero misses and 477 greens looks like a filter. This file is the filter.

**Pin:** AEB2AD (file opened under D1D38A). Ledger B greens are **not** listed here. Ledger A / named-object misses are.

| ID | Ledger | Object | What missed | What we did not do |
|----|--------|--------|-------------|--------------------|
| H0-PLANCK-CLASS | A | \(H_0=100(1+S_{\mathrm{cosm}}A_{\mathrm{bleed}}/A_{\mathrm{in}})\) vs 67.4 | **1.55%** (inside kill band [66,69], outside 0.5%) | Did not put 0.99 back into \(K\) |
| LEDGER-B-REBUILD | B | catalog \(c=m(1+\|S\|\alpha)\) | 2733 `fsot_prediction` rows rescored under \(f=\alpha\) and derived \(D_{\mathrm{eff}}\). File gate still 477/477. Cite as correction, not ToE. | Did not keep the old \(f\) table |
| ALPHA-S-MZ | A | geometric \(1/(e\pi)\) vs PDG 0.1179 | **Superseded object:** \(1/(e\pi)\) has no QCD process (0.679%). Live coupling is \(2(\mathrm{POOF}/\psi_{\mathrm{con}})^2\) at **0.0075%** (aspiration). | Did not polish \(1/(e\pi)\). Did not rewrite Ledger A freeze. |
| OMEGA-B-H2-QM-CLASS | A | \(\lvert S_{\mathrm{cosm}}\rvert(1-S_{\mathrm{quant}})\) vs 0.02237 | **11.84%** after nest collapse (QM shares Particle \(D=5\)) | Did not re-assign QM to \(D=6\). **Superseded:** live object is Chemistry rung ([`docs/MATTER_BUDGET_OBJECT.md`](../docs/MATTER_BUDGET_OBJECT.md)) |
| GLUEBALL-0PP-TEPER | A | closed gluonic mode \(\varphi^2+1\) vs Teper 3.65±0.11 | Lattice **construct** (quenched YM eigenstate), not an observed particle. String-unit seed inside Teper 1σ, **outside FSOT 0.5%**. | Did not retune 3.5. Did not treat Teper as a particle. |
| GLUEBALL-F0-PAIR | A | gluonic \((\varphi^2+1)K\) vs \(f_0(1500)\); flavor \((\pi+1)K\) vs \(f_0(1710)\) | **Superseded object:** 12.3% was the gluonic seed on the flavor particle. Flavor orifice \((\pi+1)K=1.740\,\mathrm{GeV}\) vs PDG 1733 MeV is **0.40%** (green). Gluonic vs 1506 MeV stays **0.93%** WIP. | Did not retune \(K\). Did not swap orifices. Did not restore \(4\sqrt{\sigma}\) or \(\varphi^3\). Not a glueball ID. |
| RIEMANN-N2-10 | A | Im(ρ_n) n=2..10 \(N(T)=n\), \(C\) locked by \(e/\gamma^3\) | **Superseded object:** Euler mean-spacing walk was public density from a better \(t_1\) (4.26%). Naive \(t_n\) scale lost (16.3%). Locked-\(C\) inversion is **1.63%** vs RvM 5.64% (8/9 zeros), **outside FSOT 0.5%** (accuracy WIP; \(S(T)\) not stuffed). | Did not restore 7/8 or the walk. Not RH. |
| WX-QUIET-FILL | B/dated | Quiet-fill 24 h persistence | 6/11 hold; OLCN6, 42058, 44078 | Did not drop quiet kills to inflate storm-sector |
| SH0ES-LADDER | A | SH0ES ladder chain pooled | ~0.212% (aspiration 0.05% open) | Did not β-fit the ladder |
| CEPHEID-PL | A | Cepheid PL interconnect | ~0.135% (aspiration 0.05% open) | Did not retune ρ |
| NSE-CLAY | — | 3D NSE smoothness | No native Clay theorem | 1D Stokes at Fluid nest D=12 (dark) is not that theorem |
| PREM-POISSON-ATOMIC | A/named | \(\nu=D_{\mathrm{atomic}}/25\) vs PREM lid | **Superseded object:** Atomic well \(D=6\) gave 5.43%. Continuum solid is Molecular \(D=7\), \(\nu=7/25=0.28\). | Did not put Atomic back to 7. |
| BSD-RANK | — | rank = ord L(E,s) | No native rank predictor | Named 11a1/37a1/389a1 only |
| HODGE-CLASS | — | Hodge classes algebraic | No native predictor | Named ℂP² and elliptic curve; did not steal 20 W for K3 |

Dated public scoreboard kills live in [`dated_forecast_scores/REPORT.md`](dated_forecast_scores/REPORT.md). Do not rewrite issued JSON.

Update this file when an audit finds a new Ledger A miss or a named-object miss. Do not delete a miss because a later B residual went green.
