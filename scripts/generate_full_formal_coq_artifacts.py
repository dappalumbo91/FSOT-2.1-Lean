#!/usr/bin/env python3
"""Generate chunked Coq artifacts from full_formal_spine.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import gen_coq_chunk, obligation_margin_violation, obligation_provable  # noqa: E402

OBL = ROOT / "verification" / "obligations" / "full_formal_spine.json"
COQ_DIR = ROOT / "verification" / "coq"
MARGIN_OUT = ROOT / "verification" / "obligations" / "margin_violations.json"
CHUNK_SIZE = 100


def main() -> int:
    doc = json.loads(OBL.read_text(encoding="utf-8"))
    all_obligations: list[dict] = doc["obligations"]
    if not all_obligations:
        print("No obligations in full_formal_spine.json", file=sys.stderr)
        return 1

    atomic = [ob for ob in all_obligations if ob.get("kind") != "bundle_conj"]
    provable: list[dict] = []
    violations: list[dict] = []
    for ob in atomic:
        v = obligation_margin_violation(ob)
        if v is None:
            provable.append(ob)
        else:
            violations.append({**ob, "margin_violation": v})

    MARGIN_OUT.write_text(
        json.dumps(
            {
                "count": len(violations),
                "obligations": violations,
                "note": "False inequalities — excluded from Coq proof generation.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {MARGIN_OUT} ({len(violations)} margin violations, {len(provable)} provable)")

    for old in COQ_DIR.glob("FullFormalSpine_*.v"):
        old.unlink()
    for old in COQ_DIR.glob("FullPriorsSpine_*.v"):
        old.unlink()

    chunks = [provable[i : i + CHUNK_SIZE] for i in range(0, len(provable), CHUNK_SIZE)]
    chunk_files: list[str] = ["ConnectiveSpine.v"]
    for idx, chunk in enumerate(chunks):
        name = f"FullFormalSpine_{idx:02d}.v"
        path = COQ_DIR / name
        path.write_text(gen_coq_chunk(chunk, idx, len(chunks), "FullFormalSpine"), encoding="utf-8")
        chunk_files.append(name)
        print(f"Wrote {path} ({len(chunk)} obligations)")

    project_lines = ["-R .", *chunk_files, ""]
    (COQ_DIR / "_CoqProject").write_text("\n".join(project_lines), encoding="utf-8")
    print(f"Updated _CoqProject ({len(chunks)} formal chunks, {len(provable)} provable obligations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())