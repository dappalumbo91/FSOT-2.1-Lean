#!/usr/bin/env python3
"""Audit Living FSOT hardware stack — QEMU trinary body + Rust mind gym (not ESP32)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "living_fsot_hardware_verification_report.json"

sys.path.insert(0, str(ROOT / "scripts"))
from living_fsot_lib import (  # noqa: E402
    canonical_k,
    k_parity_check,
    living_paths,
    load_json,
    qemu_available,
    resolve_living_root,
)


def _artifact_checks(paths: dict[str, Path]) -> dict:
    body = paths.get("trinary_body")
    mind = paths.get("mind_rust")
    state = paths.get("habitat_state")
    checks: dict[str, dict] = {}

    if body:
        kernel = body / "target/x86_64-unknown-none/debug/fsot_body_kernel"
        uefi = body / "target/body_image/fsot_body_uefi.img"
        bridge = body / "target/release/mind_bridge.exe"
        checks["kernel_elf"] = {"path": str(kernel), "exists": kernel.exists()}
        checks["uefi_image"] = {"path": str(uefi), "exists": uefi.exists(), "size_bytes": uefi.stat().st_size if uefi.exists() else 0}
        checks["mind_bridge_exe"] = {"path": str(bridge), "exists": bridge.exists()}
        checks["host_probe_script"] = {"path": str(body / "scripts/run_host.ps1"), "exists": (body / "scripts/run_host.ps1").exists()}
        checks["qemu_serial_script"] = {"path": str(body / "scripts/run_qemu_serial.ps1"), "exists": (body / "scripts/run_qemu_serial.ps1").exists()}

    if mind:
        checks["fsot_living_exe"] = {
            "path": str(mind / "target/release/fsot-living.exe"),
            "exists": (mind / "target/release/fsot-living.exe").exists(),
        }
        checks["scalar_rs"] = {
            "path": str(mind / "src/scalar.rs"),
            "exists": (mind / "src/scalar.rs").exists(),
        }

    if state:
        for name in ("LIVE_STATUS.json", "BODY_STATUS.json", "BENCHMARK_REPORT.json"):
            p = state / name
            checks[name] = {"path": str(p), "exists": p.exists()}

    return checks


def _live_operational(state_dir: Path) -> dict:
    live = load_json(state_dir / "LIVE_STATUS.json") or {}
    body = load_json(state_dir / "BODY_STATUS.json") or {}
    bench = load_json(state_dir / "BENCHMARK_REPORT.json") or {}

    hero = live.get("hero") or {}
    return {
        "body_online": bool(live.get("body_online")),
        "body_transport": live.get("body_transport") or body.get("transport"),
        "body_tick": live.get("body_tick") or body.get("tick"),
        "habitat_tick": live.get("tick"),
        "generation": live.get("generation"),
        "genome_fp_match": (
            str(live.get("body_genome_fp") or "") == str(body.get("genome_fp") or "")
            if live.get("body_genome_fp") and body.get("genome_fp")
            else None
        ),
        "hero_raw_s": hero.get("raw_s"),
        "hero_d_eff": hero.get("d_eff"),
        "hero_delta_psi": hero.get("delta_psi"),
        "benchmark_pass_rate": bench.get("pass_rate"),
        "benchmark_n_pass": bench.get("n_pass"),
        "benchmark_n_total": bench.get("n_total"),
        "capabilities_fsot_scalar": (live.get("capabilities") or {}).get("fsot_scalar"),
    }


def build(living_root: Path | None) -> dict:
    if not living_root:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "version": "1.0",
            "tier": "93_living_fsot_hardware",
            "overall_ok": False,
            "project_found": False,
            "reason": "Living FSOT root not found — set data/living_fsot_project_manifest.yaml default_root",
        }

    paths = living_paths(living_root)
    artifacts = _artifact_checks(paths)
    qemu_ok, qemu_path = qemu_available()
    k_check = k_parity_check()

    state = paths.get("habitat_state")
    live_ops = _live_operational(state) if state and state.exists() else {}

    components_ok = all(
        paths.get(k, Path("__missing__")).exists()
        for k in ("mind_rust", "trinary_body", "habitat_state")
    )
    build_artifacts_ok = (
        artifacts.get("kernel_elf", {}).get("exists")
        and artifacts.get("uefi_image", {}).get("exists")
        and artifacts.get("scalar_rs", {}).get("exists")
    )
    scalar_k_ok = bool(k_check.get("ok"))
    live_evidence_ok = bool(
        live_ops.get("body_online")
        or (live_ops.get("body_tick") or 0) > 0
        or artifacts.get("BODY_STATUS.json", {}).get("exists")
    )
    benchmark_ok = (
        live_ops.get("benchmark_pass_rate") == 1.0
        or live_ops.get("benchmark_n_pass") == live_ops.get("benchmark_n_total")
        if live_ops.get("benchmark_n_total")
        else True
    )

    checks_passed = {
        "project_layout": components_ok,
        "build_artifacts": build_artifacts_ok,
        "scalar_k_parity": scalar_k_ok,
        "live_or_export_evidence": live_evidence_ok,
        "task_battery_green": benchmark_ok,
        "qemu_runtime_available": qemu_ok,
    }
    core_ok = all(
        checks_passed[k]
        for k in (
            "project_layout",
            "build_artifacts",
            "scalar_k_parity",
            "live_or_export_evidence",
        )
    )
    overall_ok = core_ok and benchmark_ok

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "tier": "93_living_fsot_hardware",
        "overall_ok": overall_ok,
        "project_found": True,
        "living_root": str(living_root),
        "components": {k: str(v) for k, v in paths.items() if k != "root"},
        "checks_passed": checks_passed,
        "artifacts": artifacts,
        "qemu": {"available": qemu_ok, "path": qemu_path},
        "scalar_k_parity": k_check,
        "canonical_k": canonical_k(),
        "live_operational": live_ops,
        "scope": {
            "includes": [
                "fsot-trinary-body UEFI/QEMU bare-metal kernel",
                "fsot-living-rust mind gym + Scalar.lean port",
                "Mind ABI TCP/file bridge (BODY_STATUS / BODY_MOTOR)",
                "Closed-loop habitat state exports",
            ],
            "excludes": [
                "ESP32 RF observer serial harness (Tier 91 eight_way — deferred)",
                "Full 1331-obligation spine on metal",
            ],
        },
        "milestones_claimed": "M0–M12 per fsot-trinary-body/docs/ARCHITECTURE.md",
        "integration_note": (
            "Living FSOT is the QEMU-level hardware verification path. "
            "Lean cross-proof still triangulates numeric obligations; this audit "
            "verifies body build artifacts, scalar k parity, and live mind↔body loop."
        ),
        "remedy_if_fail": "Build fsot-trinary-body kernel+UEFI; run fsot-living-rust with body_bridge; refresh habitat exports",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Living FSOT hardware verification audit")
    parser.add_argument("--root", type=str, default=None, help="Override living FSOT project root")
    args = parser.parse_args()

    living_root = resolve_living_root(args.root)
    doc = build(living_root)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("LIVING FSOT HARDWARE AUDIT (Tier 93)")
    print(f"  project_found: {doc.get('project_found')}")
    print(f"  overall_ok: {doc.get('overall_ok')}")
    if doc.get("checks_passed"):
        for k, v in doc["checks_passed"].items():
            print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"Wrote {OUT}")
    return 0 if doc.get("overall_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())