# What the Millennium BSD statement is — vs what FSOT is doing

**Pin:** AEB2AD · Scoreboard: [`MILLENNIUM_ACCURACY_VS_SOTA.md`](MILLENNIUM_ACCURACY_VS_SOTA.md) · Outcomes: [`../results/millennium_named_outcomes.md`](../results/millennium_named_outcomes.md)

These are **two different objects**. Related arithmetic (rank of \(E(\mathbb{Q})\) vs \(L(E,s)\)). Mixing them is how false credit happens.

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

8. **Rank \(\ge 4\).** \(L'''(1)=0\) as well. Integer rank is still further vanishing of \(L\). No Weierstrass-coefficient → \(\mathbb{Z}\) seed map.

**Remainder:** \(\mathrm{ord}\,L\) for rank \(\ge 4\) without computing the modular form.

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
| Rank \(\ge 4\) | The theorem | Still further vanishing of \(L\) |
| Status | Open prize problem | Ladder **executable**; general \(E\) **OPEN_NOT_CLAIMED** |

Forbidden: “we proved Millennium BSD because five Cremona curves match.” Allowed: parity + first-of-rank leadings. Do not \(\pi^2\cdot\mathrm{POOF}\) on rank 4. Do not nearest-template arbitrary \(L(1)\).

Refresh: `python vendor/fsot_millennium_accuracy.py`
