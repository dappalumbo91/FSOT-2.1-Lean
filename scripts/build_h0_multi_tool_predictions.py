#!/usr/bin/env python3
"""Multi-tool H0 predictions under FSOT BH→WH bubble-bleed theory.

FSOT does **not** predict a single H0 number for all instruments.
Each measurement system couples to a different information-flow / bubble-density
sector (early-universe depleted → local inflated). Predictions:

  H0_tool = H0_global_fsot * (1 + density_model * bubble_bleed_fraction)

Inputs:
  data/sector_h0_seed.json
  vendor/fsot_compute.py (pin D1D38A)

Outputs:
  data/h0_multi_tool_predictions.json
  data/publication/H0_MULTI_TOOL_PREDICTIONS.md
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
    sector_h0_density_model,
)
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

SEED = ROOT / "data" / "sector_h0_seed.json"
OUT_JSON = ROOT / "data" / "h0_multi_tool_predictions.json"
OUT_MD = ROOT / "data" / "publication" / "H0_MULTI_TOOL_PREDICTIONS.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _err_pct(c: float, m: float) -> float:
    if m == 0:
        return 0.0 if c == 0 else 100.0
    return abs(c - m) / abs(m) * 100.0


def build() -> dict:
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    mod, authority = load_fsot_compute()
    authority = str(authority).replace("\\", "/") if authority else "vendor/fsot_compute.py"
    h0_global = float(seed.get("h0_global_fsot") or 68.440056829794272)
    bleed = float(seed.get("bubble_bleed_fraction") or 0.015431)

    # Wave1 engine H0 (CMB-class formula target 67.4 in wave1 table)
    wave1_h0 = None
    try:
        for r in mod.wave1():
            if getattr(r, "name", "") == "H0":
                wave1_h0 = float(r.computed)
                break
    except Exception:
        pass

    tools = []
    for row in seed.get("sectors") or []:
        name = str(row.get("name") or "")
        density_seed = float(row.get("bubble_density_proxy") or 0.0)
        measured = float(row.get("measured_h0"))
        # Sky coupling: early CMB sectors use density as model directly (no sky inflation)
        if name in ("global_cmb_background", "planck_cmb_local") or row.get(
            "tool_class"
        ) in ("early_universe_cmb", "fsot_global"):
            density_model = density_seed
        else:
            density_sky = 0.0  # literature seed path; sky overlay is panel-specific
            density_model = sector_h0_density_model(
                name if name in {
                    "sh0es_jwst",
                    "freedman_jwst",
                    "fsot_document_local",
                    "carnegie_h0",
                } else "default",
                density_seed,
                density_sky,
                mod,
            )
            # For tools not in special-case names, density_model == density_seed
            if name not in {
                "sh0es_jwst",
                "freedman_jwst",
                "fsot_document_local",
                "carnegie_h0",
            }:
                density_model = density_seed

        predicted = h0_global * (1.0 + float(density_model) * bleed)
        err = _err_pct(predicted, measured)
        tools.append(
            {
                "id": f"H0-TOOL-{name}",
                "pred_id": f"PRED-H0-{name}",
                "name": name,
                "method": row.get("method"),
                "tool_class": row.get("tool_class"),
                "reference": row.get("reference"),
                "note": row.get("note"),
                "literature_anchor_h0": measured,
                "bubble_density_proxy": density_seed,
                "bubble_density_model": round(float(density_model), 6),
                "fsot_predicted_h0": round(predicted, 6),
                "error_vs_literature_pct": round(err, 6),
                "kill": (
                    f"next_{name}_central_outside_"
                    f"{H0_CONTESTED_TOLERANCE_PCT}pct_of_fsot_predicted"
                ),
                "unit": "km/s/Mpc",
            }
        )

    tools.sort(key=lambda t: t["fsot_predicted_h0"])

    by_class: dict[str, list] = {}
    for t in tools:
        by_class.setdefault(str(t.get("tool_class") or "other"), []).append(t["id"])

    doc = {
        "generated_at": _now(),
        "version": "2.0",
        "authority_path": authority,
        "authority_pin_prefix": "D1D38A",
        "theory": seed.get("theory")
        or {
            "mechanism": "black_hole_white_hole_bubble_bleed",
            "claim": (
                "H0 discrepancy across tools is bubble-bleed / information-flow "
                "sector structure, not a single wrong number."
            ),
        },
        "h0_global_fsot": h0_global,
        "wave1_engine_h0": wave1_h0,
        "bubble_bleed_fraction": bleed,
        "formula": "H0_tool = H0_global_fsot * (1 + density_model * bubble_bleed_fraction)",
        "contested_tolerance_pct": H0_CONTESTED_TOLERANCE_PCT,
        "tool_count": len(tools),
        "tools": tools,
        "tools_by_class": by_class,
        "span_km_s_mpc": {
            "min_fsot": min(t["fsot_predicted_h0"] for t in tools),
            "max_fsot": max(t["fsot_predicted_h0"] for t in tools),
            "min_literature": min(t["literature_anchor_h0"] for t in tools),
            "max_literature": max(t["literature_anchor_h0"] for t in tools),
        },
        "seed_path": "data/sector_h0_seed.json",
        "refresh": "python scripts/build_h0_multi_tool_predictions.py",
    }
    raw = json.dumps({k: v for k, v in doc.items() if k != "bundle_sha256"}, sort_keys=True).encode()
    doc["bundle_sha256"] = hashlib.sha256(raw).hexdigest()
    return doc


def write_md(doc: dict) -> None:
    lines = [
        "# Multi-tool H₀ predictions (BH→WH bubble bleed)",
        "",
        f"*Generated {doc.get('generated_at')} · pin D1D38A · {doc.get('tool_count')} tools*",
        "",
        "## Why not one number",
        "",
        str((doc.get("theory") or {}).get("claim") or ""),
        "",
        f"**Global FSOT H₀** = `{doc.get('h0_global_fsot')}` km/s/Mpc  ",
        f"**Bleed fraction** = `{doc.get('bubble_bleed_fraction')}`  ",
        f"**Formula** = `{doc.get('formula')}`",
        "",
        "Each row is a **separate preregistered prediction** for that measurement system.",
        "Kill criteria fire per tool — a SH0ES update does not retune Planck, and vice versa.",
        "",
        "## Predictions (sorted by FSOT H₀)",
        "",
        "| Tool | Class | Method | FSOT H₀ | Literature | Density | Err % |",
        "|------|-------|--------|--------:|-----------:|--------:|------:|",
    ]
    for t in doc.get("tools") or []:
        lines.append(
            f"| `{t['name']}` | {t.get('tool_class')} | {t.get('method')} | "
            f"**{t['fsot_predicted_h0']}** | {t['literature_anchor_h0']} | "
            f"{t['bubble_density_proxy']} | {t['error_vs_literature_pct']} |"
        )
    span = doc.get("span_km_s_mpc") or {}
    lines.extend(
        [
            "",
            f"FSOT span: **{span.get('min_fsot')} – {span.get('max_fsot')}** km/s/Mpc  ",
            f"Literature span: {span.get('min_literature')} – {span.get('max_literature')} km/s/Mpc",
            "",
            f"Bundle SHA-256: `{doc.get('bundle_sha256')}`",
            "",
            "Refresh: `python scripts/build_h0_multi_tool_predictions.py`",
            "",
            "Seed: `data/sector_h0_seed.json` · Physics: `scripts/bubble_bleed_physics.py`",
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
        f"  tools={doc['tool_count']} "
        f"span={doc['span_km_s_mpc']['min_fsot']}–{doc['span_km_s_mpc']['max_fsot']} "
        f"sha={doc['bundle_sha256'][:16]}…"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
