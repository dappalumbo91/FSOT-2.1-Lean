# Millennium named-function outcomes (this arc)

**Pin:** AEB2AD. **Not a Clay Prize.** GitHub is not a Qualifying Outlet. Ledger A freeze not rewritten.

Scoreboard: `python vendor/fsot_millennium_accuracy.py` → [`docs/MILLENNIUM_ACCURACY_VS_SOTA.md`](../docs/MILLENNIUM_ACCURACY_VS_SOTA.md).
Gauntlet: `python scripts/run_goal_tracks_verification.py` (Lean / Coq / Isabelle / F* / Rust / SMT uniqueness spine).

Question/answer (not vs-SOTA): [`MILLENNIUM_YM_VS_FSOT.md`](../docs/MILLENNIUM_YM_VS_FSOT.md) · [`MILLENNIUM_NSE_VS_FSOT.md`](../docs/MILLENNIUM_NSE_VS_FSOT.md) · [`MILLENNIUM_BSD_VS_FSOT.md`](../docs/MILLENNIUM_BSD_VS_FSOT.md) · [`MILLENNIUM_HODGE_VS_FSOT.md`](../docs/MILLENNIUM_HODGE_VS_FSOT.md).

## Live tally

| Bucket | n |
|--------|---|
| Comparable | 70 |
| Beats/meets SOTA | 73 |
| Green 0.5% | 67 |
| Aspiration 0.05% | 57 |
| SOTA beat, accuracy WIP | 4 |
| Next dig (open tracks) | 3 |
| Clay remaining | 6, not claimed |
| ECMWF beaten | 0 |

WIP SOTA beats (right object, outside 0.5%): C-lock Riemann panel, typical \(\lvert S\rvert=\mathrm{POOF}\), Chen \(r_0 M\), Néron-Tate \(\mathrm{Reg}(389\mathrm{a1})\).

## BSD — first-of-rank ladder 0..4

| Rank | Curve | Seed leading | vs LMFDB |
|------|-------|--------------|----------|
| 0 | 11a1 | \(\sqrt{\varphi}/D_{\mathrm{particle}}\) | 0.22% green |
| 1 | 37a1 | \(2\cdot\mathrm{POOF}\) | 0.315% green |
| 2 | 389a1 | special \(2\pi\cdot\mathrm{POOF}/\sqrt{\varphi}\) | 0.156% green (Reg vs POOF 0.67% is the other half of that split) |
| 3 | 5077a1 | \(\mathrm{Reg}=e\cdot\mathrm{POOF}\) | 0.015% aspiration |
| 4 | 234446a1 | \(\mathrm{Reg}=(\varphi^2+1)\cdot e\cdot\mathrm{POOF}\) | 0.341% green |

Rank 4 was isolated \(e^2\cdot\mathrm{POOF}\) (24.6%). The missing fold is the same closed loop as the glueball \(\varphi^2+1\). Tamagawa 2 is the extra prime in the conductor, not a retune of volume. Integer rank classifier unique on these five. General \(E\) still produces the leading from its modular form — do not nearest-template arbitrary \(L(1)\).

## BSD — general rank 0..5 is vanishing, not magnitude

| Rank | Conversion curve | Wrong orifice | Volume |
|------|------------------|---------------|--------|
| 0 | 17a1 (19a1 oos) | raw \(L(1)\) looks like rank-3 \(e\cdot\mathrm{POOF}\) | \(\mathrm{Sha}_{\mathrm{an}}=1\) |
| 1 | 53a1 (61a1 oos) | raw \(L'\) looks like rank-3 \(e\cdot\mathrm{POOF}\) | \(\mathrm{Sha}_{\mathrm{an}}=1\) |
| 2 | 643a1 (433a1 oos) | raw \(L''/2!\) looks like rank-4 \((\varphi^2+1)\cdot e\cdot\mathrm{POOF}\) | \(\mathrm{Sha}_{\mathrm{an}}=1\) |
| 3 | 11197a1 (11642a1 oos) | raw \(L'''/3!\) looks like rank-4 \((\varphi^2+1)\cdot e\cdot\mathrm{POOF}\) | \(\mathrm{Sha}_{\mathrm{an}}=1\) |
| 4 | 501029.a1 (545723.a1 oos) | raw \(L^{(4)}/4!\approx 9.36\) is not the rank-4 seed \(1.50\); ladder saturates | \(\mathrm{Sha}_{\mathrm{an}}=1\) |
| 5 | 19047851.a1 (64921931.a1 oos) | raw \(L^{(5)}/5!\approx 30.29\) nearest-templates as rank 4; no r=5 seed | \(\mathrm{Sha}_{\mathrm{an}}=1\) |

Named LMFDB ranks **complete** \(0..5\). Rank \(\ge 6\) is the unnamed tail (Elkies–Watkins \(N=5{,}187{,}563{,}742\) outside LMFDB). Remainder: general \(E\) without the modular form.

## Hodge — named extra classes without K3 complete

Public SOTA names surfaces through Nuer \(C_{44}\). Algebraicity here is “the extra class is that surface.” Associated K3 (when it exists) already reduces to Lefschetz (1,1).

| \(d\) | Extra class | Seed disc | No K3 because |
|------|-------------|-----------|----------------|
| 8 | plane | \(F_6\) | \(4\mid d\) |
| 12 | cubic scroll | \(L_2 L_4-L_2^2\) | \(4\mid d\) |
| 18 | elliptic ruled | \(L_2 L_6-(2L_2)^2\) | \(9\mid d\) |
| 20 | Veronese | \(L_2(L_2 L_3)-L_3^2\) | \(4\mid d\) |
| 24 | nodal sextic del Pezzo | \(L_2(L_6+2)-(2L_2)^2\) | \(4\mid d\) |
| 30 | \(\mathrm{Bl}_{10}\mathbb{P}^2\) (Coble) | Nuer Gram | \(5\equiv 2\pmod{3}\) |
| 32 | \(\mathrm{Bl}_{11}\mathbb{P}^2\) | Nuer Gram | \(4\mid d\) |
| 36 | \(\mathrm{Bl}_{12}\mathbb{P}^2\) | Nuer Gram | \(4\mid d\) and \(9\mid d\) |
| 44 | Fano Enriques | \(L_2(6H^2-\chi)-H^2{}^2\) | \(11\equiv 2\pmod{3}\) |

Did not enumerate the infinite unnamed Hassett tail. Did not steal \(25-1\) for \(\chi(\mathrm{K3})=24\).

## NSE — cascade numbers (existence still open)

| Object | Seed | Meaning |
|--------|------|---------|
| 3D energy cascade | \(12/(3 D_{\mathrm{particle}})=4/5\) | Stretching exists; \(d+2=D_{\mathrm{particle}}\) |
| 2D inverse cascade | \(12/(d(d+2))=3/2\) at \(d=2\) | No stretching; \(d+2=4\) is geometry, not \(D_{\mathrm{particle}}\) |
| Euler Hölder threshold | \(1/d=1/3\) | Onsager: same cascade as 4/5, \(\delta u\sim(\varepsilon r)^{1/3}\) |
| Stretching criterion | BKM | Blow-up iff \(\int\|\omega\|_\infty dt\) diverges |

Clay question: do smooth finite-energy 3D NSE solutions exist for all time? FSOT answer so far: the cascade numbers and the BKM criterion. Remainder is whether viscosity keeps vorticity BKM-integrable. Not stuffed into 4/5.

## System connective (not millenium-only)

Rank-4 volume uses the **same** \(\varphi^2+1\) closed-loop fold as the isolated glueball \(m(0++)/\sqrt{\sigma}\). That is APPLY step 2 (interacting systems), not a new knob.

## Why these three kept looping

We were naming the next public theorem (BKM → CF → next Lipschitz; Kolyvagin → Kato; \(C_{44}\) → \(C_{48}\)) and calling it a conversion. That is the **Hassett-tail failure**: enumerate until it looks green. The miss was a concept, not a missing name.

| Track | Isolated (wrong remainder) | Missing concept | Native object now |
|-------|----------------------------|-----------------|-------------------|
| NSE | Next regularity criterion | Stretching and viscosity are **two zooms of one orifice** (Particle floor vs Fluid tank, dark), coupled by the valve — APPLY interacting systems, same miss as isolated glueball \(\varphi^2+1\) | Two-zoom split executable. Valve is **not** existence |
| BSD \(r\ge 2\) | Next Euler system | Vanishing+\(\mathrm{Sha}\) **already is** the native object (643a1…19047851.a1). Kolyvagin is an external check for \(r=0,1\) | Volume executable. Kato would be enumeration |
| Hodge unnamed | Next named surface | Seeds attach to **named varieties**. No surface name ⇒ no Gram seed | No-seed diagnosis executable. \(C_{48}\) would be enumeration |

## What actually works vs data (the inversion)

Clay asked for objects that have **no public residual**. FSOT already hits the functions that *do* have data. Isolated “solve the hurdle” looks for a measurement that is not there.

| Track | Public data (works) | Clay remainder (no table) |
|-------|---------------------|---------------------------|
| NSE | Kolmogorov \(4/5\), Kraichnan \(3/2\), Onsager \(1/3\), von Kármán \(\kappa\) vs lab/DNS/log-law | “Is 3D NSE smooth?” — no % error exists |
| BSD | LMFDB \(\Omega\), Reg, Tam, \(L^{(r)}/r!\), \(\mathrm{Sha}_{\mathrm{an}}\) on named curves | “rank \(=\) ord \(L\) \(\forall E\)” — no residual for all curves |
| Hodge | \(\chi\)/Gram of named varieties (hypersurfaces, HK Fano, abelian \(\chi=0\)) | Algebraicity with no named cycle — the cycle *is* the measurement |

## Still open (Clay leftover — not a missing seed)

| ID | Object | Why it stayed | Kill |
|----|--------|---------------|------|
| NSE-CLAY | 3D NSE existence on \(\mathbb{R}^3\) | Not a measured function. Working: 4/5, 3/2, 1/3, \(\kappa\). | Stuffing cascade numbers into smoothness |
| BSD-RANK | \(\mathrm{rank}=\mathrm{ord}\,L\) \(\forall E\) | Not a measured function. Working: LMFDB Sha and first-of-rank seeds. | Hunting Kato; Weierstrass\(\to\mathbb{Z}\) |
| HODGE-TAIL | Algebraicity with no named cycle | Not a measured function. Working: \(\chi\)/Gram of named varieties. | Hunting \(C_{48}\); stealing \(25-1\) for \(\chi(\mathrm{K3})\) |
