# Millennium measured-compare lab

**Pin:** AEB2AD · Public Apache-2.0:
[https://github.com/dappalumbo91/fsot-millennium-measured](https://github.com/dappalumbo91/fsot-millennium-measured)

FSOT 2.1 (`dappalumbo91/FSOT-2.1-Lean`) is the authority. This sibling vendors the
millenium / uniqueness slice so a clean clone can reproduce the stamp. Findings
migrate back. Not a Clay Prize. Do not rewrite the H0 freeze.

**What this lab is for:** compute the *function* each millenium question was
pointing at, against observables, without depending on Clay’s frozen formula
being the unique encoding. Full argument:
[`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md).

## Reproduce

```powershell
git clone https://github.com/dappalumbo91/fsot-millennium-measured.git
cd fsot-millennium-measured
pip install -r requirements.txt
python scripts/reproduce.py
python scripts/plot_millennium_panels.py
```

`reproduce.py` is the gauntlet (track, accuracy, measured compares, uniqueness).
The plotter is extra (needs matplotlib) and writes `results/figures/`.

## Layout

| Path | Role |
|------|------|
| `vendor/fsot_millennium_*.py`, `fsot_nse3d.py`, `fsot_seed_flavor.py` | Functions |
| `measured/run_compares.py` | 3D TG, Sha 17/17, χ 9/9 |
| `verification/` | Lean / Coq / Isabelle / F* / Rust / SMT / TLA |
| `docs/FUNCTION_NOT_FORMULA.md` | Asked vs function vs FSOT |
| `docs/HOW_THESE_ARE_DEPICTED.md` | Conventional pictures vs panels |
| `docs/FINDINGS.md` | Review and improvement areas |

Clay remaining: 6. Uniqueness in this repo: 147 obligations.
