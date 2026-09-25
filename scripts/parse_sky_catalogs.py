#!/usr/bin/env python3
"""Turn the game-drive VizieR dumps into position JSON. No network."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\FSOT_Benchmarks\anomaly_observables")


def tsv_rows(path: Path) -> list[dict[str, str]]:
    lines = [
        ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if ln and not ln.startswith("#")
    ]
    header = [c.strip() for c in lines[0].split("\t")]
    rows = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.split("\t")]
        if not cells or cells[0] in {"", "deg"} or set("".join(cells)) <= {"-"}:
            continue
        if cells[0] == header[0]:
            continue
        rows.append(dict(zip(header, cells, strict=False)))
    return rows


def fnum(text: str) -> float | None:
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    chime_rows = tsv_rows(ROOT / "frb" / "chime_frb_catalog1_vizier.tsv")
    seen: dict[str, dict] = {}
    for row in chime_rows:
        name = row.get("Name") or ""
        ra = fnum(row.get("RAJ2000") or "")
        dec = fnum(row.get("DEJ2000") or "")
        if not name or ra is None or dec is None or name in seen:
            continue
        seen[name] = {
            "name": name,
            "ra_deg": ra,
            "dec_deg": dec,
            "repeater_name": row.get("RpName") or "",
            "dm_pc": fnum(row.get("DM") or ""),
            "dm_excess_ne2001": fnum(row.get("DMeNE2001") or ""),
        }
    frb_doc = {
        "fetched_at": now,
        "citation": "CHIME/FRB Collaboration 2021 ApJS 257 59; VizieR J/ApJS/257/59/table2",
        "n_with_position": len(seen),
        "frbs": list(seen.values()),
    }
    (ROOT / "frb" / "chime_frb_catalog1_positions.json").write_text(
        json.dumps(frb_doc), encoding="utf-8"
    )

    abell_path = ROOT / "extragalactic_structure" / "abell_vii4a_j2000.tsv"
    abell_rows = tsv_rows(abell_path)
    objects = []
    for row in abell_rows:
        ra = fnum(row.get("_RAJ2000") or row.get("RAJ2000") or "")
        dec = fnum(row.get("_DEJ2000") or row.get("DEJ2000") or "")
        name = row.get("Abell") or row.get("ACO") or ""
        if ra is None or dec is None or not name:
            continue
        objects.append(
            {
                "name": f"Abell_{name}",
                "ra_deg": ra,
                "dec_deg": dec,
                "richness": row.get("RichGroup") or "",
                "kind": "abell_cluster",
            }
        )
    abell_doc = {
        "fetched_at": now,
        "citation": "Abell 1958, Corwin 1974; VizieR VII/4A/abell, J2000",
        "n": len(objects),
        "objects": objects,
    }
    (ROOT / "extragalactic_structure" / "abell_clusters.json").write_text(
        json.dumps(abell_doc), encoding="utf-8"
    )
    print(f"chime_unique={len(seen)} abell={len(objects)}")
    if not seen or not objects:
        print("abell headers", list(abell_rows[0]) if abell_rows else None)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
