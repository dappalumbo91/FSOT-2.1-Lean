"""PubChem PUG REST live ingest + Tier 68 deep panel helpers."""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VENDOR_PUBCHEM = ROOT / "vendor" / "public_data" / "pubchem"
PANEL_PATH = VENDOR_PUBCHEM / "pubchem_preregistered_panel.json"
BUNDLED_SUMMARY = VENDOR_PUBCHEM / "pubchem_summary.json"

PUG_PROPERTIES = (
    "MolecularFormula,MolecularWeight,IUPACName,XLogP,TPSA,"
    "HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,MonoisotopicMass"
)

ANCHOR_PROPERTIES = (
    ("molecular_weight", "MolecularWeight"),
    ("xlogp", "XLogP"),
    ("tpsa", "TPSA"),
    ("hbond_donor_count", "HBondDonorCount"),
    ("hbond_acceptor_count", "HBondAcceptorCount"),
    ("rotatable_bond_count", "RotatableBondCount"),
    ("heavy_atom_count", "HeavyAtomCount"),
    ("monoisotopic_mass", "MonoisotopicMass"),
)


def _deep_mode() -> bool:
    for key in ("FSOT_TIER68_DEEP", "FSOT_TIER38_DEEP"):
        if os.environ.get(key, "").strip().lower() in {"1", "true", "yes", "on"}:
            return True
    return False


def load_panel() -> list[dict]:
    doc = json.loads(PANEL_PATH.read_text(encoding="utf-8"))
    seen: set[int] = set()
    out: list[dict] = []
    for row in doc.get("compounds") or []:
        cid = int(row["cid"])
        if cid in seen:
            continue
        seen.add(cid)
        out.append(row)
    return out


def panel_cids(*, deep: bool | None = None) -> list[int]:
    panel = load_panel()
    if deep is None:
        deep = _deep_mode()
    limit = len(panel) if deep else min(50, len(panel))
    return [int(r["cid"]) for r in panel[:limit]]


def tier38_cids(*, deep: bool | None = None) -> list[int]:
    return panel_cids(deep=deep if deep is not None else _deep_mode())


def _fetch_json(url: str, *, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/pubchem"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_compounds_batch(cids: list[int]) -> list[dict]:
    panel_by_cid = {int(r["cid"]): r for r in load_panel()}
    compounds: list[dict] = []
    chunk_size = 40
    for i in range(0, len(cids), chunk_size):
        chunk = cids[i : i + chunk_size]
        cid_str = ",".join(str(c) for c in chunk)
        url = (
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid_str}/"
            f"property/{PUG_PROPERTIES}/JSON"
        )
        try:
            payload = _fetch_json(url)
        except Exception:
            time.sleep(0.35)
            continue
        for props in (payload.get("PropertyTable") or {}).get("Properties") or []:
            cid = props.get("CID")
            if cid is None:
                continue
            meta = panel_by_cid.get(int(cid), {})
            row: dict[str, Any] = {
                "cid": int(cid),
                "name": meta.get("name"),
                "category": meta.get("category"),
                "domain": meta.get("domain"),
                "molecular_formula": props.get("MolecularFormula"),
                "molecular_weight": props.get("MolecularWeight"),
                "iupac_name": props.get("IUPACName"),
                "xlogp": props.get("XLogP"),
                "tpsa": props.get("TPSA"),
                "hbond_donor_count": props.get("HBondDonorCount"),
                "hbond_acceptor_count": props.get("HBondAcceptorCount"),
                "rotatable_bond_count": props.get("RotatableBondCount"),
                "heavy_atom_count": props.get("HeavyAtomCount"),
                "monoisotopic_mass": props.get("MonoisotopicMass"),
                "source": "pubchem_pug_live",
            }
            compounds.append(row)
        time.sleep(0.25)
    return compounds


def ingest_pubchem_live(*, cache_path: Path) -> dict:
    bundled = json.loads(BUNDLED_SUMMARY.read_text(encoding="utf-8")) if BUNDLED_SUMMARY.exists() else {"compounds": []}
    bundled_map = {int(c["cid"]): c for c in bundled.get("compounds") or [] if c.get("cid") is not None}
    cids = panel_cids()
    live = fetch_compounds_batch(cids)
    source = "pubchem_bundled"
    compounds = list(bundled.get("compounds") or [])
    if live:
        live_map = {int(c["cid"]): c for c in live}
        merged: list[dict] = []
        seen: set[int] = set()
        for cid in cids:
            row = live_map.get(cid) or bundled_map.get(cid)
            if row is None:
                continue
            merged.append(row)
            seen.add(cid)
        for row in bundled.get("compounds") or []:
            cid = row.get("cid")
            if cid is not None and int(cid) not in seen:
                merged.append(row)
        compounds = merged
        source = "pubchem_pug_live+bundled"
    doc = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "panel_cids_requested": len(cids),
        "compound_count": len(compounds),
        "compounds": compounds,
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


def ingest_pubchem_tier38_summary() -> dict:
    cids = tier38_cids()
    compounds = fetch_compounds_batch(cids)
    return {
        "source": "PubChem_PUG_REST",
        "compound_count": len(compounds),
        "compounds": [
            {
                "cid": c["cid"],
                "molecular_formula": c.get("molecular_formula"),
                "molecular_weight": c.get("molecular_weight"),
                "iupac_name": c.get("iupac_name"),
                "category": c.get("category"),
                "domain": c.get("domain"),
            }
            for c in compounds
        ],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }