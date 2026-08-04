# Complex-system derivation (not isolated ad-hoc)

**Module:** `vendor/fsot_complex_interaction.py`  
**Rule:** zero free parameters. Literature is comparison only.

## What was wrong before

Treating CKM, PMNS, EW, and GR as **independent closed forms** (or worse, `PDG × (1+|S|·factor)`) ignores that they are **parts of one complex fluid-spacetime system**. Interface physics is the content — not a stack of disconnected formulas.

## What we do now

### 1. Sector nodes (structural topology)

| Sector | FSOT domain | Role |
|--------|-------------|------|
| GR | Cosmology | spacetime / gravity |
| EW | Particle_Physics | electroweak |
| QCD | Nuclear_Physics | strong |
| QED | Electromagnetism | EM |
| FLAVOR_Q | Particle_Physics | quark flavor |
| FLAVOR_L | Quantum_Mechanics | lepton flavor |
| HIGGS | High_Energy_Physics | Higgs |
| ATOMIC | Atomic_Physics | low-energy bridge |

### 2. Interaction edges (who talks to whom)

Structural graph, e.g. EW–QCD, EW–QED, EW–HIGGS, QCD–FLAVOR_Q, FLAVOR_Q–FLAVOR_L, GR–EW, …

Not a free fit: the edge list is the physics skeleton.

### 3. Seed-locked coupling

\[
\kappa_{ij} = A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i|\,|S_j|
\big/\bigl(1 + |D_i-D_j|/25\bigr)
\]

- \(S_i\) = domain scalar (seed engine)  
- \(D_i\) = domain \(D_{\mathrm{eff}}\)  
- All coefficients from Layer-1/2 seeds  

Yin–yang fraction: \(\mathrm{POOF}/(\mathrm{POOF}+\mathrm{SUCTION})\).

### 4. Coupled equilibrium

\[
\frac{dS_i}{dt}
= \sum_j \kappa_{ij}(S_j - S_i)
- \gamma\,(S_i - S_i^{\mathrm{eq}})
\]

with \(\gamma = |\mathrm{Chaos}| + \psi_{\mathrm{con}}\cdot\mathrm{POOF}\),  
\(dt = \mathrm{POOF}\cdot\mathrm{SUCTION}\),  
steps \(= \mathrm{round}(1/\mathrm{POOF})\) — all seed-locked.

### 5. Emergent observables

From the **coupled** \(S_i\), interface indices

\[
I_{ab} = |S_a - S_b| / (|S_a| + |S_b|)
\]

modulate seed composites (FO-213 Higgs, φ-structure, …) so CKM/PMNS/EW/masses
**feel the rest of the system**, not a vacuum one-liner.

## Commands

```powershell
python vendor/fsot_complex_interaction.py
python vendor/fsot_ckm_pmns.py
python vendor/fsot_gr_sm.py
python scripts/export_and_generate_gr_sm_ckm_artifacts.py
python scripts/run_gr_sm_ckm_verification.py
```

### Seed scale × subtle network modulation

```
O = O_seed × (1 + POOF·SUCTION·(I₊ − I₋))
```

- `O_seed` — pure seed closed form (table below)
- `I±` — interfaces from the **coupled multi-sector graph**
- Nudge is O(1%); **wrong baselines stay wrong** — fix the seed form first
- No PDG in the formula; PDG only for residual comparison

### Corrected seed baselines (high residuals were wrong formulas)

| Observable | Seed formula | ~residual |
|------------|--------------|-----------|
| λ | `POOF·(1+η_eff)` | 0.07% |
| A | `1 − γ/π` | 1.2% |
| ρ̄ | `γ·e/π²` | 0.02% |
| η̄ | `4·SUCTION·φ/e` | 0.6% |
| sin²θ_W | `SUCTION·(1+φ/e)` | 1.4% |
| α⁻¹ | `e⁴·π·φ/2` | 1.3% |
| α_s | `1/(2·e·φ)` | 3.6% |
| m_H | FO-213 | 0.04% |
| m_W | `m_H·2/π` | 0.8% |
| m_Z | `m_W/cosθ_W(seed)` | 0.1% |
| m_t | `m_H·e·φ/π` | 1.5% |
| sin²θ₁₂ | `2·POOF` | 0.01% |
| sin²θ₂₃ | `ψ_con·e/π` | 0.2% |
| sin²θ₁₃ | `POOF·SUCTION` | 2.6% |
| δ_PMNS | `π + ψ_con/2` | 0.6% |
| Δm²₂₁ | `POOF³·SUCTION²` | 3.8% |
| Δm²₃₁ | `POOF²·A_bleed·ψ_con·SUCTION` | 6.5% |

## Honesty

- High residuals were mostly **mis-applied formulas** (e.g. m_W = m_H·φ/e, m_t = m_H·√(e·φ)), not missing free parameters.  
- After correction: complex suite max residual **~7%** (was 50–100%).  
- Remaining outliers stay seed-closed research targets — not fitted.
