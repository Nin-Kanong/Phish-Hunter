$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Apps = @('frontend/app', 'frontend/network-artifacts')
foreach ($App in $Apps) {
    Write-Host "==> Building $App"
    Push-Location (Join-Path $Root $App)
    try {
        if (Test-Path 'package-lock.json') {
            npm ci --no-audit --no-fund
        } else {
            npm install --no-audit --no-fund
        }
        if ($LASTEXITCODE -ne 0) { throw "npm dependency installation failed for $App" }
        npm run build
        if ($LASTEXITCODE -ne 0) { throw "npm run build failed for $App" }
    } finally { Pop-Location }
}
Write-Host 'Frontend builds completed.'
