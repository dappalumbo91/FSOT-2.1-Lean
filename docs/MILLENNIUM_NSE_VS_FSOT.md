# What the Millennium Navier–Stokes statement is — vs what FSOT is doing

**Pin:** AEB2AD · Scoreboard: [`MILLENNIUM_ACCURACY_VS_SOTA.md`](MILLENNIUM_ACCURACY_VS_SOTA.md) · Outcomes: [`../results/millennium_named_outcomes.md`](../results/millennium_named_outcomes.md)

These are **two different objects**. Related physics (3D incompressible flow). Mixing them is how false credit happens.

Clay froze a smoothness yes/no. That formula has **no public residual**. The function is 3D stretching versus viscosity, against CRC/NIST/US1976 and viscous DNS. FSOT does not depend on the Clay encoding being the unique correct write-up. Spine: [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md). Pictures: [`HOW_THESE_ARE_DEPICTED.md`](HOW_THESE_ARE_DEPICTED.md).

---

## The question, and FSOT's answer

**Question (Clay, and the physics):** Given smooth, divergence-free, finite-energy initial data on \(\mathbb{R}^3\) (or \(\mathbb{T}^3\)), does the 3D incompressible Navier–Stokes solution stay smooth for all time, or can vortex stretching blow it up in finite time?

**FSOT answer (native objects, not Clay's manuscript):**

1. **2D (no stretching).** \(\omega\cdot\nabla v\equiv 0\). Enstrophy is conserved. Global existence is the proven first NSE-type theorem. Inverse energy cascade coefficient is the same Kolmogorov dimension formula at spatial \(d=2\):
   \[
   \frac{12}{d(d+2)}=\frac{3}{2}.
   \]
   Here \(d+2=4\) is geometry. Do **not** put \(D_{\mathrm{particle}}\) on 2D.

2. **3D cascade (stretching exists).** The inertial-range flux is
   \[
   \frac{12}{d(d+2)}\Big|_{d=3}=\frac{12}{3\,D_{\mathrm{particle}}}=\frac{4}{5}=1-\frac{1}{D_{\mathrm{particle}}}.
   \]
   \(d+2=D_{\mathrm{particle}}=5\): stretching sees the particle floor. That is the 3D *number*. Energy goes to small scales at a finite rate because stretching exists.

3. **Euler regularity threshold.** Same cascade, Hölder form: \(\delta u\sim(\varepsilon r)^{1/3}\). Onsager: Euler conserves energy if Hölder \(>1/d=1/3\), and can dissipate if rougher. Not \(1/D_{\mathrm{particle}}\) (wrong orifice). NSE has viscosity; this is the *inviscid* flux threshold.

4. **Stretching criterion.** Beale–Kato–Majda: the solution blows up at \(T_*\) if and only if \(\int_0^{T_*}\|\omega\|_\infty\,dt\) diverges. Mean cascade (4/5, 1/3) does not control \(\|\omega\|_\infty\).

5. **L² cascade is not L∞ existence (the conversion).** Isolated \(4/5\) is the wrong orifice for smoothness: Kolmogorov \(\varepsilon=\nu\langle\lvert\omega\rvert^2\rangle\) is mean \(L^2\) dissipation. 1D Stokes \(\partial_t v=-\mu k^2 v\) damps linear modes (\(\mu(D)>0\), Fluid dark). 3D Sobolev does not give \(L^\infty\) from \(H^1\). BKM is the \(L^\infty\) stretching channel. Do not stuff existence into \(4/5\) or \(1/3\).

6. **BKM magnitude is not direction.** Isolated \(\|\omega\|_\infty\) is the wrong orifice for the remaining channel. Constantin–Fefferman: if the vorticity direction \(\xi=\omega/\lvert\omega\rvert\) is Lipschitz in high-vorticity regions, there is no blow-up. Magnitude (BKM) and direction (CF) are two systems. Do not swallow one into the other.

7. **The missing concept (why the criterion-ladder looped).** Isolated regularity names (4/5, BKM, CF, next Lipschitz…) are **one zoom**. Stretching is the Particle-floor zoom (\(4/5=1-1/D_{\mathrm{particle}}\); 2D \(3/2\) does **not** use \(D_{\mathrm{particle}}\)). Viscosity is the Fluid-tank zoom (\(\mu(D)>0\), Stokes, **dark**). Same orifice, two zooms — Nuclear/Particle, glueball \(\varphi^2+1\) vs \(\mathrm{POOF}/D\). The valve \(\mathrm{POOF}/(\mathrm{POOF}+\mathrm{SUCTION})\) is production vs hold, **not** an existence number. Naming the next PDE theorem is the Hassett-tail failure.

8. **Enstrophy budget is two terms, not a 4/5 analog.** \(\frac{d}{dt}\int\lvert\omega\rvert^2/2=\int\omega_i S_{ij}\omega_j-\nu\int\lvert\nabla\omega\rvert^2\). 2D production vanishes. 3D production *is* stretching. Mean \(4/5\) is energy flux, not enstrophy conservation. Isolated “enstrophy 4/5” is the wrong orifice.

9. **Helicity is a 3D Euler invariant, not existence.** \(H=\int v\cdot\omega\). Conserved for Euler (\(\mu=0\)). NSE dissipates it through Fluid viscosity. 2D stretching vanishes, so helicity is not the 2D orifice. Isolated “helicity conservation ⇒ smooth” is inviscid stuffing.

10. **Clay smoothness is not a measured function.** Lab and DNS publish inertial-range flux and wall \(\kappa\). Nobody publishes a % error on “is NSE smooth?” Isolated “solve existence” looks for a residual that does not exist. Working data: \(4/5\), \(3/2\), \(1/3\) exact; \(\kappa\) vs log-law scatter.

11. **3D viscous NSE on \(\mathbb{T}^3\), not 2D and not Euler.** Spectral Taylor–Green, seed-locked \(\mu\). Stretching \(\omega_i S_{ij}\omega_j\) is 3D. Energy and \(\max|\omega|\) decay (same direction as viscous TG DNS at this Re). **3D Euler (\(\mu=0\)) is the wrong orifice:** Clay is viscous NSE; a \(16^3\) Euler run does not conserve energy, so it is not a proof Euler is singular. Isolated \(\mu=0\) is inviscid stuffing (same miss as helicity conservation).

12. **Reality bar (observables, not other theories).** Lab \(\kappa=A_{\mathrm{bleed}}/\varphi^2\) vs pipe/channel 0.40. CRC/ISO \(c_{\mathrm{water}}/c_{\mathrm{air}}=e+\varphi\). Diatomic \(\gamma=1+2/D_{\mathrm{particle}}=7/5\). 3D viscous TG decays. Euler \(\mu=0\) is not a lab table.

**Remainder:** Clay’s yes/no for **all** smooth data on \(\mathbb{R}^3\). Lab tables plus one TG run are not that theorem. Do not substitute 2D. Do not treat Euler as the standard.

Clay’s *proof object* (global smooth solutions on \(\mathbb{R}^3\)) stays `OPEN_NOT_CLAIMED`. Native cascade numbers stay executable.

---

## The difference in one table

| | Clay NSE | FSOT (this repo) |
|--|----------|------------------|
| Arena | 3D incompressible NSE on \(\mathbb{R}^3\) or \(\mathbb{T}^3\) | Seed-locked cascade identities + BKM criterion |
| Question | Global smooth / finite-time blow-up | What is the cascade number, and what is the blow-up criterion? |
| 2D | Proven (enstrophy) | Enstrophy named; Kraichnan \(3/2\) exact |
| 3D number | — | Kolmogorov \(4/5=1-1/D_{\mathrm{particle}}\) exact |
| Hölder | Onsager (Euler) | \(1/d=1/3\) exact |
| Blow-up test | BKM | Named connective criterion |
| L² vs L∞ | — | \(4/5\) is mean flux; Stokes damps linear; BKM is \(\|\omega\|_\infty\) |
| Magnitude vs direction | — | \(\|\omega\|\) is BKM; \(\xi=\omega/\lvert\omega\rvert\) is Constantin–Fefferman |
| Two zooms | — | Particle stretching vs Fluid viscosity (dark); valve is not existence |
| Status | Open prize problem | Cascade **executable**; existence **OPEN_NOT_CLAIMED** |

Forbidden: “we proved Millennium NSE because 4/5 is exact.” Allowed: two zooms + valve. Do not stuff \(L^2\) into \(L^\infty\), \(\|\omega\|\) into \(\xi\), or the valve into existence. Do not name the next Lipschitz theorem.

Refresh: `python vendor/fsot_millennium_accuracy.py`
