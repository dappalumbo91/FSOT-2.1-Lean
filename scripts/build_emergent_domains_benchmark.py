#!/usr/bin/env python3
"""Bridge autonomous MC FSOT refiner → emergent domain observables."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "emergent_domains_manifest.yaml"
OUTPUT = ROOT / "data" / "emergent_domains_benchmark.json"


def _domain_rows(domains: list) -> list[dict]:
    out: list[dict] = []
    for row in domains:
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "name": row.get("name"),
                "D_eff": row.get("D_eff"),
                "delta_psi": row.get("delta_psi"),
                "observed": bool(row.get("observed")),
                "S_final": row.get("S_final"),
                "C_interpret": row.get("C_interpret"),
                "discovery_step": row.get("discovery_step"),
                "fertile_phases": row.get("fertile_phases"),
            }
        )
    return out


def build_benchmark(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    mc_root = Path(spec["source"]["mc_root"])
    summary_path = mc_root / spec["source"]["run_summary"]
    if not summary_path.exists():
        raise FileNotFoundError(f"MC summary missing: {summary_path}")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    domains = _domain_rows(summary.get("all_emergent_domains") or [])
    observed = [d for d in domains if d.get("observed")]
    d_eff_values = [int(d["D_eff"]) for d in domains if d.get("D_eff") is not None]
    s_finals = [float(d["S_final"]) for d in domains if d.get("S_final") is not None]

    refined_path = mc_root / spec["source"].get("refined_robust", "refined_robust_emergents.json")
    refined_count = 0
    if refined_path.exists():
        refined = json.loads(refined_path.read_text(encoding="utf-8"))
        if isinstance(refined, list):
            refined_count = len(refined)
        elif isinstance(refined, dict):
            refined_count = len(refined.get("domains") or refined.get("emergents") or [])

    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(mc_root),
        "emergent_domain_count": len(domains),
        "observed_domain_count": len(observed),
        "refined_robust_count": refined_count,
        "total_steps": summary.get("total_steps"),
        "total_proposals": summary.get("total_proposals"),
        "fertile_accept_rate": summary.get("fertile_accept_rate"),
        "final_meta_S": summary.get("final_meta_S"),
        "final_emergence_health": summary.get("final_emergence_health"),
        "sampling_bias_final_D": summary.get("sampling_bias_final_D"),
        "D_eff_min": min(d_eff_values) if d_eff_values else None,
        "D_eff_max": max(d_eff_values) if d_eff_values else None,
        "S_final_mean": sum(s_finals) / len(s_finals) if s_finals else None,
        "observable_count": len(domains),
        "emergent_domains": domains,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        bench = build_benchmark(args.manifest)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  emergent domains: {bench['emergent_domain_count']}  "
        f"observed: {bench['observed_domain_count']}  "
        f"health: {bench.get('final_emergence_health')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())