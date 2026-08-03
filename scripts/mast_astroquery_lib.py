#!/usr/bin/env python3
"""MAST (Mikulski Archive for Space Telescopes) via astroquery — public access.

Docs: https://astroquery.readthedocs.io/en/latest/mast/mast.html

Policy:
  - No MAST API token required for public observations metadata and product lists.
  - Image *downloads* are optional and size-capped (default: metadata-only).
  - Never store credentials. Optional MAST_API_TOKEN env is unused unless user sets it.

This module supports FSOT open-science expansion: real astronomical catalogs +
optional cutouts/raw product pulls with explicit size budgets.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "open_science" / "mast_astroquery"
VENDOR.mkdir(parents=True, exist_ok=True)

# Safe defaults — metadata always; downloads only when explicitly requested.
DEFAULT_OBJECT = "M1"  # Crab Nebula — well-known public HST target
DEFAULT_COLLECTION = "HST"
DEFAULT_MAX_OBS = 5
DEFAULT_MAX_DOWNLOAD_MB = 15


def mast_available() -> tuple[bool, str]:
    try:
        from astroquery.mast import Observations  # noqa: F401

        return True, "astroquery.mast.Observations import ok"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def query_public_images(
    *,
    objectname: str = DEFAULT_OBJECT,
    obs_collection: str = DEFAULT_COLLECTION,
    max_obs: int = DEFAULT_MAX_OBS,
) -> dict[str, Any]:
    """Query public MAST image observations (metadata only)."""
    from astroquery.mast import Observations

    obs = Observations.query_criteria(
        obs_collection=obs_collection,
        objectname=objectname,
        dataproduct_type="image",
    )
    n = len(obs)
    colnames = list(obs.colnames)

    def _cell(row, name: str):
        if name not in colnames:
            return None
        val = row[name]
        try:
            if hasattr(val, "item"):
                return val.item()
        except Exception:
            pass
        return str(val) if val is not None else None

    # Prefer on-sky science targets; skip pure calibration DARK/BIAS when possible.
    indices: list[int] = []
    obj_u = objectname.upper()
    for i in range(len(obs)):
        tname = str(_cell(obs[i], "target_name") or "").upper()
        if any(bad in tname for bad in ("DARK", "BIAS", "FLAT", "EARTH-CAL", "INTFLAT")):
            continue
        if tname in {"ANY", "NONE", "LOW", "HIGH"}:
            continue
        if (
            obj_u in tname
            or "CRAB" in tname
            or "M1" == tname
            or "M-1" in tname
            or objectname.lower() in tname.lower()
        ):
            indices.append(i)
        if len(indices) >= int(max_obs):
            break
    if not indices:
        indices = list(range(min(int(max_obs), n)))

    rows: list[dict[str, Any]] = []
    for i in indices[: int(max_obs)]:
        row = obs[i]
        rows.append(
            {
                "obsid": _cell(row, "obsid"),
                "obs_id": _cell(row, "obs_id"),
                "target_name": _cell(row, "target_name"),
                "instrument_name": _cell(row, "instrument_name"),
                "filters": _cell(row, "filters"),
                "t_exptime": _cell(row, "t_exptime"),
                "s_ra": _cell(row, "s_ra"),
                "s_dec": _cell(row, "s_dec"),
                "jpegURL": _cell(row, "jpegURL"),
                "dataURL": _cell(row, "dataURL"),
                "obs_collection": _cell(row, "obs_collection"),
            }
        )
    take = len(rows)

    return {
        "source": "MAST",
        "auth": "none_public",
        "docs": "https://astroquery.readthedocs.io/en/latest/mast/mast.html",
        "objectname": objectname,
        "obs_collection": obs_collection,
        "query_rows_total": int(n),
        "returned": take,
        "observations": rows,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def product_manifest_for_obs(obs_row) -> dict[str, Any]:
    """List data products for one observation row (no download)."""
    from astroquery.mast import Observations

    prods = Observations.get_product_list(obs_row)
    colnames = list(prods.colnames)
    items: list[dict[str, Any]] = []
    for i in range(min(len(prods), 40)):
        p = prods[i]
        item = {}
        for key in (
            "productFilename",
            "productType",
            "productSubGroupDescription",
            "size",
            "dataURI",
            "obs_id",
            "description",
        ):
            if key in colnames:
                val = p[key]
                try:
                    item[key] = val.item() if hasattr(val, "item") else str(val)
                except Exception:
                    item[key] = str(val)
        items.append(item)
    return {
        "product_count": int(len(prods)),
        "products_sample": items,
    }


def download_small_products(
    obs_table_slice,
    *,
    download_dir: Path | None = None,
    max_mb: float = DEFAULT_MAX_DOWNLOAD_MB,
) -> dict[str, Any]:
    """Optionally download a size-capped set of SCIENCE products.

    Returns paths + sizes. Skips if total would exceed max_mb.
    """
    from astroquery.mast import Observations

    download_dir = download_dir or (VENDOR / "downloads")
    download_dir.mkdir(parents=True, exist_ok=True)

    prods = Observations.get_product_list(obs_table_slice)
    # Prefer calibrated science products when available
    try:
        filtered = Observations.filter_products(
            prods,
            productType=["SCIENCE"],
            mrp_only=False,
        )
    except Exception:
        filtered = prods

    # Estimate size
    total = 0
    if "size" in filtered.colnames:
        for i in range(len(filtered)):
            try:
                total += int(filtered["size"][i])
            except Exception:
                pass
    total_mb = total / (1024 * 1024) if total else None
    if total_mb is not None and total_mb > max_mb:
        return {
            "status": "skipped_size_budget",
            "estimated_mb": total_mb,
            "max_mb": max_mb,
            "product_count": int(len(filtered)),
            "download_dir": str(download_dir),
        }

    # Cap product count for safety
    if len(filtered) > 3:
        filtered = filtered[:3]

    manifest = Observations.download_products(
        filtered,
        download_dir=str(download_dir),
        cache=True,
    )
    files: list[dict[str, Any]] = []
    if manifest is not None:
        for row in manifest:
            try:
                path = str(row["Local Path"])
            except Exception:
                path = str(row)
            size = None
            p = Path(path) if path else None
            if p and p.exists():
                size = p.stat().st_size
            files.append({"path": path, "bytes": size})

    return {
        "status": "downloaded",
        "estimated_mb": total_mb,
        "max_mb": max_mb,
        "files": files,
        "download_dir": str(download_dir),
    }


def ingest_mast_bundle(
    *,
    objectname: str = DEFAULT_OBJECT,
    obs_collection: str = DEFAULT_COLLECTION,
    max_obs: int = DEFAULT_MAX_OBS,
    download: bool = False,
    max_download_mb: float = DEFAULT_MAX_DOWNLOAD_MB,
) -> dict[str, Any]:
    """Full ingest: metadata always; optional size-capped download."""
    ok, msg = mast_available()
    if not ok:
        raise RuntimeError(f"astroquery.mast unavailable: {msg}")

    meta = query_public_images(
        objectname=objectname,
        obs_collection=obs_collection,
        max_obs=max_obs,
    )

    # Product lists for first observation via re-query slice
    from astroquery.mast import Observations

    obs = Observations.query_criteria(
        obs_collection=obs_collection,
        objectname=objectname,
        dataproduct_type="image",
    )
    product_info = None
    download_info = None
    if len(obs) > 0:
        product_info = product_manifest_for_obs(obs[0])
        if download:
            download_info = download_small_products(
                obs[:1],
                download_dir=VENDOR / "downloads" / objectname.replace(" ", "_"),
                max_mb=max_download_mb,
            )

    bundle = {
        **meta,
        "product_manifest_first_obs": product_info,
        "download": download_info,
        "token_required": False,
        "note": (
            "Public MAST metadata/product lists need no login. "
            "Large FITS downloads are optional and budget-capped."
        ),
    }
    out = VENDOR / "live.json"
    out.write_text(json.dumps(bundle, indent=2, default=str), encoding="utf-8")
    bundle["path"] = str(out.relative_to(ROOT))
    return bundle
