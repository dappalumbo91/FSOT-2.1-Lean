# Fresh-clone reproducibility harness for FSOT-2.1-Lean
# Clones origin into a temp directory, installs deps, runs margin + TOE + optional bundle.
# Usage:
#   pwsh scripts/fresh_clone_repro.ps1
#   pwsh scripts/fresh_clone_repro.ps1 -SkipBundle
#   pwsh scripts/fresh_clone_repro.ps1 -OutDir D:\tmp\fsot-clone

param(
    [string]$RepoUrl = "https://github.com/dappalumbo91/FSOT-2.1-Lean.git",
    [string]$OutDir = "",
    [switch]$SkipBundle,
    [switch]$FullCrossProof
)

$ErrorActionPreference = "Stop"
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
if (-not $OutDir) {
    $OutDir = Join-Path $env:TEMP "fsot_fresh_clone_$stamp"
}

Write-Host "=== FSOT fresh-clone repro ===" -ForegroundColor Cyan
Write-Host "Repo: $RepoUrl"
Write-Host "Out:  $OutDir"

if (Test-Path $OutDir) {
    Write-Host "Removing existing OutDir..."
    Remove-Item -Recurse -Force $OutDir
}

git clone --depth 1 $RepoUrl $OutDir
Set-Location $OutDir

$commit = (git rev-parse HEAD).Trim()
Write-Host "Cloned commit: $commit"

python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "`n>>> audit_all_benchmark_margins.py" -ForegroundColor Yellow
python scripts/audit_all_benchmark_margins.py
if ($LASTEXITCODE -ne 0) { throw "margin audit failed" }

Write-Host "`n>>> build_tier_scalar_precision_closure.py" -ForegroundColor Yellow
python scripts/build_tier_scalar_precision_closure.py

Write-Host "`n>>> build_toe_gap_closure.py" -ForegroundColor Yellow
python scripts/build_toe_gap_closure.py
if ($LASTEXITCODE -ne 0) { throw "TOE gap closure failed" }

if (-not $SkipBundle) {
    Write-Host "`n>>> run_publication_verification_bundle.py" -ForegroundColor Yellow
    $bundleArgs = @("scripts/run_publication_verification_bundle.py")
    if ($FullCrossProof) { $bundleArgs += "--full-cross-proof" }
    python @bundleArgs
    if ($LASTEXITCODE -ne 0) { throw "publication bundle failed" }
}

# Gate summary (PowerShell-safe; no bash heredoc)
$gatePy = @'
import json, sys
from pathlib import Path

def load(p):
    path = Path(p)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

m = load("data/benchmark_margin_audit.json") or {}
t = load("data/toe_gap_closure_report.json") or {}
s = load("data/tier_scalar_precision_closure.json") or {}
c = load("data/cross_proof_verification_report.json") or {}
e = t.get("evaluation") or {}

# Note: fail_count can be 0 — do not use `or -1` (0 is falsy in Python).
_raw_fail = m.get("green_gate_fail_count")
fail = int(_raw_fail) if _raw_fail is not None else -1
_raw_n = m.get("benchmark_file_count")
n = int(_raw_n) if _raw_n is not None else 0
label_a = bool(e.get("label_A_empirical_framework"))
label_b = bool(e.get("label_B_classical_toe"))
tier_ok = bool(s.get("closed")) if s else False
cross_ok = c.get("overall_ok") if c else None

print("=== FRESH CLONE GATE SUMMARY ===")
print(f"green: {n - max(fail,0)}/{n} fail={fail}")
print(f"tier_scalar_closed: {tier_ok}")
print(f"Label A: {label_a}")
print(f"Label B: {label_b}")
print(f"cross overall_ok: {cross_ok}")

ok = fail == 0 and label_a and label_b and tier_ok
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
'@
$gatePy | Set-Content -Path "_gate_summary.py" -Encoding UTF8
python _gate_summary.py
Remove-Item _gate_summary.py -ErrorAction SilentlyContinue

$gate = $LASTEXITCODE
$report = @"
# Fresh-clone repro report

- **When:** $(Get-Date -Format o)
- **Repo:** $RepoUrl
- **Commit:** $commit
- **OutDir:** $OutDir
- **Gate exit:** $gate

## Commands run
1. ``git clone --depth 1``
2. ``pip install -r requirements.txt``
3. ``python scripts/audit_all_benchmark_margins.py``
4. ``python scripts/build_tier_scalar_precision_closure.py``
5. ``python scripts/build_toe_gap_closure.py``
$(if (-not $SkipBundle) { "6. ``python scripts/run_publication_verification_bundle.py``" } else { "6. publication bundle skipped" })

## Result
$(if ($gate -eq 0) { "**PASS** — green gate, tier aspiration, Label A + Label B." } else { "**FAIL** — see console output." })
"@

$reportPath = Join-Path $OutDir "CLEAN_CLONE_REPRO_REPORT.md"
$report | Set-Content -Path $reportPath -Encoding UTF8
Write-Host "`nReport: $reportPath" -ForegroundColor Cyan

# Also copy report next to calling repo if available
$caller = $PSScriptRoot
if ($caller) {
    $repoRoot = Split-Path $caller -Parent
    $dest = Join-Path $repoRoot "data\fresh_clone_repro_report.md"
    try {
        $report | Set-Content -Path $dest -Encoding UTF8
        Write-Host "Copied summary to $dest"
    } catch {
        Write-Host "Could not copy report to workspace: $_"
    }
}

exit $gate
