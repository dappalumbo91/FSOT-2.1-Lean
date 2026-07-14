#!/usr/bin/env python3
"""Harvest FSOT philosophy/consciousness sources into LLM training jsonl."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "philosophy_corpus_manifest.yaml"
DEFAULT_OUT = ROOT / "vendor" / "philosophy_corpus" / "fsot_philosophy_training.jsonl"

CHUNK_CHARS = 2800
CHUNK_OVERLAP = 200


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _chunk_text(text: str, source_id: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= CHUNK_CHARS:
        return [text]
    chunks: list[str] = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        if end < len(text):
            break_at = text.rfind("\n\n", start, end)
            if break_at > start + 500:
                end = break_at
        chunks.append(text[start:end].strip())
        idx += 1
        if end >= len(text):
            break
        start = max(end - CHUNK_OVERLAP, start + 1)
    return chunks


def _sections_from_markers(text: str, markers: list[str]) -> str:
    if not markers or not text:
        return text
    parts: list[str] = []
    for marker in markers:
        pat = re.compile(rf"(^|\n)(#+\s*.*{re.escape(marker)}.*|\*\*.*{re.escape(marker)}.*\*\*)", re.I)
        for m in pat.finditer(text):
            start = m.start()
            nxt = pat.search(text, m.end() + 1)
            end = nxt.start() if nxt else min(start + 12000, len(text))
            parts.append(text[start:end].strip())
    return "\n\n---\n\n".join(parts) if parts else text


def _benchmark_summary(path: Path) -> str:
    if not path.exists():
        return ""
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = [
        f"Domain: {data.get('domain', path.stem)}",
        f"Records: {data.get('record_count', data.get('observable_count', '?'))}",
        f"Median error %: {data.get('median_error_pct', data.get('headline_median_error_pct', '?'))}",
        f"D_eff: {data.get('D_eff', '?')}",
        f"Maps to Lean: {data.get('maps_to_lean', [])}",
    ]
    note = data.get("note") or (data.get("sota_comparison") or {}).get("note")
    if note:
        lines.append(f"Note: {note}")
    recs = data.get("records") or []
    for rec in recs[:8]:
        name = rec.get("name") or rec.get("property") or "record"
        err = rec.get("error_pct", "?")
        lines.append(f"  - {name}: error_pct={err}")
    if len(recs) > 8:
        lines.append(f"  ... +{len(recs) - 8} more records")
    return "\n".join(lines)


def _json_ref_summary(path: Path) -> str:
    if not path.exists():
        return ""
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return json.dumps(data, indent=2)[:8000]
    return str(data)[:8000]


def _lean_header_summary(path: Path) -> str:
    text = _read_text(path)
    if not text:
        return ""
    header = []
    for line in text.splitlines()[:40]:
        header.append(line)
        if line.strip() == "end" and len(header) > 10:
            break
    return "\n".join(header)


def _load_source(entry: dict) -> str:
    raw = entry.get("path", "")
    path = Path(raw) if Path(raw).is_absolute() else ROOT / raw
    suffix = path.suffix.lower()

    if suffix == ".json" and "benchmark" in path.name:
        return _benchmark_summary(path)
    if suffix == ".json":
        return _json_ref_summary(path)
    if suffix == ".lean":
        return _lean_header_summary(path)
    if suffix in (".yaml", ".yml"):
        return _read_text(path)

    text = _read_text(path)
    markers = entry.get("section_markers") or []
    if markers and suffix == ".md":
        extracted = _sections_from_markers(text, markers)
        if extracted.strip():
            return extracted
    return text


def build_corpus(manifest_path: Path = MANIFEST, out_path: Path = DEFAULT_OUT) -> int:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    missing: list[str] = []

    for entry in sorted(manifest.get("sources") or [], key=lambda e: e.get("priority", 99)):
        sid = entry["id"]
        content = _load_source(entry)
        if not content.strip():
            missing.append(sid)
            continue

        meta = {
            "category": entry.get("category", "philosophy_core"),
            "epistemic_tier": entry.get("epistemic_tier", "interpretive"),
            "source": entry.get("path"),
            "lean_module": entry.get("lean_module"),
            "priority": entry.get("priority"),
        }

        for i, chunk in enumerate(_chunk_text(content, sid)):
            rows.append({
                "id": f"{sid}__chunk_{i:03d}",
                "title": entry.get("id", sid).replace("_", " ").title(),
                "instruction": (
                    "Explain this aspect of FSOT (Fluid Spacetime Omni-Theory) philosophy, "
                    "ontology, or consciousness. Tag the epistemic tier. "
                    "Distinguish what is proved, measured, scaffold, interpretive, or conjectured."
                ),
                "content": chunk,
                **meta,
            })

    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rows": len(rows),
        "missing_sources": missing,
        "output": str(out_path),
    }
    summary_path = out_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote {len(rows)} rows -> {out_path}")
    if missing:
        print(f"Missing/skipped: {missing}")
    return len(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    n = build_corpus(args.manifest, args.out)
    return 0 if n > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())