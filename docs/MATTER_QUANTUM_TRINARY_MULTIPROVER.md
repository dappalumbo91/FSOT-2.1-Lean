# Matter + Quantum/Trinary multiprover export

Wires new residual panels into the Lean/multiprover fabric (same pipeline as open frontiers / GR-SM).

## Panels

| Panel | Lean module | Domain |
|-------|-------------|--------|
| `data/matter_antimatter_benchmark.json` | `FSOT/Formal/MatterAntimatterPriors.lean` | Matter_Antimatter |
| `data/quantum_trinary_syntax_benchmark.json` | `FSOT/Formal/QuantumTrinarySyntaxPriors.lean` | Quantum_Trinary_Syntax |

## Commands

```powershell
python scripts/gen_matter_quantum_trinary_priors_lean.py
python scripts/run_matter_quantum_trinary_verification.py
```

That run:

1. Generates Lean priors  
2. Builds focused multiprover spine (Coq / Isabelle / SMT / Rust)  
3. Refreshes margin audit  
4. Re-exports **scientific catalog** + **full priors** spines  

## Artifacts

| Path | Role |
|------|------|
| `verification/obligations/matter_quantum_trinary_spine.json` | Focused obligations |
| `verification/coq/MatterQuantumTrinarySpine.v` | Coq |
| `verification/isabelle/MatterQuantumTrinarySpine.thy` | Isabelle |
| `verification/smt/matter_quantum_trinary_bounds.smt2` | Z3 |
| `verification/rust/fsot_matter_quantum_trinary_replay` | Rust f64 |
| `data/matter_quantum_trinary_verification_report.json` | overall_ok report |

## Honest scope

Numeric residual gates and count/D_eff identities.  
Not continuum Sakharov theorem; not full QI complexity theory.
