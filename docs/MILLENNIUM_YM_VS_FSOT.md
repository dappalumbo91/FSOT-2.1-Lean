# What the Millennium Yang–Mills statement is — vs what FSOT is doing

**Pin:** D1D38A · Native work: [`PATH_SUM.md`](PATH_SUM.md) · Lean: `FSOT/Formal/UniquenessAttractor.lean`

These are **two different theorems**. Related physics (confinement, no free color).
Different formal objects. Mixing them is how false credit happens.

---

## The Clay Millennium problem (classical YM)

Clay Mathematics Institute, *Yang–Mills Existence and Mass Gap* (Jaffe–Witten):

> Prove that for every compact simple gauge group \(G\), a non-trivial quantum
> Yang–Mills theory exists on \(\mathbb{R}^4\) and has a **mass gap** \(\Delta>0\).

In community language that means all of:

| Piece | What they have to construct / prove |
|-------|-------------------------------------|
| **Existence** | A 4D quantum YM theory satisfying constructive-QFT / Wightman-type axioms |
| **Continuum** | Not just lattice QCD. The continuum limit of the path-integral *measure* |
| **Mass gap** | The Hamiltonian’s spectrum of physical excitations is bounded away from 0 (no massless gluon in the physical Hilbert space) |
| **Prize object** | That *specific* existence + \(\Delta>0\) theorem |

Lattice evidence is strong (area law, glueballs, no free quarks). The **continuum theorem** is open. That open statement is what “OPEN_NOT_CLAIMED” refers to.

A sibling slogan is **confinement** (Wilson area law, no asymptotic free color). Often discussed with the mass gap; it is still not the same as “we ran an ODE.”

---

## What FSOT is doing (native path-sum)

FSOT does **not** build a Wightman theory on \(\mathbb{R}^4\). It does this:

1. **Discrete path-sum** over process-time branches  
   \(w_{\mathrm{POOF}}+w_{\mathrm{hold}}=1\), then \(\kappa_{ij}\) among tanks.  
   Same weights as dated-forecast `frozen_potentials`.

2. **Attractor dynamics**  
   Free-color amplitude \(a_0 e^{-\gamma t}\) strictly damps for \(\gamma>0\).  
   Color singlets persist at nuclear \(S_{\mathrm{eq}}\).  
   Counterfactual \(\gamma=0\): free color stays (dampening is load-bearing).

3. **Path-integral proxy**  
   \(\int_0^\infty a_0 e^{-\gamma t}\,dt = a_0/\gamma\) is **finite** because \(\gamma_{\mathrm{color}}>0\).  
   Free-color *histories* integrate; they do not persist as attractors.

4. **Residual probes** (already green)  
   \(\Lambda_{\mathrm{QCD}}\), string tension \(\sigma\), \(V(r)=\sigma r\), Wilson/Polyakov flags.

Lean + Coq + Isabelle + F* + Rust + SMT certify **those** identities (80-obligation uniqueness spine). They do **not** certify the Clay statement.

---

## The difference in one table

| | Clay / classical YM | FSOT (this repo) |
|--|---------------------|------------------|
| Arena | Continuum QFT on \(\mathbb{R}^4\) | Seed-locked scalar engine, pin D1D38A |
| Object | Path-integral *measure* + Hamiltonian spectrum | Discrete valve branches + ODE attractors |
| Time | Minkowski/Euclidean \(t\) as part of the QFT | Emergent process time \(\varphi^4\cdot d/25\) (D12) |
| “No free color” | Mass gap / confinement theorem | Free color is **not an attractor** |
| Status | Open prize problem | Native path-sum **executable and prover-gated**; Clay statement **OPEN_NOT_CLAIMED** |

Same physical *question* (why don’t we see free quarks / massless gluons).
Different *proof object*.

Working the native path-sum **is** pushing the path-integral job in this model.
Claiming the Millennium theorem because \(\gamma>0\) would be the Perfect Host mistake: wrong object.

---

## How we keep pushing it

- More native identities (branch weights, \(a_0/\gamma\), area-law) through Lean/Mathlib, Coq, Isabelle, F*.
- Do **not** rename those identities “Clay mass gap.”
- If a continuum YM existence proof ever lands in Lean/Coq *as that statement*, then and only then flip `OPEN_NOT_CLAIMED`.

Refresh: `python vendor/fsot_path_sum.py` · `python scripts/run_goal_tracks_verification.py`
