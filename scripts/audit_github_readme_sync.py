#!/usr/bin/env python3
"""
Cross-check I: archive hub vs GitHub origin for publication/README sync gaps.

Writes: data/publication/GITHUB_SYNC_AUDIT.json + GITHUB_SYNC_AUDIT.md
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "publication" / "GITHUB_SYNC_AUDIT.json"
OUT_MD = ROOT / "data" / "publication" / "GITHUB_SYNC_AUDIT.md"

# Paths that must match between archive and GitHub for thesis accuracy
KEY_ARTIFACTS = (
    "README.md",
    "data/publication_claims_manifest.json",
    "data/cross_proof_verification_report.json",
    "data/publication/domain_atlas.csv",
    "data/publication/domain_atlas.json",
    "data/fsot_domain_navigator.json",
    "data/verified_desktop_cross_proof_closure.json",
    "data/external_data_manifest.yaml",
    "data/api_requirements.yaml",
    "data/domain_citations/verified_desktop.bib",
    "docs/REPOSITORY_TECHNICAL_GUIDE.md",
)

BENCHMARK_PANELS = {
    "Star_Trek_Transporter_Live_Panel": "data/star_trek_transporter_live_panel_benchmark.json",
    "Fuel_Lab_Live_Panel": "data/fuel_lab_live_panel_benchmark.json",
    "Machine_And_Molecule_Live_Panel": "data/machine_and_molecule_live_panel_benchmark.json",
    "BlackHole_WhiteHole_Cycle_Live_Panel": "data/blackhole_whitehole_cycle_live_panel_benchmark.json",
}


def _git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=str(ROOT), text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        return ""


def _load(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".json"}:
        return json.loads(text)
    return text


def _local_modified() -> list[str]:
    out = _git("status", "--porcelain")
    return [line for line in out.splitlines() if line.strip()]


def _ahead_behind() -> dict:
    ahead = _git("rev-list", "--count", "origin/main..HEAD")
    behind = _git("rev-list", "--count", "HEAD..origin/main")
    return {
        "local_ahead": int(ahead) if ahead.isdigit() else 0,
        "local_behind": int(behind) if behind.isdigit() else 0,
        "local_head": _git("rev-parse", "--short", "HEAD"),
        "origin_head": _git("rev-parse", "--short", "origin/main"),
    }


def _claims_staleness() -> list[dict]:
    claims = _load(ROOT / "data/publication_claims_manifest.json") or {}
    panels_claims = {
        r.get("panel"): r.get("record_count")
        for r in (claims.get("verified_desktop_evidence") or {}).get("panels") or []
    }
    gaps = []
    for panel, bench_rel in BENCHMARK_PANELS.items():
        bench = _load(ROOT / bench_rel) or {}
        live = bench.get("record_count")
        claimed = panels_claims.get(panel)
        if live is not None and claimed is not None and live != claimed:
            gaps.append(
                {
                    "panel": panel,
                    "benchmark_records": live,
                    "claims_manifest_records": claimed,
                    "action": "python scripts/build_publication_claims_bundle.py",
                }
            )
    return gaps


def _untracked_publication() -> list[str]:
    rows = []
    for p in (ROOT / "data" / "publication").rglob("*"):
        if p.is_file() and _git("ls-files", "--error-unmatch", str(p.relative_to(ROOT)).replace("\\", "/")) == "":
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            if _git("status", "--porcelain", rel):
                rows.append(rel)
    for rel in ("scripts/publish_github_release.py",):
        if (ROOT / rel).is_file() and "??" in _git("status", "--porcelain", rel):
            rows.append(rel)
    return sorted(set(rows))


def _readme_expansion_status() -> dict:
    manifest = ROOT / "data" / "publication" / "readme_expansion_manifest.yaml"
    sections_dir = ROOT / "data" / "publication" / "readme_sections"
    if not manifest.is_file():
        return {"exists": False, "pending_sections": "all", "action": "python scripts/build_readme_thesis_expansion.py"}
    try:
        import yaml

        doc = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    except Exception:
        doc = {}
    pending = [s["id"] for s in doc.get("sections") or [] if s.get("status") != "written"]
    written = [s["id"] for s in doc.get("sections") or [] if s.get("status") == "written"]
    return {
        "exists": True,
        "written_count": len(written),
        "pending_count": len(pending),
        "pending_ids": pending[:20],
        "sections_on_disk": len(list(sections_dir.glob("*.md"))) if sections_dir.is_dir() else 0,
    }


def main() -> int:
    sync = _ahead_behind()
    modified = _local_modified()
    claims_gaps = _claims_staleness()
    cross = _load(ROOT / "data/cross_proof_verification_report.json") or {}
    archive_audit = _load(ROOT / "data" / "archive_independence_audit.json")

    missing_on_disk = [p for p in KEY_ARTIFACTS if not (ROOT / p).is_file()]

    actions: list[dict] = []
    if sync["local_ahead"] > 0 or modified:
        actions.append(
            {
                "priority": "high",
                "action": "git add + commit + push pending verification artifacts",
                "detail": f"{len(modified)} working-tree changes; ahead of origin by {sync['local_ahead']}",
            }
        )
    if claims_gaps:
        actions.append(
            {
                "priority": "high",
                "action": "Refresh publication_claims_manifest.json",
                "detail": claims_gaps,
            }
        )
    if not cross.get("github_ready"):
        actions.append(
            {
                "priority": "critical",
                "action": "python scripts/run_cross_proof_verification.py",
                "detail": f"github_ready={cross.get('github_ready')} overall_ok={cross.get('overall_ok')}",
            }
        )
    expansion = _readme_expansion_status()
    if expansion.get("pending_count", 0) > 0 or not expansion.get("exists"):
        actions.append(
            {
                "priority": "medium",
                "action": "python scripts/build_readme_thesis_expansion.py",
                "detail": expansion,
            }
        )
    untracked = _untracked_publication()
    if untracked:
        actions.append(
            {
                "priority": "medium",
                "action": "Track and push publication support files",
                "detail": untracked,
            }
        )

    report = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "canonical_hub": str(ROOT),
        "github_repo": "https://github.com/dappalumbo91/FSOT-2.1-Lean",
        "sync": sync,
        "archive_independence_ok": (archive_audit or {}).get("ok") if archive_audit else None,
        "cross_proof": {
            "overall_ok": cross.get("overall_ok"),
            "github_ready": cross.get("github_ready"),
            "atomic_provable_count": (cross.get("full_formal_spine") or {}).get("atomic_provable_count"),
            "generated_at": cross.get("generated_at"),
        },
        "claims_staleness": claims_gaps,
        "missing_key_artifacts": missing_on_disk,
        "untracked_publication_files": untracked,
        "modified_file_count": len(modified),
        "modified_files_sample": [m[:120] for m in modified[:40]],
        "readme_expansion": expansion,
        "recommended_pipeline": [
            "python scripts/sync_verified_desktop_projects.py",
            "python scripts/run_publication_verification_bundle.py",
            "python scripts/export_publication_domain_atlas.py",
            "python scripts/build_readme_thesis_expansion.py",
            "python scripts/audit_github_readme_sync.py",
            "git add data/ verification/ README.md docs/ scripts/ && git commit && git push origin main",
        ],
        "actions": actions,
        "ok_for_expansive_run": cross.get("github_ready") and not claims_gaps and not missing_on_disk,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# GitHub / README Sync Audit",
        "",
        f"**Audited:** {report['audited_at']}",
        f"**Local HEAD:** `{sync['local_head']}` | **Origin:** `{sync['origin_head']}`",
        f"**Ahead of origin:** {sync['local_ahead']} | **Behind:** {sync['local_behind']}",
        "",
        f"**Cross-proof:** overall_ok={cross.get('overall_ok')} github_ready={cross.get('github_ready')}",
        f"**Ready for expansive README run:** `{report['ok_for_expansive_run']}`",
        "",
        "## Actions required",
        "",
    ]
    if not actions:
        md_lines.append("- None — archive and GitHub are aligned for expansion run.")
    else:
        for i, act in enumerate(actions, 1):
            md_lines.append(f"{i}. **[{act['priority']}]** {act['action']}")
            md_lines.append(f"   - {act['detail']}")
            md_lines.append("")

    if claims_gaps:
        md_lines.extend(["## Claims manifest staleness", ""])
        for g in claims_gaps:
            md_lines.append(
                f"- **{g['panel']}:** benchmark={g['benchmark_records']} vs claims={g['claims_manifest_records']}"
            )
        md_lines.append("")

    md_lines.extend(
        [
            "## Expansive run pipeline",
            "",
            "```bash",
            "cd I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full",
            "python scripts/sync_verified_desktop_projects.py",
            "python scripts/run_publication_verification_bundle.py --full-cross-proof",
            "python scripts/export_publication_domain_atlas.py",
            "python scripts/build_readme_thesis_expansion.py",
            "python scripts/audit_github_readme_sync.py",
            "```",
            "",
            f"Full JSON: `{OUT_JSON.relative_to(ROOT).as_posix()}`",
        ]
    )
    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(json.dumps({"ok": report["ok_for_expansive_run"], "actions": len(actions), "out": str(OUT_JSON)}, indent=2))
    return 0 if report["ok_for_expansive_run"] else 1


if __name__ == "__main__":
    raise SystemExit(main())