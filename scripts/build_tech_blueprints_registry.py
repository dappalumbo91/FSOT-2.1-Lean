#!/usr/bin/env python3
"""Catalog ~40 fsot tech blueprints → FSOT 2.1 panel crosswalk."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_MANIFEST = ROOT / "vendor" / "founding_corpus" / "pdf_ingest_manifest.json"
OUT_JSON = ROOT / "data" / "publication" / "tech_blueprints_registry.json"
OUT_MD = ROOT / "data" / "publication" / "TECH_BLUEPRINTS_REGISTRY.md"

# Keyword → FSOT verified panel / tier mapping
PANEL_MAP = (
    (r"warp|portal|wrps|fwd", "Warp_BH_WH_Portal", "tier39/warp_bh_wh", "interpretive"),
    (r"fusion|spfr|plasma reactor|oxoflash", "Fusion_Physics_Public_Panel", "tier71_fusion", "measured_partial"),
    (r"fuel|generator|energy unit|benben|ppfg|perpetual flux", "Fuel_Lab_Live_Panel", "tier39/fuel", "measured"),
    (r"solar|photovoltaic|quantum solar", "Electrical_Power_Systems", "tier39_electrical", "measured"),
    (r"tricorder|sensing|observer|fluid.*sensor", "Living_FSOT_Hardware_Panel", "living_fsot_qemu", "scaffold"),
    (r"armor|nanocomposite|vibranium|material", "Materials_Science_gap_fill", "tier55_materials", "scaffold"),
    (r"plant growth|agriculture", "Agriculture_Agroecology_gap_fill", "tier_gap_fill", "scaffold"),
    (r"warp drive|fluidic warp", "BlackHole_WhiteHole_Cycle_Live_Panel", "verified_desktop", "measured"),
    (r"barrier|shield|fluid barrier", "Domain_Coupling_Simulation", "domain_coupling", "measured"),
    (r"thread|flexi|comm|link", "FPC_Temporal_Coupling", "tier50_fluidlink", "measured"),
    (r"speaker|acoustic|poof", "Acoustics_gap_fill", "tier_gap_fill", "scaffold"),
    (r"philosopher|stone|decoding", "Philosophy_Corpus", "founding_interpretive", "interpretive"),
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _classify(name: str) -> tuple[str, str, str]:
    lower = name.lower()
    for pattern, panel, tier, tier_epistemic in PANEL_MAP:
        if re.search(pattern, lower):
            return panel, tier, tier_epistemic
    return "Extension_Panel_TBD", "blueprint_audit_pending", "interpretive"


def _scan_fsot_tech_dir() -> list[Path]:
    roots = [Path(r"I:/fsot tech"), Path(r"I:\fsot tech")]
    files: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() in {".pdf", ".md"} and path.is_file():
                if "fsot_updated_blueprints" in str(path):
                    continue
                files.append(path)
        break
    return files


def _unique_blueprints(manifest: dict) -> list[dict]:
    seen: set[str] = set()
    rows: list[dict] = []
    for entry in manifest.get("entries") or []:
        src = str(entry.get("source_pdf") or "")
        if "fsot tech" not in src.lower():
            continue
        if "fsot_updated_blueprints" in src:
            continue  # prefer canonical names from parent PDFs
        name = Path(src).stem
        key = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        if key in seen:
            continue
        seen.add(key)
        panel, tier, epistemic = _classify(name)
        rows.append(
            {
                "id": key,
                "title": name,
                "source_pdf": src,
                "extracted_txt": entry.get("output_txt"),
                "char_count": entry.get("char_count"),
                "fsot_panel": panel,
                "verification_tier": tier,
                "epistemic_tier": epistemic,
                "reverify_command": "python scripts/fsot_verification_runner.py",
            }
        )
    for path in _scan_fsot_tech_dir():
        name = path.stem
        key = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        if key in seen:
            continue
        seen.add(key)
        panel, tier, epistemic = _classify(name)
        rows.append(
            {
                "id": key,
                "title": name,
                "source_pdf": str(path),
                "extracted_txt": None,
                "char_count": path.stat().st_size if path.is_file() else None,
                "fsot_panel": panel,
                "verification_tier": tier,
                "epistemic_tier": epistemic,
                "reverify_command": "python scripts/fsot_verification_runner.py",
            }
        )
    # Add known .md blueprints from founding registry
    extras = [
        ("palumbo_perpetual_flux_generator", "Palumbo Perpetual Flux Generator", "Fuel_Lab_Live_Panel"),
        ("planetary_gear_board", "Planetary Gear Board", "Robotics_Control_Systems"),
        ("bh_wh_cycle", "BlackHole WhiteHole Cycle Blueprint", "BlackHole_WhiteHole_Cycle_Live_Panel"),
    ]
    for eid, title, panel in extras:
        if eid not in seen:
            seen.add(eid)
            rows.append(
                {
                    "id": eid,
                    "title": title,
                    "source_pdf": f"I:/fsot tech/{title.replace(' ', '_')}.md",
                    "extracted_txt": None,
                    "char_count": None,
                    "fsot_panel": panel,
                    "verification_tier": "verified_desktop",
                    "epistemic_tier": "measured" if "Cycle" in title else "interpretive",
                    "reverify_command": "python scripts/reproduce_domain_panel.py",
                }
            )
    return sorted(rows, key=lambda r: r["title"].lower())


def build_md(rows: list[dict], ts: str) -> str:
    measured = sum(1 for r in rows if r["epistemic_tier"] in ("measured", "measured_partial"))
    lines = [
        "# FSOT Tech Blueprints Registry",
        "",
        f"*Generated: {ts} · {len(rows)} blueprints cataloged*",
        "",
        "> Engineering vision documents from `I:/fsot tech`. **Philosophy retained; numerics verified before citing as measured.**",
        "",
        f"**Summary:** {measured}/{len(rows)} mapped to measured or partial-measured FSOT panels.",
        "",
        "| Blueprint | FSOT panel | Tier | Epistemic |",
        "|-----------|------------|------|-----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['title'][:60]} | `{r['fsot_panel']}` | {r['verification_tier']} | {r['epistemic_tier']} |"
        )
    lines.extend(
        [
            "",
            "## Re-verify a blueprint claim",
            "",
            "```bash",
            "python scripts/build_tech_blueprints_registry.py",
            "# Per founding workflow:",
            "python scripts/reconcile_founding_corpus.py",
            "```",
            "",
            "See [`FSOT_FOUNDING_LINEAGE_AND_RECONCILIATION.md`](../FSOT_FOUNDING_LINEAGE_AND_RECONCILIATION.md).",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    manifest = _load_json(PDF_MANIFEST)
    rows = _unique_blueprints(manifest)
    ts = datetime.now(timezone.utc).isoformat()
    doc = {
        "generated_at": ts,
        "blueprint_count": len(rows),
        "measured_or_partial": sum(1 for r in rows if r["epistemic_tier"] in ("measured", "measured_partial")),
        "blueprints": rows,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    OUT_MD.write_text(build_md(rows, ts[:10]), encoding="utf-8")
    print(f"Wrote {OUT_JSON}  {len(rows)} blueprints")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())