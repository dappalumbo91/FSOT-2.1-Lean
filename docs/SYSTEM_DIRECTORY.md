# FSOT system directory

Where everything lives. Live counts: [`CURRENT_STATUS.md`](CURRENT_STATUS.md). What the numbers mean: [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md).

This is **one theory**, pin **D1D38A**. Siblings are folds, not other laws.

---

## 0. Start here (three audiences)

| You | First file | Then |
|-----|------------|------|
| Anyone | [`CONCEPTS.md`](CONCEPTS.md) | 25-D fluid, yin–yang valves, BH as information flow, bubble H₀ |
| Applying it | [`APPLY.md`](APPLY.md) | densify rules + kill criteria |
| Checking it | [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md) | 15-minute kill path |
| Scientist | [`FSOT_MATH_KEY_ONEPAGER.md`](FSOT_MATH_KEY_ONEPAGER.md) | [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) |
| Mathematician | [`FSOT_MATHEMATICIAN_HOWTO.md`](FSOT_MATHEMATICIAN_HOWTO.md) | `FSOT/Formal/Scalar.lean` |
| ToE checklist | [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md) | Label A now · Label B T1–T6 frozen |

---

## 1. The law (one engine)

| Piece | Path |
|-------|------|
| Executable pin | `vendor/fsot_compute.py` (SHA prefix **D1D38A**) |
| Lean twin | `FSOT/Scalar.lean` · `FSOT/Formal/` |
| Dynamics | `vendor/fsot_dynamics.py` |
| GR / SM package | `vendor/fsot_gr_sm.py` · `vendor/fsot_ckm_pmns.py` |
| Coupled tanks \(\kappa_{ij}\) | `vendor/fsot_complex_interaction.py` · [`COMPLEX_SYSTEM_DERIVATION.md`](COMPLEX_SYSTEM_DERIVATION.md) |
| Ontology A1–A6 | `data/foundational_ontology_axioms.yaml` |

Picture → engine: [`CONCEPTS.md`](CONCEPTS.md) C1–C12.

---

## 2. How a domain is a fold (not a silo)

```text
substance / scale
    → pick D_eff + observed  (interface)
    → S = K(T1+T2+T3)
    → computed = measured × (1 + |S| × f)
    → median residual ≤ 0.5%  or change the interface
```

| Artifact | Role |
|----------|------|
| Core 35 | `FSOT_SYSTEM_MATH_AUDIT.md` · navigator |
| Extensions | `data/extension_domains_manifest.yaml` |
| Atlas (named rows) | `data/publication/domain_atlas.csv` (~403) |
| Green files | `data/benchmark_margin_audit.json` (**472/472**) |
| Application protocol | [`APPLY.md`](APPLY.md) · MPCORB worked example `MPCORB_REFINEMENT_PROCESS.md` |

---

## 3. Predictions vs results

| Folder | Meaning |
|--------|---------|
| `predictions/` | Frozen forecasts (SHA + timestamp). Do not rewrite centrals. |
| `results/` | What landed later (literature, APIs, monitor). |
| `results/siblings/` | Genetics product + Quantum fold headlines |

---

## 4. Verification layers (do not collapse)

| Layer | What | Artifact |
|-------|------|----------|
| **A** Engine math | identities, Lean/Coq/Isabelle/F*/Rust | `data/cross_proof_verification_report.json` |
| **B** Empirical | measured vs computed | `data/benchmark_margin_audit.json` |
| **C** Live streams | APIs still reachable | `data/live_api_health_report.json` |

Honesty: [`RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`](RESIDUAL_HONESTY_AND_CLAIM_TIERS.md)

---

## 5. ToE labels (frozen)

| Label | Meaning | Status file |
|-------|---------|-------------|
| **A** | Multi-domain seed-locked framework, ≤0.5% green, multiprover, kills | A1–A6 hold |
| **B** | Classical ToE checklist T1–T6 | `data/toe_gap_closure_report.json` |

Open **research** (not failed A/B): path-integral confinement uniqueness, spin-2 Fock uniqueness, Einstein–Hilbert measure uniqueness. Written in the gap report.

---

## 6. Sibling folds (same pin)

| Repo | Job |
|------|-----|
| [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics) | Protein / codon product vs bulk |
| [FSOT-Quantum](https://github.com/dappalumbo91/FSOT-Quantum) | QM/QC folds, not Hilbert \(2^n\) |
| [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) | Neural mind |
| [FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) | Owned operators |
| Physical Archive | `I:\FSOT-Physical-Archive` |

Map: [`../RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md)

---

## 7. Chapter index (26 clusters)

`data/publication/readme_domain_chapters/INDEX.md` — cosmology through verification infrastructure. Use after CONCEPTS, not instead of it.

---

## 8. Commands

```powershell
python scripts/audit_all_benchmark_margins.py          # Layer B
python scripts/live_api_health_check.py                # Layer C
python scripts/run_prediction_monitor.py --online
python scripts/sync_sibling_embodiment_ledgers.py
python scripts/build_repo_status_snapshot.py
python scripts/build_toe_gap_closure.py
```

Cross-prover (after granular fills, not first):

```powershell
python scripts/run_cross_proof_verification.py
```
