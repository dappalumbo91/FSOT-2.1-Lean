#!/usr/bin/env python3
"""Phase 0 — circuit component emergence atlas scaffold (Tier 96 design)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "circuit_component_emergence_manifest.yaml"
OUT_DOC = ROOT / "docs" / "CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md"
OUT_JSON = ROOT / "data" / "publication" / "circuit_component_atlas_scaffold.json"

PANEL_BENCH = {
    "Electrical_Power_Systems": ROOT / "data" / "electrical_power_systems_benchmark.json",
    "Desktop_Application_Wiring_Spine": ROOT / "data" / "desktop_application_wiring_spine_benchmark.json",
    "Trinary_Hardware_Live_Panel": ROOT / "data" / "trinary_hardware_live_panel_benchmark.json",
    "Robotics_Control_Systems": ROOT / "data" / "robotics_control_systems_benchmark.json",
}


def _load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _bench_summary(path: Path) -> dict:
    if not path.is_file():
        return {}
    doc = json.loads(path.read_text(encoding="utf-8"))
    return {
        "domain": doc.get("domain", path.stem),
        "record_count": doc.get("record_count"),
        "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
    }


def build_doc(manifest: dict, panels: list[dict], ts: str) -> str:
    classes = manifest.get("component_classes") or []
    class_rows = []
    for c in classes:
        vars_ = ", ".join(f"`{v}`" for v in (c.get("variables") or []))
        des = ", ".join(c.get("designators") or [])
        refs = ", ".join(c.get("industry_refs") or []) or "—"
        class_rows.append(f"| {c.get('class', '?')} | {des} | {vars_} | {refs} |")

    panel_rows = []
    for p in panels:
        med = p.get("pooled_median_error_pct")
        med_s = f"{med:.3f}" if isinstance(med, (int, float)) else "?"
        panel_rows.append(
            f"| `{p.get('domain')}` | {p.get('record_count', '?')} | {med_s}% | verified panel |"
        )

    planned = manifest.get("planned_domains") or []
    planned_lines = "\n".join(f"- `{d}`" for d in planned)

    return f"""# FSOT Circuitry & Component Emergence Spine

*Tier 96 design scaffold · {ts} · [Return to main thesis](../README.md#97-circuitry-component-emergence-roadmap)*

> **Goal:** Label every schematic variable and industry component class so seed-derived FSOT readouts **emerge a bill of materials** from parametric availability — work smarter, not harder. No guessed resistor values; arithmetic + catalog tables.

## 1. Why this domain

FSOT already closes electrical and wiring panels at sub-percent precision. The next step is **intrinsic emergence**: when the math demands a build, the repository names the parts.

| Existing verified panel | Records | Pooled median |
|-------------------------|--------:|--------------:|
{chr(10).join(panel_rows) if panel_rows else "| — | — | — | — |"}

**Manifest:** `data/circuit_component_emergence_manifest.yaml`

## 2. Component variable atlas (Phase 0)

Every designator class maps to measurable variables and industry parametric search keys:

| Class | Designators | FSOT variables | Industry refs |
|-------|-------------|----------------|---------------|
{chr(10).join(class_rows) if class_rows else "| — | — | — | — |"}

## 3. Seed routing (no per-part tuning)

| Field | Value |
|-------|-------|
| Lean route | `{manifest.get('fsot_routing', {}).get('lean_route', 'material')}` |
| Formula branches | `{", ".join(manifest.get("fsot_routing", {}).get("formula_branches") or [])}` |
| Seed-only policy | `{manifest.get("fsot_routing", {}).get("seed_only", True)}` |

Routing coordinates (`D_eff`, `δψ`, `quirk_mod`) select component **classes** and tolerance bands; numeric values emerge from strict-empirical rows, not hand-entered BOM guesses.

## 4. Planned panels (not yet benchmarked)

{planned_lines or "- —"}

## 5. Emergence pipeline (target)

```
schematic netlist → variable labels → FSOT scalar @ seed folds
    → industry parametric filter (Digi-Key/Mouser class tables)
    → ranked BOM lines + tolerance proof
```

**Next scripts (Phase 1):**

```bash
python scripts/ingest_circuit_component_catalogs.py      # planned
python scripts/build_circuit_component_emergence_benchmarks.py
python scripts/gen_circuit_component_emergence_lean.py
```

## 6. Relation to wet-lab longevity

Tier 94/95 longevity panels established the **measured-biology → seed prediction** pattern. Tier 96 reuses that pattern for **measured-electrical** targets (NIST CODATA, IEEE grid specs, datasheet anchors).

See [`WETLAB_LONGEVITY_DEPTH.md`](WETLAB_LONGEVITY_DEPTH.md) and [`CREDIBILITY_HARDENING_AUDIT.md`](../data/publication/CREDIBILITY_HARDENING_AUDIT.md).

## 7. ESP32 / trinary hardware (deferred)

Physical ESP32 eight-way closure remains **convenience-deferred** (boot-sequence ergonomics). QEMU bare-metal and `Trinary_Hardware_Live_Panel` simulation benchmarks remain authoritative until laptop-bench workflow is ready.
"""


def main() -> int:
    manifest = _load_yaml(MANIFEST)
    panels = [_bench_summary(p) for p in PANEL_BENCH.values()]
    panels = [p for p in panels if p]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": manifest.get("tier", 96),
        "status": manifest.get("status", "design_scaffold"),
        "component_classes": len(manifest.get("component_classes") or []),
        "existing_panels": panels,
        "planned_domains": manifest.get("planned_domains") or [],
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    OUT_DOC.write_text(build_doc(manifest, panels, ts), encoding="utf-8")
    print(f"Wrote {OUT_DOC}")
    print(f"Wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())