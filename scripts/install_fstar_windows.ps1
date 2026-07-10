# Tier 86 — install F* Windows binary release (no account required).
param(
    [string]$InstallRoot = "$env:USERPROFILE\tools\fstar-v2026.07.05",
    [string]$Version = "v2026.07.05"
)

$ErrorActionPreference = "Stop"
$zipUrl = "https://github.com/FStarLang/FStar/releases/download/$Version/fstar-$Version-Windows_NT-x86_64.zip"
$zipPath = Join-Path $env:TEMP "fstar-win.zip"

if (Test-Path (Join-Path $InstallRoot "bin\fstar.exe")) {
    Write-Host "F* already installed at $InstallRoot"
    exit 0
}

New-Item -ItemType Directory -Force -Path (Split-Path $InstallRoot) | Out-Null
Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath (Split-Path $InstallRoot) -Force
$extracted = Get-ChildItem (Split-Path $InstallRoot) -Directory | Where-Object { $_.Name -like "fstar*" } | Select-Object -First 1
if ($extracted -and $extracted.FullName -ne $InstallRoot) {
    if (Test-Path $InstallRoot) { Remove-Item $InstallRoot -Recurse -Force }
    Rename-Item $extracted.FullName $InstallRoot
}

$bin = Join-Path $InstallRoot "bin"
Write-Host "Installed F* to $InstallRoot"
Write-Host "Add to PATH: $bin"
Write-Host "Or set FSTAR_HOME=$InstallRoot"
& (Join-Path $bin "fstar.exe") --version