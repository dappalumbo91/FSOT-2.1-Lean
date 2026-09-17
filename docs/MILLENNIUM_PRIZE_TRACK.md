# Millennium Prize track — official rules + FSOT native objects

**Pin:** AEB2AD · **Clay Prize claimed:** **no**  
**Rules:** [CMI Millennium Prize Rules](https://www.claymath.org/millennium-problems/rules/) (Board, 26 September 2018)  
**PDF:** https://www.claymath.org/wp-content/uploads/2022/03/millennium_prize_rules_0.pdf  
**Problems:** https://www.claymath.org/millennium-problems/

This is an **attempt track**. Native identities go through Lean / Coq / Isabelle / F* / Rust / SMT.
The Clay *statement* of each unsolved problem stays `OPEN_NOT_CLAIMED` until that exact theorem is proved.

**Formula vs function:** Clay asked a frozen manuscript. FSOT answers the question that manuscript was pointing at by hitting the function that has data. Full explanation: [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md). Pictures: [`HOW_THESE_ARE_DEPICTED.md`](HOW_THESE_ARE_DEPICTED.md). Gaps: [`FINDINGS.md`](FINDINGS.md).

Question/answer (not vs-SOTA residuals):  
Yang–Mills [`MILLENNIUM_YM_VS_FSOT.md`](MILLENNIUM_YM_VS_FSOT.md) ·  
Navier–Stokes [`MILLENNIUM_NSE_VS_FSOT.md`](MILLENNIUM_NSE_VS_FSOT.md) ·  
BSD [`MILLENNIUM_BSD_VS_FSOT.md`](MILLENNIUM_BSD_VS_FSOT.md) ·  
Hodge [`MILLENNIUM_HODGE_VS_FSOT.md`](MILLENNIUM_HODGE_VS_FSOT.md).  
Named-function outcomes: [`../results/millennium_named_outcomes.md`](../results/millennium_named_outcomes.md).

---

## The questions, and FSOT's answers

Each Clay problem is a *question about reality*. The prize manuscript is one encoding of that question — and can be the wrong orifice. FSOT answers the question in native objects that have tables. The prize manuscript is a different object.

| Problem | Question | FSOT answer | Still open (native) |
|---------|----------|-------------|---------------------|
| **Yang–Mills** | Why no massless gluons / free quarks? | Gap scale \(m/\sqrt{\sigma}=\varphi^2+1\). Free color is not an attractor. Teper is a check of the σ-unit orifice \(\varphi^2+1+\mathrm{POOF}/D\), not the question. | Clay Wightman theory on \(\mathbb{R}^4\) |
| **Navier–Stokes** | Do 3D NSE solutions stay smooth, or can stretching blow up? | Working data: 4/5, 3/2, 1/3, \(\kappa\). Clay smoothness is not a measured function. | Clay yes/no (no public residual) |
| **Riemann** | Do all non-trivial zeros have real part \(1/2\)? | \(t_1=e/\gamma^3\); C-lock; \(\lvert S\rvert\le 1/e\); typical \(\lvert S\rvert=\mathrm{POOF}\); signed jitter prime-2+3. | The line for *all* zeros |
| **BSD** | Is \(\mathrm{rank}\,E(\mathbb{Q})=\mathrm{ord}_{s=1}L(E,s)\)? | Working data: LMFDB Sha and first-of-rank seeds. Clay equality ∀E is not a measured function. | Clay theorem (no residual for all \(E\)) |
| **Hodge** | Are Hodge classes algebraic cycles? | Working data: \(\chi\)/Gram of named varieties. Algebraicity without a cycle is not a measured function. | Clay theorem (cycle is the measurement) |
| **P vs NP** | Is verifying as hard as searching? | Grover \(1/2\) (QI); Cook–Levin SAT named. | Search vs verification as Clay |

---

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
| **Navier–Stokes existence and smoothness** | Global smooth (or blow-up) solutions of 3D incompressible NSE | 1D Stokes, \(\kappa\), 2D enstrophy, Kolmogorov \(4/5\), Kraichnan \(3/2\), Onsager \(1/3\), BKM. Existence on \(\mathbb{R}^3\) is BKM-integrability of stretching. | Native **probe**. Clay **OPEN_NOT_CLAIMED** |
| **P versus NP** | Proof that P=NP or P≠NP | Grover \(1/2\) (QI); Cook–Levin SAT named. Not P=?NP. | Native **probe**. Clay **OPEN_NOT_CLAIMED** |
| **Riemann hypothesis** | All non-trivial zeros of \(\zeta\) have real part \(1/2\) | C-lock; \(\lvert S\rvert\le 1/e\); typical \(\lvert S\rvert=\mathrm{POOF}\); signed jitter \(\mathrm{sign}(\sin(T\ln 2))\cdot\mathrm{POOF}\) envelope. Not RH. | Native **probe**. Clay **OPEN_NOT_CLAIMED** |
| **Birch and Swinnerton-Dyer** | Rank of \(E(\mathbb{Q})\) equals order of vanishing of \(L(E,s)\) at \(s=1\) | Parity from \(w_E\). First-of-rank leadings 0..4. Rank 0..4 vanishing not magnitude. \(\mathrm{Reg}(234446a1)=(\varphi^2+1)\cdot e\cdot\mathrm{POOF}\). General \(E\) still needs \(\mathrm{ord}\,L\). | Native **probe**. Clay **OPEN_NOT_CLAIMED** |
| **Hodge conjecture** | Hodge classes on a projective complex manifold are algebraic cycles (rational) | Lefschetz; associated K3; named extra classes \(C_8\) through \(C_{44}\) algebraic. Remainder: infinite unnamed Hassett tail, general 4-folds. | Native **probe**. Clay **OPEN_NOT_CLAIMED** |

“We already solved some of these” is true **only** for the *native* column (YM path-sum, NS transport coefficients, Riemann first-zero residual, Grover 1/2). It is **false** for the Clay column. Same Perfect Host discipline: wrong object is a false kill *and* a false win.

Accuracy vs public SOTA on those *functions* (not the Prize): [`MILLENNIUM_ACCURACY_VS_SOTA.md`](MILLENNIUM_ACCURACY_VS_SOTA.md). Teper is a check of the σ-unit glueball orifice, not the mass-gap question. ECMWF is not beaten.

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
python scripts/reproduce.py
python scripts/plot_millennium_panels.py
```

Authority (FSOT 2.1) still runs `python scripts/run_goal_tracks_verification.py`.

Lean: `FSOT/Formal/MillenniumTrack.lean` (process rules + Grover 1/2 + critical-line *goal* + BSD first-of-rank \(n=5\) + named Hodge no-K3 \(n=9\)).  
Numeric native rows export into the uniqueness spine (Coq / Isabelle / F* / Rust / SMT) with `clay_status=OPEN_NOT_CLAIMED`. Named-function outcomes: [`../results/millennium_named_outcomes.md`](../results/millennium_named_outcomes.md).

Kill: “we won a Millennium Prize.” Kill: GitHub as a Qualifying Outlet. Kill: stuffing a residual probe into the Clay statement.
