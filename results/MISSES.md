# Misses (mandatory)

A theory with zero misses and 477 greens looks like a filter. This file is the filter.

**Pin:** AEB2AD (file opened under D1D38A). Ledger B greens are **not** listed here. Ledger A / named-object misses are.

| ID | Ledger | Object | What missed | What we did not do |
|----|--------|--------|-------------|--------------------|
| H0-PLANCK-CLASS | A | wave-1 global \(100(1+S_{\mathrm{cosm}}A_{\mathrm{bleed}}/A_{\mathrm{in}})=68.445\) vs Planck 2018 67.4 | **Superseded object:** freeze scored the **global** CMB background on Planck-2018-only. Live CMB+BAO class is P-ACT-LB2 \(68.43\pm0.27\) (Louis et al. arXiv:2503.14452 eq. 41) at **0.022%**. SH0ES is the ladder object. | Did not put 0.99 back into \(K\). Did not rewrite Ledger A freeze. |
| LEDGER-B-REBUILD | B | catalog \(c=m(1+\|S\|\alpha)\) | 2733 `fsot_prediction` rows rescored under \(f=\alpha\) and derived \(D_{\mathrm{eff}}\). File gate still 477/477. Cite as correction, not ToE. | Did not keep the old \(f\) table |
| ALPHA-S-MZ | A | geometric \(1/(e\pi)\) vs PDG 0.1179 | **Superseded object:** \(1/(e\pi)\) has no QCD process (0.679%). Live coupling is \(2(\mathrm{POOF}/\psi_{\mathrm{con}})^2\) at **0.0075%** (aspiration). | Did not polish \(1/(e\pi)\). Did not rewrite Ledger A freeze. |
| OMEGA-B-H2-QM-CLASS | A | \(\lvert S_{\mathrm{cosm}}\rvert(1-S_{\mathrm{quant}})\) vs 0.02237 | **11.84%** after nest collapse (QM shares Particle \(D=5\)) | Did not re-assign QM to \(D=6\). **Superseded:** live object is Chemistry rung ([`docs/MATTER_BUDGET_OBJECT.md`](../docs/MATTER_BUDGET_OBJECT.md)) |
| GLUEBALL-0PP-TEPER | A | closed gluonic mode \(\varphi^2+1\) vs Teper 3.65±0.11 | Lattice **construct** (quenched YM eigenstate), not an observed particle. String-unit seed inside Teper 1σ, **outside FSOT 0.5%**. | Did not retune 3.5. Did not treat Teper as a particle. |
| GLUEBALL-F0-PAIR | A | gluonic \((\varphi^2+1)K\) vs \(f_0(1500)\); flavor \((\pi+1)K\) vs \(f_0(1710)\) | **Superseded object:** 12.3% was the gluonic seed on the flavor particle. Flavor orifice \((\pi+1)K=1.740\,\mathrm{GeV}\) vs PDG 1733 MeV is **0.40%** (green). Gluonic vs 1506 MeV stays **0.93%** WIP. | Did not retune \(K\). Did not swap orifices. Did not restore \(4\sqrt{\sigma}\) or \(\varphi^3\). Not a glueball ID. |
| RIEMANN-N2-10 | A | Im(ρ_n) n=2..10 \(N(T)=n\), \(C\) locked by \(e/\gamma^3\) | Locked-\(C\) is **1.63%** vs RvM 5.64% (WIP). **S(T)** is the intra-Gram remainder after C-lock (Gram phase of every invert equals t1 — identity). \|S\|≤1/e on n=1..10 (max 0.321 at n=9). | Did not invert with a trig S(n). Did not restore 7/8. Not RH. |
| WX-QUIET-FILL | B/dated | Clean quiet 24 h, uncoupled from storm latitude belt | **Superseded object:** 44078 (59.94°N) was lat-belt transfer to MDXA2 (59.44°N), \|Δlat\|<POOF·180/π. Window min_pres=1002.8. Uncoupled clean quiet **holds** (n=4). | Did not move 1010. Did not rewrite frozen JSON. Did not drop the kill to inflate storm skill. |
| SH0ES-LADDER | A | SH0ES ladder chain pooled | ~0.212% (aspiration 0.05% open) | Did not β-fit the ladder |
| CEPHEID-PL | A | Cepheid PL interconnect | ~0.135% (aspiration 0.05% open) | Did not retune ρ |
| NSE-CLAY | — | 3D NSE smoothness | No native Clay theorem | 1D Stokes + von Kármán \(\kappa=A_{\mathrm{bleed}}/\varphi^2\) are not that theorem |
| PREM-POISSON-ATOMIC | A/named | \(\nu=D_{\mathrm{atomic}}/25\) vs PREM lid | **Superseded object:** Atomic well \(D=6\) gave 5.43%. Continuum solid is Molecular \(D=7\), \(\nu=7/25=0.28\). | Did not put Atomic back to 7. |
| BSD-RANK | — | rank = ord L(E,s) | No native rank predictor | \(L(11a1,1)=\sqrt{\varphi}/D_{\mathrm{particle}}\) is the rank-0 first object. 37a1/389a1 vanish. Did not `fsot_scaled(L)`. |
| HODGE-CLASS | — | Hodge classes algebraic | No native Hodge-class predictor | \(\chi(\mathbb{CP}^2)=\varphi^2+\varphi^{-2}=3\). Did not steal 25−1 for K3. Did not pad \(h^{1,1}=1\). |

Dated public scoreboard kills live in [`dated_forecast_scores/REPORT.md`](dated_forecast_scores/REPORT.md). Do not rewrite issued JSON.

Update this file when an audit finds a new Ledger A miss or a named-object miss. Do not delete a miss because a later B residual went green.
