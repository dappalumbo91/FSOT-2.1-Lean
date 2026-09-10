# Why something is not claimed

**Pin:** D1D38A · **Freeze:** 2026-09-09 · **Labels A/B:** true / true

This page is the **unclaimed ledger**. Every “not claimed” line has a *reason*.
Not claiming is not a hole in the residual program. Mixing objects is.

Related: uniqueness spine [`UNIQUENESS_RESEARCH_SPINE.md`](UNIQUENESS_RESEARCH_SPINE.md) ·
emergent time [`TIME_EMERGENT.md`](TIME_EMERGENT.md) ·
open questions [`../predictions/reports/SCIENTIST_OPEN_QUESTIONS.md`](../predictions/reports/SCIENTIST_OPEN_QUESTIONS.md) ·
object compare [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md) ·
laws [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md).

---

## What “uniqueness” is (two different objects)

People hear “uniqueness” and think one Millennium-style theorem. FSOT splits it.

| Object | What it would take | Status here |
|--------|--------------------|-------------|
| **Classical continuum uniqueness** | Prove, from the **Yang–Mills path integral**, a mass gap and that free color cannot exist as an asymptotic particle. Same family: spin-2 **Fock** uniqueness from a fluid action; Einstein–Hilbert **measure** uniqueness. | **`OPEN_NOT_CLAIMED`** |
| **FSOT attractor uniqueness** | Under seed-locked channel dynamics, free-color amplitude \(a_0 e^{-\gamma t}\) **strictly damps** for \(\gamma>0\); color-singlet channels **persist** at \(S_{\mathrm{eq}}\). Counterfactual \(\gamma=0\): free color **persists** (dampening is load-bearing). | **Claimed as Lean identities**, not as the path-integral theorem |

Lean: `FSOT/Formal/UniquenessAttractor.lean` —
`color_amp_strictly_damped`, `color_amp_no_damp`, `singlet_gap_strictly_shrinks`,
`gamma_color_pos`, `free_color_not_attractor`.

Python probes (`vendor/fsot_uniqueness_confinement.py`): \(\gamma_{\mathrm{color}}>0\),
\(\Lambda_{\mathrm{QCD}}\) proxy, string tension \(\sigma\), Wilson/Polyakov flags.
Those probes are **executable residuals**. They are **not** a constructive-QFT existence proof.

### Why classical uniqueness is not claimed

1. **Different formal object.** A path-integral measure + spectrum theorem is not the same statement as “free color is not an attractor under this ODE.” Claiming the first because we have the second is false credit.
2. **Label B T4 is a force/scope package**, not that theorem. T3 is residual-gated limit recovery, not Einstein–Hilbert uniqueness.
3. **Residual physics of confinement is already gated** (Λ_QCD, \(\sqrt{\sigma}\), Casimirs, β₀). The open item is the *classical problem formulation*, not a missing 0.5% panel.
4. **Forbidden reading:** “Because YM uniqueness is open, FSOT is incomplete.” Dependent physics is closed. The open classical formulation is the suspect object, not the residual ToE.

Euclid DR1 (~12 Nov 2026) is a **watch**, not a uniqueness drop.

Deferred on the same uniqueness track (not started as required residual debt):
spin-2 Fock uniqueness, Einstein–Hilbert measure uniqueness.

---

## Ledger: not claimed, and why

| Item | Why it is not claimed | What *is* claimed instead |
|------|------------------------|---------------------------|
| A Clay Millennium Prize | CMI requires Qualifying Outlet + two years + community acceptance. GitHub is not a Qualifying Outlet. | Native identities + an **accuracy vs public SOTA** scoreboard ([`MILLENNIUM_ACCURACY_VS_SOTA.md`](MILLENNIUM_ACCURACY_VS_SOTA.md)). Prize flags stay zero. |
| A SOTA beat as 0.5% green | Riemann n=2..10 (4.26%) and glueball vs 4√σ (4.57%) **beat the competitor** and are **outside** the rest-of-system 0.5% gate. | Marked `beats_sota_fsot_accuracy_wip`. Do not stuff. |
| Glueball \(m(0^{++})/\sqrt{\sigma}\) beating Teper *lattice precision* | Live vs 3.65±0.11 is 1.5σ — **does not beat lattice**. Do not retune the 3.5 ballpark. | Beats Teper's own ~4√σ closed form (accuracy WIP) and √2 vs 3/2 on m(2++)/m(0++) (in 0.5%, aspiration WIP). |
| Weather 24 h beating majority class or ECMWF | Hold 22/28 = 78.6% vs majority 85.7%. ECMWF RMSE is a different object. | Finer `dt` on the same φ^4 / Omori path. |
| Continuum YM path-integral mass gap as *proved* | Different theorem than the native path-sum. No false formal credit. | Discrete path-sum \(w_{\mathrm{POOF}}+w_{\mathrm{hold}}=1\); \(\int a_0 e^{-\gamma t}=a_0/\gamma\) ([`PATH_SUM.md`](PATH_SUM.md)). Classical YM stays OPEN_NOT_CLAIMED |
| Spin-2 graviton Fock uniqueness from the fluid action | Quantization uniqueness, deferred | Spin-2 helicity / TT **probes** |
| Einstein–Hilbert measure uniqueness | Action classification theorem, deferred | Weak-field / Schwarzschild / perihelion / deflection **probes** |
| Full EH / full SM Lagrangian “derived uniquely” | T3/T4 are packages and recoveries, not uniqueness | Force package v1 in `vendor/fsot_gr_sm.py` |
| Newtonian UTC hypocenter as a 0.5% central | Wrong object: treats time as a fundamental axis, valve-blind | **Process time** (D12 / C15): \(\mathrm{process\_time}(\varphi^4,d)=\varphi^4\cdot d/25\); issued 7 d window is \(d=25\) rounded to SI. See [`TIME_EMERGENT.md`](TIME_EMERGENT.md) |
| Beating ECMWF at S2S week 3 *today* | Goal, not a present claim | 48 h process windows + class residuals; finer `dt` on φ^4 / Omori is the path ([`NEXT_GOAL_TRACKS.md`](NEXT_GOAL_TRACKS.md)) |
| Next-day ticker / crash date as 0.5% | Wrong object (one print) | Economics **class** + \(d=20\) process window started (`scripts/build_market_process_layer.py`) |
| Person-level onset as 0.5% | Needs Genetics product on public host+pathogen structure | Class epidemiology 0.015%; two-system smoke ([`SICKNESS_TWO_SYSTEM.md`](SICKNESS_TWO_SYSTEM.md)) |
| Euclid CLOE FoM as measured S8/H0/wa | Synthetic figure of merit; zero survey-level S8 | PRED-002/042/043; wait for DR1 |
| Genetics 0.13 Å as sequence-only | Sibling product vs AF vs FSC vs bulk are **four objects** | Hub **quotes** the 2026-08-17 freeze; CASP/CAMEO still OPEN |
| JWST Perfect Host 73.49 as PRED-001 | Wrong object (local ladder ≠ bridge 70.75) | Score 73.49 on PRED-024 / hosts-only |
| Live \(\lvert S_i/S_j\rvert\) vs 1 as a 0.5% central | Same-view question (law D9), not a failed gate | Dual-route APPLY residuals are the 0.5% object |
| Frozen-state potentials as calibrated ETAS probability | Not a fitted quake probability | Discrete **process-time** branches (cell POOF / transfer / quiet hold) on new issues |
| SH0ES class-bin 1% stuffed into 0.5% | Isolated on purpose; chain is the fair object (0.25%) | Work the chain; do not retune ρ |
| Cat-2 FRB dump as the 37/37 orifice classifier | Fluence without pulse width is a **catalog class** | Frozen 37/37 complete set; Cat-2 3390 is structural |
| JINR Z=119 as observed | No confirmed atom; IUPAC ceiling still 118 | PRED-017 viability **awaiting** |
| Dated issue `2026-09-09` scored early | Score after `valid_to`. Do not rewrite issued JSON | Hold 65 / kill 45 / awaiting 4 on this freeze |
| 0.05% tier-scalar as closed | Soft aspiration, open on two **named** objects | Official gate remains 0.5%; SH0ES chain ~0.212%, Cepheid PL ~0.135% not stuffed |
| Fuel / lattice **forward design** as a 477 headline | Product, not a residual file | Sibling [FSOT-Materials](https://github.com/dappalumbo91/FSOT-Materials); hub keeps PRED-034 green |
| Full FSOT-native OS shipped | Roadmap, not a delivered OS | Zig mind + neural monorepo as embodiments |
| Peer review / arXiv endorsement | Social process, not T1–T6 | This GitHub repo is the **authority preprint** |

---

## How to read a “no”

| Kind | Meaning | Example |
|------|---------|---------|
| **Goal, not yet** | Same law; more public data / finer `dt` / sibling product | ECMWF week-3 skill; market windows; sickness two-system |
| **Honest refusal of a wrong object** | Will not become a 0.5% central *as that object* | UTC hypocenter; one ticker print; person onset without structure |
| **Wrong time object** | UTC hypocenter as fundamental; process time is D12 | “M7 at 14:32:07 UTC” vs \(\varphi^4\) window at fold \(d\) |
| **Wrong object** | A real number scored against the wrong lock | Perfect Host as PRED-001 |
| **Awaiting data** | Named survey/paper has not landed | Euclid DR1, JINR 119, CASP blind |
| **Sibling-owned** | Same pin, different product repo | Genetics 0.13 Å, Quantum fold, Materials design |
| **Open theorem** | Formal object not proved; probes exist | Path-integral uniqueness |
| **Soft aspiration** | Stricter band than Label A; left open on purpose | 0.05% on two named mixtures |

Kill: converting any row above into a fitted ε so it “looks claimed.”
