#!/usr/bin/env python3
"""Generate Tier 83 Isabelle transcendental bounds artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import (  # noqa: E402
    gen_isabelle_root,
    isabelle_transcendental_parent_sessions,
    isabelle_transcendental_theory_prefix,
)
from transcendental_bounds_lib import (  # noqa: E402
    gen_isabelle_base,
    isabelle_certified_axioms,
    isabelle_proof_for,
    write_obligations_json,
)

ISA_DIR = ROOT / "verification" / "isabelle"
CHUNK_SIZE = 25


def main() -> int:
    doc = write_obligations_json()
    obligations: list[dict] = doc["obligations"]

    native_script = ROOT / "scripts" / "gen_transcendental_native_isabelle.py"
    if native_script.exists():
        subprocess.run([sys.executable, str(native_script)], cwd=str(ROOT), check=False)

    base = gen_isabelle_base()
    cert_axioms = isabelle_certified_axioms(obligations)
    cert_theory = [
        "(* FSOT Tier 83 — pointwise transcendental certificates. *)",
        "theory TranscendentalBoundsCert",
        "imports TranscendentalBoundsBase",
        "begin",
        "",
        *cert_axioms,
        "",
        "end",
        "",
    ]
    (ISA_DIR / "TranscendentalBoundsBase.thy").write_text(base, encoding="utf-8")
    (ISA_DIR / "TranscendentalBoundsCert.thy").write_text("\n".join(cert_theory), encoding="utf-8")

    for old in ISA_DIR.glob("TranscendentalBounds_*.thy"):
        if old.name not in ("TranscendentalBoundsBase.thy", "TranscendentalBoundsCert.thy"):
            old.unlink()

    chunks = [obligations[i : i + CHUNK_SIZE] for i in range(0, len(obligations), CHUNK_SIZE)]
    theory_names = ["ConnectiveSpine", *isabelle_transcendental_theory_prefix()]
    for idx, chunk in enumerate(chunks):
        theory = f"TranscendentalBounds_{idx:02d}"
        lines = [
            f"(* FSOT Tier 83 — transcendental bounds chunk {idx + 1}/{len(chunks)} (generated). *)",
            f"theory {theory}",
            "imports TranscendentalBoundsCert",
            "begin",
            "",
        ]
        for ob in chunk:
            lines += [
                f'lemma {ob["id"]}: "{ob["isabelle_statement"]}"',
                f"  {isabelle_proof_for(ob)}",
                "",
            ]
        lines += ["end", ""]
        path = ISA_DIR / f"{theory}.thy"
        path.write_text("\n".join(lines), encoding="utf-8")
        theory_names.append(theory)
        print(f"Wrote {path} ({len(chunk)} obligations)")

    formal = [p.stem for p in sorted(ISA_DIR.glob("FullFormalSpine_*.thy"))]
    theory_names += formal
    (ISA_DIR / "ROOT").write_text(
        gen_isabelle_root(
            theory_names,
            description=f"FSOT Tier 83 cross-proof ({len(theory_names)} theories)",
            parent_sessions=isabelle_transcendental_parent_sessions(),
        ),
        encoding="utf-8",
    )
    print(f"Updated ROOT ({len(theory_names)} theories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())