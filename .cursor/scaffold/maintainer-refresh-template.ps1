# Twins repo only — NOT part of copy workflow; never run before copying .cursor/
# Refreshes CHANGEME manifest template for maintainer testing. Twins keeps twins values in git.
$ErrorActionPreference = "Stop"

$scaffoldDir = $PSScriptRoot
$manifestPath = Join-Path $scaffoldDir "manifest.json"

$manifestTemplate = @{
    product_slug = "CHANGEME"
    import_package = "CHANGEME"
    product_home = "src/CHANGEME/"
    github_remote = ""
    start_script = "tools/start-CHANGEME.ps1"
    uvicorn_target = "CHANGEME.presentation.app:app"
    profile = "full"
} | ConvertTo-Json -Depth 3
$manifestTemplate | Set-Content $manifestPath -Encoding utf8

Write-Host "refreshed CHANGEME template at $manifestPath"
Write-Host ""
Write-Host "Restore twins manifest when done: git checkout .cursor/scaffold/manifest.json"
