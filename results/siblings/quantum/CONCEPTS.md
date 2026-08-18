# Traceable concepts — Damian’s pictures → FSOT engine

These are **not** a second theory. They are how the author *sees* the same pin-D1D38A engine.  
If a picture and the engine disagree, **the engine wins** until the author changes a named route.

Authority: [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) · this fold: FSOT-Quantum.

---

## C1 — Water body (quantum side of reality)

**Said (plain):** H₂O makes up oceans and lakes. The quantum side is like that water: molecular bonds grab, let go, connect, disconnect.

**Maps to**

| Picture | Engine |
|---------|--------|
| Body of water | Continuum field before collapse |
| Bond grabs | consensus (two trits agree → stay) |
| Bond lets go | trit 0 (superposed / quiet) or opposite poles |
| Different lakes / tanks | named domains at different \(D_{\mathrm{eff}}\) |

**Code:** `fsot_quantum/medium_strings.py` · `fsot_quantum/gates.py` consensus  
**Not claimed:** that liquid water *is* a qubit.

---

## C2 — Three strings that strum

**Said (plain):** Strings have three connective pieces. They strum and cause vibrations so other systems can collapse and work together.

**Maps to**

| Picture | Engine |
|---------|--------|
| Three strings | \(T_1, T_2, T_3\) with \(S = K(T_1+T_2+T_3)\) |
| String 1 “look” | \(T_1\) — observer / \(C_{\mathrm{factor}}\) when `observed` |
| String 2 “body” | \(T_2\) — scale / amplitude (defaults 1) |
| String 3 “strum” | \(T_3\) — valve + **acoustic bleed** \(A_{\mathrm{bleed}}\) + POOF/SUCTION |
| Vibration | phase rotation + \(T_3\) (tiny: \(\beta\) is \(\sim 10^{-17}\)) |

**Code:** `three_strings()` in `medium_strings.py`  
**Live check:** \(S\) from the three strings **equals** `domain_scalar` (must match).

---

## C3 — Observation / look / snap

**Said (plain):** Observation through interconnective systems, vibrationally, helps collapse.

**Maps to**

| Picture | Engine |
|---------|--------|
| Look | `observed=True` on Quantum_Mechanics (D=6) |
| Don’t look (compute) | `observed=False` on Quantum_Computing (D=11) |
| Snap | collapse through \(\Theta = C_{\mathrm{eff}}\cdot P_{\mathrm{var}}\) |
| After look, bonds agree | consensus then resolve 0 with \(\mathrm{sign}(S)\) |

**Code:** `observe_collapse_pair()` · `strum_then_look()`  
**Ledger:** `docs/MEDIUM_NEXT.md`

---

## C4 — Bleed between tanks (not one D forever)

**Said (plain):** Not every quantum interaction is the same D. Some bleed further. We refine by how the medium connects, not by adding a bolt.

**Maps to**

\[
\kappa_{ij} = A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i|\,|S_j|\big/\bigl(1+|D_i-D_j|/25\bigr)
\]

Then \(S\) relaxes. Wave = \(\Delta S\), not a new coefficient.

**Code:** `fsot_quantum/quantum_bleed.py`  
**Mother doc:** FSOT-2.1-Lean `docs/COMPLEX_SYSTEM_DERIVATION.md`  
**Ledger:** `docs/BLEED_REFINE.md`

---

## C5 — Aside only (not doctrine)

Author noticed, once: ice, metals, rock — we often chill or freeze a medium to *use* it. Same pattern as a QPU fridge.  
**Not** a claim, not a program goal. Left here so it is not mistaken for a research track.

---

## C6 — LLM vs this fold (out of scope here)

LLMs are full of free parameters. FSOT is parameter-free. They fight.  
That problem lives in FSOT-GPU, not this QC job fold.

---

## How to add the next picture

1. Write it in plain words here (C7, C8, …).  
2. Map each phrase to **one existing** engine object (seed, \(T_i\), domain, collapse, consensus, \(\kappa\)).  
3. If nothing maps, **ask Damian** — do not invent a coefficient.  
4. Add a live check that can fail.

---

## Reproduce the living checks

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.medium_next
python -m fsot_quantum.keep_going
```
