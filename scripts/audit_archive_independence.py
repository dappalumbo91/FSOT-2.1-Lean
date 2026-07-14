#!/usr/bin/env python3
"""Audit that the I: physical archive does not depend on C: Desktop for verification."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "archive_independence_audit.json"
DESKTOP_PAT = re.compile(r"C:[/\\]Users[/\\]damia[/\\]Desktop", re.I)
SKIP = {
    "desktop_project_crosswalk.json",
    "fsot_20_domain_crosswalk.json",
    "archive_independence_audit.json",
}


def _scan_file(path: Path) -> list[str]:
    if path.name in SKIP:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    issues = []
    for i, line in enumerate(text.splitlines(), 1):
        if DESKTOP_PAT.search(line):
            issues.append(f"{path.relative_to(ROOT)}:{i}")
    return issues[:5]


def main() -> int:
    from fsot_paths import canonical_archive_mode, fsot_compute_path  # noqa: WPS433

    issues: list[str] = []
    if not canonical_archive_mode():
        issues.append("not running from I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full")

    compute = fsot_compute_path()
    if "desktop" in str(compute).lower():
        issues.append(f"fsot_compute resolves to Desktop: {compute}")

    # authority_path in benchmarks is critical
    critical = []
    for path in (ROOT / "data").glob("*_benchmark.json"):
        if path.name in SKIP:
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        ap = doc.get("authority_path")
        if isinstance(ap, str) and DESKTOP_PAT.search(ap):
            critical.append(str(path.relative_to(ROOT)))

    report = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "canonical_hub": str(Path(r"I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full")),
        "ok": not issues and not critical,
        "fsot_compute_path": str(compute),
        "canonical_archive_mode": canonical_archive_mode(),
        "critical_authority_path_desktop": critical[:50],
        "critical_count": len(critical),
        "other_desktop_refs": issues[:100],
        "policy": "I:/FSOT-Physical-Archive is the definitive hub synced to GitHub; C: Desktop is legacy only.",
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())