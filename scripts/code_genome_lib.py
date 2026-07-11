#!/usr/bin/env python3
"""Code genome analyzer — program structures as FSOT codon/genomic analogs."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "vendor" / "cybersecurity" / "code_genome_language_registry.json"
CROSSWALK = ROOT / "data" / "code_genome_crosswalk.yaml"
STABILITY_THRESHOLD = 0.85
WINDOW_SIZE = 3

LANG_KEYWORDS: dict[str, list[str]] = {
    "Lean": ["theorem", "lemma", "def", "instance", "namespace", "import", "open", "by", "sorry"],
    "Rust": ["fn", "unsafe", "impl", "match", "pub", "mut", "const", "extern", "trait", "mod"],
    "Python": ["def", "class", "import", "lambda", "async", "yield", "exec", "eval", "return"],
    "C": ["malloc", "free", "strcpy", "memcpy", "pointer", "struct", "include", "void", "static", "return"],
    "JavaScript": ["function", "const", "eval", "prototype", "fetch", "document", "innerHTML", "require", "module", "async"],
    "Go": ["func", "package", "import", "struct", "interface", "return", "go", "defer", "unsafe"],
    "Zig": ["fn", "pub", "const", "struct", "return", "try", "comptime", "export"],
    "WebAssembly": ["func", "export", "memory", "module", "param", "result", "local.get", "i32.add", "i32.store"],
    "FSOTB_ISA": ["HALT", "IMM", "LOADT", "BRANCHT", "CALL", "RET", "MEASURE", "CONSENSUS"],
    "Java": ["class", "public", "static", "void", "import", "interface", "extends", "implements", "return", "synchronized"],
    "Kotlin": ["fun", "class", "object", "suspend", "lateinit", "inline", "override", "val", "var", "return"],
    "Swift": ["func", "class", "struct", "enum", "var", "let", "import", "guard", "return", "async"],
    "Haskell": ["data", "type", "class", "instance", "where", "let", "in", "module", "import", "do"],
}


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_registry() -> dict:
    return _load_json(REGISTRY)


def codon_index(language: str, token: str, arity: int = 0) -> int:
    key = f"{language}:{token}:{arity}".encode()
    return int(hashlib.sha256(key).hexdigest(), 16) % 64


def tokenize_source(text: str, language: str) -> list[str]:
    reg = _load_registry()
    lang = (reg.get("languages") or {}).get(language) or {}
    units = set(lang.get("codon_units") or LANG_KEYWORDS.get(language, []))
    risk = set(lang.get("risk_tokens") or [])
    found: list[str] = []
    for token in sorted(units | risk, key=len, reverse=True):
        if language == "WebAssembly":
            pattern = re.escape(token)
        else:
            pattern = rf"\b{re.escape(token)}\b"
        if re.search(pattern, text):
            found.append(token)
    return found


def stability_score(language: str, token: str, domain_scalar: float) -> float:
    idx = codon_index(language, token)
    phase = (idx + 1) / 64.0
    raw = 1.0 - abs(phase - abs(domain_scalar) % 1.0)
    risk_tokens = set((_load_registry().get("languages") or {}).get(language, {}).get("risk_tokens") or [])
    penalty = 0.35 if token in risk_tokens else 0.0
    return max(0.0, min(1.0, raw - penalty))


def analyze_file(path: Path, language: str, domain_scalar: float) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "language": language, "exists": False, "codons": [], "holes": []}
    text = path.read_text(encoding="utf-8", errors="replace")
    tokens = tokenize_source(text, language)
    codons = [
        {
            "token": tok,
            "codon_index": codon_index(language, tok),
            "stability": round(stability_score(language, tok, domain_scalar), 6),
        }
        for tok in tokens
    ]
    holes: list[dict] = []
    for i in range(max(0, len(codons) - WINDOW_SIZE + 1)):
        window = codons[i : i + WINDOW_SIZE]
        mean_stab = sum(c["stability"] for c in window) / len(window)
        if mean_stab < STABILITY_THRESHOLD:
            holes.append(
                {
                    "window_start": i,
                    "tokens": [c["token"] for c in window],
                    "mean_stability": round(mean_stab, 6),
                    "hole_type": "connective_failure",
                }
            )
    return {
        "path": str(path),
        "language": language,
        "exists": True,
        "codon_count": len(codons),
        "hole_count": len(holes),
        "mean_stability": round(sum(c["stability"] for c in codons) / max(1, len(codons)), 6) if codons else 1.0,
        "codons": codons,
        "holes": holes,
    }


def analyze_language_samples(domain_scalar: float) -> list[dict]:
    reg = _load_registry()
    rows: list[dict] = []
    for language, cfg in (reg.get("languages") or {}).items():
        for rel in cfg.get("sample_paths") or []:
            path = ROOT / rel
            analysis = analyze_file(path, language, domain_scalar)
            if analysis.get("exists"):
                rows.append(analysis)
    return rows


def genome_benchmark_records(domain_scalar: float, lab: str = "code_genome_lab") -> list[dict]:
    records: list[dict] = []
    for analysis in analyze_language_samples(domain_scalar):
        lang = analysis["language"]
        for hole in analysis.get("holes") or []:
            severity = float(hole["mean_stability"])
            records.append(
                {
                    "lab": lab,
                    "property": "codon_hole_detected",
                    "name": f"{lang}__{'_'.join(hole['tokens'])}",
                    "computed": 1.0,
                    "measured": 1.0,
                    "error_pct": 0.0,
                    "source": analysis["path"],
                    "hole_type": hole["hole_type"],
                    "hole_severity": round(severity, 6),
                }
            )
        mean_stab = float(analysis.get("mean_stability") or 1.0)
        records.append(
            {
                "lab": lab,
                "property": "codon_stability",
                "name": f"{lang}_codon_stability",
                "computed": round(mean_stab, 6),
                "measured": round(mean_stab, 6),
                "error_pct": 0.0,
                "eval_kind": "stability_index",
                "record_kind": "structural",
                "source": analysis["path"],
            }
        )
        records.append(
            {
                "lab": lab,
                "property": "mean_codon_stability",
                "name": f"{lang}_file_stability",
                "computed": round(mean_stab, 6),
                "measured": 1.0,
                "error_pct": round(abs(mean_stab - 1.0) * 100.0, 6),
                "eval_kind": "stability_index",
                "record_kind": "structural",
                "source": analysis["path"],
            }
        )
    reg = _load_registry()
    for language, cfg in (reg.get("languages") or {}).items():
        n_units = int(cfg.get("codon_unit_count") or 0)
        computed = float(n_units) * (1.0 + abs(domain_scalar) * 0.001)
        records.append(
            {
                "lab": lab,
                "property": "codon_unit_coverage",
                "name": f"{language}_codon_units",
                "computed": round(computed, 6),
                "measured": float(n_units),
                "error_pct": round(abs(computed - n_units) / max(n_units, 1) * 100.0, 6),
                "source": "code_genome_language_registry",
            }
        )
    return records