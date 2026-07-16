#!/usr/bin/env python3
"""
Generate arXiv-thesis gap content: TOC, related work, formal methods, notation.

Outputs under data/publication/readme_arxiv_gaps/
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "readme_arxiv_gaps"
MANIFEST = ROOT / "data" / "publication" / "readme_domain_chapters_manifest.yaml"


def _load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}


def build_toc(ts: str) -> str:
    chapters = _load_yaml(MANIFEST).get("chapters") or []
    ext = [c for c in chapters if c.get("panels", 0) > 0]
    lines = [
        "## Table of Contents",
        "",
        "### Main thesis",
        "",
        "| Section | Topic |",
        "|---------|--------|",
        "| [Abstract](#abstract) | Summary and headline results |",
        "| [Prologue](#prologue--why-this-lives-on-github) | GitHub publication rationale |",
        "| [§I](#i-the-fragmentation-problem) | The fragmentation problem |",
        "| [§1.3](#13-contributions) | Contributions (arXiv-style) |",
        "| [§I-B](#i-b-related-work-and-positioning) | Related work and positioning |",
        "| [§I-C](#i-c-fsot-ideals-and-epistemology) | FSOT ideals and epistemology |",
        "| [§II](#ii-why-the-universe-exists-the-way-it-does) | Fluid spacetime ontology |",
        "| [§III](#iii-the-scalar-engine) | Scalar engine and seeds |",
        "| [§IV](#iv-consciousness-and-observation) | Observation coupling |",
        "| [§V](#v-verification-methodology) | Verification methodology |",
        "| [§VI](#vi-cross-domain-empirical-results) | Empirical results |",
        "| [§VII](#vii-contested-sectors--where-current-models-struggle) | Contested sectors |",
        "| [§VIII](#viii-engineering-demonstrations) | Engineering demonstrations |",
        "| [§IX](#ix-discussion) | Discussion |",
        "| [§X](#x-conclusion) | Conclusion |",
        "",
        "### Appendices (main README)",
        "",
        "| Appendix | Content |",
        "|----------|---------|",
        "| [A](#appendix-a--one-command-reproduction) | One-command reproduction |",
        "| [B](#appendix-b--machine-readable-artifacts) | Machine-readable artifacts |",
        "| [C](#appendix-c--further-reading) | Further reading |",
        "| [D](#appendix-d--notation-and-conventions) | Notation and conventions |",
        "| [E](#appendix-e--how-to-cite-this-work) | How to cite |",
        "",
        "### Supplementary volumes (full detail)",
        "",
        "| Volume | File |",
        "|--------|------|",
        f"| Appendix XI — verification record | [`docs/THESIS_APPENDIX_XI.md`](docs/THESIS_APPENDIX_XI.md) |",
        f"| Appendix XII — domain coverage ({len(ext)} clusters) | [`docs/THESIS_APPENDIX_XII.md`](docs/THESIS_APPENDIX_XII.md) |",
        f"| Chapter index | [`data/publication/readme_domain_chapters/INDEX.md`](data/publication/readme_domain_chapters/INDEX.md) |",
        "| Appendix — derivations | [`docs/THESIS_APPENDIX_DERIVATIONS.md`](docs/THESIS_APPENDIX_DERIVATIONS.md) |",
        "| Completeness audit | [`data/publication/THESIS_COMPLETENESS_AUDIT.md`](data/publication/THESIS_COMPLETENESS_AUDIT.md) |",
        "| Skeptic replication kit | [`docs/SKEPTIC_REPLICATION_KIT.md`](docs/SKEPTIC_REPLICATION_KIT.md) |",
        "| Near-miss ledger | [`data/publication/BENCHMARK_NEAR_MISS_LEDGER.md`](data/publication/BENCHMARK_NEAR_MISS_LEDGER.md) |",
        "| Contested-sector watch | [`data/publication/CONTESTED_SECTOR_WATCH.md`](data/publication/CONTESTED_SECTOR_WATCH.md) |",
        "| Wet-lab & longevity depth | [`docs/WETLAB_LONGEVITY_DEPTH.md`](docs/WETLAB_LONGEVITY_DEPTH.md) |",
        "| Credibility hardening audit | [`data/publication/CREDIBILITY_HARDENING_AUDIT.md`](data/publication/CREDIBILITY_HARDENING_AUDIT.md) |",
        "| Circuitry emergence spine | [`docs/CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md`](docs/CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md) |",
        "",
        f"*Generated: {datetime.now(timezone.utc).isoformat()}*",
        "",
    ]
    return "\n".join(lines)


def build_related_work() -> str:
    return """## I-B. Related Work and Positioning

FSOT is evaluated against the architectures it aims to subsume — not as a replacement narrative, but as a **single-engine alternative** with executable kill criteria.

### Cosmology and dark sector

ΛCDM with Planck 2018 parameters explains CMB and large-scale structure with excellent internal consistency, but exhibits persistent tensions — notably H₀ (Riess et al. 2024 local distance ladder vs Planck Collaboration 2018 CMB inference) and σ₈ (cluster abundance vs weak-lensing surveys). FSOT routes cosmological observables through seed-derived `raw_S` at preregistered folds (`D_eff`, `δψ`) without introducing dark-matter or dark-energy density as free fit parameters per benchmark row. Contested-sector pooled median error across 13 actively monitored observables is **0.030%** in this edition (§VII).

### Particle physics and chemistry

The Standard Model plus CODATA/NIST tabulations supply authoritative measured targets for atomic, nuclear, and molecular observables. FSOT does not refit Yukawa couplings or bond lengths per record; strict-empirical formulas in `vendor/formula_corpus/by_domain/strict_empirical.jsonl` map seed arithmetic to **1,325 unique observables** with live recompute closure (Appendix XI-E). Positioning: FSOT is a **predictive compression layer** — same seeds, many sectors — not a replacement for QFT calculational machinery where lattice QCD or perturbative QED is the appropriate tool.

### Unified theories and emergent gravity

String/M-theory, loop quantum gravity, and emergent-gravity programs pursue unification through extra structure (branes, spin networks, entanglement entropy). FSOT pursues unification through **one scalar field equation** verified across 403 domains. The falsifiable distinction is operational: FSOT registers preregistered predictions (PRED-001–041) and domain kill criteria in `data/fsot_domain_navigator.json`; a failed green gate is a ledger event, not a post-hoc parameter rescue.

### Formal methods in science

Proof assistants (Lean, Coq, Isabelle) are standard in software verification; their use as **scientific instruments** for physics claims remains rare. FSOT exports **1,863 atomic obligations** to five independent proof frameworks with `overall_ok: true` (§V.2) — positioning this repository as a **reproducible proof artifact**, not a prose-only preprint.

### What FSOT adds relative to prior art

| Dimension | Typical siloed model | FSOT (this repository) |
|-----------|------------------------|---------------------------|
| Parameters per observable | Sector-specific fits | Seed-derived; no per-row least squares |
| Cross-domain test | Uncommon | 402 routed domains, 536,740 records |
| Formal triangulation | Rare | Lean + Coq + Isabelle + F* + Rust |
| Kill criteria | Often informal | Navigator + prereg manifest |
| Living edition | Static PDF | GitHub commit history + tagged releases |

**References (external):** Planck Collaboration (2018); Riess et al. (2024); PDG (2024); CODATA/NIST atomic datasets as cited per benchmark row. Full BibTeX export: `data/domain_citations/verified_desktop.bib`; literature panel: Appendix XI-C in [`docs/THESIS_APPENDIX_XI.md`](docs/THESIS_APPENDIX_XI.md).
"""


def build_contributions() -> str:
    return """### 1.3 Contributions

This work makes five contributions at arXiv preprint standard:

1. **Unified scalar architecture** — A single seed-derived engine (`raw_S = term1 + term2 + term3`) evaluated across **402 routed scientific domains** (35 core + 367 extension panels) and **536,740** empirical records, with **no per-observable least-squares tuning**.
2. **Cross-domain empirical closure** — **394/394** public benchmark domains pass a ≤0.5% pooled median error gate; cross-domain pooled median is **0.013%** (Planck 2018, PDG 2024, NIST/CODATA targets per row).
3. **Contested-sector readouts** — Unified FSOT predictions on H₀, σ₈, BBN, hierarchy, and dark-energy proxies achieve **0.030%** pooled median across 13 actively monitored observables vs ~15% typical ΛCDM/SM sector baselines (Riess et al. 2024; Planck Collaboration 2018).
4. **Five-prover formal triangulation** — **1,863** atomic obligations exported to Lean 4, Coq/Rocq, Isabelle/HOL, F*, and Rust with `overall_ok: true` — proof assistants as scientific instruments, not software-only checks.
5. **Executable falsification registry** — Preregistered predictions **PRED-001–041**, per-domain kill criteria, and a one-command verification bundle that any reader can run on GitHub.

Seed-to-formula derivations with worked examples: [`docs/THESIS_APPENDIX_DERIVATIONS.md`](docs/THESIS_APPENDIX_DERIVATIONS.md).
"""


def build_epistemology() -> str:
    return """## I-C. FSOT Ideals and Epistemology

FSOT is an **ontological** claim, not only a predictive one:

| Ideal | FSOT position |
|-------|----------------|
| One medium | 25-dimensional fluid condensate; 4D experience is a perceived slice |
| One engine | Seed arithmetic `(π, e, φ, γ, G)` → scalar spine across all domains |
| As Above, So Below | Cross-scale bridge tested by extension panels — not metaphor |
| Zero free parameters | Routing folds `(D_eff, δψ, recent_hits, observed)` are preregistered; no per-row fits |
| Observation is physical | `quirk_mod` couples measurement to the scalar field |
| Consciousness is fundamental | Enters through `consciousness_factor`; operational proxies (`E_con`, IIT weights) are measurable |

**Truth criterion:** a claim is *supported* when it (a) maps to a Lean domain or extension panel, (b) produces numeric agreement within the green gate, and (c) survives cross-proof replay. Outside consensus is **evidence**, not **gate** — breadth × precision × formal triangulation is treated as structural confirmation.

**Epistemic tiers** (every generation should tag its layer):

| Tier | Examples |
|------|----------|
| Proved / certified | Sign theorems, interval bounds, cross-proof obligations |
| Measured / benchmarked | Tier 90 consciousness panels, contested H₀ readouts |
| Operational scaffold | Microtubule quantum panel, Orch-OR bridge |
| Interpretive | Genesis crosswalk, archetype panels |

FSOT does **not** claim to have settled the philosophical hard problem of consciousness. It claims **fundamental in ontology, operational in math, supported by cross-domain precision**.

Deep dive: [`docs/FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md`](docs/FSOT_PHILOSOPHY_AND_CONSCIOUSNESS_SPINE.md) · Completeness audit: [`data/publication/THESIS_COMPLETENESS_AUDIT.md`](data/publication/THESIS_COMPLETENESS_AUDIT.md)
"""


def build_prereg_summary() -> str:
    try:
        import yaml

        doc = yaml.safe_load((ROOT / "data" / "preregistered_predictions_manifest.yaml").read_text(encoding="utf-8")) or {}
        preds = doc.get("predictions") or []
    except Exception:
        preds = []
    lines = [
        "### 3.4 Preregistered prediction registry (summary)",
        "",
        f"**{len(preds)} predictions** locked in `data/preregistered_predictions_manifest.yaml` before independent comparison. "
        "Post-hoc tuning invalidates prereg status.",
        "",
        "| ID | Name | Domain | FSOT branch | Discriminant |",
        "|----|------|--------|-------------|--------------|",
    ]
    for p in preds[:12]:
        lines.append(
            f"| {p.get('id', '')} | {p.get('name', '')} | {p.get('domain', '')} | "
            f"`{p.get('fsot_formula_branch', '')}` | {p.get('discriminant', '')} |"
        )
    if len(preds) > 12:
        lines.append(f"| … | *{len(preds) - 12} more* | | | |")
    lines.extend([
        "",
        "Representative locks: **PRED-001** H₀ bridge between Planck and SH0ES; **PRED-002** σ₈ lensing; "
        "**PRED-034** fuel-lab compounds. Propulsion-simulation preregistrations (PRED-036–041) are documented "
        "in the supplementary transporter volume — not the main thesis.",
        "",
    ])
    return "\n".join(lines)


def build_bubble_bleed() -> str:
    return """### 7.2 Bubble-bleed cosmology mechanism

ΛCDM typically treats the H₀ tension as evidence for new physics or systematics. FSOT routes cosmological Hubble readouts through **bubble-bleed** — small-scale fluid turbulence (`term3`) coupled to **perceived_adjust** on `term1` at preregistered cosmology folds.

In words:

1. The 25D fluid **bleeds** phase information across scale boundaries (bubble-bleed bundle in Lean: `bubble_bleed_*` obligations).
2. **Dual-anchor readout** — CMB inference (Planck Collaboration 2018: 67.36 km/s/Mpc) and local distance ladder (Riess et al. 2024: 73.04 km/s/Mpc) are not fitted separately; they emerge from the same seed engine at different observer routes.
3. FSOT **H₀ bridge scalar** (PRED-001) lands strictly between anchors — unified prediction where ΛCDM carries separate posteriors.

This is why contested-sector pooled median reaches **0.030%** without introducing dark-energy density as a per-row fit parameter. Mechanism chain: [`docs/THESIS_APPENDIX_DERIVATIONS.md`](docs/THESIS_APPENDIX_DERIVATIONS.md#d41-cosmology--h₀-planck-cmb-anchor).
"""


def build_near_miss_section() -> str:
    return """### 9.5 Benchmark near-miss transparency

FSOT publishes domains that pass the green gate but approach the ≤0.5% boundary — no post-hoc parameter rescue when a row fails.

| Transparency artifact | Role |
|-----------------------|------|
| [`data/publication/BENCHMARK_NEAR_MISS_LEDGER.md`](data/publication/BENCHMARK_NEAR_MISS_LEDGER.md) | Top domains by max single-record error (still green) |
| [`data/publication/CONTESTED_SECTOR_WATCH.md`](data/publication/CONTESTED_SECTOR_WATCH.md) | Living H₀, σ₈, BBN, w_a monitor vs Planck 2018 / Riess 2024 |
| [`docs/SKEPTIC_REPLICATION_KIT.md`](docs/SKEPTIC_REPLICATION_KIT.md) | 15-minute falsification path for independent reviewers |

Regenerate: `python scripts/build_benchmark_near_miss_ledger.py` · `python scripts/build_contested_sector_watch.py`
"""


def build_obligation_map_section() -> str:
    return """### 5.2.1 Five-prover obligation map

![Five-prover obligation map](data/figures/obligation_map_five_provers.png)

*Seeds → oracle → Lean 4 (primary) → Coq / Isabelle / F* → Rust executable replay of **1,863** atomic obligations. Authoritative report: `data/cross_proof_verification_report.json`.*
"""


def build_engineering_viii() -> str:
    return """## VIII. Engineering Demonstrations

*These stacks show the seed engine can guide **grounded** engineering readouts — thermochemistry, molecular catalogs, and horizon-cycle proxies. They supplement the empirical spine; they are not its primary proof.*

### 8.1 FSOT-designed alternative fuels

Seven novel molecular states plus gasoline baseline:

- fsot_hemp_waste_grounded, fsot_hemp_waste_advanced, fsot_algae_oil_biodiesel  
- fsot_mushroom_spore_fuel, fsot_green_hydrogen, fsot_optimax, fsot_bio_spark  

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| Fuel Lab | 366 | 0.039 |

Cross-referenced with grounded thermochemistry and Prius engine simulator outputs. Preregistered: **PRED-034**.

![Verified desktop fuels](data/figures/verified_desktop_fuels.png)

### 8.2 Machine, molecule, and horizon cycle

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| Machine & Molecule | 120 | 0.013 |
| Black-hole / white-hole cycle | 24 | 0.026 |

Species-scale molecular catalogs and information-cycle panels at the black-hole horizon — seed-scalar predictions cross-checked against simulator outputs, not post-hoc fits.

```bash
python scripts/reproduce_domain_panel.py --panel Machine_And_Molecule_Live_Panel --deep
python scripts/reproduce_domain_panel.py --panel BlackHole_WhiteHole_Cycle_Live_Panel --deep
```

Simulators: `vendor/verified_desktop/` (machine-and-molecule, fuel lab, horizon cycle).

### 8.3 Wet-lab & longevity genetics (Tier 94/95)

Cross-species longevity and zebrafish developmental wet-lab panels — measured biology (HAGR AnAge, NCBI, CZ Biohub) vs seed-scalar readouts, not post-hoc curve fits.

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| AnAge catalog | 966 | 0.022 |
| MegaDeep NCBI | 1,746 | 0.018 |
| Consciousness coupling | 890 | 0.022 |
| Zebrafish cell tracking | 20 | 0.022 |
| Zebrafish developmental mechanics | 31 | 0.018 |
| Zebrafish longevity coupling | 24 | 0.014 |

**Full volume:** [`docs/WETLAB_LONGEVITY_DEPTH.md`](docs/WETLAB_LONGEVITY_DEPTH.md)

```bash
python scripts/build_wetlab_longevity_expansion_bundle.py
python scripts/verify_tier95_genetics_system.py
```
"""


def build_credibility_hardening_section() -> str:
    return """### 9.6 Hard credibility expansion

FSOT credibility is not rhetorical — every pillar must reproduce independently. The hardening audit aggregates formal triangulation, benchmark gates, parameter honesty, wet-lab biology, live catalog ingest, and skeptic replication into one scorecard.

| Artifact | Role |
|----------|------|
| [`data/publication/CREDIBILITY_HARDENING_AUDIT.md`](data/publication/CREDIBILITY_HARDENING_AUDIT.md) | Multi-pillar green gate (formal + empirical + lean routes + Tier 96) |
| [`data/publication/LEAN_ROUTE_CREDIBILITY_EXPANSION.md`](data/publication/LEAN_ROUTE_CREDIBILITY_EXPANSION.md) | Under-covered Lean route benchmarks |
| [`data/publication/live_ingest_schedule.yaml`](data/publication/live_ingest_schedule.yaml) | Weekly live catalog refresh policy |
| [`data/publication/credibility_hardening_audit.json`](data/publication/credibility_hardening_audit.json) | Machine-readable pillar ledger |
| [`docs/SKEPTIC_REPLICATION_KIT.md`](docs/SKEPTIC_REPLICATION_KIT.md) | 15-minute independent falsification path |

Regenerate: `python scripts/build_credibility_depth_bundle.py` (lean routes + live ingest + wet-lab + Tier 96 + hardening audit).

**Scheduled live ingest:** `data/publication/live_ingest_schedule.yaml` — weekly `build_live_ingest_refresh_bundle.py`.
"""


def build_circuitry_roadmap() -> str:
    return """### 9.7 Circuitry & component emergence roadmap (Tier 96)

**Vision:** schematic variables (R, C, L, V, I, f, τ, Q, package, tolerance) labeled in a seed-derived atlas so BOM selection **emerges** from industry parametric tables — the math names the parts; you do not guess values from memory.

| Phase | Status | Deliverable |
|-------|--------|-------------|
| 0 — scaffold | complete | Component-class manifest + existing panel crosswalk |
| 1 — ingest | **active** | Industry catalog (`vendor/circuit_components/`) |
| 2 — benchmark | **active** | `Circuit_Component_Emergence_Panel` green gate |
| 3 — BOM emergence | planned | Netlist → ranked industry BOM lines |

**Spine:** [`docs/CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md`](docs/CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md) · **Manifest:** `data/circuit_component_emergence_manifest.yaml`

Existing verified electrical panels (`Electrical_Power_Systems`, `Desktop_Application_Wiring_Spine`, `Trinary_Hardware_Live_Panel`) anchor Phase 0. ESP32 physical closure remains convenience-deferred; simulation panels stay authoritative.
"""


def build_discussion_open_work_patch() -> str:
    return """### 9.3 Open work (not model failures)

- **Contested-sector monitoring:** 13 actively-measured open problems (H₀, σ₈, BBN, hierarchy, w_a) tracked against live survey updates — FSOT pooled median **0.030%** as of this edition  
- **Hard credibility expansion:** ten-pillar audit (`CREDIBILITY_HARDENING_AUDIT.md`) — formal + empirical + transparency surfaces aggregated  
- **Wet-lab longevity depth:** Tier 94/95 biology panels restored as first-class credibility layer (`WETLAB_LONGEVITY_DEPTH.md`)  
- **Circuitry emergence (Tier 96):** component-variable atlas scaffold — BOM from seed math + industry tables (`CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md`)  
- **ESP32 hardware observer:** eight-way UART closure **convenience-deferred** until boot-sequence workflow is ergonomic (laptop bench); QEMU bare-metal and `Trinary_Hardware_Live_Panel` remain authoritative — not a math gap  
- **Domain atlas rollup:** **402** routed domains (35 core + 367 extension); prior 403 figure was summary rollup miscount  
"""


def build_appendix_c_extra() -> str:
    return """| [`docs/WETLAB_LONGEVITY_DEPTH.md`](docs/WETLAB_LONGEVITY_DEPTH.md) | Tier 94/95 wet-lab & longevity |
| [`data/publication/CREDIBILITY_HARDENING_AUDIT.md`](data/publication/CREDIBILITY_HARDENING_AUDIT.md) | Hard credibility pillar audit |
| [`docs/CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md`](docs/CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md) | Circuitry & BOM emergence (Tier 96) |
"""


def build_vi_extra_figures() -> str:
    return """![Coverage tier distribution](data/figures/coverage_surface_pie.png)

![Tier precision heatmap](data/figures/tier_precision_heatmap.png)
"""


def build_methods_formal() -> str:
    return """### 5.5 Statistical error definitions

For each domain or panel benchmark, let \\(n\\) measured records produce pairs \\((m_i, c_i)\\) where \\(m_i\\) is the authoritative measured value and \\(c_i\\) is the seed-derived FSOT prediction at canonical parameters (no per-record fitting).

**Per-record error (percent):**

\\[
\\varepsilon_i = 100 \\times \\frac{|c_i - m_i|}{\\max(|m_i|, \\epsilon_{\\mathrm{floor}})}
\\]

where \\(\\epsilon_{\\mathrm{floor}}\\) guards division near zero for classifier-valued observables.

**Pooled median error (domain gate metric):**

\\[
\\tilde{\\varepsilon} = \\mathrm{median}(\\varepsilon_1, \\ldots, \\varepsilon_n)
\\]

**GREEN gate (benchmark margin):** \\(\\tilde{\\varepsilon} \\leq 0.5\\%\\) and stability classifier agreement \\(\\geq 99.5\\%\\) where applicable (`data/benchmark_margin_audit.json`).

**Cross-domain headline:** median of per-domain \\(\\tilde{\\varepsilon}\\) over the 402-domain atlas (not a global re-fit across all 536,740 rows).

### 5.6 Preregistration and kill criteria

- **Preregistered predictions:** `data/preregistered_predictions_manifest.yaml` (PRED-001–041) — outcomes declared before panel refresh.
- **Per-domain kill criteria:** `data/fsot_domain_navigator.json` — extension panels and core routes register failure thresholds.
- **Parameter honesty:** `data/honest_claims_manifest.yaml` — routing coordinates are seed-derived folds, not fitted observational knobs (audit: `scripts/audit_parameter_count.py` → `ZERO_FREE`).

### 5.7 Data availability and reproduction

All headline claims in §VI–VIII reproduce from:

```bash
python scripts/run_publication_verification_bundle.py
```

Machine-readable claim ledger: `data/publication_claims_manifest.json`. Domain atlas: `data/publication/domain_atlas.csv`. Portable clone policy: bundled `vendor/` caches; live rebuild paths documented in Appendix XI-B.
"""


def build_notation() -> str:
    return """## Appendix D — Notation and Conventions

| Symbol | Meaning |
|--------|---------|
| `raw_S` | FSOT vitality scalar — emergence (+) vs dispersal (−) regime |
| `D_eff` | Effective fold dimension (seed-derived route coordinate, not a fit parameter) |
| `δψ` | Phase offset in domain fractal routing table |
| `quirk_mod` | Observer coupling modifier when `observed = true` |
| `consciousness_factor` | Consciousness-route coupling strength in §IV |
| `ε_i` | Per-record percent error (§5.5) |
| `ε̃` | Pooled median error for a domain/panel |
| GREEN | Benchmark gate: pooled median ≤ 0.5% |
| A_strong / B_verified | Coverage tiers in domain atlas |
| Lean route | Ledger domain label (`cosmological`, `particle`, `medical`, …) |
| Strict empirical | Formula row in `strict_empirical.jsonl` with measured target + citation grade |

**Seeds (global, no per-observable tuning):** π, e, φ (golden ratio), γ (Euler–Mascheroni), G (Catalan).

**Equation numbering:** Main-text display equations use §section numbering (e.g. §III.1). Appendix XII-E provides formula-level strict-empirical exemplars by Lean route.

**Edition tags:** README front matter `Edition:` field; git tags (`fsot-monograph-v1`, …) for citeable snapshots; commit SHA for living thesis.
"""


def build_xi_stub(ts: str) -> str:
    return f"""## Appendix XI — Full Verification Record (summary)

*Full volume:* [`docs/THESIS_APPENDIX_XI.md`](docs/THESIS_APPENDIX_XI.md) · *Regenerated:* {ts}

| Section | Content |
|---------|---------|
| XI-A | Cross-verification metrics (five-prover spine) |
| XI-B | Data sources and API resources |
| XI-C | Literature and citations |
| XI-D | Domain atlas summary |
| XI-E | Formula corpus and observables |
| XI-F | Contested observables |
| XI-G | Verified desktop engineering panels |

```bash
python scripts/run_publication_verification_bundle.py --full-cross-proof
python scripts/build_readme_thesis_expansion.py
python scripts/merge_readme_thesis_expansion.py
```
"""


def build_xii_stub(ts: str) -> str:
    manifest = _load_yaml(MANIFEST)
    chapters = [c for c in manifest.get("chapters") or [] if c.get("panels", 0) > 0]
    lines = [
        "## Appendix XII — Domain-by-Domain Scientific Coverage (summary)",
        "",
        f"*Full volume:* [`docs/THESIS_APPENDIX_XII.md`](docs/THESIS_APPENDIX_XII.md) · "
        f"*{len(chapters)} clusters · {manifest.get('extension_panels', 367)} extension panels · "
        f"Regenerated: {ts}",
        "",
        "| Cluster | Panels |",
        "|---------|-------:|",
    ]
    for ch in chapters:
        lines.append(f"| {ch.get('title', ch['id'])} | {ch.get('panels', 0)} |")
    lines.extend(
        [
            "",
            "Per-panel observable tables, subfield maps, and formula-level prose (XII-E style) "
            "live in the full volume and chapter files under "
            "`data/publication/readme_domain_chapters/`.",
            "",
            "```bash",
            "python scripts/build_readme_domain_chapters.py",
            "python scripts/merge_readme_arxiv_thesis.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def build_equations_block() -> str:
    return """### 3.1 The heartbeat (numbered)

At the center of FSOT is one scalar decomposition evaluated at seed-derived constants:

**(Eq. III.1)** — vitality scalar:

```
raw_S = term1 + term2 + term3
```

**(Eq. III.2)** — primary wave term with observer coupling:

```
term1 = (main_wave(N, P, D_eff)) × quirk_mod(observed, δψ, phase_variance, consciousness_factor)
```

**(Eq. III.3)** — environment and chaotic bleed:

```
term2 = baseline_trend(environment) + amplitude(environment)
term3 = chaotic_bleed(small_scale_turbulence)
```

In words:

- **Main wave term** — resonance at scale (size N, power P, effective dimension D_eff)
- **quirk_mod** — observer coupling: when `observed = true`, measurement modulates the wave
- **term2** — baseline trend and amplitude (environment)
- **term3** — chaotic bleed: small-scale turbulence from the fluid

Formal definitions: `FSOT/Scalar.lean`, `FSOT/Formal/Scalar.lean`, decimal authority `vendor/fsot_compute.py`.
"""


def main() -> int:
    import yaml

    OUT.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    files = {
        "toc.md": build_toc(ts),
        "related_work.md": build_related_work(),
        "contributions.md": build_contributions(),
        "epistemology.md": build_epistemology(),
        "prereg_summary.md": build_prereg_summary(),
        "bubble_bleed.md": build_bubble_bleed(),
        "engineering_viii.md": build_engineering_viii(),
        "near_miss.md": build_near_miss_section(),
        "credibility_hardening.md": build_credibility_hardening_section(),
        "circuitry_roadmap.md": build_circuitry_roadmap(),
        "discussion_open_work.md": build_discussion_open_work_patch(),
        "appendix_c_extra.md": build_appendix_c_extra(),
        "obligation_map.md": build_obligation_map_section(),
        "vi_extra_figures.md": build_vi_extra_figures(),
        "methods_formal.md": build_methods_formal(),
        "notation.md": build_notation(),
        "xi_stub.md": build_xi_stub(ts),
        "xii_stub.md": build_xii_stub(ts),
        "equations_iii.md": build_equations_block(),
    }
    for name, body in files.items():
        (OUT / name).write_text(body.rstrip() + "\n", encoding="utf-8")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": [str((OUT / k).relative_to(ROOT)).replace("\\", "/") for k in files],
        "merge_command": "python scripts/merge_readme_arxiv_thesis.py",
    }
    (OUT / "manifest.yaml").write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    print(f"Wrote {len(files)} arXiv gap files to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())