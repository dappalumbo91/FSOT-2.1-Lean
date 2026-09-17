# How these problems are normally depicted — vs FSOT panels

**Pin:** AEB2AD · **Clay not claimed.**

People who attempt millenium problems publish a *picture of the formula*.
FSOT publishes a *picture of the function that has data*. Generate:

```powershell
python scripts/plot_millennium_panels.py
```

Output: [`../results/figures/`](../results/figures/). Not a Clay certificate.

Spine: [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md).

---

## Navier–Stokes

| Conventional picture | What it is trying to show | FSOT panel |
|----------------------|---------------------------|------------|
| Kolmogorov \(E(k)\sim k^{-5/3}\) log-log spectrum | Inertial-range cascade exists | \(4/5=1-1/D_{\mathrm{particle}}\) as an identity, not a slope fit |
| Taylor–Green vorticity isosurfaces | 3D stretching geometry | Energy and \(\max|\omega|\) vs time at seed \(\mu\); Euler \(\mu=0\) overplotted as the **wrong** orifice |
| Enstrophy blow-up cartoons / Riccati ODE | Possible finite-time singularity | \(\omega_0\) scan vs \(\mu/\mathrm{POOF}\) threshold **6/6**, labeled cartoon |
| Smoothness as a green/red lamp | Clay yes/no | **No panel.** That lamp has no residual |

Figures: `nse_spectrum_conventional_vs_fsot.png`, `nse_tg_energy_viscous_vs_euler.png`, `nse_omega0_scan.png`.

---

## Birch–Swinnerton-Dyer

| Conventional picture | What it is trying to show | FSOT panel |
|----------------------|---------------------------|------------|
| Graph of \(L(E,s)\) for real \(s\) near 1 | Order of vanishing \(=\) analytic rank | Schematic \(L(s)\sim c(s-1)^r\) for \(r=0,1,2\) — vanishing, not magnitude |
| Rank vs conductor scatter | How large rank gets | Named LMFDB ranks \(0..5\) complete; \(r\ge 6\) unnamed |
| BSD formula as a product of symbols | Volume equality | Sha vs 1 on named curves (**17/17**) |

Figures: `bsd_L_vanishing_orders.png`, `bsd_sha_panel.png`.

The misfire the original encoding invites: raw \(L(1)\) of 17a1 looks like a
rank-3 seed. The function is \(\mathrm{Sha}_{\mathrm{an}}=1\).

---

## Hodge

| Conventional picture | What it is trying to show | FSOT panel |
|----------------------|---------------------------|------------|
| Hodge diamond of a cubic 4-fold | Hodge numbers, middle \((2,2)\) | Diamond with \(h^{2,2}=21\), primitive 20, very-general rational rank 1 |
| Hassett divisors \(C_d\) on the moduli of cubics | Extra algebraic classes | Named \(C_8..C_{44}\) only; unnamed no-K3 has no Gram |
| \(\chi\) vs degree for hypersurfaces | Topology of named varieties | \(\chi\) vs Chern **9/9** (cubic 27, quartic 188, quintic 825, sextic 2610, abelian 0, …) |

Figures: `hodge_diamond_cubic.png`, `hodge_chi_panel.png`.

---

## Yang–Mills, Riemann, P vs NP

| Conventional picture | FSOT panel |
|----------------------|------------|
| Wilson loop area law; glueball spectrum \(m/\sqrt{\sigma}\) | Free-color damping \(a_0 e^{-\gamma t}\) plus isolated gap \(\varphi^2+1\) vs flux-tube orifice |
| Zeros as dots on the critical line \(\mathrm{Re}=1/2\) | Odlyzko dots plus FSOT \(t_1=e/\gamma^3\) on the same line. Not RH. |
| Complexity-class inclusion diagram | Grover \(1/2\) as a query exponent. Not P=?NP. |

Figures: `ym_free_color_damping.png`, `riemann_critical_line.png`.

---

## How to read a pair of panels

Left (or dashed) is **how the formula is drawn**. Right (or solid, seed-locked)
is **the function FSOT hit**. If the left picture has no table behind it
(smoothness lamp, “all \(E\)”, “all Hodge classes”), FSOT does not color it green.
That is the whole doctrine.
