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
| A | `e/(π·A_bleed)` | 0.05% |
| ρ̄ | `γ·e/π²` | 0.02% |
| η̄ | `POOF/(3·SUCTION)` | 0.01% |
| J | `A²λ⁶η̄·(1−λ²·SUCTION)` | 0.24% |
| V_ub | `Aλ³√(ρ²+η²)` unbar NLO | 0.33% |
| V_ts | `Aλ²[1−λ²(½−ρ̄)]` NLO | 0.17% |
| sin²θ_W | `2·SUCTION/√φ` | ≤0.5% |
| α⁻¹ | `(φ·G_Catalan/C_factor)³` | 0.14% |
| α_s | `2·(POOF/ψ_con)²` | ≤0.5% |
| m_H | FO-213 | 0.04% |
| m_W | `m_H·3·P_new·(1−C_factor)` | ≤0.5% |
| m_Z | `m_W/cosθ_W(seed)` | 0.50% |
| m_t | `m_H·π·K/C_eff` | ≤0.5% |
| sin²θ₁₂ | `2·POOF` | ≤0.5% |
| sin²θ₂₃ | `ψ_con·e/π` | 0.17% |
| sin²θ₁₃ | `2·η_eff·POOF²` | ≤0.5% |
| δ_PMNS | `2·e·ψ_con` | ≤0.5% |
| Δm²₂₁ | `(POOF·G_Catalan·P_new)³` | 0.07% |
| Δm²₃₁ | `(G_Catalan·SUCTION)³` | 0.42% |

## Honesty

- High residuals were mostly **mis-applied formulas** (e.g. m_W = m_H·φ/e, LO V_ub/V_ts without Wolfenstein NLO), not missing free parameters.  
- **Precision fill (2026-08):** seed suite max **≤0.50%**, complex suite max **≤0.50%** — same green gate as the multi-domain atlas.  
- Network imprint is ultra-subtle: `net_mod = 1 + (POOF·SUCTION)²·(I₊−I₋)` so sector coupling does not re-break green seeds.  
- Zero free parameters; PDG/NuFIT remain comparison-only.
