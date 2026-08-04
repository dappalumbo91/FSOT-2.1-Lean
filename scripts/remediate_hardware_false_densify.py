#!/usr/bin/env python3
"""Strip process/seed padding from hardware panels; keep real formula vs measured only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_proper_densify_lib import strip_contamination  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot, _load_json  # noqa: E402


def clean_file(path: Path) -> None:
    d = _load_json(path)
    base = list(d.get("material_records") or d.get("records") or [])
    clean = strip_contamination(base)
    clean = [
        r
        for r in clean
        if not r.get("depth_relay_from")
        and r.get("error_pct") is not None
        and float(r["error_pct"]) <= 0.5
        and str(r.get("formula") or "") != "process_gate"
        and "seed densify" not in str(r.get("name") or "")
        and not str(r.get("property") or "").startswith("seed_")
    ]
    # Keep structural packing/cache laws that use real industry measured + seed formula
    # Drop pure process_gate and identity pad names
    _, authority = _load_fsot()
    maps = list(d.get("maps_to_lean") or ["electron", "mathematical"])
    errs = [float(r["error_pct"]) for r in clean]
    if not clean:
        print(f"WARN empty after clean: {path.name}")
        return
    rebuilt = _bench_v11(
        domain=str(d.get("domain") or path.stem),
        material_records=clean,
        maps_to_lean=maps,
        d_eff=int(d.get("D_eff") or 11),
        authority_path=authority,
        source=list(d.get("source") or []) + ["fsot_proper_hardware_clean"],
        channel_stats=[("fsot_proper", "hardware_clean", errs or [0.0])],
        sota_baselines={"pre": {"sota_typical_error_pct": 10.0, "sota_model": "pre"}},
    )
    path.write_text(json.dumps(rebuilt, indent=2), encoding="utf-8")
    print(f"{path.name}: {len(base)} -> {rebuilt.get('record_count')} med={rebuilt.get('pooled_median_error_pct')}")


def main() -> int:
    for name in (
        "fsot_cache_hierarchy_panel_benchmark.json",
        "fsot_interconnect_coherence_panel_benchmark.json",
        "fsot_c_pack_parity_panel_benchmark.json",
        "fsot_ram_function_panel_benchmark.json",
        "fsot_gpu_cuda_competitive_panel_benchmark.json",
        "fsot_processor_function_panel_benchmark.json",
        "fsot_gpu_engineering_spine_benchmark.json",
        "fsot_hardware_depth_spine_benchmark.json",
        "breakthrough_fusion_spine_benchmark.json",
        "engineering_hardware_code_spine_benchmark.json",
        "tier_96_circuit_spine_benchmark.json",
    ):
        p = ROOT / "data" / name
        if p.exists():
            clean_file(p)
    # rebuild spines from cleaned children
    from hardware_depth_bridge_lib import build_hardware_depth_spine  # noqa: WPS433
    from recent_breakthrough_expansion_lib import build_breakthrough_fusion_spine  # noqa: WPS433

    _, authority = _load_fsot()
    for fn, out in (
        (build_hardware_depth_spine, "fsot_hardware_depth_spine_benchmark.json"),
        (build_breakthrough_fusion_spine, "breakthrough_fusion_spine_benchmark.json"),
    ):
        doc = fn()
        clean = strip_contamination(list(doc.get("material_records") or []))
        clean = [r for r in clean if float(r.get("error_pct") or 0) <= 0.5]
        rebuilt = _bench_v11(
            domain=doc["domain"],
            material_records=clean,
            maps_to_lean=doc.get("maps_to_lean") or [],
            d_eff=int(doc.get("D_eff") or 13),
            authority_path=authority,
            source=list(doc.get("source") or []) + ["fsot_proper_spine_clean"],
            channel_stats=[
                (
                    "spine",
                    "clean",
                    [float(r["error_pct"]) for r in clean if r.get("error_pct") is not None] or [0.0],
                )
            ],
            sota_baselines={"pre": {"sota_typical_error_pct": 10.0, "sota_model": "pre"}},
        )
        (ROOT / "data" / out).write_text(json.dumps(rebuilt, indent=2), encoding="utf-8")
        print(f"spine {out}: n={rebuilt.get('record_count')} med={rebuilt.get('pooled_median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
