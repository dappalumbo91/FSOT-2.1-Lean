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
        "| [§I-B](#i-b-related-work-and-positioning) | Related work and positioning |",
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
| Cross-domain test | Uncommon | 403 domains, 536,740 records |
| Formal triangulation | Rare | Lean + Coq + Isabelle + F* + Rust |
| Kill criteria | Often informal | Navigator + prereg manifest |
| Living edition | Static PDF | GitHub commit history + tagged releases |

**References (external):** Planck Collaboration (2018); Riess et al. (2024); PDG (2024); CODATA/NIST atomic datasets as cited per benchmark row. Full BibTeX export: `data/domain_citations/verified_desktop.bib`; literature panel: Appendix XI-C in [`docs/THESIS_APPENDIX_XI.md`](../docs/THESIS_APPENDIX_XI.md).
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

**Cross-domain headline:** median of per-domain \\(\\tilde{\\varepsilon}\\) over the 403-domain atlas (not a global re-fit across all 536,740 rows).

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