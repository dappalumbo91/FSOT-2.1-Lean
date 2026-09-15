# What the Millennium Navier–Stokes statement is — vs what FSOT is doing

**Pin:** AEB2AD · Scoreboard: [`MILLENNIUM_ACCURACY_VS_SOTA.md`](MILLENNIUM_ACCURACY_VS_SOTA.md) · Outcomes: [`../results/millennium_named_outcomes.md`](../results/millennium_named_outcomes.md)

These are **two different objects**. Related physics (3D incompressible flow). Mixing them is how false credit happens.

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

**Remainder:** whether viscosity keeps vorticity BKM-integrable. That *is* Clay smoothness. Do not stuff it into 4/5 or 1/3.

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
| Status | Open prize problem | Cascade **executable**; existence **OPEN_NOT_CLAIMED** |

Forbidden: “we proved Millennium NSE because 4/5 is exact.” Allowed: the cascade numbers and the BKM criterion.

Refresh: `python vendor/fsot_millennium_accuracy.py`
