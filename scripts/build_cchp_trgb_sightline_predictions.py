#!/usr/bin/env python3
"""CCHP / Carnegie TRGB galaxy sightline H0 predictions.

Bulk host catalog lives on external drive:
  G:/FSOT-PublicData/anomaly_observables/carnegie_trgb/

Monorepo outputs (lightweight):
  data/cchp_trgb_sightline_predictions.json
  data/publication/CCHP_TRGB_SIGHTLINE_PREDICTIONS.md
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from bubble_bleed_physics import (  # noqa: E402
    H0_CONTESTED_TOLERANCE_PCT,
    bubble_density_for_sector,
    sector_h0_density_model,
    sky_sector,
)
from cosmology_lambda import H0_CANONICAL  # noqa: E402
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

# Prefer external Seagate; fall back to monorepo vendor mirror if present
EXTERNAL_HOSTS = Path(r"G:\FSOT-PublicData\anomaly_observables\carnegie_trgb\cchp_trgb_hosts.json")
LOCAL_MIRROR = ROOT / "vendor" / "public_data_pointers" / "cchp_trgb_hosts.json"
SECTOR_SEED = ROOT / "data" / "sector_h0_seed.json"
NEBULA = ROOT / "data" / "nebula_lensing_cache.json"
FRB = ROOT / "data" / "frb_repeater_cache.json"
OUT_JSON = ROOT / "data" / "cchp_trgb_sightline_predictions.json"
OUT_MD = ROOT / "data" / "publication" / "CCHP_TRGB_SIGHTLINE_PREDICTIONS.md"
POINTER = ROOT / "data" / "external_data_pointers.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_hosts() -> tuple[dict, Path]:
    for p in (EXTERNAL_HOSTS, LOCAL_MIRROR):
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8")), p
    raise FileNotFoundError(
        f"CCHP TRGB host catalog not found. Expected {EXTERNAL_HOSTS}"
    )


def build() -> dict:
    hosts_doc, source_path = _load_hosts()
    seed = json.loads(SECTOR_SEED.read_text(encoding="utf-8"))
    h0_global = float(seed.get("h0_global_fsot") or H0_CANONICAL)
    bleed = float(seed.get("bubble_bleed_fraction") or 0.015431)
    freedman = next(
        (s for s in seed.get("sectors") or [] if s.get("name") == "freedman_jwst"),
        {"bubble_density_proxy": 1.85, "measured_h0": 70.39},
    )
    carnegie = next(
        (s for s in seed.get("sectors") or [] if s.get("name") == "carnegie_h0"),
        {"bubble_density_proxy": 2.04, "measured_h0": 69.8},
    )
    density_seed_trgb = float(freedman.get("bubble_density_proxy") or 1.85)
    density_seed_anchor = float(carnegie.get("bubble_density_proxy") or 2.04)
    lit_trgb = float(
        (hosts_doc.get("literature_h0") or {}).get("trgb_plus_hst_jwst_best")
        or freedman.get("measured_h0")
        or 70.39
    )

    nebulae = json.loads(NEBULA.read_text(encoding="utf-8")).get("nebulae") or [] if NEBULA.is_file() else []
    frbs = json.loads(FRB.read_text(encoding="utf-8")).get("frbs") or [] if FRB.is_file() else []
    mod, authority = load_fsot_compute()
    authority = str(authority).replace("\\", "/")

    # Merge primary JWST sample + extended HST-era (dedupe by name)
    by_name: dict[str, dict] = {}
    for row in hosts_doc.get("hosts") or []:
        by_name[str(row["name"])] = {**row, "sample": "jwst_primary"}
    for row in hosts_doc.get("extended_cchp_hst_era_hosts") or []:
        name = str(row["name"])
        if name not in by_name:
            by_name[name] = {**row, "sample": "hst_era_extended"}
        else:
            by_name[name]["also_hst_era"] = True

    host_preds = []
    for name, row in sorted(by_name.items()):
        ra = float(row.get("ra_deg") or 0.0)
        dec = float(row.get("dec_deg") or 0.0)
        method = str(row.get("method") or "CCHP_TRGB")
        role = str(row.get("role") or "calibrator")
        sector = sky_sector(ra)
        density_sky = bubble_density_for_sector(nebulae, frbs, sector)
        if role == "zero_point_anchor" or "Maser" in method:
            density_model = sector_h0_density_model(
                "carnegie_h0", density_seed_anchor, density_sky, mod
            )
            tool_class = "trgb_geometric_anchor_sightline"
        else:
            density_model = sector_h0_density_model(
                "freedman_jwst", density_seed_trgb, density_sky, mod
            )
            tool_class = "cchp_trgb_host_sightline"

        predicted = h0_global * (1.0 + float(density_model) * bleed)
        host_preds.append(
            {
                "id": f"H0-TRGB-{name}",
                "pred_id": f"PRED-H0-TRGB-{name.replace(' ', '_')}",
                "host": name,
                "ra_deg": ra,
                "dec_deg": dec,
                "method": method,
                "role": role,
                "sn_name": row.get("sn_name"),
                "sample": row.get("sample"),
                "sky_sector": sector,
                "bubble_density_sky": round(density_sky, 6),
                "bubble_density_model": round(float(density_model), 6),
                "fsot_predicted_h0": round(predicted, 6),
                "literature_program_h0": lit_trgb,
                "tool_class": tool_class,
                "unit": "km/s/Mpc",
                "kill": (
                    f"cchp_trgb_host_{name}_outside_"
                    f"{H0_CONTESTED_TOLERANCE_PCT}pct_of_fsot_when_updated"
                ),
            }
        )

    host_preds.sort(key=lambda h: h["fsot_predicted_h0"])
    mean_h0 = (
        sum(h["fsot_predicted_h0"] for h in host_preds) / len(host_preds)
        if host_preds
        else None
    )

    sector_preds = []
    for sector_name in sorted({h["sky_sector"] for h in host_preds}):
        members = [h for h in host_preds if h["sky_sector"] == sector_name]
        sector_preds.append(
            {
                "id": f"H0-TRGB-SECTOR-{sector_name}",
                "pred_id": f"PRED-H0-TRGB-SECTOR-{sector_name}",
                "sky_sector": sector_name,
                "host_count": len(members),
                "hosts": [h["host"] for h in members],
                "fsot_predicted_h0_mean": round(
                    sum(h["fsot_predicted_h0"] for h in members) / len(members), 6
                ),
                "fsot_predicted_h0_min": min(h["fsot_predicted_h0"] for h in members),
                "fsot_predicted_h0_max": max(h["fsot_predicted_h0"] for h in members),
            }
        )

    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "authority_path": authority,
        "authority_pin_prefix": "D1D38A",
        "external_catalog_path": str(source_path).replace("\\", "/"),
        "external_drive_policy": (
            "Large catalogs stay on G:/FSOT-PublicData; monorepo stores predictions only."
        ),
        "theory": {
            "mechanism": "black_hole_white_hole_bubble_bleed",
            "claim": (
                "CCHP TRGB galaxies are intermediate-ladder sightlines — milder bubble "
                "density than SH0ES Cepheid hosts, distinct from CMB-depleted sectors. "
                "Each galaxy gets its own FSOT H0 prediction."
            ),
            "formula": "H0_host = H0_global_fsot * (1 + density_model * bubble_bleed_fraction)",
        },
        "h0_global_fsot": h0_global,
        "bubble_bleed_fraction": bleed,
        "trgb_density_seed": density_seed_trgb,
        "literature_program_h0": lit_trgb,
        "host_count": len(host_preds),
        "host_mean_fsot_h0": round(mean_h0, 6) if mean_h0 is not None else None,
        "span_km_s_mpc": {
            "min_fsot": min((h["fsot_predicted_h0"] for h in host_preds), default=None),
            "max_fsot": max((h["fsot_predicted_h0"] for h in host_preds), default=None),
        },
        "hosts": host_preds,
        "sky_sectors": sector_preds,
        "refresh": "python scripts/build_cchp_trgb_sightline_predictions.py",
    }
    raw = json.dumps({k: v for k, v in doc.items() if k != "bundle_sha256"}, sort_keys=True).encode()
    doc["bundle_sha256"] = hashlib.sha256(raw).hexdigest()
    return doc


def write_md(doc: dict) -> None:
    lines = [
        "# CCHP / Carnegie TRGB sightline H₀ predictions",
        "",
        f"*Generated {doc.get('generated_at')} · pin D1D38A · {doc.get('host_count')} hosts*",
        "",
        str((doc.get("theory") or {}).get("claim") or ""),
        "",
        f"**External catalog:** `{doc.get('external_catalog_path')}`  ",
        f"**Host-mean FSOT H₀** = `{doc.get('host_mean_fsot_h0')}`  ",
        f"**Literature program H₀** ≈ `{doc.get('literature_program_h0')}`  ",
        f"**Span** = `{doc.get('span_km_s_mpc')}`",
        "",
        "| Host | Role | RA° | Sector | FSOT H₀ | Sample |",
        "|------|------|----:|--------|--------:|--------|",
    ]
    for h in doc.get("hosts") or []:
        lines.append(
            f"| {h['host']} | {h.get('role')} | {h['ra_deg']:.3f} | `{h['sky_sector']}` | "
            f"**{h['fsot_predicted_h0']}** | {h.get('sample')} |"
        )
    lines.extend(
        [
            "",
            f"Bundle SHA-256: `{doc.get('bundle_sha256')}`",
            "",
            "Refresh: `python scripts/build_cchp_trgb_sightline_predictions.py`",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_pointer(doc: dict) -> None:
    ptr = {}
    if POINTER.is_file():
        try:
            ptr = json.loads(POINTER.read_text(encoding="utf-8"))
        except Exception:
            ptr = {}
    ptr.setdefault("external_root", "G:/FSOT-PublicData")
    ptr.setdefault("datasets", {})
    ptr["datasets"]["carnegie_trgb"] = {
        "path": doc.get("external_catalog_path"),
        "predictions": "data/cchp_trgb_sightline_predictions.json",
        "updated_at": doc.get("generated_at"),
        "host_count": doc.get("host_count"),
    }
    ptr["policy"] = (
        "Store large open-science dumps on G:/FSOT-PublicData. "
        "Monorepo keeps engines, predictions, and path pointers only."
    )
    POINTER.write_text(json.dumps(ptr, indent=2), encoding="utf-8")


def main() -> int:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    write_pointer(doc)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"  hosts={doc['host_count']} mean={doc['host_mean_fsot_h0']} "
        f"span={doc['span_km_s_mpc']} src={doc['external_catalog_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
