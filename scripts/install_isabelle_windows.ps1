# Install Isabelle on Windows - free, no account required.
# Run: powershell -ExecutionPolicy Bypass -File scripts/install_isabelle_windows.ps1

$ErrorActionPreference = "Stop"
$InstallRoot = "C:\Isabelle"
$Downloads = Join-Path $env:USERPROFILE "Downloads"
$InstallerName = "Isabelle2025-2.exe"

$existing = Get-ChildItem -Path $InstallRoot, "$env:USERPROFILE\Isabelle*", "$env:USERPROFILE\Desktop\Isabelle*" -ErrorAction SilentlyContinue |
    Where-Object { $_.PSIsContainer } | Select-Object -First 1
if ($existing) {
    $bin = Get-ChildItem -Path $existing.FullName -Recurse -Filter "isabelle.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($bin) {
        Write-Host "Isabelle already present: $($bin.FullName)"
        $binDir = $bin.Directory.FullName
        $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
        if ($userPath -notlike "*$binDir*") {
            [Environment]::SetEnvironmentVariable("Path", "$userPath;$binDir", "User")
        }
        & $bin.FullName version
        exit 0
    }
}

$urls = @(
    "https://isabelle.in.tum.de/dist/$InstallerName",
    "https://mirror.clarkson.edu/isabelle/dist/$InstallerName"
)

$dest = Join-Path $Downloads $InstallerName
$downloaded = $false

foreach ($url in $urls) {
    Write-Host "Trying $url ..."
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $url -OutFile $dest -MaximumRedirection 10 -TimeoutSec 600 -UseBasicParsing
        if ((Test-Path $dest) -and ((Get-Item $dest).Length -gt 100000000)) {
            $downloaded = $true
            break
        }
    } catch {
        Write-Host "  failed: $($_.Exception.Message)"
    }
}

if (-not $downloaded) {
    Write-Host ""
    Write-Host "AUTO-DOWNLOAD FAILED."
    Write-Host "Manual: https://isabelle.in.tum.de/ -> download $InstallerName (~600MB)"
    Write-Host "Save to: $dest then re-run this script."
    if (Test-Path $dest) {
        $sz = (Get-Item $dest).Length
        Write-Host "Found $dest size=$sz (too small if under 100MB)"
    }
    exit 1
}

$sizeMb = [math]::Round((Get-Item $dest).Length / 1MB, 1)
Write-Host "Installer: $dest (${sizeMb} MB)"
New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null
$proc = Start-Process -FilePath $dest -ArgumentList "-q", "-d", $InstallRoot -Wait -PassThru
if ($proc.ExitCode -ne 0) {
    throw "Isabelle installer exit code $($proc.ExitCode)"
}

$searchRoots = @($InstallRoot, "$env:USERPROFILE\Desktop")
$bin = $null
foreach ($root in $searchRoots) {
    if (-not (Test-Path $root)) { continue }
    $bin = Get-ChildItem -Path $root -Recurse -Filter "isabelle.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($bin) { break }
    $sh = Get-ChildItem -Path $root -Recurse -Filter "isabelle" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -like "*\bin\isabelle" } | Select-Object -First 1
    if ($sh) {
        Write-Host "Installed (Cygwin wrapper): $($sh.FullName)"
        Write-Host "Isabelle home: $($sh.Directory.Parent.FullName)"
        exit 0
    }
}
if (-not $bin) {
    throw "isabelle not found under $InstallRoot or Desktop"
}

$binDir = $bin.Directory.FullName
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$binDir", "User")
}
Write-Host "Installed: $($bin.FullName)"
& $bin.FullName version
Write-Host "Run: python scripts/run_cross_proof_verification.py"