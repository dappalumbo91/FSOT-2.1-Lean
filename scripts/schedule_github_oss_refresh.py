#!/usr/bin/env python3
"""Scheduled GitHub OSS snapshot refresh — re-fetch stale samples and rebuild Tier 44."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE = ROOT / "data" / "github_oss_refresh_schedule.yaml"
LOG_PATH = ROOT / "data" / "github_oss_refresh_log.json"


def _load_schedule() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(SCHEDULE.read_text(encoding="utf-8"))


def _summary_mtime(spec: dict) -> float | None:
    rel = spec.get("ingest", {}).get("summary_vendor") or "vendor/github_oss/github_oss_code_genome_summary.json"
    path = ROOT / rel
    if not path.is_file():
        return None
    return path.stat().st_mtime


def _is_stale(spec: dict, *, force: bool) -> tuple[bool, str]:
    if force:
        return True, "forced_refresh"
    if not spec.get("enabled", True):
        return False, "schedule_disabled"
    cadence = int(spec.get("cadence_days") or 7)
    mtime = _summary_mtime(spec)
    if mtime is None:
        return True, "missing_summary"
    age_days = (datetime.now(timezone.utc).timestamp() - mtime) / 86400.0
    if age_days >= cadence:
        return True, f"stale_{age_days:.1f}d"
    return False, f"fresh_{age_days:.1f}d"


def _run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:] if proc.stdout else "",
        "stderr_tail": proc.stderr[-1000:] if proc.stderr else "",
    }


def refresh(*, force: bool = False, skip_rebuild: bool = False) -> dict:
    spec = _load_schedule()
    stale, reason = _is_stale(spec, force=force)
    result: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stale": stale,
        "reason": reason,
        "cadence_days": spec.get("cadence_days"),
        "steps": [],
    }
    if not stale:
        result["status"] = "skipped"
        LOG_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    ingest_script = spec.get("ingest", {}).get("script") or "scripts/ingest_github_oss_code_genome.py"
    ingest_cmd = [sys.executable, str(ROOT / ingest_script)]
    if force:
        ingest_cmd.append("--refresh")
    step = _run(ingest_cmd)
    result["steps"].append(step)
    if step["returncode"] != 0:
        result["status"] = "ingest_failed"
        LOG_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    if not skip_rebuild:
        for rel in spec.get("rebuild_pipeline") or []:
            step = _run([sys.executable, str(ROOT / rel)])
            result["steps"].append(step)
            if step["returncode"] != 0:
                result["status"] = "rebuild_failed"
                LOG_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
                return result

    result["status"] = "ok"
    LOG_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh GitHub OSS snapshots on cadence")
    parser.add_argument("--refresh", action="store_true", help="Force re-fetch all samples")
    parser.add_argument("--skip-rebuild", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        spec = _load_schedule()
        stale, reason = _is_stale(spec, force=args.refresh)
        print(json.dumps({"stale": stale, "reason": reason, "cadence_days": spec.get("cadence_days")}, indent=2))
        return 0
    result = refresh(force=args.refresh, skip_rebuild=args.skip_rebuild)
    print(json.dumps({"status": result.get("status"), "reason": result.get("reason"), "steps": len(result.get("steps", []))}, indent=2))
    return 0 if result.get("status") in ("ok", "skipped") else 1


if __name__ == "__main__":
    raise SystemExit(main())