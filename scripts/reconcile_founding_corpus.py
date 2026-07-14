#!/usr/bin/env python3
"""Harvest I:\\fsuft aasb + I:\\fsot tech founding docs; reconcile against FSOT 2.1 registry."""

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
REGISTRY = ROOT / "data" / "founding_concepts_registry.yaml"
DEFAULT_OUT = ROOT / "vendor" / "philosophy_corpus" / "fsot_founding_reconciled.jsonl"

FOUNDING_ROOTS = [
    Path(r"I:\fsuft aasb"),
    Path(r"I:\fsot tech"),
]

CHUNK_CHARS = 2600
HALLUCINATION_PATTERNS = [
    r"99\.999999%",
    r"4\.578\s*billion",
    r"11\.828\s*billion",
    r"zero\s*percent\s*difference",
    r"0%\s*\|",
]

CONCEPT_KEYWORDS = {
    "as_above_so_below": ["as above", "so below", "cross-scale", "cross scale"],
    "fluid_25d_ontology": ["25d", "25-d", "fluid spacetime", "fluidic spacetime", "condensate"],
    "consciousness_fundamental": ["consciousness", "ψ_con", "psi_con", "Ψ_con", "observer"],
    "zero_free_parameters": ["zero free", "zero-free", "no free parameter", "first principles"],
    "scalar_unification": ["theory of everything", "unified field", "single formula", "scalar"],
    "tech_blueprints": ["blueprint", "reactor", "warp", "aetherion", "generator"],
}


def _chunk(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= CHUNK_CHARS:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        if end < len(text):
            brk = text.rfind("\n\n", start, end)
            if brk > start + 400:
                end = brk
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - 180, start + 1)
    return chunks


def _detect_hallucination_risk(text: str) -> list[str]:
    flags = []
    for pat in HALLUCINATION_PATTERNS:
        if re.search(pat, text, re.I):
            flags.append(pat)
    if re.search(r"multiplier.*base|auto_tune|MLPRegressor", text, re.I):
        flags.append("founding_fitting_method")
    return flags


def _match_concepts(text: str, registry: dict) -> list[dict]:
    lower = text.lower()
    hits = []
    for concept in registry.get("concepts") or []:
        cid = concept["id"]
        kws = CONCEPT_KEYWORDS.get(cid, [])
        if any(kw in lower for kw in kws) or cid.replace("_", " ") in lower:
            hits.append({
                "concept_id": cid,
                "status": concept.get("status"),
                "fsot_21": concept.get("fsot_21"),
                "epistemic_tier": concept.get("epistemic_tier"),
            })
    return hits


def _wrap_reconciliation(chunk: str, concepts: list[dict], flags: list[str], source: str) -> str:
    header = [
        f"[FOUNDING SOURCE: {source}]",
        "[RECONCILIATION: FSOT 2.1 Lean is ground truth for numeric claims.]",
    ]
    if flags:
        header.append(f"[HALLUCINATION RISK FLAGS: {', '.join(flags)}]")
        header.append("[DO NOT TRAIN THESE NUMBERS AS FACT — re-verify via fsot_verification_runner.py]")
    if concepts:
        header.append("[MAPPED CONCEPTS:]")
        for c in concepts[:6]:
            header.append(
                f"  - {c['concept_id']}: status={c['status']} → {c['fsot_21']} (tier: {c['epistemic_tier']})"
            )
    header.append("---")
    return "\n".join(header) + "\n" + chunk


def _iter_founding_files() -> list[Path]:
    files: list[Path] = []
    pdf_extracted = ROOT / "vendor" / "founding_corpus" / "pdf_extracted"
    if pdf_extracted.exists():
        files.extend(sorted(pdf_extracted.glob("*.txt")))
    for root in FOUNDING_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() in (".md", ".py", ".txt"):
                if "fsot_updated_blueprints" in str(path) and path.suffix.lower() != ".md":
                    continue
                files.append(path)
    return sorted(set(files))


def build_founding_corpus(
    registry_path: Path = REGISTRY,
    out_path: Path = DEFAULT_OUT,
) -> int:
    if yaml is None:
        raise SystemExit("PyYAML required")

    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for fpath in _iter_founding_files():
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if len(text.strip()) < 80:
            continue

        rel = str(fpath)
        root_label = "fsuft_aasb" if "fsuft aasb" in rel.lower() else "fsot_tech"

        for i, chunk in enumerate(_chunk(text)):
            flags = _detect_hallucination_risk(chunk)
            concepts = _match_concepts(chunk, registry)
            wrapped = _wrap_reconciliation(chunk, concepts, flags, rel)

            epistemic = "founding_interpretive"
            if flags:
                epistemic = "founding_caveat"
            if concepts and all(c.get("epistemic_tier") == "proved" for c in concepts):
                epistemic = "founding_philosophy_verified_math"

            rows.append({
                "id": f"founding_{root_label}_{fpath.stem}__{i:03d}",
                "title": f"Founding: {fpath.stem}",
                "instruction": (
                    "Present this FSOT founding research accurately. Retain philosophical intent. "
                    "Where reconciliation flags appear, cite FSOT 2.1 Lean as ground truth. "
                    "Never present founding multiplier-fitting or inflated accuracy as verified fact."
                ),
                "content": wrapped,
                "category": "founding_lineage",
                "epistemic_tier": epistemic,
                "source": rel,
                "founding_root": root_label,
                "hallucination_flags": flags,
                "mapped_concepts": [c["concept_id"] for c in concepts],
                "reconciliation_status": "founding_with_caveat" if flags else "founding_philosophy",
            })

    # Add registry concept summaries as explicit training rows
    for concept in registry.get("concepts") or []:
        summary = json.dumps(concept, indent=2)
        rows.append({
            "id": f"registry_{concept['id']}",
            "title": f"Concept map: {concept['id']}",
            "instruction": "Explain how this founding FSOT concept maps to FSOT 2.1 Lean.",
            "content": summary,
            "category": "founding_reconciliation",
            "epistemic_tier": concept.get("epistemic_tier", "proved"),
            "source": str(registry_path),
            "founding_root": "registry",
            "reconciliation_status": concept.get("status"),
        })

    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rows": len(rows),
        "files_scanned": len(_iter_founding_files()),
        "output": str(out_path),
    }
    out_path.with_name("fsot_founding_reconciled.summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(rows)} founding rows -> {out_path}")
    return len(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", type=Path, default=REGISTRY)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    return 0 if build_founding_corpus(args.registry, args.out) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())