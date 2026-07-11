# Tier 88 — install ESP32 flash tooling (no account required).
# Requires esp rustup toolchain: rustup toolchain install esp

Write-Host "Installing espflash (Tier 88 ESP32 harness)..."
cargo install espflash --locked
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$export = Join-Path $env:USERPROFILE "export-esp.ps1"
if (-not (Test-Path $export)) {
    Write-Host "export-esp.ps1 not found — run: espup install"
    exit 1
}

Write-Host "Sourcing $export before ESP32 builds..."
. $export
Write-Host "espflash: $(espflash --version)"
Write-Host "Tier 88 ESP32 tooling ready."