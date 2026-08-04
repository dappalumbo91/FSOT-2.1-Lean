#!/usr/bin/env python3
"""Strip identity/process densify; refill with seed formulas vs real measured data."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from c_thin_depth_lib import deepen_all_c_thin, remediate_contaminated_benchmark  # noqa: E402
from fsot_proper_densify_lib import is_contaminating_row, strip_contamination  # noqa: E402
from tier_gap_fill_lib import _load_json  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None

OUT = ROOT / "data" / "false_densify_remediation_report.json"

# High-contamination panels from densify campaigns — force FSOT recompute path
FORCE_REMEDIATE = [
    ("data/energy_lean_route_credibility_benchmark.json", "Thermodynamics", ["energy"]),
    ("data/fusion_lean_route_credibility_benchmark.json", "Particle_Physics", ["fusion", "particle"]),
    ("data/proton_lean_route_credibility_benchmark.json", "Particle_Physics", ["proton", "particle"]),
    ("data/nuclear_lean_route_credibility_benchmark.json", "Nuclear_Physics", ["nuclear", "particle"]),
    ("data/perceived_lean_route_credibility_benchmark.json", "Neuroscience", ["neural"]),
    ("data/observer_lean_route_credibility_benchmark.json", "Neuroscience", ["observer", "neural"]),
    ("data/consciousness_lean_route_credibility_benchmark.json", "Neuroscience", ["consciousness"]),
    ("data/binary_decoder_panel_benchmark.json", "Quantum_Computing", ["ai", "mathematical"]),
    ("data/bibliography_corpus_panel_benchmark.json", "Atomic_Physics", ["mathematical"]),
    ("data/neuroscience_fi_precision_benchmark.json", "Neuroscience", ["neural"]),
    ("data/h0_planck_benchmark.json", "Cosmology", ["cosmological"]),
    ("data/desi_wa_constraint_benchmark.json", "Cosmology", ["cosmological"]),
    ("data/higgs_branching_benchmark.json", "Particle_Physics", ["particle"]),
    ("data/evolution_operon_benchmark.json", "Biology", ["biology"]),
    ("data/open_science_seed_constants_benchmark.json", "Atomic_Physics", ["particle"]),
    ("data/desktop_observer_loop_panel_benchmark.json", "Neuroscience", ["consciousness", "observer"]),
    ("data/coding_structure_verifier_panel_benchmark.json", "Quantum_Computing", ["ai", "mathematical"]),
    ("data/schematic_netlist_intrinsic_panel_benchmark.json", "Electromagnetism", ["electron"]),
    ("data/qce_elm_fusion_edge_panel_benchmark.json", "Particle_Physics", ["fusion", "energy"]),
    ("data/recent_breakthroughs_expansion_panel_benchmark.json", "Particle_Physics", ["fusion", "energy"]),
]


def _scan_contamination() -> list[dict]:
    rows = []
    for p in (ROOT / "data").glob("*benchmark*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        recs = d.get("material_records") or d.get("records") or []
        bad = sum(1 for r in recs if is_contaminating_row(r) or r.get("depth_relay_from"))
        if bad:
            rows.append({"file": p.name, "bad": bad, "total": len(recs)})
    rows.sort(key=lambda x: -x["bad"])
    return rows


def main() -> int:
    before = _scan_contamination()
    actions: list[dict] = []

    # 1) Rebuild lean routes with proper densify
    try:
        from build_lean_route_credibility_expansion import main as lean_main  # noqa: WPS433

        lean_main()
        actions.append({"action": "rebuild_lean_routes", "ok": True})
    except Exception as e:
        actions.append({"action": "rebuild_lean_routes", "ok": False, "error": str(e)})

    # 2) Force remediate known bad densify panels
    for rel, domain, maps in FORCE_REMEDIATE:
        path = ROOT / rel
        try:
            actions.append(remediate_contaminated_benchmark(path, domain=domain, maps=maps))
        except Exception as e:
            actions.append({"path": rel, "status": "error", "error": str(e)})

    # 3) Extension manifest: strip + FSOT densify all that are thin OR contaminated
    if yaml is not None:
        man = ROOT / "data" / "extension_domains_manifest.yaml"
        ext = yaml.safe_load(man.read_text(encoding="utf-8")).get("extension_domains") or {}
        # deepen_all now uses proper densify; also force any with depth_relay
        depth = deepen_all_c_thin(ext)
        actions.append({"action": "deepen_all_c_thin", "results": len(depth), "sample": depth[:15]})
        # force remediate extension benches that still have depth_relay
        forced = 0
        for name, cfg in ext.items():
            bp = ROOT / cfg["benchmark_data"]
            if not bp.exists():
                continue
            b = _load_json(bp)
            recs = b.get("material_records") or []
            if any(r.get("depth_relay_from") or is_contaminating_row(r) for r in recs):
                maps = list(cfg.get("maps_to_lean") or ["particle"])
                domain = {
                    "particle": "Particle_Physics",
                    "energy": "Thermodynamics",
                    "neural": "Neuroscience",
                    "mathematical": "Atomic_Physics",
                    "electron": "Electromagnetism",
                    "biology": "Biology",
                    "fusion": "Particle_Physics",
                }.get(str(maps[0]).lower(), "Particle_Physics")
                actions.append(remediate_contaminated_benchmark(bp, domain=domain, maps=maps))
                forced += 1
                if forced >= 80:
                    break
        actions.append({"action": "extension_force_remediate", "count": forced})

    after = _scan_contamination()
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "fsot_proper_densify — seed formula / domain S vs real measured only",
        "contamination_files_before": len(before),
        "contamination_files_after": len(after),
        "top_before": before[:25],
        "top_after": after[:25],
        "actions": actions,
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  contaminated files: {len(before)} -> {len(after)}")
    print(f"  top remaining: {after[:8]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
