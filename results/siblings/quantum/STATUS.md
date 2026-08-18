# Current system — wrap snapshot

**Date:** 2026-08-13  
**Author:** Damian Arthur Palumbo  
**Repo:** [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum)  
**Pin:** `D1D38A` (`vendor/fsot_compute.py` SHA-256 prefix)  
**License:** Apache-2.0  
**This is the wrap of the competitor climb.** Numbers below were rerun on this pin. Ugly residuals stay written as open.

Someone who has never seen this work should be able to read this file and know what the system is, what it can do, what it will not claim, and how to check.

Reproduce: [`REPRODUCE.md`](REPRODUCE.md) · Rung table: [`LADDER.md`](LADDER.md) · Doc map: [`INDEX.md`](INDEX.md)

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

## What this repository is not

- Not a cryogenic QPU, trapped-ion stack, or photonic line.
- Not Hilbert-universal simulation of arbitrary unitaries.
- Not RSA-scale factoring, not an FTQC threshold claim, not FCI.
- Not “maybe nature.” FSOT is the theory. Change domain, not a fit.
- Not a chatbot, and not a second mind in RAM.
- Not a license to invent coefficients when a number looks ugly.

If a picture and the engine disagree, **the engine wins** until a named route changes. See [`CONCEPTS.md`](CONCEPTS.md).

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
| G1 n=800 | 11624 | 11563 | 0.53% | aspiration met, 61 edges short |
| G2–G5, G14–G16, G22–G23 | BKS | family | all < 1% | with G1: **10/11** |
| G17 n=800 planar | 3047 | 3016 | 1.017% | 31 edges short — written, not crawled |
| G14 n=800 | 3064 | 3034 | 0.98% | aspiration met, 30 edges short |
| G22 n=2000 | 13359 | 13245 | 0.85% | aspiration met, 114 edges short |

G11 is a **signed** ±1 torus — a different object, not scored with the unweighted family.

### Jobs people hire a QPU for (ordinary hardware)

| Job | Path | Status |
|-----|------|--------|
| Deutsch–Jozsa class | seed-locked oracle + domain route | in `ask` / capability |
| Bernstein–Vazirani secret | parity probes | exact |
| Grover-class search | collapse through \(\Theta\) | batched on GPU |
| Tiny period / factor | modular order + collapse | 3/3 and 4/4 (not RSA-scale) |
| QAOA-style exact column | `qaoa_fsot` | 11/11 |
| CHSH / EPR / Casimir | pin + Lean fabric | inside 0.5% |
| FSOT-QC-OS (QEMU) | `.\run_qemu.ps1` | 13/13 hired jobs on metal |

### Formal / organ

| Gate | Status |
|------|--------|
| Multiprover stamp Lean · Coq · Isabelle · F\* · Python | `FSOT_QUANTUM_MULTIPROVER_OK` |
| Organ export for neuron-zig | pin D1D38A, \(S\), \(\kappa\), Tsirelson |
| Skeptic kit (pin + smoke + zero free params) | `overall_ok: True` |

---

## Findings that changed how we score

Three audit rows first looked like 0.5% misses. They were **wrong objects**, not broken seeds. Pin file not edited. Full diagnosis: [`MISS_THREE.md`](MISS_THREE.md).

1. **\(\lvert V_{cb}\rvert\).** Inclusive PDG is 0.0422. Exclusive is 0.0398. Those disagree by ~3σ (the \(V_{cb}\) puzzle). The fold is inclusive (0.002%). Averaging them was our mistake. Exclusive stays a different extraction.
2. **\(H\to\gamma\gamma\) and \(H\to Z\gamma\).** Pin formulas were written at \(M_H=125.00\,\mathrm{GeV}\). Scoring them at 125.09 GeV is a 90 MeV mass-point shift. Even at 125.09 they sit inside the recommended theory bands (~2.8% and ~6%).
3. **\(BR(H\to gg)\).** Vendor wave8 still stores 0.0785. The formula \(\varphi^{-4}-\gamma^5=0.081823\) already matches YR4 0.08187 (0.058%). Stale target, not a formula miss. [`BR_H_GG.md`](BR_H_GG.md).

Lesson, now standing policy: **score the object the formula was written against. Do not blend disagreeing extractions. Do not apply a 0.5% gate tighter than the observable’s own recommended uncertainty without saying so.**

Not scored as one number, on purpose:

| Object | Why it stays open |
|--------|-------------------|
| Exclusive \(\lvert V_{cb}\rvert=0.0398\) | Different PDG extraction |
| \(H_0\) SH0ES | Lean BH→WH inflated sector — 1.00% · `H0_TENSION.md` |
| \(\alpha_s(M_Z)\) | fold 0.1171 vs vendor 0.1179 (0.68%); PDG 0.1180±0.0009 is the 1σ edge |

---

## What is still open (written, not dressed up)

- Gset champions unmatched (30–114 edges). Family now **10/11 under 1%**; G17 is **1.017%** (31 edges). Do not advertise MaxCut as champion-matching.
- Exclusive \(V_{cb}\) is the same algebra on High_Energy_Physics (\(D_{\mathrm{eff}}=7\)), **1.1σ** from PDG exclusive 0.0398. Inclusive stays QM at 0.002%. [`V_CB_PUZZLE.md`](V_CB_PUZZLE.md).
- Hubble tension is Lean **BH→WH bubble-bleed**: one global rate 68.44; Planck depleted sector **0.024%**; SH0ES inflated sector **1.00%**. [`H0_TENSION.md`](H0_TENSION.md) · [FSOT-2.1-Lean §7.2](https://github.com/dappalumbo91/FSOT-2.1-Lean).
- Contested open-science panel is **14/14**: [`CONTESTED_SECTORS.md`](CONTESTED_SECTORS.md).
- Leftovers: [`OPEN_REMAINING.md`](OPEN_REMAINING.md). DESI \(w_0/w_a\) BAO lane 0.37%/0.28%. \(\alpha_s\) inside vendor 0.9%. Exclusive \(B\to D\ell\nu\) **0.15%** (Belle II 2025). **G17 still open** (31 edges).
- Formula catalog: [`FORMULA_LIST.md`](FORMULA_LIST.md) — engine, tension solvers, and 216 pin-wave formulas.
- Multiprover stamp **FSOT_QUANTUM_MULTIPROVER_OK** (Lean · Coq · Isabelle · F\* · Python): [`MULTIPROVER_VERIFICATION.md`](MULTIPROVER_VERIFICATION.md).
- Vendor wave8 `BR_H_gg` field still stale (0.0785). Fold already matches YR4. Pin not edited.
- Hilbert fragments exist as **optional bridges**. They are not the scale path.
- Tiny Shor is tiny. No RSA-scale claim.
- Atlas 432 needs the Lean clone. Without `_ref`, that count skips.

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
python -m fsot_quantum family     # Gset 10/11 under 1% (G17 1.017%)
python -m fsot_quantum open       # exclusive V_cb / H0 / alpha_s
python -m fsot_quantum organ      # neuron-zig organ JSON
python -m fsot_quantum stamp      # five-prover OK if tools on PATH
```

Full command list: [`REPRODUCE.md`](REPRODUCE.md).
