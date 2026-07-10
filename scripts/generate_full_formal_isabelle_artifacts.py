#!/usr/bin/env python3
"""Generate chunked Isabelle artifacts from full_formal_spine.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import (  # noqa: E402
    gen_isabelle_chunk,
    gen_isabelle_root,
    obligation_margin_violation,
    obligation_provable,
)

OBL = ROOT / "verification" / "obligations" / "full_formal_spine.json"
ISA_DIR = ROOT / "verification" / "isabelle"
CHUNK_SIZE = 100


def main() -> int:
    doc = json.loads(OBL.read_text(encoding="utf-8"))
    all_obligations: list[dict] = doc["obligations"]
    if not all_obligations:
        print("No obligations in full_formal_spine.json", file=sys.stderr)
        return 1

    provable = [ob for ob in all_obligations if obligation_provable(ob)]
    violations = [ob for ob in all_obligations if obligation_margin_violation(ob) is not None]
    print(f"Isabelle provable: {len(provable)} | margin violations excluded: {len(violations)}")

    for old in ISA_DIR.glob("FullFormalSpine_*.thy"):
        old.unlink()

    chunks = [provable[i : i + CHUNK_SIZE] for i in range(0, len(provable), CHUNK_SIZE)]
    theory_names = ["ConnectiveSpine"]
    for idx, chunk in enumerate(chunks):
        name = f"FullFormalSpine_{idx:02d}"
        path = ISA_DIR / f"{name}.thy"
        path.write_text(
            gen_isabelle_chunk(chunk, idx, len(chunks), theory_name=name),
            encoding="utf-8",
        )
        theory_names.append(name)
        print(f"Wrote {path} ({len(chunk)} obligations)")

    (ISA_DIR / "ROOT").write_text(gen_isabelle_root(theory_names), encoding="utf-8")
    print(
        f"Updated ROOT (session FSOT_CrossProof, {len(theory_names)} theories, "
        f"{len(provable)} provable obligations)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())