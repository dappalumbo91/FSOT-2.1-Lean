#!/usr/bin/env python3
"""Generate wet-lab & longevity depth supplementary thesis volume."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "WETLAB_LONGEVITY_DEPTH.md"
TIER94 = ROOT / "data" / "tier94_longevity_genetics_manifest.yaml"
TIER95 = ROOT / "data" / "tier95_zebrahub_development_manifest.yaml"

PANELS = (
    "longevity_anage_catalog_panel_benchmark.json",
    "longevity_genetic_mechanics_panel_benchmark.json",
    "longevity_extreme_species_panel_benchmark.json",
    "longevity_megadeep_ncbi_panel_benchmark.json",
    "longevity_telomere_repair_panel_benchmark.json",
    "longevity_consciousness_coupling_panel_benchmark.json",
    "zebrafish_longevity_genetics_coupling_panel_benchmark.json",
    "zebrafish_developmental_mechanics_panel_benchmark.json",
    "zebrafish_cell_tracking_panel_benchmark.json",
)


def _bench_row(fname: str) -> dict:
    path = ROOT / "data" / fname
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build(ts: str) -> str:
    rows = []
    total_records = 0
    for fname in PANELS:
        doc = _bench_row(fname)
        if not doc:
            continue
        rc = int(doc.get("record_count") or 0)
        total_records += rc
        rows.append(
            f"| `{doc.get('domain', fname)}` | {rc:,} | {doc.get('pooled_median_error_pct', '?')}% | "
            f"`data/{fname}` |"
        )

    return f"""# FSOT Wet-Lab & Longevity Depth

*Supplementary science volume · {ts} · [Return to main thesis](../README.md#viii-engineering-demonstrations)*

> **Scope:** Cross-species longevity genetics (Tier 94), zebrafish developmental wet-lab coupling (Tier 95), and AnAge/NCBI public anchors — seed-derived predictions against measured biology, not post-hoc curve fits.

## 1. Why this volume exists

Before repository presentation refinement, FSOT longevity depth was a primary research spine. This volume restores that work as a **first-class credibility layer**: biology measured in the wild (HAGR AnAge, NCBI taxonomy, CZ Biohub zebrafish developmental tracks) compared to the same scalar engine that closes cosmology and particle panels.

## 2. Tier 94 — Longevity genetics (AnAge + NCBI)

| Panel | Records | Pooled median | Benchmark |
|-------|--------:|--------------:|-----------|
{chr(10).join(rows) if rows else '| — | run build bundle | — | — |'}

**Total longevity/wet-lab records (above panels):** {total_records:,}

**Manifest:** `data/tier94_longevity_genetics_manifest.yaml`

**Sources:** AnAge HAGR catalog (maximum longevity, IMR, MRDT, metabolic rate); NCBI Entrez for extreme long-lived species; telomere/repair literature anchors; consciousness–longevity coupling.

## 3. Tier 95 — Zebrafish developmental wet-lab (Danio rerio)

| Panel | Role |
|-------|------|
| `Zebrafish_Cell_Tracking_Panel` | 3D+time cell tracking from public Zebrahub releases |
| `Zebrafish_Developmental_Mechanics_Panel` | Developmental mechanics vs seed-scalar readouts |
| `Zebrafish_Longevity_Genetics_Coupling_Panel` | Bridges Tier 94 longevity ↔ Tier 95 development |

**Manifest:** `data/tier95_zebrahub_development_manifest.yaml`

**Crosswalk report:** `data/tier95_genetics_system_crosswalk_report.json`

## 4. Reproduction

```bash
python scripts/build_wetlab_longevity_expansion_bundle.py
python scripts/verify_tier95_genetics_system.py
python scripts/run_tier95_biological_validation.py
```

Deep ingest (optional, uses bundled caches when offline):

```bash
python scripts/ingest_tier94_longevity_genetics.py --deep
python scripts/ingest_tier95_zebrahub_development.py --deep
```

## 5. Credibility coupling

Longevity panels feed the hard credibility audit (`data/publication/CREDIBILITY_HARDENING_AUDIT.md`) — biology is not a silo; it is part of the cross-domain spine that includes Raichle brain-power (`E_con`) and species-scale AnAge catalogs.

## 6. Relation to circuitry expansion

Longevity genetics establishes the **measured-biology** pattern FSOT will reuse for circuitry emergence: label every variable, map to industry component classes, let seed arithmetic select BOM lines — see [`CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md`](CIRCUITRY_COMPONENT_EMERGENCE_SPINE.md).
"""


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUT.write_text(build(ts), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())