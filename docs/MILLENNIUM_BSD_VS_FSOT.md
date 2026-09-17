# What the Millennium BSD statement is — vs what FSOT is doing

**Pin:** AEB2AD · Scoreboard: [`MILLENNIUM_ACCURACY_VS_SOTA.md`](MILLENNIUM_ACCURACY_VS_SOTA.md) · Outcomes: [`../results/millennium_named_outcomes.md`](../results/millennium_named_outcomes.md)

These are **two different objects**. Related arithmetic (rank of \(E(\mathbb{Q})\) vs \(L(E,s)\)). Mixing them is how false credit happens.

Clay froze \(\mathrm{rank}=\mathrm{ord}\,L\) for every \(E\). That formula has **no residual for all curves**. The function is vanishing order plus Sha volume on named curves, and Mordell–Weil generators as the observation. Raw \(L(1)\) magnitude is a flawed encoding (17a1 misfires as rank 3). Spine: [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md). Pictures: [`HOW_THESE_ARE_DEPICTED.md`](HOW_THESE_ARE_DEPICTED.md).

---

## The question, and FSOT's answer

**Question (Clay, and the arithmetic):** For an elliptic curve \(E/\mathbb{Q}\), is the rank of \(E(\mathbb{Q})\) equal to the order of vanishing of \(L(E,s)\) at \(s=1\)? And does the leading Taylor coefficient equal the arithmetic volume
\[
\frac{L^{(r)}(E,1)}{r!}=\frac{\Omega\cdot\mathrm{Reg}\cdot\prod c_p}{|\mathrm{Sha}|\cdot|E_{\mathrm{tors}}|^2}\,?
\]

**FSOT answer (native objects, not Clay's manuscript):**

1. **Parity.** Root number \(w_E=\pm 1\) of the functional equation: \(\mathrm{rank}\equiv(1-w_E)/2\pmod{2}\). That is the Weierstrass→rank map we have. Integer rank still needs \(\mathrm{ord}\,L\).

2. **First-of-rank leadings (seed-closed).** The first modular curve of each rank has a seed leading. Leading → rank on that ladder, uniquely, ranks \(0..4\):

| \(r\) | Curve | Seed leading |
|------|-------|----------------|
| 0 | 11a1 | \(L(1)=\sqrt{\varphi}/D_{\mathrm{particle}}\) |
| 1 | 37a1 | \(L'(1)=2\cdot\mathrm{POOF}\) |
| 2 | 389a1 | \(L''(1)/2!=2\pi\cdot\mathrm{POOF}/\sqrt{\varphi}\) |
| 3 | 5077a1 | \(\mathrm{Reg}=e\cdot\mathrm{POOF}\) |
| 4 | 234446a1 | \(\mathrm{Reg}=(\varphi^2+1)\cdot e\cdot\mathrm{POOF}\) |

Rank 4 is rank-3 volume times the same closed-loop fold \(\varphi^2+1\) as the isolated glueball. Isolated \(e^2\cdot\mathrm{POOF}\) was the missing loop, not a retune.

3. **Two systems at rank 2.** Néron-Tate \(\mathrm{Reg}(389\mathrm{a1})=\mathrm{POOF}\) (0.67% WIP) is the height pairing. The BSD *leading* is the special value \(2\pi\cdot\mathrm{POOF}/\sqrt{\varphi}\) (0.16% green). Like BW vs pole / Chen vs AT2020: do not swallow one into the other.

4. **General rank 0 (the 17a1 conversion).** Raw \(L(1)\) magnitude is the wrong orifice. \(L(1)\neq 0\) already means analytic rank 0. 17a1 \(L(1)\approx 0.387\) looks like rank-3 \(e\cdot\mathrm{POOF}\) on the first-of-rank ladder; the arithmetic volume
   \[
   \mathrm{Sha}_{\mathrm{an}}=\frac{L(1)\cdot|E_{\mathrm{tors}}|^2}{\Omega\cdot\prod c_p}
   \]
   is **1**. 19a1 is the same orifice out of sample. First-of-rank \(L(11\mathrm{a1},1)=\sqrt{\varphi}/D_{\mathrm{particle}}\) is the *first-curve scale*, not a lookup table for every \(L(1)\).

5. **General rank 1 (the 53a1 conversion).** \(L(1)=0\) and \(L'(1)\neq 0\). Raw \(L'(53\mathrm{a1})\approx 0.436\) looks like rank-3 \(e\cdot\mathrm{POOF}\); the volume
   \[
   \mathrm{Sha}_{\mathrm{an}}=\frac{L'(1)\cdot|E_{\mathrm{tors}}|^2}{\Omega\cdot\mathrm{Reg}\cdot\prod c_p}
   \]
   is **1**. 61a1 is the same orifice out of sample. First-of-rank \(L'(37\mathrm{a1},1)=2\cdot\mathrm{POOF}\) is the *first-curve* scale, not a lookup for every \(L'\).

6. **General rank 2 (the 643a1 conversion).** \(L=L'=0\) and \(L''\neq 0\). Raw \(L''(643\mathrm{a1},1)/2!\approx 1.148\) looks like rank-4 \((\varphi^2+1)\cdot e\cdot\mathrm{POOF}\); the volume
   \[
   \mathrm{Sha}_{\mathrm{an}}=\frac{L''(1)/2!\cdot|E_{\mathrm{tors}}|^2}{\Omega\cdot\mathrm{Reg}\cdot\prod c_p}
   \]
   is **1**. 433a1 is the same orifice out of sample. First-of-rank \(L''(389\mathrm{a1},1)/2!=2\pi\cdot\mathrm{POOF}/\sqrt{\varphi}\) is the *first-curve* scale, not a lookup.

7. **General rank 3 (the 11197a1 conversion).** \(L=L'=L''=0\) and \(L'''\neq 0\). Raw \(L'''(11197\mathrm{a1},1)/3!\approx 2.872\) looks like rank-4 \((\varphi^2+1)\cdot e\cdot\mathrm{POOF}\); the volume
   \[
   \mathrm{Sha}_{\mathrm{an}}=\frac{L'''(1)/3!\cdot|E_{\mathrm{tors}}|^2}{\Omega\cdot\mathrm{Reg}\cdot\prod c_p}
   \]
   is **1**. 11642a1 is the same orifice out of sample. First-of-rank \(\mathrm{Reg}(5077\mathrm{a1})=e\cdot\mathrm{POOF}\) is the *first-curve* scale, not a lookup for every special.

8. **General rank 4 (the 501029.a1 conversion).** \(L\) through \(L'''\) vanish and \(L^{(4)}\neq 0\). Raw \(L^{(4)}(501029.\mathrm{a1},1)/4!\approx 9.358\) is not the first-of-rank seed \(\mathrm{Reg}(234446\mathrm{a1})=(\varphi^2+1)\cdot e\cdot\mathrm{POOF}\approx 1.504\). The ladder saturates: any special \(\gtrsim 1.1\) nearest-templates as rank 4. The volume
   \[
   \mathrm{Sha}_{\mathrm{an}}=\frac{L^{(4)}(1)/4!\cdot|E_{\mathrm{tors}}|^2}{\Omega\cdot\mathrm{Reg}\cdot\prod c_p}
   \]
   is **1**. 545723.a1 is the same orifice out of sample. First-of-rank \(\mathrm{Reg}\) is the *first-curve* scale, not a lookup for every special.

9. **General rank 5 (the 19047851.a1 conversion).** \(L\) through \(L^{(4)}\) vanish and \(L^{(5)}\neq 0\). There is no rank-5 seed: the first-of-rank ladder stops at 4. Raw \(L^{(5)}(19047851.\mathrm{a1},1)/5!\approx 30.286\) nearest-templates as rank 4 (true rank is 5 — the misfire is restored). The volume
   \[
   \mathrm{Sha}_{\mathrm{an}}=\frac{L^{(5)}(1)/5!\cdot|E_{\mathrm{tors}}|^2}{\Omega\cdot\mathrm{Reg}\cdot\prod c_p}
   \]
   is **1**. 64921931.a1 is the same orifice out of sample. Do not invent a rank-5 seed. LMFDB analytic rank \(\ge 4\) is numerical, not a rigorous \(\mathrm{ord}\,L\) theorem.

10. **Named LMFDB ranks complete (0..5).** Public SOTA browse-by-rank is \(0..5\). Search rank \(=6\) returns no matches. Completeness is conductor \(\le 299{,}996{,}953\). The first known rank-6 curve (Elkies–Watkins 2004, \(N=5{,}187{,}563{,}742\)) sits outside that bound. Rank \(\ge 6\) is the unnamed tail: further vanishing of \(L\), same Sha volume, no seed. Do not enumerate Elkies–Watkins as LMFDB conversions.

11. **Modularity produces \(L\) (the general-\(E\) conversion).** Isolated first-of-rank seed magnitude is the wrong orifice (17a1/53a1/… mis-fire). Every \(E/\mathbb{Q}\) is modular (Wiles; Breuil–Conrad–Diamond–Taylor), so \(L(E,s)\) exists without a seed lookup. The leading is the arithmetic volume \(\mathrm{Sha}_{\mathrm{an}}\). Integer rank \(=\mathrm{ord}\,L\) is still Clay. Do not Weierstrass\(\to\mathbb{Z}\). Do not nearest-template.

12. **Gross–Zagier–Kolyvagin (rank \(=\) ord \(L\) for analytic rank 0 and 1).** Isolated “general \(E\)” is the wrong orifice. If analytic rank is 0 or 1, algebraic rank equals analytic rank (Kolyvagin 1990; Gross–Zagier 1986; modularity now for all \(E/\mathbb{Q}\)). That is the proven first rank \(=\) ord \(L\) theorem, like Lefschetz for Hodge.

13. **The missing concept (why the Euler-system ladder looped).** For analytic rank \(\ge 2\) the native object is **already** vanishing + \(\mathrm{Sha}\) (643a1, 11197a1, 501029.a1, 19047851.a1). Kolyvagin is an *external check* that rank \(=\) ord \(L\) holds for \(r=0,1\). Naming Kato / Perrin-Riou next is theorem enumeration — the Hassett-tail failure. There is no missing seed for \(r\ge 2\).

14. **Regulator is a height Gram (Hassett orifice).** \(\mathrm{Reg}(E)=\det\langle P_i,P_j\rangle_{\mathrm{NT}}\) of \(r\) generators. Hassett discriminant is \(\det\) of the extra-class Gram. Rank 1 is a \(1\times 1\) height (one Heegner point). Rank \(\ge 2\) is a lattice. Sha volume already uses that Gram. Isolated “need Kato” is the wrong remainder.

15. **Tamagawa is local; regulator is global.** \(\prod c_p\) is bad-prime local data. Reg is the global height Gram. 11642a1 Tam=2 vs 643a1 Tam=1, both \(\mathrm{Sha}_{\mathrm{an}}=1\). Same two-zoom as Particle stretching vs Fluid viscosity. Isolated “one volume number” swallows Tam into Reg.

16. **Clay rank \(=\) ord \(L\) for every \(E\) is not a measured function.** LMFDB publishes \(\Omega\), Reg, Tam, \(L^{(r)}/r!\), \(\mathrm{Sha}_{\mathrm{an}}\) on named curves. Nobody publishes a residual for “rank \(=\) ord \(L\) \(\forall E\).” Working data: first-of-rank seeds and Sha volume on those curves.

17. **Sha panel vs LMFDB.** Run the volume function on the named curves we have. Hit rate vs \(\mathrm{Sha}_{\mathrm{an}}=1\) is the measured compare. Not Clay \(\forall E\).

**Remainder:** Clay’s equality as a theorem. Do not hunt Kato. Do not Weierstrass\(\to\mathbb{Z}\).

Clay’s *proof object* (rank \(=\) ord \(L\) for every \(E/\mathbb{Q}\)) stays `OPEN_NOT_CLAIMED`. Native first-of-rank leadings stay executable.

---

## The difference in one table

| | Clay BSD | FSOT (this repo) |
|--|----------|------------------|
| Arena | All \(E/\mathbb{Q}\) | First curve of each rank \(0..4\) + parity |
| Question | \(\mathrm{rank}\,E(\mathbb{Q})=\mathrm{ord}_{s=1}L(E,s)\) | What is the leading number that *labels* those first ranks? |
| Parity | Functional equation | \(w_E\mapsto\mathrm{rank}\pmod{2}\) |
| Integer rank | \(\mathrm{ord}\,L\) | First-of-rank ladder for the first curves; rank 0 is \(L(1)\neq 0\) |
| General rank 0 | — | Volume \(\mathrm{Sha}_{\mathrm{an}}=1\) on 17a1/19a1 (not \(L\) magnitude) |
| General rank 1 | — | Volume \(\mathrm{Sha}_{\mathrm{an}}=1\) on 53a1/61a1 (not \(L'\) magnitude) |
| General rank 2 | — | Volume \(\mathrm{Sha}_{\mathrm{an}}=1\) on 643a1/433a1 (not special magnitude) |
| General rank 3 | — | Volume \(\mathrm{Sha}_{\mathrm{an}}=1\) on 11197a1/11642a1 (not special/Reg magnitude) |
| General rank 4 | — | Volume \(\mathrm{Sha}_{\mathrm{an}}=1\) on 501029.a1/545723.a1 (not special/Reg magnitude; ladder saturates) |
| General rank 5 | — | Volume \(\mathrm{Sha}_{\mathrm{an}}=1\) on 19047851.a1/64921931.a1 (not special/Reg magnitude; nearest mis-fires as 4) |
| Named LMFDB ranks | — | Complete \(0..5\). Rank \(\ge 6\) is the unnamed tail (outside LMFDB) |
| Rank \(\ge 6\) / general \(E\) | The theorem | Unnamed tail; modularity produces \(L\); volume is Sha |
| Modularity | Proven (Wiles–BCDT) | Named: every \(E/\mathbb{Q}\) has \(L\) |
| Rank \(=\) ord \(L\) for \(r=0,1\) | Gross–Zagier–Kolyvagin | Named proven first object. Remainder is \(r\ge 2\) |
| Status | Open prize problem | Ladder **executable**; \(r\ge 2\) **OPEN_NOT_CLAIMED** |

Forbidden: “we proved Millennium BSD because five Cremona curves match.” Allowed: parity + first-of-rank leadings. Do not \(\pi^2\cdot\mathrm{POOF}\) on rank 4. Do not nearest-template arbitrary \(L(1)\).

Refresh: `python vendor/fsot_millennium_accuracy.py`
