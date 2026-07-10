# Add Rocq Platform to user PATH (no admin, no account required).
$rocqBin = "C:\Rocq-Platform~9.0~2025.08\bin"
if (-not (Test-Path "$rocqBin\coqc.exe")) {
    Write-Error "coqc not found at $rocqBin — run: winget install Coq.CoqPlatform"
    exit 1
}
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$rocqBin*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$rocqBin", "User")
    Write-Host "Added to user PATH: $rocqBin"
} else {
    Write-Host "Already on user PATH: $rocqBin"
}
$env:Path = "$env:Path;$rocqBin"
coqc -v