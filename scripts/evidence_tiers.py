#!/usr/bin/env python3
"""Label every domain and benchmark record as exploratory, frozen-pending, or confirmed.

Missing dates stay exploratory. A row is confirmed only when a hashed freeze
is dated before the data release. Ledger B rows and identity rows are a
separate bucket. This script does not edit freeze files or benchmark values.

  python scripts/evidence_tiers.py
  python scripts/evidence_tiers.py --check
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from benchmark_margin_lib import is_ledger_b_scale_step  # noqa: E402

DATA = ROOT / "data"
OUT = DATA / "evidence_tiers.json"
DOC = ROOT / "docs" / "EVIDENCE_TIERS.md"
FREEZE_DIR = ROOT / "predictions" / "domain_freezes"
PREREG = ROOT / "predictions" / "toe_prereg_freeze.json"
EXTENSION = DATA / "extension_folds_derived.json"
AUTHORITY = ROOT / "vendor" / "fsot_compute.py"

IDENTITY_ROWS = frozenset(
    {
        "Proton_radius",
        "STDP_Tau_Plus_ms",
        "STDP_Tau_Minus_ms",
        "Metatron_Spheres",
        "Metatron_Pathways",
        "Max_Trits",
        "Potts3_beta",
        "Quark_condensate",
    }
)
RELEASE_KEYS = ("release_date", "published", "publication_date", "dataset_release", "data_release")
RETRIEVAL_KEYS = ("retrieved_at", "retrieval_date", "fetched_at", "download_date")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_last(path: Path) -> dict:
    try:
        text = subprocess.check_output(
            ["git", "log", "-1", "--format=%H%n%cI", "--", path.relative_to(ROOT).as_posix()],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        return {"commit": None, "committed_at": None}
    if not text:
        return {"commit": None, "committed_at": None}
    commit, committed_at = text.splitlines()[:2]
    return {"commit": commit, "committed_at": committed_at}


def _parse_dt(value) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _first(obj: dict, keys: tuple[str, ...]):
    for key in keys:
        if obj.get(key):
            return obj.get(key)
    return None


def _data_ref(doc: dict, rec: dict | None = None) -> dict:
    src = doc if rec is None else rec
    source = src.get("source") or src.get("ingest_source") or doc.get("source")
    if isinstance(source, list):
        source = "; ".join(str(item) for item in source[:4])
    doi = src.get("doi") or src.get("reference") or doc.get("doi")
    url = src.get("url") or doc.get("url")
    release = _first(src, RELEASE_KEYS) or _first(doc, RELEASE_KEYS)
    retrieval = _first(src, RETRIEVAL_KEYS) or _first(doc, RETRIEVAL_KEYS)
    return {
        "source": source if isinstance(source, str) else None,
        "doi_or_url": doi or url,
        "release_date": release if isinstance(release, str) else None,
        "retrieval_date": retrieval if isinstance(retrieval, str) else None,
    }


def _records(doc: dict) -> list[dict]:
    recs = doc.get("material_records") or doc.get("records") or []
    if not isinstance(recs, list):
        return []
    return [r for r in recs if isinstance(r, dict)]


def _is_identity(rec: dict) -> bool:
    name = str(rec.get("name") or rec.get("property") or "")
    return name in IDENTITY_ROWS


def _load_freezes() -> list[dict]:
    found = []
    if PREREG.is_file():
        doc = json.loads(PREREG.read_text(encoding="utf-8"))
        found.append(
            {
                "kind": "sector_prereg",
                "path": PREREG.relative_to(ROOT).as_posix(),
                "sha256": _sha256(PREREG),
                "date": doc.get("frozen_at"),
                "freeze_id": doc.get("freeze_id"),
                "sectors": doc.get("sector_predictions") or [],
            }
        )
    if FREEZE_DIR.is_dir():
        for path in sorted(FREEZE_DIR.glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            found.append(
                {
                    "kind": "domain_mapping",
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": doc.get("mapping_sha256") or _sha256(path),
                    "file_sha256": _sha256(path),
                    "date": doc.get("frozen_at"),
                    "domain": doc.get("domain"),
                    "mapping": doc.get("mapping") or {},
                }
            )
    return found


def _blank_ref() -> dict:
    return {"source": None, "doi_or_url": None, "release_date": None, "retrieval_date": None}


def _domain_rows(freezes: list[dict], extension: dict, core_names: list[str], git_notes: dict) -> list[dict]:
    frozen_domains = {
        item["domain"]: item for item in freezes if item["kind"] == "domain_mapping" and item.get("domain")
    }
    rows = []
    folds = (extension or {}).get("folds") or {}
    names = list(dict.fromkeys([*core_names, *folds.keys()]))
    for name in names:
        fold = folds.get(name) or {}
        freeze = frozen_domains.get(name)
        if freeze and _parse_dt(freeze.get("date")) is not None:
            tier = "frozen_pending"
            reason = (
                "Mapping freeze is hashed and dated. No data release dated after that "
                "freeze was found for this domain, so it is waiting on a later test."
            )
            freeze_ref = {
                "path": freeze["path"],
                "sha256": freeze["sha256"],
                "date": freeze["date"],
            }
        else:
            tier = "exploratory"
            reason = (
                "No dated per-domain freeze of D_eff, look, hits, observed, or formula. "
                "File history of the mapping is not a held-out lock. Default exploratory."
            )
            freeze_ref = None
        rows.append(
            {
                "domain": name,
                "group": "core" if name in core_names else "extension",
                "tier": tier,
                "reason": reason,
                "mapping": {
                    "D_eff": fold.get("D_eff"),
                    "look": fold.get("look"),
                    "hits": fold.get("hits"),
                    "observed": fold.get("observed"),
                    "parent_core": fold.get("parent_core"),
                }
                if fold
                else {"source": "vendor/fsot_compute.py DOMAINS"},
                "freeze_ref": freeze_ref,
                "data_ref": _blank_ref(),
                "mapping_file_history": git_notes,
            }
        )
    prereg = next((item for item in freezes if item["kind"] == "sector_prereg"), None)
    if prereg and _parse_dt(prereg.get("date")) is not None:
        freeze_ref = {
            "path": prereg["path"],
            "sha256": prereg["sha256"],
            "date": prereg["date"],
            "freeze_id": prereg.get("freeze_id"),
        }
        for sector in prereg["sectors"]:
            sid = str(sector.get("id") or "")
            rows.append(
                {
                    "domain": sid,
                    "group": "frozen_sector_prediction",
                    "tier": "frozen_pending",
                    "reason": (
                        "The predicted value and kill are inside the hashed preregistration. "
                        "No benchmark row for this id carried a data release dated after the freeze, "
                        "so the prediction is frozen and still awaiting that test."
                    ),
                    "mapping": {
                        "fsot_predicted": sector.get("fsot_predicted"),
                        "unit": sector.get("unit"),
                        "kill": sector.get("kill"),
                        "future_survey": sector.get("future_survey"),
                    },
                    "freeze_ref": freeze_ref,
                    "data_ref": _blank_ref(),
                    "mapping_file_history": git_notes,
                }
            )
    return rows


def _record_tier(rec: dict, doc: dict, domain_freeze: dict | None) -> tuple[str, str]:
    if is_ledger_b_scale_step(rec) or _is_identity(rec):
        return "structural_identity", "Ledger B scale step or an identity row. Not a tier."
    data = _data_ref(doc, rec)
    release = _parse_dt(data.get("release_date"))
    if domain_freeze is None or _parse_dt(domain_freeze.get("date")) is None:
        return (
            "exploratory",
            "No dated freeze covers this row. A retrieval stamp is not a release date. Default exploratory.",
        )
    frozen = _parse_dt(domain_freeze["date"])
    if release is not None and frozen < release:
        return (
            "confirmed_held_out",
            "Freeze timestamp is before the data release date.",
        )
    if release is not None:
        return (
            "exploratory",
            "The data release is not after the freeze, so this score is not a held-out confirmation.",
        )
    return (
        "exploratory",
        "The domain mapping may be frozen, and this row has no data release date. Default exploratory.",
    )


def build() -> dict:
    extension = json.loads(EXTENSION.read_text(encoding="utf-8")) if EXTENSION.is_file() else {}
    import importlib

    compute = importlib.import_module("fsot_compute")
    core_names = list(compute.DOMAINS)
    git_notes = {
        "extension_folds": {**_git_last(EXTENSION), "generated_at": extension.get("generated_at")},
        "authority": _git_last(AUTHORITY),
        "note": "These are file-level commits. They do not by themselves freeze one domain.",
    }
    freezes = _load_freezes()
    domain_freeze = {
        item["domain"]: item for item in freezes if item["kind"] == "domain_mapping" and item.get("domain")
    }
    domains = _domain_rows(freezes, extension, core_names, git_notes)
    # Confirmed domains are filled after records, if any row for that domain is confirmed.
    counts = {
        "exploratory": 0,
        "frozen_pending": 0,
        "confirmed_held_out": 0,
        "structural_identity": 0,
    }
    undetermined = []
    files = []
    tier3_records = []
    for path in sorted(DATA.glob("*_benchmark.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            undetermined.append({"file": path.name, "reason": f"JSON did not parse: {exc}"})
            continue
        if not isinstance(doc, dict):
            undetermined.append({"file": path.name, "reason": "Top-level JSON is not an object."})
            continue
        file_counts = {key: 0 for key in counts}
        domain_name = str(doc.get("domain") or "")
        freeze = domain_freeze.get(domain_name)
        for rec in _records(doc):
            rec_domain = str(rec.get("fsot_domain") or rec.get("domain") or domain_name)
            rec_freeze = domain_freeze.get(rec_domain) or freeze
            tier, reason = _record_tier(rec, doc, rec_freeze)
            file_counts[tier] += 1
            counts[tier] += 1
            if tier == "confirmed_held_out":
                tier3_records.append(
                    {
                        "file": path.name,
                        "domain": rec_domain,
                        "name": rec.get("name") or rec.get("property"),
                        "reason": reason,
                        "freeze_ref": {
                            "path": rec_freeze["path"],
                            "sha256": rec_freeze["sha256"],
                            "date": rec_freeze["date"],
                        },
                        "data_ref": _data_ref(doc, rec),
                    }
                )
        if sum(file_counts.values()) == 0:
            file_tier = "exploratory"
            file_reason = "No records. Default exploratory."
        elif file_counts["exploratory"] == 0 and file_counts["confirmed_held_out"] and file_counts["frozen_pending"] == 0:
            file_tier = "confirmed_held_out"
            file_reason = "Every scored row is a held-out confirmation."
        elif file_counts["structural_identity"] == sum(file_counts.values()):
            file_tier = "structural_identity"
            file_reason = "Every row is a Ledger B step or an identity row."
        else:
            file_tier = "exploratory"
            file_reason = "At least one scored row lacks a freeze dated before its data release."
        files.append(
            {
                "file": path.name,
                "domain": domain_name or None,
                "tier": file_tier,
                "reason": file_reason,
                "counts": file_counts,
                "freeze_ref": (
                    {"path": freeze["path"], "sha256": freeze["sha256"], "date": freeze["date"]}
                    if freeze
                    else None
                ),
                "data_ref": _data_ref(doc),
            }
        )
    confirmed_domains = {row["domain"] for row in tier3_records}
    for row in domains:
        if row["domain"] in confirmed_domains:
            row["tier"] = "confirmed_held_out"
            row["reason"] = "A scored row for this domain has a data release after the mapping freeze."
    domain_counts = {
        "exploratory": sum(1 for row in domains if row["tier"] == "exploratory"),
        "frozen_pending": sum(1 for row in domains if row["tier"] == "frozen_pending"),
        "confirmed_held_out": sum(1 for row in domains if row["tier"] == "confirmed_held_out"),
    }
    closest = [
        {
            "domain": row["domain"],
            "freeze_ref": row["freeze_ref"],
            "future_survey": (row.get("mapping") or {}).get("future_survey"),
            "reason": "Frozen, and this repo does not yet record a data release after the freeze.",
        }
        for row in domains
        if row["tier"] == "frozen_pending"
    ]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rule": (
            "Tier 3 requires freeze_ref.date strictly before data_ref.release_date. "
            "A retrieval date is stored and is not used as a release date. "
            "Missing dates stay exploratory. Ledger B and identity rows are not a tier."
        ),
        "headline": {
            "exploratory": counts["exploratory"],
            "frozen_pending": counts["frozen_pending"],
            "confirmed_held_out": counts["confirmed_held_out"],
            "structural_identity": counts["structural_identity"],
            "accuracy_claim": "confirmed_held_out",
            "confirmed_held_out_is_the_accuracy_claim": counts["confirmed_held_out"],
        },
        "record_counts": counts,
        "domain_counts": domain_counts,
        "closest_to_promotion": closest,
        "undetermined": undetermined,
        "tier3_records": tier3_records,
        "domains": domains,
        "files": files,
    }


def _md(report: dict) -> str:
    h = report["headline"]
    lines = [
        "# Evidence tiers",
        "",
        "Exploratory work stays visible. Confirmation is a separate count.",
        "The accuracy claim is the confirmed held-out count.",
        "",
        "| Group | Records |",
        "|-------|--------:|",
        f"| Exploratory | {h['exploratory']} |",
        f"| Frozen, pending | {h['frozen_pending']} |",
        f"| Confirmed held-out | {h['confirmed_held_out']} |",
        f"| Structural / identity | {h['structural_identity']} |",
        "",
        f"Confirmed held-out accuracy claim: **{h['confirmed_held_out']}**.",
        "",
        "Structural / identity counts Ledger B scale steps and identity-named rows.",
        "The margin audit's Ledger B structural-correction count is the scale steps only.",
        "",
        "A retrieval date is not treated as the day the data came into existence.",
        "Where a release date or a freeze date is missing, the row stays exploratory.",
        "",
        "## Domains",
        "",
        "| Domain | Tier | Reason |",
        "|--------|------|--------|",
    ]
    for row in report["domains"]:
        reason = row["reason"].replace("|", "/")
        lines.append(f"| `{row['domain']}` | {row['tier']} | {reason} |")
    lines.extend(
        [
            "",
            "## Closest to a later confirmation",
            "",
        ]
    )
    if not report["closest_to_promotion"]:
        lines.append("No domain is both frozen and tied to a data release dated after that freeze.")
    else:
        lines.append(
            "These are frozen. This repo does not yet record a public data release dated after the freeze, so none move to confirmed."
        )
        for row in report["closest_to_promotion"]:
            survey = row.get("future_survey") or "no future survey named"
            lines.append(f"- `{row['domain']}` — {survey}")
    lines.extend(["", "## Undetermined", ""])
    if not report["undetermined"]:
        lines.append("Every parsed benchmark file received a tier. Unparsed files are listed here when they occur.")
    else:
        for row in report["undetermined"]:
            lines.append(f"- `{row['file']}` — {row['reason']}")
    lines.append("")
    return "\n".join(lines) + "\n"


def check(report: dict) -> int:
    bad = []
    for row in report.get("tier3_records") or []:
        freeze = _parse_dt((row.get("freeze_ref") or {}).get("date"))
        release = _parse_dt((row.get("data_ref") or {}).get("release_date"))
        if freeze is None or release is None or not (freeze < release):
            bad.append(row)
    for row in report.get("domains") or []:
        if row.get("tier") != "confirmed_held_out":
            continue
        freeze = _parse_dt((row.get("freeze_ref") or {}).get("date"))
        release = _parse_dt((row.get("data_ref") or {}).get("release_date"))
        if freeze is None or release is None or not (freeze < release):
            bad.append({"domain": row.get("domain"), "freeze_ref": row.get("freeze_ref"), "data_ref": row.get("data_ref")})
    print(
        "tier3",
        len(report.get("tier3_records") or []),
        "violations",
        len(bad),
        "confirmed_claim",
        (report.get("headline") or {}).get("confirmed_held_out"),
    )
    for row in bad[:20]:
        print(json.dumps(row, default=str)[:300])
    return 1 if bad else 0


def main() -> int:
    if "--check" in sys.argv:
        if not OUT.is_file():
            print("missing", OUT)
            return 1
        return check(json.loads(OUT.read_text(encoding="utf-8")))
    report = build()
    OUT.write_bytes((json.dumps(report, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    DOC.write_bytes(_md(report).encode("utf-8"))
    h = report["headline"]
    print(
        "exploratory",
        h["exploratory"],
        "frozen_pending",
        h["frozen_pending"],
        "confirmed",
        h["confirmed_held_out"],
        "structural",
        h["structural_identity"],
        "domains",
        report["domain_counts"],
        "undetermined",
        len(report["undetermined"]),
        "closest",
        len(report["closest_to_promotion"]),
    )
    return check(report)


if __name__ == "__main__":
    raise SystemExit(main())
