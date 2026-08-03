# Local verification tools

Downloaded by:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_verification_tools.ps1
# optional permanent PATH:
powershell -ExecutionPolicy Bypass -File scripts/setup_verification_tools.ps1 -PersistUserPath
```

| Tool | Location (after setup) |
|------|------------------------|
| Z3 | `tools/z3/**/bin/z3.exe` |
| CVC5 | `tools/cvc5/**/bin/cvc5.exe` |
| TLA+/TLC | `tools/tla/tla2tools.jar` + `tlc.cmd` |
| F* | Portable `I:\...\fstar` or `FSTAR_HOME` (not always under `tools/`) |
| Isabelle | Desktop `Isabelle2025-2` (detected by cross-proof runner) |
| Coq/Rocq | Platform install (already on PATH if coqc works) |
| Lean | elan/lake |

Binaries are **gitignored**. Re-run the setup script on a fresh machine.
