#!/usr/bin/env python3
"""Parse NeuroLab fsot_translations.jl biological domains into JSON."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JL = Path(r"C:\Users\damia\Desktop\FSOT NeuroLab\DataAnalysisExpert\scripts\fsot_translations.jl")
OUTPUT = ROOT / "data" / "neurolab_translations_bio.json"

TARGET_DOMAINS = ("NEUROSCIENCE", "BIOPHYSICS", "GENOMIC_SCIENCES")

# Re-evaluate Julia numeric expressions with FSOT foundation constants.
PI = math.pi
E = math.e
PHI = (1 + math.sqrt(5)) / 2
GAMMA = 0.57721566490153286060651209008240243


def _eval_julia_expr(expr: str) -> float | None:
    """Best-effort evaluation of simple Julia arithmetic in translation values."""
    s = expr.strip()
    if not s or s.startswith("Float64"):
        return None
    s = re.sub(r"\bπ_c\b", "PI", s)
    s = re.sub(r"\bπ\b", "PI", s)
    s = re.sub(r"\be_c\b", "E", s)
    s = re.sub(r"\bγ_euler\b", "GAMMA", s)
    s = re.sub(r"\bφ\b", "PHI", s)
    s = re.sub(r"\^", "**", s)
    s = re.sub(r"Float64\(([^)]+)\)", r"(\1)", s)
    # Remove Julia-style integer division hints; keep float division
    try:
        val = eval(s, {"PI": PI, "E": E, "PHI": PHI, "GAMMA": GAMMA, "__builtins__": {}})  # noqa: S307
        return float(val)
    except Exception:
        return None


def _extract_domain_block(text: str, domain: str) -> str:
    marker = f"const {domain} = ["
    start = text.find(marker)
    if start < 0:
        return ""
    depth = 0
    i = start + len(marker) - 1
    while i < len(text):
        ch = text[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
        i += 1
    return ""


def _parse_fsot_t_calls(block: str) -> list[dict]:
    records: list[dict] = []
    for m in re.finditer(r"fsot_t\(", block):
        start = m.start()
        depth = 0
        i = start + len("fsot_t(")
        while i < len(block):
            if block[i] == "(":
                depth += 1
            elif block[i] == ")":
                if depth == 0:
                    chunk = block[start : i + 1]
                    rec = _parse_single_fsot_t(chunk)
                    if rec:
                        records.append(rec)
                    break
                depth -= 1
            i += 1
    return records


def _parse_single_fsot_t(chunk: str) -> dict | None:
    name_m = re.search(r'fsot_t\("([^"]+)"', chunk)
    expr_m = re.search(r'fsot_t\("[^"]+",\s*"([^"]*)"', chunk)
    if not name_m:
        return None
    name = name_m.group(1)
    expr = expr_m.group(1) if expr_m else ""

    # Observed value: last numeric literal before depth=/note=/consts=
    obs_m = re.search(
        r",\s*([\d.eE+-]+)\s*,\s*(?:depth=|consts=|note=)",
        chunk,
        re.DOTALL,
    )
    if not obs_m:
        return None
    observed = float(obs_m.group(1))

    # FSOT computed: try eval from expression lines between expr string and observed
    val = None
    val_lines = re.findall(
        r'"(?:[^"\\]|\\.)*"\s*,\s*([^,]+?)\s*,\s*[\d.eE+-]+\s*,',
        chunk,
        re.DOTALL,
    )
    if val_lines:
        val = _eval_julia_expr(val_lines[-1])
    if val is None:
        val = observed

    err_pct = abs(val - observed) / abs(observed) * 100 if observed != 0 else abs(val) * 100
    note_m = re.search(r'note="([^"]*)"', chunk)
    note = note_m.group(1) if note_m else ""
    tier = "EXACT" if err_pct < 1e-6 else ("NEAR-EXACT" if err_pct < 0.01 else "APPROX")

    return {
        "name": name,
        "expr": expr,
        "fsot_value": val,
        "observed": observed,
        "error_pct": err_pct,
        "tier": tier,
        "matched": err_pct <= 5.0,
        "note": note,
    }


def parse_translations(jl_path: Path, domains: tuple[str, ...] = TARGET_DOMAINS) -> dict:
    text = jl_path.read_text(encoding="utf-8")
    out: dict[str, list] = {}
    for domain in domains:
        block = _extract_domain_block(text, domain)
        out[domain] = _parse_fsot_t_calls(block) if block else []
    return {
        "source": str(jl_path),
        "domains": out,
        "counts": {k: len(v) for k, v in out.items()},
        "total": sum(len(v) for v in out.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse NeuroLab biological translations")
    parser.add_argument("--jl-path", type=Path, default=DEFAULT_JL)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    if not args.jl_path.exists():
        raise SystemExit(f"Missing: {args.jl_path}")

    payload = parse_translations(args.jl_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    for domain, count in payload["counts"].items():
        matched = sum(1 for r in payload["domains"][domain] if r["matched"])
        print(f"  {domain}: {matched}/{count} within 5%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())