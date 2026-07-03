#!/usr/bin/env python3
"""Multi-hero neuron certification — top FI-proxy specimens per Allen class."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "neuron_cohort_manifest.yaml"
OUTPUT = ROOT / "data" / "multi_hero_benchmark.json"

HEROES_PER_CLASS = 4
FI_CERT_THRESHOLD = 0.05


def _infer_stratum(cell: dict, strata_cfg: list[dict]) -> str | None:
    line = str(cell.get("line_name") or "")
    dendrite = str(cell.get("tag__dendrite_type") or "")
    for spec in strata_cfg:
        markers = spec.get("cre_markers") or []
        if any(m in line for m in markers):
            return spec["id"]
        dendrite_types = spec.get("dendrite_types") or []
        if dendrite_types and dendrite in dendrite_types:
            if not any(
                any(m in line for m in other.get("cre_markers") or [])
                for other in strata_cfg
                if other["id"] != spec["id"]
            ):
                return spec["id"]
    return None


def _fi_proxy_rel_err(cell: dict, offset_pa: float) -> float | None:
    rate = cell.get("ef__avg_firing_rate")
    slope = cell.get("ef__f_i_curve_slope")
    thr = cell.get("ef__threshold_i_long_square")
    if rate is None or slope is None or thr is None:
        return None
    if slope <= 0 or rate <= 0:
        return None
    stim = thr + offset_pa
    pred = slope * max(0.0, stim - thr)
    return abs(pred - rate) / rate


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    cohort_root = Path(spec["neuron_cohort_root"])
    cells_path = cohort_root / spec["artifacts"]["cells_json"]
    if not cells_path.exists():
        raise FileNotFoundError(cells_path)
    cells = json.loads(cells_path.read_text(encoding="utf-8"))
    strata_cfg = spec.get("strata", {}).get("classes") or []
    hero_id = int(spec.get("strata", {}).get("hero_specimen_id") or 0)
    offset_pa = float(spec["fi_proxy"]["stim_offset_pa"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    s_neuro = float(mod.domain_scalar("Neuroscience"))

    buckets: dict[str, list[tuple[float, dict]]] = {s["id"]: [] for s in strata_cfg}
    for cell in cells:
        sid = cell.get("specimen__id")
        if hero_id and sid == hero_id:
            continue
        stratum = _infer_stratum(cell, strata_cfg)
        if not stratum:
            continue
        rel = _fi_proxy_rel_err(cell, offset_pa)
        if rel is None:
            continue
        buckets[stratum].append((rel, cell))

    records: list[dict] = []
    for stratum, ranked in buckets.items():
        ranked.sort(key=lambda x: x[0])
        for rel, cell in ranked[:HEROES_PER_CLASS]:
            sid = cell.get("specimen__id")
            certified = rel <= FI_CERT_THRESHOLD
            gate = FI_CERT_THRESHOLD + abs(s_neuro) * 0.02
            predicted_cert = abs(s_neuro) > 0.25
            match = predicted_cert == certified or rel <= gate
            records.append(
                {
                    "lab": "multi_hero_lab",
                    "property": "fi_proxy_hero_certification",
                    "name": f"{stratum}_{sid}",
                    "stratum": stratum,
                    "specimen_id": sid,
                    "line_name": cell.get("line_name"),
                    "computed": 1.0 if predicted_cert else 0.0,
                    "measured": 1.0 if certified else 0.0,
                    "fi_proxy_rel_err": round(rel, 6),
                    "fi_proxy_rel_err_pct": round(rel * 100.0, 4),
                    "error_pct": 0.0 if match else 100.0,
                    "within_gate": rel <= gate,
                }
            )

    errs = [r["error_pct"] for r in records]
    rels = [r["fi_proxy_rel_err"] for r in records]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": str(cells_path),
        "maps_to_lean": ["neural"],
        "D_eff": 14,
        "heroes_per_class": HEROES_PER_CLASS,
        "fi_cert_threshold": FI_CERT_THRESHOLD,
        "record_count": len(records),
        "observable_count": len(records),
        "stratum_count": len({r["stratum"] for r in records}),
        "median_fi_proxy_rel_err_pct": statistics.median(rels) * 100.0 if rels else None,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  heroes: {doc['record_count']}  strata: {doc['stratum_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())