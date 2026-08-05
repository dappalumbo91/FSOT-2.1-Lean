#!/usr/bin/env python3
"""Build quantum-depth + trinary string-syntax residual panel for Reality OS."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_quantum_trinary_syntax import run_suite, suite_summary  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402

OUT = ROOT / "data" / "quantum_trinary_syntax_benchmark.json"
REPORT = ROOT / "data" / "quantum_trinary_syntax_research.json"


def main() -> int:
    _, authority = _load_fsot()
    rows = run_suite()
    summary = suite_summary(rows)
    errs = [float(r["error_pct"]) for r in rows if r.get("error_pct") is not None]
    doc = _bench_v11(
        domain="Quantum_Trinary_Syntax",
        material_records=rows,
        maps_to_lean=["quantum", "consciousness", "ai"],
        d_eff=11,
        authority_path=authority,
        source=[
            "vendor/fsot_quantum_trinary_syntax.py",
            "vendor/trinary_os/isa/fsotb_opcode_registry.json",
            "CHSH/Tsirelson/Bell literature structure",
            "existing quantum_* residual panels",
        ],
        channel_stats=[
            ("fsot_prediction", "quantum_depth", errs or [0.0]),
            ("seed_identity", "trinary_syntax", [0.0]),
        ],
        sota_baselines={
            "bell_tests": {"sota_typical_error_pct": 1.0, "sota_model": "CHSH experiment class"},
            "trinary_abi": {"sota_typical_error_pct": 5.0, "sota_model": "binary ISA baseline"},
        },
    )
    doc["generated_at"] = datetime.now(timezone.utc).isoformat()
    doc["summary_physics"] = summary
    doc["policy"] = "fsot_quantum_trinary_same_S"
    doc["ontology"] = summary["ontology"]
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    research = {
        "generated_at": doc["generated_at"],
        "version": "1.0",
        "benchmark": "data/quantum_trinary_syntax_benchmark.json",
        "module": "vendor/fsot_quantum_trinary_syntax.py",
        "summary": summary,
        "claims_allowed": [
            "CHSH classical / Tsirelson residual-gated under Quantum_Mechanics",
            "Bell entropy / EPR correlation structure under same residual law",
            "27 Metatron opcodes = 3³; 25 registers = D_eff ceiling",
            "sign(S) is the balanced trit of the reality string",
            "Trinary OS is the machine syntax of the fluid continuum — not a second physics",
        ],
        "claims_forbidden": [
            "New free parameters for entanglement",
            "Trinary OS uses different seeds than fsot_compute",
        ],
        "related_existing_panels": [
            "data/quantum_mechanics_entanglement_depth_panel_benchmark.json",
            "data/quantum_information_benchmark.json",
            "data/quantum_computing_math_depth_panel_benchmark.json",
            "data/trinary_os_tier_e_benchmark.json",
        ],
    }
    REPORT.write_text(json.dumps(research, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} n={doc.get('record_count')} pooled={doc.get('pooled_median_error_pct')}%")
    print(f"  string={summary['sample_reality_string']} opcodes={summary['opcodes']} regs={summary['register_count']}")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
