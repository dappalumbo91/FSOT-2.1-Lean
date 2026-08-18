#!/usr/bin/env python3
"""Public names-only tech index.

Does **not** scan I:\\fsot tech, founding PDF extracts, or any private
blueprint file. Titles and fold labels only. Specs stay unpublished.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "publication" / "tech_blueprints_registry.json"
OUT_MD = ROOT / "data" / "publication" / "TECH_BLUEPRINTS_REGISTRY.md"

# Public to-do index. No wattages, parts, paths, or extracts.
PUBLIC_INDEX: list[dict] = [
    {"id": "qveh", "title": "Quantum Vacuum Energy Harvester (QVEH)", "fold": "quantum vacuum / Casimir", "epistemic": "unpublished", "notes": "law_11 family"},
    {"id": "enerframe", "title": "Compact Integrated Quantum Vacuum EnerFrame", "fold": "quantum vacuum", "epistemic": "unpublished", "notes": "same fold"},
    {"id": "neo_benben", "title": "Neo-Benben Household Energy Unit", "fold": "vacuum / fuel-lab concept", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "ppfg", "title": "Palumbo Perpetual Flux Generator", "fold": "fuel-lab concept", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "dual_surface_barrier", "title": "Dual-Surface Quantum Fluid Barrier", "fold": "domain coupling / valve", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "fluidic_warp", "title": "Fluidic Warp Drive", "fold": "BH→WH valve (C2)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "warp_portal", "title": "Warp Portal", "fold": "BH→WH valve (C2)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "mini_10d_wrps", "title": "Mini 10D-WRPS-D", "fold": "BH→WH valve (C2)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "e10d_wd", "title": "Warp Drive (E10D-WD)", "fold": "BH→WH valve (C2)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "warp_disc", "title": "Warp disc (starate)", "fold": "BH→WH valve (C2)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "em_propulsion_ring", "title": "Electromagnetic Propulsion Ring", "fold": "propulsion fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "aetherion", "title": "Aetherion spacecraft", "fold": "propulsion / atmosphere", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "aetherion_colossus", "title": "Aetherion Colossus", "fold": "propulsion / atmosphere", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "gxt01", "title": "GXT-01", "fold": "observer / embodiment", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "gxt01_cryo", "title": "GXT-01 Cryogenic Cooling", "fold": "thermal / vacuum sink", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "standalone_emf", "title": "Standalone electromagnetic field generator", "fold": "magnetosphere analog", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "mini_oxoflash", "title": "Mini-Oxoflash", "fold": "atmosphere / ozone (law_26)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "oxoflash", "title": "The Oxoflash", "fold": "atmosphere / ozone (law_26)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "oxohive", "title": "OxoHive", "fold": "atmosphere / ozone (law_26)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "mars_terraform", "title": "Mars Terraforming Blueprint", "fold": "atmosphere / ozone (law_26)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "neutrfusion", "title": "NeutriFusion Reactor", "fold": "fusion panel family", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "sun_pocket", "title": "The Sun Pocket", "fold": "fusion panel family", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "spfr", "title": "Seawater Plasma Fusion Reactor (SPFR)", "fold": "fusion panel family", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "double_helix_plasma", "title": "Double Helix Plasma", "fold": "plasma fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "quantum_solar", "title": "The Quantum Solar Panel", "fold": "electrical-power fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "wood_poofcone", "title": "wood-PoofCone Thermo-Plasma Speaker", "fold": "acoustics / POOF–SUCTION (C9)", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "flexithread", "title": "FlexiThread", "fold": "materials fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "rubber_aluminum", "title": "Rubber-Aluminum Nanocomposite", "fold": "materials fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "vibranium", "title": "FSUFT-Vibranium Synthesizer", "fold": "materials fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "gigaflux_armor", "title": "GigaFlux Armor", "fold": "materials fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "memorphium", "title": "Memorphium", "fold": "materials fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "metaforge", "title": "MetaForge 3D Printer", "fold": "manufacturing fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "holoflex", "title": "Holoflex", "fold": "observer / display", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "tricorder", "title": "Quantum Fluid Tricorder", "fold": "observer / living-FSOT", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "qnr", "title": "Quantum noise reducer", "fold": "observer / noise as fluid", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "f8v", "title": "FSUFT 8.3 Verifier (F8V)", "fold": "observer / measurement", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "nanohlsd", "title": "NanoHLSD", "fold": "observer / embodiment", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "plant_growth", "title": "FSUFT-U Plant Growth Stimulator", "fold": "agroecology fold", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "the_blob", "title": "The Blob", "fold": "civic / metabolism analog", "epistemic": "unpublished", "notes": "unpublished"},
    {"id": "planetary_gear_board", "title": "Planetary Gear Board", "fold": "as-above-so-below (C12)", "epistemic": "unpublished", "notes": "unpublished"},
    {
        "id": "bh_wh_cycle",
        "title": "BlackHole WhiteHole Cycle",
        "fold": "already scored",
        "epistemic": "measured_concept",
        "notes": "BlackHole_WhiteHole_Cycle_Live_Panel — concept residual, not a gadget spec",
        "panel": "BlackHole_WhiteHole_Cycle_Live_Panel",
    },
    {
        "id": "philosophers_stone",
        "title": "Decoding the Philosopher's Stone (6.0)",
        "fold": "interpretive philosophy",
        "epistemic": "interpretive",
        "notes": "not a device",
    },
]


def build_md(rows: list[dict]) -> str:
    lines = [
        "# FSOT tech index (names only)",
        "",
        "**Status:** unpublished working list. These are **titles of private designs**. "
        "Specs, wattages, parts lists, and build files are **not** in this repo. "
        "Each item will get its own simulation repo later. Until then this is a *to-do index*, not a product catalog.",
        "",
        "**How to read a row:** the name is public; the *fold* is the FSOT 2.1 interface that design will score against when a simulation exists. "
        "Epistemic is `unpublished` unless a *separate* residual panel already exists for the *concept* (not the gadget).",
        "",
        "| Name | Fold (later score) | Notes |",
        "|------|--------------------|-------|",
    ]
    for r in rows:
        lines.append(f"| {r['title']} | {r['fold']} | {r['notes']} |")
    lines.extend(
        [
            "",
            "Machine copy: [`tech_blueprints_registry.json`](tech_blueprints_registry.json).",
            "",
            "Regenerate names (does **not** ingest private files into public docs):",
            "",
            "```powershell",
            "python scripts/build_tech_blueprints_registry.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    rows = [dict(r) for r in PUBLIC_INDEX]
    doc = {
        "generated_at": ts,
        "policy": "names_only_unpublished_index",
        "scans_private_tech_folder": False,
        "blueprint_count": len(rows),
        "unpublished_count": sum(1 for r in rows if r["epistemic"] == "unpublished"),
        "scored_concept_count": sum(1 for r in rows if r["epistemic"] == "measured_concept"),
        "interpretive_count": sum(1 for r in rows if r["epistemic"] == "interpretive"),
        "blueprints": rows,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    import json

    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    OUT_MD.write_text(build_md(rows), encoding="utf-8")
    print(f"Wrote {OUT_JSON}  {len(rows)} names (no private paths)")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
