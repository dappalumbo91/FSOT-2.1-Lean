# Tier 86 — install QEMU via winget (no account required).
$ErrorActionPreference = "Stop"

if (Get-Command qemu-system-x86_64 -ErrorAction SilentlyContinue) {
    qemu-system-x86_64 --version
    exit 0
}

winget install --id SoftwareFreedomConservancy.QEMU -e --accept-package-agreements --accept-source-agreements
Write-Host "QEMU installed. Restart shell or add QEMU to PATH if needed."
if (Get-Command qemu-system-x86_64 -ErrorAction SilentlyContinue) {
    qemu-system-x86_64 --version
}