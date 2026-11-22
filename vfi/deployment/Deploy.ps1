$ErrorActionPreference = 'Stop'
$taskApp = Split-Path -Parent $PSScriptRoot
# Shell scripts must retain LF endings when edited on Windows.
Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.sh' -File | ForEach-Object {
    $taskShellText = [System.IO.File]::ReadAllText($_.FullName).Replace("`r`n", "`n")
    [System.IO.File]::WriteAllText($_.FullName, $taskShellText, [System.Text.UTF8Encoding]::new($false))
}
$taskPrivate = Join-Path $taskApp '.private'
New-Item -ItemType Directory -Path $taskPrivate -Force | Out-Null
$taskBundle = Join-Path $taskPrivate 'vfi-simulation-source.tar.gz'
$taskFiles = @(Get-ChildItem -LiteralPath $taskApp -File | Where-Object {
    $_.Extension -in @('.py','.jsx','.js','.css','.html','.json') -or
    $_.Name -in @('Dockerfile','compose.yaml','requirements.txt','.dockerignore','.gitignore','README.md','AGENTS.md')
} | Select-Object -ExpandProperty Name)
$taskFiles += @('public','specifications','deployment','assets')
& tar -czf $taskBundle -C $taskApp @taskFiles
if ($LASTEXITCODE -ne 0) { throw 'Local packaging failed.' }
Write-Host 'Uploading the app source and deployment script to Keeper.'
& scp $taskBundle 'keeper:/tmp/vfi-simulation-source.tar.gz'
if ($LASTEXITCODE -ne 0) { throw 'Source upload failed.' }
& scp (Join-Path $PSScriptRoot 'keeper-deploy.sh') 'keeper:/tmp/vfi-simulation-deploy.sh'
if ($LASTEXITCODE -ne 0) { throw 'Deployment script upload failed.' }
& ssh -t keeper 'bash /tmp/vfi-simulation-deploy.sh'
if ($LASTEXITCODE -ne 0) { throw 'Deployment stopped. Read the server error above.' }
