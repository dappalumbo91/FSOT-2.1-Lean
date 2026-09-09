# Why something is not claimed

**Pin:** D1D38A · **Freeze:** 2026-09-09 · **Labels A/B:** true / true

This page is the **unclaimed ledger**. Every “not claimed” line has a *reason*.
Not claiming is not a hole in the residual program. Mixing objects is.

Related: uniqueness spine [`UNIQUENESS_RESEARCH_SPINE.md`](UNIQUENESS_RESEARCH_SPINE.md) ·
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
| Continuum YM path-integral mass gap / confinement uniqueness | Different theorem than the Lean attractor. No false formal credit. | Attractor identities + residual confinement probes |
| Spin-2 graviton Fock uniqueness from the fluid action | Quantization uniqueness, deferred | Spin-2 helicity / TT **probes** |
| Einstein–Hilbert measure uniqueness | Action classification theorem, deferred | Weak-field / Schwarzschild / perihelion / deflection **probes** |
| Full EH / full SM Lagrangian “derived uniquely” | T3/T4 are packages and recoveries, not uniqueness | Force package v1 in `vendor/fsot_gr_sm.py` |
| Clock-time of the next earthquake, hurricane, VEI≥4 | Valve geometry ≠ a calendar of a hypocenter | Dated **windows** on live cells; `kill_if` stays the scored cell |
| Beating ECMWF at S2S week 3 | Honest refusal — class residuals on NDBC/NCEI are not NWP | Weather **class** holds; not a track forecast |
| Next-day prices / crash date | Honest refusal — a ticker as a 0.5% central is a kill | World Bank YoY **class** residuals |
| Individual diagnosis / onset date | Honest refusal — person-level onset is clinical | Immunology/cardiology **class** residuals; 20.00 W observer lock |
| Euclid CLOE FoM as measured S8/H0/wa | Synthetic figure of merit; zero survey-level S8 | PRED-002/042/043; wait for DR1 |
| Genetics 0.13 Å as sequence-only | Sibling product vs AF vs FSC vs bulk are **four objects** | Hub **quotes** the 2026-08-17 freeze; CASP/CAMEO still OPEN |
| JWST Perfect Host 73.49 as PRED-001 | Wrong object (local ladder ≠ bridge 70.75) | Score 73.49 on PRED-024 / hosts-only |
| Live \(\lvert S_i/S_j\rvert\) vs 1 as a 0.5% central | Same-view question (law D9), not a failed gate | Dual-route APPLY residuals are the 0.5% object |
| Frozen-state potentials as calibrated quake probability | Seed-split of valve geometry, not ETAS | Discrete potentials on new issues only |
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
| **Honest refusal** | The model will not claim this even later as a 0.5% central | S2S beat, prices, diagnoses |
| **Wrong object** | A real number scored against the wrong lock | Perfect Host as PRED-001 |
| **Awaiting data** | Named survey/paper has not landed | Euclid DR1, JINR 119, CASP blind |
| **Sibling-owned** | Same pin, different product repo | Genetics 0.13 Å, Quantum fold, Materials design |
| **Open theorem** | Formal object not proved; probes exist | Path-integral uniqueness |
| **Soft aspiration** | Stricter band than Label A; left open on purpose | 0.05% on two named mixtures |

Kill: converting any row above into a fitted ε so it “looks claimed.”
