# Local launcher for the Value spoke app.
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
$env:PYTHONPATH = "src"
uvicorn value.presentation.app:app --reload --host 127.0.0.1 --port 8000
