#!/usr/bin/env python3
"""
Verified desktop panels — Python oracle + Lean obligation prep for five-prover cross-proof.

Regenerates Lean priors, exports obligations into full_formal_spine, and triangulates
benchmark scalars against fsot_compute.py before Coq/Isabelle/F*/Rust replay.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "verified_desktop_cross_proof_closure.json"
PY = sys.executable
SCRIPTS = ROOT / "scripts"

PANELS = (
    "Machine_And_Molecule_Live_Panel",
    "Fuel_Lab_Live_Panel",
    "BlackHole_WhiteHole_Cycle_Live_Panel",
    "Star_Trek_Transporter_Live_Panel",
)

LEAN_MODULE = {
    "Machine_And_Molecule_Live_Panel": "MachineAndMoleculeLivePanelPriors",
    "Fuel_Lab_Live_Panel": "FuelLabLivePanelPriors",
    "BlackHole_WhiteHole_Cycle_Live_Panel": "BlackHoleWhiteholeCycleLivePanelPriors",
    "Star_Trek_Transporter_Live_Panel": "StarTrekTransporterLivePanelPriors",
}

BENCH_SLUG = {
    "Machine_And_Molecule_Live_Panel": "machine_and_molecule_live_panel",
    "Fuel_Lab_Live_Panel": "fuel_lab_live_panel",
    "BlackHole_WhiteHole_Cycle_Live_Panel": "blackhole_whitehole_cycle_live_panel",
    "Star_Trek_Transporter_Live_Panel": "star_trek_transporter_live_panel",
}


def _run(script: str, *extra: str) -> None:
    subprocess.run([PY, str(SCRIPTS / script), *extra], cwd=str(ROOT), check=True)


def _oracle_sample(panel: str, bench: dict, *, limit: int = 12) -> list[dict]:
    from fsot_api_predict_lib import make_fsot_record  # noqa: WPS433

    rows: list[dict] = []
    for rec in bench.get("material_records") or []:
        if rec.get("eval_kind") == "cross_panel_relay":
            continue
        measured = rec.get("measured")
        if measured is None:
            continue
        replay = make_fsot_record(
            lab=str(rec.get("lab") or "verified_desktop"),
            property_name=str(rec.get("property") or "value"),
            name=str(rec.get("name") or "obs"),
            measured=float(measured),
            domain=str(rec.get("fsot_domain") or "Quantum_Mechanics"),
        )
        rows.append(
            {
                "name": rec.get("name"),
                "property": rec.get("property"),
                "stored_error_pct": float(rec.get("error_pct") or 0),
                "replay_error_pct": float(replay["error_pct"]),
                "delta_pct": abs(float(replay["error_pct"]) - float(rec.get("error_pct") or 0)),
                "ok": abs(float(replay["error_pct"]) - float(rec.get("error_pct") or 0)) < 1e-6,
            }
        )
        if len(rows) >= limit:
            break
    return rows


def _obligation_ids(lean_module: str) -> list[str]:
    spine = ROOT / "verification" / "obligations" / "full_formal_spine.json"
    if not spine.is_file():
        return []
    doc = json.loads(spine.read_text(encoding="utf-8"))
    return [
        ob["id"]
        for ob in doc.get("obligations") or []
        if ob.get("lean_module") == lean_module
    ]


def main() -> int:
    _run("gen_verified_desktop_lean.py")
    _run("export_full_formal_obligations.py")

    panel_rows: list[dict] = []
    oracle_ok = True
    for panel in PANELS:
        bench_path = ROOT / "data" / f"{BENCH_SLUG[panel]}_benchmark.json"
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        samples = _oracle_sample(panel, bench)
        panel_oracle_ok = all(s["ok"] for s in samples) if samples else False
        oracle_ok = oracle_ok and panel_oracle_ok
        mod = LEAN_MODULE[panel]
        panel_rows.append(
            {
                "panel": panel,
                "lean_module": f"FSOT.Formal.{mod}",
                "record_count": bench.get("record_count"),
                "pooled_median_error_pct": bench.get("pooled_median_error_pct"),
                "python_oracle_samples": samples,
                "python_oracle_ok": panel_oracle_ok,
                "cross_proof_obligation_ids": _obligation_ids(mod),
            }
        )

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "verdict": "VERIFIED_DESKTOP_CROSS_PROOF_READY" if oracle_ok else "PYTHON_ORACLE_MISMATCH",
        "panels": panel_rows,
        "frameworks": {
            "lean": "priors regenerated — norm_num bundle + anchor scalars",
            "python_oracle": "vendor/fsot_compute.py replay triangulation",
            "coq": "via run_cross_proof_verification.py → full_formal_coq chunks",
            "isabelle": "via run_cross_proof_verification.py → full_formal Isabelle",
            "fstar": "via run_cross_proof_verification.py → fstar_scalar_spec",
            "rust": "via run_cross_proof_verification.py → fsot_obligation_replay",
        },
        "full_cross_proof_command": "python scripts/run_cross_proof_verification.py",
        "reproduce_panel_command": "python scripts/reproduce_domain_panel.py --panel <Panel> --deep",
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  verdict: {doc['verdict']}")
    for row in panel_rows:
        print(
            f"  {row['panel']}: oracle={'OK' if row['python_oracle_ok'] else 'FAIL'} "
            f"obligations={len(row['cross_proof_obligation_ids'])}"
        )
    if not oracle_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())