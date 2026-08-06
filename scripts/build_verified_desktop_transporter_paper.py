#!/usr/bin/env python3
"""Standalone supplementary volume for the transporter simulation stack (not main thesis)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "VERIFIED_DESKTOP_TRANSPORTER.md"
BENCH = ROOT / "data" / "star_trek_transporter_live_panel_benchmark.json"
PREREG = ROOT / "predictions" / "preregistered_predictions_manifest.yaml"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _transporter_preds() -> list[dict]:
    try:
        import yaml

        doc = yaml.safe_load(PREREG.read_text(encoding="utf-8")) or {}
        return [
            p
            for p in doc.get("predictions") or []
            if "transporter" in (p.get("name") or "").lower()
            or p.get("id", "") in {"PRED-036", "PRED-037", "PRED-038", "PRED-039", "PRED-040", "PRED-041"}
        ]
    except Exception:
        return []


def build(ts: str) -> str:
    bench = _load_json(BENCH)
    preds = _transporter_preds()
    pooled = bench.get("pooled_median_error_pct", "?")
    records = bench.get("record_count", "?")

    lines = [
        "# FSOT Verified Desktop — Transporter Simulation Stack",
        "",
        f"*Supplementary engineering volume · {ts} · "
        "[Return to main thesis](../README.md#viii-engineering-demonstrations)",
        "",
        "> **Scope note:** This document describes a **simulation-tier engineering stack**, not a claim "
        "that FSOT has demonstrated physical teleportation. The panel lives in the verification architecture "
        "as an extension of seed-scalar readouts across information-theory and quantum-channel proxies. "
        "It is **deliberately excluded from the main README** to keep the primary preprint focused on "
        "cross-domain empirical and formal proof.",
        "",
        "## 1. What this volume is",
        "",
        "The **Star Trek Transporter Live Panel** (`Star_Trek_Transporter_Live_Panel`) is a multi-layer "
        "desktop simulator that tests whether the same seed-derived scalar engine can coordinate "
        "engineering observables across:",
        "",
        "- Quantum information channel proxies",
        "- Pattern-buffer and scan-resolution engineering metrics",
        "- Portal / traverse scalar readouts",
        "- Beam-forming and acoustic-valve hardware simulators",
        "- Two-gate entanglement closure",
        "",
        "Lean module: `FSOT.Formal.StarTrekTransporterLivePanelPriors`",
        "",
        "## 2. Headline metrics (live benchmark)",
        "",
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Records | {records} |",
        f"| Pooled median error | {pooled}% |",
        f"| Benchmark | `data/star_trek_transporter_live_panel_benchmark.json` |",
        f"| Figure | `data/figures/verified_desktop_transporter.png` |",
        "",
        "![Verified desktop transporter stack](../data/figures/verified_desktop_transporter.png)",
        "",
        "## 3. Eleven-layer stack (simulation)",
        "",
        "1. Quantum channel  \n2. Information theory  \n3. Poof/suction portal  \n4. Transporter engineering  \n"
        "5. Warp actuation  \n6. Black-hole / white-hole portal crosswalk  \n7. Beam-forming grid  \n"
        "8. T3 acoustic scan valve  \n9. Pad A hardware  \n10. Pad B receiver  \n11. Two-gate entanglement  ",
        "",
        "Simulators: `vendor/verified_desktop/star_trek_transporter/`",
        "",
        "## 4. Preregistered predictions (transporter subset)",
        "",
        "| ID | Name | FSOT branch | Discriminant |",
        "|----|------|-------------|--------------|",
    ]
    for p in preds:
        lines.append(
            f"| {p.get('id', '')} | {p.get('name', '')} | `{p.get('fsot_formula_branch', '')}` | "
            f"{p.get('discriminant', '')} |"
        )
    if not preds:
        lines.append("| PRED-036–041 | transporter stack channels | various | see prereg manifest |")

    lines.extend([
        "",
        "Full registry: `predictions/preregistered_predictions_manifest.yaml`",
        "",
        "## 5. Reproduction",
        "",
        "```bash",
        "python scripts/reproduce_domain_panel.py --panel Star_Trek_Transporter_Live_Panel --deep",
        "python scripts/build_verified_desktop_transporter_figure.py",
        "python vendor/verified_desktop/star_trek_transporter/pattern_buffer_beam_simulator.py --deep",
        "python vendor/verified_desktop/star_trek_transporter/two_gate_entanglement_simulator.py",
        "```",
        "",
        "Cross-proof closure (includes this panel among verified-desktop set):",
        "",
        "```bash",
        "python scripts/build_verified_desktop_cross_proof_closure.py",
        "```",
        "",
        "## 6. Relationship to the main thesis",
        "",
        "- **Main README (§VIII):** fuels, machine-and-molecule catalog, black-hole / white-hole cycle — "
        "engineering demos with direct thermochemistry / catalog anchors.",
        "- **This volume:** speculative propulsion / information-transport **simulation** kept in-repo for "
        "completeness and preregistration integrity.",
        "- **Appendix XII:** panel still listed under Engineering cluster; detail remains in chapter "
        "`06_engineering_propulsion.md`.",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(ts), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())