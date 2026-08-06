#!/usr/bin/env python3
"""Per-host / per-sightline H0 predictions (SH0ES hosts × BH→WH bubble density).

Each Cepheid host samples a different sky sector bubble density. FSOT predicts
a host-level H0, not one ladder number:

  H0_host = H0_global * (1 + density_model(host) * bleed_fraction)

Outputs:
  predictions/h0_sightline_predictions.json
  predictions/reports/H0_SIGHTLINE_PREDICTIONS.md
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

HOST_COORDS = ROOT / "data" / "sh0es_host_coordinates.json"
SECTOR_SEED = ROOT / "predictions" / "sector_h0_seed.json"
NEBULA = ROOT / "data" / "nebula_lensing_cache.json"
FRB = ROOT / "data" / "frb_repeater_cache.json"
OUT_JSON = ROOT / "predictions" / "h0_sightline_predictions.json"
OUT_MD = ROOT / "predictions" / "reports" / "H0_SIGHTLINE_PREDICTIONS.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build() -> dict:
    seed = json.loads(SECTOR_SEED.read_text(encoding="utf-8"))
    h0_global = float(seed.get("h0_global_fsot") or H0_CANONICAL)
    bleed = float(seed.get("bubble_bleed_fraction") or 0.015431)
    sh0es_seed = next(
        (s for s in seed.get("sectors") or [] if s.get("name") == "sh0es_jwst"),
        {"bubble_density_proxy": 5.1, "measured_h0": 73.04},
    )
    sh0es_density_seed = float(sh0es_seed.get("bubble_density_proxy") or 5.1)
    sh0es_measured = float(sh0es_seed.get("measured_h0") or 73.04)

    nebulae = []
    frbs = []
    if NEBULA.is_file():
        nebulae = json.loads(NEBULA.read_text(encoding="utf-8")).get("nebulae") or []
    if FRB.is_file():
        frbs = json.loads(FRB.read_text(encoding="utf-8")).get("frbs") or []

    mod, authority = load_fsot_compute()
    authority = str(authority).replace("\\", "/")

    hosts_raw = []
    if HOST_COORDS.is_file():
        hosts_raw = json.loads(HOST_COORDS.read_text(encoding="utf-8")).get("hosts") or []

    host_preds = []
    for row in hosts_raw:
        name = str(row.get("name") or "")
        ra = float(row.get("ra_deg") or 0.0)
        dec = float(row.get("dec_deg") or 0.0)
        method = str(row.get("method") or "SH0ES_Cepheid")
        sector = sky_sector(ra)
        density_sky = bubble_density_for_sector(nebulae, frbs, sector)
        # Anchor ladders (maser/TRGB) use milder density coupling than Cepheid hosts
        if "Maser" in method or method == "Maser_anchor":
            density_model = sector_h0_density_model(
                "carnegie_h0", 2.0, density_sky, mod
            )
            tool_class = "geometric_anchor_sightline"
        elif "TRGB" in method:
            density_model = sector_h0_density_model(
                "freedman_jwst", 1.85, density_sky, mod
            )
            tool_class = "trgb_anchor_sightline"
        else:
            density_model = sector_h0_density_model(
                "sh0es_jwst", sh0es_density_seed, density_sky, mod
            )
            tool_class = "cepheid_host_sightline"

        predicted = h0_global * (1.0 + float(density_model) * bleed)
        host_preds.append(
            {
                "id": f"H0-HOST-{name}",
                "pred_id": f"PRED-H0-HOST-{name.replace(' ', '_')}",
                "host": name,
                "ra_deg": ra,
                "dec_deg": dec,
                "method": method,
                "sky_sector": sector,
                "bubble_density_sky": round(density_sky, 6),
                "bubble_density_model": round(float(density_model), 6),
                "fsot_predicted_h0": round(predicted, 6),
                "ladder_class_anchor_h0": sh0es_measured,
                "tool_class": tool_class,
                "unit": "km/s/Mpc",
                "kill": (
                    f"host_{name}_effective_H0_outside_"
                    f"{H0_CONTESTED_TOLERANCE_PCT}pct_of_fsot_when_published"
                ),
                "note": (
                    "Sightline-resolved prediction: host samples local bubble density "
                    "via RA sector + nebula/FRB sky map; not a free-fit per host."
                ),
            }
        )

    host_preds.sort(key=lambda h: h["fsot_predicted_h0"])

    # Aggregate sky-sector predictions (6 coarse zones)
    sector_preds = []
    for sector_name in sorted({h["sky_sector"] for h in host_preds}):
        members = [h for h in host_preds if h["sky_sector"] == sector_name]
        if not members:
            continue
        mean_h0 = sum(h["fsot_predicted_h0"] for h in members) / len(members)
        sector_preds.append(
            {
                "id": f"H0-SECTOR-{sector_name}",
                "pred_id": f"PRED-H0-SECTOR-{sector_name}",
                "sky_sector": sector_name,
                "host_count": len(members),
                "hosts": [h["host"] for h in members],
                "fsot_predicted_h0_mean": round(mean_h0, 6),
                "fsot_predicted_h0_min": min(h["fsot_predicted_h0"] for h in members),
                "fsot_predicted_h0_max": max(h["fsot_predicted_h0"] for h in members),
                "unit": "km/s/Mpc",
                "kill": f"sector_{sector_name}_host_mean_outside_tolerance",
            }
        )

    weighted = None
    if host_preds:
        weighted = sum(h["fsot_predicted_h0"] for h in host_preds) / len(host_preds)

    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "authority_path": authority,
        "authority_pin_prefix": "D1D38A",
        "theory": {
            "mechanism": "black_hole_white_hole_bubble_bleed",
            "claim": (
                "SH0ES host galaxies lie on different sightlines through the "
                "BH→WH information-flow / nebula-bleed field. Each host gets its "
                "own FSOT H0 prediction; the ladder average is a mixture, not a "
                "single fundamental constant."
            ),
            "formula": "H0_host = H0_global_fsot * (1 + density_model * bubble_bleed_fraction)",
        },
        "h0_global_fsot": h0_global,
        "bubble_bleed_fraction": bleed,
        "sh0es_class_density_seed": sh0es_density_seed,
        "sh0es_literature_anchor": sh0es_measured,
        "nebula_count": len(nebulae),
        "frb_count": len(frbs),
        "host_count": len(host_preds),
        "sky_sector_count": len(sector_preds),
        "host_mean_fsot_h0": round(weighted, 6) if weighted is not None else None,
        "span_km_s_mpc": {
            "min_fsot": min((h["fsot_predicted_h0"] for h in host_preds), default=None),
            "max_fsot": max((h["fsot_predicted_h0"] for h in host_preds), default=None),
        },
        "hosts": host_preds,
        "sky_sectors": sector_preds,
        "refresh": "python scripts/build_h0_sightline_predictions.py",
    }
    raw = json.dumps({k: v for k, v in doc.items() if k != "bundle_sha256"}, sort_keys=True).encode()
    doc["bundle_sha256"] = hashlib.sha256(raw).hexdigest()
    return doc


def write_md(doc: dict) -> None:
    lines = [
        "# Per-host / sightline H₀ predictions",
        "",
        f"*Generated {doc.get('generated_at')} · pin D1D38A · {doc.get('host_count')} hosts*",
        "",
        str((doc.get("theory") or {}).get("claim") or ""),
        "",
        f"**Global FSOT H₀** = `{doc.get('h0_global_fsot')}`  ",
        f"**Host-mean FSOT H₀** = `{doc.get('host_mean_fsot_h0')}`  ",
        f"**Span** = `{doc.get('span_km_s_mpc')}`  ",
        f"**Nebulae / FRBs used for sky density** = {doc.get('nebula_count')} / {doc.get('frb_count')}",
        "",
        "## Sky sectors",
        "",
        "| Sector | Hosts | Mean FSOT H₀ | Min | Max |",
        "|--------|------:|-------------:|----:|----:|",
    ]
    for s in doc.get("sky_sectors") or []:
        lines.append(
            f"| `{s['sky_sector']}` | {s['host_count']} | **{s['fsot_predicted_h0_mean']}** | "
            f"{s['fsot_predicted_h0_min']} | {s['fsot_predicted_h0_max']} |"
        )
    lines.extend(
        [
            "",
            "## Hosts (sorted by FSOT H₀)",
            "",
            "| Host | Method | RA° | Sector | Density sky | FSOT H₀ |",
            "|------|--------|----:|--------|------------:|--------:|",
        ]
    )
    for h in doc.get("hosts") or []:
        lines.append(
            f"| {h['host']} | {h['method']} | {h['ra_deg']:.3f} | `{h['sky_sector']}` | "
            f"{h['bubble_density_sky']} | **{h['fsot_predicted_h0']}** |"
        )
    lines.extend(
        [
            "",
            f"Bundle SHA-256: `{doc.get('bundle_sha256')}`",
            "",
            "Refresh: `python scripts/build_h0_sightline_predictions.py`",
            "",
            "Related: multi-tool table `H0_MULTI_TOOL_PREDICTIONS.md` · seed `predictions/sector_h0_seed.json`",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"  hosts={doc['host_count']} sectors={doc['sky_sector_count']} "
        f"mean={doc['host_mean_fsot_h0']} span={doc['span_km_s_mpc']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
