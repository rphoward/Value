param(
  [Parameter(Mandatory = $true)]
  [string]$Draft
)

$ErrorActionPreference = "Stop"
$draftPath = $Draft
if (-not [System.IO.Path]::IsPathRooted($draftPath)) {
  $draftPath = Join-Path (Get-Location) $Draft
}
$draftPath = (Resolve-Path $draftPath).Path

python (Join-Path $PSScriptRoot "smoke.py") $draftPath
exit $LASTEXITCODE
