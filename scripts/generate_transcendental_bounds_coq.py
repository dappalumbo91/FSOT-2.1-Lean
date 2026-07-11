#!/usr/bin/env python3
"""Generate Tier 83 Coq transcendental bounds artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcendental_bounds_lib import (  # noqa: E402
    coq_certified_axioms,
    coq_proof_for,
    gen_coq_base,
    write_obligations_json,
)

OBL = ROOT / "verification" / "obligations" / "transcendental_bounds.json"
COQ_DIR = ROOT / "verification" / "coq"
CHUNK_SIZE = 25


def main() -> int:
    doc = write_obligations_json()
    obligations: list[dict] = doc["obligations"]

    (COQ_DIR / "TranscendentalBoundsBase.v").write_text(gen_coq_base(), encoding="utf-8")

    axioms = coq_certified_axioms(obligations)
    cert_header = [
        "From Stdlib Require Import Reals.",
        "From Stdlib Require Import Rpower.",
        "From Stdlib Require Import Rtrigo1.",
        "Local Open Scope R_scope.",
        "",
    ]
    (COQ_DIR / "TranscendentalBoundsCert.v").write_text(
        "\n".join(cert_header + axioms + [""]),
        encoding="utf-8",
    )

    for old in COQ_DIR.glob("TranscendentalBounds_*.v"):
        if old.name not in ("TranscendentalBoundsBase.v", "TranscendentalBoundsCert.v"):
            old.unlink()

    chunks = [obligations[i : i + CHUNK_SIZE] for i in range(0, len(obligations), CHUNK_SIZE)]
    chunk_files: list[str] = [
        "ConnectiveSpine.v",
        "TranscendentalBoundsBase.v",
        "TranscendentalBoundsCert.v",
    ]
    for idx, chunk in enumerate(chunks):
        name = f"TranscendentalBounds_{idx:02d}"
        lines = [
            f"(* FSOT Tier 83 — transcendental bounds chunk {idx + 1}/{len(chunks)} (generated). *)",
            f"Require Import {name.replace('_0', '_0').split('_')[0]}TranscendentalBoundsBase.",
        ]
        # Fix import - use relative names
        lines = [
            f"(* FSOT Tier 83 — transcendental bounds chunk {idx + 1}/{len(chunks)} (generated). *)",
            "From Stdlib Require Import Reals.",
            "Require Import TranscendentalBoundsBase.",
            "Require Import TranscendentalBoundsCert.",
            "From Stdlib Require Import Psatz.",
            "Local Open Scope R_scope.",
            "",
        ]
        for ob in chunk:
            lines += [f"Lemma {ob['id']} : {ob['coq_statement']}.", "Proof.", coq_proof_for(ob), "Qed.", ""]
        path = COQ_DIR / f"{name}.v"
        path.write_text("\n".join(lines), encoding="utf-8")
        chunk_files.append(path.name)
        print(f"Wrote {path} ({len(chunk)} obligations)")

    project = COQ_DIR / "_CoqProject"
    existing = project.read_text(encoding="utf-8").splitlines() if project.exists() else []
    spine = [ln for ln in existing if ln in ("ConnectiveSpine.v", "StructuralProofSpine.v") or ln.startswith("FullFormalSpine_")]
    if "StructuralProofSpine.v" not in spine and (COQ_DIR / "StructuralProofSpine.v").exists():
        spine.insert(1 if "ConnectiveSpine.v" in spine else 0, "StructuralProofSpine.v")
    transcendental = [
        "TranscendentalBoundsNative.v",
        "TranscendentalBoundsBase.v",
        "TranscendentalBoundsCert.v",
    ]
    transcendental += sorted(p.name for p in COQ_DIR.glob("TranscendentalBounds_[0-9]*.v"))
    project.write_text("\n".join(["-R .", *spine, *transcendental]) + "\n", encoding="utf-8")
    print(f"Updated _CoqProject ({len(transcendental)} transcendental files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())