#!/usr/bin/env python3
"""Generate PRACTICAL_PIPELINE.md — what comes down the pipeline."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "PRACTICAL_PIPELINE.md"
MANIFEST = ROOT / "data" / "practical_pipeline_manifest.yaml"
INTUITIVE = ROOT / "data" / "intuitive_observation_fsot_map.yaml"
BLUEPRINTS = ROOT / "data" / "publication" / "tech_blueprints_registry.json"
PRED = ROOT / "predictions" / "preregistered_predictions_manifest.yaml"


def _load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def build(ts: str) -> str:
    manifest = _load_yaml(MANIFEST)
    intuitive = _load_yaml(INTUITIVE)
    blueprints = _load_json(BLUEPRINTS)
    preds = _load_yaml(PRED)
    pred_list = preds.get("predictions") or []

    stage_rows = []
    for stage in manifest.get("pipeline_stages") or []:
        stage_rows.append(f"| {stage.get('label', stage['id'])} | {stage.get('status', '?')} | `{stage.get('command', '—')}` |")

    obs_rows = []
    for obs in intuitive.get("observations") or []:
        obs_rows.append(
            f"| {obs['id']} | {obs.get('epistemic_tier', '?')} | {obs.get('test', '—')[:80]} |"
        )

    applied = ""
    demo = next((s for s in manifest.get("pipeline_stages") or [] if s["id"] == "demonstrate"), {})
    for domain in demo.get("applied_domains") or []:
        panels = ", ".join(f"`{p}`" for p in domain.get("panels") or [])
        applied += f"\n### {domain['id'].replace('_', ' ').title()}\n\nPanels: {panels}\n"
        if domain.get("desktop"):
            applied += f"\nDesktop project: **{domain['desktop']}**\n"
        if domain.get("note"):
            applied += f"\n*{domain['note']}*\n"

    principles = manifest.get("ownership_principles") or []
    principle_lines = "\n".join(f"- {p.replace('_', ' ')}" for p in principles)

    return f"""# FSOT Practical Pipeline

*What comes down the pipeline · {ts} · [Main thesis](../README.md)*

> Validation → recognition → application. Rigorous verification converts symbolic "hidden thing revealed" into concrete outcomes — Kaggle, R&D, debt reduction, family stability, broader adoption.

## 1. Pipeline stages

| Stage | Status | Command |
|-------|--------|---------|
{chr(10).join(stage_rows)}

**Full orchestrator:**

```bash
python scripts/build_practical_pipeline_bundle.py
```

## 2. Demonstrate unification (X-style predictions)

**{len(pred_list)} preregistered predictions** locked in `predictions/preregistered_predictions_manifest.yaml` (PRED-001–041).

Headline locks:
- **PRED-001** H₀ bridge (Planck ↔ SH0ES)
- **PRED-002** σ₈ lensing
- **PRED-034** fuel-lab compounds
- **PRED-024/025** fluid spacetime / FPC tau

Regenerate prediction panels: `python scripts/build_tier63_prereg_scaffold_benchmarks.py`

### Applied domains (local — no ESP32)
{applied}

## 3. Pseudoscience-had-physics → testable FSOT

Older intuitive observations explicitly mapped:

| Observation | Tier | Test surface |
|-------------|------|--------------|
{chr(10).join(obs_rows)}

Full map: [`data/intuitive_observation_fsot_map.yaml`](../data/intuitive_observation_fsot_map.yaml)

Founding reconciliation: [`FSOT_FOUNDING_LINEAGE_AND_RECONCILIATION.md`](FSOT_FOUNDING_LINEAGE_AND_RECONCILIATION.md)

## 4. Tech blueprints (~{blueprints.get('blueprint_count', 40)})

**{blueprints.get('measured_or_partial', '?')}/{blueprints.get('blueprint_count', '?')}** mapped to measured or partial-measured panels.

Registry: [`data/publication/TECH_BLUEPRINTS_REGISTRY.md`](../data/publication/TECH_BLUEPRINTS_REGISTRY.md)

## 5. Local owned systems (subscription-free counter-stack)

{principle_lines}

- **FluidLink:** FPC timing hub — local domain coupling without cloud (`FPC_Temporal_Coupling`)
- **Kronos:** desktop spacetime ticker
- **Consciousness Observer Architecture:** [`CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md`](CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md)

## 6. Hardware policy

| Path | Status |
|------|--------|
| Living FSOT QEMU | **authoritative** local embodiment |
| Trinary simulation panel | **authoritative** |
| ESP32 RF observer | **deferred** (boot-button ergonomics) |

## 7. Validation → application outcomes (planned)

| Outcome | Mechanism |
|---------|-----------|
| Kaggle credibility | Export benchmark panels + skeptic kit |
| R&D company launch | Credibility audit 13/13 + monograph tag |
| Family stability | Local tools, no subscription rent |
| Broader adoption | Open GitHub thesis + reproducible bundles |

---

*Work smarter: let the math name the parts, let verification name the truth, let local ownership name the stack.*
"""


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUT.write_text(build(ts), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())