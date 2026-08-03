# Local mirror of .github/workflows/ci.yml (margin + TOE + tier + smoke).
# Use when GitHub Actions cannot start runners (billing lock, etc.).
# Exit 0 only if all hard gates pass.
param(
    [switch]$SkipNavigator,
    [switch]$SkipContested
)

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

function Step([string]$Name, [scriptblock]$Block) {
    Write-Host "`n=== $Name ===" -ForegroundColor Cyan
    & $Block
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
        throw "Step failed: $Name (exit $LASTEXITCODE)"
    }
}

Write-Host "FSOT local CI  root=$Root" -ForegroundColor Green

Step "Benchmark margin audit" {
    python scripts/audit_all_benchmark_margins.py
}

Step "Assert zero green-gate failures" {
    python -c @"
import json, sys
m = json.load(open('data/benchmark_margin_audit.json', encoding='utf-8'))
fail = m.get('green_gate_fail_count')
fail = int(fail) if fail is not None else -1
n = m.get('benchmark_file_count')
n = int(n) if n is not None else 0
print(f'green {n - max(fail, 0)}/{n} fail={fail}')
if fail != 0:
    print('FAIL', m.get('green_gate_failures'))
    sys.exit(1)
"@
}

Step "Tier scalar aspiration" {
    python scripts/build_tier_scalar_precision_closure.py
}

Step "Assert tier_scalar closed" {
    python -c @"
import json, sys
s = json.load(open('data/tier_scalar_precision_closure.json', encoding='utf-8'))
print('tier_scalar closed=', s.get('closed'), 'fails=', s.get('tier_scalar_fail_count'))
if not s.get('closed'):
    print(s.get('failing_domains'))
    sys.exit(1)
"@
}

Step "TOE gap closure" {
    python scripts/build_toe_gap_closure.py
}

Step "Assert Label A and Label B" {
    python -c @"
import json, sys
t = json.load(open('data/toe_gap_closure_report.json', encoding='utf-8'))
e = t.get('evaluation') or {}
print('Label A', e.get('label_A_empirical_framework'))
print('Label B', e.get('label_B_classical_toe'))
for k, v in (e.get('criteria') or {}).items():
    print(f'  {k}: {v.get(\"pass\")}')
if not e.get('label_A_empirical_framework') or not e.get('label_B_classical_toe'):
    sys.exit(1)
"@
}

if (-not $SkipNavigator) {
    Step "Domain navigator build" {
        python scripts/build_fsot_domain_navigator_db.py
    }
}

if (-not $SkipContested) {
    Step "Contested observables closure" {
        python scripts/build_contested_observables_closure.py
    }
}

if (Test-Path scripts/audit_parameter_count.py) {
    Step "Parameter honesty audit" {
        python scripts/audit_parameter_count.py
    }
}

Write-Host "`n=== LOCAL CI PASS ===" -ForegroundColor Green
exit 0
