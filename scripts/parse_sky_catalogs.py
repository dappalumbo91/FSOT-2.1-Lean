#!/usr/bin/env python3
"""Turn the game-drive catalog dumps into position JSON. No network."""
from __future__ import annotations

import csv
import json
import math
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
        value = float(text)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):
        return None
    return value


def flag_num(text: str) -> int:
    try:
        return int(float(text))
    except (TypeError, ValueError):
        return 0


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
    cat2 = parse_chime_catalog2(now)
    print(
        f"chime_unique={len(seen)} abell={len(objects)} "
        f"cat2_sky={cat2['n_with_position']} cat2_rows={cat2['n_csv_rows']} "
        f"cat2_sources={cat2['n_source_keys']} cat2_sidelobe_rows={cat2['n_sidelobe_rows']}"
    )
    if not seen or not objects or not cat2["n_with_position"]:
        print("abell headers", list(abell_rows[0]) if abell_rows else None)
        return 1
    return 0


def parse_chime_catalog2(now: str) -> dict:
    """One sky position per Catalog 2 source.

    A repeater_name groups that source's bursts. Otherwise the source is the
    TNS name. Sub-bursts share a burst. The lowest sub_num row with a finite
    non-sidelobe position supplies the coordinate. Sidelobe rows in this file
    have no RA or Dec and are not stored as (0, 0).
    """
    path = ROOT / "frb" / "chimefrbcat2.csv"
    by_source: dict[str, dict] = {}
    n_rows = 0
    n_missing = 0
    n_sidelobe_rows = 0
    source_keys: set[str] = set()
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            n_rows += 1
            tns = (row.get("tns_name") or "").replace(" ", "")
            repeater = (row.get("repeater_name") or "").strip()
            source = repeater or tns
            if source:
                source_keys.add(source)
            if flag_num(row.get("sidelobe_flag") or ""):
                n_sidelobe_rows += 1
            ra = fnum(row.get("ra") or "")
            dec = fnum(row.get("dec") or "")
            if not source or ra is None or dec is None:
                n_missing += 1
                continue
            if flag_num(row.get("sidelobe_flag") or ""):
                continue
            sub = flag_num(row.get("sub_num") or "")
            item = {
                "name": source,
                "ra_deg": ra,
                "dec_deg": dec,
                "repeater_name": repeater,
                "burst_name": tns,
                "dm_pc": fnum(row.get("dm_fitb") or ""),
                "dm_excess_ne2001": fnum(row.get("dm_exc_ne2001") or ""),
                "excluded_flag": flag_num(row.get("excluded_flag") or ""),
                "sub_num": sub,
            }
            prior = by_source.get(source)
            if prior is None or (sub, tns) < (int(prior["sub_num"]), prior["burst_name"]):
                by_source[source] = item
    frbs = []
    for item in by_source.values():
        kept = dict(item)
        kept.pop("sub_num", None)
        frbs.append(kept)
    doc = {
        "fetched_at": now,
        "citation": (
            "CHIME/FRB Collaboration 2026, ApJS 283 34, arXiv:2601.09399; "
            "CISTI.CANFAR/25.0066 table/chimefrbcat2.csv"
        ),
        "n_csv_rows": n_rows,
        "n_source_keys": len(source_keys),
        "n_rows_missing_position": n_missing,
        "n_sidelobe_rows": n_sidelobe_rows,
        "n_with_position": len(frbs),
        "position_rule": (
            "One row per source. repeater_name groups bursts of that source; "
            "otherwise the source is tns_name. Lowest sub_num with finite RA and Dec. "
            "sidelobe rows have no coordinates and are omitted. "
            "Missing coordinates are not stored as (0, 0)."
        ),
        "frbs": frbs,
    }
    (ROOT / "frb" / "chime_frb_catalog2_positions.json").write_text(
        json.dumps(doc), encoding="utf-8"
    )
    return doc


if __name__ == "__main__":
    raise SystemExit(main())
