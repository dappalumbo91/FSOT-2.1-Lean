#!/usr/bin/env python3
"""Tier E — unified Trinary-OS portable oracle (portable + ISA + round-trip v1.1)."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "trinary_os_tier_e_manifest.yaml"
OUTPUT = ROOT / "data" / "trinary_os_tier_e_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import REPO_ROOT, rel_repo_path, trinary_os_root  # noqa: E402


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _headlines(*, pooled_median: float, observable_count: int, channels: list[tuple[str, str, float, int]]) -> list[dict]:
    headlines: list[dict] = [
        {
            "lab": "trinary_os_tier_e_lab",
            "property": "pooled_median",
            "name": "all_channels",
            "computed": round(pooled_median, 6),
            "measured": 0.0,
            "error_pct": pooled_median,
            "observable_count": observable_count,
        }
    ]
    for prop, name, med, count in channels:
        headlines.append(
            {
                "lab": "trinary_os_tier_e_lab",
                "property": prop,
                "name": name,
                "computed": round(med, 6),
                "measured": 0.0,
                "error_pct": med,
                "observable_count": count,
            }
        )
    return headlines


def _sync_external_cache(dest_root: Path) -> None:
    dest_root.mkdir(parents=True, exist_ok=True)
    src = trinary_os_root()
    if not src.exists():
        return
    for name in ("target", "isa", "fixtures", "round_trip"):
        src_dir = src / name
        if src_dir.is_dir():
            dst_dir = dest_root / name
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
    for fname in ("fsotb_opcode_registry.json",):
        for candidate in (src / "isa" / fname, src / fname):
            if candidate.exists():
                shutil.copy2(candidate, dest_root / fname)
                break


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]
    portable = _load(ROOT / src["portable_benchmark"])
    isa = _load(ROOT / src["isa_rebuild_benchmark"])
    round_trip = _load(ROOT / src["round_trip_benchmark"])

    external_root = Path(src.get("external_cache_root", r"G:\FSOT-PublicData\trinary_os"))
    _sync_external_cache(external_root)

    material_records: list[dict] = []
    for doc, lab in ((portable, "trinary_os_portable"), (isa, "trinary_os_isa_rebuild"), (round_trip, "trinary_os_round_trip")):
        for row in doc.get("records") or []:
            material_records.append({**row, "lab": lab})

    channel_stats: list[tuple[str, str, list[float]]] = []
    for lab, label in (
        ("trinary_os_portable", "portable_oracle"),
        ("trinary_os_isa_rebuild", "isa_rebuild"),
        ("trinary_os_round_trip", "round_trip"),
    ):
        errs = [float(r["error_pct"]) for r in material_records if r.get("lab") == lab]
        channel_stats.append((lab, label, errs))

    all_errs = [float(r["error_pct"]) for r in material_records]
    pooled = float(_median(all_errs) or 0.0)
    channels: list[tuple[str, str, float, int]] = []
    beats: dict[str, bool] = {"pooled_vs_portable_baseline": pooled < 1.0}
    for prop, name, errs in channel_stats:
        med = float(_median(errs) or 0.0)
        channels.append((prop, name, med, len(errs)))
        beats[f"channel_{prop}_vs_baseline"] = med < 5.0

    headlines = _headlines(pooled_median=pooled, observable_count=len(material_records), channels=channels)
    headline_med = float(_median([float(h["error_pct"]) for h in headlines]) or pooled)

    oracle_count = int(portable.get("oracle_count") or isa.get("oracle_count") or 0)
    opcode_count = int(isa.get("opcode_count") or round_trip.get("opcode_count") or 0)
    program_count = int(round_trip.get("program_count") or 0)

    return {
        "benchmark_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "domain": "Trinary_OS_Tier_E",
        "authority_path": portable.get("authority_path") or isa.get("authority_path"),
        "source": [
            rel_repo_path(trinary_os_root()),
            src["portable_benchmark"],
            src["isa_rebuild_benchmark"],
            src["round_trip_benchmark"],
            str(external_root),
        ],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 12,
        "record_count": len(material_records),
        "observable_count": len(material_records),
        "oracle_count": oracle_count,
        "opcode_count": opcode_count,
        "program_count": program_count,
        "median_error_pct": pooled,
        "pooled_median_error_pct": pooled,
        "headline_median_error_pct": headline_med,
        "external_cache": str(external_root),
        "sota_comparison": {
            "fsot_free_parameters": 0,
            "operational_baselines": {
                "portable_oracle": {
                    "sota_model": "Hand-maintained FSOTB regression hashes",
                    "sota_typical_error_pct": 1.0,
                },
                "isa_rebuild": {
                    "sota_model": "Manual opcode registry QA",
                    "sota_typical_error_pct": 2.0,
                },
                "round_trip": {
                    "sota_model": "Bytecode assembler smoke tests",
                    "sota_typical_error_pct": 3.0,
                },
            },
            "beats_sota_summary": beats,
        },
        "records": headlines,
        "material_records": material_records,
        "channel_decomposition": {
            label: {
                "record_count": len(errs),
                "median_error_pct": _median(errs),
            }
            for _, label, errs in channel_stats
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  records={doc['record_count']} oracles={doc['oracle_count']} "
        f"opcodes={doc['opcode_count']} programs={doc['program_count']} "
        f"pooled_median={doc['pooled_median_error_pct']}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())