#!/usr/bin/env python3
"""SH0ES three-rung ladder chain — fill the class-bin gap.

Does **not** retune predictions/sector_h0_seed.json ρ=5.05.
The published 73.04 is the information-weighted mixture of
geometric-anchor sectors and Cepheid-host sectors. Weights are
public Cepheid counts (Riess+2022 table). Sky density is host-local
(angular kernel), not 60° RA bins.

  H0_chain = Σ n_i H0_i / Σ n_i
  H0_i     = H0_global (1 + ρ_i ε)
  ρ_i      = class interface (anchor vs host) + local_sky_density
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from bubble_bleed_physics import (  # noqa: E402
    ladder_chain_h0,
    ladder_object_density_model,
    local_sky_density,
)
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
from tier_gap_fill_lib import _bench_v11, pooled_gate_passes  # noqa: E402

HOST_COORDS = ROOT / "data" / "sh0es_host_coordinates.json"
PARSED = ROOT / "data" / "sh0es_hosts_parsed.json"
SECTOR_SEED = ROOT / "predictions" / "sector_h0_seed.json"
NEBULA = ROOT / "data" / "nebula_lensing_cache.json"
FRB = ROOT / "data" / "frb_repeater_cache.json"
OUT = ROOT / "data" / "sh0es_ladder_chain_benchmark.json"
OUTCOME = ROOT / "results" / "sh0es_ladder_chain_outcome.json"

HOST_ALIASES = {
    "N1015": "NGC1015",
    "N1309": "NGC1309",
    "N1365": "NGC1365",
    "N1448": "NGC1448",
    "N2442": "NGC2442",
    "N3021": "NGC3021",
    "N3370": "NGC3370",
    "N3447": "NGC3447",
    "N3972": "NGC3972",
    "N3982": "NGC3982",
    "N4038": "NGC4038",
    "N4258": "NGC4258",
    "N4424": "NGC4424",
    "N4536": "NGC4536",
    "N4639": "NGC4639",
    "N5584": "NGC5584",
    "N5917": "NGC5917",
    "N7250": "NGC7250",
    "U9391": "UGC9391",
}


def _err(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def _counts() -> dict[str, int]:
    out: dict[str, int] = {}
    if not PARSED.is_file():
        return out
    for row in json.loads(PARSED.read_text(encoding="utf-8")):
        n = int(row.get("cepheid_count") or 0)
        for key in (
            str(row.get("canonical_name") or ""),
            HOST_ALIASES.get(str(row.get("host") or ""), ""),
            str(row.get("host") or ""),
        ):
            if key:
                out[key] = max(out.get(key, 0), n)
    return out


def main() -> int:
    seed = json.loads(SECTOR_SEED.read_text(encoding="utf-8"))
    h0_global = float(seed.get("h0_global_fsot") or 68.44005682979427)
    bleed = float(seed.get("bubble_bleed_fraction") or 0.015431)
    sh0es_lit = float(
        next(s["measured_h0"] for s in seed["sectors"] if s["name"] == "sh0es_hst_cepheid")
    )
    freedman_lit = float(
        next(s["measured_h0"] for s in seed["sectors"] if s["name"] == "freedman_jwst")
    )
    class_rho = float(
        next(s["bubble_density_proxy"] for s in seed["sectors"] if s["name"] == "sh0es_hst_cepheid")
    )
    class_h0 = h0_global * (1.0 + class_rho * bleed)
    cepheid_seed = float(
        next(s["bubble_density_proxy"] for s in seed["sectors"] if s["name"] == "sh0es_jwst")
    )

    nebulae = json.loads(NEBULA.read_text(encoding="utf-8")).get("nebulae") or []
    frbs = json.loads(FRB.read_text(encoding="utf-8")).get("frbs") or []
    hosts = json.loads(HOST_COORDS.read_text(encoding="utf-8")).get("hosts") or []
    counts = _counts()
    mod, authority = load_fsot_compute()

    objects = []
    for row in hosts:
        name = str(row["name"])
        ra = float(row["ra_deg"])
        dec = float(row["dec_deg"])
        method = str(row.get("method") or "SH0ES_Cepheid")
        sky = local_sky_density(ra, dec, nebulae, frbs, mod=mod)
        rho, kind = ladder_object_density_model(
            method, sky, mod, cepheid_class_seed=cepheid_seed
        )
        h0 = h0_global * (1.0 + float(rho) * bleed)
        n = counts.get(name, 1) or 1
        objects.append(
            {
                "host": name,
                "method": method,
                "kind": kind,
                "ra_deg": ra,
                "dec_deg": dec,
                "density_sky": round(float(sky), 6),
                "density_model": round(float(rho), 6),
                "fsot_h0": round(float(h0), 6),
                "cepheid_count": int(n),
            }
        )

    chain = ladder_chain_h0(objects, h0_global=h0_global, bleed_frac=bleed)
    h0_chain = float(chain["h0_chain"])
    h0_anc = float(chain["h0_anchors_only"])
    h0_host = float(chain["h0_hosts_only"])

    records = [
        {
            "lab": "sh0es_ladder_chain_lab",
            "property": "published_h0",
            "name": "SH0ES_R22_ladder_chain",
            "computed": round(h0_chain, 6),
            "measured": sh0es_lit,
            "error_pct": round(_err(h0_chain, sh0es_lit), 6),
            "eval_kind": "fsot_prediction",
            "record_kind": "scalar",
            "unit": "km/s/Mpc",
            "note": "Cepheid-count weighted mixture of anchor + host FSOT H0. Not a ρ retune.",
        },
        {
            "lab": "sh0es_ladder_chain_lab",
            "property": "anchor_rung_h0",
            "name": "SH0ES_geometric_anchors_vs_Freedman",
            "computed": round(h0_anc, 6),
            "measured": freedman_lit,
            "error_pct": round(_err(h0_anc, freedman_lit), 6),
            "eval_kind": "fsot_prediction",
            "record_kind": "scalar",
            "unit": "km/s/Mpc",
            "note": "LMC+NGC4258 count-weighted vs Freedman JWST TRGB (same mild sector).",
        },
    ]

    doc = _bench_v11(
        domain="SH0ES_Ladder_Chain",
        material_records=records,
        maps_to_lean=["cosmological", "blackhole", "astronomy"],
        d_eff=20,
        authority_path=str(authority).replace("\\", "/"),
        source=[
            "data/sh0es_host_coordinates.json",
            "data/sh0es_hosts_parsed.json",
            "predictions/sector_h0_seed.json",
            "data/nebula_lensing_cache.json",
            "data/frb_repeater_cache.json",
            "Riess+2022 SH0ES public Cepheid counts",
        ],
        channel_stats=[("fsot_prediction", "ladder_chain", [float(r["error_pct"]) for r in records])],
        sota_baselines={
            "ladder_chain": {
                "sota_typical_error_pct": 1.0,
                "sota_model": "Single class-bin ρ=5.05 (73.773 vs 73.04)",
            }
        },
    )
    doc["tier"] = 51
    doc["policy"] = "do_not_retune_frozen_class_rho"
    doc["h0_global_fsot"] = h0_global
    doc["bubble_bleed_fraction"] = bleed
    doc["objects"] = objects
    doc["chain"] = chain
    doc["class_bin_h0"] = round(class_h0, 6)
    doc["class_bin_error_pct"] = round(_err(class_h0, sh0es_lit), 6)
    doc["sh0es_status"] = (
        "GREEN" if pooled_gate_passes(doc.get("pooled_median_error_pct")) else "YELLOW"
    )
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    outcome = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "prediction_left_frozen": "predictions/sector_h0_seed.json sh0es_hst_cepheid ρ=5.05",
        "measured": {"SH0ES_R22": sh0es_lit, "Freedman_JWST_TRGB": freedman_lit},
        "computed": {
            "ladder_chain": round(h0_chain, 6),
            "anchors_only": round(h0_anc, 6),
            "hosts_only": round(h0_host, 6),
            "class_bin": round(class_h0, 6),
        },
        "error_pct": {
            "ladder_chain_vs_SH0ES": round(_err(h0_chain, sh0es_lit), 6),
            "anchors_vs_Freedman": round(_err(h0_anc, freedman_lit), 6),
            "class_bin_vs_SH0ES": round(_err(class_h0, sh0es_lit), 6),
        },
        "interface": "local_sky_density + ladder_object_density_model + cepheid_count weights",
        "kill": "ladder_chain median > 0.5% on refresh, or class rho retuned to hit 73.04",
    }
    OUTCOME.parent.mkdir(parents=True, exist_ok=True)
    OUTCOME.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUTCOME}")
    print(
        f"  chain={h0_chain:.3f} vs {sh0es_lit} ({_err(h0_chain, sh0es_lit):.3f}%)  "
        f"anchors={h0_anc:.3f} vs {freedman_lit} ({_err(h0_anc, freedman_lit):.3f}%)  "
        f"class={class_h0:.3f} ({_err(class_h0, sh0es_lit):.3f}%)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
