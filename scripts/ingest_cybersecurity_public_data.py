#!/usr/bin/env python3
"""Ingest MalwareBazaar + CISA KEV into external cache and portable vendor summaries."""

from __future__ import annotations

import argparse
import csv
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys_path = ROOT / "scripts"

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from tier38_public_data_lib import cache_path, external_data_root, vendor_path  # noqa: E402

MALWAREBazaar_CSV_URL = "https://bazaar.abuse.ch/export/csv/recent/"
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def _fetch_bytes(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-Tier43-cyber-ingest/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _fetch_json(url: str, timeout: int = 60) -> dict | list:
    return json.loads(_fetch_bytes(url, timeout=timeout).decode("utf-8"))


def _parse_malwarebazaar_csv(text: str) -> list[dict]:
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    if not lines:
        return []
    reader = csv.DictReader(io.StringIO("\n".join(lines)))
    rows: list[dict] = []
    for row in reader:
        rows.append(
            {
                "sha256_hash": row.get("sha256_hash") or row.get("sha256"),
                "md5_hash": row.get("md5_hash"),
                "sha1_hash": row.get("sha1_hash"),
                "file_type": row.get("file_type"),
                "signature": row.get("signature"),
                "tags": row.get("tags"),
                "first_seen": row.get("first_seen_utc") or row.get("first_seen"),
                "filename": row.get("file_name"),
            }
        )
    return rows


def ingest_malwarebazaar(*, limit: int = 200) -> dict:
    ext = cache_path("cybersecurity", "malwarebazaar_recent.json")
    vend = ROOT / "vendor" / "cybersecurity" / "malwarebazaar_summary.json"
    vend.parent.mkdir(parents=True, exist_ok=True)
    vend_pub = vendor_path("cybersecurity", "malwarebazaar_summary.json")
    try:
        csv_text = _fetch_bytes(MALWAREBazaar_CSV_URL).decode("utf-8", errors="replace")
        samples = _parse_malwarebazaar_csv(csv_text)
        source = "live_csv"
    except Exception as exc:
        if ext.exists():
            cached = json.loads(ext.read_text(encoding="utf-8"))
            samples = cached.get("samples") or []
            source = "cache_fallback"
        else:
            raise RuntimeError(f"MalwareBazaar fetch failed: {exc}") from exc

    trimmed = samples[:limit]
    ext.write_text(json.dumps({"fetched_at": datetime.now(timezone.utc).isoformat(), "samples": trimmed}, indent=2), encoding="utf-8")

    families: dict[str, int] = {}
    tags: dict[str, int] = {}
    records: list[dict] = []
    for row in trimmed:
        if not isinstance(row, dict):
            continue
        fam = str(row.get("signature") or row.get("malware_family") or row.get("tags") or "unknown")
        families[fam] = families.get(fam, 0) + 1
        for tag in str(row.get("tags") or "").split(","):
            tag = tag.strip()
            if tag:
                tags[tag] = tags.get(tag, 0) + 1
        records.append(
            {
                "sha256_hash": row.get("sha256_hash") or row.get("sha256"),
                "file_type": row.get("file_type"),
                "signature": row.get("signature"),
                "tags": row.get("tags"),
                "first_seen": row.get("first_seen"),
            }
        )

    summary = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "sample_count": len(records),
        "family_histogram": dict(sorted(families.items(), key=lambda x: -x[1])[:30]),
        "tag_histogram": dict(sorted(tags.items(), key=lambda x: -x[1])[:40]),
        "records": records,
        "external_cache": str(ext),
    }
    payload = json.dumps(summary, indent=2)
    vend.write_text(payload, encoding="utf-8")
    vend_pub.write_text(payload, encoding="utf-8")
    return {"malwarebazaar_samples": len(records), "external": str(ext), "vendor": str(vend)}


def ingest_cisa_kev() -> dict:
    ext = cache_path("cybersecurity", "cisa_kev_catalog.json")
    vend = ROOT / "vendor" / "cybersecurity" / "cisa_kev_summary.json"
    vend.parent.mkdir(parents=True, exist_ok=True)
    vend_pub = vendor_path("cybersecurity", "cisa_kev_summary.json")
    try:
        raw = _fetch_json(CISA_KEV_URL)
    except Exception as exc:
        if ext.exists():
            raw = json.loads(ext.read_text(encoding="utf-8"))
            source = "cache_fallback"
        else:
            raise RuntimeError(f"CISA KEV fetch failed: {exc}") from exc
    else:
        source = "live_api"

    ext.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    vulns = raw.get("vulnerabilities") or []
    vendors: dict[str, int] = {}
    cwes: dict[str, int] = {}
    records: list[dict] = []
    for row in vulns:
        vendor = str(row.get("vendorProject") or "unknown")
        vendors[vendor] = vendors.get(vendor, 0) + 1
        cwe = str(row.get("cwes") or row.get("cwe") or "unknown")
        cwes[cwe] = cwes.get(cwe, 0) + 1
        records.append(
            {
                "cve_id": row.get("cveID"),
                "vendor": vendor,
                "product": row.get("product"),
                "vulnerability_name": row.get("vulnerabilityName"),
                "date_added": row.get("dateAdded"),
                "due_date": row.get("dueDate"),
                "cwes": row.get("cwes"),
                "ransomware_use": row.get("knownRansomwareCampaignUse"),
            }
        )

    summary = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "catalog_version": raw.get("catalogVersion"),
        "vulnerability_count": len(records),
        "vendor_histogram": dict(sorted(vendors.items(), key=lambda x: -x[1])[:25]),
        "cwe_histogram": dict(sorted(cwes.items(), key=lambda x: -x[1])[:25]),
        "records": records,
        "external_cache": str(ext),
    }
    payload = json.dumps(summary, indent=2)
    vend.write_text(payload, encoding="utf-8")
    vend_pub.write_text(payload, encoding="utf-8")
    return {"cisa_kev_count": len(records), "external": str(ext), "vendor": str(vend)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--malware-limit", type=int, default=200)
    args = parser.parse_args()
    root = external_data_root()
    print(f"External cache: {root}")
    mb = ingest_malwarebazaar(limit=args.malware_limit)
    kev = ingest_cisa_kev()
    print(json.dumps({"malwarebazaar": mb, "cisa_kev": kev}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())