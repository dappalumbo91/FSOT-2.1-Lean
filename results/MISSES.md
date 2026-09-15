# Misses (mandatory)

A theory with zero misses and 477 greens looks like a filter. This file is the filter.

**Pin:** AEB2AD (file opened under D1D38A). Ledger B greens are **not** listed here. Ledger A / named-object misses are.

| ID | Ledger | Object | What missed | What we did not do |
|----|--------|--------|-------------|--------------------|
| H0-PLANCK-CLASS | A | wave-1 global \(100(1+S_{\mathrm{cosm}}A_{\mathrm{bleed}}/A_{\mathrm{in}})=68.445\) vs Planck 2018 67.4 | **Superseded object:** freeze scored the **global** CMB background on Planck-2018-only. Live CMB+BAO class is P-ACT-LB2 \(68.43\pm0.27\) (Louis et al. arXiv:2503.14452 eq. 41) at **0.022%**. SH0ES is the ladder object. | Did not put 0.99 back into \(K\). Did not rewrite Ledger A freeze. |
| LEDGER-B-REBUILD | B | catalog \(c=m(1+\|S\|\alpha)\) | 2733 `fsot_prediction` rows rescored under \(f=\alpha\) and derived \(D_{\mathrm{eff}}\). File gate still 477/477. Cite as correction, not ToE. | Did not keep the old \(f\) table |
| ALPHA-S-MZ | A | geometric \(1/(e\pi)\) vs PDG 0.1179 | **Superseded object:** \(1/(e\pi)\) has no QCD process (0.679%). Live coupling is \(2(\mathrm{POOF}/\psi_{\mathrm{con}})^2\) at **0.0075%** (aspiration). | Did not polish \(1/(e\pi)\). Did not rewrite Ledger A freeze. |
| OMEGA-B-H2-QM-CLASS | A | \(\lvert S_{\mathrm{cosm}}\rvert(1-S_{\mathrm{quant}})\) vs 0.02237 | **11.84%** after nest collapse (QM shares Particle \(D=5\)) | Did not re-assign QM to \(D=6\). **Superseded:** live object is Chemistry rung ([`docs/MATTER_BUDGET_OBJECT.md`](../docs/MATTER_BUDGET_OBJECT.md)) |
| GLUEBALL-0PP-TEPER | A | isolated \(\varphi^2+1\) vs Teper \(m/\sqrt{\sigma}\) | **Superseded object:** σ-units couple the loop to the flux tube: \(\varphi^2+1+\mathrm{POOF}/D_{\mathrm{particle}}\) vs 3.65 is **0.035%**. Chen vs AT2020-implied \(r_0 M\) is a **5%** scheme split (like 1997 vs AT2020). Isolated loop stays on the GeV pole and \(r_0\) product. | Did not retune \(\varphi^2+1\). Did not put \(\mathrm{POOF}/D\) on \(r_0\). |
| GLUEBALL-F0-PAIR | A | isolated \((\varphi^2+1)K\) vs \(f_0(1500)\) BW | **Superseded object:** BW is glue–flavor mixing, \(V=\mathrm{POOF}\cdot K\). Lower 2×2 eigenvalue vs 1506 is **0.24%**. Isolated 1.520 GeV stays the T-matrix pole (inside 1.43–1.53). Flavor vs 1710 unmixed **0.40%**. | Did not retune \(K\). Did not mix 1710. Not a glueball ID. |
| RIEMANN-N2-10 | A | Im(ρ_n) n=2..10 C-lock point-T | **Superseded object:** prime-2 sign + prime-3 cancellation of the POOF envelope. Isolated sign*POOF leftover 0.62% was missing p=3. Bound \(\lvert S\rvert\le 1/e\) holds. n=1 stays C-lock. | Did not Euler-invert the full product. Not RH. |
| WX-QUIET-FILL | B/dated | Clean quiet 24 h, uncoupled from storm latitude belt | **Superseded object:** 44078 (59.94°N) was lat-belt transfer to MDXA2 (59.44°N), \|Δlat\|<POOF·180/π. Window min_pres=1002.8. Uncoupled clean quiet **holds** (n=4). | Did not move 1010. Did not rewrite frozen JSON. Did not drop the kill to inflate storm skill. |
| SH0ES-LADDER | A | SH0ES ladder chain pooled | ~0.212% (aspiration 0.05% open) | Did not β-fit the ladder |
| CEPHEID-PL | A | Cepheid PL interconnect | ~0.135% (aspiration 0.05% open) | Did not retune ρ |
| NSE-CLAY | — | 3D NSE existence on R^3 | Kolmogorov 4/5 cascade is the 3D number (`1−1/D_particle`). Global-in-time existence is a different object. | Did not stuff existence into 4/5. |
| PREM-POISSON-ATOMIC | A/named | \(\nu=D_{\mathrm{atomic}}/25\) vs PREM lid | **Superseded object:** Atomic well \(D=6\) gave 5.43%. Continuum solid is Molecular \(D=7\), \(\nu=7/25=0.28\). | Did not put Atomic back to 7. |
| BSD-RANK | — | integer rank of a general E | First-curve leadings uniquely label ranks 0..4. Rank 4 is \((\varphi^2+1)\cdot e\cdot\mathrm{POOF}\) (missing loop fold, not \(e^2\)). Parity from \(w_E\). General E still produces the leading from its modular form. | Did not nearest-template arbitrary \(L(1)\) (17a1 would mis-fire). Did not \(\pi^2\cdot\mathrm{POOF}\). |
| HODGE-CLASS | — | Extra Hodge classes beyond \(C_{32}\) | \(C_8\) through \(C_{32}\) extra classes algebraic. Named remainder without K3: \(C_{36}\) (\(\mathrm{Bl}_{12}\mathbb{P}^2\)), \(C_{44}\) (Enriques). Then an infinite Hassett tail and general 4-folds. | Did not steal 25−1 for \(\chi(\mathrm{K3})=24\). Did not pad \(d=32\) as \(4\cdot 8\). |

Dated public scoreboard kills live in [`dated_forecast_scores/REPORT.md`](dated_forecast_scores/REPORT.md). Do not rewrite issued JSON.

Update this file when an audit finds a new Ledger A miss or a named-object miss. Do not delete a miss because a later B residual went green.
