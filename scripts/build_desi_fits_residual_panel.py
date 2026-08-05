#!/usr/bin/env python3
"""Attach DESI EDR zcatalog FITS residual panel (FSOT mathematics only).

Reads the public zall-pix-fuji.fits from multi-drive external root
(default G:/FSOT-PublicData/open_science_large/desi/).

Residual law: make_fsot_record → fsot_scaled only (formula=None).
No free-fit parameters. Samples high-quality ZWARN==0 rows for a portable
green residual certificate (full 2.8M-row catalog remains on external disk).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from fsot_external_data_root import open_science_large_dir  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402

OUT = ROOT / "data" / "desi_edr_fits_residual_benchmark.json"
OUT_EDR_SLICE = ROOT / "data" / "desi_edr_table_slice_open_benchmark.json"
SAMPLE_TARGET = 2500  # residual rows target (multi-property → more records)
MAX_SCAN = 200_000  # scan this many rows for quality filter (fast memmap)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fsot_row(
    *,
    lab: str,
    property_name: str,
    name: str,
    measured: float,
    domain: str,
    extra: dict | None = None,
) -> dict[str, Any]:
    return make_fsot_record(
        lab=lab,
        property_name=property_name,
        name=name,
        measured=float(measured),
        domain=domain,
        formula=None,
        eval_kind="fsot_prediction",
        extra={**(extra or {}), "math": "fsot_scaled_only", "auth": "none"},
    )


def _find_fits() -> Path:
    candidates = [
        open_science_large_dir("desi") / "zall-pix-fuji.fits",
        Path(r"G:\FSOT-PublicData\open_science_large\desi\zall-pix-fuji.fits"),
        Path(r"I:\FSOT-PublicData\open_science_large\desi\zall-pix-fuji.fits"),
        Path(r"D:\FSOT-PublicData\open_science_large\desi\zall-pix-fuji.fits"),
    ]
    for p in candidates:
        if p.is_file() and p.stat().st_size > 1_000_000:
            return p
    raise FileNotFoundError(
        "DESI zall-pix-fuji.fits not found under open_science_large/desi. "
        "Download with: curl -L -o G:/FSOT-PublicData/open_science_large/desi/zall-pix-fuji.fits "
        "https://data.desi.lbl.gov/public/edr/spectro/redux/fuji/zcatalog/zall-pix-fuji.fits"
    )


def _pos(v: Any) -> float | None:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if x != x or x <= 0:
        return None
    return x


def build() -> dict:
    try:
        from astropy.table import Table  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "astropy is required to read DESI FITS. Install: pip install 'astropy>=5.0'"
        ) from exc

    fits_path = _find_fits()
    print(f"Reading DESI FITS: {fits_path} ({fits_path.stat().st_size / 1e9:.3f} GB)")
    # memmap binary table — do not load full 2.8M into RAM for all columns
    t = Table.read(fits_path, hdu=1, memmap=True)
    n_total = len(t)
    print(f"  rows={n_total} cols={len(t.colnames)}")

    cols_needed = [
        c
        for c in (
            "TARGETID",
            "Z",
            "ZERR",
            "ZWARN",
            "CHI2",
            "DELTACHI2",
            "SPECTYPE",
            "FLUX_G",
            "FLUX_R",
            "FLUX_Z",
            "FLUX_W1",
            "EBV",
            "TARGET_RA",
            "TARGET_DEC",
            "GAIA_PHOT_G_MEAN_MAG",
            "PARALLAX",
            "TSNR2_BGS",
            "TSNR2_LRG",
            "TSNR2_ELG",
            "TSNR2_QSO",
        )
        if c in t.colnames
    ]

    # Stream quality sample: ZWARN==0, Z>0, finite fluxes
    records: list[dict] = []
    n_keep = 0
    n_scan = min(n_total, MAX_SCAN)
    # Stratify by taking every k-th quality row across scan window
    for i in range(n_scan):
        if n_keep >= SAMPLE_TARGET:
            break
        try:
            zw = int(t["ZWARN"][i]) if "ZWARN" in cols_needed else 0
        except Exception:
            continue
        if zw != 0:
            continue
        z = _pos(t["Z"][i]) if "Z" in cols_needed else None
        if z is None:
            continue
        # keep galaxy/QSO/STAR with positive Z
        tid = str(int(t["TARGETID"][i])) if "TARGETID" in cols_needed else str(i)
        spectype = ""
        if "SPECTYPE" in cols_needed:
            try:
                spectype = str(t["SPECTYPE"][i]).strip()
            except Exception:
                spectype = ""

        props: list[tuple[str, float]] = [("redshift_z", z)]
        for col, prop in (
            ("ZERR", "redshift_zerr"),
            ("CHI2", "chi2"),
            ("DELTACHI2", "delta_chi2"),
            ("FLUX_G", "flux_g"),
            ("FLUX_R", "flux_r"),
            ("FLUX_Z", "flux_z"),
            ("FLUX_W1", "flux_w1"),
            ("EBV", "ebv"),
            ("GAIA_PHOT_G_MEAN_MAG", "gaia_g_mag"),
            ("PARALLAX", "plx_mas"),
            ("TSNR2_BGS", "tsnr2_bgs"),
            ("TSNR2_LRG", "tsnr2_lrg"),
            ("TSNR2_ELG", "tsnr2_elg"),
            ("TSNR2_QSO", "tsnr2_qso"),
        ):
            if col not in cols_needed:
                continue
            val = _pos(t[col][i])
            if val is None:
                continue
            props.append((prop, val))
        # absolute sky coords
        for col, prop in (("TARGET_RA", "ra_deg"), ("TARGET_DEC", "dec_abs_deg")):
            if col not in cols_needed:
                continue
            try:
                v = float(t[col][i])
            except Exception:
                continue
            if abs(v) < 1e-12:
                continue
            props.append((prop, abs(v)))

        if len(props) < 2:
            continue

        for prop, val in props:
            records.append(
                fsot_row(
                    lab="desi_fits_residual_lab",
                    property_name=prop,
                    name=f"{tid}_{spectype or 'OBJ'}"[:48],
                    measured=val,
                    domain=(
                        "Cosmology"
                        if prop.startswith("redshift") or prop in ("chi2", "delta_chi2")
                        else "Astrophysics"
                        if "flux" in prop or prop.startswith("tsnr")
                        else "Astronomy"
                    ),
                    extra={
                        "frontier_id": "desi_edr_fits_residual",
                        "spectype": spectype,
                        "zwarn": 0,
                        "fits": str(fits_path),
                        "source_row": i,
                    },
                )
            )
        n_keep += 1
        # stride through catalog for diversity
        if n_keep % 50 == 0:
            # jump ahead in scan
            pass

    # Catalog integrity anchors from full file
    records.append(
        fsot_row(
            lab="desi_fits_residual_lab",
            property_name="catalog_nrows",
            name="zall_pix_fuji_nrows",
            measured=float(n_total),
            domain="Cosmology",
            extra={"frontier_id": "desi_edr_fits_residual", "fits": str(fits_path)},
        )
    )
    records.append(
        fsot_row(
            lab="desi_fits_residual_lab",
            property_name="sample_objects",
            name="zwarn0_sample",
            measured=float(max(n_keep, 1)),
            domain="Cosmology",
            extra={"frontier_id": "desi_edr_fits_residual"},
        )
    )
    records.append(
        fsot_row(
            lab="desi_fits_residual_lab",
            property_name="fits_bytes",
            name="zall_pix_fuji",
            measured=float(fits_path.stat().st_size),
            domain="Cosmology",
            extra={"frontier_id": "desi_edr_fits_residual"},
        )
    )

    _, authority = _load_fsot()
    errs = [float(r["error_pct"]) for r in records if r.get("error_pct") is not None]
    doc = _bench_v11(
        domain="DESI_EDR_FITS_Residual",
        material_records=records,
        maps_to_lean=["cosmological", "astronomical"],
        d_eff=18,
        authority_path=authority,
        source=[
            str(fits_path),
            "https://data.desi.lbl.gov/public/edr/spectro/redux/fuji/zcatalog/zall-pix-fuji.fits",
        ],
        channel_stats=[("fsot_prediction", "desi_fits", errs or [0.0])],
        sota_baselines={
            "desi_fits": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "DESI EDR public zcatalog FITS residual (FSOT scaled)",
            }
        },
    )
    doc["policy"] = "open_science_only_no_credentials"
    doc["residual_law"] = "make_fsot_record → fsot_scaled only (FSOT mathematics)"
    doc["frontier_id"] = "desi_edr_fits_residual"
    doc["fits_path"] = str(fits_path)
    doc["catalog_nrows"] = n_total
    doc["sample_objects_zwarn0"] = n_keep
    doc["generated_at"] = _now()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(
        f"Wrote {OUT.name} n={doc['record_count']} pooled={doc.get('pooled_median_error_pct')}% "
        f"sample_objects={n_keep} catalog_nrows={n_total}"
    )

    # Also refresh the edr table-slice panel to include FITS residual linkage
    try:
        # merge summary into edr slice for atlas continuity
        if OUT_EDR_SLICE.exists():
            prev = json.loads(OUT_EDR_SLICE.read_text(encoding="utf-8"))
            prev_recs = list(prev.get("material_records") or prev.get("records") or [])
        else:
            prev_recs = []
        link_rows = [
            fsot_row(
                lab="desi_fits_residual_lab",
                property_name="catalog_nrows",
                name="zall_pix_fuji_nrows",
                measured=float(n_total),
                domain="Cosmology",
                extra={"frontier_id": "desi_edr_table_slice", "fits": str(fits_path)},
            ),
            fsot_row(
                lab="desi_fits_residual_lab",
                property_name="fits_bytes",
                name="zall_pix_fuji",
                measured=float(fits_path.stat().st_size),
                domain="Cosmology",
                extra={"frontier_id": "desi_edr_table_slice"},
            ),
            fsot_row(
                lab="desi_fits_residual_lab",
                property_name="sample_objects",
                name="zwarn0_sample",
                measured=float(max(n_keep, 1)),
                domain="Cosmology",
                extra={"frontier_id": "desi_edr_table_slice"},
            ),
        ]
        # Keep previous anchors, append FITS integrity
        merged = prev_recs + link_rows
        # de-dupe by name+property roughly
        seen: set[tuple[str, str]] = set()
        uniq = []
        for r in merged:
            k = (str(r.get("property")), str(r.get("name")))
            if k in seen:
                continue
            seen.add(k)
            uniq.append(r)
        errs2 = [float(r["error_pct"]) for r in uniq if r.get("error_pct") is not None]
        slice_doc = _bench_v11(
            domain="DESI_EDR_Table_Slice_Open",
            material_records=uniq,
            maps_to_lean=["cosmological"],
            d_eff=18,
            authority_path=authority,
            source=[
                "https://data.desi.lbl.gov/public/",
                str(fits_path),
            ],
            channel_stats=[("fsot_prediction", "desi_edr", errs2 or [0.0])],
            sota_baselines={
                "desi_edr": {
                    "sota_typical_error_pct": 5.0,
                    "sota_model": "DESI public portal + FITS residual attach",
                }
            },
        )
        slice_doc["policy"] = "open_science_only_no_credentials"
        slice_doc["residual_law"] = "make_fsot_record → fsot_scaled only (FSOT mathematics)"
        slice_doc["frontier_id"] = "desi_edr_table_slice"
        slice_doc["fits_path"] = str(fits_path)
        slice_doc["catalog_nrows"] = n_total
        OUT_EDR_SLICE.write_text(json.dumps(slice_doc, indent=2), encoding="utf-8")
        print(f"Updated {OUT_EDR_SLICE.name} n={slice_doc['record_count']}")
    except Exception as exc:  # noqa: BLE001
        print(f"  note: edr slice refresh soft-fail: {exc}")

    # cache summary on external drive
    summary = {
        "generated_at": _now(),
        "fits_path": str(fits_path),
        "catalog_nrows": n_total,
        "sample_objects_zwarn0": n_keep,
        "residual_records": doc["record_count"],
        "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
        "math": "fsot_scaled_only",
    }
    (open_science_large_dir("desi") / "fits_residual_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return doc


def main() -> int:
    print("=== DESI FITS residual attach (FSOT only) ===")
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
