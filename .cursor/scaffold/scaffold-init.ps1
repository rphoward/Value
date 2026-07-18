# Initialize a scaffolded repo: read manifest, retarget slug, optional git, verify tests.
param(
    [string]$ProductSlug,
    [string]$GitHubRemote,
    [switch]$InitGit,
    [switch]$SkipVerify,
    [switch]$UseGh
)

$ErrorActionPreference = "Stop"
$scaffoldDir = $PSScriptRoot
$repoRoot = Split-Path -Parent (Split-Path -Parent $scaffoldDir)
Set-Location $repoRoot

$manifestPath = Join-Path $scaffoldDir "manifest.json"
if (-not (Test-Path $manifestPath)) {
    throw "missing .cursor/scaffold/manifest.json"
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$sourceSlug = $manifest.product_slug
if ($ProductSlug) {
    $targetSlug = $ProductSlug
} elseif ($sourceSlug -eq "CHANGEME") {
    throw "-ProductSlug is required when manifest.json has product_slug CHANGEME"
} else {
    $targetSlug = $sourceSlug
}

if ($sourceSlug -eq $targetSlug) {
    Write-Host "product slug unchanged ($targetSlug); skipping retarget"
} else {
    $retargetArgs = @(
        (Join-Path $scaffoldDir "retarget.py"),
        "--from", $sourceSlug,
        "--to", $targetSlug,
        "--repo-root", $repoRoot
    )
    if ($GitHubRemote) {
        $retargetArgs += @("--github-remote", $GitHubRemote)
    }
    & python @retargetArgs
    if ($LASTEXITCODE -ne 0) {
        throw "retarget.py failed with exit code $LASTEXITCODE"
    }
}

if ($InitGit) {
    if (-not (Test-Path (Join-Path $repoRoot ".git"))) {
        git init $repoRoot | Out-Host
    }
    if (-not (Test-Path (Join-Path $repoRoot ".gitignore"))) {
        throw "missing .gitignore (required for InitGit)"
    }
}

$remoteUrl = $GitHubRemote
if (-not $remoteUrl -and $manifest.github_remote) {
    $remoteUrl = $manifest.github_remote
}
if ($remoteUrl) {
    $remotes = git -C $repoRoot remote
    if (-not ($remotes -match "^origin$")) {
        git -C $repoRoot remote add origin $remoteUrl | Out-Host
    }
}

if ($UseGh -and $remoteUrl) {
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        gh repo create $targetSlug --source $repoRoot --remote origin --push 2>$null
    } else {
        Write-Warning "gh not found; skipping gh repo create"
    }
}

if (-not $SkipVerify) {
    pip install -e . | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "pip install -e . failed"
    }
    $env:PYTHONPATH = "src"
    python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) {
        throw "unittest discover failed"
    }
}

Write-Host "scaffold-init complete for $targetSlug"
