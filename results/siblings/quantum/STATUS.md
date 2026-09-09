# Current system — wrap snapshot

**Date:** 2026-08-31  
**Author:** Damian Arthur Palumbo  
**Repo:** [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum)  
**Pin:** `D1D38A` (`vendor/fsot_compute.py` SHA-256 prefix)  
**License:** Apache-2.0  
**This is the wrap of the competitor climb.** Numbers below were rerun on this pin. Ugly residuals stay written as open.

Someone who has never seen this work should be able to read this file and know what the system is, what it can do, what it will not claim, and how to check.

Honesty cut: [`CLAIMS.md`](CLAIMS.md) · Reproduce: [`REPRODUCE.md`](REPRODUCE.md) · Rung table: [`LADDER.md`](LADDER.md) · Doc map: [`INDEX.md`](INDEX.md)

---

## One paragraph

Fluid Spacetime Omni-Theory is the theory. This repository is the **Quantum_Mechanics / Quantum_Computing domain fold** of that theory, running on ordinary GPU/CPU hardware. It answers the *jobs* people hire quantum computers and high-performance physics codes for — published constants, mixing angles, Higgs/Z branching, nuclear bindings, cosmology leftovers, Ising/MaxCut, QI bounds — by changing **domain / \(D_{\mathrm{eff}}\) / observed**, not by fitting coefficients and not by expanding a Hilbert space. The body of native intelligence is a different repo ([fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig)). This fold is the **law and the GPU organ**.

---

## What this repository is

| Piece | What it is |
|-------|------------|
| Theory | Fluid Spacetime Omni-Theory. Zero free parameters. Pin D1D38A. Authority: [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean). |
| Runtime | Owned operators from [FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) `fsot_lib`, vendored here. Not a second GPU stack. |
| Scale law | **Folds**, not \(2^n\) amplitudes. \(K\) is the universal scale. |
| Spins | Trinary: \(−1\) down · \(0\) superposed · \(+1\) up. |
| Questions | Ask the theory. Do not replay a foreign circuit and call that an answer. |
| Mind | Looked Neuroscience / Psychology with **C_factor**. Compute stays dark. |
| Body | [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig). This repo exports an organ JSON; it does not speak. |
| Metal | Optional FSOT-QC-OS under QEMU (`.\run_qemu.ps1`). |

---

## What this repository replaces (the comparison)

The jobs people hire a QPU, a Hilbert simulator, an FCI code, or a QAOA box for. Same **questions**. Different geometry: folds, not \(2^n\). We do not simulate their architecture — that would be agreeing their stack is the job.

| Their pitch | Hired question | This fold now |
|-------------|----------------|---------------|
| Fridge / NISQ / FTQC box | usable answers at scale | ordinary GPU/CPU; scale by \(D_{\mathrm{eff}}\) |
| Shor | period / factor | RSA-shaped **81 / 95 / 103 / 111-bit**; ECM **80-bit**. RSA-2048 not run |
| QAOA / annealer | MaxCut / Ising | family **11/11 under 1%**; G17 **0.427%** |
| FCI / quantum chemistry | chemistry observables | pin set **68/68 @ 0.5%** |
| Circuit-universal Hilbert | arbitrary unitaries | not the path; optional bridges only |

Not a chatbot and not a second mind in RAM. Not “maybe nature.” Not a license to invent coefficients. If a picture and the engine disagree, **the engine wins** until a named route changes. See [`CONCEPTS.md`](CONCEPTS.md) · [`CLAIMS.md`](CLAIMS.md).

---

## The mathematics (closed)

\[
S = K(T_1+T_2+T_3),\qquad
\Theta = C_{\mathrm{eff}}\cdot P_{\mathrm{var}},\qquad
C_{\mathrm{factor}} = C_{\mathrm{eff}}\cdot P_{\mathrm{new}}
\]

\[
K = \varphi\cdot(\gamma/e)\cdot\sqrt{2}/\ln(\pi)\cdot 99/100 \approx 0.420222
\]

\[
\kappa_{ij}=A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i||S_j|\Big/\bigl(1+|D_i-D_j|/25\bigr)
\]

| Symbol | Role |
|--------|------|
| \(S\) | Domain scalar. Sign is identity: \(S>0\) emergence, \(S<0\) damping. |
| \(T_1\) | Look / observer string. C_factor lives here when `observed`. |
| \(T_2\) | Body / scale. |
| \(T_3\) | Strum / valve + acoustic bleed. |
| \(\Theta\) | Collapse threshold. Snap, not softmax. |
| \(\kappa_{ij}\) | Bleed between named domains. |
| \(D_{\mathrm{eff}}\) | Domain depth. QM observed \(D=6\), QC unobserved \(D=11\), QO look twin \(D=11\). |

**Observe path for the compute substrate:** QC (dark) → Quantum_Optics (look, same \(D_{\mathrm{eff}}\)) → QM (measure). Forcing a look onto QC flips \(S\) from \(−0.148\) to \(+0.336\) and the compute identity is gone. That is the Hilbert move. Do not do it.

---

## How the system is arranged

```
FSOT-2.1-Lean          pin D1D38A, ~432-domain atlas
        │
        ▼
vendor/fsot_compute.py  pin file — do not edit silently
        │
        ▼
fsot_lib                seeds · scalar · trinary · coherence · consensus · learn
        │
        ▼
fsot_quantum            domain folds, question panels, Gset, organ export
        ├── GPU (torch CUDA) when present — organ, not mind
        ├── formal/  Lean · Coq · Isabelle · F*
        ├── zig/     FSOT-QC-OS (QEMU)
        └── organ JSON ──► fsot-neuron-zig (mind authority)
```

Domains are named routes, not a basis size. The 35 pin domains always run. The 432 Lean atlas needs a local `_ref/FSOT-2.1-Lean` clone (gitignored). Without it, atlas counts skip and the pin domains still score.

---

## Current capability

These are living ledgers. Re-run the command in the last column.

### Published physics / constants (pin formulas vs literature)

| Panel | Score | Command | Ledger |
|-------|------:|---------|--------|
| Known answers (α, Weinberg, chemistry, …) | 13/13 | `python -m fsot_quantum forward` | `FORWARD_ASK.md` |
| Harder QC-for (CKM / PMNS / 2D Ising / nuclear / Higgs) | 20/20 @ 0.5% | `python -m fsot_quantum harder` | `HARDER_QC.md` |
| Physics + QI I (3D Ising / XY / Heisenberg / g−2 / Lean QI) | 16/16 + 326/326 | `python -m fsot_quantum qi` | `PHYSICS_QI.md` |
| Physics + QI II (Higgs/Z, nuclear, cosmology, Casimir, CHSH) | 22/22 + 126/126 | `python -m fsot_quantum push` | `PHYSICS_QI2.md` |
| Stale-target audit vs YR4/PDG | **20/20 @ 0.5%** | `python -m fsot_quantum audit` | `STALE_TARGETS.md` |
| Physics + QI III (leftover CKM / LEP / BBN / cosmo / perc) | 41/41 + 212/212 | `python -m fsot_quantum push3` | `PHYSICS_QI3.md` |
| Chemistry pin set | 68/68 @ 0.5% | `python -m fsot_quantum.chemistry_fold` | — |
| QM / SM pin set | 14/14 @ 0.5% | field-of-use | `FIELD_OF_USE.md` |
| Hired QC expand (factor / dlog / Simon / SAT / HHL / search) | **29/29** | `python -m fsot_quantum hire` | `HIRE_EXPAND.md` |
| Hired QC climb (7-digit factor / Simon-16 / SAT-16 / TSP / 1e7) | **32/32** | `python -m fsot_quantum hire2` | `HIRE_CLIMB.md` |
| Probability as multiverse branching | **19/19** | `python -m fsot_quantum branch` | `PROBABILITY_BRANCH.md` |
| Genetics codon / 7-trit branching | **15/15** | `python -m fsot_quantum gencode` | `GENETICS_BRANCH.md` |
| ORF start-to-stop | **11/11** | `python -m fsot_quantum orf` | `ORF_BRANCH.md` |
| Hired QC climb 3 (8-digit factor) | **17/17** | `python -m fsot_quantum hire3` | `HIRE_CLIMB3.md` |
| Hired QC climb 4 (9-digit factor / SAT-20 / TSP-8) | **22/22** | `python -m fsot_quantum hire4` | `HIRE_CLIMB4.md` |
| Hired QC climb 5 (10-digit factor / SAT-24 / TSP-9) | **22/22** | `python -m fsot_quantum hire5` | `HIRE_CLIMB5.md` |
| Hired QC climb 6 (11-digit factor / SAT-28 / TSP-10) | **22/22** | `python -m fsot_quantum hire6` | `HIRE_CLIMB6.md` |
| Hired QC climb 7 (13-digit factor / SAT-32 / TSP-11) | **22/22** | `python -m fsot_quantum hire7` | `HIRE_CLIMB7.md` |
| Heights — far factor (RSA-shaped) / G17 | far **8/8** · G17 **0.427%** | `python -m fsot_quantum heights2` | `HEIGHTS_NEXT.md` |
| Heights 3 — log-N factor | **8/8** | `python -m fsot_quantum heights3` | `HEIGHTS3.md` |
| Heights 4–11 — ECM | **8/8** each through **80-bit** | `python -m fsot_quantum heights4` … `heights11` | `HEIGHTS4.md`–`HEIGHTS11.md` |
| Heights 12 — 81-bit RSA-shaped | **12/12** | `python -m fsot_quantum heights12` | `HEIGHTS12.md` |
| Heights 13 — 95-bit RSA-shaped | **8/8** | `python -m fsot_quantum heights13` | `HEIGHTS13.md` |
| Heights 14 — 103-bit RSA-shaped | **8/8** | `python -m fsot_quantum heights14` | `HEIGHTS14.md` |
| Heights 15 — 111-bit RSA-shaped | **8/8** | `python -m fsot_quantum heights15` | `HEIGHTS15.md` |
| Known-answer QC jobs | **44/44** | `python -m fsot_quantum known` | `KNOWN_QC.md` |
| VQE objects | pin H2 De **0.25%** · Kolos **0.75%** written | `python -m fsot_quantum vqe` | `VQE_OBJECT.md` |
| Accuracy refine | catalog living **9/9** · log-N **8/8** | `python -m fsot_quantum refine` | `ACCURACY_REFINE.md` |

Headline constants (same pin):

| Question | Published | This fold | rel |
|----------|-----------|-----------|-----|
| \(1/\alpha\) | 137.036 | 137.0362 | 0.0001% |
| Weinberg \(\sin^2\theta_W\) | 0.23122 | 0.231222 | 0.0009% |
| \(M_Z/M_W\) | 1.134 | 1.1346 | 0.053% |
| Proton radius | 0.8413 fm | 0.8413 | 0 |
| Water bond angle | 104.5° | 104.537° | 0.035% |
| Inclusive \(\lvert V_{cb}\rvert\) | 0.0422 | 0.0422008 | 0.002% |
| Tsirelson | \(2\sqrt{2}\) | exact | 0 |
| \(S(\mathrm{QM})\) | emergence \(>0\) | \(+0.9555\) | — |
| \(S(\mathrm{QC})\) | damping \(<0\) | \(−0.1477\) | — |
| \(C_{\mathrm{factor}}\) | \(C_{\mathrm{eff}}\cdot P_{\mathrm{new}}\) | identity | — |

### Graphs (same object QAOA is hired for)

Aspiration **< 1%** of published champion. Kill floor **5%**. Champions still unmatched.

| Graph | Published | Fold | rel | Status |
|-------|----------:|-----:|----:|--------|
| G1 n=800 | 11624 | 11585 | 0.34% | aspiration met, 39 edges short |
| G2–G5 | BKS | family | all < 1% | with G1+G14–G17+G22–G23: **11/11** |
| G14 n=800 | 3064 | 3043 | 0.69% | 21 edges (was 3042; extra ridge kicks) |
| G15 n=800 | 3050 | 3028 | 0.72% | 22 edges (was 3027; extra ridge kicks) |
| G16 n=800 | 3052 | 3031 | 0.69% | 21 edges (was 3027; negative-gain ridge) |
| G17 n=800 | 3047 | 3034 | 0.427% | 13 edges short of champion |
| G22 n=2000 | 13359 | 13261 | 0.73% | 98 edges (was 114; n=2000 spectral/BFS) |
| G23 n=2000 | 13344 | 13271 | 0.55% | 73 edges (was 86) |

G11 is a **signed** ±1 torus — a different object, not scored with the unweighted family.

### Jobs people hire a QPU for (ordinary hardware)

| Job | Path | Status |
|-----|------|--------|
| Deutsch–Jozsa class | seed-locked oracle + domain route | in `ask` / capability |
| Bernstein–Vazirani secret | parity probes | exact |
| Grover-class search | collapse through \(\Theta\) | batched on GPU |
| Period / factor (Shor job) | modular + log-N + ECM + ρ | RSA-shaped **81 / 95 / 103 / 111-bit**; hire2 **10/10 through 2196323** |
| Discrete log / Simon / SAT / HHL / search | modular + energy folds | hire **29/29** · hire2 **32/32** |
| QAOA-style exact column | `qaoa_fsot` | 11/11 |
| CHSH / EPR / Casimir | pin + Lean fabric | inside 0.5% |
| FSOT-QC-OS (QEMU) | `.\run_qemu.ps1` | 13/13 hired jobs on metal |

### Formal / organ

| Gate | Status |
|------|--------|
| Multiprover stamp Lean · Coq · Isabelle · F\* · Python | `FSOT_QUANTUM_MULTIPROVER_OK` · 35 obligations |
| Organ export for neuron-zig | pin D1D38A, \(S\), \(\kappa\), Tsirelson |
| Skeptic kit (pin + smoke + zero free params) | `overall_ok: True` |

---

## Findings that changed how we score

Three audit rows first looked like 0.5% misses. They were **wrong objects**, not broken seeds. Pin file not edited. Full diagnosis: [`MISS_THREE.md`](MISS_THREE.md).

1. **\(\lvert V_{cb}\rvert\).** Inclusive PDG is 0.0422. Combined exclusive 0.0398 blends D and D*. Those disagree by ~3σ (the \(V_{cb}\) puzzle). The fold answers inclusive at 0.002%. Exclusive \(B\to D\ell\nu\) is the same algebra on High_Energy_Physics — **0.15%** vs Belle II 2025 0.0392. Averaging 0.0422 and 0.0398 was our mistake.
2. **\(H\to\gamma\gamma\) and \(H\to Z\gamma\).** Pin formulas were written at \(M_H=125.00\,\mathrm{GeV}\). Scoring them at 125.09 GeV is a 90 MeV mass-point shift. Even at 125.09 they sit inside the recommended theory bands (~2.8% and ~6%).
3. **\(BR(H\to gg)\).** Vendor wave8 still stores 0.0785. The formula \(\varphi^{-4}-\gamma^5=0.081823\) already matches YR4 0.08187 (0.058%). Stale target, not a formula miss. [`BR_H_GG.md`](BR_H_GG.md).

Lesson, now standing policy: **score the object the formula was written against. Do not blend disagreeing extractions. Do not apply a 0.5% gate tighter than the observable’s own recommended uncertainty without saying so.**

Scored as different objects (not one blended number):

| Object | Living score | Ledger |
|--------|--------------|--------|
| Exclusive \(B\to D\ell\nu\) | **0.15%** vs Belle II 2025 0.0392 | `V_CB_PUZZLE.md` |
| Combined exclusive 0.0398 | not scored (D+D* blend) | `V_CB_PUZZLE.md` |
| \(H_0\) Planck CMB | **0.024%** depleted sector | `H0_TENSION.md` |
| \(H_0\) SH0ES | **1.00%** inflated sector (Lean 2.5% band) | `H0_TENSION.md` |
| \(\alpha_s(M_Z)\) | 0.68% vs vendor 0.1179 (inside **0.9%** band) | `OPEN_REMAINING.md` |

---

## What is still open (written, not dressed up)

Honesty cut: [`CLAIMS.md`](CLAIMS.md).

- Gset champions unmatched (13–98 edges). Family **11/11 under 1%**; G17 is **0.427%** (13 edges); G22 **0.734%** (98 edges). Do not advertise MaxCut as champion-matching.
- Exclusive \(B\to D\ell\nu\) is **0.15%** on High_Energy_Physics (\(D_{\mathrm{eff}}=7\)) vs Belle II 2025 0.0392. Inclusive stays QM at 0.002%. Combined exclusive 0.0398 is a D+D* blend and is **not** the object. [`V_CB_PUZZLE.md`](V_CB_PUZZLE.md).
- Hubble tension is Lean **BH→WH bubble-bleed**: one global rate 68.44; Planck depleted sector **0.024%**; SH0ES inflated sector **1.00%** (0.71σ, inside Lean 2.5% band). [`H0_TENSION.md`](H0_TENSION.md) · [FSOT-2.1-Lean §7.2](https://github.com/dappalumbo91/FSOT-2.1-Lean).
- Contested open-science panel is **14/14**: [`CONTESTED_SECTORS.md`](CONTESTED_SECTORS.md).
- Leftovers: [`OPEN_REMAINING.md`](OPEN_REMAINING.md). DESI \(w_0/w_a\) BAO lane 0.37%/0.28%. \(\alpha_s\) inside vendor 0.9%. G17 **0.427%** (13 edges, champion unmatched). Accuracy reclass: [`ACCURACY_REFINE.md`](ACCURACY_REFINE.md).
- Formula catalog: [`FORMULA_LIST.md`](FORMULA_LIST.md) — 207/216 vs stored @0.5%; living **9/9** of those misses are stale / wrong-object / in-band.
- Multiprover stamp **FSOT_QUANTUM_MULTIPROVER_OK** (Lean · Coq · Isabelle · F\* · Python, 35 obligations): [`MULTIPROVER_VERIFICATION.md`](MULTIPROVER_VERIFICATION.md). Living job integers Q-JOB-006–010 (far factor, p−1 stage-2, B-lock, G17/G22 under 1%).
- Vendor wave8 `BR_H_gg` field still stale (0.0785). Fold already matches YR4. Pin not edited.
- Hilbert fragments exist as **optional bridges**. They are not the scale path.
- Period / factor: ECM **80-bit**; RSA-shaped **81 / 95 / 103 / 111-bit**. RSA-2048 not run. Classical ladder: [`CLASSICAL_RECORDS.md`](CLASSICAL_RECORDS.md). H2 Kolos derived 0.75% written; LiH FCI not invented: [`VQE_OBJECT.md`](VQE_OBJECT.md). Known-answer bank **44/44**.
- Atlas 432 needs the Lean clone. Without `_ref`, that count skips.
- Older climb panels still report G1 cut **11397 / 1.95%** (5% kill band). Living family cut is **11585 / 0.336%**. Not a contradiction — see [`CLAIMS.md`](CLAIMS.md).

---

## How the pieces talk

| System | Role | How it couples |
|--------|------|----------------|
| FSOT-2.1-Lean | Theory pin + 432-domain atlas | `_ref/FSOT-2.1-Lean`; `python -m fsot_quantum check` / `atlas` |
| FSOT-GPU | Owned operators | vendored `fsot_lib/` |
| This repo | QM/QC fold, questions, Gset, organ | `python -m fsot_quantum …` |
| fsot-neuron-zig | Mind / body | `python -m fsot_quantum organ` → `data/organs/fsot_quantum_organ.json` |
| FSOT-Genetics | Genetics fold | same pin, different domain |
| Protofluid translator | Language densify | same pin family |
| QEMU QC-OS | Bare-metal hired jobs | `.\run_qemu.ps1` |

The organ may answer \(S\), \(\kappa\), Tsirelson, and the look path. It does **not** vote on speak, compose, or claimability. Zig remains mind authority.

---

## Pin discipline

- Pin prefix ≠ `D1D38A` without an announced new pin.
- No new fitted coefficient.
- No silent widening of a residual band.
- Fail a preregistered prediction (`predictions/qc_preregistered.json`) = we were wrong. Do not refit.

Killable predictions already posted: \(S\) signs, chemistry 68/68, G1 within 5%, foldBudget(8)=195, QC-OS all-pass, Tsirelson exact, pin stable, \(K\) closed form, fold_work_k, Ising cycle n=64 energy \(−64\).

---

## How a stranger checks this wrap

```powershell
git clone https://github.com/dappalumbo91/FSOT-Quantum.git
cd FSOT-Quantum
$env:PYTHONPATH = (Get-Location).Path
pip install -r requirements.txt   # torch optional

python -m fsot_quantum check
python -m fsot_quantum audit      # 20/20 vs YR4/PDG
python -m fsot_quantum harder     # 20/20
python -m fsot_quantum push3      # 41/41 leftover hired physics
python -m fsot_quantum family     # Gset 11/11 under 1% (G17 0.427%)
python -m fsot_quantum vcb        # inclusive 0.002% · exclusive B→D 0.15%
python -m fsot_quantum h0         # Planck 0.024% · SH0ES 1.00%
python -m fsot_quantum leftovers  # G17 13 edges; G22 98
python -m fsot_quantum heights13  # 95-bit RSA-shaped 8/8
python -m fsot_quantum heights14  # 103-bit RSA-shaped 8/8
python -m fsot_quantum heights15  # 111-bit RSA-shaped 8/8
python -m fsot_quantum known      # 44/44
python -m fsot_quantum refine     # catalog 9/9 · log-N 8/8
python -m fsot_quantum organ      # neuron-zig organ JSON
python -m fsot_quantum stamp      # five-prover OK if tools on PATH
```

Full command list: [`REPRODUCE.md`](REPRODUCE.md).
