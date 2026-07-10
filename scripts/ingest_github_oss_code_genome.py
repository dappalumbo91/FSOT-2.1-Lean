#!/usr/bin/env python3
"""Ingest curated GitHub OSS files for external code-genome verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "github_oss_code_genome_manifest.yaml"
VENDOR = ROOT / "vendor" / "github_oss"

sys.path.insert(0, str(ROOT / "scripts"))
from code_genome_lib import analyze_file, codon_index  # noqa: E402
from tier38_public_data_lib import cache_path, external_data_root  # noqa: E402
from tier_gap_fill_lib import _load_fsot, _scalar  # noqa: E402


def _raw_url(repo: str, ref: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"


def _fetch_text(url: str, timeout: int = 45) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-GitHub-OSS-ingest/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _needs_refresh(meta_path: Path, *, force: bool, stale_days: int | None) -> bool:
    if force:
        return True
    if stale_days is None or not meta_path.is_file():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        fetched = meta.get("fetched_at") or meta.get("generated_at")
        if not fetched:
            return True
        ts = datetime.fromisoformat(str(fetched).replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - ts).total_seconds() / 86400.0
        return age >= stale_days
    except (json.JSONDecodeError, ValueError, OSError):
        return True


def ingest(*, limit: int | None = None, force: bool = False, stale_days: int | None = None) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    _, _ = _load_fsot()
    domain_scalar = _scalar("Quantum_Computing")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    samples = spec.get("samples") or []
    if limit:
        samples = samples[:limit]

    ext_dir = external_data_root() / "github_oss" / "snapshots"
    ext_dir.mkdir(parents=True, exist_ok=True)
    vend_dir = VENDOR / "snapshots"
    vend_dir.mkdir(parents=True, exist_ok=True)

    analyses: list[dict] = []
    failures: list[dict] = []
    for row in samples:
        sid = row["id"]
        url = _raw_url(row["repo"], row["ref"], row["path"])
        lang = row["language"]
        out_ext = ext_dir / f"{sid}{Path(row['path']).suffix}"
        out_vend = vend_dir / f"{sid}{Path(row['path']).suffix}"
        meta_path = vend_dir / f"{sid}.json"
        try:
            refresh = _needs_refresh(meta_path, force=force, stale_days=stale_days)
            if out_ext.exists() and not refresh:
                text = out_ext.read_text(encoding="utf-8", errors="replace")
                source = "cache"
            else:
                text = _fetch_text(url)
                out_ext.write_text(text, encoding="utf-8")
                source = "live" if refresh or not out_vend.exists() else "refreshed"
            out_vend.write_text(text, encoding="utf-8")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if out_vend.exists():
                text = out_vend.read_text(encoding="utf-8", errors="replace")
                source = "vendor_fallback"
            else:
                failures.append({"id": sid, "url": url, "error": str(exc)})
                continue

        analysis = analyze_file(out_vend, lang, domain_scalar)
        analysis["sample_id"] = sid
        analysis["repo"] = row["repo"]
        analysis["category"] = row.get("category")
        analysis["url"] = url
        analysis["source"] = source
        analysis["fetched_at"] = datetime.now(timezone.utc).isoformat()
        analysis["content_sha256"] = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
        meta_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
        analyses.append(analysis)

    summary = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sample_count": len(analyses),
        "failure_count": len(failures),
        "failures": failures,
        "analyses": analyses,
        "external_cache": str(ext_dir),
    }
    summary_path = VENDOR / "github_oss_code_genome_summary.json"
    ext_summary = cache_path("github_oss", "github_oss_code_genome_summary.json")
    payload = json.dumps(summary, indent=2)
    summary_path.write_text(payload, encoding="utf-8")
    ext_summary.write_text(payload, encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--refresh", action="store_true", help="Force re-fetch all samples from GitHub")
    parser.add_argument("--stale-days", type=int, default=None, help="Re-fetch samples older than N days")
    args = parser.parse_args()
    stale_days = args.stale_days
    if stale_days is None and yaml is not None and MANIFEST.exists():
        spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        stale_days = int((spec.get("refresh_schedule") or {}).get("cadence_days") or 0) or None
    print(f"External cache: {external_data_root()}")
    summary = ingest(limit=args.limit, force=args.refresh, stale_days=stale_days)
    print(json.dumps({"sample_count": summary["sample_count"], "failure_count": summary["failure_count"]}, indent=2))
    return 0 if summary["sample_count"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())