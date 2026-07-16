# FSOT Wet-Lab & Longevity Depth

*Supplementary science volume · 2026-07-16 · [Return to main thesis](../README.md#viii-engineering-demonstrations)*

> **Scope:** Cross-species longevity genetics (Tier 94), zebrafish developmental wet-lab coupling (Tier 95), and AnAge/NCBI public anchors — seed-derived predictions against measured biology, not post-hoc curve fits.

## 1. Why this volume exists

Before repository presentation refinement, FSOT longevity depth was a primary research spine. This volume restores that work as a **first-class credibility layer**: biology measured in the wild (HAGR AnAge, NCBI taxonomy, CZ Biohub zebrafish developmental tracks) compared to the same scalar engine that closes cosmology and particle panels.

## 2. Tier 94 — Longevity genetics (AnAge + NCBI)

| Panel | Records | Pooled median | Benchmark |
|-------|--------:|--------------:|-----------|
| `Longevity_AnAge_Catalog_Panel` | 966 | 0.022236% | `data/longevity_anage_catalog_panel_benchmark.json` |
| `Longevity_Genetic_Mechanics_Panel` | 35 | 0.022236% | `data/longevity_genetic_mechanics_panel_benchmark.json` |
| `Longevity_Extreme_Species_Panel` | 164 | 0.017789% | `data/longevity_extreme_species_panel_benchmark.json` |
| `Longevity_MegaDeep_NCBI_Panel` | 1,746 | 0.017789% | `data/longevity_megadeep_ncbi_panel_benchmark.json` |
| `Longevity_Telomere_Repair_Panel` | 60 | 0.022236% | `data/longevity_telomere_repair_panel_benchmark.json` |
| `Longevity_Consciousness_Coupling_Panel` | 890 | 0.022424% | `data/longevity_consciousness_coupling_panel_benchmark.json` |
| `Zebrafish_Longevity_Genetics_Coupling_Panel` | 15 | 0.013342% | `data/zebrafish_longevity_genetics_coupling_panel_benchmark.json` |
| `Zebrafish_Developmental_Mechanics_Panel` | 31 | 0.017789% | `data/zebrafish_developmental_mechanics_panel_benchmark.json` |
| `Zebrafish_Cell_Tracking_Panel` | 20 | 0.022236% | `data/zebrafish_cell_tracking_panel_benchmark.json` |

**Total longevity/wet-lab records (above panels):** 3,927

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
