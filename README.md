# FSOT 2.0 Lean Formalization

**Fluid Spacetime Omni-Theory (FSOT) 2.0**

This is the Lean 4 formalization of **Fluid Spacetime Omni-Theory (FSOT) 2.0**, created and architected by **Damian Arthur Palumbo**.

It was developed in close collaboration with the Python reference implementation.

## Structure

- `FSOT/Scalar.lean` — Executable `Float`-based core (for the Python verification runner and quick checks). Includes extracted internal terms (`growth_term`, `quirk_mod`, `perceived_adjust`, `term3` + sub-components).

- `FSOT/Theorems.lean` — Theorems and Examples section (Float layer). Includes scaling proofs, `quirk_mod` case analysis, emergence/damping interpretation, quantitative dominance theorems, and documented `#eval` examples.

- `FSOT/Formal/` — Heavier `Real`-based proof layer (aligned with the attached `FSOT.Formal.*` files).
  - `Formal/Scalar.lean` — `Real` version of the core scalar engine.
  - `Formal/Theorems.lean` — Rigorous theorems using Mathlib analysis, with references to MC evidence and combustion triangulation from the attached files.

- `FSOT2_0_Compute.lean` — Executable entry point (run with `lake env lean FSOT2_0_Compute.lean`).

## Key Features

- **Extracted internal terms** for clean, rigorous proofs (`quirk_mod`, `growth_term`, `term3` sub-components, etc.).
- **Observer effect** (`quirk_mod`) formalized with case analysis.
- **Emergence vs Damping** interpretation theorems.
- **Quantitative dominance theorems** (when `term3` dominates Term1 + `quirk_mod`).
- **Examples section** with domain sweeps, observer intervention comparisons, stability delta style, and trinary collapse demos.
- Strong alignment with the attached reference files (`VibRegister.lean`, `RealData.lean`, `Domains.lean`, etc.), including MC + combustion justification in comments.

## Verification status (2026-06-20)

Full pipeline: `python scripts/fsot_verification_runner.py`

- **33 proved claims**, 0 active `sorry`, `lean_build_ok: true`
- Genomic exact identities (`FSOT.Formal.Genomic`)
- Brain component priors (`FSOT.Formal.BrainPriors`) — 10 NeuroLab components
- Protein amino-acid trinary phases (`FSOT.Formal.ProteinPriors`) — 20 canonical AAs, 10 distinct patterns ⊆ 27
- Certificate: `data/certificate.json` | Run log: `data/verification_runs.jsonl`

See `REPRODUCE.md` and `docs/genomic_brain_priors_verification.md` for details.

## Usage

```bash
pip install -r requirements.txt
python scripts/fsot_verification_runner.py

# Or Lean-only build
lake build FSOT.Formal.Genomic FSOT.Formal.BrainPriors FSOT.Formal.ProteinPriors FSOT.Formal.Lab
```

## Alignment with Reference Files

This project closely follows the structure and justification style of the attached reference files:
- Uses MC evidence and combustion triangulation anchors (from `VibRegister.lean`, `Domains.lean`, `RealData.lean`).
- Extracts internal terms for proof hygiene (similar to attached `Scalar.lean`).
- References `VibRegister` observer lemmas and stability proxies.
- Keeps a clean separation between executable (`Float`) and rigorous (`Real` + Mathlib analysis) layers.

## Next Steps / Roadmap

- Close remaining numeric `sorry` in `Formal/Theorems.lean` with tighter `nlinarith` using MC bounds.
- Port more observer lemmas from `VibRegister.lean`.
- Add combustion proxy theorems using `RealData` anchors.
- Expand Examples with full multi-step stability delta calculations on synthetic register data.

## License

Apache 2.0 (consistent with the reference implementation).
