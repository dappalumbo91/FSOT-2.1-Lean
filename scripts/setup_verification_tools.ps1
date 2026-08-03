# Install / wire open-source verification tools for FSOT-2.1-Lean.
# Lean · Coq · Isabelle · F* · Z3 · CVC5 · TLA+/TLC · Rust
#
# Usage (from repo root or any cwd):
#   powershell -ExecutionPolicy Bypass -File scripts/setup_verification_tools.ps1
#   powershell -ExecutionPolicy Bypass -File scripts/setup_verification_tools.ps1 -PersistUserPath
#
param(
    [switch]$PersistUserPath,
    [switch]$SkipDownload
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -ErrorAction SilentlyContinue
# scripts/ is under repo root
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Tools = Join-Path $RepoRoot "tools"
New-Item -ItemType Directory -Force -Path $Tools | Out-Null

function Get-Z3Bin {
    Get-ChildItem (Join-Path $Tools "z3") -Recurse -Filter "z3.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}
function Get-Cvc5Bin {
    Get-ChildItem (Join-Path $Tools "cvc5") -Recurse -Filter "cvc5.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}

function Ensure-Z3 {
    $existing = Get-Z3Bin
    if ($existing) { Write-Host "Z3 OK: $existing"; return $existing }
    if ($SkipDownload) { Write-Host "Z3 missing (SkipDownload)"; return $null }
    Write-Host "Downloading Z3 4.15.4..."
    $zip = Join-Path $Tools "z3.zip"
    $url = "https://github.com/Z3Prover/z3/releases/download/z3-4.15.4/z3-4.15.4-x64-win.zip"
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    $dest = Join-Path $Tools "z3"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Expand-Archive -Path $zip -DestinationPath $dest -Force
    return (Get-Z3Bin)
}

function Ensure-Cvc5 {
    $existing = Get-Cvc5Bin
    if ($existing) { Write-Host "CVC5 OK: $existing"; return $existing }
    if ($SkipDownload) { Write-Host "CVC5 missing (SkipDownload)"; return $null }
    Write-Host "Downloading CVC5 1.2.1..."
    $zip = Join-Path $Tools "cvc5.zip"
    $url = "https://github.com/cvc5/cvc5/releases/download/cvc5-1.2.1/cvc5-Win64-x86_64-static.zip"
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    $dest = Join-Path $Tools "cvc5"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Expand-Archive -Path $zip -DestinationPath $dest -Force
    return (Get-Cvc5Bin)
}

function Ensure-Tla {
    $jar = Join-Path $Tools "tla\tla2tools.jar"
    $dir = Join-Path $Tools "tla"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    if (-not (Test-Path $jar)) {
        if ($SkipDownload) { Write-Host "TLA jar missing (SkipDownload)"; return $null }
        Write-Host "Downloading tla2tools.jar..."
        $url = "https://github.com/tlaplus/tlaplus/releases/download/v1.8.0/tla2tools.jar"
        Invoke-WebRequest -Uri $url -OutFile $jar -UseBasicParsing
    }
    # Wrappers so `tlc` resolves on PATH
    $tlcCmd = Join-Path $dir "tlc.cmd"
    $tlcBat = Join-Path $dir "tlc.bat"
    $wrapper = @"
@echo off
java -cp "%~dp0tla2tools.jar" tlc2.TLC %*
"@
    Set-Content -Path $tlcCmd -Value $wrapper -Encoding ASCII
    Set-Content -Path $tlcBat -Value $wrapper -Encoding ASCII
    Write-Host "TLA+/TLC OK: $jar"
    return $jar
}

function Resolve-FstarHome {
    $candidates = @(
        $env:FSTAR_HOME,
        "I:\FSOT-Physical-Archive\07_Portable-Toolchain\fstar",
        (Join-Path $env:USERPROFILE "tools\fstar-v2026.07.05"),
        (Join-Path $Tools "fstar")
    ) | Where-Object { $_ }
    foreach ($c in $candidates) {
        $exe = Join-Path $c "bin\fstar.exe"
        if (Test-Path $exe) { return $c }
    }
    return $null
}

function Resolve-IsabelleHome {
    $candidates = @(
        (Join-Path $env:USERPROFILE "Desktop\Isabelle2025-2"),
        (Join-Path $env:USERPROFILE "Desktop\Isabelle2024-1"),
        "C:\Isabelle2025-2",
        "C:\Program Files\Isabelle"
    )
    foreach ($c in $candidates) {
        if ((Test-Path (Join-Path $c "bin\isabelle")) -or (Test-Path (Join-Path $c "bin\isabelle.exe"))) {
            return $c
        }
    }
    # glob Desktop
    $desk = Join-Path $env:USERPROFILE "Desktop"
    if (Test-Path $desk) {
        $hit = Get-ChildItem $desk -Directory -Filter "Isabelle*" -ErrorAction SilentlyContinue |
            Sort-Object Name -Descending | Select-Object -First 1
        if ($hit) { return $hit.FullName }
    }
    return $null
}

Write-Host "=== FSOT verification tool setup ==="
Write-Host "Repo: $RepoRoot"
Write-Host "Tools: $Tools"

$z3 = Ensure-Z3
$cvc5 = Ensure-Cvc5
$null = Ensure-Tla
$fstarHome = Resolve-FstarHome
$isaHome = Resolve-IsabelleHome

# Python z3-solver (pip often writes progress to stderr — do not fail the script)
Write-Host "Ensuring Python z3-solver..."
$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
try {
    & python -m pip install --upgrade z3-solver 2>&1 | Select-Object -Last 8
} catch {
    Write-Host "pip z3-solver warning: $_"
}
$ErrorActionPreference = $prevEap

# Session PATH
$pathAdds = [System.Collections.Generic.List[string]]::new()
if ($z3) { $pathAdds.Add((Split-Path $z3)) }
if ($cvc5) { $pathAdds.Add((Split-Path $cvc5)) }
$pathAdds.Add((Join-Path $Tools "tla"))
if ($fstarHome) {
    $env:FSTAR_HOME = $fstarHome
    $pathAdds.Add((Join-Path $fstarHome "bin"))
    Write-Host "F* OK: $fstarHome"
} else {
    Write-Host "F* not found — run scripts/install_fstar_windows.ps1 or use I: portable toolchain"
}
if ($isaHome) {
    Write-Host "Isabelle OK: $isaHome"
} else {
    Write-Host "Isabelle not found on Desktop — install Isabelle2025 if needed"
}

# Prepend PATH for this process
$newPath = ($pathAdds + @($env:PATH)) -join ";"
$env:PATH = $newPath

if ($PersistUserPath) {
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if (-not $userPath) { $userPath = "" }
    $parts = $userPath -split ";" | Where-Object { $_ -and $_.Trim() }
    foreach ($p in $pathAdds) {
        if ($parts -notcontains $p) { $parts = @($p) + $parts }
    }
    $merged = ($parts -join ";")
    [Environment]::SetEnvironmentVariable("Path", $merged, "User")
    if ($fstarHome) {
        [Environment]::SetEnvironmentVariable("FSTAR_HOME", $fstarHome, "User")
    }
    Write-Host "Persisted User PATH + FSTAR_HOME (new terminals pick this up)."
}

# Write machine-local resolve map for Python runners
$map = @{
    generated_at = (Get-Date).ToUniversalTime().ToString("o")
    z3 = $z3
    cvc5 = $cvc5
    tla2tools_jar = (Join-Path $Tools "tla\tla2tools.jar")
    fstar_home = $fstarHome
    fstar_exe = if ($fstarHome) { Join-Path $fstarHome "bin\fstar.exe" } else { $null }
    isabelle_home = $isaHome
    tools_dir = $Tools
}
$mapPath = Join-Path $Tools "tool_paths.json"
$map | ConvertTo-Json | Set-Content -Path $mapPath -Encoding UTF8
Write-Host "Wrote $mapPath"

Write-Host ""
Write-Host "=== Smoke versions ==="
if ($z3) { & $z3 --version }
if ($cvc5) { & $cvc5 --version 2>&1 | Select-Object -First 2 }
if ($fstarHome) { & (Join-Path $fstarHome "bin\fstar.exe") --version 2>&1 | Select-Object -First 2 }
try { python -c "import z3; print('z3py', z3.get_version_string())" } catch { Write-Host "z3py fail: $_" }
try { java -cp (Join-Path $Tools "tla\tla2tools.jar") tlc2.TLC -h 2>&1 | Select-Object -First 3 } catch { Write-Host "tlc fail: $_" }
try { coqc --version 2>&1 | Select-Object -First 1 } catch { Write-Host "coqc: not on PATH" }
try { lake --version 2>&1 | Select-Object -First 1 } catch { Write-Host "lake: not on PATH" }
try { rustc --version 2>&1 } catch { Write-Host "rustc: not on PATH" }

Write-Host ""
Write-Host "Setup complete. Re-run verification with:"
Write-Host "  python scripts/run_smt_catalog_bounds.py"
Write-Host "  python scripts/run_tla_domain_routing_check.py"
Write-Host "  python scripts/run_fstar_verification.py"
Write-Host "  python scripts/run_cross_proof_verification.py"
