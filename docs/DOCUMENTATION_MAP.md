# Documentation map — who reads what

**Purpose:** One accurate front door so PhD readers, working scientists, and lay readers do not get lost in old numbers or the wrong tone.  
**Live status (always prefer this over memorized counts):** [`CURRENT_STATUS.md`](CURRENT_STATUS.md)  
**Regenerate status:** `python scripts/build_repo_status_snapshot.py`

---

## Three audiences, three depths

| Audience | Start here | Then | Depth / tone |
|----------|------------|------|----------------|
| **Layman** (curious, no degree required) | [`FSOT_EXPLAINED_LAYMAN.md`](FSOT_EXPLAINED_LAYMAN.md) | [`FSOT_NARRATIVE_CORE.md`](FSOT_NARRATIVE_CORE.md) → [`START_HERE.md`](START_HERE.md) | Stories, metaphors, honest non-claims |
| **Scientist / engineer** | [`FSOT_MATH_KEY_ONEPAGER.md`](FSOT_MATH_KEY_ONEPAGER.md) | Full [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) → [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | Seeds, residual law, gates, commands |
| **PhD / formal methods** | [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) §0–3 + §7 + §PhD | [`VERIFICATION_HONESTY_AND_ISABELLE_MATH.md`](VERIFICATION_HONESTY_AND_ISABELLE_MATH.md) · [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md) · Lean `FSOT/Formal/Scalar.lean` | Layers A/B/C, what is *proved* vs residual-gated |

Everyone who will **run code** also reads [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) or the skeptic kit.

---

## Accuracy rule (non-negotiable)

1. **Pin** = first 6 hex of SHA-256 of `vendor/fsot_compute.py` (must be **D1D38A** when pin_match is true).  
2. **Green count** = `data/benchmark_margin_audit.json` → `green_gate_pass_count` / `benchmark_file_count` (gate ≤ **0.5%** pooled median).  
3. **Multiprover** = `data/cross_proof_verification_report.json` → `overall_ok`.  
4. If a doc disagrees with [`CURRENT_STATUS.md`](CURRENT_STATUS.md), **the status file wins** until the doc is regenerated.

Hand-edited numbers go stale. Prefer generators:

| Doc | Generator |
|-----|-----------|
| `CURRENT_STATUS.md` | `python scripts/build_repo_status_snapshot.py` |
| `FSOT_MATH_KEY_ONEPAGER.md` (+ PDF if reportlab present) | `python scripts/build_fsot_math_key_onepager.py` |
| `SKEPTIC_REPLICATION_KIT.md` | `python scripts/build_skeptic_replication_kit.py` |

---

## Claim language (all audiences)

| Allowed when true | Not allowed |
|-------------------|-------------|
| Label A empirical framework (green gate + multiprover + zero free params) | “Proved the universe in Coq” |
| Label B under frozen T1–T6 checklist | “Peer-reviewed” without arXiv/journal |
| Residual ≤ 0.5% on named panel | Free-parameter fit to a measurement |
| Exported residual inequality re-proved in Lean/Coq/… | Prover re-downloaded every catalog |

Frozen criteria: [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md).

---

## Reproducibility ladder

| Speed | Doc / command |
|-------|----------------|
| ~15 min kill path | [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md) |
| Full human guide | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |
| Lean-first formal | [`../REPRODUCE.md`](../REPRODUCE.md) |
| Publication bundle | `python scripts/run_publication_verification_bundle.py` |
| Cross-prover (long) | `python scripts/run_cross_proof_verification.py` |

---

## Hardware / mind (optional track)

| Doc | Role |
|-----|------|
| [`NEURON_ZIG_TO_OS_ROADMAP.md`](NEURON_ZIG_TO_OS_ROADMAP.md) | Mind → trinary OS → bare metal (direction, not shipped full OS) |
| [`ENGINEERING_HARDWARE_CODE_DIRECTION.md`](ENGINEERING_HARDWARE_CODE_DIRECTION.md) | Engineering rails |

---

## Related embodiments (same pin)

[`../RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md) — Zig mind, neural monorepo, GPU operators. Do not evaluate one without the pin story.
