#!/usr/bin/env python3
"""Download public sky catalogs onto the game drive.

CHIME/FRB Catalog 1 (Amiri et al. 2021, J/ApJS/257/59) has RA and Dec.
Pantheon+SH0ES is the Hubble-flow supernova table.
Abell clusters (VII/4) are the extragalactic structure catalog.

Does not rewrite frozen prediction JSON.
"""
from __future__ import annotations

import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\FSOT_Benchmarks\anomaly_observables")
FRB_DIR = ROOT / "frb"
SN_DIR = ROOT / "pantheon_plus"
CL_DIR = ROOT / "extragalactic_structure"

CHIME_URL = (
    "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"
    "?-source=J/ApJS/257/59/table2"
    "&-out=Name,RAJ2000,DEJ2000,RpName,DM,DMeNE2001"
    "&-out.max=99999"
)
ABELL_URL = (
    "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"
    "?-source=VII/4A/catalog"
    "&-out=ACO,RAJ2000,DEJ2000,Rich"
    "&-out.max=9999"
)
PANTHEON_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
    "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat"
)


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-sky-catalog/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read()


def _tsv_rows(text: str) -> list[dict[str, str]]:
    lines = [ln for ln in text.splitlines() if ln and not ln.startswith("#")]
    if not lines:
        return []
    header = [c.strip() for c in lines[0].split("\t")]
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.split("\t")]
        if not cells or cells[0] in {"", "deg"} or set("".join(cells)) <= {"-"}:
            continue
        if cells[0] == header[0]:
            continue
        rows.append(dict(zip(header, cells, strict=False)))
    return rows


def _f(text: str) -> float | None:
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def fetch_chime() -> int:
    FRB_DIR.mkdir(parents=True, exist_ok=True)
    raw = _get(CHIME_URL)
    (FRB_DIR / "chime_frb_catalog1_vizier.tsv").write_bytes(raw)
    rows = _tsv_rows(raw.decode("utf-8", errors="replace"))
    # One sky position per TNS name. Sub-bursts repeat the same coordinates.
    seen: dict[str, dict] = {}
    for row in rows:
        name = row.get("Name") or ""
        ra = _f(row.get("RAJ2000") or "")
        dec = _f(row.get("DEJ2000") or "")
        if not name or ra is None or dec is None or name in seen:
            continue
        seen[name] = {
            "name": name,
            "ra_deg": ra,
            "dec_deg": dec,
            "repeater_name": row.get("RpName") or "",
            "dm_pc": _f(row.get("DM") or ""),
            "dm_excess_ne2001": _f(row.get("DMeNE2001") or ""),
            "source": "CHIME/FRB Catalog 1, J/ApJS/257/59",
        }
    out = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "citation": "CHIME/FRB Collaboration 2021 ApJS 257 59, VizieR J/ApJS/257/59",
        "n_with_position": len(seen),
        "frbs": list(seen.values()),
    }
    (FRB_DIR / "chime_frb_catalog1_positions.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    (FRB_DIR / "README.txt").write_text(
        "CHIME/FRB Catalog 1 positions from VizieR J/ApJS/257/59.\n"
        "Amiri et al. 2021, ApJS 257, 59. RA and Dec are J2000 degrees.\n"
        "The in-repo cache data/frb_repeater_cache.json has names without Dec "
        "and is not this file.\n",
        encoding="utf-8",
    )
    return len(seen)


def fetch_abell() -> int:
    CL_DIR.mkdir(parents=True, exist_ok=True)
    raw = _get(ABELL_URL)
    (CL_DIR / "abell_vii4a_vizier.tsv").write_bytes(raw)
    rows = _tsv_rows(raw.decode("utf-8", errors="replace"))
    objects = []
    for row in rows:
        ra = _f(row.get("RAJ2000") or "")
        dec = _f(row.get("DEJ2000") or "")
        name = row.get("ACO") or row.get("Abell") or ""
        if ra is None or dec is None or not name:
            continue
        objects.append(
            {
                "name": f"Abell_{name}",
                "ra_deg": ra,
                "dec_deg": dec,
                "richness": row.get("Rich") or "",
                "kind": "abell_cluster",
            }
        )
    doc = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "citation": "Abell, Corwin, and Olowin 1989, VizieR VII/4A",
        "n": len(objects),
        "objects": objects,
    }
    (CL_DIR / "abell_clusters.json").write_text(json.dumps(doc), encoding="utf-8")
    return len(objects)


def fetch_pantheon() -> int:
    SN_DIR.mkdir(parents=True, exist_ok=True)
    raw = _get(PANTHEON_URL)
    path = SN_DIR / "Pantheon+SH0ES.dat"
    path.write_bytes(raw)
    (SN_DIR / "README.txt").write_text(
        "Pantheon+SH0ES distance table from\n"
        "https://github.com/PantheonPlusSH0ES/DataRelease\n"
        "Scolnic et al. 2022, Brout et al. 2022.\n"
        "Hubble-flow supernovae inherit the host mix. No sightline sector.\n",
        encoding="utf-8",
    )
    return len(raw)


def main() -> int:
    n_frb = fetch_chime()
    n_abell = fetch_abell()
    n_bytes = fetch_pantheon()
    print(f"chime_positions={n_frb}")
    print(f"abell_clusters={n_abell}")
    print(f"pantheon_bytes={n_bytes}")
    return 0 if n_frb > 100 and n_abell > 100 and n_bytes > 1000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
