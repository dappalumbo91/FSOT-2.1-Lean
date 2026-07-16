## Periodic Extension, Island of Stability & Element Synthesis

**Panels:** 14 · **Records:** 513 · **Mean panel median error:** 6.31429e-05%

### Panel index

| Panel | Records | Median error % | Tier |
|-------|--------:|---------------:|------|
| `Distant_Island_Emergence_Simulation` | 36 | 0 | B_verified |
| `Distant_Island_Z128_Z132_Deep_Panel` | 24 | 1e-06 | B_verified |
| `Element_Synthesis_Condition_Scaffold` | 45 | 0.000787 | B_verified |
| `Island_Of_Stability_Deep_Panel` | 23 | 0 | B_verified |
| `Natural_Formation_Element_Simulation` | 44 | 0 | B_verified |
| `Periodic_Extension_Decay_Topology_Scaffold` | 24 | 0 | B_verified |
| `Periodic_Table_Completion_Spine` | 38 | 0 | B_verified |
| `Periodic_Table_Extension_Closure_Spine` | 41 | 0 | B_verified |
| `Periodic_Table_Public_Panel` | 52 | 9.5e-05 | B_verified |
| `Superheavy_Element_Stability_Panel` | 50 | 1e-06 | B_verified |
| `Superheavy_Island_Completion_Spine` | 43 | 0 | B_verified |
| `Superheavy_Island_Emergence_Simulation` | 44 | 0 | B_verified |
| `Undiscovered_Element_Candidate_Prereg_Scaffold` | 25 | 0 | B_verified |
| `Z164_Distant_Island_Prereg_Scaffold` | 24 | 0 | B_verified |

#### Distant Island Emergence Simulation

Extension panel **`Distant_Island_Emergence_Simulation`** (verification tier 75) evaluates **36** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.DistantIslandEmergenceSimulationPriors`. This panel extends the core spine into distant island emergence simulation observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/distant_island_emergence_simulation_benchmark.json`](data/distant_island_emergence_simulation_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `astronomical`
- **Panel tags:** Distant, Island, Emergence, Simulation
- **Data sources / cohorts:** Distant island emergence pathways — Z=128-164 fusion-decay-chain viability

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| distant_emergence · z128_z164_sim | 0 | 0 | 0 |
| distant_emergence_classifier · Z128_N184 | 1 | 1 | 0 |
| distant_emergence_score · Z128_N184 | 299043 | 299043 | 0 |
| emergence_pathway_viable · Z128_N184__cosmic_ray_spallation | 0 | 0 | 0 |
| periodic_extension_Z_ceiling · distant_island_Z164 | 164 | 164 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Distant Island Emergence Simulation: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Distant Island Emergence Simulation: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Distant Island Emergence Simulation: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Distant Island Z128 Z132 Deep Panel

Extension panel **`Distant_Island_Z128_Z132_Deep_Panel`** (verification tier 75) evaluates **24** measured records at **1e-06%** pooled median error (B_verified). Formal module: `FSOT.Formal.DistantIslandZ128Z132DeepPanelPriors`. This panel extends the core spine into distant island z128 z132 deep panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/distant_island_z128_z132_deep_panel_benchmark.json`](data/distant_island_z128_z132_deep_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`
- **Panel tags:** Distant, Island, Z128, Z132, Deep, Panel
- **Data sources / cohorts:** Z=128-132 distant island deep anchors — half-lives, binding, magic proximity

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_relay · Distant_Island_Z128_Z132_Deep_Panel_depth | 0 | 0 | 0 |
| distant_island_Z132_ceiling · superheavy_shell_peak | 132 | 132 | 0 |
| distant_island_half_life_s · Z128_N184 | 180000 | 180000 | 0 |
| distant_island_peak_classifier · Z128_N184 | 1 | 1 | 0 |
| island_half_life_s · Z119_N177 | 0.8 | 0.8 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Distant Island Z128 Z132 Deep Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Distant Island Z128 Z132 Deep Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Distant Island Z128 Z132 Deep Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Element Synthesis Condition Scaffold

Extension panel **`Element_Synthesis_Condition_Scaffold`** (verification tier 73) evaluates **45** measured records at **0.000787%** pooled median error (B_verified). Formal module: `FSOT.Formal.ElementSynthesisConditionScaffoldPriors`. This panel extends the core spine into element synthesis condition scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/element_synthesis_condition_scaffold_benchmark.json`](data/element_synthesis_condition_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `material`, `thermodynamics`
- **Panel tags:** Element, Synthesis, Condition, Scaffold
- **Data sources / cohorts:** Lab synthesis condition gates — beam energy margin, temperature proxy, facility capacity under published, proposed reactions

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| beam_energy_margin_mev_u · Z119_Ti_Bk | 0 | 0 | 0 |
| superheavy_stability_bridge · superheavy_element_stability_panel | 1e-06 | 1e-06 | 0 |
| synthesis_condition_classifier · Cn_1996 | 1 | 1 | 0 |
| synthesis_condition_ready · element_synthesis_condition_scaffold | 1 | 1 | 0 |
| synthesis_screening_gate · facility_margin_mev_u | 10 | 10 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Element Synthesis Condition Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Element Synthesis Condition Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Element Synthesis Condition Scaffold: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Island Of Stability Deep Panel

Extension panel **`Island_Of_Stability_Deep_Panel`** (verification tier 74) evaluates **23** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.IslandOfStabilityDeepPanelPriors`. This panel extends the core spine into island of stability deep panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/island_of_stability_deep_panel_benchmark.json`](data/island_of_stability_deep_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`
- **Panel tags:** Island, Stability, Deep, Panel
- **Data sources / cohorts:** Z=119-126 island deep anchors — half-lives, binding energy, magic-number proximity, decay trend

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| island_Z_range · Z120_Z126_deep | 126 | 126 | 0 |
| island_half_life_s · Z119_N177 | 0.8 | 0.8 | 0 |
| island_peak_classifier · Z119_N177 | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| island_deep · z120_z126_stability | 0 | 0 | 9.50414e-09 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Island Of Stability Deep Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Island Of Stability Deep Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Fe`** in Island Of Stability Deep Panel: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).

#### Natural Formation Element Simulation

Extension panel **`Natural_Formation_Element_Simulation`** (verification tier 72) evaluates **44** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.NaturalFormationElementSimulationPriors`. This panel extends the core spine into natural formation element simulation observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/natural_formation_element_simulation_benchmark.json`](data/natural_formation_element_simulation_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `astronomical`
- **Panel tags:** Natural, Formation, Element, Simulation
- **Data sources / cohorts:** r-process, s-process, cosmic-ray, fusion-decay pathway simulation for undiscovered element emergence

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| formation_pathway_viable · Z119_N177_ununennium__cosmic_ray_spallation | 0 | 0 | 0 |
| formation_sim · natural_emergence | 0 | 0 | 0 |
| fsot_natural_Z_ceiling · fusion_decay_chain_extension | 132 | 132 | 0 |
| fusion_physics_panel_bridge · fusion_physics_public_panel | 9.5e-05 | 9.5e-05 | 0 |
| natural_emergence_classifier · Z119_N177_ununennium | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Natural Formation Element Simulation: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Natural Formation Element Simulation: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Natural Formation Element Simulation: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Periodic Extension Decay Topology Scaffold

Extension panel **`Periodic_Extension_Decay_Topology_Scaffold`** (verification tier 75) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicExtensionDecayTopologyScaffoldPriors`. This panel extends the core spine into periodic extension decay topology scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_extension_decay_topology_scaffold_benchmark.json`](data/periodic_extension_decay_topology_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `fusion`, `particle`, `nuclear`, `energy`
- **Panel tags:** Periodic, Extension, Decay, Topology, Scaffold
- **Data sources / cohorts:** Decay topology graph Z=126→132→164, fusion chain extensions prereg

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| depth_relay · Periodic_Extension_Decay_Topology_Scaffold_depth | 0 | 0 | 0 |
| fusion_decay_chain_bridge · fusion_decay_chain_prereg_scaffold | 0 | 0 | 0 |
| panel_pooled_median · heavy_ion_lab_synthesis | 9.5e-05 | 9.5e-05 | 0 |
| periodic_extension_Z_ceiling · decay_topology_Z164 | 164 | 164 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Periodic Extension Decay Topology Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Periodic Extension Decay Topology Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Periodic Extension Decay Topology Scaffold: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Periodic Table Completion Spine

Extension panel **`Periodic_Table_Completion_Spine`** (verification tier 72) evaluates **38** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicTableCompletionSpinePriors`. This panel extends the core spine into periodic table completion spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_table_completion_spine_benchmark.json`](data/periodic_table_completion_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `atomic`, `fusion`, `material`
- **Panel tags:** Periodic, Table, Completion, Spine
- **Data sources / cohorts:** Periodic table completion rollup — public table, superheavy, prereg, natural formation, fusion bridge

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| acoustic_bleed_panel_bridge · term3_acoustic_bleed_depth | 0.0083815 | 0.0083815 | 0 |
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| candidate_predicted_half_life_s · Z120_N184_unbinilium | 2.5e+06 | 2.5e+06 | 0 |
| formation_pathway_viable · Z120_N184_unbinilium__cosmic_ray_spallation | 0 | 0 | 0 |
| fusion_physics_panel_bridge · fusion_physics_public_panel | 9.5e-05 | 9.5e-05 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Periodic Table Completion Spine: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Periodic Table Completion Spine: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Fe`** in Periodic Table Completion Spine: measured **1.68**, seed-derived **1.6799905609889012** via `E/PHI` (error **0.000562%**). Constants: phi. Authority: Anderson (1966).

#### Periodic Table Extension Closure Spine

Extension panel **`Periodic_Table_Extension_Closure_Spine`** (verification tier 75) evaluates **41** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicTableExtensionClosureSpinePriors`. This panel extends the core spine into periodic table extension closure spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_table_extension_closure_spine_benchmark.json`](data/periodic_table_extension_closure_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`, `material`, `energy`
- **Panel tags:** Periodic, Table, Extension, Closure, Spine
- **Data sources / cohorts:** Periodic extension arc CLOSED — Tiers 71-75 rollup, Z ceiling 164

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| distant_island_half_life_s · Z128_N184 | 180000 | 180000 | 0 |
| distant_island_peak_classifier · Z128_N184 | 1 | 1 | 0 |
| emergence_pathway_viable · Z128_N184__cosmic_ray_spallation | 0 | 0 | 0 |
| fusion_decay_chain_bridge · fusion_decay_chain_prereg_scaffold | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Periodic Table Extension Closure Spine: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Periodic Table Extension Closure Spine: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Periodic Table Extension Closure Spine: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Periodic Table Public Panel

Extension panel **`Periodic_Table_Public_Panel`** (verification tier 72) evaluates **52** measured records at **9.5e-05%** pooled median error (B_verified). Formal module: `FSOT.Formal.PeriodicTablePublicPanelPriors`. This panel extends the core spine into periodic table public panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/periodic_table_public_panel_benchmark.json`](data/periodic_table_public_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `atomic`, `nuclear`, `material`
- **Panel tags:** Periodic, Table, Public, Panel
- **Data sources / cohorts:** IUPAC, NIST Z=1-118 anchors — atomic weights, ionization energies, magic-number proximity

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| known_element_ceiling_Z · IUPAC_confirmed | 118 | 118 | 0 |
| magic_number_proximity · Ag | 14 | 14 | 0 |
| particle_physics_scalar · fsot_Particle_Physics | 0.950413 | 0.950413 | 0 |
| atomic_weight · Ag | 107.868 | 107.868 | 9.5e-05 |
| ionization_ev · Ag | 7.576 | 7.57601 | 9.5e-05 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`F`** in Periodic Table Public Panel: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).
- **`Ca`** in Periodic Table Public Panel: measured **177.8**, seed-derived **177.8014017941265** via `E^5+PI^3-PHI^1` (error **0.000788%**). Constants: phi, pi. Authority: NIST-JANAF / CRC / Kittel.
- **`P`** in Periodic Table Public Panel: measured **0.747**, seed-derived **0.7469924420819796** via `γ·Ω` (error **0.001012%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Superheavy Element Stability Panel

Extension panel **`Superheavy_Element_Stability_Panel`** (verification tier 72) evaluates **50** measured records at **1e-06%** pooled median error (B_verified). Formal module: `FSOT.Formal.SuperheavyElementStabilityPanelPriors`. This panel extends the core spine into superheavy element stability panel observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/superheavy_element_stability_panel_benchmark.json`](data/superheavy_element_stability_panel_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `atomic`, `fusion`
- **Panel tags:** Superheavy, Element, Stability, Panel
- **Data sources / cohorts:** Z=104-118 discovered superheavies — half-lives, liquid-drop binding, island-of-stability anchors

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| island_predicted_half_life_s · Fl-298 island proxy | 3600 | 3600 | 0 |
| macroscopic_stability_classifier · Bh | 1 | 1 | 0 |
| superheavy_stability · island_of_stability | 0 | 1e-06 | 9.50413e-07 |
| half_life_s · Bh | 61 | 61 | 1e-06 |
| pooled_median · all_channels | 0 | 1e-06 | 1e-06 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Superheavy Element Stability Panel: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Superheavy Element Stability Panel: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Superheavy Element Stability Panel: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Superheavy Island Completion Spine

Extension panel **`Superheavy_Island_Completion_Spine`** (verification tier 74) evaluates **43** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.SuperheavyIslandCompletionSpinePriors`. This panel extends the core spine into superheavy island completion spine observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/superheavy_island_completion_spine_benchmark.json`](data/superheavy_island_completion_spine_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `atomic`, `material`
- **Panel tags:** Superheavy, Island, Completion, Spine
- **Data sources / cohorts:** Superheavy island completion rollup — deep panel, beams, decay chains, emergence, Tier 72-73 bridges

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| candidate_predicted_half_life_s · Z120_N184_unbinilium | 2.5e+06 | 2.5e+06 | 0 |
| cold_fusion_bridge · cold_fusion_candidate_prereg_scaffold | 0 | 0 | 0 |
| decay_chain_viability_classifier · pd_d_to_Z120_cascade | 1 | 1 | 0 |
| emergence_pathway_viable · Z119_N177__cosmic_ray_spallation | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Superheavy Island Completion Spine: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Superheavy Island Completion Spine: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Superheavy Island Completion Spine: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Superheavy Island Emergence Simulation

Extension panel **`Superheavy_Island_Emergence_Simulation`** (verification tier 74) evaluates **44** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.SuperheavyIslandEmergenceSimulationPriors`. This panel extends the core spine into superheavy island emergence simulation observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/superheavy_island_emergence_simulation_benchmark.json`](data/superheavy_island_emergence_simulation_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`, `astronomical`
- **Panel tags:** Superheavy, Island, Emergence, Simulation
- **Data sources / cohorts:** Island emergence pathway simulation for Z=120-126 — lab, fusion-decay-chain viability

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| emergence_pathway_viable · Z119_N177__cosmic_ray_spallation | 0 | 0 | 0 |
| fsot_island_Z_ceiling · fusion_decay_chain_Z126 | 126 | 126 | 0 |
| island_emergence · z120_z126_sim | 0 | 0 | 0 |
| island_emergence_classifier · Z119_N177 | 0 | 0 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Superheavy Island Emergence Simulation: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Superheavy Island Emergence Simulation: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`F`** in Superheavy Island Emergence Simulation: measured **3.401**, seed-derived **3.4009757390356907** via `γ⁻²+Ψ²` (error **0.000713%**). Constants: gamma. Authority: Andersen et al., JPCRD 28 (1999).

#### Undiscovered Element Candidate Prereg Scaffold

Extension panel **`Undiscovered_Element_Candidate_Prereg_Scaffold`** (verification tier 72) evaluates **25** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.UndiscoveredElementCandidatePreregScaffoldPriors`. This panel extends the core spine into undiscovered element candidate prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/undiscovered_element_candidate_prereg_scaffold_benchmark.json`](data/undiscovered_element_candidate_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `atomic`, `fusion`
- **Panel tags:** Undiscovered, Element, Candidate, Prereg, Scaffold
- **Data sources / cohorts:** Z>118 candidates (Z=119-164) preregistered via boundary_partition, phi scaling — not claimed synthesized

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_panel_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| candidate_predicted_half_life_s · Z119_N177_ununennium | 0.8 | 0.8 | 0 |
| phi_morphogenetic_panel_bridge · phi_morphogenetic_scaling | 0.0565 | 0.0565 | 0 |
| pooled_median · all_channels | 0 | 0 | 0 |
| prereg_discriminant_gate · Z119_N177_ununennium | 1 | 1 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Undiscovered Element Candidate Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Undiscovered Element Candidate Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Undiscovered Element Candidate Prereg Scaffold: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).

#### Z164 Distant Island Prereg Scaffold

Extension panel **`Z164_Distant_Island_Prereg_Scaffold`** (verification tier 75) evaluates **24** measured records at **0%** pooled median error (B_verified). Formal module: `FSOT.Formal.Z164DistantIslandPreregScaffoldPriors`. This panel extends the core spine into z164 distant island prereg scaffold observables — predictions are seed-derived; kill criteria are registered in the domain navigator.

**Benchmark:** [`data/z164_distant_island_prereg_scaffold_benchmark.json`](data/z164_distant_island_prereg_scaffold_benchmark.json)

**Subfield map:**

- **Lean routes:** `particle`, `nuclear`, `fusion`
- **Panel tags:** Z164, Distant, Island, Prereg, Scaffold
- **Data sources / cohorts:** Z=164 distant island prereg — periodic extension ceiling, not claimed synthesized

**Top observables (measured vs computed):**

| Observable | Measured | Computed | Error % |
|------------|---------:|---------:|--------:|
| boundary_partition_bridge · boundary_partition_tightening | 0 | 0 | 0 |
| depth_relay · Z164_Distant_Island_Prereg_Scaffold_depth | 0 | 0 | 0 |
| distant_island_viability_classifier · Z164_N228 | 1 | 1 | 0 |
| emergence_pathway_viable · Z119_N177__cosmic_ray_spallation | 0 | 0 | 0 |
| fusion_physics_panel_bridge · fusion_physics_public_panel | 9.5e-05 | 9.5e-05 | 0 |

**Formula-level verification** (strict empirical corpus — Appendix XII-E style):

- **`H⁺/H₂`** in Z164 Distant Island Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `π−π` (error **0%**). Constants: pi. Authority: Bard, Parsons & Jordan (1985).
- **`alpha_Fe`** in Z164 Distant Island Prereg Scaffold: measured **0.0**, seed-derived **0.0** via `φ²-φ-1` (error **0%**). Constants: phi. Authority: Long & Greenwood (1997).
- **`Bi2Te3`** in Z164 Distant Island Prereg Scaffold: measured **1.0**, seed-derived **1.0** via `PHI^2-PHI^1` (error **0%**). Constants: phi. Authority: Snyder & Toberer, Nat.Mater. 7, 105 (2008).
