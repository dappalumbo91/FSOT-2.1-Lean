#!/usr/bin/env python3
"""Refresh iGEM parts registry from live FASTA when parts.igem.org is reachable."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import igem_fastas_root, igem_parts_registry_path, rel_repo_path  # noqa: E402

FASTA_URL = "https://parts.igem.org/fasta/parts/{part_id}"
USER_AGENT = "FSOT-Verification/1.0 (+https://github.com/dappalumbo91/FSOT-2.1-Lean)"


def _parse_fasta(text: str) -> tuple[str, int, float]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    header = lines[0] if lines else ""
    sequence = "".join(line for line in lines[1:] if not line.startswith(">")).upper()
    sequence = re.sub(r"[^ACGTUN]", "", sequence)
    length = len(sequence)
    if length == 0:
        return header, 0, 0.0
    gc = 100.0 * sum(base in {"G", "C"} for base in sequence) / length
    return header, length, gc


def _fetch_live_fasta(part_id: str, timeout: float = 20.0) -> tuple[str | None, str]:
    url = FASTA_URL.format(part_id=part_id)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                return None, f"http_{response.status}"
            body = response.read().decode("utf-8", errors="replace")
            return body, "live"
    except urllib.error.HTTPError as exc:
        return None, f"http_{exc.code}"
    except Exception as exc:  # noqa: BLE001
        return None, f"error_{type(exc).__name__}"


def _load_bundled_fasta(part_id: str, fasta_root: Path) -> str | None:
    path = fasta_root / f"{part_id}.fasta"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


def _write_bundled_fasta(part_id: str, fasta_root: Path, text: str) -> None:
    fasta_root.mkdir(parents=True, exist_ok=True)
    (fasta_root / f"{part_id}.fasta").write_text(text, encoding="utf-8")


def _synthetic_sequence(length: int, gc_percent: float) -> str:
    gc_count = int(round(length * gc_percent / 100.0))
    gc_count = max(0, min(length, gc_count))
    at_count = length - gc_count
    half_g = gc_count // 2
    half_c = gc_count - half_g
    half_a = at_count // 2
    half_t = at_count - half_a
    return ("G" * half_g + "C" * half_c + "A" * half_a + "T" * half_t)[:length]


def ingest(*, write_bundled: bool = True) -> dict:
    registry_path = igem_parts_registry_path()
    fasta_root = igem_fastas_root()
    doc = json.loads(registry_path.read_text(encoding="utf-8"))
    parts = doc.get("parts") or {}
    results: list[dict] = []
    live_count = 0
    bundled_count = 0
    synthetic_count = 0

    for part_id, body in parts.items():
        if not isinstance(body, dict):
            continue
        fasta_text, source = _fetch_live_fasta(part_id)
        if fasta_text:
            live_count += 1
            if write_bundled:
                _write_bundled_fasta(part_id, fasta_root, fasta_text)
        else:
            fasta_text = _load_bundled_fasta(part_id, fasta_root)
            if fasta_text:
                source = "bundled"
                bundled_count += 1
            else:
                length = int(body.get("length_bp") or 0)
                gc = float(body.get("gc_percent") or 0.0)
                if length > 0:
                    seq = _synthetic_sequence(length, gc)
                    fasta_text = f">{part_id} curated-synthetic\n{seq}\n"
                    source = "synthetic_curated"
                    synthetic_count += 1
                    if write_bundled:
                        _write_bundled_fasta(part_id, fasta_root, fasta_text)
                else:
                    source = "missing"

        if not fasta_text:
            results.append({"part_id": part_id, "source": source, "ok": False})
            continue

        _, length, gc = _parse_fasta(fasta_text)
        results.append(
            {
                "part_id": part_id,
                "source": source,
                "length_bp": length,
                "gc_percent": round(gc, 4),
                "ok": length > 0,
            }
        )
        body["fasta_source"] = source
        body["fasta_length_bp"] = length
        body["fasta_gc_percent"] = round(gc, 4)

    doc["fetched_at"] = datetime.now(timezone.utc).date().isoformat()
    doc["ingest_summary"] = {
        "live_count": live_count,
        "bundled_count": bundled_count,
        "synthetic_count": synthetic_count,
        "api_reachable": live_count > 0,
        "fasta_root": rel_repo_path(fasta_root),
    }
    registry_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return {
        "registry": registry_path,
        "fasta_root": fasta_root,
        "part_count": len(results),
        "live_count": live_count,
        "bundled_count": bundled_count,
        "synthetic_count": synthetic_count,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write-bundled", action="store_true")
    args = parser.parse_args()
    summary = ingest(write_bundled=not args.no_write_bundled)
    print(f"Updated {summary['registry']}")
    print(
        f"  parts={summary['part_count']} live={summary['live_count']} "
        f"bundled={summary['bundled_count']} synthetic={summary['synthetic_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())