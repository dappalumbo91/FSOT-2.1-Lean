# Millennium Prize track — official rules + FSOT native objects

**Pin:** D1D38A · **Clay Prize claimed:** **no**  
**Rules:** [CMI Millennium Prize Rules](https://www.claymath.org/millennium-problems/rules/) (Board, 26 September 2018)  
**PDF:** https://www.claymath.org/wp-content/uploads/2022/03/millennium_prize_rules_0.pdf  
**Problems:** https://www.claymath.org/millennium-problems/

This is an **attempt track**. Native identities go through Lean / Coq / Isabelle / F* / Rust / SMT.
The Clay *statement* of each unsolved problem stays `OPEN_NOT_CLAIMED` until that exact theorem is proved.

Yang–Mills detail: [`MILLENNIUM_YM_VS_FSOT.md`](MILLENNIUM_YM_VS_FSOT.md).

---

## How you actually win (CMI rules)

CMI **does not accept direct submission**. Before they will even *consider* a solution, **all three** must hold:

1. Published in a **Qualifying Outlet** (rules §6 — a short list of top journals; not a GitHub README and not arXiv alone).
2. **At least two years** since that publication.
3. **General acceptance** in the global mathematics community.

Then the CMI Scientific Advisory Board may consider it. CMI has sole authority to award. **$1 million** per problem. Poincaré is the one solved problem (Perelman, 2002–03; he declined the prize).

Machine flags in this repo (all honest zeros except remaining=6 and Poincaré historical):

| Flag | Live |
|------|------|
| `clay_problems_remaining` | 6 |
| `clay_direct_submit_accepted` | 0 |
| `clay_wait_years_required` | 2 |
| `clay_published_qualifying_outlet` | 0 |
| `clay_two_years_elapsed` | 0 |
| `clay_general_acceptance` | 0 |
| `clay_prize_awarded` | 0 |
| `poincare_solved_historical` | 1 |

---

## The six unsolved problems — Clay object vs FSOT native

| Problem | Clay object (what the prize pays for) | FSOT native (what we machine-check) | Status |
|---------|----------------------------------------|-------------------------------------|--------|
| **Yang–Mills existence and mass gap** | Continuum quantum YM on \(\mathbb{R}^4\) + Hamiltonian \(\Delta>0\) | Discrete path-sum \(w_{\mathrm{POOF}}+w_{\mathrm{hold}}=1\); free color damps; \(a_0/\gamma\) finite | Native **executable**. Clay **OPEN_NOT_CLAIMED** |
| **Navier–Stokes existence and smoothness** | Global smooth (or blow-up) solutions of 3D incompressible NSE | Seed-locked \(\mu(D_{\mathrm{eff}})>0\), \(c_s^2>0\), 1D continuity/momentum toy (`fsot_dynamics.py`) | Native **executable** (toy continuum). Clay **OPEN_NOT_CLAIMED** |
| **P versus NP** | Proof that P=NP or P≠NP | Grover exponent \(1/2\) (QI class); complexity-fold residual panel is **not** this theorem | Native **probe**. Clay **OPEN_NOT_CLAIMED** |
| **Riemann hypothesis** | All non-trivial zeros of \(\zeta\) have real part \(1/2\) | First-zero Im(\(\rho_1\)) seed probe \(e/\gamma^3\) vs 14.1347; critical line named as a goal | Native **probe**. Clay **OPEN_NOT_CLAIMED** |
| **Birch and Swinnerton-Dyer** | Rank of \(E(\mathbb{Q})\) equals order of vanishing of \(L(E,s)\) at \(s=1\) | No BSD theorem in-repo yet | **OPEN_TRACK** |
| **Hodge conjecture** | Hodge classes on a projective complex manifold are algebraic cycles (rational) | No Hodge theorem in-repo yet | **OPEN_TRACK** |

“We already solved some of these” is true **only** for the *native* column (YM path-sum, NS transport coefficients, Riemann first-zero residual, Grover 1/2). It is **false** for the Clay column. Same Perfect Host discipline: wrong object is a false kill *and* a false win.

---

## Why Navier–Stokes and P vs NP help the rest of FSOT

| Clay problem | Why the *native* work is load-bearing here |
|--------------|--------------------------------------------|
| Navier–Stokes | Weather 24 h windows, Earth fluid, \(\mu(D)\), process time — same continuum layer T2 |
| P vs NP | Checking a residual (green gate) vs inventing a coefficient — APPLY protocol is verification-easy; search-hard is still open as Clay |
| Yang–Mills | Confinement / no free color — already the uniqueness track |
| Riemann | Prime / zero probes sit in the seed catalog; RH itself is the line Re=1/2 for *all* zeros |

---

## Gauntlet

```powershell
python vendor/fsot_millennium_track.py
python scripts/run_goal_tracks_verification.py
```

Lean: `FSOT/Formal/MillenniumTrack.lean` (process rules + Grover 1/2 + critical-line *goal*).  
Numeric native rows export into the uniqueness spine (Coq / Isabelle / F* / Rust / SMT) with `clay_status=OPEN_NOT_CLAIMED`.

Kill: “we won a Millennium Prize.” Kill: GitHub as a Qualifying Outlet. Kill: stuffing a residual probe into the Clay statement.
