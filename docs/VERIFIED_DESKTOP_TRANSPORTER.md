# FSOT Verified Desktop — Transporter Simulation Stack

*Supplementary engineering volume · 2026-07-16 · [Return to main thesis](../README.md#viii-engineering-demonstrations)

> **Scope note:** This document describes a **simulation-tier engineering stack**, not a claim that FSOT has demonstrated physical teleportation. The panel lives in the verification architecture as an extension of seed-scalar readouts across information-theory and quantum-channel proxies. It is **deliberately excluded from the main README** to keep the primary preprint focused on cross-domain empirical and formal proof.

## 1. What this volume is

The **Star Trek Transporter Live Panel** (`Star_Trek_Transporter_Live_Panel`) is a multi-layer desktop simulator that tests whether the same seed-derived scalar engine can coordinate engineering observables across:

- Quantum information channel proxies
- Pattern-buffer and scan-resolution engineering metrics
- Portal / traverse scalar readouts
- Beam-forming and acoustic-valve hardware simulators
- Two-gate entanglement closure

Lean module: `FSOT.Formal.StarTrekTransporterLivePanelPriors`

## 2. Headline metrics (live benchmark)

| Metric | Value |
|--------|------:|
| Records | 1575 |
| Pooled median error | 0.031159% |
| Benchmark | `data/star_trek_transporter_live_panel_benchmark.json` |
| Figure | `data/figures/verified_desktop_transporter.png` |

![Verified desktop transporter stack](../data/figures/verified_desktop_transporter.png)

## 3. Eleven-layer stack (simulation)

1. Quantum channel  
2. Information theory  
3. Poof/suction portal  
4. Transporter engineering  
5. Warp actuation  
6. Black-hole / white-hole portal crosswalk  
7. Beam-forming grid  
8. T3 acoustic scan valve  
9. Pad A hardware  
10. Pad B receiver  
11. Two-gate entanglement  

Simulators: `vendor/verified_desktop/star_trek_transporter/`

## 4. Preregistered predictions (transporter subset)

| ID | Name | FSOT branch | Discriminant |
|----|------|-------------|--------------|
| PRED-036 | fsot_transporter_technology_stack | `term3.poof_factor` | within_10pct_of_observed_gap |
| PRED-039 | transporter_pattern_buffer_beam_grid | `term3.acoustic_bleed` | within_10pct_of_observed_gap |
| PRED-040 | transporter_t3_acoustic_valve_hardware | `term3.acoustic_bleed` | within_10pct_of_observed_gap |
| PRED-041 | transporter_pad_b_receiver_hardware | `term3.acoustic_bleed` | within_10pct_of_observed_gap |
| PRED-038 | transporter_portal_traverse_scalar | `term1.perceived_adjust` | fsot_exceeds_sota_by_0.4 |
| PRED-037 | blackhole_whitehole_cycle_constant_drift | `term3.poof_factor` | within_10pct_of_observed_gap |

Full registry: `data/preregistered_predictions_manifest.yaml`

## 5. Reproduction

```bash
python scripts/reproduce_domain_panel.py --panel Star_Trek_Transporter_Live_Panel --deep
python scripts/build_verified_desktop_transporter_figure.py
python vendor/verified_desktop/star_trek_transporter/pattern_buffer_beam_simulator.py --deep
python vendor/verified_desktop/star_trek_transporter/two_gate_entanglement_simulator.py
```

Cross-proof closure (includes this panel among verified-desktop set):

```bash
python scripts/build_verified_desktop_cross_proof_closure.py
```

## 6. Relationship to the main thesis

- **Main README (§VIII):** fuels, machine-and-molecule catalog, black-hole / white-hole cycle — engineering demos with direct thermochemistry / catalog anchors.
- **This volume:** speculative propulsion / information-transport **simulation** kept in-repo for completeness and preregistration integrity.
- **Appendix XII:** panel still listed under Engineering cluster; detail remains in chapter `06_engineering_propulsion.md`.
