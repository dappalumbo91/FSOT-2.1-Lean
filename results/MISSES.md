# Misses (mandatory)

A theory with zero misses and 477 greens looks like a filter. This file is the filter.

**Pin:** AEB2AD (file opened under D1D38A). Ledger B greens are **not** listed here. Ledger A / named-object misses are.

| ID | Ledger | Object | What missed | What we did not do |
|----|--------|--------|-------------|--------------------|
| H0-PLANCK-CLASS | A | wave-1 global \(100(1+S_{\mathrm{cosm}}A_{\mathrm{bleed}}/A_{\mathrm{in}})=68.445\) vs Planck 2018 67.4 | **Superseded object:** freeze scored the **global** CMB background on Planck-2018-only. Live CMB+BAO class is P-ACT-LB2 \(68.43\pm0.27\) (Louis et al. arXiv:2503.14452 eq. 41) at **0.022%**. SH0ES is the ladder object. | Did not put 0.99 back into \(K\). Did not rewrite Ledger A freeze. |
| LEDGER-B-REBUILD | B | catalog \(c=m(1+\|S\|\alpha)\) | 2733 `fsot_prediction` rows rescored under \(f=\alpha\) and derived \(D_{\mathrm{eff}}\). File gate still 477/477. Cite as correction, not ToE. | Did not keep the old \(f\) table |
| ALPHA-S-MZ | A | geometric \(1/(e\pi)\) vs PDG 0.1179 | **Superseded object:** \(1/(e\pi)\) has no QCD process (0.679%). Live coupling is \(2(\mathrm{POOF}/\psi_{\mathrm{con}})^2\) at **0.0075%** (aspiration). | Did not polish \(1/(e\pi)\). Did not rewrite Ledger A freeze. |
| OMEGA-B-H2-QM-CLASS | A | \(\lvert S_{\mathrm{cosm}}\rvert(1-S_{\mathrm{quant}})\) vs 0.02237 | **11.84%** after nest collapse (QM shares Particle \(D=5\)) | Did not re-assign QM to \(D=6\). **Superseded:** live object is Chemistry rung ([`docs/MATTER_BUDGET_OBJECT.md`](../docs/MATTER_BUDGET_OBJECT.md)) |
| GLUEBALL-0PP-TEPER | A | \(\varphi^2+1\) vs lattice \(m(0^{++})/\sqrt{\sigma}\) | **Superseded object:** 6.26% vs AT2020 3.405 was σ-scheme mismatch (1997 vs 2020 Wilson 0++ dip disagree by ~7%). Seed vs 1997 is **0.88%**. \(\sqrt{\sigma} r_0=1+1/(2\pi)\) vs 1.160(6). \(r_0 M=(\varphi^2+1)(1+1/(2\pi))\) vs Chen 4.16(11) is **0.82%** (0.31σ). | Did not retune \(\varphi^2+1\). Did not treat 6% as an FSOT miss. |
| GLUEBALL-F0-PAIR | A | gluonic \((\varphi^2+1)K\) vs \(f_0(1500)\); flavor \((\pi+1)K\) vs \(f_0(1710)\) | Flavor vs 1710 is **0.40%** green. Gluonic **1.520 GeV is inside** PDG T-matrix pole Re **1.43–1.53 GeV**. BW 1506±6 MeV **0.93%** is the lineshape leftover (not stuffed). | Did not retune \(K\). Did not move the BW central. Did not swap orifices. Not a glueball ID. |
| RIEMANN-N2-10 | A | Im(ρ_n) n=2..10 \(N(T)=n\), \(C\) locked by \(e/\gamma^3\) | **Superseded object:** signed leftover is prime-2 phase + POOF envelope. n=2..10 **0.62%** (beats C-lock 1.63%); oos n=11..20 **0.43%**, sign 19/19. Bound \(\lvert S\rvert\le 1/e\) holds. | Did not Euler-invert the full product. Did not replace 1/e. n=1 stays C-lock. Not RH. |
| WX-QUIET-FILL | B/dated | Clean quiet 24 h, uncoupled from storm latitude belt | **Superseded object:** 44078 (59.94°N) was lat-belt transfer to MDXA2 (59.44°N), \|Δlat\|<POOF·180/π. Window min_pres=1002.8. Uncoupled clean quiet **holds** (n=4). | Did not move 1010. Did not rewrite frozen JSON. Did not drop the kill to inflate storm skill. |
| SH0ES-LADDER | A | SH0ES ladder chain pooled | ~0.212% (aspiration 0.05% open) | Did not β-fit the ladder |
| CEPHEID-PL | A | Cepheid PL interconnect | ~0.135% (aspiration 0.05% open) | Did not retune ρ |
| NSE-CLAY | — | 3D NSE existence on R^3 | Kolmogorov 4/5 cascade is the 3D number (`1−1/D_particle`). Global-in-time existence is a different object. | Did not stuff existence into 4/5. |
| PREM-POISSON-ATOMIC | A/named | \(\nu=D_{\mathrm{atomic}}/25\) vs PREM lid | **Superseded object:** Atomic well \(D=6\) gave 5.43%. Continuum solid is Molecular \(D=7\), \(\nu=7/25=0.28\). | Did not put Atomic back to 7. |
| BSD-RANK | — | integer rank of general E | Parity map \(E\mapsto\) rank (mod 2) from \(w_E\) holds on first curves 0..4. No Weierstrass→ℤ. | \(e^{r-2}\mathrm{POOF}\) fails at rank 4 (234446a1). Did not `fsot_scaled`. |
| HODGE-CLASS | — | Primitive (2,2) on general X | CP²×CP² primitive (2,2) is algebraic (H1 H2). | \(\chi=L_2^2=9\). Did not steal 25−1 for K3. |

Dated public scoreboard kills live in [`dated_forecast_scores/REPORT.md`](dated_forecast_scores/REPORT.md). Do not rewrite issued JSON.

Update this file when an audit finds a new Ledger A miss or a named-object miss. Do not delete a miss because a later B residual went green.
