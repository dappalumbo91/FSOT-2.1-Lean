# FSOT Mathlib re-derivation campaign (Windows helper)
# Usage:
#   .\scripts\run_mathlib_rederivation_campaign.ps1
#   .\scripts\run_mathlib_rederivation_campaign.ps1 -EngineOnly
#   .\scripts\run_mathlib_rederivation_campaign.ps1 -Wave W2_theorems
param(
    [switch]$EngineOnly,
    [string]$Wave = "",
    [switch]$SkipLake,
    [switch]$SkipAux
)
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root
$pyArgs = @("scripts/run_mathlib_rederivation_campaign.py")
if ($EngineOnly) { $pyArgs += "--engine-only" }
if ($Wave) { $pyArgs += @("--wave", $Wave) }
if ($SkipLake) { $pyArgs += "--skip-lake" }
if ($SkipAux) { $pyArgs += "--skip-aux" }
Write-Host "Running: python $($pyArgs -join ' ')"
& python @pyArgs
exit $LASTEXITCODE
