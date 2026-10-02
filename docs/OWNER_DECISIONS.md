# Owner decisions OD-1 and OD-2, and the Γ_Z/M_Z target (2026-10-02)

Damian Palumbo made these decisions on 2026-10-02 at 18:10 EDT. This note records the hub implementation. The C++ record is FSOT-2.1-Cpp `audit/OWNER_DECISIONS_2026-10-02i.md` (commit e023f46) and the rescored gate `audit/precision_2026-10-02.md` (87/91 confirmed with the decisions, 85/91 pinned only). Evidence for the neutrino object is FSOT-2.1-Cpp FREEZE_2026-10-02h DM-R1.

No constant, gate, or other domain parameter was changed. `derived_D_eff` is unchanged. Preregistration `TOE-PREREG-20260909` stays on its original pin. These post-prereg owner decisions are reported separately from preregistered results.

New authority `2C9442B7295A1D39928C5C7CCB81280B443210681FAA74C4D8D4DF37D43A23D2` (owner decisions OD-1/OD-2 + Γ_Z/M_Z target fix, 2026-10-02); previous AEB2AD. That digest is the CRLF bytes of `vendor/fsot_compute.py`. `scripts/fsot_hash_gate.py` stores it as `AUTHORITY_SHA256`. `PREVIOUS_OWNER_OD_SHA256` stores `AEB2ADAD6E80F487772C5DF90A2E3DDA71624AB831A6A83B94AB471AC9AAC170`. Prediction freezes, including `predictions/domain_freezes/AEB2AD_mapping.json`, Paper 03, and `TOE-PREREG-20260909`, were not rewritten. `scripts/audit_parameter_count.py` rewrites `data/domain_table_freeze.json` when the pin prefix changes. That file is the identity freeze for the new pin. Desktop copies of `fsot_compute.py` were not edited.

## OD-1 — neutrino ratio object is Δm²₂₁/Δm²₃₁ (normal ordering)

The formula stays `γ³·Poof`. The computed value is unchanged: `0.02951701148028642063`.

| | Before | After |
|---|---|---|
| Row name | `Dm2_21/Dm2_32` | `Dm2_21/Dm2_31` |
| Display target | `0.0295` | `0.029759` |
| Comparison | Δm²₂₁/Δm²₃₂, z 1.42 | Δm²₂₁/Δm²₃₁ = 0.0297593 ± 0.000765, z 0.3167 |

PDG 2024, normal ordering, rpp2024-sum-leptons: Δm²₂₁ = 7.53(18)×10⁻⁵ eV², Δm²₃₂ = 2.455(28)×10⁻³ eV², so Δm²₃₁ = 2.5303×10⁻³ eV². The Result target is the display value `mpf("0.029759")`. The cited σ is 0.000765. z is |0.02951701148028642 − 0.0297593| / 0.000765.

Flavor literature anchors follow the same object. The key stays `dm2_31_abs`. The reference becomes 2.5303×10⁻³, and `neutrino_m3_over_m2` uses `sqrt(2.5303e-3 / 7.53e-5)`, in `vendor/fsot_seed_flavor.py`, `vendor/fsot_complex_interaction.py`, and `vendor/fsot_gr_sm.py`. No seed formula changed. `scripts/atmospheric_neutrino_seed_check.py` already calls the seed splitting `dm2_31`. Its docstring now cites OD-1. The NuFIT adopted bars in that script were not retuned.

## OD-2 — Quantum_Mechanics live D_eff is 6

`OWNER_D_EFF_OVERRIDES = {"Quantum_Mechanics": 6}` is applied in `_build_domains()`. `derived_D_eff("Quantum_Mechanics")` still returns 5.

Provenance: Quantum_Mechanics D_eff was 6 in D1D38A (012e5c64, 2026-08-04) and in 3090BC (ba6a8288, 2026-09-11 15:19:52 −0400, `data/domain_table_freeze.json`). Commit 3c74a180 (2026-09-11 15:28:37 −0400, pin FE23A2) introduced `derived_D_eff`, which gives 5 for generation 1.

`S_QUANT = domain_scalar("Quantum_Mechanics")`.

| Row | Before (D_eff 5) | After (D_eff 6) |
|---|---:|---:|
| S_QUANT | 0.95019747016701420407 | 0.95528934009164053391 |
| m_H/m_W | 1.550836826006469 | 1.559147371593332 |
| Omega_Lambda | 0.6827360381352781 | 0.6846092323976673 |
| sigma_8 | 0.8083818394107467 | 0.8109398793679822 |
| M_W/M_Z | 0.8753736653192966 | 0.8812024809968741 |
| \|V_us\| | 0.2295864790996646 | 0.2244946091750383 |
| \|V_cb\| | 0.04191887880725658 | 0.04214351156515606 |
| Ising2D_gamma | 1.248223871739745 | 1.237642523444749 |

m_H/m_W matches the 3090BC lineage value. The owner record cites z 0.96 for that row. M_W/M_Z, |V_us|, |V_cb|, and Ising2D_gamma also return to the pin-3090BC readings. The `Result` sigma on M_W/M_Z is a weight of 0.1, not the experimental uncertainty.

Rows that do not use S_QUANT stay put: Omega_b_h2 0.02246162141864744, Omega_m 0.3153291882450067, Omega_DM_h2 0.1205858200965383, m_t/m_W 2.149765929068164.

### Extension folds

`scripts/derive_extension_folds.py` sets each fold's D_eff from `derived_D_eff(parent)`, not from `DOMAINS[parent].D_eff`. The override does not move them. `derive_extension_folds.py` was not run. These five Quantum_Mechanics parents stay at D_eff 5, before and after:

- Founding_Quantum_Vacuum_Panel
- Microtubule_Quantum_Consciousness_Panel
- Quantum_Information
- Quantum_Materials
- Quantum_Mechanics_Entanglement_Depth_Panel

`scripts/assert_derived_folds.py` checks `derived_D_eff("Quantum_Mechanics") == derived_D_eff("Particle_Physics")`. That remains true. The same script used to require `S_QUANT` to stay off `S_CHEM`, which was the D_eff 5 signature. Live `S_QUANT` now matches `S_CHEM` because both sit at D_eff 6. `Omega_b_h2` still multiplies `S_CHEM` (`|S_cosm|·(1 − S_chem)`), and that chemistry reading stays inside 0.5% of 0.02237. The kill-path now requires the live override to be 6 and the derived nest to stay 5.

### Ledger B

Stored Ledger B verdicts were not regenerated. `scripts/close_ledger_b.py` restamps `ledger_b_closed_at` and classifies stored medians. It does not recompute physics from S_QUANT, so a close would not move a verdict and would dirty benchmark clocks. It was not run. `data/ledger_b_closure.json` stays stamped with the pin it was closed under.

## Γ_Z/M_Z target

The formula stays `φ⁵/e⁶`. Computed value 0.027489782887668835. The old target `0.02749` was that output. The target is now `mpf("0.027366")`.

PDG 2024, rpp2024-sum-gauge-higgs-bosons: Γ_Z/M_Z = 2.4955(23)/91.1880(20) = 0.027366(25). z versus σ 0.000025 is 4.951. The row stays a miss. No extra sigma argument was added to `Result`.
